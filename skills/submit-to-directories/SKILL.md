---
name: submit-to-directories
description: "Use this skill when the user wants to submit their published AI skill or rule repository to community directories and awesome-lists to increase visibility. This includes identifying which directories accept the repo's format, formatting the entry correctly per each directory's CONTRIBUTING.md, and walking through the fork → add entry → open PR process. Trigger when the user says 'submit to awesome list', 'how do I get my skill listed', 'add to the community directory', 'submit a PR to awesome-cursorrules', 'how do people find my skill', or 'promote my repo'. Also trigger right after the repo has been published and the user asks what to do next. Do NOT trigger before the repo is live on GitHub — the repo URL must exist before submitting anywhere. Do NOT trigger for the Claude Plugin Marketplace submission process, which requires a separate .claude-plugin/marketplace.json configuration."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start

Pick one directory from the reference table that matches your rule format. Read its CONTRIBUTING.md. Then:

```bash
# Fork the directory repo on GitHub, then:
git clone https://github.com/{your-username}/{directory-repo}.git
git checkout -b add-{your-repo-name}
# Add your entry alphabetically in the correct category
git commit -m "Add {repo-name}: {description}"
gh pr create --title "Add {repo-name}: {description}"
```

Submit to one directory first. Add others after the first PR is merged.

---

## Directory reference

| Directory | Accepts | Stars | Key requirement |
|---|---|---|---|
| PatrickJS/awesome-cursorrules | .cursorrules / .mdc (Cursor) | 39.9k | PR to `rules/` subdirectory |
| travisvn/awesome-claude-skills | SKILL.md (Claude) | 12.8k | ≥ 10 GitHub stars |
| hesreallyhim/awesome-claude-code | Claude Code tools | 44.9k | See CONTRIBUTING.md |
| github/awesome-copilot | .instructions.md / .agent.md / SKILL.md | 34.5k | Named file conventions required |
| Code-and-Sorts/awesome-copilot-agents | Copilot agents/instructions | 532 | See CONTRIBUTING.md |
| detailobsessed/awesome-windsurf | Windsurf resources | 548 | See CONTRIBUTING.md |
| sanjeed5/awesome-cursor-rules-mdc | .mdc files | 3.5k | Via rules.json |

Always check the current CONTRIBUTING.md before submitting. Requirements change.

---

## Phase 1: Check eligibility

- [ ] The repo is public on GitHub
- [ ] The rule file exists and is in the correct format for that directory
- [ ] The rule has been tested against the target agent
- [ ] For travisvn/awesome-claude-skills: ≥ 10 stars on the repo
- [ ] For github/awesome-copilot: file follows the `.instructions.md` naming convention

---

## Phase 2: Read the target directory's CONTRIBUTING.md

Not optional. Two things to check before writing anything:

1. **Entry format** — exactly how the line should be written
2. **PR title format** — what the title must start with

Also read the last 3 merged PRs to calibrate the format in practice.

---

## Phase 3: Write the entry

Standard format used by most awesome-lists:

```markdown
- **[{Repo Name}]({full GitHub URL})** — {verb-first description, 10–20 words, no trailing period}
```

Description rules:
- Start with a verb: "Blocks", "Generates", "Enforces", "Detects", "Automates"
- 10–20 words
- No "A skill that..." opener
- No trailing period

```markdown
# Bad
- **[my-rules](url)** — Cursor rules for TypeScript.

# Good
- **[my-rules](url)** — Blocks the 5 most common TypeScript patterns that cause silent runtime failures in production
```

---

## Phase 4: Submit the PR

```bash
# 1. Fork the target directory repo on GitHub (click Fork button)
# 2. Clone your fork
git clone https://github.com/{your-username}/{directory-repo-name}.git
cd {directory-repo-name}

# 3. Create a branch
git checkout -b add-{your-repo-name}

# 4. Add your entry in the correct category, in alphabetical order
# Edit README.md (or the relevant file per that directory's structure)

# 5. Commit
git add README.md
git commit -m "Add {repo-name}: {one-line description}"

# 6. Push and open PR
git push origin add-{your-repo-name}
gh pr create \
  --title "Add {repo-name}: {one-line description}" \
  --body "Adds [{repo-name}]({url}) to {Category}."
```

---

## Phase 5: After submitting

Check the PR within 24–48 hours for review comments. If the maintainer requests changes, apply them promptly; stale PRs get closed. Do not open a duplicate PR if there's no response after a week; leave a comment on the existing one.

---

## Platform marketplaces (separate process, not covered here)

**Claude Plugin Marketplace** — requires `.claude-plugin/marketplace.json`. Install command becomes `/plugin marketplace add {username}/{repo}`. See anthropics/skills for the reference implementation.

**cursor.directory** — submit via https://cursor.directory/plugins/new (web form). The site auto-detects `.mdc` files, `SKILL.md`, and `.mcp.json` from the repo.

---

## Common Mistakes

**Submitting before reading CONTRIBUTING.md.**
Every directory has specific format requirements. "PRs Welcome" does not mean any format is acceptable. A non-conforming PR gets closed, and you've wasted the maintainer's time.

**Opening the PR against the upstream repo without forking.**
You don't have write access to someone else's repo. Fork first, change in your fork, then PR from your fork's branch.

**Submitting to directories that don't accept your format.**
A SKILL.md repo submitted to a `.cursorrules`-only directory will be rejected. Match format to directory.

**Not placing the entry alphabetically.**
Most awesome-lists maintain alphabetical order within categories. Adding at the bottom is the most common reason for a "please reorder" review comment.

**Submitting to five directories simultaneously.**
Start with one. A merged PR in one directory makes every subsequent PR easier; an unreviewed PR in five repos at once signals low effort.
