#!/usr/bin/env python3
"""Choose a host adapter, preview/apply setup, and report unverified delivery honestly."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from astra import ROOT, load_config, router_context
from setup_hook import handler, OWNED_LABELS
import hosts
import setup_rules
import onboarding


def installed_scope(root=ROOT):
    if root.parent.name == "skills" and root.parent.parent.name in (".codex", ".agents", ".claude", ".cursor"):
        owner = root.parent.parent.parent
        return owner, owner == Path.home()
    return None, False


def default_hooks(root=ROOT):
    # Infer only standard installed locations. A source checkout needs --hooks.
    if root.parent.name != "skills" or root.parent.parent.name not in (".codex", ".agents"):
        return None
    owner = root.parent.parent.parent
    if owner == Path.home():
        return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "hooks.json"
    return owner / ".codex/hooks.json"


def status(path, config, validate=True):
    settings = load_config(config) if validate else {"modules": {}}
    router = router_context(settings) if validate else ""
    result = {"skill_installed": True, "routing": settings.get("routing", "semantic"),
              "enabled_modules": [k for k, v in settings["modules"].items() if v["enabled"]],
              "adapter_probe": "passed" if router else "no enabled modules",
              "hook_registered": False, "host_trust": "not_verified",
              "native_delivery": "not_verified", "hooks_file": str(path) if path else None}
    if path is None:
        result["next_step"] = "Choose the installed skill location and an explicit --hooks path."
        return result
    doc = json.loads(path.read_text()) if path.exists() else {}
    if not isinstance(doc, dict) or not isinstance(doc.get("hooks", {}), dict):
        raise ValueError("invalid hooks.json object")
    groups = doc.get("hooks", {}).get("UserPromptSubmit", [])
    if not isinstance(groups, list):
        raise ValueError("invalid UserPromptSubmit groups")
    expected = handler(config)
    count, current = 0, 0
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            raise ValueError("invalid hook group")
        for item in group["hooks"]:
            if not isinstance(item, dict):
                raise ValueError("invalid handler")
            if item.get("statusMessage") in OWNED_LABELS:
                count += 1
                if item == expected:
                    current += 1
    result["hook_registered"] = count == current == 1
    result["matching_registrations"] = count
    result["next_step"] = ("Review/trust this definition in Codex /hooks, then run a normal task and inspect hook diagnostics."
                           if result["hook_registered"] else "Register or update the hook with initialize.py --apply.")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    hosts.add_arguments(parser)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--user", action="store_true")
    scope.add_argument("--project", type=Path)
    parser.add_argument("--config", type=Path, default=ROOT / "config.json")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--onboarding", action="store_true", help="read-only module and hook inventory for the first-use conversation; no audit or registration")
    parser.add_argument("--remove", action="store_true", help="remove only the selected adapter's registration")
    args = parser.parse_args()
    try:
        if args.onboarding and (args.apply or args.remove or args.export):
            raise ValueError("--onboarding is read-only; omit --apply, --remove and --export")
        owner, user = installed_scope()
        if args.user:
            owner, user = Path.home(), True
        elif args.project:
            owner, user = args.project.expanduser().resolve(), False
        if owner is None:
            if not (args.hooks or args.rules_file or args.mode == "manual" or args.surface == "cloud"):
                raise ValueError("source checkout/custom layout needs --user, --project, an explicit target, or --mode manual")
            owner = ROOT
        selected = hosts.plan(args.host, args.surface, args.mode, owner, user, args.rules_file, args.hooks)
        if args.export and (selected["mode"] != "manual" or args.remove):
            raise ValueError("--export requires manual mode without --remove")
        config = args.config.expanduser().resolve()
        settings = load_config(config) if not args.remove else {"modules": {}}
        if args.onboarding:
            print(json.dumps(dict(selected, onboarding=onboarding.snapshot(selected, config, owner, user)),
                             ensure_ascii=False, indent=2))
            return 0
        if not args.remove:
            router_context(settings)
        state = dict(selected, skill_installed=(ROOT / "SKILL.md").is_file(),
                     enabled_modules=[k for k, v in settings["modules"].items() if v["enabled"]],
                     adapter_probe="passed" if not args.remove else "not_run_for_removal", host_trust="not_applicable", rules_registered=False,
                     hook_registered=False, action="apply" if args.apply else "preview")
        if selected["mode"] == "hook":
            target = Path(selected["hooks_file"])
            rule_plan = hosts.plan("codex", args.surface, "rules", owner, user)
            rule_path = Path(rule_plan["rules_file"])
            if not args.remove and rule_path.exists() and setup_rules.BEGIN in rule_path.read_text(encoding="utf-8"):
                raise ValueError("existing Welcome to AGI rule found; remove it with --mode rules --remove --apply before switching to hooks")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/setup_hook.py"),
                                     "--hooks", str(target), "--config", str(config)] +
                                    (["--remove"] if args.remove else []) + (["--apply"] if args.apply else []))
            if result.returncode:
                return result.returncode
            state.update(status(target, config, validate=not args.remove))
            state["next_step"] = ("Start a fresh task in the actual client; registration is removed." if args.remove else
                "Review/trust via Codex CLI /hooks in the SAME runtime/profile, then verify in the actual desktop/CLI client. "
                "If blocked, retain pending status and explain the exact user step; ask before switching to rules. "
                "Shared config is not proof of desktop delivery; see references/hosts.md.")
        elif selected["mode"] == "rules":
            target = Path(selected["rules_file"])
            # Avoid creating a second entrypoint during a legacy hook migration.
            hook_path = Path(hosts.plan("codex", args.surface, "hook", owner, user)["hooks_file"]) if selected["host"] == "codex" and os.name != "nt" else None
            if hook_path and hook_path.exists() and not args.remove:
                old = status(hook_path, config)
                if old.get("matching_registrations", 0):
                    raise ValueError("existing Welcome to AGI hook found at " + str(hook_path) +
                                     "; remove it with --hooks PATH --remove --apply before switching to rules")
            state.update(setup_rules.manage(target, config, selected["rule_format"], args.apply, args.remove))
            state["next_step"] = ("Start a fresh task in the actual client. Check the active instruction source, "
                                  "then ordinary-task module reads; see references/hosts.md. File registration does not prove loading.")
        else:
            if args.remove:
                raise ValueError("manual mode has no registration to remove")
            state["next_step"] = ("No automatic entrypoint installed. Invoke the installed SKILL.md explicitly, "
                                  "or use --mode manual --export PATH --apply and attach that pack in your client. "
                                  "For persistent custom instructions, use --mode rules --rules-file PATH only if the host loads it.")
            if args.export:
                target = args.export.expanduser().absolute()
                if target.exists() or target.is_symlink():
                    raise ValueError("export destination exists; choose a new file")
                pack = (setup_rules.BEGIN + setup_rules.entry(config) + setup_rules.END
                        if args.export_format == "entry" else setup_rules.manual_pack(config))
                state.update(export_file=str(target), export_format=args.export_format,
                             export_chars=len(pack), export_written=False)
                if args.export_format == "entry":
                    state["next_step"] = "Paste this entry into the actual client's always-loaded settings, then verify local file reads. Export alone does not install a rule."
                if args.apply:
                    setup_rules.save(target, b"", pack.encode("utf-8"))
                    state["export_written"] = True
        if not args.remove:
            state["onboarding"] = onboarding.snapshot(selected, config, owner, user)
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, "welcome-to-agi initialization: " + str(error) + "\n")


if __name__ == "__main__":
    sys.exit(main())
