---
name: skill-skill
description: "Create, revise, validate, package, or publish AI skills and rule files. Use as the main entry for the user's skill-authoring workflow, including creating a new SKILL.md, improving an existing rule, and preparing a skill repository. Choose only the requested stage; ordinary product code or content work is outside this skill."
license: PolyForm-Noncommercial-1.0.0
---

# Skill authoring and publishing

Use this as the main workflow for the user's own skills. Keep the requested result, existing decisions and current authorization in view. Select the relevant mode; do not run the entire publishing pipeline for local creation, edits, reviews or installation.

| Request | Read and do |
|---|---|
| Create a new skill | Read [authoring guidance](references/authoring.md). Define the capability and create only useful instructions and resources. |
| Revise an existing skill or rule | Read [polish-rule-content](modules/polish-rule-content/SKILL.md). Preserve working behavior; change only what the request or evidence supports. |
| Review or propose a plan | Inspect and explain the relevant differences. Keep installed files unchanged unless editing was also requested. |
| Validate or install a skill | Read [authoring guidance](references/authoring.md). Use current available official validation or installation tools; separately verify installation and host activation. |
| Package, renovate or publish a repository | Read [publishing workflow](references/publishing.md) and [repository presentation standard](references/repository-presentation.md); load producing modules only when needed. |
| One packaging step | Read the matching module below and complete that step. Do not automatically continue to publishing or promotion. |

For creation and revision, apply the maintained authoring guidance directly. Official Codex skill-creator supplies host-specific structure, metadata conventions, initialization and validation tools when available. Read its current relevant instructions before relying on those tools. Keep the official skill installed; do not duplicate or freeze its scripts inside this bundle. This division does not change the host instruction hierarchy.

Use a supplied path or infer it from the task. Ask only when missing information materially affects the result. An authorized narrow edit does not require a second generic rewrite confirmation. A request for a plan or diagnosis remains a plan or diagnosis.

The packaging modules are shared implementation resources, resolved relative to this skill directory:

- [Polish skill content](modules/polish-rule-content/SKILL.md)
- [Write a README](modules/write-readme/SKILL.md)
- [Prepare repository files](modules/scaffold-repo-files/SKILL.md)
- [Create visual assets](modules/create-visual-assets/SKILL.md)
- [Translate a README](modules/translate-readme/SKILL.md)
- [Publish to GitHub](modules/publish-to-github/SKILL.md)
- [Submit to directories](modules/submit-to-directories/SKILL.md)

Preserve the user's existing publishing conventions: PolyForm Noncommercial is the default for their new original repositories; preserve existing and third-party licenses. The publication workflow checks repository identity, rendered visuals, catalogue accuracy, complete language editions and truthful validation status; banner existence and placeholder scans alone do not establish completion. These apply to publication, not to creating or testing a local skill. User-specified exceptions and existing authorization remain valid.

Do not create a GitHub repository, push, send messages or submit directory PRs solely because a local skill is ready. Complete authorized local preparation and follow the actual request's external-action scope.

Finish with the resulting files, meaningful checks performed and any remaining runtime verification. File validation, installation, host discovery, Hook trust and observed activation are separate results.
