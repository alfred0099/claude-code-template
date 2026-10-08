# Project Name

One paragraph: what this is, who it's for, and what state it's in.

@decisions/BUSINESS.md

## How work is gated
Classify every task by tier before starting (`.claude/rules/change-tiers.md`). Tier 1 and 2 need an approved record in `decisions/`. Honesty rules in `.claude/rules/honesty.md` apply to everything, including subagents. Commands: `/propose`, `/board D-NNNN`, `/outcome-review`, `/review`, `/fix-issue`.

## Commands
```bash
# setup
# run
# test (default run must not spend money or need credentials)
# lint / type check
```

## Architecture
Keep this to what Claude needs in every session. Put area-specific detail in a `CLAUDE.md` inside that folder (loaded only when Claude works there) or in a path-scoped rule under `.claude/rules/`.

## Invariants
Things that must stay true, and where they are enforced.
