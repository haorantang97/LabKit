# Welcome to AGI

[English](README.md) | **中文**

普通任务提交后，由当前 Agent 判断需要哪些指导，再读取对应的官方 Astra 提示词并执行任务。无需先抱怨，也无需额外模型 API 或向量库。

```text
普通任务 → Hook／常驻规则 → 当前模型判断 → 读取所需模块 → 完成原任务
```

## 安装并初始化

桌面端可以直接对 Agent 说：

> 安装 LabKit 的 welcome-to-agi，用于我当前客户端和项目，并完成初始化。请检查 Hook 能力并引导完成信任和验证；请替我执行步骤，保留原有配置，说明还需要在当前客户端验证什么。

**支持 Hook 的 Codex 环境优先引导 Hook；常驻规则作为用户可选的兼容方案。** 缺少信任时会保留待办并引导完成，不会自动切换成 AGENTS.md。 有本地执行能力的 Agent 可以代为安装。仅复制文件无法触发初始化，下载器需继续按 SKILL.md 操作。

首次引导会列出五项模块开关与当前 Hook 注册情况，集中询问：要关闭哪些模块、是否检查现有 Skills 和指令冲突、是否调整接入方式。新安装默认全部开启，包含多 Agent 协作；升级保留已有选择。模块按任务需要选用，多 Agent 模块也不会替你开启宿主的多 Agent 功能。检查由用户选择后执行。[完整初始化引导](references/onboarding.md)。

| 客户端 | 已实现的接入方式 |
|---|---|
| 本地 Codex 桌面端／CLI／IDE | Hook 加信任验证；可选择 AGENTS.md 规则块 |
| Claude Code Desktop／CLI | CLAUDE.md 规则块 |
| Cursor 项目 Agent | Always Apply 项目规则 |
| 其他可读取本地文件的 Agent | 指定宿主已自动加载的规则文件 |
| 只有设置界面／普通聊天／云环境 | 导出简短规则入口，或完整手动提示词包 |

[各客户端详细引导、限制与实际生效检查](references/hosts.md)

需要命令行时，先预览再安装。Python 3.10+，脚本已在 macOS/Linux 验证：

```bash
python3 skills/welcome-to-agi/scripts/install.py --host codex --surface desktop --project /path/to/project
python3 skills/welcome-to-agi/scripts/install.py --host codex --surface desktop --project /path/to/project --apply
```

其他客户端换成 `--host claude-code` 或 `--host cursor`。用户级安装用 `--user` 替换 `--project PATH`；Cursor 用户级采用手动入口，不直接改内部设置数据库。未知宿主明确回退到手动模式。Codex macOS/Linux 默认注册 Hook 并引导信任；选择 `--mode rules` 则使用常驻规则；`--skill-only` 表示手动模式。

## 普通任务也能识别

- “帮我实现这个功能并验证”：Codex 判断是否需要自主推进和测试指导。
- “分析这三个独立方案”：判断能否从并行子任务获益。
- “写一份说明”：判断是否需要写作指导。
- 简单计算或事实问题：可以不加载任何模块，直接回答。

这些是选择场景的说明，不是固定关键词匹配结果。常驻规则要求模型每个任务读取最新配置和场景描述；Hook 在提交事件中补充目录。前者依赖指令遵循，后者有程序入口，两者的语义判断都由当前模型完成。手动包会包含全部启用模块，占用更多上下文，配置变更后需重新导出。

## 五个模块，分别改造

| 模块 | 用途 |
|---|---|
| `initiative` | 持续完成已授权的多步骤工作 |
| `instruction-following` | 处理实际存在的规则冲突 |
| `writing-style` | 清楚地写作、解释和总结 |
| `delegation` | 在适合且允许时拆分独立子任务 |
| `testing` | 做与改动相称的验证 |

新安装默认提供全部五个候选，但不会全部加载。委派仍受任务边界、工具权限和用户要求约束，不会仅因模块可用就启动子 agent。

每个模块拆成 `module.json`（场景描述）、`prompt.md`（官方原文）、`guard.md`（本项目适用条件）。在 `config.json` 开关模块；修改 `when` 调整语义选择条件；增加模块无需改引擎。

## 初始化与工具

- `install.py`：安装完整 skill，并衔接初始化。
- `initialize.py`：初始化规则／hook、撤销注册、导出手动包；`--onboarding` 只读列出模块与 Hook 状态。
- `onboarding.py`：独立的初始化状态读取组件，不扫描其他 Skills，也不执行 Hook。
- `adapters/hosts.json`：独立的宿主适配配置，便于增减改造。
- `astra.py router`：预览每次提交时补充的判断入口。
- `astra.py compose`：单独生成选中模块，保留原 prompt。
- `audit.py`：初始化时主动询问的一次性只读检查，用户选择后检查约定范围，不自动清理其他技能。

[详细安装、旧版改名迁移、配置与撤销](references/setup.md)

## 验证与边界

默认按宿主选择 Hook、常驻规则或手动方式。Codex hook 用 `gpt-6-astra` 过滤事件；常驻规则在其他模型中使用时需判断适用性，不会切换模型或增加工具能力。

[测试记录](references/evaluation.md)区分脚本检查、模型实际选模块的试用，以及原生 hook 投递验证。已验证文件适配器的安装、更新、撤销和导出；尚未逐一完成各桌面客户端原生加载与执行实测。规则已写入不等于客户端已经加载。

官方提示词来自 [OpenAI Astra 指南](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)，核验于 2026-09-05。模块路由和初始化是 LabKit 的设计，详见[来源](references/sources.md)。原创代码沿用 [PolyForm Noncommercial 许可](../../LICENSE)。
