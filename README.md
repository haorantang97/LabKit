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
[![Last Updated](https://img.shields.io/badge/updated-Sep%202026-blue.svg?style=flat-square)](https://github.com/haorantang97/LabKit/commits/main)

> Reusable agent skills for publishing, everyday work, and configurable Astra behavior.

**New: [Welcome to AGI](skills/welcome-to-agi/README.md)** packages five official GPT-6 Astra prompt modules with individual switches, ordinary-task semantic routing, guided initialization, and a read-only configuration audit. [中文介绍](skills/welcome-to-agi/README.zh-CN.md)

## Install

```bash
git clone https://github.com/haorantang97/LabKit.git
cd LabKit
```

LabKit exposes four top-level skills. `skill-skill` is one complete publishing toolkit; its pipeline modules live under `skills/skill-skill/modules/` and are not separate top-level skills. Astra's behavior modules are also internal to one skill.

Each top-level skill has a `SKILL.md` entrypoint. Install the **complete folder**, including any scripts and references. For Codex, copy the chosen skill into your project's skill directory:

```bash
python3 skills/welcome-to-agi/scripts/install.py --project /path/to/project --apply
```

Use `--user` instead of `--project` for user-wide installation. Complete host trust via Codex `/hooks` after registration. Check existing installations before copying to preserve customizations. For other hosts, follow their skill installation instructions and retain referenced files; copying `SKILL.md` over `AGENTS.md` loses resources and can overwrite project rules. Optional hooks have their own host-specific setup.

The four top-level skills are independent. Install only the ones you want.

## What it does

LabKit is a small collection of four skills. `skill-skill` is the publishing toolkit; `open-loops` and `reading-plan-mentor` are daily-use tools. `welcome-to-agi` combines attributed official prompt blocks with modular routing and optional setup tools.

## Skills

- **[welcome-to-agi](skills/welcome-to-agi/README.md)** — Routes ordinary tasks through selected official guidance; includes modular prompts, guided hook initialization, and optional configuration audit

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
