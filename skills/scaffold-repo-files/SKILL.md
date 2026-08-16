---
name: scaffold-repo-files
description: "Use this skill when the user needs to create the supporting files for a GitHub repository beyond the rule file itself and the README. This includes choosing and writing the LICENSE file, writing CONTRIBUTING.md with submission format and quality gates, creating .github/PULL_REQUEST_TEMPLATE.md, setting up the correct directory structure, and creating optional files like CHANGELOG.md and SECURITY.md. Trigger when the user says 'set up my repo files', 'what other files do I need', 'create a CONTRIBUTING file', 'scaffold the repo structure', 'set up the directory layout', or 'I have the skill and README, what's next'. Also trigger when the user is about to publish and asks what supporting files a proper repo should have. Do NOT trigger for writing the README itself (that is write-readme), for creating banner images (that is create-visual-assets), or for the git and GitHub operations (that is publish-to-github)."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start

Three files cover 90% of cases:

1. `LICENSE` — CC0 if pure rule/prompt content, MIT if there are scripts (Phase 2)
2. `CONTRIBUTING.md` — even a 10-line version beats nothing (Phase 3)
3. `.github/PULL_REQUEST_TEMPLATE.md` — copy the template in Phase 4

Create them in that order.

---

## Phase 1: Determine repo type and license

**Repo type determines directory structure:**
- **Single-skill**: rule file at root, flat layout
- **Multi-skill collection**: `skills/{name}/SKILL.md` or `plugins/{name}/SKILL.md`
- **Awesome-list**: no rule files, only README + CONTRIBUTING

**License selection:**

| Content type | License | Reason |
|---|---|---|
| Pure rule/prompt content | **CC0 1.0** | No copyright barriers, maximum community reuse |
| CLI tool or code-heavy repo | **MIT** | Standard for code, attribution preserved |
| Both code and content | **MIT + CC0** (dual) | Code under MIT, prompt/rule content under CC0 |

When in doubt: if there are no executable scripts, use CC0.

---

## Phase 2: Write LICENSE

**CC0 (pure content):**
```
CC0 1.0 Universal

The person who associated a work with this deed has dedicated the work to the
public domain by waiving all of their rights to the work worldwide under
copyright law, including all related and neighboring rights, to the extent
allowed by law.

You can copy, modify, distribute and perform the work, even for commercial
purposes, all without asking permission.
```

**MIT (tools/code):**
```
MIT License

Copyright (c) {YEAR} {AUTHOR NAME}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Fill `{YEAR}` with the current year. Fill `{AUTHOR NAME}` with the user's name or GitHub username.

---

## Phase 3: Write CONTRIBUTING.md

Adjust based on repo type. Remove sections that don't apply.

```markdown
# Contributing

## Entry Format

Each submission must follow this pattern:

```markdown
- **[Name](link)** — One-line description starting with a verb. (10–25 words, no trailing period)
```

## Requirements

Submissions must:
- Include a working rule file tested against the target agent
- Solve a specific, named problem — not a general "best practices" collection
- Not duplicate an existing entry without meaningful differentiation

## Quality Gate

> [!NOTE]
> Submissions with fewer than 10 GitHub stars will be closed without review.

## PR Title Format

✅ `Add {name}: {one-line description}`
✅ `Fix {name}: {what changed and why}`
❌ `Update README`
❌ `Add my skill`

## What Gets Rejected

- Duplicates of existing entries
- Rule files not tested against the target agent before submission
- AI-generated PRs submitted without human review

## Process

1. Fork this repository
2. Add your entry in the correct category, alphabetically
3. Open a PR with the title format above
```

**For single-skill repos** (shorter version):
```markdown
# Contributing

Bug reports and improvements are welcome. Open an issue before submitting a PR.

For changes to the rule content, describe what the change fixes and confirm you tested it against the target agent.
```

---

## Phase 4: Create .github/ templates

**PR Template** (`.github/PULL_REQUEST_TEMPLATE.md`):
```markdown
## What does this add or change?

[One sentence.]

## Have you tested this?

- [ ] I tested the rule/skill against the target agent
- [ ] The rule file is valid (no broken YAML front matter or syntax errors)
- [ ] The entry follows the format in CONTRIBUTING.md

## Link to the skill or rule repository

[URL — required for collection repo submissions]
```

**CI workflow** (`.github/workflows/ci.yml`) — recommended for collection repos:
```yaml
name: CI
on: [push, pull_request]
jobs:
  links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check Markdown links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: 'yes'
```

---

## Phase 5: Set up directory structure

**Single-skill repo:**
```
{repo-name}/
├── SKILL.md          (or .cursorrules / .windsurfrules / AGENTS.md)
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── assets/
│   ├── banner.svg
│   └── banner-dark.svg
└── .github/
    └── PULL_REQUEST_TEMPLATE.md
```

**Multi-skill collection:**
```
{repo-name}/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── CHANGELOG.md      (optional)
├── skills/
│   ├── skill-a/
│   │   └── SKILL.md
│   └── skill-b/
│       └── SKILL.md
├── assets/
│   ├── banner.svg
│   └── banner-dark.svg
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── ci.yml
```

**Awesome-list:**
```
awesome-{topic}/
├── README.md
├── CONTRIBUTING.md
├── LICENSE           (CC0)
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── ci.yml
```

---

## Optional files

**CHANGELOG.md** — add when the repo is actively maintained:
```markdown
# Changelog

## [Unreleased]

## [1.0.0] - {YYYY-MM-DD}

### Added
- Initial release
```

**SECURITY.md** — required for repos whose rules execute arbitrary code:
```markdown
# Security Policy

## Reporting a Vulnerability

Do not open a public GitHub issue for security concerns.
Email: {contact email}

We will respond within 72 hours.

## Important Notice

Rules in this repository may execute code in your agent's environment.
Only install from sources you trust. Review all rule content before use.
```

---

## Common Mistakes

**Skipping CONTRIBUTING.md for collection repos.**
A missing CONTRIBUTING.md tells potential contributors there's no clear process. A 20-line file makes the difference between getting drive-by PRs and getting well-formatted ones.

**Using GPL for AI rule content.**
GPL applies to software distributed as executable code. Applying it to prompt files creates legal ambiguity and discourages use. CC0 or MIT are the right choices.

**Creating .github/ but leaving PULL_REQUEST_TEMPLATE.md empty.**
An empty PR template is worse than no template; it signals an abandoned intention. Either write a minimal working template or skip the file.

**Putting all rule files in the root directory for a collection repo.**
Five rule files at root is manageable. Twenty is chaos. Use `skills/` or `rules/` subdirectories from the start.

**Not creating an assets/ directory.**
Even without banner images yet, create the `assets/` directory with placeholder files so the README's `<picture>` tag has a valid path.
