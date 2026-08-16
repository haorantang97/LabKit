<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner.svg">
    <img width="700" alt="reading-plan-mentor" src="assets/banner.svg">
  </picture>
</p>

# Reading Plan Mentor｜导师陪读

[English](README.md) | **中文**

[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-blue.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![Last Updated](https://img.shields.io/badge/updated-Jul%202026-blue.svg?style=flat-square)]()

> 把一份书单变成长期的、有导师陪读的每日阅读计划，按时投递。

## 安装

**Claude Code / Claude Cowork：**

```bash
git clone https://github.com/haorantang97/reading-plan-mentor.git
mkdir -p ~/.claude/skills/reading-plan-mentor
cp -r reading-plan-mentor/SKILL.md reading-plan-mentor/references ~/.claude/skills/reading-plan-mentor/
```

**AGENTS.md（Codex / 任意 agent）：**

```bash
cat reading-plan-mentor/SKILL.md >> ~/your-project/AGENTS.md
# 把 references/ 一并放在旁边，详细手册都在里面
```

本 skill 针对 Claude Code / Cowork 构建和测试（依赖其定时任务与邮件投递）；在其他 agent 上自动降级为计划设计 + 每日导读文本生成。

## 它做什么

大多数读书计划死于"它只是一张日历"：日历不知道霍布斯比爽文难读五倍，你跳过一天它就塌，你周二问过什么它周三就忘。reading-plan-mentor 把书单变成一个带导师的长期计划：先判断这几本书放在一起读有没有意义——凑不出主线会直说；再按书的性质决定读法，按难度加权的时间而不是页数排节奏；每天一封导读邮件，回应你昨天随口提的问题。

## 示例

```
「我想用 8 周读完《君主论》《利维坦》《理想国》，每天 45 分钟。」
```

它会找出这三本书共享的那个问题（政治权力的正当性从哪来？），标注哪两本是强对照、哪本是弱关联，核算你的阅读速度下时间线是否真的可行，然后给出周框架 + 完整的 Day 1 样例邮件。你确认之前，不建立任何自动发送。

换成《战争与和平》加一部玄幻网文？它拒绝硬凑主题：小说各走各的线性轨道，按叙事停顿切块，不剧透，不穿插。

## 功能

- 排计划前先审书单，凑不出真主线绝不硬编
- 每本书按两条轴分类：可跳读 vs 必须顺读，享受向 vs 分析向
- 每日负荷按难度加权分钟数计算，从不按页数
- 少读、想休息、多读时，重排剩余计划而不是让整张表塌掉
- 显式维护跨文本钩子台账，承诺过的回收必须真回收
- 把你聊天时随口冒出的问题压缩进记忆库，第二天的邮件里回应你
- 对不确定的章节事实示弱标注而非编造，自动日更不产生幻觉引用

## 结构

```
reading-plan-mentor/
├── SKILL.md                              # 工作流：主题闸门 → 设计 → 确认 → 每日循环
└── references/
    ├── book-classifier.md                # 两轴分类、并发上限、小说专项处理
    ├── capacity-and-pacing.md            # 难度加权容量模型 + 节奏控制器
    ├── email-format-and-voice.md         # 七块每日模板、语气、抗幻觉
    ├── memory-and-continuity.md          # 记忆库 schema、对话抓取、回指、看板
    └── delivery-and-scheduling.md        # 投递通道、定时任务自包含、幂等
```

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 许可

PolyForm Noncommercial License 1.0.0 — 见 [LICENSE](LICENSE)。
