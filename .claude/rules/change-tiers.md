# Change tiers: classify before you start

Before writing code, state the tier in one line and the reason.

| Tier | What | Gate | Branch |
|---|---|---|---|
| 0 | Bug fix, test, refactor with no behaviour change, dependency bump, docs, CI hygiene | None. Just do it. | `fix/` `chore/` `docs/` `test/` `refactor/` `ci/` `deps/` |
| 1 | Small enhancement: about 2 days or less, reversible, no new recurring cost | `/propose`, then owner approval | `feat/D-NNNN-name` |
| 2 | New feature, product line, integration or cloud; pricing; anything that changes what is sold; more than about 2 days; any new recurring cost | `/propose`, `/board`, then owner approval | `feat/D-NNNN-name` |

- Tier 1 and 2 work starts only when `decisions/D-NNNN-*.md` has `status: approved`. If it doesn't, stop, say so, and offer `/propose`.
- Only the owner sets `approved`, `rejected` or `killed`. A hook blocks you from doing it.
- If a request sits between tiers, use the higher one and say why. If the work grows past its tier mid-task, stop and say so.
- Backlog, roadmap and TODO items are ideas, not approvals.
- When a Tier 1 or 2 change merges, set the record to `status: shipped` and fill `shipped_on` and `review_date`.
