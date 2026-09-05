# Host and desktop guide / 客户端与桌面端引导

## 用户先做什么

桌面端可以直接对 Agent 说：

> 安装 LabKit 的 welcome-to-agi，并完成初始化。我使用的是【客户端名称】，用于【当前项目／所有本地项目】。请优先检查 Hook 能力并引导完成信任和验证；请替我执行安装步骤，保留原有配置，并说明还需要在这个客户端里验证什么。

Agent 能执行本地命令时，由它运行安装器。用户只需要补充无法识别的客户端和作用范围，以及完成宿主要求的人机确认。安装器不操作 GUI；如果 Agent 只有聊天能力，使用下方手动包。下载文件本身不会自动运行初始化。

## 模型与宿主分开确认

提示词针对 Astra；Codex、Hermes、OpenClaw 等宿主负责加载指令和提供工具。先核对实际选用的模型，再配置接入。Claude Code、Cursor 的规则格式适配不等于已提供或验证 Astra，也不表示这些提示词在其他模型上效果相同。安装器不会切换模型或配置供应商。

## 当前接入范围

| 客户端／环境 | 默认接入 | 写入位置 | 还需确认 |
|---|---|---|---|
| 本地 Codex 桌面端、CLI、IDE（macOS/Linux） | 优先检查并注册 Hook | 活跃配置层旁的 `hooks.json` | 当前宿主支持、信任及实际客户端投递；未验证时保留待办 |
| Hermes 项目 | 常驻规则 | 已有项目上下文文件；无既有文件时用 AGENTS.md | 后端实际工作目录、上下文优先级、所选模型；[专门引导](hermes-openclaw.md) |
| OpenClaw Agent 工作区 | 常驻规则 | `<workspace>/AGENTS.md`，包位于 `<workspace>/skills` | 当前 Agent 的真实 workspace、profile、所选模型；[专门引导](hermes-openclaw.md) |
| Claude Code Desktop、CLI | 常驻规则 | 项目 `CLAUDE.md`；用户 `~/.claude/CLAUDE.md` | 当前 Code 项目及权限；不代表普通 Claude 聊天或 Cowork 已适配 |
| Cursor 项目 Agent | Always Apply 项目规则 | `.cursor/rules/welcome-to-agi.mdc` | 当前项目的规则面板与 Agent 会话 |
| Cursor 用户级 | 手动模式 | 不猜测或改写应用内部设置库 | 可将生成的入口粘贴到 User Rules；需验证本机路径可读 |
| 其他可读文件的本地 Agent | 显式指定常驻规则文件 | `--host generic --mode rules --rules-file PATH` | 该客户端确实自动加载此文件；本工具不替它添加加载能力 |
| 普通桌面聊天、网页、云端或无法读本地文件 | 手动提示词包 | `--mode manual --export PATH` | 把文件附到会话；自动跨对话生效不受保证 |
| Codex，用户选择兼容方案 | 常驻规则 | 项目 `AGENTS.md`；用户 `$CODEX_HOME/AGENTS.md` | 当前会话实际加载该文件，模块路径可读 |

代码已实现这些文件生成／编辑路径，使用临时项目验证。**Hermes、OpenClaw、Claude Code、Cursor 的原生会话仍未实测；Codex CLI 已验证 Hook 投递，桌面端仍待观察**；表格不表示所有版本都已验证可用。脚本检查使用 macOS/Linux、Python 3.10+；Windows 原生运行尚未验证，hook 安装器明确拒绝 Windows。

`--host auto` 仅检查 `CODEX_THREAD_ID`、`CLAUDECODE=1` 的运行环境线索；这些也可能从父进程继承。线索冲突或缺失就选择 generic/manual，不扫描已安装软件来猜客户端。Agent 应根据真实会话选择 `--host` 和 `--surface`；有终端工具不代表用户在使用 CLI。

## 无 hooks 如何工作

```text
宿主加载常驻规则
  → 用户正常提交任务
  → 当前模型按规则读取最新模块配置和场景描述
  → 选择 0～max_modules 个模块
  → 读取选中的官方原文与适用条件
  → 执行原任务
```

常驻入口不复制完整模块目录；开关和新增模块在下次读取配置时生效。它依赖模型遵守指令，不能承诺每次提交都有程序回调。Codex 的 AGENTS.md 通常在启动时加载；改动入口后应开启新会话。Hook 的提交事件入口更确定，但模块判断仍由模型完成。两种方式都不需要向量库或额外模型 API。

这些是 Astra 提示词的接入适配，不是模型切换功能。其他模型可以读取文本，但需判断适用性；不会因此获得多 Agent、读文件或执行命令能力。`config.models` 仅过滤 Codex hook 事件。

## 桌面端与终端的关系

Codex 的桌面 agent、CLI 和 IDE 共享 agent 配置；但配置文件、客户端版本、运行机器、用户/profile 和项目仍必须对应。[官方设置](https://learn.chatgpt.com/docs/developer-settings)

Claude Code Desktop 与 CLI 共享引擎和 CLAUDE.md 项目上下文；这不等于同一个品牌下所有聊天模式共享本地文件。[官方 Desktop 说明](https://code.claude.com/docs/en/desktop)

连接远程机器、容器、WSL 或云任务时，要在执行 Agent 的环境里安装，并在那里生成有效路径。本机写入成功不能证明远程会话能读取。`--surface cloud` 仅导出手动方案；若能在远程环境执行安装器，应在那个环境按本地 CLI/desktop 接入。当前规则包含本机绝对路径，不能原样提交给其他机器复用；在目标环境重新初始化。项目文件是否进入版本控制由用户决定。

## 在实际使用的客户端验证

安装结束后不要只检查文件。新建一个实际使用该项目和配置的会话，按顺序做：

1. 查看当前客户端的已加载规则／指令来源。Codex 可让 Agent 报告当前指令来源；Claude Code 可检查 `/context` 的 Memory files（入口因界面版本而异）；Cursor 在规则面板确认 `Always Apply`。模型自述只作线索，结合宿主显示的来源和可见文件读取。
2. 正常提交“在这个临时项目实现一个秒数转分钟秒数的函数，并验证边界情况”，不要提 skill 名称或提示它选模块。观察所选 `prompt.md`／`guard.md` 的读取和实际产物。不要为了验收额外开放权限或多 Agent。
3. 提交“17 × 6 等于多少”。允许直接回答、不读模块；不能要求每个任务都加载提示词。
4. 禁用一个相关模块后再提交任务，观察最新配置读取和模块变化。常驻入口更改或卸载后重开会话，避免旧上下文干扰。

只在诊断阶段记录客户端、版本、运行位置、实际指令来源、模块读取和结果。日常使用无需输出路由报告。`native_delivery: not_verified` 是程序无法观察客户端投递的事实；它不会依据用户填写的开关自动变成已验证。

## Hook 信任与验证流程

Codex Hook 使用 CLI 的 `/hooks` 管理信任。先检查实际运行时版本与 Hook 列表；存在注册不代表受信任或已经触发。必须针对实际桌面 agent 所在机器和 profile；不要在无关终端环境里信任后声称桌面已生效。信任后仍按上面的普通任务流程，在实际客户端确认投递。若客户端确实不支持 Hook，可建议 rules，由用户选择是否切换。若仅缺少信任或 Agent 无法操作界面，保留待完成状态，说明具体步骤，不移除 Hook、不自动改写为 rules。完成信任后提交普通任务，分别核对 Hook 事件、目录投递和模块读取；CLI 验证不能冒充桌面端验证。[官方 hooks](https://learn.chatgpt.com/docs/hooks)

## 排查与撤销

- **Codex 规则没加载：** 检查非空 `AGENTS.override.md` 是否遮蔽 AGENTS.md、项目是否受信任、指令大小上限、当前目录和 CODEX_HOME。安装器发现同目录 override 会停止写入，说明应检查哪个文件；不删除 override。[官方 AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- **Claude Code 规则没加载：** 确认使用 Code 环境、项目位置及文件读取权限。普通聊天附件不等于 Code 的 CLAUDE.md。[官方项目指令](https://code.claude.com/docs/en/memory)
- **Cursor 没加载：** 使用 `.mdc` 扩展名并确认 `alwaysApply: true`；普通 `.md` 文件放进规则目录不等于有效项目规则。[官方 Rules](https://prod.cursor.com/docs/rules)
- **文件读不到：** 修正实际运行环境中的路径，或使用 portable manual pack。不要靠本地安装成功猜远端支持。
- **重复入口：** 在同一作用范围内选一种模式。安装器会阻止它发现的旧 Welcome hook 与默认规则重复；其他层、其他 profile、自定义路径仍需查看当前加载来源。规则遇到当轮 hook catalog 会复用，避免再路由一次。
- **撤销：** 使用 [setup.md](setup.md) 的 `--remove`。只移除带本项目标记的段落，保留其余指令；备份在原文件旁。Cursor 撤销后保留空规则头和用户后来写的内容，不删除整个文件。

## Extend / 增减适配器

`adapters/hosts.json` 独立维护宿主名、技能目录、用户／项目规则路径及格式。`scripts/hosts.py` 决定模式；`setup_rules.py` 管理规则块；`setup_hook.py` 仅处理 Codex 事件；提示词仍独立在 `modules/`。新增 Markdown 指令宿主可增加一项 profile 和对应安装测试；新格式或 hook 协议需要实际适配器，不能只把 `hook_adapter` 改成 true 后宣称兼容。
