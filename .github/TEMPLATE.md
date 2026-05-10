# Using Claude Code Template

Welcome! This guide helps you get started with your new project.

## First Steps

### 1. Initialize Claude Code
```bash
./scripts/setup-claude-code.sh .
```

This script:
- Creates `.claude/` structure
- Installs git hooks
- Creates CLAUDE.local.md

### 2. Customize Your Project

Edit **CLAUDE.md** with your project info:
- Project name and description
- Tech stack
- Setup and run commands
- Architecture overview

### 3. (Optional) Local Customization

Edit **CLAUDE.local.md** (git-ignored) for your machine.

### 4. Commit and Push
```bash
git add .
git commit -m "Initialize Claude Code"
git push origin main
```

## What Runs Automatically

### Pre-commit Hook
Validates before each commit:
- Bash script formatting
- Python linting/typing
- Test coverage
- No secrets

### GitHub Actions
On every push:
- Validates `.claude/settings.json`
- Checks required files exist
- Ensures hooks are executable

## Rules and Conventions

See `.claude/rules/`:
- **code-style.md** — PEP 8, naming, type hints
- **testing.md** — Test patterns, fixtures
- **api-conventions.md** — REST API design

## Commands

See `.claude/commands/`:
- **review.md** — Code review workflow
- **fix-issue.md** — Bug diagnosis workflow

Use as `/review` and `/fix-issue` slash commands in Claude Code.

## Hooks

Git pre-commit hook validates:
- Bash formatting/linting
- Python type-checking
- Tests pass
- No secrets committed

Use `git commit --no-verify` to skip (use carefully).

## Troubleshooting

### "command not found"
Make script executable:
```bash
chmod +x scripts/setup-claude-code.sh
./scripts/setup-claude-code.sh .
```

### Pre-commit hook not running
```bash
ls -la .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Settings invalid
```bash
cat .claude/settings.json | python3 -m json.tool
```

## Questions?

See CLAUDE.md for project-specific documentation, or README.md for general info.
