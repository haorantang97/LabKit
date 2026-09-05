# Evaluation

Run from the LabKit root:

```bash
python3 -m unittest discover -s skills/welcome-to-agi/tests -v
```

The suite checks ordinary-message catalog delivery without keyword gating; disabled/plan modules; no user-message promotion; router size/error behavior; original official snapshots; optional legacy keyword mode; installation + initialization; old-label replacement; backups; idempotence; unrelated handlers; and read-only audit coverage.

## Host adapter update (2026-09-05)

### Guided onboarding update

45 automated tests pass locally, including six onboarding cases. They verify that read-only inspection works before a legacy-hook migration, never executes the inspected commands, preserves existing module choices, reports malformed/unsupported hook sources without claiming they are off, rejects mutating inspection flags, and installs user-selected module switches before registration without changing the source. Disabled module files may be removed without breaking inspection.

These are script tests in disposable directories. The user will test the revised installation conversation themselves; no real user Skills audit, configuration adjustment, native hook activation, or independent agent trial was run for this update. The expected conversation is documented in [onboarding.md](onboarding.md).

### Previous file-adapter update

39 automated tests pass locally. Added coverage includes real installer subprocesses for Codex, Claude Code and Cursor project profiles; preview without writes; generated references to the installed folder (including Unicode/spaced paths); repeated initialization; exact preservation of surrounding CRLF/UTF-8 instructions; backups and scoped removal after later user edits; override/symlink/marker conflicts; changed Cursor activation metadata; unknown/conflicting host detection; CODEX_HOME paths; cloud/manual fallback; hook/rule migration; removal with broken config; and portable/manual UI exports.

These tests execute file adapters in temporary projects, not the named desktop applications. Codex Desktop, Claude Code Desktop and Cursor native loading and ordinary-task execution remain **not verified** for this update. Use the [actual-client checks](hosts.md#在实际使用的客户端验证) and record source loading, module reads and deliverables before making a native compatibility claim. There is no extra model evaluation in this update; the v2 trial below remains historical evidence for the shared routing instructions.

## Version 2 independent model trial

An independent agent received the actual generated router context and ordinary requests, without expected module choices:

| Request | Observed module reads and outcome |
|---|---|
| `17 × 6 等于多少？` | No module files read; answered 102 |
| Implement a Python nonnegative integer seconds-to-mm:ss function, retain total minutes above one hour, reject invalid input, and verify | Read initiative/testing prompts and guards; implemented the function; 13 boundary/invalid-input cases passed |
| Initialize a fresh installed copy in a disposable project | Inspected status and applied registration; exactly one hook; all five candidates available; trust/delivery still not_verified |

The supplied context is an **actual hook-generated fixture**, not a trusted native host invocation. This establishes one model's selection and execution, not statistical reliability or guaranteed native delivery. No extra classifier, embeddings, or subagents were used by the evaluated workflow.

The trial found stale v1 setup/evaluation descriptions (keyword gating, delegation default off, unrelated prompts expected to skip). Version 2 documentation replaces these with ordinary-task semantic routing. The v1 malformed JSON bug remains covered by regression tests.

## First-use cases

- Installed through the integrated installer: present module switches and hook facts, ask the unresolved module/audit/routing choices, then complete authorized file setup. Report any unanswered choice as pending. Rules lead to actual-client loading checks; hooks add the separate trust step; manual explicitly reports no automatic entrypoint.
- Manually copied and explicitly invoked: the skill inspects initialization status and guides setup instead of only saying “available next turn.”
- Normal task without persistent-setup authorization: complete it in manual mode while offering the setup choice once.
- User chooses skill-only or declines: honor that choice, do not repeatedly ask within the conversation.
- Registered hook provides the router marker or a persistent rule is already loaded: ordinary tasks follow its entry without repeating onboarding. Explicit installation, upgrade or setup-adjustment requests still use the first-use conversation.
- Audit accepted: run only the agreed scope and explain findings in context; audit declined: skip and record that choice. Do not start by scanning the user's Skills.
- New install keeps all five modules available, including delegation, unless the user names exclusions. An existing disabled module stays disabled on upgrade.

## Native Codex smoke test after trust

1. Install in a disposable project and review/trust the definition with Codex `/hooks`.
2. With an allowed model, submit an ordinary implementation request without correction keywords. Inspect host diagnostics for successful catalog delivery, then selected module reads and the actual deliverable.
3. Submit a simple question. The hook should still supply the catalog; the model may choose no modules. Switch to an unlisted model; the hook should return no guidance.
4. Disable a module, submit another task, and confirm it is absent from the new catalog.
5. Remove registration and start a fresh conversation; confirm this hook no longer runs and unrelated hooks remain.

Record host version, registration/trust status, and observed diagnostics. Native trusted hook delivery is not yet established by this release's automated suite. A valid adapter response or local status field does not prove it.
