# API Overview

Complete API reference for python-app-0.

## Base URL
```
https://python-app-0-dev.roofstacks.com
```

## API Versioning

The API uses URL-based versioning:

- Current version: `v1`
- Base path: `/api/v1/`

## Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/info` | GET | System information |
| `/api/v1/healthz` | GET | Health check |

## Authentication

Currently, this service does not require authentication. Future versions may implement:

- API Keys
- JWT tokens
- OAuth 2.0

## Request Format

All requests should include:
```http
Accept: application/json
```

## Response Format

All responses are in JSON format:
```json
{
  "status": "success",
  "data": { ... }
}
```

## HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid request format |
| 404 | Not Found | Endpoint not found |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service is down |

## Error Responses

Error responses follow this format:
```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "timestamp": "2025-12-01T10:30:00Z"
}
```

## Rate Limiting

Currently no rate limiting is implemented. Future versions may include:

- 1000 requests per hour per IP
- Rate limit headers in responses

## Examples

### Using cURL
```bash
curl -X GET \
  https://python-app-0-dev.roofstacks.com/api/v1/info \
  -H 'Accept: application/json'
```

### Using Python
```python
import requests

base_url = "https://python-app-0-dev.roofstacks.com"
response = requests.get(f"{base_url}/api/v1/info")
data = response.json()
print(data)
```

### Using JavaScript
```javascript
fetch('https://python-app-0-dev.roofstacks.com/api/v1/info')
  .then(response => response.json())
  .then(data => console.log(data));
```

## Next Steps

- [System Info Endpoint](info-endpoint.md)
- [Health Check Endpoint](health-endpoint.md)