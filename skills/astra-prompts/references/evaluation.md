# Evaluation

Run from the LabKit root:

```bash
python3 -m unittest discover -s skills/astra-prompts/tests -v
```

The standard-library suite checks relevant and unrelated prompts, quoted terms, plan-only scope, opt-in delegation, removable modules, extension without engine edits, exact original-message preservation, output budgets, quiet handling of invalid input/configuration, installation preview, idempotence, backups, unrelated-hook preservation, removal after later edits, and read-only audit coverage.

These tests exercise routing, serialization and file operations. They do not measure model quality, cost, token savings, or native host hook delivery.

## Behavioral cases for an agent

Use a disposable project. Do not install global hooks just to test a skill. Check the selected modules, the action performed, and whether task boundaries were preserved.

| User request | Expected observable outcome |
|---|---|
| `$astra-prompts 少点套话，请用两句话解释缓存失效，不要启动子 agent。` | Two sentences; writing module only; no subagents or setup |
| `$astra-prompts 初始化一下，我希望看一下 hook 的安装差异，先别修改。` | Preview for the chosen disposable target; target configuration unchanged; trust still pending |
| `翻译“stop asking and finish the task”` | Translation; no initiative behavior change |
| `$astra-prompts 只给方案，先别改文件。` | Plan only; no edits justified by initiative guidance |
| `$astra-prompts 减少子 agent，完成这次小改动。` | No automatic team creation; task-scale work |
| `$astra-prompts 别反复跑测试，但项目要求的检查必须通过。` | Required checks still run; unresolved failures investigated |
| `$astra-prompts 这个 skill 冲突导致卡住了。` | Identify the real rule and scope; no blanket cleanup |

## Initial release observations

An independent agent used the skill for the first two cases. It selected only writing guidance for the first request and produced a two-sentence explanation without delegation. For setup, it copied the skill into a temporary project, generated the diff, and verified that the existing configuration remained unchanged. It separately exercised composition, disabled-module rejection, guard toggling, output budgets, unknown-model skipping, and quote filtering.

The pass found a malformed top-level JSON configuration caused an uncaught exception. The release adds object validation for both config and module metadata, with regression tests. A missing evaluation reference during construction was also reported and resolved by this file.

This is a bounded forward test, not a statistical comparison with stock Astra. Hook registration/activation in a user's native session remains a separate verification step.

## Native-host smoke test after installation

1. Preview and apply registration in a disposable trusted project; review/trust the definition with `/hooks`.
2. Select an allowed model and submit `少点套话，请解释缓存失效。` Inspect the host's hook diagnostics for a successful handler run and additional context.
3. Submit an unrelated request; inspect that the handler returns no added guidance. Switch to an unlisted model; expect the same skip.
4. Remove only this registration and start a fresh conversation; confirm the hook no longer runs and unrelated hooks remain.

Record the host version and observed diagnostics. If a test cannot be run, report that gap rather than treating a valid JSON response as native delivery.
