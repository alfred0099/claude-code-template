---
description: Run the advisory board on a decision record. Research, finance, red-team and engineering review, then a chair's memo and recommendation. The owner decides.
argument-hint: "D-NNNN"
disable-model-invocation: true
---
Run the board on decision $ARGUMENTS.

1. Find `decisions/$ARGUMENTS-*.md`. If it is missing, or its status isn't `proposed` or `board-reviewed`, stop and say why.
2. Read `decisions/BUSINESS.md`. If token spend this month is unknown or at least 80% of budget, tell the owner the board run costs tokens and ask before continuing.
3. Pick members by tier:
   - Tier 1: `red-team` only.
   - Tier 2: `market-researcher`, `finance`, `red-team` and `eng-lead`, launched in parallel. Give each the record's path and nothing else; they read the files themselves.
4. As chair, read their reports and append to the record under `## Board review (YYYY-MM-DD)`:
   - each member's report, condensed but keeping every labelled claim and URL
   - **Where they disagree**, and which side the evidence favours
   - **Recommendation:** approve, approve a smaller version (describe it), reject, or get more evidence first (say exactly what, and the cheapest way)
   - **Do not trust without checking** and **Left out**, per `.claude/rules/honesty.md`
5. Set `status: board-reviewed`. You cannot approve, and must not try.
6. Reply to the owner in under 12 lines: the recommendation, the top two risks, the one assumption to check first, and how to decide. "Edit the record: set `status: approved` and `approved_by`, or `rejected`."

Don't soften the recommendation because the owner seems keen on the idea.
