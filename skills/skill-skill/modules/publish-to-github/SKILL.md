---
name: publish-to-github
description: "Use this skill when the user is ready to push their local AI skill or rule repository to GitHub for the first time. This includes running git init and the initial commit, creating the GitHub repository via the gh CLI or manual browser steps, setting the repository description and Topics tags, and confirming the push succeeded. Trigger when the user says 'upload to GitHub', 'push this to GitHub', 'create my repo on GitHub', 'how do I publish this', 'make this live', or 'I have all the files ready, now what'. Also trigger when the user has a complete local folder with all files and just needs the final publishing step. Also covers environments with no usable git at all — sandboxed agents, browser-only sessions — via the GitHub API with a fine-grained PAT, browser drag-and-drop upload, agent-driven web editor commits, and a repair mode for repos that already exist. Do NOT trigger if any files still need to be written or edited before publishing — all content must be finalized first. Do NOT trigger for submitting the repo to awesome-lists after publishing (that is submit-to-directories)."
license: PolyForm-Noncommercial-1.0.0
---

## Quick Start

If all files are ready and the user has `gh` installed:

```bash
git init && git add . && git commit -m "feat: initial release of {name}"
gh repo create {username}/{repo} --public --description "{tagline}" --source=. --push
```

First complete the presentation pre-flight below and follow the repository workflow. After publication, set relevant metadata and verify the live page; a successful push alone is not completion.

If `gh` is not installed, follow the manual path in Phase 2. No usable git at all (sandboxed agent, browser-only session)? Use Phase 2b.

---

## Pre-flight checklist

Read [the repository presentation standard](../../references/repository-presentation.md). Before publication, confirm its acceptance checks and the following:

- [ ] `README.md` exists with no unfilled `{PLACEHOLDER}` tokens
- [ ] `LICENSE` file exists
- [ ] Rule file exists (SKILL.md / .cursorrules / .windsurfrules / AGENTS.md)
- [ ] **Identity and visual gate**: the hero names the repository (not a child skill), appropriate light/dark assets render correctly, and the assembled README has been visually inspected
- [ ] `.gitignore` exists (see template below)
- [ ] Repository identity is decided; preserve the existing name and remote
- [ ] GitHub username is known

If anything is missing, stop and complete it first.

Read image text, check stale branding and real catalogue counts, validate navigation and both language editions, and keep badge claims within actual evidence. Apply user-specified omissions and scope. A supplied reference already answers the style question. Repair missing assets through create-visual-assets; do not substitute a generic text template for the requested standard.

For an existing repository, inspect its current branch, pending changes and contribution rules. Publish only the authorized change. Prefer an ordinary commit or the required PR flow; do not initialize another repository, rename branches or rewrite history as part of decoration.

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

Verify the About description and select topics that reflect actual capability and supported hosts. Preserve existing relevant metadata. Do not add awesome/awesome-list solely because this is a collection, or claim an arbitrary number of topics improves ranking. If a social card is in scope, use the generated image and confirm the setting separately from the asset's existence.

---

## Phase 4: Verify

```bash
git log --oneline
gh repo view --web    # or open https://github.com/{username}/{repo-name}
```

Check:
- [ ] Default-branch content matches the intended change, not merely a pushed feature branch
- [ ] README renders correctly with no broken images, stale image text, clipping or incorrect catalogue entries
- [ ] Both theme assets work; inspect using a scoped preview or browser theme emulation without changing the user's global preference
- [ ] Topics are set
- [ ] Description is set

---

## Common Mistakes

**Using "Initial commit" as the commit message.**
The git log is visible on GitHub. "feat: initial release of {name}" takes 5 extra seconds and tells future visitors what was in the first commit.

**Initializing GitHub repo with a README.**
Checking "Add a README" on GitHub when you already have local content creates a diverged history. git will refuse to push. Always create an empty GitHub repo when local files are ready.

**Forgetting to set Topics before announcing the repo.**
Topics help readers understand the repository. Verify relevance and the About description without adding unsupported ranking claims.

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
