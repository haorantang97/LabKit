# Astra guidance in Hermes and OpenClaw

The prompt modules target **Astra, the model**. Hermes, OpenClaw and Codex are **hosts** that can supply instructions and tools. Check the actual selected model/provider before claiming an Astra setup. This package does not configure model endpoints, credentials or subscriptions, and a rule adapter does not prove that a host currently offers Astra. Claude Code/Cursor adapters are reusable file formats, not evidence of an Astra runtime or equivalent effects on other models.

## Hermes

Use the actual project/backend working directory, including when interacting through a dashboard or messaging gateway:

```bash
python3 scripts/install.py --host hermes --surface cli --project /actual/project
python3 scripts/install.py --host hermes --surface cli --project /actual/project --apply
```

Project mode stores the complete bundle in `/actual/project/.hermes/skills/welcome-to-agi` and adds a scoped entry to the selected project context file. That project-local bundle is loaded through explicit rule paths; this does **not** claim Hermes automatically indexes that directory as a skill catalog. The adapter preserves an existing `.hermes.md`, `HERMES.md`, `AGENTS.override.md`, `AGENTS.md`, `CLAUDE.md` or `.cursorrules` by appending only its own block to the first nonempty candidate. With no candidate it uses AGENTS.md. If existing Cursor modules would be masked, it asks for an explicit target. Ancestor context, host version and actual startup CWD still need inspection; pass `--rules-file PATH` for the verified active file when needed.

For catalog installation, `--host hermes --user` copies into `$HERMES_HOME/skills` (default `~/.hermes/skills`). It defaults to manual activation because there is no assumed global AGENTS.md. Supply `--rules-file /actual/project/AGENTS.md --mode rules` only after confirming that file is loaded. Do not write routing instructions into SOUL.md automatically or claim a home-directory AGENTS.md affects every project. Existing installations are preserved; upgrades keep custom config/modules.

Sources checked 2026-09-05: [Hermes context files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files/) and [Skills system](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/).

## OpenClaw

Use the workspace of the intended agent, as configured in the running Gateway. `--project` means that workspace, not an arbitrary code repository or assumed `~/.openclaw/workspace`:

```bash
python3 scripts/install.py --host openclaw --surface cli --project /actual/agent-workspace
python3 scripts/install.py --host openclaw --surface cli --project /actual/agent-workspace --apply
```

The bundle goes into `<workspace>/skills/welcome-to-agi`; a scoped routing entry goes into `<workspace>/AGENTS.md`. Existing instructions are preserved and backed up. User scope stores shared skill files under `$OPENCLAW_STATE_DIR/skills` (default `~/.openclaw/skills`) and defaults to manual activation. A shared skill directory is not a shared AGENTS.md; each intended workspace needs its own verified rule entry. Do not overwrite SOUL.md, USER.md, memory or Gateway settings.

Sources checked 2026-09-05: [OpenClaw workspace files](https://docs.openclaw.ai/concepts/agent-workspace) and [Skills locations](https://docs.openclaw.ai/tools/skills).

## Verification and limits

These adapters implement file installation, scoped rule updates, backup and removal. Tests exercise disposable directories; native Hermes/OpenClaw model calls and gateway sessions have not been tested for this package. Their hooks are not Codex's UserPromptSubmit protocol: this release provides **rule adapters only** and `--mode hook` rejects these hosts.

In the real host, confirm the selected model, profile, working directory/workspace, context-file loading and accessible module paths. Start a fresh session, submit an ordinary task without naming the skill and observe the module reads and result. Respect the host's context scanning, trust, skill allowlists and sandbox boundaries. A file rejected or truncated by the host is not an active rule; use the host's supported review/configuration process, never bypass its checks. Keep initialization choices from [onboarding.md](onboarding.md), including the optional conflict audit and user-selected module switches.
