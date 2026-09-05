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
[![Last Updated](https://img.shields.io/badge/updated-Sep%202026-blue.svg?style=flat-square)](https://github.com/haorantang97/LabKit/commits/main)

> 可复用的 Agent 工具：发布 skill、处理日常任务、按需调整 Astra 行为。

**新增：[Welcome to AGI](skills/welcome-to-agi/README.zh-CN.md)**。把五类官方提示词拆成可独立开关的模块，在普通任务提交时做语义路由，提供初始化引导和只读配置审计工具。[English](skills/welcome-to-agi/README.md)

## 安装

```bash
git clone https://github.com/haorantang97/LabKit.git
cd LabKit
```

LabKit 对外有四个顶层 skill。`skill-skill` 是一整套完整的发布工具；它的流水线模块放在 `skills/skill-skill/modules/` 里，不作为独立的顶层 skill 展示。Astra 的五个行为模块也属于一个 skill。

每个顶层 skill 都有 `SKILL.md` 入口。安装时复制**完整文件夹**，保留脚本和引用文件。例如，在 Codex 中安装到目标项目：

```bash
python3 skills/welcome-to-agi/scripts/install.py --project /path/to/project --apply
```

希望全局安装，将 `--project /path/to/project` 换成 `--user`。注册后在 Codex 的 `/hooks` 中完成信任。复制前先检查已有安装，保留自定义配置。其他宿主按其 skill 安装方式配置，并保留引用文件；不要把 `SKILL.md` 覆盖到项目 `AGENTS.md`，以免丢失资源或覆盖原有规则。可选 hook 另有对应宿主的安装步骤。

四个顶层 skill 相互独立，只装需要的即可。

## 这是什么

LabKit 收录四个 skill。`skill-skill` 是发布工具箱，`open-loops` 和 `reading-plan-mentor` 是日常工具；`welcome-to-agi` 将有来源标注的官方提示词与模块路由、可选初始化工具组合起来。

## Skill 清单

- **[welcome-to-agi](skills/welcome-to-agi/README.zh-CN.md)** — 普通任务提交后自动提供场景判断入口，按需加载官方提示模块；带初始化引导和独立配置审计

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
