#!/usr/bin/env bash
# One-shot publisher for the `SKILL-SKILL` repo.
# Run: ./setup.sh

set -euo pipefail

REPO_NAME="SKILL-SKILL"
REPO_DESC="From local draft to a published GitHub repo, in six atomic skills. Platform-agnostic."

cd "$(dirname "$0")"

# --- 1. Preflight ---
echo "→ Checking prerequisites..."

if ! command -v git >/dev/null 2>&1; then
  echo "✗ git is not installed. Install it first: brew install git"
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "✗ gh CLI is not installed. Install it: brew install gh"
  echo "  Then: gh auth login"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "✗ gh CLI is not logged in. Run: gh auth login"
  exit 1
fi

GH_USER=$(gh api user --jq .login)
if [ -z "$GH_USER" ]; then
  echo "✗ Could not detect GitHub username from gh CLI."
  exit 1
fi

echo "✓ git, gh, and auth OK. Username: $GH_USER"

# --- 2. Fill placeholders ---
echo "→ Filling {YOUR_GH_USERNAME} placeholders..."

if grep -l '{YOUR_GH_USERNAME}' README.md README.zh-CN.md >/dev/null 2>&1; then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/{YOUR_GH_USERNAME}/$GH_USER/g" README.md README.zh-CN.md
  else
    sed -i "s/{YOUR_GH_USERNAME}/$GH_USER/g" README.md README.zh-CN.md
  fi
  echo "✓ Placeholders filled with $GH_USER"
else
  echo "✓ No placeholders to fill (already done)"
fi

if grep -rn --exclude=setup.sh --exclude-dir=.git '{YOUR_GH_USERNAME}' . >/dev/null 2>&1; then
  echo "✗ Some placeholders are still present. Aborting."
  grep -rn --exclude=setup.sh --exclude-dir=.git '{YOUR_GH_USERNAME}' .
  exit 1
fi

# --- 3. Git init + first commit ---
if [ ! -d .git ]; then
  echo "→ Initializing git repo..."
  git init -q
  git branch -M main
fi

if [ -z "$(git log --oneline 2>/dev/null)" ]; then
  echo "→ Creating initial commit..."
  git add .
  git commit -q -m "feat: initial release of SKILL SKILL

- 6 atomic skills covering the publish-to-GitHub pipeline
- 1 orchestrator skill (publish-skill-bundle)
- README, CONTRIBUTING, PolyForm Noncommercial LICENSE, banner SVGs
- Platform-agnostic SKILL.md format (Claude Code, Cursor, Windsurf, Copilot, AGENTS.md)
- Bilingual docs (English / 中文)"
  echo "✓ Initial commit created"
else
  echo "✓ Repo already has commits, skipping initial commit"
fi

# --- 4. Create GitHub repo ---
if gh repo view "$GH_USER/$REPO_NAME" >/dev/null 2>&1; then
  echo "⚠ Repo $GH_USER/$REPO_NAME already exists on GitHub."
  read -p "  Push to it anyway? (y/N) " yn
  if [[ "$yn" =~ ^[Yy]$ ]]; then
    if ! git remote get-url origin >/dev/null 2>&1; then
      git remote add origin "https://github.com/$GH_USER/$REPO_NAME.git"
    fi
    git push -u origin main
  else
    echo "Stopped. Rename the repo or delete the existing one and re-run."
    exit 1
  fi
else
  echo "→ Creating GitHub repo $GH_USER/$REPO_NAME..."
  gh repo create "$GH_USER/$REPO_NAME" \
    --public \
    --description "$REPO_DESC" \
    --source=. \
    --push
  echo "✓ Repo created and pushed"
fi

# --- 5. Set topics ---
echo "→ Setting topics..."
gh repo edit "$GH_USER/$REPO_NAME" \
  --add-topic ai \
  --add-topic llm \
  --add-topic skills \
  --add-topic ai-agents \
  --add-topic publishing \
  --add-topic prompt-engineering \
  --add-topic claude \
  --add-topic claude-code \
  --add-topic cursor \
  --add-topic cursorrules \
  --add-topic agents-md \
  --add-topic github-copilot
echo "✓ Topics set"

# --- 6. Open in browser ---
echo ""
echo "🎉 Done. Opening the repo page..."
gh repo view --web "$GH_USER/$REPO_NAME"

echo ""
echo "Check the rendered page:"
echo "  - README renders, banner shows"
echo "  - Toggle GitHub theme to verify dark-mode banner"
echo "  - English / 中文 language switcher works"
echo "  - Topics are set"
echo "  - LICENSE shows as PolyForm-Noncommercial-1.0.0 in the sidebar"
