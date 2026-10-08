#!/usr/bin/env bash
# Pull template-owned files (listed in .claude/template-manifest.txt) into this project.
# Leaves changes unstaged so you can review them with `git diff` before committing.
set -eu
repo="${TEMPLATE_REPO:-https://github.com/alfred0099/claude-code-template}"
ref="${1:-main}"
root=$(git rev-parse --show-toplevel)
cd "$root"
git fetch --depth 1 "$repo" "$ref"
manifest=$(git show FETCH_HEAD:.claude/template-manifest.txt)
echo "$manifest" | grep -vE '^\s*(#|$)' | while read -r path; do
  if git cat-file -e "FETCH_HEAD:$path" 2>/dev/null; then
    git checkout FETCH_HEAD -- "$path"
    git restore --staged -- "$path"
    echo "synced  $path"
  else
    echo "missing in template: $path"
  fi
done
git status --short
