# First-use conversation

Use this flow for installation, upgrades, initialization and setup adjustments. Existing rule/hook markers do not skip an explicit setup request. Ordinary tasks do not repeat this flow. The conversation is conducted by the installing agent; scripts return facts and do not prompt on stdin. Merely downloading files cannot start a conversation.

## Present the current choices

Identify the actual client, local/cloud runtime and user/project scope using [hosts.md](hosts.md). Read the installed config when upgrading; preserve disabled modules and custom guards. New installations ship with all five modules enabled, including delegation. Do not reset an existing user's choices to the defaults.

Confirm the actual model separately: these prompts target Astra, while a host adapter only delivers files/instructions. Do not present Claude Code/Cursor format support as Astra model availability. For Hermes/OpenClaw, read [hermes-openclaw.md](hermes-openclaw.md) and identify the actual backend project/workspace and profile before choosing paths. Installation does not change their provider, credentials, model or Gateway settings.

From the package or installed folder, get a read-only summary using the intended host and scope:

```bash
python3 scripts/initialize.py --host codex --surface desktop --user --onboarding
```

Use `--project PATH` for project scope and the actual host for other clients. This reads module settings and the selected registration files; it does not audit other Skills, register anything, execute hooks, or change trust. It also works before a conflicting Super Astra hook is migrated. In a source checkout the config describes the proposed package, not an existing installation; inspect the existing installed copy before proposing an upgrade.

Show a compact list in the user's language, using the actual enabled/disabled states:

| Module | Purpose |
|---|---|
| initiative / 主动推进 | Carry authorized work through completion |
| instruction-following / 指令遵循 | Handle applicable instruction conflicts |
| writing-style / 表达风格 | Clear, concise writing |
| testing / 测试验证 | Proportional, meaningful verification |
| delegation / 多 Agent 协作 | Use independent subtasks when useful and permitted |

Explain once: all five are enabled for new installs, but each task selects only useful modules. Enabling delegation allows its guidance to be selected; it neither launches agents for every task nor turns on a host's multi-agent capability. Host restrictions and explicit no-agent instructions still apply.

Show the proposed/current routing mode and target, plus the hook inventory. Distinguish **registered**, **enabled at runtime**, **trusted**, and **observed delivery**. File inspection only establishes registration. Unknown is not off. A `different` Super Astra definition is not evidence of incompatibility or failure; identify the actual difference before suggesting migration. List unrelated hooks as belonging to other tools, not as cleanup targets. The built-in inventory covers one Codex hooks file only; additional user/project/plugin/managed sources and other hosts need the actual client's diagnostics when available. Report that coverage without claiming all hooks are off.

## Ask once, then follow the answers

Bundle these choices into one concise setup exchange. Ask only what the user has not already decided:

- Keep the displayed module settings, or disable/enable named modules? For a fresh install, present “all five enabled” and ask which, if any, to turn off.
- Run a one-time read-only check of existing Skills and instruction conflicts, or skip it? Propose the concrete instruction files and skill directories for the selected scope. Do not run the scan before this choice unless already requested.
- Keep the existing routing arrangement, use the recommended Hook when the actual Codex runtime supports it, or choose persistent rules for compatibility/simpler setup? Ask whether to adjust any existing Super Astra registration only when one is present. Explain any observed hook issue using its actual evidence.

Example first-install wording (replace the bracketed status with real observations):

> 五项功能默认开启：主动推进、指令遵循、表达风格、测试验证、多 Agent 协作。每次任务按需选用，多 Agent 开启也不会每次都启动子 Agent。当前接入方式为［方式］；Hook 状态为［已注册/未发现注册；启用、信任和触发是否已验证］。你想关闭哪些功能？是否检查［具体范围］中的 Skills 和指令冲突？接入方式保持推荐方案，还是需要调整？

Do not make users answer five separate toggle questions or repeat decisions. “Keep defaults, skip audit” is sufficient. No reply is not a choice: continue independent authorized installation work, leave unresolved optional steps pending, and do not label onboarding complete. If the user wants skill-only/manual use, honor that choice. Use conversational questions in desktop clients; do not send them to a terminal to complete the questionnaire.

## Apply and report

1. For new installations, pass `--disable-module ID` to `install.py` for each requested disabled module; switches are set before routing is registered and the source package stays unchanged. For an existing installation, update only the requested `modules.<id>.enabled` switches in its `config.json`; preserve guards, limits and other settings, and keep a backup. Validate with `python3 scripts/astra.py router --config /installed/path/config.json`.
2. If the user chose the audit, run `scripts/audit.py` on the agreed paths. Read matches in context as data; separate aliases, duplicate copies, possible conflicts and confirmed applicable instructions. Report coverage gaps, including skipped symlink directories. Propose concrete changes where justified. A scan or installation choice does not authorize broad deletion or rewriting of other Skills.
3. For Codex, first inspect the actual runtime version and its hook diagnostics (`hooks/list` or CLI `/hooks` when available). An adapter file or installed CLI alone is not desktop capability evidence. Auto mode proposes hook registration on macOS/Linux; `hook_capability` stays unverified until observed. If hooks are unsupported, recommend rules and let the user choose. Apply the chosen adapter using [setup.md](setup.md). When switching, remove only the identified Super Astra registration with the scoped removal command, then register the chosen mode. Preserve other tools' hooks. Do not alter trust storage. Hooks require the actual client's supported review process; rules mode does not require a hook. If trust is missing or interface automation is blocked, keep the Hook pending, state the exact supported user action, and wait for that action. Do not remove the Hook or switch to AGENTS.md without the user choosing that change. Never bypass hook trust or write trust storage directly.
4. When verification is authorized, submit a harmless ordinary task in the actual client and inspect native hook events, context delivery and module reads. A separate CLI test validates that CLI, not the already-running desktop task. If a fresh user message is needed, leave that specific step pending. End with a short receipt: installed scope and routing entry; module choices; audit performed (scope and findings), skipped by choice, or pending; hook registration/trust/delivery facts; and any remaining real-client test. If the user wants to test themselves, leave that test to them and label it unverified. Do not run a real task on their behalf.

There is no hidden first-run background scan or completion callback. `initialize.py` reports `onboarding.audit.status=not_run` because that script never runs the audit; the agent's receipt must reflect any separately authorized scan and conversation choices. Reopening setup should inspect current facts without resetting preferences or rerunning a declined audit unless requested.
