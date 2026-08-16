---
name: translate-readme
description: "Use this skill when the user wants a bilingual or multilingual README for their AI skill or rule repository. This includes translating README.md into a second language as a separate file (README.zh-CN.md, README.ja.md), adding the language switcher line to the top of both files, and keeping the two versions in sync after edits. Trigger when the user says 'add a Chinese README', 'make my repo bilingual', 'translate the README', 'add 中文 docs', 'I want English and Chinese versions', or 'add a language toggle'. Also trigger when the repo targets a bilingual audience and the README exists in only one language. Do NOT trigger for translating the rule file or SKILL.md content itself (rule files stay in one language so agent behavior is predictable), or for writing the original README from scratch (that is write-readme), or when no README exists yet."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start

Two inputs: the finished README.md and the target language. Then:

1. Create `README.{lang-code}.md` with the full translation
2. Add the same language switcher line to the top of both files
3. Report which sections were NOT translated and why (see the do-not-translate list)

Translate only after README.md is final. A translation of a draft goes stale on the first edit.

---

## Phase 1: Pick the file name and switcher

File naming, by convention on GitHub:

| Language | File name |
|---|---|
| Simplified Chinese | `README.zh-CN.md` |
| Traditional Chinese | `README.zh-TW.md` |
| Japanese | `README.ja.md` |
| Spanish | `README.es.md` |
| Other | `README.{BCP-47 code}.md` |

Language switcher, placed on the first content line of BOTH files, directly under the banner embed if one exists:

```markdown
**English** | [中文](README.zh-CN.md)
```

And in the translated file, invert the bold:

```markdown
[English](README.md) | **中文**
```

The current language is bold plain text, never a self-link. A self-link that reloads the same page reads as a bug.

---

## Phase 2: Translate

Work section by section in the original order. Do not reorder, merge, or drop sections.

**Do-not-translate list.** These stay in the source language, always:

- Code blocks and inline code (commands, file paths, flags)
- File names, directory names, repo names, skill names
- Badge URLs and image paths
- YAML front matter examples
- Proper nouns: GitHub, Cursor, Windsurf, Copilot, product names
- Link URLs (translate the link text, keep the target)

**Translation rules:**

- Translate meaning, not word order. A README that reads like machine output costs more trust than an English-only README
- Keep technical register consistent: pick one term per concept and reuse it (repo = 仓库 everywhere, not 仓库/存储库 mixed)
- Headings translate, but anchors then change. Rewrite any in-page `#anchor` links to match the translated headings
- Numbers, dates, and version strings stay identical to the original

---

## Phase 3: Verify sync

Before delivering, check:

- [ ] Both files have the switcher line, correct bold, correct link target
- [ ] Section count matches between the two files
- [ ] All code blocks are byte-identical between the two files
- [ ] No `{PLACEHOLDER}` tokens in either file
- [ ] In-page anchor links work in the translated file

---

## Phase 4: Keep in sync after edits

Whenever README.md changes later, the translated file must change in the same commit. Add this line to CONTRIBUTING.md if the repo accepts PRs:

```markdown
If your PR edits README.md, apply the same change to README.zh-CN.md in the same PR.
```

A translation more than one release behind the original is worse than no translation. If the user stops maintaining the second language, delete the file and the switcher rather than leaving it stale.

---

## Common Mistakes

**Translating the rule file or SKILL.md itself.**
The rule content is instructions to an agent. Two language versions of the same instructions drift apart, and the agent may load the stale one. Keep rule files in one language; translate only human-facing docs.

**Adding the switcher to only one file.**
A reader landing on README.zh-CN.md from a search result has no path back to English without the switcher in that file too. Both files get the line.

**Translating code blocks and commands.**
`git clone` translated into any other language breaks copy-paste. Everything in the do-not-translate list stays verbatim.

**Leaving in-page anchors pointing at English headings.**
GitHub generates anchors from heading text. After headings are translated, `#install` no longer exists in the translated file. Rewrite every in-page link.

**Creating the translation before the README is final.**
Every later edit to README.md now has to be made twice. Run this skill last among the content steps, right before publish-to-github.
