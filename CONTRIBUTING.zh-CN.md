# 贡献指南

[English](CONTRIBUTING.md) | **中文**

这个仓库收三个顶层 skill。`skill-skill` 发布工具箱内部可以有流水线模块，但这些模块不作为独立的顶层入口展示。符合这个范围的 PR 都欢迎。

## 文件格式

每个顶层 skill 都按这个结构：

```
skills/{top-level-skill-name}/
  └── SKILL.md
```

`skill-skill` 的内部模块放在 `skills/skill-skill/modules/` 下。

`SKILL.md` 是带 YAML front matter 的 markdown，含 `name`、`description`、`license` 三个字段，再加正文。

## 要求

提交的 skill 必须：

- 覆盖一个现有 skill 没处理的发布步骤
- description 用五段式（主触发、正向枚举、口语化触发词、边界扩展、负样本）
- 含 Quick Start 节，含至少两条 Common Mistakes
- 通过 `skills/skill-skill/modules/polish-rule-content/SKILL.md` 里的去 AI 味清单
- 至少在一个 agent 上测过再提

## 质量门槛

> [!NOTE]
> 跟现有 skill 范围重叠、没有负样本、或者只用模糊约束（"小心点"、"按最佳实践来"）的 skill，会不经讨论关闭。

## PR 标题格式

可以：
- `Add {skill-name}: {一句话描述}`
- `Fix {skill-name}: {改了什么、为什么}`

不行：
- `Update README`
- `Add my skill`

## 什么样的会被拒

- 跟现有 skill 范围重叠、又没有明确差异化
- 提交前没在任何 agent 上跑过
- 改版本号的 commit 里塞了无关改动

## 流程

1. Fork 这个仓库
2. 新的独立 skill 放到 `skills/{skill-name}/SKILL.md`；发布工具的内部模块放到 `skills/skill-skill/modules/{module-name}/SKILL.md`
3. 在 README 的 "Skills" 节加一条链接
4. 按上面的标题格式开 PR

改现有 skill 的，说清楚改了什么、修了什么问题、在哪个 agent 上验过。
