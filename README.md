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

> A personal collection of reusable agent skills, publishing workflows, and everyday tools.

LabKit is the working toolbox behind a small family of portable `SKILL.md` packages. It contains the tools used to publish, inspect, write, design, and operate with coding agents.

## Install

```bash
git clone https://github.com/haorantang97/LabKit.git
cd LabKit
```

Each skill is independent. Copy only the folder you need into the skill directory supported by your agent. Keep any `references/`, `scripts/`, or `assets/` directory next to its `SKILL.md`.

## Collections

### Publishing pipeline

The original LabKit core is the publishing pipeline for turning a working rule file into a release-ready GitHub repository:

- [publish-skill-bundle](skills/publish-skill-bundle/SKILL.md) — end-to-end publishing orchestrator
- [polish-rule-content](skills/polish-rule-content/SKILL.md) — make an existing rule file publishable
- [write-readme](skills/write-readme/SKILL.md) — write a release README
- [scaffold-repo-files](skills/scaffold-repo-files/SKILL.md) — add repository scaffolding
- [create-visual-assets](skills/create-visual-assets/SKILL.md) — create release banner assets
- [translate-readme](skills/translate-readme/SKILL.md) — produce a second-language README
- [publish-to-github](skills/publish-to-github/SKILL.md) — publish and configure the live repository
- [submit-to-directories](skills/submit-to-directories/SKILL.md) — submit to compatible directories

### Everyday toolbox

- [dbs](skills/everyday-toolbox/dbs/SKILL.md) — route business and content tasks to the right diagnostic skill
- [dbs-content](skills/everyday-toolbox/dbs-content/SKILL.md) — diagnose how an approved topic should become content
- [dbs-ai-check](skills/everyday-toolbox/dbs-ai-check/SKILL.md) — identify AI-writing fingerprints without rewriting by default
- [dbs-script-flow](skills/everyday-toolbox/dbs-script-flow/SKILL.md) — find short-video pacing and retention risks
- [humanizer-zh](skills/everyday-toolbox/humanizer-zh/SKILL.md) — edit Chinese copy for less machine-like phrasing
- [screenshot-card-composer](skills/everyday-toolbox/screenshot-card-composer/SKILL.md) — turn private-message and comment screenshots into publishable cards

### Reading

- [reading-plan-mentor](skills/reading/reading-plan-mentor/SKILL.md) — turn a booklist into a paced, mentor-guided reading plan

### Integrations and local tools

- [dws](skills/integrations/dws/SKILL.md) — DingTalk workspace operations; retain its bundled Apache-2.0 license and NOTICE
- [figma](skills/integrations/figma/SKILL.md) — Figma-to-code workflow using the Figma MCP server
- [frontend-design](skills/integrations/frontend-design/SKILL.md) — deliberate visual direction for frontend work
- [yichen-wechat-local-vault](skills/integrations/yichen-wechat-local-vault/SKILL.md) — local WeChat vault workflows with strict privacy boundaries

## Boundaries

LabKit contains reusable instructions and local-tool adapters, not private account data. Credentials, decrypted databases, personal exports, company materials, and runtime state are never part of this repository.

Some integration skills require a matching local CLI, MCP server, or operating-system environment. They degrade honestly or stop when their required runtime is unavailable.

## Related collections

- [Personal-Ontology](https://github.com/haorantang97/Personal-Ontology) — personal knowledge and context methods
- [TArt](https://github.com/haorantang97/TArt) — visual and artistic creation skills
- [open-loops](https://github.com/haorantang97/open-loops) — independent long-conversation continuity auditing skill

## License

The original LabKit materials are distributed under the PolyForm Noncommercial License 1.0.0. Components with their own license or NOTICE file retain those terms; see the component directory before redistribution.
