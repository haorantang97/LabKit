# 参与贡献

[English](CONTRIBUTING.md) · **中文**

LabKit 收录 Skill 编写、发布、日常工作与 Agent 行为指引相关的独立工具。内部模块属于对应工具，不单独计入首页目录。

## 准备改动

每个完整 Skill 放在 `skills/{name}/` 下，保留 `SKILL.md` 入口，以及实际需要的脚本、参考资料和资产。保留有效行为、来源声明与既有许可证。创建或修改指令时，使用当前的[编写指导](skills/skill-skill/references/authoring.md)。

说明 Skill 在什么情况下使用、产出什么。根据流程选择有用的结构，不强制五段式描述或固定标题集合。提供与改动相称的验证依据，并区分文件检查与实际 Agent 行为。

## 仓库展示

仓库门面的改动遵循[展示标准](skills/skill-skill/references/repository-presentation.md)。首页 Hero 使用 LabKit 品牌，子工具保留各自名称。公开数量与真实顶层入口一致，每个目录项都能打开对应工具。

同一次改动同步 README.md 与 README.zh-CN.md。命令、数量、能力、依赖与验证表述保持一致，导航和图示标签分别翻译。视觉改动需检查明暗两套资产与完整页面。延续 assets/STYLE.md 记录的设计方向。

## 提交

1. 在分支上工作，保持改动范围明确。
2. 更新受影响的指令、引用与读者文档。
3. 执行相关检查，审阅差异，排除无关文件。
4. 发起 PR，说明具体变化、验证结果和剩余限制。

标题说明真实改动，例如 `Fix open-loops: preserve deferred decisions` 或 `Improve repository identity and navigation`。避免无依据的兼容性声明、无关版本变更，以及没有明确理由的重复工具。

## 许可证

见 [LICENSE](LICENSE)。保留第三方来源声明及组件级许可例外。
