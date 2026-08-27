<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner.svg">
    <img width="700" alt="LabKit" src="assets/banner.svg">
  </picture>
</p>

# LabKit

**English** | [中文](README.zh-CN.md)

[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-blue.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![Last Updated](https://img.shields.io/badge/updated-Jul%202026-blue.svg?style=flat-square)]()

> Take a working AI rule file from local draft to a published GitHub repo.

## Install

```bash
git clone https://github.com/haorantang97/LabKit.git
cd LabKit
```

LabKit exposes three top-level skills. `skill-skill` is one complete publishing toolkit; its pipeline modules live under `skills/skill-skill/modules/` and are not separate top-level skills.

Each top-level `SKILL.md` is plain markdown with YAML front matter. Drop the one you want into whichever agent you use:

| Agent | Where to put it |
|---|---|
| Claude Code | `cp -r skills/* ~/.claude/skills/` |
| Cursor | `cp skills/{name}/SKILL.md ~/your-project/.cursor/rules/{name}.mdc` |
| Windsurf | `cat skills/{name}/SKILL.md >> ~/your-project/.windsurfrules` |
| GitHub Copilot | `cp skills/{name}/SKILL.md ~/your-project/.github/copilot-instructions.md` |
| Codex / AGENTS.md | `cp skills/{name}/SKILL.md ~/your-project/AGENTS.md` |

The three top-level skills are independent. Install only the ones you want.

## What it does

LabKit is a small collection of three original personal skills. `skill-skill` is the publishing toolkit; `open-loops` and `reading-plan-mentor` are standalone daily-use tools.

## Skills

- **[skill-skill](skills/skill-skill/SKILL.md)** — Packages a working AI rule or skill and guides it through publication as a GitHub repository

- **[open-loops](skills/open-loops/SKILL.md)** — Audits long conversations for unanswered, unacknowledged, or assistant-decided information points
- **[reading-plan-mentor](skills/reading-plan-mentor/SKILL.md)** — Turns a book list into a paced, long-term reading plan with daily guidance and continuity

These two skills are also maintained in their standalone repositories: [open-loops](https://github.com/haorantang97/open-loops) and [reading-plan-mentor](https://github.com/haorantang97/reading-plan-mentor).

## File format

```
skills/{name}/SKILL.md
```

YAML front matter (`name`, `description`, `license`) followed by markdown:

```yaml
---
name: skill-name
description: "Use when the skill's triggering conditions match the user's request."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start
...
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

PolyForm Noncommercial License 1.0.0. See [LICENSE](LICENSE).
