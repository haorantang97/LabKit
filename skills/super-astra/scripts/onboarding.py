"""Read-only facts for conversational setup; never scan skills or execute hooks."""
import json
import os
from pathlib import Path

from astra import load_config, load_module
import hosts
from setup_hook import handler, OWNED_LABELS
import setup_rules


def hook_inventory(path, config):
    result = {"file": str(path), "registration": "unknown", "handlers": [],
              "runtime_enabled": "not_verified", "trust": "not_verified",
              "delivery": "not_verified", "coverage": "named_file_only"}
    try:
        if not path.exists():
            result["registration"] = "absent"
            return result
        document = json.loads(path.read_text(encoding="utf-8"))
        groups_by_event = document.get("hooks", {})
        if not isinstance(groups_by_event, dict):
            raise ValueError("hooks must be an object")
        for event, groups in groups_by_event.items():
            if not isinstance(groups, list):
                raise ValueError("event groups must be a list")
            for group in groups:
                if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                    raise ValueError("invalid hook group")
                for item in group["hooks"]:
                    if not isinstance(item, dict):
                        raise ValueError("invalid handler")
                    owned = item.get("statusMessage") in OWNED_LABELS
                    result["handlers"].append({
                        "event": event, "type": item.get("type"),
                        "owner": "super-astra" if owned else "other",
                        "label": item.get("statusMessage", "unlabelled"),
                        "definition": ("current" if item == handler(config) else "different") if owned else "not_compared",
                    })
        result["registration"] = "present" if result["handlers"] else "absent"
    except (OSError, ValueError, TypeError, AttributeError) as error:
        # Do not leak command text or malformed file contents in the setup summary.
        result.update(registration="unreadable_or_invalid", error=type(error).__name__)
    return result


def snapshot(selected, config, owner, user, settings=None):
    settings = load_config(config) if settings is None else settings
    modules = []
    for name, value in settings["modules"].items():
        try:
            meta, _ = load_module(name)
        except (OSError, ValueError, TypeError, KeyError):
            if value["enabled"]:
                raise
            # Disabled modules may be physically removed from a custom bundle.
            meta = {"title": name}
        modules.append(dict(id=name, title=meta.get("title", name),
                            enabled=value["enabled"], guard=value["guard"]))
    hooks = {"registration": "not_inspected", "runtime_enabled": "not_verified",
             "trust": "not_verified", "delivery": "not_verified",
             "reason": "No hook inventory adapter for this host/surface; this does not mean hooks are disabled."}
    if selected["host"] == "codex" and selected["surface"] != "cloud" and os.name != "nt":
        path = Path(selected["hooks_file"]) if selected["hooks_file"] else Path(
            hosts.plan("codex", selected["surface"], "hook", owner, user)["hooks_file"])
        hooks = hook_inventory(path, config)
    rule_file = selected["rules_file"]
    if not rule_file and selected["host"] == "codex" and selected["surface"] != "cloud":
        rule_file = hosts.plan("codex", selected["surface"], "rules", owner, user)["rules_file"]
    rule = {"file": rule_file, "registration": "not_inspected"}
    if rule["file"]:
        try:
            path = Path(rule["file"])
            text = path.read_text(encoding="utf-8") if path.exists() else ""
            rule["registration"] = "present" if setup_rules.has_managed_rule(text) else "absent"
        except (OSError, UnicodeError):
            rule["registration"] = "unreadable"
    return {
        "read_only": True, "modules": modules, "config_file": str(config),
        "module_policy": "New installs enable all modules; upgrades preserve existing choices. Enabled means available for selection, not forced use or host multi-agent enablement.",
        "rules": rule, "hooks": hooks,
        "audit": {"status": "not_run", "choice": "ask_user",
                  "scope": "Agree on instruction files and skill directories before running audit.py."},
        "guide": "references/onboarding.md",
        "next_step": "Present these facts and ask together about module changes, optional audit and routing changes. Honor choices already given; registration alone is not completed onboarding.",
    }
