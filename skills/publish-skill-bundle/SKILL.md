---
name: publish-skill-bundle
description: "Use this skill when the user has a working AI rule or skill file and wants to take it from local draft to a published GitHub repository, end to end. This is the orchestrator that routes through the publishing pipeline sub-skills in order. Trigger when the user says 'I have a skill, help me publish it', 'turn my prompt into a GitHub repo', 'publish my Cursor rule', 'put this skill on GitHub end to end', 'walk me through publishing this', or 'I have a working SKILL.md and don't know what to do next'. Also trigger when the user has a single rule file in hand and says any phrase that implies the full publishing path. Do NOT trigger when the user only wants one step of the pipeline (call that sub-skill directly), or when the rule file does not exist yet (writing from scratch is out of scope), or when the repo is already live on GitHub and only needs a single follow-up action like submitting to a directory."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start

Ask the user for one thing: the path to their existing rule file. Then call the sub-skills below in order, letting each one finish before invoking the next.

```
polish-rule-content      →  cleaned SKILL.md / .cursorrules / AGENTS.md
write-readme             →  README.md
scaffold-repo-files      →  LICENSE, CONTRIBUTING.md, .github/
create-visual-assets     →  assets/banner.svg, banner-dark.svg, badges
translate-readme         →  README.zh-CN.md + language switcher (optional)
publish-to-github        →  live GitHub repo
submit-to-directories    →  awesome-list PRs (optional)
```

The "published" milestone is `publish-to-github`. Anything after that is promotion.

---

## polish-rule-content

Rewrites the user's existing file with a five-segment description, Quick Start section, Common Mistakes section, and the AI-fingerprint checklist applied.

A weak description here propagates into the README and the awesome-list entry, so finish this step before moving on.

---

## write-readme

Input: the polished rule file plus the repo name and one-line value statement. Output: `README.md` with banner placeholder, badge row, install commands, what-it-does section, content list, and footer.

The README's one-liner becomes the GitHub repo description later, and the awesome-list entry after that. Lock it here.

---

## scaffold-repo-files

Input: repo type (single-skill / collection / awesome-list) and the chosen license. Output: `LICENSE`, `CONTRIBUTING.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and the directory layout.

---

## create-visual-assets

Input: repo name and tagline from the README. Output: `assets/banner.svg`, `assets/banner-dark.svg`, the `<picture>` embed snippet, and the badge markdown row.

On its first run in a project this sub-skill asks one style question: whether the user has an image-style skill to load, wants to describe a style, or takes the default (white background, black text). The answer is saved to `assets/STYLE.md` and never asked again. Let it ask; do not answer on the user's behalf.

Drop the embed snippet and badge row into the README placeholders. After this step the README has no unfilled `{PLACEHOLDER}` tokens.

---

## translate-readme (optional)

Input: the finalized README.md and a target language. Output: `README.{lang}.md` plus the language switcher line in both files.

Runs after `create-visual-assets` so the translation captures the final README, and before `publish-to-github` so both language files land in the initial commit. Skip when the repo targets a single-language audience.

---

## publish-to-github

Input: a completed local folder with all files prepared above. Output: a live GitHub repo with topics set and metadata configured.

Run the pre-flight checklist before any git command. If anything is missing, return to the relevant earlier step.

---

## submit-to-directories (optional)

Input: the live repo URL. Output: PRs to one or more awesome-lists matching the rule format.

Submit to one directory first. Wait for the merge, then submit to the next.

---

## Hard gates

Two checks block `publish-to-github`. No inference lifts them; only an explicit user statement in the current conversation does.

1. **Banner gate.** `assets/banner.svg` and `assets/banner-dark.svg` exist and the README embeds them. The user not mentioning visuals is not an opt-out; run `create-visual-assets` with the default style. Only "I don't want a banner" said outright waives this.
2. **Placeholder gate.** Zero `{PLACEHOLDER}` tokens in README.md and any translated README.

If either gate fails, route back to the producing step before touching git.

---

## When to skip steps

- Rule file already clean → skip `polish-rule-content`
- User already wrote the README → skip `write-readme`
- Going to be a private gist, not a repo → skip `scaffold-repo-files`, `publish-to-github`, `submit-to-directories`
- User has no visual preference → `create-visual-assets` still runs, with the default style
- Repo targets a single-language audience → skip `translate-readme`
- User does not want awesome-list visibility → skip `submit-to-directories`

If the repo has additional steps beyond these (forked variant, custom pipeline), insert them in the order that matches the dependency: anything that produces a file consumed by `write-readme` runs before it; anything that needs the live repo URL runs after `publish-to-github`.

---

## Common Mistakes

**Treating this skill as a single rewrite pass.**
This skill is an orchestrator. It does not write any file itself; it routes to the sub-skills. If the agent starts editing the rule file directly instead of calling `polish-rule-content`, the user loses the per-step verification.

**Running `publish-to-github` before `create-visual-assets` finishes.**
A README with `{REPO_NAME}` placeholders pushed to GitHub looks unfinished. The visual assets and badge row have to be in place first so the README has no unfilled tokens.

**Translating before the README is final.**
`translate-readme` runs last among the content steps. A translation made from a draft has to be redone after every README edit.

**Calling several sub-skills in a single tool call.**
Each sub-skill has its own information-gathering step. Call them sequentially, let each one ask its own questions, and only move forward when its output is finalized.
