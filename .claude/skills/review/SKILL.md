---
description: Review the current branch's changes, or a named PR, for correctness, security and scope creep.
argument-hint: "[PR number or base branch, default main]"
---
Review the changes against: $ARGUMENTS. If that is empty, compare the current branch with `main`. If it is a PR number, use `gh pr diff`.

Report, most severe first, each with file:line and a concrete failure scenario:
1. Bugs and incorrect behaviour
2. Security: secrets, injection, authz gaps, unsafe defaults
3. Missing or weakened tests
4. Scope: does the diff match its tier and its decision record (if `feat/D-NNNN`)? Flag any work beyond what was approved.
5. Anything that will cost money at runtime (LLM calls, cloud resources) that isn't mentioned.

Rules: per `.claude/rules/honesty.md`, no praise section and no balancing. If you didn't run the tests, say so. If you find nothing, say "no findings" and list what you checked.
