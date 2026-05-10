# Code Review Workflow

Systematic code review for quality and consistency.

## Review Checklist

### 1. Architecture & Design
- Does code follow project architecture?
- Are design decisions documented?
- Could this be simpler?

### 2. Type Safety
- All function signatures have return types?
- All parameters are type-hinted?
- Pydantic models used for complex data?

### 3. Error Handling
- Specific exceptions caught?
- Errors logged with context?
- Meaningful error messages?

### 4. Testing
- Unit tests cover happy path?
- Edge cases tested?
- Mocks used for external calls?
- Coverage >= 80%?

### 5. Code Style
- Follows code-style.md?
- Imports ordered correctly?
- Naming is consistent?

### 6. Logging & Debugging
- Logs at appropriate levels?
- No sensitive data logged?
- Helpful for debugging?

### 7. Documentation
- Docstrings on public functions?
- Complex logic explained?
- README updated?

### 8. Final Check
- Code reviewed by others?
- All tests passing?
- Ready to merge?

## Common Issues

**Missing type hints:**
```python
# ❌ Bad
def calculate(x, y):
    return x + y

# ✓ Good
def calculate(x: float, y: float) -> float:
    return x + y
```

**Bare except:**
```python
# ❌ Bad
try:
    result = operation()
except:
    pass

# ✓ Good
try:
    result = operation()
except ValueError as e:
    logger.exception("Operation failed")
    raise
```
