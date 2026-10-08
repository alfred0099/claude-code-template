---
paths:
  - "**/*.py"
---
# Python style

Only what ruff and pyright don't already enforce. Run them; don't restate them.

- Type-hint every function signature. Use concrete types (`list[Resource]`), not bare `list` or `dict`.
- `logger = logging.getLogger(__name__)`. Never log secrets, tokens or credentials.
- Catch specific exceptions. Never swallow one silently; log with context and re-raise or return a typed failure.
- Pydantic v2 `BaseModel` for structured data crossing module boundaries.
- Docstrings on public functions whose behaviour isn't obvious from name and types. Skip them otherwise.
