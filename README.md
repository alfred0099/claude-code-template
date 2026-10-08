# Claude Code project template

Shared Claude Code setup for all of Al's projects: honesty rules, a decision gate that keeps work tied to revenue, an advisory board of subagents, and guard hooks. Everything lives in the repo, so it behaves the same on every machine and in cloud sessions (web, mobile).

## Start a project
1. "Use this template" on GitHub, clone, then run `./scripts/setup-claude-code.sh` once per clone.
2. Fill in `decisions/BUSINESS.md` (target, deadline, token budget, hours per week) and `CLAUDE.md`.

## Adopt in an existing project, or pull updates
```bash
curl -fsSL https://raw.githubusercontent.com/alfred0099/claude-code-template/main/scripts/sync-from-template.sh | bash
# or, once the script is in the repo:
./scripts/sync-from-template.sh
git diff   # review, then commit
```
Only paths in `.claude/template-manifest.txt` are overwritten. `CLAUDE.md`, `BUSINESS.md`, decision records, `lessons.md` and path-scoped rules belong to the project.

## How it works
| Piece | Where | Enforced by |
|---|---|---|
| Honesty rules (label claims, no fabrication, report checks truthfully, "do not trust without checking") | `.claude/rules/honesty.md` | Loaded into every session and subagent |
| Change tiers (0: just do it, 1: `/propose` + owner approval, 2: `/propose` + `/board` + owner approval) | `.claude/rules/change-tiers.md` | Instructions, plus the CI decision gate |
| Board: `market-researcher`, `finance`, `red-team` (Opus), `eng-lead` | `.claude/agents/` | Read-only tools, turn caps |
| `/propose`, `/board D-NNNN`, `/outcome-review`, `/review`, `/fix-issue` | `.claude/skills/` | `/board` and `/outcome-review` run only when you invoke them, never automatically |
| Only the owner approves; no `--no-verify`, force push, push to main, or reading secret files | `.claude/hooks/guard.py` | PreToolUse hook (exit 2 blocks) |
| Board status on every session start | `.claude/hooks/board_status.py` | SessionStart hook |
| Tier 1/2 PRs need an approved record | `scripts/decision_gate.py` | `decision-gate.yml` |
| Pre-commit: secret patterns, shellcheck, `make precommit` | `scripts/git-hooks/pre-commit` | `core.hooksPath`, set by the setup script |

Project-specific blocked commands: add `regex<TAB>reason` lines to `.claude/guard-patterns.txt`.

## Limits (read these)
- The guard hooks need `python3`. Without it they **fail open**. CI is the backstop.
- CI can't tell whether you or an agent wrote `status: approved`. The hook stops Claude Code from writing it; nothing stops other tools.
- The pre-commit hook needs the setup script run once per clone. Cloud sessions don't run it, so CI repeats the checks.
- Spend tracking is manual: update `token_spend_month_usd` weekly from the Anthropic Console. Claude can't see your bill.
- The secret scan is pattern-based, not a real scanner. Add gitleaks or similar if this repo ever holds client data.

## Test the hooks
`python3 scripts/test_hooks.py`
