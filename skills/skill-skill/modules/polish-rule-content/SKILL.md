---
name: polish-rule-content
description: "Use this skill when the user has an existing AI rule or skill file that works but needs quality improvement before publishing. This includes rewriting the description/trigger field using the five-segment method, restructuring content into Quick Start + core sections + Common Mistakes, removing AI-sounding language, adding quantified constraints, and ensuring the file follows progressive disclosure architecture. Trigger when the user says things like 'clean up my skill', 'improve this rule file', 'polish my SKILL.md', 'make this publishable', 'my description is bad', or 'prepare this for GitHub'. Also trigger when the user shows you a rule file and asks what's wrong with it. Do NOT trigger for creating a rule file from scratch with no existing content, or for changes to files other than the rule file itself (README, CONTRIBUTING, etc.)."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start

User pastes a file and says "improve this." Run these three steps before touching anything:

1. Check the `description` field against the five-segment template in Phase 2
2. Check the body for a Quick Start section and a Common Mistakes section
3. Report what's missing — confirm before rewriting

If the user only says "make it better" with no other context, start with the description field. It has the highest return per edit.

---

## Phase 1: Assess

Read the file and check each item:

- [ ] Does it have a description/trigger field? Is it specific enough to avoid false positives?
- [ ] Does the content have a Quick Start section?
- [ ] Is there a Common Mistakes section?
- [ ] Are constraints quantified ("≤ 50 lines") or vague ("keep it short")?
- [ ] Does the language read like a human expert, or like a documentation bot?
- [ ] For SKILL.md: does the `description` field have negative samples (Do NOT trigger for...)?
- [ ] Is the total length over 500 lines?

Tell the user what you found before rewriting anything.

---

## Phase 2: Rewrite the description / trigger field

For **SKILL.md** — use the five-segment method:

```
[1] MAIN TRIGGER
"Use this skill when the user wants to [primary action]."

[2] POSITIVE ENUMERATION
"This includes [A], [B], [C], and [D]."

[3] COLLOQUIAL TRIGGERS
"Trigger even if the user phrases it casually — things like '[informal phrase]' or '[informal phrase 2]'."

[4] EDGE CASE EXPANSION
"Also trigger when [adjacent scenario that is still in scope]."

[5] NEGATIVE SAMPLES
"Do NOT trigger for [out-of-scope A], [out-of-scope B], or [out-of-scope C], even if [related keyword] appears."
```

Target length: 80–200 words. Under 80 is usually under-specified; over 250 hurts retrieval.

For **.mdc** (Cursor/Windsurf) — write the `description` as a value pitch, not a file label:

```yaml
# Bad — no information value
description: "Cursor rules for TypeScript development."

# Good — states what specific problems this prevents
description: "Blocks the 5 most common Next.js 15 auth bugs: getSession misuse, missing RLS, synchronous params, deprecated imports, and Stripe key exposure."
```

For **AGENTS.md / copilot-instructions.md** — no description field; the filename is the trigger. Focus the rewrite on content quality only.

---

## Phase 3: Restructure the content body

Target structure for SKILL.md and AGENTS.md:

```
## Quick Start
[1–2 code blocks covering the most common 80% of use cases.
A reader should be able to use the skill without reading further.]

## [Core Section A]
[Technical detail, examples, constraints.]

## [Core Section B]

## Common Mistakes
- NEVER [anti-pattern] — [one-line reason]
- Do not [anti-pattern]; use [correct approach] instead.

## Quick Reference  (optional, for lookup-heavy skills)
| Scenario | Approach | Notes |
```

For **.mdc** rules — if the rule exceeds 120 lines, split it. Rules covering multiple independent concerns should be separate `.mdc` files.

---

## Phase 4: Apply the de-AI checklist

Work through each item. Fix every one that fails.

**Language**
- [ ] No "Leverage", "Utilize", "Streamline", "Facilitate", "Ensure", "Comprehensive"
- [ ] No em dash (—) in running prose; use a period, semicolon, or comma
- [ ] No "Here are the key points:" or "Here's what you need to know:"
- [ ] No "It's not X, it's Y" rhetorical framing
- [ ] No vague quality claims without criteria ("high-quality output", "best practices")

**Constraints**
- [ ] At least one constraint expressed as a number ("≤ 50 lines", "at least 3 test cases", "within 500ms")
- [ ] At least one named anti-pattern with a concrete reason (not just "avoid bad code")
- [ ] If the rule targets a framework or library: at least one version-specific note (e.g., "v5 breaking change")

**Structure**
- [ ] Quick Start section exists and is first
- [ ] Common Mistakes section exists with ≥ 2 named items
- [ ] For SKILL.md: `description` field has negative samples
- [ ] For .mdc: `globs` field is specific to the relevant file types, not `**/*`
- [ ] Total body length ≤ 500 lines; if over, content after line 500 moves to `references/`

**The final test:** Read it aloud. Would a senior engineer in this domain write this, or does it sound like a documentation generator? If the latter, keep editing.

---

## Common Mistakes

**Treating the description as a file label.**
The description is read by an AI to decide whether to invoke this skill. "A skill for PDF processing" tells it nothing useful. "Use this skill whenever the user mentions a .pdf file or wants to produce one" gives it a decision rule.

**Leaving all constraints vague.**
"Keep functions small" is unenforceable. "Functions must not exceed 40 lines; extract if longer" is a rule the AI can apply.

**Adding a Common Mistakes section with only one item.**
One item looks like an afterthought. Two or more items signals that the author knows where this skill goes wrong in practice.

**Making the Quick Start too generic.**
The Quick Start should show the single most common use case with runnable code or a concrete example, not a list of five things the skill can do.

**Splitting into references/ prematurely.**
Only move content to `references/` if the main file genuinely exceeds 500 lines. Premature splitting makes the skill harder to read.
