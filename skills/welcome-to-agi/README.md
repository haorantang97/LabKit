# Welcome to AGI

**English** | [中文](README.zh-CN.md)

Route ordinary tasks through relevant official Astra guidance. The current Codex model selects modules before working; users do not need to complain first. No embedding service or extra model API is required.

```text
ordinary prompt -> hook supplies a short catalog -> Codex selects modules
                -> reads selected prompts/guards -> completes the task
```

## Install and initialize

From the LabKit checkout, preview and then apply:

```bash
python3 skills/welcome-to-agi/scripts/install.py --user
python3 skills/welcome-to-agi/scripts/install.py --user --apply
```

For one project, replace `--user` with `--project /path/to/project`. The installer supports macOS/Linux with Python 3.10+. It installs the complete skill and registers its Codex hook. Then **review and trust the definition in Codex CLI `/hooks`**. File installation, registration, and host activation are reported separately.

You can also ask an agent to install `welcome-to-agi` from LabKit and complete initialization according to its SKILL.md. For manually downloaded copies, the first explicit `$welcome-to-agi` invocation guides initialization. Copying files alone cannot execute an install callback. Use `--skill-only` if you explicitly want manual mode.

## Select by task intent

An implementation can use initiative and testing. Independent deliverables may benefit from delegation. Writing may need prose guidance. A simple factual question can use no modules. These are semantic decisions made by the current host model, not hard-coded keyword classifications.

The hook supplies a short catalog on every valid submission for an allowed model. Module bodies are read only when selected. This provides a consistent entrypoint, not guaranteed model correctness.

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
- `initialize.py`: registration/status and next host steps for an installed copy.
- `astra.py router`: preview the actual semantic entrypoint.
- `astra.py compose`: output selected guidance separately from the original prompt.
- `audit.py`: optional read-only scan of explicit configuration paths.

[Setup, migration from astra-prompts, configuration, and removal](references/setup.md).

## Validation and provenance

[Evaluation](references/evaluation.md) separates deterministic script checks, actual model-selection trials, and native host delivery. Codex hook defaults target `gpt-6-astra`; other models require an explicit configuration choice, and other hosts need their own integration.

The five prompt blocks are from [OpenAI's Astra guide](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices), checked 2026-09-05. Routing and onboarding are LabKit additions. See [sources](references/sources.md) and the [PolyForm Noncommercial license](../../LICENSE).
