# Health Check Endpoint

The `/api/v1/healthz` endpoint provides service health status.

## Endpoint Details

- **URL**: `/api/v1/healthz`
- **Method**: `GET`
- **Auth Required**: No
- **Purpose**: Kubernetes liveness and readiness probes

## Request

### Example Request
```bash
curl https://python-app-0-dev.roofstacks.com/api/v1/healthz
```

### Request Headers
```http
GET /api/v1/healthz HTTP/1.1
Host: python-app-0-dev.roofstacks.com
Accept: application/json
```

## Response

### Success Response (200 OK)

Service is healthy and ready to accept traffic:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-01T10:30:00Z",
  "checks": {
    "application": "ok",
    "dependencies": "ok"
  }
}
```

### Unhealthy Response (503 Service Unavailable)

Service is experiencing issues:
```json
{
  "status": "unhealthy",
  "timestamp": "2025-12-01T10:30:00Z",
  "checks": {
    "application": "ok",
    "dependencies": "failed"
  },
  "error": "Database connection failed"
}
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Overall health status: `healthy` or `unhealthy` |
| `timestamp` | string | Health check timestamp in ISO 8601 format |
| `checks` | object | Individual component health checks (optional) |
| `error` | string | Error message if unhealthy (optional) |

## HTTP Status Codes

| Code | Status | Meaning |
|------|--------|---------|
| 200 | OK | Service is healthy |
| 503 | Service Unavailable | Service is unhealthy |

## Use Cases

### 1. Kubernetes Liveness Probe

Detects if pod needs restart:
```yaml
livenessProbe:
  httpGet:
    path: /api/v1/healthz
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 30
  timeoutSeconds: 5
  failureThreshold: 3
```

### 2. Kubernetes Readiness Probe

Detects if pod can receive traffic:
```yaml
readinessProbe:
  httpGet:
    path: /api/v1/healthz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
```

### 3. Load Balancer Health Check

Configure load balancer to check health:
```bash
# Check interval: 10s
# Timeout: 5s
# Healthy threshold: 2
# Unhealthy threshold: 3
```

### 4. Monitoring Alert

Create alerts based on health status:
```yaml
alert: ServiceUnhealthy
expr: probe_success{job="python-app-0"} == 0
for: 5m
labels:
  severity: critical
annotations:
  summary: "Service python-app-0 is unhealthy"
```

## Code Examples

### Python
```python
import requests
import time

def check_health():
    url = "https://python-app-0-dev.roofstacks.com/api/v1/healthz"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print("✓ Service is healthy")
            return True
        else:
            print("✗ Service is unhealthy")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Health check failed: {e}")
        return False

# Poll health status
while True:
    check_health()
    time.sleep(30)
```

### Shell Script
```bash
#!/bin/bash

URL="https://python-app-0-dev.roofstacks.com/api/v1/healthz"
MAX_RETRIES=3
RETRY_DELAY=5

for i in $(seq 1 $MAX_RETRIES); do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL)
    
    if [ $HTTP_CODE -eq 200 ]; then
        echo "✓ Service is healthy"
        exit 0
    else
        echo "✗ Health check failed (attempt $i/$MAX_RETRIES)"
        sleep $RETRY_DELAY
    fi
done

echo "✗ Service is unhealthy after $MAX_RETRIES attempts"
exit 1
```

### Docker Healthcheck
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/api/v1/healthz || exit 1

CMD ["python", "app.py"]
```

## Best Practices

1. **Fast Response**: Health checks should complete quickly (< 1 second)
2. **Lightweight**: Don't perform expensive operations
3. **Accurate**: Reflect actual service health
4. **Consistent**: Return predictable status codes
5. **Detailed**: Include check details when unhealthy

## Troubleshooting

### Health Check Always Failing

Check:
- Application is running
- Port is accessible
- No firewall blocking
- Resource limits not exceeded
```bash
# Test locally
curl -v http://localhost:8080/api/v1/healthz

# Check pod logs
kubectl logs -l app=python-app-0

# Check pod status
kubectl describe pod -l app=python-app-0
```

### Intermittent Failures

Adjust probe settings:
```yaml
# Increase timeout
timeoutSeconds: 10

# Increase failure threshold
failureThreshold: 5

# Increase period
periodSeconds: 60
```

## Next Steps

- [System Info Endpoint](info-endpoint.md)
- [Monitoring](../operations/monitoring.md)
- [Troubleshooting](../operations/troubleshooting.md)