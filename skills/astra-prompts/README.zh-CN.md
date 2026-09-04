# Astra Prompts

[English](README.md) | **中文**

把 OpenAI 为 GPT-6 Astra 提供的五类提示词，按实际需要加到当前任务里。一个 skill，五个独立模块，可选 Codex hook；初始化和配置审计作为同目录下的独立工具，需要时再用。

## 先安装 skill

在 LabKit 仓库目录执行，把完整文件夹放进目标项目：

```bash
mkdir -p /path/to/project/.agents/skills
cp -R skills/astra-prompts /path/to/project/.agents/skills/
```

复制前检查目标是否已安装，避免覆盖自己的配置。希望所有项目都能发现它，可以放进 `~/.agents/skills/`。安装后直接说：

```text
$astra-prompts 少点套话，继续完成当前任务。
```

Agent 会选择有关模块，继续完成原任务。它也可以根据“别反复跑测试”等行为调整请求自动选择 skill。不过，这种隐式触发由模型决定，不能保证每条消息都调用。单纯下载或第一次调用，不会修改全局指令、启动初始化或清理其他技能。

## 五个模块，分别开关

| 模块 | 解决的问题 | 默认状态 |
|---|---|---|
| `initiative` | 已授权的工作持续推进，减少无必要确认 | 匹配时启用 |
| `instruction-following` | 说明规则冲突和暂停原因，遵循指令优先级 | 匹配时启用 |
| `writing-style` | 简洁表达，减少套话和术语 | 匹配时启用 |
| `testing` | 测试与改动相称，避免重复检查 | 匹配时启用 |
| `delegation` | 调整子 agent 并行委派 | **关闭** |

官方的委派提示词是鼓励**增加**调用，不是减少调用。因此这个模块默认关闭，另外提供单独的适用条件，方便按需求启用或修改。

每个模块都拆成三份文件：

```text
modules/writing-style/
  module.json   # 触发条件、排序和官方来源
  prompt.md     # 官方提示词原文
  guard.md      # 单独标注的 LabKit 适用条件
```

在 `config.json` 中开关模块和适用条件；在 `module.json` 中修改触发词；修改 `prompt.md` 可以制作自己的版本，但应同步调整来源标注。新增模块只需添加文件和配置项，不需要改引擎。

## 想要自动补充提示词，再启用 hook

Codex 提供了 `UserPromptSubmit` 事件。这个工具在消息提交时匹配明确语句，将选中的静态提示词作为额外上下文补充，保留原用户消息。它不读取聊天记录、不调用模型、不启动子 agent。

从**安装后的目录**运行预览：

```bash
python3 /path/to/project/.agents/skills/astra-prompts/scripts/setup_hook.py \
  --hooks /path/to/project/.codex/hooks.json
```

检查差异后，加 `--apply` 写入。最后在 Codex CLI 的 `/hooks` 中审阅并信任这条 hook。写入配置只代表注册完成，不能直接当成已启用。项目级 hook 还需要项目已受信任。

安装脚本支持 macOS/Linux，需要 Python 3.10+。同一个 hook 只选一个作用范围安装，避免多个配置层重复注入。默认只作用于 `gpt-6-astra`；模型未知、没有匹配或配置异常时不补充内容。计划模式不注入自主执行和委派模块。

Hook 使用本地正则匹配，容易检查和改造；skill 本身由宿主模型做语义选择。两者都不需要向量库。正则可能漏掉含蓄表达，也可能匹配粘贴的正文，因此不能把它当作完整的意图理解或行为监测器。

[详细安装、配置、撤销和初始化审计流程](references/setup.md)

## 单独使用工具

在 skill 目录运行：

```bash
printf '%s' '少点套话，继续完成当前任务。' | python3 scripts/astra.py route
printf '%s' '请解释缓存失效。' | python3 scripts/astra.py compose --modules writing-style
python3 scripts/audit.py /path/to/project/AGENTS.md /path/to/project/.agents/skills
```

`route` 预览模块选择；`compose` 输出原消息和提示词两个独立字段；`audit.py` 只读扫描指定路径，报告候选冲突、重复入口和检查盲区。审计结果需要结合上下文判断，不会自动删文件或重写 `AGENTS.md`。

## 已验证什么

脚本有自动测试，并做过一次独立 Agent 的实际 skill 试用。安装、撤销、原文保留等机制与模型行为验证分开记录。本版本没有在已信任 hook 的原生 Codex 会话里完成端到端实测；安装后可按[验证说明](references/evaluation.md)检查，不把脚本成功当成宿主已成功注入，也不承诺更省 token 或更高质量。

提示词来自 [OpenAI 官方 Astra 指南](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)，核验日期为 2026-09-05。路由、适用条件、安装工具和审计流程是本项目增加的部分，详见[来源与兼容性](references/sources.md)。原创代码沿用仓库的 [PolyForm Noncommercial 许可](../../LICENSE)，官方提示词保留来源归属。
