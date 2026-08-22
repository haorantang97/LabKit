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
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.zh-CN.md)

> 一套用于发布、检查、创作和日常 Agent 工作的可复用 Skill 工具箱。

LabKit 是一组相互独立的 `SKILL.md` 工具包，包含 Skill 发布流水线、日常内容诊断、设计工作流、读书计划和本地工具适配器。

## 安装

```bash
git clone https://github.com/haorantang97/LabKit.git
cd LabKit
```

每个 skill 都可以独立使用。只把需要的文件夹复制到对应 Agent 的 skill 目录，并保留旁边的 `references/`、`scripts/` 或 `assets/`。

## 内容分区

### 发布流水线

LabKit 的核心来自原 `SKILL-SKILL`：把一个已经跑通的规则文件整理成可以发布的 GitHub 仓库。

- [publish-skill-bundle](skills/publish-skill-bundle/SKILL.md) — 发布总入口
- [polish-rule-content](skills/polish-rule-content/SKILL.md) — 整理已有规则文件
- [write-readme](skills/write-readme/SKILL.md) — 写发布 README
- [scaffold-repo-files](skills/scaffold-repo-files/SKILL.md) — 补齐仓库文件
- [create-visual-assets](skills/create-visual-assets/SKILL.md) — 生成发布横幅
- [translate-readme](skills/translate-readme/SKILL.md) — 生成第二语言 README
- [publish-to-github](skills/publish-to-github/SKILL.md) — 发布并配置 GitHub 仓库
- [submit-to-directories](skills/submit-to-directories/SKILL.md) — 提交到相关目录

### 日常工具箱

- [dbs](skills/everyday-toolbox/dbs/SKILL.md) — 把商业与内容任务路由到合适的诊断 skill
- [dbs-content](skills/everyday-toolbox/dbs-content/SKILL.md) — 诊断选题应该如何做成内容
- [dbs-ai-check](skills/everyday-toolbox/dbs-ai-check/SKILL.md) — 识别 AI 写作痕迹，默认不改稿
- [dbs-script-flow](skills/everyday-toolbox/dbs-script-flow/SKILL.md) — 检查短视频稿的逻辑与留存风险
- [humanizer-zh](skills/everyday-toolbox/humanizer-zh/SKILL.md) — 编辑中文文本，减少机器腔
- [screenshot-card-composer](skills/everyday-toolbox/screenshot-card-composer/SKILL.md) — 把私信和评论截图做成可发布卡片

### 阅读

- [reading-plan-mentor](skills/reading/reading-plan-mentor/SKILL.md) — 把书单变成有节奏的导师式阅读计划

### 集成与本地工具

- [dws](skills/integrations/dws/SKILL.md) — 钉钉工作区操作；保留其中的 Apache-2.0 LICENSE 与 NOTICE
- [figma](skills/integrations/figma/SKILL.md) — 基于 Figma MCP 的设计转代码流程
- [frontend-design](skills/integrations/frontend-design/SKILL.md) — 有明确视觉方向的前端设计
- [yichen-wechat-local-vault](skills/integrations/yichen-wechat-local-vault/SKILL.md) — 带严格隐私边界的微信本地 Vault 工具

## 边界

LabKit 只包含可复用说明和本地工具适配器，不包含账号数据、解密数据库、个人导出物、公司材料或运行时状态。

部分集成 skill 需要对应的本地 CLI、MCP 服务或操作系统环境；运行条件不满足时，应明确降级或停止。

## 相关合集

- [Personal-Ontology](https://github.com/haorantang97/Personal-Ontology) — 个人知识与上下文方法
- [TArt](https://github.com/haorantang97/TArt) — 艺术与视觉创作 skills
- [open-loops](https://github.com/haorantang97/open-loops) — 独立的长对话连续性审查 skill

## License

LabKit 原创内容使用 PolyForm Noncommercial License 1.0.0。带有独立 LICENSE 或 NOTICE 的组件继续遵循各自条款；重新分发前请查看对应目录。
