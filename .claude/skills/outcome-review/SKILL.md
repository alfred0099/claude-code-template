---
description: Compare shipped decisions' predictions with what actually happened, and record calibration. Run monthly or when the session start banner says outcome reviews are due.
disable-model-invocation: true
---
1. Find `decisions/D-*.md` with `status: shipped` and `review_date` on or before today.
2. For each one, ask the owner for the actual metric value, or read it from wherever the record says it is measured. Never estimate an outcome. If the value is unavailable, record "not measured" and say that is itself a finding.
3. Append `## Outcome (YYYY-MM-DD)`: predicted, actual, the gap, and why (labelled). Set `status: reviewed`.
4. Add one row per decision to `decisions/CALIBRATION.md`.
5. Read the last 10 rows of CALIBRATION.md and report any pattern in 5 lines or fewer. For example: "effort estimates run 2.5x low", "revenue predictions have all missed", "the red team's top risk was right 3 of 4 times". These patterns are the point of the exercise.
