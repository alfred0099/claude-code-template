---
paths:
  - "**/api/**"
  - "**/api.py"
  - "**/routes/**"
  - "**/interfaces/**"
---
# HTTP API conventions

Defaults for new projects. If the existing code does something different, the code wins; update this file instead of "fixing" the code to match it.

- Auth via a header (`X-API-Key` or `Authorization`). Never accept credentials in query strings; they end up in logs.
- 401 for missing or invalid credentials, 403 for valid credentials without permission.
- Validate input with Pydantic models. Return 422/400 with a field-level message.
- Version breaking changes (`/v2/...`). No breaking changes within a version.
- Rate-limit unauthenticated and expensive endpoints. Anything that triggers a paid LLM call counts as expensive.
