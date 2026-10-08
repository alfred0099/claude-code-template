---
description: Diagnose and fix a bug from an issue number, error message or failing test.
argument-hint: "[issue number | error | test id]"
---
Fix: $ARGUMENTS

1. If given an issue number, read it with `gh issue view`.
2. Reproduce it. Write a failing test first if the project has tests.
3. Find the root cause, not the symptom. If the fix needs a Tier 1 or 2 change, stop and say so.
4. Make the smallest fix. No drive-by refactors.
5. Run the checks in CLAUDE.md and report the actual results. Name any adjacent code the fix could affect.
