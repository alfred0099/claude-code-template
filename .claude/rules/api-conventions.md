# API Conventions

## Framework

- **Framework:** FastAPI or Flask
- **Authentication:** API key in `X-API-Key` header
- **Rate limiting:** 100 requests/minute per IP

## Response Format

```json
{
  "success": true,
  "data": {},
  "error": null,
  "timestamp": "2024-05-10T10:30:45.123Z"
}
```

Error response:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request"
  }
}
```

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 202 | Accepted (async) |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Server Error |

## Authentication

**Header:**
```bash
curl -H "X-API-Key: sk-test-123" https://api.example.com/endpoint
```

**Query:**
```bash
curl https://api.example.com/endpoint?api_key=sk-test-123
```

## Naming

- Endpoints: `/api/v1/resource` (lowercase, plural)
- Query params: `snake_case`
- Request/response: JSON with `snake_case`

## Pagination

```json
{
  "items": [],
  "total": 42,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

Query params: `limit`, `offset`

## Versioning

- Current: `/api/v1/`
- No breaking changes within v1
- New versions: `/api/v2/`

## Testing

```python
from fastapi.testclient import TestClient

def test_requires_auth():
    client = TestClient(app)
    response = client.get("/api/v1/data")
    assert response.status_code == 403

def test_with_auth():
    client = TestClient(app)
    response = client.get("/api/v1/data", headers={"X-API-Key": "valid"})
    assert response.status_code == 200
```
