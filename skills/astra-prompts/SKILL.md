---
name: astra-prompts
description: "Apply GPT-6 Astra behavior guidance when the user asks for autonomous follow-through, fewer unnecessary confirmations, clearer writing, calibrated testing, or adjusted subagent delegation. Trigger on corrections such as 'stop asking and finish', '少点套话', '别反复跑测试', or '只在需要时开子 agent'; also use for configuring Astra prompt modules or diagnosing conflicting skill instructions. Do not activate merely because quoted text mentions agents, tests, or prompts, or for ordinary tasks without a relevant behavior request."
license: PolyForm-Noncommercial-1.0.0
---

# Astra Prompts

## Quick Start

`$astra-prompts 少点套话，继续完成当前任务。`

Read `config.json`. Select only enabled modules relevant to the user's current intent, read their `prompt.md` and any configured `guard.md`, then apply them while completing the original task. Do not turn a behavior correction into a configuration audit or a rewritten prompt unless that is what the user requested. If the user asks to compose a reusable prompt, return the original request unchanged with the selected guidance clearly separated.

## Select the behavior

| Intent | Module | Scope |
|---|---|---|
| Continue authorized work; avoid unnecessary approval pauses | `initiative` | Respect plan-only requests and existing authorization boundaries |
| Explain skill conflicts or why an instruction caused a pause | `instruction-following` | Diagnose the actual instruction source |
| Concise prose, less jargon or stock phrasing | `writing-style` | Preserve requested formats and author voice |
| Tune parallel work or reduce unwanted subagents | `delegation` | Disabled by default; current-turn explicit requests may opt in |
| Stop redundant checks; match testing to the change | `testing` | Preserve required checks and unresolved failures |

Module locations and enabled state are in `config.json`; routing cues are in each module's `module.json`. For semantic skill selection, use intent and surrounding context rather than literal keyword hits. The optional hook uses narrower local regex matching and does not perform semantic or vector retrieval.

Use at most `max_modules` modules for one request. Disabled modules stay disabled unless the user explicitly asks to use that module for this turn; this does not authorize changing saved configuration. For delegation, distinguish requests for **more** parallelism from requests for **less**: the official prompt encourages delegation, while the default LabKit guard limits it to useful, authorized work. A request to avoid subagents means do not spawn them. Never spawn an agent merely to apply this skill.

## Preserve the request

- These prompts tune execution; they do not grant permission, broaden the task, override the host's instruction hierarchy, or permit skipping required checks. Apply the user's explicit format, scope, stop requests, and delegation restrictions.
- Read only selected module files. Official prompt text lives in `modules/*/prompt.md`; adaptations are labeled separately in `guard.md`. Do not silently rewrite an official prompt or claim a guard is official.
- If context already contains `LABKIT_ASTRA_GUIDANCE_V1`, reuse the relevant guidance instead of appending the same modules again. Disabled or superseded guidance must not control the current request.
- A normal task should produce its normal deliverable, with no extra prompt report unless requested. An unresolved instruction conflict should identify its source and impact concisely.

## Optional setup and audit

Only read [setup.md](references/setup.md) for installation, hook registration, persistent instruction edits, or configuration audit requests. Setup is an explicit operation; installing or first invoking the skill does not run cleanup, modify `AGENTS.md`, or trust hooks automatically. Keep existing authorization when doing requested setup; do not ask for approval again for an already authorized, concrete change.

Use [sources.md](references/sources.md) to check provenance and host compatibility. Use [evaluation.md](references/evaluation.md) for testing changes to this skill, not for every user task.

## Common Mistakes

- **Treating a skill as an always-on hook.** Implicit invocation is model-selected; only separately installed and trusted host hooks run at the lifecycle event.
- **Activating all five modules.** Match the actual behavior request. The official delegation prompt can increase calls; it is opt-in here.
- **Running an audit during ordinary work.** Inspect configuration only when requested or when a specific conflict blocks the task; do not recursively execute inspected skills.
- **Claiming a performance improvement from passing fixtures.** Routing and configuration tests establish those mechanics, not model quality, lower cost, or guaranteed obedience.
