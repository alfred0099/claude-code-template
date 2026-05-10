# Code Style Guide

## Python Style

- **Formatter:** Use `ruff format` (PEP 8 compliant)
- **Line length:** 120 characters
- **Naming:**
  - Classes: `PascalCase`
  - Functions: `snake_case`
  - Constants: `SCREAMING_SNAKE_CASE`
  - Private: prefix with `_`

## Type Hints

**Required for all function signatures and class attributes.**

```python
def process(items: list, threshold: float = 0.5) -> dict:
    return {}
```

## Imports

```python
# Standard library
import json
import logging

# Third-party
import requests

# Local
from .models import MyModel
```

## Logging

- Use `logger = logging.getLogger(__name__)`
- Never log secrets or credentials

## Docstrings

Use Google-style docstrings:

```python
def estimate_cost(resource: str, config: dict) -> float:
    """Estimate cost for resource.

    Args:
        resource: Resource type
        config: Configuration dict

    Returns:
        Estimated cost in USD
    """
```

## Error Handling

- Catch specific exceptions
- Log with context: `logger.exception("message")`

```python
try:
    result = api_call()
except ValueError as e:
    logger.exception("Failed")
    raise
```

## Comments

- Explain *why*, not *what*
- Keep comments updated with code

## Pydantic Models

- Use Pydantic v2 `BaseModel`
- Add `Field` descriptions

```python
from pydantic import BaseModel, Field

class Resource(BaseModel):
    type: str = Field(..., description="Resource type")
    cost: float = Field(..., ge=0)
```
