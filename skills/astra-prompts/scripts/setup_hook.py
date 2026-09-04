#!/usr/bin/env python3
"""Preview, install, or remove only this skill's hook in an explicit hooks.json."""
import argparse
from copy import deepcopy
import difflib
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile

from astra import ROOT, load_config

LABEL = "LabKit Astra Prompts v1"


def handler(config):
    return {
        "type": "command",
        "command": shlex.join([sys.executable, str(ROOT / "scripts/astra.py"),
                               "hook", "--config", str(config.resolve())]),
        "timeout": 5,
        "statusMessage": LABEL,
        "additionalContextLimit": 2500,
    }


def update(document, config, remove=False):
    result = deepcopy(document)
    if not isinstance(result, dict):
        raise ValueError("hooks.json must contain an object")
    if remove and "hooks" not in result:
        return result
    events = result.setdefault("hooks", {})
    if not isinstance(events, dict):
        raise ValueError("hooks must be an object")
    groups = events.get("UserPromptSubmit", [])
    if not isinstance(groups, list):
        raise ValueError("UserPromptSubmit must be a list")
    new_groups = []
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            raise ValueError("invalid matcher group")
        if not all(isinstance(h, dict) for h in group["hooks"]):
            raise ValueError("invalid hook handler")
        owned = [h for h in group["hooks"] if h.get("statusMessage") == LABEL]
        if not owned:
            new_groups.append(group)
            continue
        for existing in owned:
            # Refuse ambiguous ownership rather than deleting another handler.
            command = existing.get("command", "")
            if not isinstance(command, str) or "scripts/astra.py" not in command:
                raise ValueError("hook label collision; inspect manually")
        kept = [h for h in group["hooks"] if h.get("statusMessage") != LABEL]
        if kept:
            group["hooks"] = kept
            new_groups.append(group)
    if not remove:
        new_groups.append({"hooks": [handler(config)]})
    if new_groups:
        events["UserPromptSubmit"] = new_groups
    else:
        events.pop("UserPromptSubmit", None)
    # Preserve all unrelated fields and events, including an empty hooks object.
    return result


def write_atomic(path, data, mode):
    fd, name = tempfile.mkstemp(prefix=".astra-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hooks", type=Path, required=True,
                        help="explicit target hooks.json (no automatic global selection)")
    parser.add_argument("--config", type=Path, default=ROOT / "config.json")
    parser.add_argument("--apply", action="store_true", help="write after previewing the diff")
    parser.add_argument("--remove", action="store_true", help="remove only our handler")
    args = parser.parse_args()
    try:
        if os.name == "nt":
            raise ValueError("automatic hook registration currently supports macOS/Linux")
        path = args.hooks.expanduser().absolute()
        if path.name != "hooks.json" or path.is_symlink():
            raise ValueError("target must be a regular hooks.json path, not a symlink")
        if not args.remove:
            load_config(args.config)
        exists = path.exists()
        original = path.read_bytes() if exists else b""
        doc = json.loads(original) if original else {}
        result = update(doc, args.config, args.remove)
        if (args.remove and not exists) or result == doc:
            print("No changes.")
            return 0
        after = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
        print("".join(difflib.unified_diff(
            original.decode().splitlines(True), after.decode().splitlines(True),
            fromfile=str(path), tofile=str(path) + " (proposed)"
        )), end="")
        if not args.apply:
            print("Preview only. Repeat with --apply to write. Then review trust in Codex /hooks.")
            return 0
        path.parent.mkdir(parents=True, exist_ok=True)
        # Detect edits between reading and writing; never overwrite a newer snapshot.
        if path.is_symlink() or path.exists() != exists or (exists and path.read_bytes() != original):
            raise ValueError("hooks.json changed during setup; rerun preview")
        mode = path.stat().st_mode & 0o777 if exists else 0o600
        if exists:
            digest = hashlib.sha256(original).hexdigest()[:16]
            backup = path.with_name(path.name + ".astra-" + digest + ".bak")
            if backup.exists() and backup.read_bytes() != original:
                raise ValueError("backup collision")
            if not backup.exists():
                with backup.open("xb") as stream:
                    stream.write(original)
                backup.chmod(0o600)
            print("Backup:", backup)
        write_atomic(path, after, mode)
        print("Removed registration." if args.remove else
              "Registered; activation still requires Codex hook trust. Open /hooks in the CLI.")
        return 0
    except (OSError, ValueError, TypeError) as error:
        parser.exit(1, "astra-prompts setup: " + str(error) + "\n")


if __name__ == "__main__":
    sys.exit(main())
