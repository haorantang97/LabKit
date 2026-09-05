"""Capability-based setup plans. Detect runtime hints, never installed binaries."""
import json
import os
from pathlib import Path

from astra import ROOT

PROFILES = json.loads((ROOT / "adapters/hosts.json").read_text(encoding="utf-8"))


def detect_host(environ=None):
    env = os.environ if environ is None else environ
    hints = []
    if env.get("CODEX_THREAD_ID"):
        hints.append("codex")
    if env.get("CLAUDECODE") == "1":
        hints.append("claude-code")
    return (hints[0], "runtime environment hint; confirm the active client") if len(hints) == 1 else (
        "generic", "unknown or conflicting runtime hints; specify --host")


def add_arguments(parser):
    parser.add_argument("--host", choices=["auto", *PROFILES], default="auto")
    parser.add_argument("--surface", choices=("desktop", "cli", "ide", "unknown", "cloud"), default="unknown")
    parser.add_argument("--mode", choices=("auto", "rules", "hook", "manual"), default="auto")
    parser.add_argument("--rules-file", type=Path, help="explicit host-loaded instruction file")
    parser.add_argument("--hooks", type=Path, help="explicit Codex hooks.json; selects hook mode")
    parser.add_argument("--export", type=Path, help="write a portable manual prompt pack to this file")
    parser.add_argument("--export-format", choices=("pack", "entry"), default="pack",
                        help="pack is portable; entry is a short local-file rule for UI-only settings")


def plan(host, surface, mode, owner, user=False, rules_file=None, hooks=None, environ=None):
    env = os.environ if environ is None else environ
    evidence = "explicit host selection"
    if host == "auto":
        host, evidence = ("codex", "explicit --hooks path") if hooks else detect_host(env)
    profile = PROFILES[host]
    codex_home = Path(env.get("CODEX_HOME", str(owner / ".codex"))).expanduser().absolute()
    hook_path = Path(hooks).expanduser().absolute() if hooks else (
        codex_home / "hooks.json" if user else owner / ".codex/hooks.json")
    relative = profile["user_rule" if user else "project_rule"]
    rule_path = Path(rules_file).expanduser().absolute() if rules_file else (
        owner / relative if relative else None)
    if host == "codex" and user and not rules_file:
        rule_path = codex_home / "AGENTS.md"
    skill_dir = profile.get("user_skill_dir", profile["skill_dir"]) if user else profile["skill_dir"]
    if user and host in ("hermes", "openclaw"):
        home_key = "HERMES_HOME" if host == "hermes" else "OPENCLAW_STATE_DIR"
        default_home = owner / (".hermes" if host == "hermes" else ".openclaw")
        skill_dir = str(Path(env.get(home_key, str(default_home))).expanduser().absolute() / "skills")
    if host == "hermes" and not user and not rules_file:
        # Reuse the active context type rather than masking existing project instructions.
        for name in (".hermes.md", "HERMES.md", "AGENTS.override.md", "AGENTS.md", "CLAUDE.md", ".cursorrules"):
            candidate = owner / name
            if candidate.is_file() and candidate.read_text(encoding="utf-8").strip():
                rule_path = candidate
                break
        else:
            if any((owner / ".cursor/rules").glob("*.mdc")):
                raise ValueError("Hermes project already uses Cursor rule modules; choose an explicit active --rules-file to avoid shadowing them")
    if hooks and mode not in ("auto", "hook"):
        raise ValueError("--hooks selects hook mode; omit it for rules/manual mode")
    if mode == "auto":
        # A CLI-shaped command is not evidence that the user uses a terminal UI.
        mode = ("hook" if hooks else "manual" if surface == "cloud" else
                "rules" if rules_file else
                "hook" if host == "codex" and profile["hook_adapter"] and os.name != "nt" else
                "rules" if rule_path else "manual")
    if surface == "cloud" and mode != "manual":
        raise ValueError("cloud surface cannot use this machine's registration; install inside the actual runtime or export a manual pack")
    if mode == "hook" and (host != "codex" or not profile["hook_adapter"] or os.name == "nt"):
        raise ValueError("hook adapter supports Codex on macOS/Linux; use --mode rules or manual")
    if mode == "rules" and rule_path is None:
        raise ValueError("no known rule path for this host/scope; supply --rules-file or use --mode manual")
    if rules_file and mode != "rules":
        raise ValueError("--rules-file requires rules mode")
    return {"host": host, "host_evidence": evidence, "surface": surface, "mode": mode,
            "hook_capability": "adapter_available_runtime_not_verified" if mode == "hook" else "not_probed",
            "fallback_policy": "Ask before changing the selected mode; missing trust is pending setup, not unsupported hooks.",
            "rules_file": str(rule_path) if mode == "rules" else None,
            "hooks_file": str(hook_path) if mode == "hook" else None,
            "rule_format": profile["format"],
            "skill_dir": skill_dir, "native_delivery": "not_verified"}
