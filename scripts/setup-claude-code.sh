#!/usr/bin/env bash
# One-time setup per clone. Safe to re-run.
set -eu
root=$(git rev-parse --show-toplevel)
cd "$root"

git config core.hooksPath scripts/git-hooks
echo "git hooks: core.hooksPath -> scripts/git-hooks"

if [ ! -f CLAUDE.local.md ]; then
  printf '# Local notes (git-ignored)\n\nMachine-specific paths and personal preferences for this project.\n' > CLAUDE.local.md
  echo "created CLAUDE.local.md"
fi

missing=""
for tool in python3 gh shellcheck; do
  command -v "$tool" >/dev/null 2>&1 || missing="$missing $tool"
done
if [ -n "$missing" ]; then
  echo "not installed:$missing"
  echo "  python3 is required for the Claude Code guard hooks; without it they fail open."
  echo "  gh is used by /review and /fix-issue. shellcheck is optional."
fi
echo "done"
