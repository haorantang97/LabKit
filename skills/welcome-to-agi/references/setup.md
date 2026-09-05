# Installation and first-use initialization

The default experience is install + choose an appropriate entrypoint. Copying files alone cannot execute a callback: an agent downloading this package must read SKILL.md and complete authorized initialization. See [the desktop and host guide](hosts.md) before choosing paths.

## Desktop-first setup

Users can ask their agent to install Welcome to AGI for their client and project; the agent runs the commands below when tools permit. A user does not need to operate a terminal for rules mode. The client loads a short persistent instruction; the current model reads module metadata and selects useful guidance for ordinary tasks.

From a LabKit checkout, Python 3.10+ (scripts tested on macOS/Linux):

```bash
python3 skills/welcome-to-agi/scripts/install.py --host codex --surface desktop --project /path/to/project
python3 skills/welcome-to-agi/scripts/install.py --host codex --surface desktop --project /path/to/project --apply
```

The first command previews paths; the second installs and initializes. Auto mode prefers **rules** for known local hosts. This is a change from the old unconditional hook default. Use `--user` instead of `--project PATH` for user scope. No other skills or instructions are cleaned.

Other project hosts use the same entrypoint:

```bash
python3 skills/welcome-to-agi/scripts/install.py --host claude-code --surface desktop --project /path/to/project --apply
python3 skills/welcome-to-agi/scripts/install.py --host cursor --surface desktop --project /path/to/project --apply
```

Codex and Cursor packages go into `.agents/skills/welcome-to-agi`; Claude Code uses `.claude/skills/welcome-to-agi`. Cursor integration relies on the generated rule's explicit paths, not a claim about skill autodiscovery. Existing skill destinations are never overwritten; initialize that copy or review an upgrade preserving its config. Unknown clients default to manual, visibly reporting that automatic routing is absent. `--host auto` uses limited runtime hints, not installed binary discovery; pass the actual host whenever known.

## Already downloaded / first invocation

Run from the actual installed copy with the host and scope:

```bash
python3 /installed/welcome-to-agi/scripts/initialize.py --host codex --surface desktop --project /path/to/project
python3 /installed/welcome-to-agi/scripts/initialize.py --host codex --surface desktop --project /path/to/project --apply
```

Without `--apply`, rules/hook changes are shown as a diff and not written. Standard installed directories allow scope inference; source checkouts and custom layouts need explicit scope or target. Use `--user` to select the active Codex profile's AGENTS.md when CODEX_HOME is nondefault. Rule writes preserve surrounding bytes, back up previous contents, and update only one marked block. Damaged markers, symlinks and shadowed Codex targets produce an actionable error.

For ordinary tasks without setup authorization, offer initialization once while continuing manually; honor declined setup. An install request authorizes our scoped registration, not unrelated configuration cleanup or bypassing host permissions.

## Capabilities and fallbacks

| Mode | Selection | Result |
|---|---|---|
| `auto` | Rules for a known local host/scope; otherwise manual | No assumption that a desktop user uses CLI |
| `rules` | Codex, Claude Code, Cursor project; or explicit custom file | Persistent entry, model-driven per-task assessment |
| `hook` | Explicit Codex selection, macOS/Linux | UserPromptSubmit entry, separate trust required |
| `manual` / `--skill-only` | Any host | No registration; explicit use or portable export |

For an agent with a known always-loaded file but no built-in adapter:

```bash
python3 scripts/initialize.py --host generic --mode rules --rules-file /path/to/host-instructions.md --apply
```

The file must actually be loaded by the host. Writing an arbitrary file cannot make a closed application read it. If settings are UI-only, export a short entry and paste it into that client's persistent instructions; verify the file paths remain readable. Cursor user scope defaults to manual rather than modifying its internal settings database:

```bash
python3 scripts/initialize.py --host cursor --user --mode manual --export /path/to/local-rule.txt --export-format entry --apply
```

This entry contains local paths. It is for a client that can read the installed folder; use the default portable `pack` format for a chat client without that ability. Exporting an entry does not apply it to GUI settings automatically.

For chat/cloud clients without local file access:

```bash
python3 scripts/initialize.py --host generic --surface cloud --mode manual --export /path/to/welcome-prompt-pack.md
python3 scripts/initialize.py --host generic --surface cloud --mode manual --export /path/to/welcome-prompt-pack.md --apply
```

Attach that self-contained Markdown pack to the actual conversation and ask the model to use relevant sections while completing tasks. The export includes all enabled module bodies (more context than dynamic loading), no machine-specific file paths, and no automatic persistence promise. Re-export after config edits. Installing the pack does not provide missing tools or change the model. An existing export is not overwritten.

## Optional Codex hook

```bash
python3 scripts/initialize.py --host codex --mode hook --project /path/to/project --apply
# Equivalent explicit target (backward compatible):
python3 scripts/initialize.py --hooks /path/to/project/.codex/hooks.json --apply
```

Use Codex CLI `/hooks` to review/trust the exact definition in the SAME runtime/profile as the actual client. Shared agent configuration is documented, but CLI registration/trust alone does not establish desktop delivery. Desktop users can use rules without this step. Project hooks also need project trust; changed definitions may require review again. Never edit trust storage or bypass review.

The hook handles valid UserPromptSubmit events for configured models, supplies a short catalog, and leaves semantic selection to the current model. It does not copy user text into developer context, call another classifier, read transcripts, or launch agents. Unknown models skip. Errors fail open with no guidance so the original task can continue.

## Status and actual-client verification

Status distinguishes `host`/`host_evidence`, `surface`, selected `mode`, exact target, `skill_installed`, `adapter_probe`, `rules_registered`/`hook_registered`, `host_trust` and `native_delivery`. Trust is not applicable for rules/manual; hook trust remains unverified. `native_delivery` remains `not_verified` because local file checks cannot observe your client.

Follow [hosts.md](hosts.md#在实际使用的客户端验证): start a fresh conversation in the real desktop/CLI client, inspect loaded sources, submit an ordinary task without naming this skill, and observe module reads and the delivered result. A passing script test is not a native host test. Scope, active profile, remote runtime, context limits and overrides can affect loading.

## Configuration and modular editing

`config.json`:

- `routing`: `semantic` by default; `keyword` retains the older narrow phrase-matching mode.
- `modules.<id>.enabled`: whether the module appears in the available catalog. All five are available by default for new installations; this does not select them all.
- `modules.<id>.guard`: whether the separate LabKit conditions must also be read.
- `models`: exact model slugs accepted by the Codex hook, default `gpt-6-astra`. Unknown/missing models skip; add other slugs only after deciding that Astra guidance is appropriate for them.
- `max_modules`: maximum selected modules per task, default 3.
- `max_context_chars`: router/catalog and composed-prompt character budget. Oversized catalogs fail with no injection instead of silently omitting a constraint.

Each `modules/<id>/` contains `module.json`, `prompt.md`, and `guard.md`. Edit `when` for semantic routing; `patterns` and `exclude` only affect keyword mode. Add the module to `config.json` or remove its entry to extend/shrink the skill without editing engine code. Original official prompts and custom conditions remain separate.

Delegation is available in new installs because ordinary tasks may benefit from it. The guard still requires independent bounded work, useful coordination tradeoffs, available tools, and authorization. A no-agent request means no spawning. Plan sessions omit initiative and delegation: programmatically in hook mode, by the routing instructions in rules mode.

## Upgrade from astra-prompts

The new name is `welcome-to-agi`. Preserve customized configuration and modules, and remove the old discoverable entry after backing it up outside skill discovery directories. Do not install two competing copies. `setup_hook.py` recognizes the old `LabKit Astra Prompts v1` registration and replaces it with one current handler in the same JSON file. If the hook lives in another source, migrate that source explicitly too. Review/trust the updated definition again.

The new default enables delegation as a candidate; retaining an older explicit disabled setting is supported. Select `routing: semantic` to get ordinary-task routing. Official prompt bodies are unchanged.

## Standalone tools and optional audit

From the skill directory:

```bash
python3 scripts/astra.py router
printf '%s' 'Explain cache invalidation.' | python3 scripts/astra.py compose --modules writing-style
printf '%s' '少点套话' | python3 scripts/astra.py route
python3 scripts/audit.py /path/to/project/AGENTS.md /path/to/project/.agents/skills
```

`router` previews the exact semantic entrypoint without a model call. `route` is explicitly a **legacy keyword diagnostic**, not the semantic selector. `compose` returns separate unchanged `prompt` and `guidance` fields. For custom hosts, use `--host generic --mode rules --rules-file PATH` for a file the host already loads, or export a portable manual pack. No non-Codex hook adapter is claimed here.

Auditing is optional and read-only. Candidate rules, duplicates, and coverage gaps need contextual review. An audit does not authorize deleting skills, rewriting AGENTS.md, or editing a knowledge base. Keep reports containing local paths/excerpts local unless the user asks to share them.

## Remove or switch mode

Run from the installed skill folder; retain the same host, scope, and any explicit path used during setup:

```bash
python3 scripts/initialize.py --host codex --project /path/to/project --mode rules --remove
python3 scripts/initialize.py --host codex --project /path/to/project --mode rules --remove --apply
python3 scripts/initialize.py --hooks /path/to/project/.codex/hooks.json --remove --apply
```

Replace codex with claude-code or cursor for those rule adapters. For a custom target, also supply `--rules-file PATH`. First remove the old mode, then initialize the new one. Known Welcome hook/rule conflicts stop setup rather than silently stacking two registrations. Check additional configuration layers yourself; only the named target is managed. Removing a hook does not revoke or change trust storage.

Removal preserves surrounding instructions and later edits. Backups remain beside modified files; remove registration before moving the skill. Start a fresh conversation to exclude old context. A portable export has no automatic registration to remove; stop attaching it and start a fresh chat.
