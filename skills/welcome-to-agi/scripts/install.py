#!/usr/bin/env python3
"""Install the complete skill and guide hook initialization in one entrypoint."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from astra import ROOT, load_config, router_context


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--user", action="store_true")
    scope.add_argument("--project", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--skill-only", action="store_true", help="explicitly skip hook registration")
    args = parser.parse_args()
    owner = Path.home() if args.user else args.project.expanduser().resolve()
    destination = owner / ".agents/skills/welcome-to-agi"
    hooks = ((Path(os.environ.get("CODEX_HOME", str(owner / ".codex"))) / "hooks.json")
             if args.user else owner / ".codex/hooks.json")
    try:
        if destination.exists():
            raise ValueError("destination exists; initialize that installed copy or review an update without overwriting customizations")
        if destination.is_symlink():
            raise ValueError("destination is a symlink")
        settings = load_config(ROOT / "config.json")
        router_context(settings)
        print(json.dumps({"destination": str(destination), "hooks": None if args.skill_only else str(hooks),
                          "action": "apply" if args.apply else "preview", "routing": settings.get("routing", "semantic"),
                          "host_trust": "user review required after registration"}, indent=2))
        if not args.apply:
            print("Preview only. Repeat with --apply to install and initialize.")
            return 0
        shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.bak"))
        if args.skill_only:
            print("Skill installed in manual mode; automatic routing not registered.")
            return 0
        result = subprocess.run([sys.executable, str(destination / "scripts/initialize.py"),
                                 "--hooks", str(hooks), "--apply"])
        if result.returncode:
            print("Skill files installed, initialization failed; fix the reported issue and rerun installed initialize.py.", file=sys.stderr)
        return result.returncode
    except (ValueError, OSError) as error:
        parser.exit(1, "welcome-to-agi install: " + str(error) + "\n")


if __name__ == "__main__":
    sys.exit(main())
