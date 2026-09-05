# Contributing

**English** · [中文](CONTRIBUTING.zh-CN.md)

LabKit collects independent tools for skill authoring, publishing, everyday work and agent guidance. Internal modules belong to their parent tool and are not separate catalogue entries.

## Prepare a change

Keep each complete skill under `skills/{name}/`, with a `SKILL.md` entrypoint and the scripts, references or assets it actually needs. Preserve working behavior, attribution and existing licenses. Use the maintained [authoring guidance](skills/skill-skill/references/authoring.md) for new or revised instructions.

Describe when the skill applies and what it produces. Choose useful structure for its workflow; a fixed five-part description or mandatory heading set is not required. Give validation evidence appropriate to the change and distinguish file checks from observed agent behavior.

## Repository presentation

Follow the [presentation standard](skills/skill-skill/references/repository-presentation.md) for repository-facing changes. The hero names LabKit; child tools retain their own names. Keep public counts consistent with real top-level entries and preserve a working path from the catalogue to each tool.

Change README.md and README.zh-CN.md together. Keep commands, counts, capabilities, dependencies and validation claims aligned; translate navigation and diagram labels. Inspect both theme assets and the assembled page for visual changes. Use assets/STYLE.md to preserve the chosen direction.

## Submit

1. Work on a branch and keep the change focused.
2. Update the affected instructions, references and human documentation.
3. Run relevant checks and review the diff for unrelated files.
4. Open a PR explaining the concrete change, validation and remaining limitations.

Use descriptive titles such as `Fix open-loops: preserve deferred decisions` or `Improve repository identity and navigation`. Avoid unsupported compatibility claims, unrelated version changes and duplicated tools without a clear reason.

## License

See [LICENSE](LICENSE). Preserve third-party attribution and component-specific exceptions.
