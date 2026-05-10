# Fix Issue Workflow

Systematic approach to diagnosing and fixing bugs.

## Fix Checklist

### 1. Understand the Issue
- Read error message carefully
- Reproduce locally
- Check logs for context
- Gather stack trace

### 2. Root Cause Analysis
- What changed recently?
- Is this a known issue?
- Check git history
- Isolate failing code

### 3. Reproduce Consistently
- Can you reproduce reliably?
- What are the exact steps?
- Does it affect specific cases?
- Create a minimal test case

### 4. Investigate Dependencies
- Is external API failing?
- Check database queries
- Review configuration
- Look for race conditions

### 5. Write a Test
- Create failing test
- Test reproduces the bug
- Test passes after fix
- Add edge case tests

### 6. Implement Fix
- Make minimal changes
- Don't refactor while fixing
- Add comments explaining fix
- Update documentation

### 7. Verify the Fix
- All tests pass?
- Manual testing successful?
- No regressions?
- Performance acceptable?

### 8. Document and Deploy
- Commit with clear message
- Note root cause
- Update CHANGELOG
- Deploy and monitor

## Debugging Techniques

**Add strategic logging:**
```python
logger.debug(f"Entering with: {param}")
logger.debug(f"After processing: {result}")
```

**Narrow down the problem:**
```python
assert variable is not None
assert len(items) > 0
assert isinstance(data, dict)
```

**Use a debugger:**
```python
import pdb; pdb.set_trace()
```

## Common Bugs

**None-related errors:**
```python
# ❌ Bug
value = fetch_value()
return value.upper()  # Fails if None

# ✓ Better
value = fetch_value()
if value is None:
    raise ValueError("No value")
return value.upper()
```

**Off-by-one errors:**
```python
# ❌ Bug: skips first
for i in range(1, len(items)):
    process(items[i])

# ✓ Correct
for i in range(len(items)):
    process(items[i])
```
