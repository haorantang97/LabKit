<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner.svg">
    <img width="700" alt="reading-plan-mentor" src="assets/banner.svg">
  </picture>
</p>

> **Archived repository:** The maintained copy now lives in [`LabKit/skills/reading-plan-mentor`](https://github.com/haorantang97/LabKit/tree/main/skills/reading-plan-mentor). This repository is kept for its history and existing stars.

# Reading Plan Mentor

**English** | [中文](README.zh-CN.md)

[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-blue.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![Last Updated](https://img.shields.io/badge/updated-Jul%202026-blue.svg?style=flat-square)]()

> Turn a booklist into a long-term, mentor-guided daily reading plan, delivered on schedule.

## Install

**Claude Code / Claude Cowork:**

```bash
git clone https://github.com/haorantang97/reading-plan-mentor.git
mkdir -p ~/.claude/skills/reading-plan-mentor
cp -r reading-plan-mentor/SKILL.md reading-plan-mentor/references ~/.claude/skills/reading-plan-mentor/
```

**AGENTS.md (Codex / any agent):**

```bash
cat reading-plan-mentor/SKILL.md >> ~/your-project/AGENTS.md
# keep references/ next to it for the detailed playbooks
```

Built and tested against Claude Code / Cowork (it uses scheduled tasks and email delivery there); on other agents it degrades gracefully to plan design + daily text generation.

## What It Does

Most reading plans die because they are calendars: they don't know Hobbes reads five times slower than a thriller, they collapse the first day you skip, and they never remember what confused you on Tuesday. reading-plan-mentor turns a booklist into a long-running plan with a mentor attached. It first checks whether the books belong together at all, and says so honestly when they don't. Then it schedules each book by its nature, paces by difficulty-weighted time instead of page count, and delivers a daily guided-reading email that answers what you asked yesterday.

## Example

```
"I want to read The Prince, Leviathan, and The Republic
 in 8 weeks, 45 minutes a day."
```

The skill finds the one question these three books share (what makes political power legitimate?), marks which pairs are strong contrasts and which are loose, checks the timeline is actually feasible at your reading speed, then drafts the weekly framework plus a full Day-1 sample email. Nothing auto-sends until you approve both.

Hand it *War and Peace* plus a fantasy webnovel instead, and it refuses to fake a theme: novels run as parallel linear tracks, cut at narrative pauses, never spoiled, never interleaved.

## Features

- Vets the booklist before planning and refuses to invent a thematic thread that isn't there
- Classifies each book on two axes: skippable vs. strictly linear, immersive vs. analytical
- Budgets daily load by difficulty-weighted minutes, never by raw page counts
- Reflows the remaining schedule when you fall behind, want a rest day, or read ahead
- Keeps an explicit cross-text hook ledger so every promised callback is actually honored
- Compresses your offhand chat remarks into memory and echoes them in tomorrow's mail
- Flags uncertain chapter facts instead of asserting them, so daily automation never invents citations

## Structure

```
reading-plan-mentor/
├── SKILL.md                              # workflow: Phase 0 gate → design → confirm → daily loop
└── references/
    ├── book-classifier.md                # two-axis classification, concurrency caps, novel handling
    ├── capacity-and-pacing.md            # difficulty-weighted load model + pacing controller
    ├── email-format-and-voice.md         # seven-block daily template, voice, anti-hallucination
    ├── memory-and-continuity.md          # memory schema, capture-from-chat, callbacks, dashboards
    └── delivery-and-scheduling.md        # channels, self-contained cron rules, idempotency
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

PolyForm Noncommercial License 1.0.0 — see [LICENSE](LICENSE).
