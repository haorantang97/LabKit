# Authoring and validation

This guide adapts the local official Codex skill-creator guidance into skill-skill's workflow. It adds creation and validation to the existing publishing capability. It is maintained guidance, not a verbatim official manual or a higher-priority instruction source.

Read this for creating a skill, changing its behavior or structure, validating it, or selecting an official helper. Packaging-only work may use the existing modules directly.

## Start with the capability

Define what a successful invocation produces and which requests need the skill. Use examples from the task or observed failures. Ask for more only when the missing distinction would materially change the design.

Assume the model is already capable. Add instructions that change decisions or improve reliability. Preserve scope, chosen artifacts and version; do not convert a local edit into a publication, review pipeline or broad configuration audit.

Keep discovery concise and specific. Required frontmatter is name and description; preserve supported existing metadata. Use a lowercase letters/digits/hyphens name under 64 characters. Other rule formats retain their own host requirements rather than receiving SKILL frontmatter indiscriminately.

## Choose resources by need

- Keep shared purpose, real constraints and useful routing in SKILL.md.
- Use references for substantial detail relevant only to particular modes, and link them at the point of use.
- Use scripts for repeated or fragile deterministic operations; verify changed scripts by running them safely.
- Use assets for files that belong in the generated output.
- Do not create empty resource directories, placeholder examples, a README, a changelog or an extra router without a task reason. Publishing a repository can provide that reason; a small local skill often does not.

There is no universal minimum description length, mandatory five-part trigger, numeric constraint quota, fixed test count or minimum size before moving detail into references. Choose specificity and structure for the actual risk and workflow.

## Official tools remain the host-specific reference

In Codex, resolve the current official skill-creator from the live skill catalog. A standard location is the active CODEX_HOME's skills/.system/skill-creator directory. Read its relevant SKILL.md and helper usage before relying on current flags or supported metadata. On other hosts or when absent, use that host's documented format and state which checks were unavailable.

Typical official helpers, run only when appropriate:

```text
python3 <official-skill-creator>/scripts/init_skill.py <name> --path <destination>
python3 <official-skill-creator>/scripts/quick_validate.py <skill-folder>
```

Use the initializer for a new skill when it helps; do not reinitialize an existing skill. Request only resource folders the task needs. For agents/openai.yaml, read the current official metadata reference. A generator can replace the whole YAML file: preserve policy, dependencies and unrelated fields when editing existing metadata. Preserve automatic discovery unless the user requested a different invocation policy.

For installation, use the current official skill-installer when applicable. Install the intended version, preserve customizations and verify files reached the correct runtime. Registration is not evidence of host loading, Hook trust or actual delivery.

Keep official system skills and helper scripts intact and updateable. Do not ship copies of host scripts or assume this machine's absolute paths are portable. If official guidance changes, compare the relevant change with this guide before applying it; user conventions and host constraints still govern the task.

## Validate behavior that matters

Run the official validator when available. Structural checks do not establish that the skill makes good decisions. Inspect discovery scope, reference reachability, permission boundaries and the actual change.

For a substantial revision, use realistic cases from the capability. Include a narrow task that should stay narrow and an out-of-scope request when misrouting is a concern. Use independent evaluation only when complexity or risk justifies it and host and user permit delegation. Do not turn every small edit into a mandatory evaluation pipeline.

Testing a local authoring workflow must not publish a repository, send a message, delete user data or grant Hook trust. Those steps require corresponding task authorization. Distinguish structural validation, a reasoned walkthrough, an executed example and actual client behavior in the receipt.

## Source and maintenance

Adapted on 2026-09-05 from the installed official skill-creator/SKILL.md, its references/openai_yaml.md and the official skill-installer instructions. Source hashes are in official-source-snapshot.json; they identify the guidance read for this integration and are not permanent pins or evidence of future currency.

The user's packaging conventions remain in publishing.md. Official guidance informs creation, scope, progressive disclosure and validation; it does not silently erase explicit publishing choices.
