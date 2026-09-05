# Rename: Welcome to AGI → Super Astra

The display name is **Super Astra**, the skill ID and directory are `super-astra`, and explicit Codex invocation is `$super-astra`. Earlier releases used `welcome-to-agi` and, before that, `astra-prompts`.

New installations use `skills/super-astra`. An existing installed copy continues to work under its old path until it is migrated; renaming the repository does not modify any user's machine or hook trust. The installer refuses to create a sibling copy beside a detected legacy installation.

For an authorized upgrade, the installing agent should:

1. Identify the actual installed directory, config, host scope and existing rule/hook targets. Preserve user-disabled modules and custom prompt/guard files. Read [onboarding.md](onboarding.md) for unresolved choices.
2. Back up the complete old skill and affected registrations outside skill discovery paths. Prepare the updated package and merge the user's customizations before changing its entrypoint.
3. Use the old installed initializer (or the new scoped removal command) to remove only the old registration. Move the old discoverable directory to its backup location, then install the prepared `super-astra` folder. Do not leave two active skill copies.
4. Initialize the selected mode with the new installed paths. Hook definitions now use `LabKit Super Astra v1`; previous `LabKit Welcome to AGI v1/v2` and `LabKit Astra Prompts v1` labels remain recognized for replacement/removal. A changed command/label requires reviewing the new definition in the actual host's supported trust UI. Do not copy trust records or bypass trust.
5. Verify the actual client after migration. If migration has not been requested, report the new repository name and leave the user's functioning old installation alone.

The internal `LABKIT_WELCOME_TO_AGI_RULE_V1` and `LABKIT_WELCOME_TO_AGI_ROUTER_V2` markers intentionally remain stable for compatibility and deduplication. They are protocol identifiers, not the public product name. Existing Cursor managed headers are recognized and updated on rule refresh; custom headers still require inspection. Official prompt bodies are unchanged.
