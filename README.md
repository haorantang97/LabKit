# Open Loops

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md) [![Last Updated](https://img.shields.io/badge/updated-Aug%202026-blue.svg?style=flat-square)]()

> 让独立审查员找回长对话中被遗漏、默认或越权决定的信息点。

## 安装到 Codex

```bash
git clone https://github.com/haorantang97/open-loops.git
mkdir -p ~/.codex/skills/open-loops
cp -R open-loops/SKILL.md open-loops/references ~/.codex/skills/open-loops/
```

重新开启一个 Codex 任务，让新任务加载这个 Skill。

## 其他平台

**Claude Code**

```bash
mkdir -p ~/.claude/skills/open-loops
cp -R SKILL.md references ~/.claude/skills/open-loops/
```

**OpenClaw**

```bash
mkdir -p ~/.agents/skills/open-loops
cp -R SKILL.md references ~/.agents/skills/open-loops/
```

**Cowork / claude.ai**

在设置的 Capabilities 页面上传完整技能目录（`SKILL.md` 和 `references/`）。

## 它解决什么

长对话里的遗漏通常不会发出声音：AI 可能漏答用户的问题，用户也可能只接住 AI 回答中的部分内容；AI 还可能在没有确认时替用户选定方案。Open Loops 把逐字会话存档交给一个没有参与主对话的独立子 agent，让它逐项检查四类信息断点，并维护一份可对账的未闭环清单。

它追踪“用户是否明确接住每个需要回应的独立实质内容”，不追踪任务是否已经完成，也不把范围限制在执行项目。研究问答、学习、咨询、分析诊断、写作反馈、创意讨论与开发执行使用同一套判据。接受、反对、质疑、搁置、转入别处或无歧义地整组确认后，该条就离开清单。

## 功能

- 找出用户提出但 AI 没有实质回答的信息点
- 找出 AI 已经提出、用户却没有逐项接住的独立实质内容，包括执行点、建议点、知识点、判断、限定、风险与分支
- 标记 AI 未经确认代替用户做出的选择
- 标记 AI 本该提问却自行决定的岔路
- 启用后持续逐轮运行，直到用户明确暂停或停止
- 每轮先核销已经被后续答案解决的旧条目，再检查新增掉点
- 把 Open Loops 自身的调试、状态查询与发布讨论隔离在业务项目账外
- 把同一份状态卡注册为宿主输出物；无法挂载时交付可点击文件地址
- 首次接入时从原始会话记录重建历史清单
- 稳态运行时只报告本轮新增项，没有新增则保持静默

## 仓库内容

- `SKILL.md`：常驻流程和宿主集成规则
- `references/audit-protocol.md`：生产审查员必须读取的语义协议
- `references/eval-cases.md`：仅在修改 Skill 时使用的回归标准

## 使用边界

单轮、带编号的多问清单通常不需要 Open Loops。它也不是任务管理器：已经看见但决定稍后执行的事项，应交给项目清单或知识库。

清单仍由模型维护，不能提供绝对不会漏项的保证。重要项目应偶尔回看逐字原文存档。

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT — see [LICENSE](LICENSE).
