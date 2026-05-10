# Testing Guide

## Running Tests

```bash
pytest tests/ -v
pytest tests/ -m "not integration" -v
pytest tests/ --cov=src --cov-report=html
```

## Test Structure

```
tests/
├── conftest.py
├── test_feature_one.py
├── test_feature_two.py
└── fixtures/
```

## Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    return {"key": "value"}
```

## Unit Tests

```python
def test_calculate():
    result = calculate(10, 20)
    assert result == 30

def test_invalid_input():
    with pytest.raises(ValueError):
        calculate(None)
```

## Mocking

```python
from unittest.mock import patch

@patch('module.external_api')
def test_with_mock(mock_api):
    mock_api.return_value = {"status": "ok"}
    result = my_function()
    assert result is not None
```

## Coverage Goals

- Overall: 80%+
- Critical paths: 90%+

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## Debugging

```bash
pytest tests/ -s          # Show print statements
pytest tests/ -x          # Stop on first failure
pytest tests/ --pdb       # Drop into debugger
```
