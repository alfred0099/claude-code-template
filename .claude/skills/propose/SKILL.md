---
description: Turn an idea, feature request or enhancement into a decision record in decisions/. Use when the owner proposes Tier 1 or Tier 2 work, or when you notice requested work is Tier 1 or 2 and has no approved record.
argument-hint: "[idea in a sentence]"
---
Create a decision record for: $ARGUMENTS

1. Classify the tier using `.claude/rules/change-tiers.md`. If it is Tier 0, say so and stop. No record is needed.
2. Next ID: one more than the highest `decisions/D-NNNN-*.md` (start at D-0001). File: `decisions/D-NNNN-short-slug.md`, copied from `decisions/_template.md`.
3. Fill every section from what you know now. Label every claim per `.claude/rules/honesty.md`. Read the code if the proposal touches it. Do not do web research here; that is the board's job. Write `unknown` where you don't know.
4. Write a prediction that can be checked: a metric, a number and a date.
5. Leave `status: proposed`. Never set approved, rejected or killed.
6. Tell the owner, in under 8 lines: the ID, the tier, the single weakest assumption, and the next step. Tier 1: "approve it, or run `/board D-NNNN` for a red-team pass". Tier 2: "run `/board D-NNNN`".
