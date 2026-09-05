# Welcome to AGI

**English** | [中文](README.zh-CN.md)

Route ordinary tasks through relevant official Astra guidance. The current agent model selects modules before working; users do not need to complain first. No embedding service or extra model API is required.

```text
ordinary prompt -> persistent rule or optional hook -> current model selects
                -> reads selected prompts/guards -> completes the task
```

## Install and initialize

In a desktop agent, ask:

> Install LabKit's welcome-to-agi for my current client and project. Complete initialization, preserve existing instructions, and explain what remains to verify in this client.

The agent can run the installer for you. It chooses a persistent rule for supported local hosts; **you do not need CLI hook setup for rules mode**. Copying files alone cannot execute initialization, so a downloader should follow SKILL.md.

First-use guidance lists the five module switches and current hook registration facts, then asks which modules to turn off, whether to check existing Skills and instruction conflicts, and whether to adjust routing. All five modules, including delegation, start enabled in a new install; existing preferences survive upgrades. Enabled modules are selected only when useful, and delegation does not enable a host's multi-agent feature. The audit runs only if chosen. [Initialization conversation](references/onboarding.md).

| Client | Implemented entrypoint |
|---|---|
| Local Codex desktop / CLI / IDE | Scoped AGENTS.md block; optional Codex hook |
| Claude Code Desktop / CLI | Scoped CLAUDE.md block |
| Cursor project Agent | Always Apply .mdc rule |
| Other local file-reading agents | Explicit host-loaded rule file |
| UI-only settings / chat / cloud | Short rule export or portable manual prompt pack |

[Client-specific guidance, limitations and actual-client verification](references/hosts.md).

From a LabKit checkout, preview and then apply (Python 3.10+, scripts tested on macOS/Linux):

```bash
python3 skills/welcome-to-agi/scripts/install.py --host codex --surface desktop --project /path/to/project
python3 skills/welcome-to-agi/scripts/install.py --host codex --surface desktop --project /path/to/project --apply
```

Use `--host claude-code` or `--host cursor` for those clients. `--user` selects user scope instead of `--project PATH`; Cursor user scope exports manually instead of editing the app settings database. Unknown hosts fall back to clearly labeled manual mode. `--mode hook` explicitly opts into the Codex adapter and its separate trust review. `--skill-only` means manual mode.

## Select by task intent

An implementation can use initiative and testing. Independent deliverables may benefit from delegation. Writing may need prose guidance. A simple factual question can use no modules. These are semantic decisions made by the current host model, not hard-coded keyword classifications.

Rules ask the model to read current config and module descriptions each task; hooks supply a short catalog on each valid submission for an allowed model. Selected module bodies are read as needed. Rules rely on instruction adherence, hooks provide an event entrypoint, and neither guarantees correct model decisions. Manual packs include all enabled bodies and require re-export after edits.

| Module | Intended use |
|---|---|
| `initiative` | Complete authorized multi-step work |
| `instruction-following` | Resolve relevant instruction conflicts |
| `writing-style` | Clear writing, explanations, and summaries |
| `delegation` | Useful, permitted independent subtasks |
| `testing` | Proportional meaningful verification |

All five are available by default in new installs; availability does not mean selection or spawning. The delegation guard preserves user restrictions, tool permissions, and coordination tradeoffs.

## Modular configuration

Each module has `module.json` (including semantic `when`), `prompt.md` (official blocks), and `guard.md` (separate LabKit conditions). Toggle modules in `config.json`. Add/remove modules without changing the engine. `routing: keyword` retains the older optional regex mode; semantic routing is the default.

## Included tools

- `install.py`: complete-folder installation followed by initialization.
- `initialize.py`: rules/hook setup, scoped removal, manual exports, and `--onboarding` read-only module/hook facts.
- `onboarding.py`: separate inventory component for the initialization conversation; no Skill scan or hook execution.
- `adapters/hosts.json`: independently editable host profiles.
- `astra.py router`: preview the actual semantic entrypoint.
- `astra.py compose`: output selected guidance separately from the original prompt.
- `audit.py`: read-only scan of agreed configuration paths, offered during onboarding and run only if chosen.

[Setup, migration from astra-prompts, configuration, and removal](references/setup.md).

## Validation and provenance

[Evaluation](references/evaluation.md) separates deterministic script checks, actual model-selection trials, and native host delivery. Codex hooks filter `gpt-6-astra` by default. Rules can deliver the guidance to other models, which must judge its applicability; this does not switch models or add tools. File adapter tests pass, but native desktop loading has not been verified across these clients.

The five prompt blocks are from [OpenAI's Astra guide](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices), checked 2026-09-05. Routing and onboarding are LabKit additions. See [sources](references/sources.md) and the [PolyForm Noncommercial license](../../LICENSE).
