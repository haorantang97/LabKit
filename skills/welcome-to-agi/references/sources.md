# Sources and compatibility

Checked on **2026-09-05**. This is a community package in LabKit, not an OpenAI product.

## Prompt provenance

[Using GPT-6 Astra: Prompting best practices](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices) is the source of the five behavior modules. Each `modules/*/prompt.md` preserves that subsection's `text` code blocks verbatim, joined by a blank line. Explanatory article prose is not copied. Each `module.json` records the exact subsection and verification date. [prompt-snapshot.json](prompt-snapshot.json) records SHA-256 hashes so an update can be reviewed explicitly.

The `latest-model` URL can change models over time. Before updating, verify that the fetched page is still about GPT-6 Astra; do not silently replace prompts with guidance for a different model. Review changed prompt blocks, update hashes and dates, and run the relevant evaluation cases. There is no network fetch during normal use.

**LabKit additions**, not official recommendations: ordinary-task semantic routing, bounded delegation, per-module guards, model filtering, output budgets, the optional installer and candidate scanner. The official delegation prompt encourages more delegation; it does not claim to reduce agent calls. All five modules are available in new installations; the model selects only useful ones. The original official blocks remain separate from our adaptations so users can compare or remove the adaptations.

LabKit's license applies to its original code and adaptations. OpenAI remains the source of the attributed prompt excerpts; the repository license does not assert ownership or independently relicense third-party material.

## Host evidence

| Source | What it establishes |
|---|---|
| [Build skills](https://learn.chatgpt.com/docs/build-skills) | Explicit and implicit invocation, discovery through description, `agents/openai.yaml`, user/project `.agents/skills` locations |
| [Hooks](https://learn.chatgpt.com/docs/hooks) | Current Codex hook configuration, trust, model/event input, `UserPromptSubmit` and extra developer context |
| [UserPromptSubmit](https://learn.chatgpt.com/docs/hooks#userpromptsubmit) | `prompt` input and `hookSpecificOutput.additionalContext` output; event `matcher` is ignored |
| [Review and trust hooks](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks) | Non-managed definitions must be reviewed/trusted; installation is not activation |
| [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Global/project instruction discovery, override precedence, context limits, new-session loading |
| [Developer settings](https://learn.chatgpt.com/docs/developer-settings) | Shared local Codex agent configuration across desktop, CLI and IDE; cloud environment distinction |
| [Claude Code memory](https://code.claude.com/docs/en/memory) | User/project CLAUDE.md instruction paths and loading |
| [Claude Code Desktop](https://code.claude.com/docs/en/desktop) | Desktop and CLI share the underlying engine and CLAUDE.md project context |
| [Cursor rules](https://prod.cursor.com/docs/rules) | Project .mdc files and alwaysApply frontmatter |

The native CLI present during development was **0.153.0**. The hook handler and registration shape were exercised locally with event fixtures and generated commands. A separately trusted native Codex hook session was **not** run as part of this release, so this version is a development reference, not a verified minimum supported version. Use `/hooks` to check support on the actual host. Managed configurations and older versions may differ.

Skill-only use needs a host that understands skills and can read this folder; semantic triggering remains the host model's choice. The standalone composer can be called from another application. Hook installation here targets Codex on macOS/Linux with Python 3.10+. No Claude Code, Cursor, Windsurf, or Windows hook adapter is claimed.

The current package also implements scoped persistent-rule adapters for Codex, Claude Code and Cursor projects, explicit custom rule files, and manual exports. Rule file editing is tested; native desktop loading and routing remain unverified for those clients. The compatibility table and client-specific verification steps are in [hosts.md](hosts.md). Prompt applicability on other models is not established by transport compatibility.

The hook uses no embedding model, API key, external service, transcript parser, background monitor, or tool interceptor. It never starts agents itself; the host can delegate after selecting that module when permitted. The semantic hook supplies a catalog for the current model to assess each ordinary task. It does not itself classify intent or guarantee changed behavior.
