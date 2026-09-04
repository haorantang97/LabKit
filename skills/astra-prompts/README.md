# Astra Prompts

**English** | [中文](README.zh-CN.md)

Apply the relevant official GPT-6 Astra prompt blocks when a user asks for a behavior change. Five independent modules, a normal skill entrypoint, and an optional Codex hook. Setup and configuration auditing are optional tools in the same folder.

## Start with the skill

From the LabKit checkout, copy the complete folder into a project:

```bash
mkdir -p /path/to/project/.agents/skills
cp -R skills/astra-prompts /path/to/project/.agents/skills/
```

Check for an existing installation before copying so you preserve local customizations. For user-wide discovery, use `~/.agents/skills/` instead. Invoke explicitly if needed:

```text
$astra-prompts 少点套话，继续完成当前任务。
```

The agent selects the applicable modules and continues the original task. It can also select the skill implicitly from a matching behavior request, such as “stop asking and finish the task” or “avoid redundant tests.” Implicit selection is a model decision, not a guaranteed lifecycle trigger. Ordinary requests do not need this skill.

## Modules

| Module | Intended adjustment | Default |
|---|---|---|
| `initiative` | Complete authorized work; reduce unnecessary approval pauses | On when matched |
| `instruction-following` | Explain conflicts and respect instruction precedence | On when matched |
| `writing-style` | Clearer, concise prose with less jargon | On when matched |
| `testing` | Match verification to the change; stop redundant checks | On when matched |
| `delegation` | Tune use of parallel subagents | **Off** |

The official delegation prompt encourages **more** delegation. LabKit supplies a separate scope guard, and keeps this module opt-in. Each module has three files:

```text
modules/writing-style/
  module.json   # routing patterns, priority, source
  prompt.md     # official prompt blocks, unchanged
  guard.md      # separately labeled LabKit adaptation
```

Edit `config.json` to enable/disable modules or adaptations. Edit `module.json` to change matching. Add or remove a module without editing the engine. The hook uses simple local regexes, no vector store or API calls. Semantic intent selection is provided by the skill's host model.

## Optional automatic hook

Codex's `UserPromptSubmit` hook can add selected guidance before a request reaches the model. It retains the user message and adds only static module text as separate developer context. It does not run an agent or scan the transcript.

Preview from the installed copy:

```bash
python3 /path/to/project/.agents/skills/astra-prompts/scripts/setup_hook.py \
  --hooks /path/to/project/.codex/hooks.json
```

Repeat with `--apply` to register it. Then review and trust the definition through `/hooks` in Codex CLI. Downloads and first use do not automatically install or trust it. Use one scope to avoid duplicate hooks. Python 3.10+ and macOS/Linux are required for this installer.

The hook only injects on configured phrases and allowed model slugs (`gpt-6-astra` by default). It skips unknown models, limits context size, and omits initiative/delegation in a plan session. An error yields no guidance and does not block the user's request. Regex matching can still miss intent or match pasted prose; it is not a behavior detector.

[Setup, customization, removal, and optional one-time audit](references/setup.md)

## Inspect or compose a prompt

From this skill folder:

```bash
printf '%s' '少点套话，继续完成当前任务。' | python3 scripts/astra.py route
printf '%s' 'Explain cache invalidation.' | python3 scripts/astra.py compose --modules writing-style
python3 scripts/audit.py /path/to/project/AGENTS.md /path/to/project/.agents/skills
```

Composition returns separate `prompt` and `guidance` JSON fields. Auditing is read-only: it reports candidate rules, duplicate entries, and gaps for contextual review. It never rewrites global instructions, deletes skills, or treats a candidate match as a proven defect.

## Validation and sources

[Evaluation cases and observed results](references/evaluation.md) distinguish script tests, a bounded independent agent trial, and the native hook smoke test users can run after trusting their installation. Native hook delivery was not tested in a trusted live Codex session for this release; no performance or token-saving claim is made.

[Official sources and snapshot](references/sources.md). Prompt blocks come from [OpenAI's Astra guide](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices), checked 2026-09-05. Routing, guards, setup and auditing are LabKit additions. Original LabKit code uses the repository's [PolyForm Noncommercial license](../../LICENSE); third-party prompt attribution is retained.
