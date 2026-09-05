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


class HostTests(unittest.TestCase):
    def run_script(self, script, *args, env=None):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
                              capture_output=True, text=True, env=env)

    def test_detection_requires_runtime_evidence_and_handles_conflicts(self):
        self.assertEqual(hosts.detect_host({})[0], "generic")
        self.assertEqual(hosts.detect_host({"PATH": "/codex/claude/cursor"})[0], "generic")
        self.assertEqual(hosts.detect_host({"CODEX_THREAD_ID": "fixture"})[0], "codex")
        self.assertEqual(hosts.detect_host({"CODEX_THREAD_ID": "fixture", "CLAUDECODE": "1"})[0], "generic")

    def test_desktop_defaults_rules_and_cloud_defaults_manual(self):
        owner = Path("/fixture")
        for host in ("codex", "claude-code", "cursor"):
            local = hosts.plan(host, "desktop", "auto", owner, environ={})
            self.assertEqual(local["mode"], "rules")
            self.assertIsNone(local["hooks_file"])
            self.assertEqual(hosts.plan(host, "cloud", "auto", owner, environ={})["mode"], "manual")
        with self.assertRaises(ValueError):
            hosts.plan("codex", "cloud", "hook", owner)
        with self.assertRaises(ValueError):
            hosts.plan("claude-code", "desktop", "hook", owner)

    def test_profile_and_unknown_fallback_paths(self):
        owner = Path("/fixture")
        codex = hosts.plan("codex", "desktop", "auto", owner, True, environ={"CODEX_HOME": "/alternate"})
        self.assertEqual(codex["rules_file"], "/alternate/AGENTS.md")
        self.assertEqual(hosts.plan("cursor", "desktop", "auto", owner, True)["mode"], "manual")
        self.assertEqual(hosts.plan("generic", "unknown", "auto", owner)["mode"], "manual")
        custom = hosts.plan("generic", "desktop", "auto", owner, rules_file=owner / "MY-RULES.md")
        self.assertEqual(custom["mode"], "rules")

    def test_three_project_installations_use_actual_installed_paths(self):
        for host, rule in (("codex", "AGENTS.md"), ("claude-code", "CLAUDE.md"),
                           ("cursor", ".cursor/rules/welcome-to-agi.mdc")):
            with self.subTest(host=host), tempfile.TemporaryDirectory(prefix="welcome 空格 ") as tmp:
                project = Path(tmp).resolve() / "project with spaces"
                args = ("--host", host, "--surface", "desktop", "--project", project)
                preview = self.run_script("install.py", *args)
                self.assertEqual(preview.returncode, 0, preview.stderr)
                self.assertFalse(project.exists())
                result = self.run_script("install.py", *args, "--apply")
                self.assertEqual(result.returncode, 0, result.stderr)
                installed = project / hosts.PROFILES[host]["skill_dir"] / "welcome-to-agi"
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
            installed = project / ".agents/skills/welcome-to-agi"
            command = [sys.executable, str(installed / "scripts/initialize.py"), *map(str, args)]
            def run(*extra):
                return subprocess.run(command + list(extra), capture_output=True, text=True)
            blocked = run("--mode", "rules", "--apply")
            self.assertNotEqual(blocked.returncode, 0)
            self.assertFalse((project / "AGENTS.md").exists())
            self.assertEqual(run("--mode", "hook", "--remove", "--apply").returncode, 0)
            result = run("--mode", "rules", "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
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


if __name__ == "__main__":
    unittest.main()
