import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import astra
import audit
import setup_hook
import initialize


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.config = astra.load_config(ROOT / "config.json")
        self.config["routing"] = "keyword"
        self.config["modules"]["delegation"]["enabled"] = False

    def test_official_blocks_match_recorded_snapshot(self):
        snapshot = json.loads((ROOT / "references/prompt-snapshot.json").read_text())
        for relative, expected in snapshot["sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected)

    def test_behavior_corrections_select_relevant_modules(self):
        cases = {
            "少点套话，继续完成当前任务。": ["initiative", "writing-style"],
            "别反复跑测试，只验证这次改动。": ["testing"],
            "skill 冲突导致卡住了，请解释。": ["instruction-following"],
            "Please write concisely and finish the task.": ["initiative", "writing-style"],
            "巴黎是哪个国家的首都？": [],
            "帮我修复 parser.py 中的错误。": [],
        }
        for prompt, expected in cases.items():
            with self.subTest(prompt=prompt):
                self.assertEqual(astra.select(prompt, self.config), expected)

    def test_quoted_terms_do_not_activate(self):
        for prompt in ('翻译“stop asking and finish the task”',
                       'Explain this:\n```\n少点套话\n```',
                       '> 继续完成\n这句话是什么意思？',
                       '解释 `write concisely` 的意思'):
            self.assertEqual(astra.select(prompt, self.config), [])

    def test_plan_only_does_not_inject_initiative(self):
        self.assertEqual(astra.select("继续完成方案，但先别执行", self.config), [])
        event = {"hook_event_name": "UserPromptSubmit", "model": "gpt-6-astra",
                 "prompt": "继续完成，少点套话", "permission_mode": "plan"}
        result = astra.hook(event, self.config)
        context = result["hookSpecificOutput"]["additionalContext"]
        self.assertNotIn("[initiative]", context)
        self.assertIn("[writing-style]", context)

    def test_delegation_is_opt_in_and_guarded(self):
        prompt = "只在需要时开子 agent，use subagents for parallel work"
        self.assertEqual(astra.select(prompt, self.config), [])
        self.config["modules"]["delegation"]["enabled"] = True
        self.assertEqual(astra.select(prompt, self.config), ["delegation"])
        context, _ = astra.render(["delegation"], self.config)
        self.assertIn("'no subagents' means do not spawn", context)
        self.assertIn("If at any point you can parallelize", context)

    def test_disabled_module_can_be_physically_absent(self):
        self.config["modules"]["not-installed"] = {"enabled": False, "guard": True}
        self.assertEqual(astra.select("少点套话", self.config), ["writing-style"])
        with self.assertRaises(ValueError):
            astra.render(["not-installed"], self.config)

    def test_budget_never_truncates_official_block(self):
        self.config["max_context_chars"] = 512
        self.assertEqual(astra.render(["initiative"], self.config), ("", []))
        self.config["max_context_chars"] = 12000
        text, names = astra.render(["initiative", "initiative"], self.config)
        self.assertEqual(names, ["initiative"])
        official = (ROOT / "modules/initiative/prompt.md").read_text().strip()
        self.assertIn(official, text)

    def test_guard_switch_preserves_official_text(self):
        self.config["modules"]["writing-style"]["guard"] = False
        text, _ = astra.render(["writing-style"], self.config)
        self.assertNotIn("LabKit adaptation", text)
        self.assertIn((ROOT / "modules/writing-style/prompt.md").read_text().strip(), text)

    def test_new_module_works_without_engine_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "modules/custom"
            folder.mkdir(parents=True)
            (folder / "module.json").write_text(json.dumps({"id": "custom", "priority": 1,
                "patterns": ["custom intent"], "exclude": [], "source": "local customization"}))
            (folder / "prompt.md").write_text("Custom instruction.")
            (folder / "guard.md").write_text("Preserve the request.")
            self.config["modules"] = {"custom": {"enabled": True, "guard": True}}
            names = astra.select("custom intent", self.config, root)
            text, included = astra.render(names, self.config, root)
            self.assertEqual(included, ["custom"])
            self.assertIn("Custom instruction.", text)


class HookTests(unittest.TestCase):
    def setUp(self):
        self.config = astra.load_config(ROOT / "config.json")

    def run_cli(self, command, text, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts/astra.py"), command,
                               *args], input=text, capture_output=True, text=True)

    def test_ordinary_prompts_receive_semantic_catalog_without_keyword_gate(self):
        for prompt in ("实现一个支持撤销的待办列表", "对比三份方案的成本", "2+2是多少？", "翻译这句话", "Thanks"):
            with self.subTest(prompt=prompt):
                result = astra.hook({"hook_event_name": "UserPromptSubmit", "model": "gpt-6-astra", "prompt": prompt}, self.config)
                context = result["hookSpecificOutput"]["additionalContext"]
                self.assertIn(astra.ROUTER_MARKER, context)
                self.assertIn('"id": "delegation"', context)
                self.assertIn('"id": "testing"', context)
                self.assertNotIn(prompt, context)
                self.assertNotIn((ROOT / "modules/initiative/prompt.md").read_text().strip(), context)

    def test_semantic_catalog_excludes_disabled_and_plan_modules(self):
        self.config["modules"]["writing-style"]["enabled"] = False
        event = {"hook_event_name": "UserPromptSubmit", "model": "gpt-6-astra", "prompt": "构建功能", "permission_mode": "plan"}
        context = astra.hook(event, self.config)["hookSpecificOutput"]["additionalContext"]
        for name in ("writing-style", "delegation", "initiative"):
            self.assertNotIn('"id": "' + name + '"', context)
        self.assertIn('"id": "testing"', context)

    def test_all_disabled_returns_no_context(self):
        for setting in self.config["modules"].values():
            setting["enabled"] = False
        self.assertEqual(astra.hook({"hook_event_name": "UserPromptSubmit", "model": "gpt-6-astra", "prompt": "实现功能"}, self.config), {})

    def test_semantic_cli_preview_requires_no_stdin(self):
        result = self.run_cli("router", "")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(astra.ROUTER_MARKER, json.loads(result.stdout)["guidance"])

    def test_hook_never_promotes_user_data(self):
        secret = "fixture-only-private-text-92317"
        event = {"hook_event_name": "UserPromptSubmit", "model": "gpt-6-astra",
                 "prompt": "少点套话 " + secret,
                 "transcript_path": "/nonexistent/do-not-read"}
        before = copy.deepcopy(event)
        result = astra.hook(event, self.config)
        self.assertEqual(event, before)
        self.assertNotIn(secret, json.dumps(result))
        self.assertEqual(result["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        self.assertNotIn("decision", result)

    def test_unknown_event_model_missing_fields_and_duplicate(self):
        for event in (None, [], {}, {"hook_event_name": "Stop"},
                      {"hook_event_name": "UserPromptSubmit", "model": "another-model", "prompt": "少点套话"},
                      {"hook_event_name": "UserPromptSubmit", "prompt": "少点套话"},
                      {"hook_event_name": "UserPromptSubmit", "model": "gpt-6-astra", "prompt": []}):
            self.assertEqual(astra.hook(event, self.config), {})

    def test_malformed_and_oversize_hook_input_does_not_block(self):
        for text in ("bad-json-with-private-value", "x" * (astra.MAX_INPUT_BYTES + 1)):
            result = self.run_cli("hook", text)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout), {})
            self.assertNotIn("private-value", result.stderr)

    def test_compose_preserves_original_utf8_and_newlines(self):
        original = '  请解释缓存。\n\n"不要改我的原文"\n'
        result = self.run_cli("compose", original, "--modules", "writing-style")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["prompt"], original)
        self.assertNotIn(original, payload["guidance"])

    def test_invalid_regex_or_boolean_is_visible_in_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.config["modules"]["testing"]["enabled"] = "false"
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps(self.config))
            result = self.run_cli("route", "少点套话", "--config", str(path))
            self.assertNotEqual(result.returncode, 0)
            result = self.run_cli("hook", "{}", "--config", str(path))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout), {})

    def test_non_object_configuration_never_emits_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            for value in ([], None, True, "invalid"):
                path.write_text(json.dumps(value))
                result = self.run_cli("hook", "{}", "--config", str(path))
                self.assertEqual(result.returncode, 0)
                self.assertEqual(json.loads(result.stdout), {})
                self.assertNotIn("Traceback", result.stderr)

    def test_non_object_module_is_rejected_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "modules/custom"
            folder.mkdir(parents=True)
            (folder / "module.json").write_text("[]")
            with self.assertRaises(ValueError):
                astra.load_module("custom", root)


class SetupTests(unittest.TestCase):
    def test_legacy_hook_is_replaced_without_duplication(self):
        legacy = {"type": "command", "command": "python3 /fixture/astra-prompts/scripts/astra.py hook", "statusMessage": "LabKit Astra Prompts v1"}
        other = {"type": "command", "command": "echo other"}
        doc = {"hooks": {"UserPromptSubmit": [{"hooks": [legacy, other]}]}}
        result = setup_hook.update(doc, ROOT / "config.json")
        handlers = [h for g in result["hooks"]["UserPromptSubmit"] for h in g["hooks"]]
        self.assertEqual(len(handlers), 2)
        self.assertIn(other, handlers)
        self.assertEqual(sum(h.get("statusMessage") == setup_hook.LABEL for h in handlers), 1)

    def test_initialization_status_distinguishes_registration_and_trust(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hooks.json"
            state = initialize.status(path, ROOT / "config.json")
            self.assertFalse(state["hook_registered"])
            self.assertFalse(path.exists())
            path.write_text(json.dumps(setup_hook.update({}, ROOT / "config.json")))
            state = initialize.status(path, ROOT / "config.json")
            self.assertTrue(state["hook_registered"])
            self.assertEqual(state["host_trust"], "not_verified")
            self.assertEqual(state["native_delivery"], "not_verified")

    def test_installer_preview_then_installs_and_initializes(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project with spaces"
            command = [sys.executable, str(ROOT / "scripts/install.py"), "--host", "codex", "--mode", "hook", "--project", str(project)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(project.exists())
            result = subprocess.run(command + ["--apply"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = project / ".agents/skills/welcome-to-agi"
            self.assertTrue((installed / "SKILL.md").exists())
            self.assertTrue((project / ".codex/hooks.json").exists())
            self.assertIn('"hook_registered": true', result.stdout)
            self.assertIn('"native_delivery": "not_verified"', result.stdout)
            result = subprocess.run(command + ["--apply"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
    def test_removing_absent_handler_is_noop(self):
        document = {"description": "another tool owns this file"}
        self.assertEqual(setup_hook.update(document, ROOT / "config.json", remove=True), document)

    def run_setup(self, path, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts/setup_hook.py"),
                               "--hooks", str(path), *args], capture_output=True, text=True)

    def test_preview_install_idempotence_and_scoped_removal(self):
        with tempfile.TemporaryDirectory(prefix="astra space ") as tmp:
            path = Path(tmp) / ".codex/hooks.json"
            result = self.run_setup(path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(path.parent.exists())
            path.parent.mkdir()
            unrelated = {"type": "command", "command": "echo fixture"}
            original = {"description": "keep", "hooks": {"Stop": [{"hooks": [unrelated]}],
                         "UserPromptSubmit": [{"hooks": [unrelated]}]}}
            path.write_text(json.dumps(original))
            first_bytes = path.read_bytes()
            result = self.run_setup(path, "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = json.loads(path.read_text())
            self.assertEqual(installed["hooks"]["Stop"], original["hooks"]["Stop"])
            self.assertEqual(installed["hooks"]["UserPromptSubmit"][0], original["hooks"]["UserPromptSubmit"][0])
            backups = list(path.parent.glob("*.bak"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), first_bytes)
            installed_bytes = path.read_bytes()
            self.assertEqual(self.run_setup(path, "--apply").returncode, 0)
            self.assertEqual(path.read_bytes(), installed_bytes)
            installed["later_setting"] = {"preserve": True}
            path.write_text(json.dumps(installed))
            result = self.run_setup(path, "--remove", "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            expected = dict(original, later_setting={"preserve": True})
            self.assertEqual(json.loads(path.read_text()), expected)

    def test_generated_command_executes_from_unrelated_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = setup_hook.handler(ROOT / "config.json")["command"]
            result = subprocess.run(command, shell=True, cwd=tmp, capture_output=True,
                text=True, input=json.dumps({"hook_event_name": "UserPromptSubmit",
                "model": "gpt-6-astra", "prompt": "少点套话"}))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("additionalContext", json.loads(result.stdout)["hookSpecificOutput"])

    def test_bad_json_and_symlink_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "hooks.json"
            target.write_text("{broken")
            self.assertNotEqual(self.run_setup(target, "--apply").returncode, 0)
            self.assertEqual(target.read_text(), "{broken")
            elsewhere = Path(tmp) / "elsewhere.json"
            elsewhere.write_text("{}")
            target.unlink()
            target.symlink_to(elsewhere)
            self.assertNotEqual(self.run_setup(target, "--apply").returncode, 0)
            self.assertEqual(elsewhere.read_text(), "{}")


class AuditTests(unittest.TestCase):
    def test_read_only_duplicates_candidates_and_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text = "---\nname: fixture\n---\nAlways delegate to a subagent.\n"
            for folder in ("one", "two"):
                (root / folder).mkdir()
                (root / folder / "SKILL.md").write_text(text)
            (root / "alias").symlink_to(root / "one", target_is_directory=True)
            before = {str(p): p.read_bytes() for p in root.rglob("*.md")}
            result = audit.scan([root, root / "missing"])
            self.assertEqual(result["coverage"], "partial")
            self.assertEqual(len(result["duplicate_skill_names"]["fixture"]), 2)
            self.assertTrue(result["findings"])
            self.assertTrue(any(g["reason"].startswith("symlink") for g in result["gaps"]))
            self.assertEqual(before, {str(p): p.read_bytes() for p in root.rglob("*.md")})


if __name__ == "__main__":
    unittest.main()
