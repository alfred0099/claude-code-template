---
paths:
  - "tests/**"
  - "**/test_*.py"
  - "**/*_test.py"
---
# Testing

- Every bug fix gets a test that fails before the fix and passes after.
- Mock external services (cloud APIs, LLM calls, HTTP). Tests that need real credentials or spend money must carry a marker and be excluded from the default run. Name the marker in CLAUDE.md.
- Never delete, skip or loosen a failing test to get green. Fix the code, or tell the owner the test is wrong and why.
- Coverage targets are only claims if a coverage command was run. Don't state a coverage number you didn't measure.
