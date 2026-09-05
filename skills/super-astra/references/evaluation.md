# Evaluation

Run from the LabKit root:

```bash
python3 -m unittest discover -s skills/super-astra/tests -v
```

## Automated coverage

The suite checks ordinary-message catalog delivery without keyword gating; disabled and plan-only modules; no user-message promotion; router size/error behavior; official prompt snapshots; optional keyword mode; installation and initialization; configuration audit coverage; and portable manual exports.

File-adapter tests use disposable projects for Codex, Claude Code, Cursor, Hermes and OpenClaw. They cover preview without writes, references to the installed folder (including Unicode and spaced paths), repeated initialization, current hook updates, preservation of unrelated handlers, exact CRLF/UTF-8 instruction bytes, backups and scoped removal after later user edits. They also check damaged or duplicate rule markers, symlinks, shadowed targets, changed Cursor activation metadata, host detection, profile paths and conflicts between hook and rule modes.

Onboarding tests verify that inspection never executes registered commands, preserves module choices, reports malformed or unsupported hook sources without claiming they are off, rejects mutating inspection flags, and applies selected module switches before registration without changing the source package.

These tests exercise scripts and file adapters. They do not establish native client loading, hook trust, model availability or reliable module selection. Use the [actual-client checks](hosts.md#在实际使用的客户端验证) and record source loading, module reads and deliverables before making a native compatibility claim. See [Hermes/OpenClaw guidance](hermes-openclaw.md) for their workspace and catalog boundaries.

## First-use cases

- Installed through the integrated installer: present module switches and hook facts, ask the unresolved module/audit/routing choices, then complete authorized file setup. Report any unanswered choice as pending. Rules lead to actual-client loading checks; hooks add the separate trust step; manual explicitly reports no automatic entrypoint.
- Manually copied and explicitly invoked: inspect initialization status and guide setup instead of only saying “available next turn.”
- Normal task without persistent-setup authorization: complete it in manual mode while offering the setup choice once.
- User chooses skill-only or declines: honor that choice and do not repeatedly ask within the conversation.
- Registered hook provides the router marker or a persistent rule is already loaded: ordinary tasks follow its entry without repeating onboarding. Explicit installation or setup-adjustment requests still use the first-use conversation.
- Audit accepted: run only the agreed scope and explain findings in context; audit declined: skip and record that choice. Do not start by scanning the user's Skills.
- New install keeps all five modules available, including delegation, unless the user names exclusions. Reopening setup preserves disabled modules.

The expected conversation is documented in [onboarding.md](onboarding.md).

## Native Codex smoke test after trust

1. Install in a disposable project and review/trust the definition with Codex `/hooks`.
2. With an allowed model, submit an ordinary implementation request without correction keywords. Inspect host diagnostics for successful catalog delivery, then selected module reads and the actual deliverable.
3. Submit a simple question. The hook should still supply the catalog; the model may choose no modules. Switch to an unlisted model; the hook should return no guidance.
4. Disable a module, submit another task, and confirm it is absent from the new catalog.
5. Remove registration and start a fresh conversation; confirm this hook no longer runs and unrelated hooks remain.

Record host version, registration/trust status, and observed diagnostics. Native trusted hook delivery is not established by the automated suite. A valid adapter response or local status field does not prove it.
