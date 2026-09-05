# Welcome to AGI

[English](README.md) | **中文**

普通任务提交后，由当前 Codex 判断需要哪些指导，再读取对应的官方 Astra 提示词并执行任务。无需先抱怨，也无需额外模型 API 或向量库。

```text
普通任务 → Hook 加入场景目录 → Codex 判断 → 读取所需模块 → 完成原任务
```

## 安装并初始化

在 LabKit 仓库目录执行，第一条预览，第二条安装并注册 hook：

```bash
python3 skills/welcome-to-agi/scripts/install.py --user
python3 skills/welcome-to-agi/scripts/install.py --user --apply
```

只用于一个项目时，把 `--user` 换成 `--project /path/to/project`。需要 Python 3.10+，安装器目前支持 macOS/Linux。

**最后在 Codex CLI 的 `/hooks` 中审阅并信任该 hook。** 安装程序会分别报告文件安装、hook 注册和未验证的宿主状态，不会把写入成功当成已启用。

也可以让 Agent 操作：

> 安装 LabKit 的 welcome-to-agi，并按它的 SKILL.md 完成初始化，告诉我还剩哪些宿主操作。

已通过其他窗口下载的用户：首次显式调用 `$welcome-to-agi` 会引导初始化。单纯复制文件没有自动执行能力；标准安装入口已把下载后的安装与初始化连起来。

## 普通任务也能识别

- “帮我实现这个功能并验证”：Codex 判断是否需要自主推进和测试指导。
- “分析这三个独立方案”：判断能否从并行子任务获益。
- “写一份说明”：判断是否需要写作指导。
- 简单计算或事实问题：可以不加载任何模块，直接回答。

这些是选择场景的说明，不是固定关键词匹配结果。Hook 每次只补充简短目录；语义判断由正在处理任务的 Codex 完成。无法保证模型每次判断正确。

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
- `initialize.py`：检查已安装版本，注册 hook，给出信任与生效检查步骤。
- `astra.py router`：预览每次提交时补充的判断入口。
- `astra.py compose`：单独生成选中模块，保留原 prompt。
- `audit.py`：可选的一次性只读配置审计，不自动清理其他技能。

[详细安装、旧版改名迁移、配置与撤销](references/setup.md)

## 验证与边界

默认适配 Codex 的 `UserPromptSubmit`，模型默认限定为 `gpt-6-astra`。规则和模块可以移植；其他宿主需要相应的接入方式。

[测试记录](references/evaluation.md)区分脚本检查、模型实际选模块的试用，以及原生 hook 投递验证。普通 skill 的隐式选择不是每次提交事件的保证；希望自动路由需要完成 hook 初始化和宿主信任。

官方提示词来自 [OpenAI Astra 指南](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)，核验于 2026-09-05。模块路由和初始化是 LabKit 的设计，详见[来源](references/sources.md)。原创代码沿用 [PolyForm Noncommercial 许可](../../LICENSE)。
