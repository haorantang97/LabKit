<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner.svg">
    <img width="700" alt="LabKit" src="assets/banner.svg">
  </picture>
</p>

# LabKit

[English](README.md) | **中文**

[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-blue.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![Last Updated](https://img.shields.io/badge/updated-Jul%202026-blue.svg?style=flat-square)]()

> 把一个跑通的 AI 规则文件，从本地草稿做成 GitHub 上发布质量的 repo。

## 安装

```bash
git clone https://github.com/haorantang97/LabKit.git
cd LabKit
```

LabKit 对外只有三个顶层 skill。`skill-skill` 是一整套完整的发布工具；它的流水线模块放在 `skills/skill-skill/modules/` 里，不作为独立的顶层 skill 展示。

每个顶层 `SKILL.md` 都是带 YAML front matter 的 markdown。把你需要的那个装进 agent：

| Agent | 放哪里 |
|---|---|
| Claude Code | `cp -r skills/* ~/.claude/skills/` |
| Cursor | `cp skills/{name}/SKILL.md ~/your-project/.cursor/rules/{name}.mdc` |
| Windsurf | `cat skills/{name}/SKILL.md >> ~/your-project/.windsurfrules` |
| GitHub Copilot | `cp skills/{name}/SKILL.md ~/your-project/.github/copilot-instructions.md` |
| Codex / AGENTS.md | `cp skills/{name}/SKILL.md ~/your-project/AGENTS.md` |

三个顶层 skill 相互独立，只装你要的那个就行。

## 这是什么

LabKit 是一组原创的个人 skill。`skill-skill` 是发布工具箱，`open-loops` 和 `reading-plan-mentor` 是两个独立的日常自用工具。

## Skill 清单

- **[skill-skill](skills/skill-skill/SKILL.md)** — 把一个跑通的 AI 规则或 skill 打包，并引导完成 GitHub 发布

- **[open-loops](skills/open-loops/SKILL.md)** — 审计长对话里未回答、未确认，或被 Agent 擅自决定的信息点
- **[reading-plan-mentor](skills/reading-plan-mentor/SKILL.md)** — 把书单变成有节奏、可持续、带每日导读与连续性的长期阅读计划

这两个 skill 也继续保留在独立仓库中：[open-loops](https://github.com/haorantang97/open-loops) 和 [reading-plan-mentor](https://github.com/haorantang97/reading-plan-mentor)。

## 文件格式

```
skills/{name}/SKILL.md
```

YAML front matter（`name`、`description`、`license`）加 markdown：

```yaml
---
name: skill-name
description: "Use when the skill's triggering conditions match the user's request."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start
...
```

## 贡献

见 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)。

## License

PolyForm Noncommercial License 1.0.0。见 [LICENSE](LICENSE)。
