#!/usr/bin/env python3
"""Inspect onboarding or register the hook; never claim host trust from a file."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from astra import ROOT, load_config, router_context
from setup_hook import handler, OWNED_LABELS


def default_hooks(root=ROOT):
    # Infer only standard installed locations. A source checkout needs --hooks.
    if root.parent.name != "skills" or root.parent.parent.name not in (".codex", ".agents"):
        return None
    owner = root.parent.parent.parent
    if owner == Path.home():
        return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "hooks.json"
    return owner / ".codex/hooks.json"


def status(path, config):
    settings = load_config(config)
    router = router_context(settings)
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
    parser.add_argument("--hooks", type=Path, default=default_hooks())
    parser.add_argument("--config", type=Path, default=ROOT / "config.json")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        target = args.hooks.expanduser().absolute() if args.hooks else None
        if args.apply:
            if target is None:
                raise ValueError("source checkout requires an explicit --hooks path")
            load_config(args.config)
            router_context(load_config(args.config))
            result = subprocess.run([sys.executable, str(ROOT / "scripts/setup_hook.py"),
                                     "--hooks", str(target), "--config", str(args.config), "--apply"])
            if result.returncode:
                return result.returncode
        print(json.dumps(status(target, args.config), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, "welcome-to-agi initialization: " + str(error) + "\n")


if __name__ == "__main__":
    sys.exit(main())
