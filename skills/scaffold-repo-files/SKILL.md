---
name: scaffold-repo-files
description: "Use this skill when the user needs to create the supporting files for a GitHub repository beyond the rule file itself and the README. This includes choosing and writing the LICENSE file, writing CONTRIBUTING.md with submission format and quality gates, creating .github/PULL_REQUEST_TEMPLATE.md, setting up the correct directory structure, and creating optional files like CHANGELOG.md and SECURITY.md. Trigger when the user says 'set up my repo files', 'what other files do I need', 'create a CONTRIBUTING file', 'scaffold the repo structure', 'set up the directory layout', or 'I have the skill and README, what's next'. Also trigger when the user is about to publish and asks what supporting files a proper repo should have. Do NOT trigger for writing the README itself (that is write-readme), for creating banner images (that is create-visual-assets), or for the git and GitHub operations (that is publish-to-github)."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start

Three files cover 90% of cases:

1. `LICENSE` — PolyForm Noncommercial 1.0.0 by default; use another license only when explicitly requested (Phase 2)
2. `CONTRIBUTING.md` — even a 10-line version beats nothing (Phase 3)
3. `.github/PULL_REQUEST_TEMPLATE.md` — copy the template in Phase 4

Create them in that order.

---

## Phase 1: Determine repo type and license

**Repo type determines directory structure:**
- **Single-skill**: rule file at root, flat layout
- **Multi-skill collection**: `skills/{name}/SKILL.md` or `plugins/{name}/SKILL.md`
- **Awesome-list**: no rule files, only README + CONTRIBUTING

**License default:**

For all original skill and rule repositories, use **PolyForm Noncommercial License 1.0.0** by default. It allows noncommercial use, modification, and distribution; commercial use requires separate permission. Only use MIT, CC0, or another license when the user explicitly requests or has already chosen it.

When in doubt, keep PolyForm Noncommercial 1.0.0 rather than selecting a license based on whether the repository contains scripts.---

## Phase 2: Write LICENSE

**PolyForm Noncommercial 1.0.0 (default):**
Use the exact official text below. Put the repository owner's notice on the plain-text line immediately before it; replace the placeholders first.

```text
Required Notice: Copyright (c) {YEAR} {AUTHOR NAME}

# PolyForm Noncommercial License 1.0.0

<https://polyformproject.org/licenses/noncommercial/1.0.0>

## Acceptance

In order to get any license under these terms, you must agree to them as both strict obligations and conditions to all your licenses.

## Copyright License

The licensor grants you a copyright license for the software to do everything you might do with the software that would otherwise infringe the licensor's copyright in it for any permitted purpose.  However, you may only distribute the software according to [Distribution License](#distribution-license) and make changes or new works based on the software according to [Changes and New Works License](#changes-and-new-works-license).

## Distribution License

The licensor grants you an additional copyright license to distribute copies of the software.  Your license to distribute covers distributing the software with changes and new works permitted by [Changes and New Works License](#changes-and-new-works-license).

## Notices

You must ensure that anyone who gets a copy of any part of the software from you also gets a copy of these terms or the URL for them above, as well as copies of any plain-text lines beginning with `Required Notice:` that the licensor provided with the software.  For example:

> Required Notice: Copyright Yoyodyne, Inc. (http://example.com)

## Changes and New Works License

The licensor grants you an additional copyright license to make changes and new works based on the software for any permitted purpose.

## Patent License

The licensor grants you a patent license for the software that covers patent claims the licensor can license, or becomes able to license, that you would infringe by using the software.

## Noncommercial Purposes

Any noncommercial purpose is a permitted purpose.

## Personal Uses

Personal use for research, experiment, and testing for the benefit of public knowledge, personal study, private entertainment, hobby projects, amateur pursuits, or religious observance, without any anticipated commercial application, is use for a permitted purpose.

## Noncommercial Organizations

Use by any charitable organization, educational institution, public research organization, public safety or health organization, environmental protection organization, or government institution is use for a permitted purpose regardless of the source of funding or obligations resulting from the funding.

## Fair Use

You may have "fair use" rights for the software under the law. These terms do not limit them.

## No Other Rights

These terms do not allow you to sublicense or transfer any of your licenses to anyone else, or prevent the licensor from granting licenses to anyone else.  These terms do not imply any other licenses.

## Patent Defense

If you make any written claim that the software infringes or contributes to infringement of any patent, your patent license for the software granted under these terms ends immediately. If your company makes such a claim, your patent license ends immediately for work on behalf of your company.

## Violations

The first time you are notified in writing that you have violated any of these terms, or done anything with the software not covered by your licenses, your licenses can nonetheless continue if you come into full compliance with these terms, and take practical steps to correct past violations, within 32 days of receiving notice.  Otherwise, all your licenses end immediately.

## No Liability

***As far as the law allows, the software comes as is, without any warranty or condition, and the licensor will not be liable to you for any damages arising out of these terms or the use or nature of the software, under any kind of legal claim.***

## Definitions

The **licensor** is the individual or entity offering these terms, and the **software** is the software the licensor makes available under these terms.

**You** refers to the individual or entity agreeing to these terms.

**Your company** is any legal entity, sole proprietorship, or other kind of organization that you work for, plus all organizations that have control over, are under the control of, or are under common control with that organization.  **Control** means ownership of substantially all the assets of an entity, or the power to direct its management and policies by vote, contract, or otherwise.  Control can be direct or indirect.

**Your licenses** are all the licenses granted to you for the software under these terms.

**Use** means anything you do with the software requiring one of your licenses.
```

**CC0 (only if explicitly requested):**
```
CC0 1.0 Universal

The person who associated a work with this deed has dedicated the work to the
public domain by waiving all of their rights to the work worldwide under
copyright law, including all related and neighboring rights, to the extent
allowed by law.

You can copy, modify, distribute and perform the work, even for commercial
purposes, all without asking permission.
```

**MIT (only if explicitly requested):**
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
├── LICENSE           (PolyForm Noncommercial)
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
GPL applies to software distributed as executable code. Applying it to prompt files creates legal ambiguity and discourages use. PolyForm Noncommercial is the default for these original skills; CC0 or MIT are alternatives only when explicitly requested.

**Creating .github/ but leaving PULL_REQUEST_TEMPLATE.md empty.**
An empty PR template is worse than no template; it signals an abandoned intention. Either write a minimal working template or skip the file.

**Putting all rule files in the root directory for a collection repo.**
Five rule files at root is manageable. Twenty is chaos. Use `skills/` or `rules/` subdirectories from the start.

**Not creating an assets/ directory.**
Even without banner images yet, create the `assets/` directory with placeholder files so the README's `<picture>` tag has a valid path.
