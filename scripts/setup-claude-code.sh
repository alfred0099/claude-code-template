#!/bin/bash
# Setup script for Claude Code configuration

set -e

PROJECT_ROOT="${1:-.}"
FORCE_OVERWRITE=0

if [ "$2" == "--force" ]; then
  FORCE_OVERWRITE=1
fi

echo "🚀 Setting up Claude Code in $PROJECT_ROOT"

# Create .claude directory structure
mkdir -p "$PROJECT_ROOT/.claude/rules"
mkdir -p "$PROJECT_ROOT/.claude/commands"
mkdir -p "$PROJECT_ROOT/.claude/hooks"
mkdir -p "$PROJECT_ROOT/scripts"

echo "✓ Created .claude directory structure"

# Create CLAUDE.local.md
if [ ! -f "$PROJECT_ROOT/CLAUDE.local.md" ] || [ "$FORCE_OVERWRITE" -eq 1 ]; then
  cat > "$PROJECT_ROOT/CLAUDE.local.md" << 'LOCALEOF'
# Local Configuration

Local machine-specific overrides (git-ignored).

## Model Overrides

```json
{
  "models": {
    "default": "claude-opus-4-6"
  }
}
```

## Tool Settings

- Adjust context limits
- Set local paths
- Configure credentials
LOCALEOF
  echo "✓ Created CLAUDE.local.md"
fi

# Install git pre-commit hook
if [ -d "$PROJECT_ROOT/.git/hooks" ]; then
  if [ -f "$PROJECT_ROOT/.claude/hooks/validate-bash.sh" ]; then
    cp "$PROJECT_ROOT/.claude/hooks/validate-bash.sh" "$PROJECT_ROOT/.git/hooks/pre-commit"
    chmod +x "$PROJECT_ROOT/.git/hooks/pre-commit"
    echo "✓ Installed git pre-commit hook"
  fi
fi

echo ""
echo "✅ Setup complete!"
echo "Next: Edit CLAUDE.md with your project info"
