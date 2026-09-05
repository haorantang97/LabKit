#!/usr/bin/env python3
"""Install the complete skill and initialize a host-appropriate routing entry."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from astra import ROOT, load_config, router_context
import hosts
import setup_rules
import onboarding


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--user", action="store_true")
    scope.add_argument("--project", type=Path)
    hosts.add_arguments(parser)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--skill-only", action="store_true", help="alias for --mode manual")
    parser.add_argument("--disable-module", action="append", default=[], metavar="ID",
                        help="new installation only: disable a chosen module before registering routing; repeat for several")
    args = parser.parse_args()
    owner = Path.home() if args.user else args.project.expanduser().resolve()
    try:
        if args.skill_only and args.mode not in ("auto", "manual"):
            raise ValueError("--skill-only conflicts with the selected mode")
        selected = hosts.plan(args.host, args.surface, "manual" if args.skill_only else args.mode,
                              owner, args.user, args.rules_file, args.hooks)
        if args.export and selected["mode"] != "manual":
            raise ValueError("--export requires manual mode")
        if args.export and (args.export.expanduser().exists() or args.export.expanduser().is_symlink()):
            raise ValueError("export destination exists; choose a new file")
        destination = owner / selected["skill_dir"] / "welcome-to-agi"
        if destination.exists():
            raise ValueError("destination exists; initialize that installed copy or review an update without overwriting customizations")
        if destination.is_symlink():
            raise ValueError("destination is a symlink")
        settings = load_config(ROOT / "config.json")
        for name in args.disable_module:
            if name not in settings["modules"]:
                raise ValueError("unknown module: " + name)
            settings["modules"][name]["enabled"] = False
        router_context(settings)
        if selected["mode"] == "rules":
            setup_rules.prepare(Path(selected["rules_file"]), destination / "config.json", selected["rule_format"])
        print(json.dumps(dict(selected, destination=str(destination),
                              action="apply" if args.apply else "preview",
                              onboarding=onboarding.snapshot(selected, ROOT / "config.json", owner, args.user, settings)), indent=2))
        if not args.apply:
            print("Preview only. Repeat with --apply to install and initialize.")
            return 0
        shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.bak"))
        if args.disable_module:
            (destination / "config.json").write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        command = [sys.executable, str(destination / "scripts/initialize.py"),
                   "--host", selected["host"], "--surface", args.surface, "--mode", selected["mode"],
                   "--export-format", args.export_format, "--apply"]
        command += ["--user"] if args.user else ["--project", str(owner)]
        for flag, value in (("--hooks", selected["hooks_file"]), ("--rules-file", selected["rules_file"]),
                            ("--export", str(args.export.expanduser().absolute()) if args.export else None)):
            if value:
                command += [flag, value]
        result = subprocess.run(command)
        if result.returncode:
            print("Skill files installed, initialization failed; fix the reported issue and rerun installed initialize.py.", file=sys.stderr)
        return result.returncode
    except (ValueError, OSError) as error:
        parser.exit(1, "welcome-to-agi install: " + str(error) + "\n")


if __name__ == "__main__":
    sys.exit(main())
