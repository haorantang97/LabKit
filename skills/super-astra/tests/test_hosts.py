import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import hosts
import setup_rules
import setup_hook


class HostTests(unittest.TestCase):
    def test_rename_recognizes_old_hook_and_cursor_header(self):
        old = setup_hook.handler(ROOT / "config.json")
        old["statusMessage"] = "LabKit Welcome to AGI v2"
        other = {"type": "command", "command": "echo unrelated"}
        doc = {"hooks": {"UserPromptSubmit": [{"hooks": [old, other]}]}}
        updated = setup_hook.update(doc, ROOT / "config.json")
        items = [h for g in updated["hooks"]["UserPromptSubmit"] for h in g["hooks"]]
        self.assertEqual(len(items), 2)
        self.assertIn(other, items)
        self.assertEqual(sum(h.get("statusMessage") == "LabKit Super Astra v1" for h in items), 1)
        legacy = setup_rules.LEGACY_CURSOR_HEADER + setup_rules.BEGIN + "old body\n" + setup_rules.END
        refreshed = setup_rules.transform(legacy, "new body\n", "cursor")
        self.assertTrue(refreshed.startswith(setup_rules.CURSOR_HEADER))
        self.assertEqual(refreshed.count(setup_rules.BEGIN), 1)
        self.assertEqual(setup_rules.transform(legacy, "", "cursor", remove=True), setup_rules.LEGACY_CURSOR_HEADER)

    def test_rename_does_not_install_beside_legacy_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            old = project / ".agents/skills/welcome-to-agi"
            old.mkdir(parents=True)
            (old / "config.json").write_text("user customizations")
            result = self.run_script("install.py", "--host", "codex", "--project", project, "--apply")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((old.parent / "super-astra").exists())
            self.assertEqual((old / "config.json").read_text(), "user customizations")

    def run_script(self, script, *args, env=None):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
                              capture_output=True, text=True, env=env)

    def test_detection_requires_runtime_evidence_and_handles_conflicts(self):
        self.assertEqual(hosts.detect_host({})[0], "generic")
        self.assertEqual(hosts.detect_host({"PATH": "/codex/claude/cursor"})[0], "generic")
        self.assertEqual(hosts.detect_host({"CODEX_THREAD_ID": "fixture"})[0], "codex")
        self.assertEqual(hosts.detect_host({"CODEX_THREAD_ID": "fixture", "CLAUDECODE": "1"})[0], "generic")

    def test_codex_prefers_hook_other_local_hosts_rules_and_cloud_manual(self):
        owner = Path("/fixture")
        for host in ("codex", "claude-code", "cursor"):
            local = hosts.plan(host, "desktop", "auto", owner, environ={})
            self.assertEqual(local["mode"], "hook" if host == "codex" else "rules")
            if host == "codex":
                self.assertEqual(local["hook_capability"], "adapter_available_runtime_not_verified")
            else:
                self.assertIsNone(local["hooks_file"])
            self.assertEqual(hosts.plan(host, "cloud", "auto", owner, environ={})["mode"], "manual")
        with self.assertRaises(ValueError):
            hosts.plan("codex", "cloud", "hook", owner)
        with self.assertRaises(ValueError):
            hosts.plan("claude-code", "desktop", "hook", owner)

    def test_profile_and_unknown_fallback_paths(self):
        owner = Path("/fixture")
        codex = hosts.plan("codex", "desktop", "rules", owner, True, environ={"CODEX_HOME": "/alternate"})
        self.assertEqual(codex["rules_file"], "/alternate/AGENTS.md")
        self.assertEqual(hosts.plan("cursor", "desktop", "auto", owner, True)["mode"], "manual")
        self.assertEqual(hosts.plan("generic", "unknown", "auto", owner)["mode"], "manual")
        custom = hosts.plan("generic", "desktop", "auto", owner, rules_file=owner / "MY-RULES.md")
        self.assertEqual(custom["mode"], "rules")

    def test_three_project_installations_use_actual_installed_paths(self):
        for host, rule in (("codex", "AGENTS.md"), ("claude-code", "CLAUDE.md"),
                           ("cursor", ".cursor/rules/super-astra.mdc")):
            with self.subTest(host=host), tempfile.TemporaryDirectory(prefix="welcome 空格 ") as tmp:
                project = Path(tmp).resolve() / "project with spaces"
                args = ("--host", host, "--surface", "desktop", "--project", project, "--mode", "rules")
                preview = self.run_script("install.py", *args)
                self.assertEqual(preview.returncode, 0, preview.stderr)
                self.assertFalse(project.exists())
                result = self.run_script("install.py", *args, "--apply")
                self.assertEqual(result.returncode, 0, result.stderr)
                installed = project / hosts.PROFILES[host]["skill_dir"] / "super-astra"
                text = (project / rule).read_text()
                self.assertIn(str(installed), text)
                self.assertNotIn(str(ROOT), text)
                self.assertFalse((project / ".codex/hooks.json").exists())
                self.assertIn('"rules_registered": true', result.stdout)
                self.assertIn('"native_delivery": "not_verified"', result.stdout)
                if host == "cursor":
                    self.assertTrue(text.startswith(setup_rules.CURSOR_HEADER))
                # Repeat initialization preserves bytes and a later user edit survives removal.
                command = [sys.executable, str(installed / "scripts/initialize.py"), *map(str, args)]
                self.assertEqual(subprocess.run(command + ["--apply"], capture_output=True).returncode, 0)
                self.assertEqual((project / rule).read_text(), text)
                with (project / rule).open("a") as stream:
                    stream.write("\nUser instruction added later.\n")
                removed = subprocess.run(command + ["--remove", "--apply"], capture_output=True, text=True)
                self.assertEqual(removed.returncode, 0, removed.stderr)
                remaining = (project / rule).read_text()
                self.assertNotIn(setup_rules.BEGIN, remaining)
                self.assertIn("User instruction added later.", remaining)

    def test_block_edit_preserves_bytes_and_is_reversible(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "AGENTS.md"
            original = "# Existing\r\n保留原始规则。".encode()
            path.write_bytes(original)
            with redirect_stdout(StringIO()):
                setup_rules.manage(path, ROOT / "config.json", apply=True)
            current = path.read_bytes()
            self.assertTrue(current.startswith(original))
            with redirect_stdout(StringIO()):
                setup_rules.manage(path, ROOT / "config.json", apply=True)
            self.assertEqual(path.read_bytes(), current)
            self.assertEqual(next(path.parent.glob("*.bak")).read_bytes(), original)
            with redirect_stdout(StringIO()):
                setup_rules.manage(path, ROOT / "config.json", apply=True, remove=True)
            self.assertEqual(path.read_bytes(), original)

    def test_shadowing_bad_markers_and_symlinks_fail_without_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "AGENTS.md"
            (path.parent / "AGENTS.override.md").write_text("active instructions")
            with self.assertRaises(ValueError):
                setup_rules.prepare(path, ROOT / "config.json")
            self.assertFalse(path.exists())
            path = path.with_name("RULES.md")
            path.write_text("<!-- BEGIN LABKIT_WELCOME_TO_AGI_RULE_V1 -->")
            with self.assertRaises(ValueError):
                setup_rules.prepare(path, ROOT / "config.json")
            alias = path.with_name("ALIAS.md")
            alias.symlink_to(path)
            with self.assertRaises(ValueError):
                setup_rules.prepare(alias, ROOT / "config.json")
            with self.assertRaises(ValueError):
                setup_rules.transform("---\nalwaysApply: false\n---\nForeign rule", "body", "cursor")

    def test_manual_export_is_portable_and_respects_enabled_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.json"
            data = json.loads((ROOT / "config.json").read_text())
            data["modules"]["delegation"]["enabled"] = False
            config.write_text(json.dumps(data))
            output = Path(tmp) / "prompt-pack.md"
            args = ("--host", "generic", "--surface", "cloud", "--mode", "manual",
                    "--config", config, "--export", output)
            self.assertEqual(self.run_script("initialize.py", *args).returncode, 0)
            self.assertFalse(output.exists())
            result = self.run_script("initialize.py", *args, "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            pack = output.read_text()
            self.assertNotIn(str(ROOT), pack)
            self.assertNotIn("## delegation", pack)
            self.assertIn("## testing", pack)
            before = output.read_bytes()
            self.assertNotEqual(self.run_script("initialize.py", *args, "--apply").returncode, 0)
            self.assertEqual(output.read_bytes(), before)

    def test_generic_install_does_not_silently_register_codex(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_script("install.py", "--host", "generic", "--project", tmp, "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"mode": "manual"', result.stdout)
            self.assertFalse((Path(tmp) / "AGENTS.md").exists())
            self.assertFalse((Path(tmp) / ".codex").exists())

    def test_hook_rule_switch_requires_scoped_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp).resolve()
            args = ("--host", "codex", "--project", project)
            result = self.run_script("install.py", *args, "--mode", "hook", "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = project / ".agents/skills/super-astra"
            command = [sys.executable, str(installed / "scripts/initialize.py"), *map(str, args)]
            def run(*extra):
                return subprocess.run(command + list(extra), capture_output=True, text=True)
            blocked = run("--mode", "rules", "--apply")
            self.assertNotEqual(blocked.returncode, 0)
            self.assertFalse((project / "AGENTS.md").exists())
            self.assertEqual(run("--mode", "hook", "--remove", "--apply").returncode, 0)
            result = run("--mode", "rules", "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            rules_before = (project / "AGENTS.md").read_bytes()
            # Auto now recommends a hook, but must not silently migrate an existing rule.
            self.assertNotEqual(run("--apply").returncode, 0)
            self.assertEqual((project / "AGENTS.md").read_bytes(), rules_before)
            self.assertEqual(json.loads((project / ".codex/hooks.json").read_text())["hooks"], {})
            self.assertNotEqual(run("--mode", "hook", "--apply").returncode, 0)
            # Broken config must not prevent uninstalling the rule or hook.
            (installed / "config.json").write_text("{broken")
            self.assertEqual(run("--mode", "rules", "--remove", "--apply").returncode, 0)
            self.assertEqual(run("--mode", "hook", "--remove", "--apply").returncode, 0)

    def test_ui_entry_export_does_not_claim_installed_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rule.txt"
            result = self.run_script("initialize.py", "--host", "cursor", "--mode", "manual",
                                     "--export-format", "entry", "--export", path, "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            state = json.loads(result.stdout)
            self.assertFalse(state["rules_registered"])
            self.assertEqual(state["native_delivery"], "not_verified")
            self.assertIn(str(ROOT), path.read_text())
            self.assertLess(path.stat().st_size, 3000)

    def test_existing_cursor_rule_cannot_claim_always_apply_after_header_edit(self):
        original = setup_rules.transform("", "body", "cursor")
        altered = original.replace("alwaysApply: true", "alwaysApply: false")
        with self.assertRaises(ValueError):
            setup_rules.transform(altered, "updated", "cursor")
        self.assertNotIn(setup_rules.BEGIN, setup_rules.transform(altered, "", "cursor", remove=True))

    def test_hermes_and_openclaw_install_preserve_rules_and_remove_scoped_entry(self):
        for host, rule, skill_dir in (("hermes", ".hermes.md", ".hermes/skills"),
                                      ("openclaw", "AGENTS.md", "skills")):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp).resolve()
                original = "# Existing instructions\r\n保留原有配置。\r\n".encode()
                (project / rule).write_bytes(original)
                args = ("--host", host, "--project", project)
                result = self.run_script("install.py", *args, "--apply")
                self.assertEqual(result.returncode, 0, result.stderr)
                installed = project / skill_dir / "super-astra"
                self.assertTrue((installed / "SKILL.md").exists())
                after = (project / rule).read_bytes()
                self.assertTrue(after.startswith(original))
                self.assertIn(str(installed).encode(), after)
                self.assertFalse((project / ".codex").exists())
                if host == "hermes":
                    self.assertFalse((project / "AGENTS.md").exists())
                result = subprocess.run([sys.executable, str(installed / "scripts/initialize.py"),
                                         *map(str, args), "--remove", "--apply"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((project / rule).read_bytes(), original)

    def test_agent_homes_are_not_assumed_global_rules_or_codex_hooks(self):
        for host, key in (("hermes", "HERMES_HOME"), ("openclaw", "OPENCLAW_STATE_DIR")):
            plan = hosts.plan(host, "cli", "auto", Path("/fixture"), user=True,
                              environ={key: "/profile"})
            self.assertEqual(plan["skill_dir"], "/profile/skills")
            self.assertEqual(plan["mode"], "manual")
            self.assertIsNone(plan["rules_file"])
            with self.assertRaises(ValueError):
                hosts.plan(host, "cli", "hook", Path("/fixture"))
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            folder = project / ".cursor/rules"
            folder.mkdir(parents=True)
            (folder / "existing.mdc").write_text("Existing Hermes context")
            with self.assertRaises(ValueError):
                hosts.plan("hermes", "cli", "auto", project)
            self.assertFalse((project / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
