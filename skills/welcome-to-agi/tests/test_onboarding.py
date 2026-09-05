import json
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import onboarding
import setup_hook


class OnboardingTests(unittest.TestCase):
    def run_script(self, name, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / name), *map(str, args)],
                              capture_output=True, text=True)

    def test_inventory_before_legacy_migration_never_executes_or_changes_hooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            hook = project / ".codex/hooks.json"
            hook.parent.mkdir()
            sentinel = project / "hook-executed"
            item = setup_hook.handler(ROOT / "config.json")
            item["statusMessage"] = "LabKit Astra Prompts v1"
            item["command"] = "touch " + str(sentinel)
            hook.write_text(json.dumps({"hooks": {"UserPromptSubmit": [{"hooks": [item]}]}}))
            original = hook.read_bytes()
            result = self.run_script("initialize.py", "--host", "codex", "--surface", "desktop",
                                     "--project", project, "--onboarding")
            self.assertEqual(result.returncode, 0, result.stderr)
            state = json.loads(result.stdout)["onboarding"]
            self.assertEqual(state["hooks"]["registration"], "present")
            self.assertEqual(state["hooks"]["handlers"][0]["definition"], "different")
            self.assertEqual(state["hooks"]["trust"], "not_verified")
            self.assertEqual(state["hooks"]["runtime_enabled"], "not_verified")
            self.assertEqual(state["audit"]["status"], "not_run")
            self.assertNotIn(item["command"], result.stdout)
            self.assertEqual(hook.read_bytes(), original)
            self.assertFalse(sentinel.exists())
            self.assertFalse((project / "AGENTS.md").exists())

    def test_existing_disabled_choices_are_displayed_and_not_reset(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            config = project / "config.json"
            data = json.loads((ROOT / "config.json").read_text())
            data["modules"]["delegation"] = {"enabled": False, "guard": False}
            config.write_text(json.dumps(data))
            before = config.read_bytes()
            result = self.run_script("initialize.py", "--host", "codex", "--project", project,
                                     "--config", config, "--onboarding")
            self.assertEqual(result.returncode, 0, result.stderr)
            state = json.loads(result.stdout)["onboarding"]
            delegation = next(m for m in state["modules"] if m["id"] == "delegation")
            self.assertFalse(delegation["enabled"])
            self.assertFalse(delegation["guard"])
            self.assertEqual(config.read_bytes(), before)
            self.assertEqual(list(project.iterdir()), [config])

    def test_bad_hook_file_is_reported_and_preserved_for_user_choice(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hooks.json"
            path.write_text('{broken "secret command"')
            state = onboarding.hook_inventory(path, ROOT / "config.json")
            self.assertEqual(state["registration"], "unreadable_or_invalid")
            self.assertNotIn("secret command", json.dumps(state))
            self.assertEqual(path.read_text(), '{broken "secret command"')

    def test_other_hosts_and_cloud_do_not_claim_hooks_are_off(self):
        with tempfile.TemporaryDirectory() as tmp:
            for host, surface in (("claude-code", "desktop"), ("codex", "cloud")):
                result = self.run_script("initialize.py", "--host", host, "--surface", surface,
                                         "--project", tmp, "--onboarding")
                self.assertEqual(result.returncode, 0, result.stderr)
                state = json.loads(result.stdout)["onboarding"]
                self.assertEqual(state["hooks"]["registration"], "not_inspected")
                self.assertEqual(state["hooks"]["runtime_enabled"], "not_verified")
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_onboarding_rejects_mutating_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            for flags in (("--apply",), ("--remove",), ("--export", str(Path(tmp) / "pack.md"))):
                result = self.run_script("initialize.py", "--host", "codex", "--project", tmp,
                                         "--onboarding", *flags)
                self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_new_install_applies_choices_before_registration_without_changing_source(self):
        before = (ROOT / "config.json").read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            args = ("--host", "codex", "--project", project, "--disable-module", "delegation")
            result = self.run_script("install.py", *args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(project.exists())
            result = self.run_script("install.py", *args, "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = project / ".agents/skills/welcome-to-agi"
            config = json.loads((installed / "config.json").read_text())
            self.assertFalse(config["modules"]["delegation"]["enabled"])
            self.assertTrue(config["modules"]["delegation"]["guard"])
            self.assertTrue((project / "AGENTS.md").exists())
            router = subprocess.run([sys.executable, str(installed / "scripts/astra.py"), "router"],
                                    capture_output=True, text=True)
            self.assertEqual(router.returncode, 0, router.stderr)
            self.assertNotIn('"id": "delegation"', json.loads(router.stdout)["guidance"])
            shutil.rmtree(installed / "modules/delegation")
            inspect = subprocess.run([sys.executable, str(installed / "scripts/initialize.py"),
                                      "--host", "codex", "--project", str(project), "--onboarding"],
                                     capture_output=True, text=True)
            self.assertEqual(inspect.returncode, 0, inspect.stderr)
            self.assertFalse(next(m for m in json.loads(inspect.stdout)["onboarding"]["modules"]
                                  if m["id"] == "delegation")["enabled"])
            invalid = self.run_script("install.py", "--host", "codex", "--project", Path(tmp) / "invalid",
                                      "--disable-module", "does-not-exist", "--apply")
            self.assertNotEqual(invalid.returncode, 0)
            self.assertFalse((Path(tmp) / "invalid").exists())
        self.assertEqual((ROOT / "config.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
