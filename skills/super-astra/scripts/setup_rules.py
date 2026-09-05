"""Manage only the Super Astra block; preserve surrounding instruction bytes."""
import difflib
import hashlib
import json
from pathlib import Path

from astra import ROOT, ROUTER_MARKER, load_config, load_module
from setup_hook import write_atomic

BEGIN = "\n<!-- BEGIN LABKIT_SUPER_ASTRA_RULE_V1 -->\n"
END = "<!-- END LABKIT_SUPER_ASTRA_RULE_V1 -->\n"
# Read old registrations for migration/removal; always emit the current markers.
LEGACY_BEGIN = "\n<!-- BEGIN LABKIT_WELCOME_TO_AGI_RULE_V1 -->\n"
LEGACY_END = "<!-- END LABKIT_WELCOME_TO_AGI_RULE_V1 -->\n"
MARKER_PAIRS = ((BEGIN, END), (LEGACY_BEGIN, LEGACY_END))
CURSOR_HEADER = '---\ndescription: Super Astra task routing\nalwaysApply: true\n---\n'
LEGACY_CURSOR_HEADER = '---\ndescription: Welcome to AGI task routing\nalwaysApply: true\n---\n'


def entry(config, root=ROOT):
    # Keep metadata live: disabling/adding a module must not require reinstalling a rule.
    return (
        "Super Astra: before each ordinary task, assess useful guidance without waiting for a keyword. "
        f"If this turn already has {ROUTER_MARKER} or an earlier version of this skill's router catalog, "
        "use that catalog and do not route twice. "
        "Otherwise read the current config file " + json.dumps(str(config.resolve()), ensure_ascii=False) +
        " and each enabled module's module.json under " + json.dumps(str(root / "modules"), ensure_ascii=False) +
        ". Follow " + json.dumps(str(root / "references/router.md"), ensure_ascii=False) +
        "; select zero to max_modules by task intent, then read only selected prompt.md and enabled guard.md files. "
        "Use max_context_chars as the combined selected-guidance character budget; keep whole modules. "
        "Do not use disabled modules retained from earlier turns. Reuse unchanged module bodies when appropriate. "
        "This is an installed persistent routing entry, so skip onboarding during ordinary tasks. "
        "Apply only guidance suitable for the current model and available tools; config.models is the Codex hook filter, "
        "not a model switch. Respect user restrictions, plan-only scope, permissions and no-subagent requests. "
        "Do not start agents to classify a task. If referenced files are unavailable, continue the original task "
        "under existing instructions and explain the limitation when relevant.\n"
    )


def has_managed_rule(text):
    # Include damaged markers so hook setup cannot stack over an ambiguous rule.
    return any(marker.strip().removesuffix(" -->") in text
               for pair in MARKER_PAIRS for marker in pair)


def transform(original, body, fmt="markdown", remove=False):
    found = []
    for begin, end in MARKER_PAIRS:
        starts, ends = original.count(begin), original.count(end)
        # Catch damaged, mismatched or duplicated markers across both versions.
        if (original.count(begin.strip().removesuffix(" -->")) != starts or
                original.count(end.strip().removesuffix(" -->")) != ends or
                starts != ends or starts > 1):
            raise ValueError("ambiguous managed rule markers; inspect the file")
        if starts:
            found.append((begin, end))
    if len(found) > 1:
        raise ValueError("ambiguous managed rule markers; inspect the file")
    if found:
        if fmt == "cursor" and not remove and not original.startswith((CURSOR_HEADER, LEGACY_CURSOR_HEADER)):
            raise ValueError("Cursor rule header changed; inspect Always Apply settings before updating")
        if fmt == "cursor" and not remove and original.startswith(LEGACY_CURSOR_HEADER):
            original = CURSOR_HEADER + original[len(LEGACY_CURSOR_HEADER):]
        begin_marker, end_marker = found[0]
        start, end = original.index(begin_marker), original.index(end_marker)
        if end < start:
            raise ValueError("reversed managed rule markers")
        end += len(end_marker)
        replacement = "" if remove else BEGIN + body + END
        return original[:start] + replacement + original[end:]
    if remove:
        return original
    if fmt == "cursor":
        if original and original != CURSOR_HEADER:
            raise ValueError("dedicated Cursor rule exists without our block; choose another path")
        return CURSOR_HEADER + BEGIN + body + END
    return original + BEGIN + body + END


def prepare(path, config, fmt="markdown", remove=False):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError("rule target must be a regular file, not a symlink")
    if not remove and path.name == "AGENTS.md":
        override = path.with_name("AGENTS.override.md")
        if override.exists() and override.read_text(encoding="utf-8").strip():
            raise ValueError("AGENTS.override.md shadows this target; inspect it and explicitly select the active --rules-file")
    original = path.read_bytes() if path.exists() else b""
    after = transform(original.decode("utf-8"), entry(config), fmt, remove).encode("utf-8")
    return original, after


def save(path, original, after):
    if original == after:
        return
    existed = path.exists()
    if path.is_symlink() or (path.read_bytes() if existed else b"") != original:
        raise ValueError("target changed during setup; rerun preview")
    path.parent.mkdir(parents=True, exist_ok=True)
    if existed:
        backup = path.with_name(path.name + ".super-astra-" + hashlib.sha256(original).hexdigest()[:16] + ".bak")
        if backup.is_symlink() or (backup.exists() and backup.read_bytes() != original):
            raise ValueError("backup collision")
        if not backup.exists():
            with backup.open("xb") as stream:
                stream.write(original)
            backup.chmod(0o600)
    write_atomic(path, after, (path.stat().st_mode & 0o777) if existed else 0o600)


def manage(path, config, fmt="markdown", apply=False, remove=False):
    before, after = prepare(path, config, fmt, remove)
    print("".join(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True),
                                     fromfile=str(path), tofile=str(path) + " (proposed)")), end="")
    if apply:
        save(path, before, after)
    return {"rules_registered": after == before and BEGIN.encode() in before if not apply else (
            not remove and BEGIN.encode() in after), "changed": before != after}


def manual_pack(config):
    settings = load_config(config)
    text = ("# Super Astra — portable manual pack\n\n"
            "Use this pack for tasks in this conversation. Select zero to " + str(settings["max_modules"]) +
            " useful modules by intent; a simple request may need none. Read selected sections below. "
            "Preserve the original task, output format, permissions, plan-only scope and delegation restrictions. "
            "Do not spawn agents for routing. These are Astra-oriented prompts, not a model switch. "
            "This is a static export: all enabled bodies occupy context; editing config requires re-export. "
            "Attaching this file does not enable future conversations automatically.\n")
    for name, setting in settings["modules"].items():
        if setting["enabled"]:
            meta, folder = load_module(name)
            text += "\n## " + name + "\n\nWhen useful: " + meta["when"] + "\n"
            if setting["guard"]:
                text += "\nLabKit conditions:\n" + (folder / "guard.md").read_text(encoding="utf-8")
            text += "\nOfficial source: " + meta["source"] + "\n" + (folder / "prompt.md").read_text(encoding="utf-8")
    return text
