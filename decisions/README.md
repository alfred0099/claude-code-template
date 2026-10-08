# Decisions

Every Tier 1 or 2 change starts here (see `.claude/rules/change-tiers.md`).

| File | Who writes it | What it is |
|---|---|---|
| `BUSINESS.md` | Owner (Claude may propose edits) | Target, budget, constraints. Loaded into every session. |
| `D-NNNN-slug.md` | Claude drafts, board reviews, **owner decides** | One proposal from idea to outcome |
| `CALIBRATION.md` | `/outcome-review` | Predicted vs actual, so the board learns |
| `_template.md` | Nobody | Copied by `/propose` |

Lifecycle: `proposed` → (`/board`) `board-reviewed` → **owner**: `approved` / `rejected` → `shipped` → (`/outcome-review`) `reviewed`. The owner can set `killed` at any point.

To approve: edit the record yourself (terminal, editor, or the GitHub web or mobile editor) and set `status: approved`, `approved_by: <you>`, `approved_on: <date>`. Claude is blocked from writing those fields. CI blocks `feat/D-NNNN-*` PRs until the record says approved.

Update `token_spend_month_usd` and `token_spend_updated` in BUSINESS.md weekly from your Anthropic Console usage page. When they are more than 7 days old, sessions treat spend as unknown.
