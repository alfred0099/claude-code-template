# Claude Code Template Repository

A GitHub template repository for scaffolding new projects with consistent Claude Code configuration across all devices and team members.

## Quick Start

### For New Projects

1. Go to https://github.com/alfred0099/claude-code-template
2. Click the green "Use this template" button
3. Name your repository and create it
4. Clone the generated repository:
   ```bash
   git clone https://github.com/your-username/your-new-project
   cd your-new-project
   ```
5. Run the setup script:
   ```bash
   ./scripts/setup-claude-code.sh .
   ```
6. Edit `CLAUDE.md` and `CLAUDE.local.md` for project-specific customization

## Directory Structure

```
.claude/
├── settings.json              # Tool permissions and LLM model selection
├── rules/                     # Code style, testing, API design guidelines
│   ├── code-style.md
│   ├── testing.md
│   └── api-conventions.md
├── commands/                  # Reusable workflow commands
│   ├── review.md
│   └── fix-issue.md
└── hooks/                     # Git hooks for validation
    └── validate-bash.sh       # Pre-commit hook

scripts/
└── setup-claude-code.sh       # Initialization script

CLAUDE.md                      # Project documentation (edit per-project)
CLAUDE.local.md                # Local overrides (git-ignored)
README.md                      # This file

.gitignore
.gitattributes
.github/
├── TEMPLATE.md               # Guide for users creating repos from template
└── workflows/
    └── validate-claude-config.yml  # GitHub Actions validation
```

## What's Included

- **settings.json** — Centralized tool permissions and LLM model assignment
- **rules/** — Code style (PEP 8), testing patterns, API design conventions
- **commands/** — Reusable code review and bug-fix workflows
- **hooks/** — Pre-commit validation (formatting, linting, type checking, tests)
- **setup-claude-code.sh** — Automated initialization with fallbacks
- **CLAUDE.md template** — Project documentation starter
- **.gitignore** — Ignores local overrides and IDE files
- **GitHub Actions workflow** — Validates Claude Code structure on push

## Customization

After running `./scripts/setup-claude-code.sh .`:

1. **Edit CLAUDE.md** with your project-specific information:
   - Project overview and status
   - Tech stack
   - Commands (setup, run, test, lint)
   - Architecture diagram
   - Common workflows

2. **Edit CLAUDE.local.md** (git-ignored) for local overrides:
   - Local tool configuration
   - Personal preferences
   - Machine-specific paths

3. **Update .claude/rules/** if your project has different conventions

4. **Add commands** in .claude/commands/ for project-specific workflows

## Features

- **Single source of truth**: All Claude Code standards in one place
- **One-click setup**: `./scripts/setup-claude-code.sh .` configures everything
- **Automatic consistency**: Every project created from this template inherits standards
- **Git-ignored locals**: CLAUDE.local.md and settings.local.json not committed
- **Pre-commit validation**: Bash formatting, linting, type checking, tests run automatically
- **CI/CD ready**: GitHub Actions validates structure on every push

## Updates

When you improve `.claude/` standards in any project:

1. Update the template repository (https://github.com/alfred0099/claude-code-template)
2. All future projects created from the template inherit the improvements
3. Existing projects can cherry-pick updates by comparing CLAUDE.md and .claude/ files

## Troubleshooting

### setup-claude-code.sh fails with "command not found"
Make sure the script is executable:
```bash
chmod +x scripts/setup-claude-code.sh
./scripts/setup-claude-code.sh .
```

### Pre-commit hook not running
Verify the hook is installed:
```bash
ls -la .git/hooks/pre-commit
```

If missing, reinstall:
```bash
./scripts/setup-claude-code.sh . --reinstall-hooks
```

### Settings not loading
Verify `.claude/settings.json` exists and is valid JSON:
```bash
cat .claude/settings.json | python3 -m json.tool
```

## License

Use this template as-is or customize for your organization.
