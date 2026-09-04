# Contributing

**English** | [中文](CONTRIBUTING.zh-CN.md)

This repo collects four top-level skills. Publishing and behavior toolkits may contain internal modules, but those modules are not separate top-level entries. PRs that fit this scope are welcome.

## Entry Format

Each top-level skill in this repo follows the same structure:

```
skills/{top-level-skill-name}/
  └── SKILL.md
```

Internal modules for `skill-skill` belong under `skills/skill-skill/modules/`.

`SKILL.md` is plain markdown with a YAML front matter holding `name`, `description`, and `license`.

## Requirements

Submissions must:

- Serve a distinct publishing, daily-work, or agent-behavior need that existing skills do not already handle
- Use the five-segment description method (main trigger, positive enumeration, colloquial triggers, edge case expansion, negative samples)
- Include a Quick Start section and a Common Mistakes section with at least two items
- Pass the de-AI checklist in `skills/skill-skill/modules/polish-rule-content/SKILL.md`
- Be tested against at least one agent before submission

## Quality Gate

> [!NOTE]
> Skills that overlap an existing skill's scope, lack negative samples, or use vague constraints ("be careful", "follow best practices") will be closed without review.

## PR Title Format

Good:
- `Add {skill-name}: {one-line description}`
- `Fix {skill-name}: {what changed and why}`

Not good:
- `Update README`
- `Add my skill`

## What Gets Rejected

- Skills that duplicate an existing skill's scope without clear differentiation
- Skills not tested against the target agent before submission
- Bumping version numbers in commits that touch unrelated files

## Process

1. Fork this repository
2. Add a new standalone skill under `skills/{skill-name}/SKILL.md`, or an internal publishing module under `skills/skill-skill/modules/{module-name}/SKILL.md`
3. Update the README's "Skills" section with a link to the new file
4. Open a PR with the title format above

For changes to existing skills, describe what the change fixes and confirm you tested it.
