# Setup and configuration audit

Use this reference only for requested setup/audit work. Downloads and ordinary skill invocations have no initialization side effects. This package has no installation lifecycle event or vector database. Setup and audit are optional tools within the same skill, so the folder remains independently installable.

## Install the complete skill

From a LabKit checkout on macOS/Linux, install in the project where you want to use it:

```bash
mkdir -p /path/to/project/.agents/skills
cp -R skills/astra-prompts /path/to/project/.agents/skills/
```

For user-wide discovery, use `~/.agents/skills/` instead. Check whether the target already exists before copying; preserve customized `config.json`, `guard.md`, and trigger patterns during updates. Install the **entire folder**, not just `SKILL.md`. Do not copy it over `AGENTS.md`. If the skill does not appear, restart Codex and invoke `$astra-prompts` explicitly.

## Choose the activation mechanism

1. **Skill only:** no setup command required. The host may select it from the description or the user can invoke it explicitly. Read enabled modules semantically; scripts are optional.
2. **Codex hook:** deterministic local phrase/regex routing on `UserPromptSubmit`. It appends selected static guidance as extra developer context. The original user message remains unchanged. It does not monitor every tool call, infer unseen behavior, read transcripts, or run other agents.
3. **Persistent instruction snippet:** if explicitly requested, use `compose` to obtain selected guidance, then propose a small identified block in the actual active `AGENTS.md` or developer prompt. Inspect existing instructions first; merge only within the authorized scope. Do not stack a persistent copy and the hook for the same modules without evaluating duplication. This mode is manual and is not installed by `setup_hook.py`.

## Register the optional hook

Python 3.10+ is required. Automatic registration supports macOS/Linux. Windows and other agents can use the skill/prompts, but this package does not ship a validated hook installer for them.

Run from the **installed skill** path so the hook doesn't depend on a temporary checkout:

```bash
python3 /path/to/project/.agents/skills/astra-prompts/scripts/setup_hook.py \
  --hooks /path/to/project/.codex/hooks.json
```

This displays a diff without writing. To apply the concrete registration:

```bash
python3 /path/to/project/.agents/skills/astra-prompts/scripts/setup_hook.py \
  --hooks /path/to/project/.codex/hooks.json --apply
```

For a user-level hook, specify `--hooks ~/.codex/hooks.json`. Pick one scope: Codex loads matching hooks from **all** active sources; it does not replace lower-precedence hooks. Inspect other `hooks.json` files and inline `[hooks]` in active `config.toml` layers to avoid registering this handler twice. The script manages only its labeled handler in the explicitly named JSON file; it does not migrate inline TOML.

Existing JSON settings and other handlers are preserved. On change, the installer writes a content-addressed backup beside the file. Repeating the same registration is a no-op. Generated commands quote the interpreter, script, and configuration paths. Moving the skill requires re-registering it.

**Activation is a separate host step:** open `/hooks` in the Codex CLI to review and trust the exact definition. Project-level hooks also require a trusted project. New or changed definitions may be skipped until trusted. Managed environments may disable hooks. Do not edit trust storage or bypass review. A successful file write means registered, not active.

## Configure modules

Edit the installed `config.json`:

- `modules.<id>.enabled`: toggle the module. All except delegation are enabled initially, but only matching modules are injected.
- `modules.<id>.guard`: toggle the separate LabKit adaptation. Official `prompt.md` blocks stay unchanged. Disabling the delegation guard makes the official encouragement broader; choose this deliberately.
- `models`: exact permitted model slugs for the hook. The default is `gpt-6-astra`. Unknown/missing model values yield no guidance. Add an alias only after confirming what your host sends; do not guess a wildcard.
- `max_modules`: maximum per request (default 3).
- `max_context_chars`: hard character budget (default 12000). Whole modules that do not fit are omitted, never truncated. This is not a token count.

To add a module, create `modules/<id>/{module.json,prompt.md,guard.md}` and add its boolean settings to `config.json`. `module.json` holds `id`, `title`, integer `priority`, arrays `patterns` and `exclude`, and `source`. Use simple bounded regexes; patterns are trusted executable configuration, not user-supplied input. Lower priorities are selected first. To remove one, delete its config entry and optionally its folder; disabled entries need no files.

The hook's matching is deliberately narrower than semantic skill selection. Quoted strings, fenced code, and Markdown block quotes are filtered, but arbitrary pasted text and ambiguous negation can still produce false positives. Retain the scope guards. A vector index would retrieve candidate modules, not provide a hook or a stronger instruction priority; no embeddings or model API calls are needed here.

## Preview selection and composition

```bash
printf '%s' '少点套话，继续完成当前任务。' | python3 scripts/astra.py route
printf '%s' '请解释缓存失效。' | python3 scripts/astra.py compose --modules writing-style
```

`compose` returns JSON with separate `prompt` and `guidance` fields. The prompt field preserves the original input byte-for-byte for valid UTF-8. A custom application should keep these at their appropriate message roles; do not interpolate user input into developer instructions. Explicit `--modules` selection still respects disabled modules and the size/count budgets. Inspect returned `modules` to see what was included.

## Optional one-time audit

```bash
python3 scripts/audit.py /path/to/project/AGENTS.md /path/to/project/.agents/skills
```

Only inspect user-selected paths. Output contains local paths and excerpts; keep reports local unless the user asks to share them. The scanner reports candidate lines, duplicate names/content, aliases, and coverage gaps. It cannot determine active instruction precedence or prove a behavioral defect. It never executes inspected files or edits them.

For each actionable candidate, read enough context to establish the scope. Report the file/line, trigger, likely effect, proposed minimal diff, and how to verify it. Preserve deliberate project gates and existing permissions. A scoped rule, a quoted example, or a duplicate symlink is not automatically a defect. No change is a valid outcome. Apply only authorized concrete changes; this audit does not imply approval to disable skills, remove files, or edit a knowledge base.

## Remove and recover

```bash
python3 scripts/setup_hook.py --hooks /path/to/project/.codex/hooks.json --remove
python3 scripts/setup_hook.py --hooks /path/to/project/.codex/hooks.json --remove --apply
```

Removal affects only this handler in the named file, preserving later unrelated edits. Backups are for inspection/manual recovery; do not overwrite a newer config wholesale. Remove registration before relocating/deleting the skill. Start a fresh conversation to exclude previously injected context; removing the hook cannot erase text already present in an existing conversation. Toggle individual modules in `config.json` for future events. `/hooks` can disable the handler at the host level.
