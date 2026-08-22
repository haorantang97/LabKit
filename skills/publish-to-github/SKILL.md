---
name: publish-to-github
description: "Use this skill when the user is ready to publish a complete AI skill or rule repository to GitHub. It covers git initialization, the first commit, creating the repository with gh or manual browser steps, setting the description and Topics, and confirming the push. It also covers browser-only or API-based publishing and repair of an existing repository. Do not trigger while files still need editing, or for submitting an already-published repository to awesome-lists."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start

If all files are ready and the user has `gh` installed:

```bash
git init && git add . && git commit -m "feat: initial release of {name}"
gh repo create {username}/{repo} --public --description "{tagline}" --source=. --push
```

Then set Topics on the repo page (Phase 3). Done.

If `gh` is not installed, follow the manual path in Phase 2. No usable git at all (sandboxed agent, browser-only session)? Use Phase 2b.

---

## Pre-flight checklist

Confirm all of these before running any git commands:

- [ ] `README.md` exists with no unfilled `{PLACEHOLDER}` tokens
- [ ] `LICENSE` file exists
- [ ] Rule file exists (SKILL.md / .cursorrules / .windsurfrules / AGENTS.md)
- [ ] **Banner gate**: `assets/banner.svg` and `assets/banner-dark.svg` exist AND the README embeds them
- [ ] `.gitignore` exists (see template below)
- [ ] Repo name is decided (kebab-case, no spaces)
- [ ] GitHub username is known

If anything is missing, stop and complete it first.

The banner gate is hard. The only thing that waives it is the user explicitly saying in the current conversation that they want no banner. A missing banner file, a skipped upstream step, or a README with no banner reference does NOT count as opting out; in those cases run create-visual-assets (default style takes under a minute), add the embed snippet to the README, then return here.

---

## .gitignore template

```
# OS
.DS_Store
Thumbs.db

# Editors
.vscode/
.idea/
*.swp

# Python (if repo has scripts)
__pycache__/
*.pyc
.venv/
.env

# Node (if repo has tools)
node_modules/
dist/
```

---

## Phase 1: Initialize and commit

```bash
cd {repo-name}
git init
git add .
git status       # review before committing
git commit -m "feat: initial release of {skill-name}

- {rule-file}: {one-line description}
- README: install instructions and usage
- LICENSE: PolyForm Noncommercial 1.0.0 (unless the user explicitly chose another license)"
```

Commit message rules:
- First line: `feat: initial release of {name}` (50 chars max)
- Body: bullet list of what's included
- NEVER use "Initial commit"

---

## Phase 2: Create the GitHub repository

### With `gh` CLI

```bash
gh repo create {github-username}/{repo-name} \
  --public \
  --description "{one-line description}" \
  --source=. \
  --push
```

### Manual (no `gh` CLI)

1. Go to https://github.com/new
2. Fill in: repo name, description, Public. Do NOT initialize with README or license.
3. Click "Create repository"
4. Run:

```bash
git remote add origin https://github.com/{github-username}/{repo-name}.git
git branch -M main
git push -u origin main
```

---

## Phase 2b: No-git fallback

Use this phase when the environment has no usable git at all — no CLI, no credentials, or a sandboxed agent (browser-only sessions, Claude Cowork and similar). Three paths, in order of preference.

### Path A — GitHub API with a fine-grained PAT (standard, atomic)

The programmatic equivalent of `git push`, and what `gh` does under the hood. One-time setup: create a fine-grained personal access token scoped to the target repo only, permission "Contents: Read and write" (add "Administration" if the repo must be created too). Store it in an environment variable or keychain. Never paste the token into a chat or agent conversation — agents should read it from the environment, not from the transcript.

Create the repo:

```bash
curl -s -X POST https://api.github.com/user/repos \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{"name":"{repo-name}","description":"{tagline}","auto_init":false}'
```

Then commit all files atomically with the Git Data API — blob → tree → commit → ref:

1. `POST /repos/{u}/{r}/git/blobs` for each file (base64 content)
2. `POST /repos/{u}/{r}/git/trees` listing every path with its blob sha
3. `POST /repos/{u}/{r}/git/commits` with the tree sha and the Phase 1 message format
4. `POST /repos/{u}/{r}/git/refs` pointing `refs/heads/main` at the new commit

Result: one clean initial commit, identical to the git path. Any HTTP client or octokit works.

### Path B — Browser drag-and-drop (human, zero tooling, atomic)

1. Create the repo at https://github.com/new — do NOT initialize with README
2. On the empty-repo page, click "uploading an existing file"
3. Drag the entire local folder into the drop zone — directory structure is preserved, and every file lands in a single commit
4. Replace the default commit message with the Phase 1 format before committing

Two minutes, no tools, clean history. Prefer this over the web file editor whenever a human is at the keyboard.

### Path C — Agent-driven web editor (last resort)

For agents that hold only a logged-in browser session: create each file via `github.com/{u}/{r}/new/main?filename={path}` and the web editor (the `filename` query parameter pre-fills the path and creates directories). Accept the cost — one commit per file, no atomicity. Three rules learned the hard way:

- Inject content as a single transaction (`document.execCommand('insertText')` after select-all), never keystroke-by-keystroke typing — the editor's markdown auto-indent silently corrupts lists and YAML front matter
- Set the commit message in the dialog via the native value setter plus a dispatched `input` event, or the framework ignores the change
- Verify through the contents API by comparing SHA-256 of the decoded content, not raw.githubusercontent.com — the raw CDN caches for ~5 minutes and will show a stale file

---

## Repair mode: the repo already exists

When fixing a repo that was published wrong or half-published, do not delete and recreate it — stars, clones, and inbound links break. Update in place:

- With a token: `PUT /repos/{u}/{r}/contents/{path}` per file, passing the current file's `sha` to overwrite
- Browser only: the web editor per file (Path C rules apply)
- History from the broken attempt cannot be rewritten from the browser; accept it, and make the fix commits tell a clear story with proper messages

---

## Phase 3: Configure GitHub metadata

Do this on the repo page immediately after pushing. Topics directly affect search ranking.

Click the gear icon next to "About" and add:

```
# Platform (pick what matches your rule file format)
cursor, cursorrules, cursor-ai         ← Cursor
windsurf, windsurf-ai, windsurfrules  ← Windsurf
claude, claude-code, claude-skills    ← Claude
agents-md, ai-agents                  ← AGENTS.md
github-copilot                        ← Copilot

# Always include
ai, llm, rules

# For collection repos
awesome, awesome-list

# Domain tags (add as applicable)
security, typescript, python, react...
```

Aim for 6–12 topics. Fewer than 5 hurts search visibility; more than 15 dilutes relevance.

---

## Phase 4: Verify

```bash
git log --oneline
gh repo view --web    # or open https://github.com/{username}/{repo-name}
```

Check:
- [ ] README renders correctly with no broken images
- [ ] Dark mode banner works (toggle GitHub theme in Settings)
- [ ] Topics are set
- [ ] Description is set

---

## Common Mistakes

**Using "Initial commit" as the commit message.**
The git log is visible on GitHub. "feat: initial release of {name}" takes 5 extra seconds and tells future visitors what was in the first commit.

**Initializing GitHub repo with a README.**
Checking "Add a README" on GitHub when you already have local content creates a diverged history. git will refuse to push. Always create an empty GitHub repo when local files are ready.

**Forgetting to set Topics before announcing the repo.**
Topics are the primary way GitHub search surfaces repos. A repo with no topics is invisible to most discovery paths. Set them immediately after pushing.

**Pushing to `master` instead of `main`.**
GitHub defaults new repos to `main`. If the local branch is `master`, run `git branch -M main` before pushing.

**Not reviewing `git status` before the first commit.**
A stray `git add .` can accidentally stage secrets, build artifacts, or system files. Always check `git status` output before committing.

**Publishing without a banner because an upstream step got skipped.**
"The README has no banner reference" is a symptom of a skipped step, not permission to publish without one. Silence from the user is not an opt-out. Generate the default banner and embed it, or get an explicit "no banner" from the user before pushing.

**Pasting an access token into a chat or agent conversation.**
Tokens belong in environment variables or a keychain. An agent that needs one should read `$GITHUB_TOKEN` from the environment; a token that has passed through a conversation transcript should be treated as leaked and revoked.

**Trusting raw.githubusercontent.com right after a commit.**
The raw CDN caches aggressively (~5 minutes). Verify pushes through the contents API or the repo page, or you will "confirm" a stale version.
