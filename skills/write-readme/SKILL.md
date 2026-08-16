---
name: write-readme
description: "Use this skill when the user needs a README.md written for their AI skill or rule repository. This includes writing the first-screen section (banner image placeholder, badge row, one-line value statement), multi-platform installation commands, a what-it-does prose section, a features or skills list, contributing section, and license footer. Trigger when the user says 'write a README', 'create the README for my repo', 'I need a README for my skill', 'document this rule', or 'help me write the GitHub page for this'. Also trigger when the user has a finished rule file and wants to package it for GitHub but hasn't written the README yet. Do NOT trigger for editing an existing README (edit the file directly), for writing CONTRIBUTING.md or LICENSE (that is scaffold-repo-files), or for generating banner images (that is create-visual-assets)."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start

Ask for two things if not already provided: repo name and a one-line value statement. Then write sections in this order: first screen → install commands → what it does → content list → footer. Use PolyForm Noncommercial License 1.0.0 by default; do not ask about licensing unless the user explicitly wants a different license.

---

## Phase 1: Gather before writing

| What you need | Default if not provided |
|---|---|
| Repo name (kebab-case) | Infer from skill/rule file name |
| Platform(s) | Ask — determines install commands |
| One-line value statement | Ask — cannot be invented reliably |
| GitHub username | Ask |
| License type | PolyForm Noncommercial 1.0.0 by default; ask only for an explicit override |
| Repo type | single-skill / collection / awesome-list |

Do not ask more than two questions at once. If the skill file is already available, read it to extract most of this.

---

## Phase 2: Write the first screen

Everything above the fold. Must contain: banner placeholder, badge row, title, one-liner. Installation command must appear within 10 lines of the title.

```markdown
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner.svg">
    <img width="700" alt="{REPO_NAME}" src="assets/banner.svg">
  </picture>
</p>

# {Repo Name}

[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-blue.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![Last Updated](https://img.shields.io/badge/updated-{Mon YYYY}-blue.svg?style=flat-square)]()

> {One-line value statement: what problem does this solve, for whom.}
```

Badge rules:
- Use `style=flat-square` on all badges; it's cleaner than the default
- 3–5 badges; never more than 6
- "Last Updated" badge must match the actual month/year of writing

---

## Phase 3: Write the install section

Place before any long description. Cover every platform the user targets.

```markdown
## Install

**Claude Code:**
```
/plugin marketplace add {username}/{repo-name}
```

**Cursor:**
```bash
cp .cursorrules ~/your-project/
# or for .mdc rules:
cp -r .cursor/rules/ ~/your-project/.cursor/
```

**Windsurf:**
```bash
cp .windsurfrules ~/your-project/
```

**AGENTS.md (Codex / any agent):**
```bash
cp AGENTS.md ~/your-project/
```
```

Only include platforms that are actually supported. Do not pad with platforms that have no rule file.

---

## Phase 4: Write the description section

Two to four sentences of prose. No bullet lists. Lead with the problem, then the solution.

```markdown
## What It Does

{Problem sentence: what situation or pain point does this address.}
{Solution sentence: how this rule/skill changes the AI's behavior.}
{Optional: one concrete before/after statement or measurable outcome.}
```

If the user has quantified effectiveness (e.g., eval pass rate), include it here.

---

## Phase 5: Write the content section

**Single-skill repo:**
```markdown
## Features

- {Specific capability A, stated as a concrete outcome}
- {Specific capability B}
```

**Multi-skill collection:**
```markdown
## Skills

### {Category A}

- **[{skill-name}]({path/to/SKILL.md})** — {verb-first, 10–20 words, what it does}

### {Category B}

- **[{skill-name}]({path/to/SKILL.md})** — {description}
```

**Awesome-list:**
```markdown
## {Category A}

- **[{Name}]({url})** — {verb-first description, 10–20 words}
```

Entry description rules:
- Start with a verb ("Blocks", "Generates", "Enforces", "Detects")
- 10–20 words; no trailing period; no "A skill that..." opener

---

## Phase 6: Write the footer

```markdown
## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

PolyForm Noncommercial License 1.0.0 — see [LICENSE](LICENSE).
```

If CONTRIBUTING.md doesn't exist yet, write: `Pull requests are welcome. Please open an issue first to discuss what you'd like to change.`

---

## Common Mistakes

**Opening with a long description paragraph before the install command.**
Readers who arrive from a search want the command, not a description. Install first, describe second.

**Writing features as noun phrases.**
"PDF extraction" is a feature label. "Extracts text and tables from any PDF without additional dependencies" is a feature description. Use the second form.

**Using placeholder text in the final output.**
Never leave `{REPO_NAME}`, `{username}`, or `{description}` in the delivered README. Fill every placeholder or ask for the missing information before writing.

**Omitting the dark-mode banner alternative.**
GitHub renders in dark mode for many users. A `<picture>` tag with both `srcset` options takes 5 lines and prevents the banner from appearing broken.

**Making the badge row the only content above the fold.**
Badges show metadata; they don't show what the repo does. Always include the one-liner value statement above the fold.
