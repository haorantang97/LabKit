# Installation and first-use initialization

The default experience is **install + initialize**, not “files downloaded, available next turn.” The installer and first-use skill instructions guide setup. Copying files alone cannot execute a lifecycle callback: an agent doing a manual download must read SKILL.md and run the installed initializer, or use the integrated installer below.

## One installation entrypoint

From a LabKit checkout, on macOS/Linux with Python 3.10+:

```bash
python3 skills/welcome-to-agi/scripts/install.py --user
python3 skills/welcome-to-agi/scripts/install.py --user --apply
```

The first command previews paths and configuration. The second installs the complete folder under `~/.agents/skills/welcome-to-agi` and registers the user-level Codex hook. To limit it to one project:

```bash
python3 skills/welcome-to-agi/scripts/install.py --project /path/to/project --apply
```

The project skill goes under `.agents/skills`, with its hook under `.codex/hooks.json`. `--skill-only` explicitly selects manual use. Existing installations are never overwritten by this installer; initialize the installed copy or review an upgrade that preserves customizations.

## Already downloaded / first invocation

Locate the actual installed folder. Run its `scripts/initialize.py` first. It infers a hook target only from standard `.agents/skills` or `.codex/skills` locations; use `--hooks` in a source checkout or custom layout.

```bash
python3 /installed/welcome-to-agi/scripts/initialize.py
python3 /installed/welcome-to-agi/scripts/initialize.py --apply
```

For an explicit target:

```bash
python3 /installed/welcome-to-agi/scripts/initialize.py --hooks /path/to/project/.codex/hooks.json --apply
```

An agent handling installation should explain the detected scope and enabled modules, complete authorized registration, and surface the remaining host-trust step. Do not silently leave initialization for the user to discover. For a normal task without setup authorization, offer initialization once while continuing in manual mode. Respect a user's request to skip setup.

The status report separates:

- `skill_installed`: files can be read.
- `adapter_probe`: the catalog can be generated locally.
- `hook_registered`: exactly one current handler exists in the inspected file.
- `host_trust` and `native_delivery`: remain `not_verified` until separately observed in the host.

No local flag is treated as evidence of native activation. Inspect other active hook sources and inline `[hooks]` before registration; Codex loads all matching sources. The scripts manage only the named JSON file and preserve unrelated handlers. Inline TOML is not automatically migrated.

## Review trust and check delivery

Codex requires review/trust of non-managed hooks. Open `/hooks` in the CLI, review the installed definition, and trust it there. A trusted project is also required for project hooks. Changed definitions can require re-review. Do not edit trust storage or bypass review. Installation authorization does not override a managed restriction.

After trust, submit an ordinary task, such as “implement a function and verify it.” Inspect hook diagnostics for delivery, then verify the selected module files are read and the original task is completed. Record what was actually observed; an adapter probe is not a native end-to-end test. New sessions may be needed after configuration changes.

## Runtime architecture

```text
ordinary user message
  -> UserPromptSubmit
  -> short routing instructions + enabled module descriptions/paths
  -> current Codex chooses zero or more modules by task intent
  -> reads selected official prompts and configured guards
  -> executes the original task
```

The hook runs on each valid submission for a configured model, including simple questions. It does not wait for keywords or complaints. A simple task may select no modules. The hook never echoes the original user text into developer context. It does not call another model, embed messages, inspect transcripts, or start agents. The current model performs the semantic selection and can still make mistakes.

## Configuration and modular editing

`config.json`:

- `routing`: `semantic` by default; `keyword` retains the older narrow phrase-matching mode.
- `modules.<id>.enabled`: whether the module appears in the available catalog. All five are available by default for new installations; this does not select them all.
- `modules.<id>.guard`: whether the separate LabKit conditions must also be read.
- `models`: exact model slugs accepted by the Codex hook, default `gpt-6-astra`. Unknown/missing models skip; add other slugs only after deciding that Astra guidance is appropriate for them.
- `max_modules`: maximum selected modules per task, default 3.
- `max_context_chars`: router/catalog and composed-prompt character budget. Oversized catalogs fail with no injection instead of silently omitting a constraint.

Each `modules/<id>/` contains `module.json`, `prompt.md`, and `guard.md`. Edit `when` for semantic routing; `patterns` and `exclude` only affect keyword mode. Add the module to `config.json` or remove its entry to extend/shrink the skill without editing engine code. Original official prompts and custom conditions remain separate.

Delegation is available in new installs because ordinary tasks may benefit from it. The guard still requires independent bounded work, useful coordination tradeoffs, available tools, and authorization. A no-agent request means no spawning. Plan sessions omit initiative and delegation from the catalog.

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

`router` previews the exact semantic entrypoint without a model call. `route` is explicitly a **legacy keyword diagnostic**, not the semantic selector. `compose` returns separate unchanged `prompt` and `guidance` fields. For custom hosts, place the router in an appropriate persistent instruction or submission middleware and let the host read selected modules. No non-Codex hook adapter is claimed here.

Auditing is optional and read-only. Candidate rules, duplicates, and coverage gaps need contextual review. An audit does not authorize deleting skills, rewriting AGENTS.md, or editing a knowledge base. Keep reports containing local paths/excerpts local unless the user asks to share them.

## Remove

```bash
python3 scripts/setup_hook.py --hooks /path/to/project/.codex/hooks.json --remove
python3 scripts/setup_hook.py --hooks /path/to/project/.codex/hooks.json --remove --apply
```

Removal preserves unrelated edits; backups are written beside changed hook files. Remove registration before moving the skill. Start a fresh conversation to exclude old injected context; removing a hook cannot erase an existing conversation.
