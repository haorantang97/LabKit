# Packaging and publishing

Use for repository packaging, renovation or publication. A local skill edit remains local unless publication is requested. Existing user choices and authorization persist.

Read [the repository presentation standard](repository-presentation.md) first. It defines the user's default level of finish, based on the Personal-Ontology benchmark. Inspect the current repository and chosen reference before generating files.

## Installation boundary

Identify the exact directory or artifact the host installs before arranging repository files. A folder-installed skill contains its instructions, host metadata, resources needed by its workflow, and required license notices. Keep repository introductions, cover images, social cards and their design or generation records outside that directory. Classify resources by their use: templates, images or prompts needed to perform the skill's work belong in the package.

For a skill repository with presentation files, use a self-contained `skills/<name>/` installation directory by default; keep repository presentation at the repository level. Preserve other hosts' required rule-file locations. An existing layout may use a separate build artifact or an installer with verified exclusions; do not assume an installer filters out unreferenced files. Documentation must name the actual installation unit, include its dependencies and describe an update method supported by that installation.

For plugins, inspect the marketplace source, plugin manifest, build configuration and installer to determine which files are copied. Keep required manifests, UI icons, runtime code, bundled skills and their dependencies inside that installation unit. Put repository-only artwork, production records and development files outside it, or exclude them through a packaging mechanism verified against the actual artifact. Preserve resource paths and plugin identity when changing the layout.

When creating or changing the package layout or installation method, verify the local installation unit and its dependencies before publication. Exercise installation in a temporary destination and inspect the resulting file inventory, including hidden files, for missing dependencies and unrelated repository material. If the documented remote command depends on unpublished content, use an equivalent local installation for this preflight, then run the documented command against the published version after publication. Distinguish local package checks from remote installation verification. Report an unavailable check precisely; format validation alone does not verify package contents.

## Packaging workflow

Choose the producing modules relative to the skill root:

| Work needed | Module |
| --- | --- |
| Revise skill instructions | modules/polish-rule-content/SKILL.md |
| Build the introduction and catalogue | modules/write-readme/SKILL.md |
| Prepare license and contribution files | modules/scaffold-repo-files/SKILL.md |
| Create the repository identity and assets | modules/create-visual-assets/SKILL.md |
| Complete an additional language edition | modules/translate-readme/SKILL.md |
| Publish or repair the live repository | modules/publish-to-github/SKILL.md |
| Requested community-directory submission | modules/submit-to-directories/SKILL.md |

Do the steps the task needs. Resolve shared facts once; do not repeat style, name or authorization questions already answered. For a renovation, preserve working code, component boundaries, licenses and existing setup behavior. Synchronize root and component documentation only where changed claims require it.

Before publication, the page needs its own correctly branded hero and appropriate theme variants, complete text with no unfinished template tokens, coherent public entries, valid links, synchronized supported language editions, and truthful status. Render the assets and assembled README; file existence is insufficient. The user's explicit omission or narrower scope takes precedence.

PolyForm Noncommercial remains the user's default for new original repositories. Preserve existing and third-party licenses. Do not generate release badges, CI claims, topics or documentation that imply unsupported capabilities.

Review the diff and current remote branch before committing. Follow the target repository's contribution workflow and the user's actual external-action scope. For an existing repository, update it in place without rewriting its history or losing stars. A social-preview file is not an uploaded social preview; a branch push is not a default-branch update.

Finish with the real resulting state, meaningful checks, live links when published and precise remaining limitations. Promotion is a separate step and runs only when requested.
