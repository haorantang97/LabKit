# Evaluation

Run from the LabKit root:

```bash
python3 -m unittest discover -s skills/welcome-to-agi/tests -v
```

The suite checks ordinary-message catalog delivery without keyword gating; disabled/plan modules; no user-message promotion; router size/error behavior; original official snapshots; optional legacy keyword mode; installation + initialization; old-label replacement; backups; idempotence; unrelated handlers; and read-only audit coverage.

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

- Installed through the integrated installer: files and registration must complete, followed by clear host-trust instructions.
- Manually copied and explicitly invoked: the skill inspects initialization status and guides setup instead of only saying “available next turn.”
- Normal task without persistent-setup authorization: complete it in manual mode while offering the setup choice once.
- User chooses skill-only or declines: honor that choice, do not repeatedly ask within the conversation.
- Registered hook provides the router marker: follow the catalog directly, without repeating onboarding.

## Native Codex smoke test after trust

1. Install in a disposable project and review/trust the definition with Codex `/hooks`.
2. With an allowed model, submit an ordinary implementation request without correction keywords. Inspect host diagnostics for successful catalog delivery, then selected module reads and the actual deliverable.
3. Submit a simple question. The hook should still supply the catalog; the model may choose no modules. Switch to an unlisted model; the hook should return no guidance.
4. Disable a module, submit another task, and confirm it is absent from the new catalog.
5. Remove registration and start a fresh conversation; confirm this hook no longer runs and unrelated hooks remain.

Record host version, registration/trust status, and observed diagnostics. Native trusted hook delivery is not yet established by this release's automated suite. A valid adapter response or local status field does not prove it.
