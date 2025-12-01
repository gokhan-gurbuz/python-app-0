# Environment Variables

Complete reference for environment variables used in python-app-0.

## Overview

Environment variables control application behavior, feature flags, and integration settings.

## Variable Categories

### Application Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `APP_ENV` | Deployment environment | `development` | No |
| `APP_NAME` | Application name | `python-app-0` | No |
| `PORT` | Application port | `8080` | No |
| `HOST` | Bind address | `0.0.0.0` | No |
| `DEBUG_MODE` | Enable debug mode | `false` | No |

### Logging Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LOG_LEVEL` | Logging verbosity | `INFO` | No |
| `LOG_FORMAT` | Log output format | `json` | No |
| `LOG_OUTPUT` | Log destination | `stdout` | No |

**Valid LOG_LEVEL values:**
- `DEBUG`: Detailed debug information
- `INFO`: General information messages
- `WARNING`: Warning messages
- `ERROR`: Error messages only
- `CRITICAL`: Critical errors only

**Valid LOG_FORMAT values:**
- `json`: Structured JSON logs
- `text`: Plain text logs

### Performance Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `WORKERS` | Number of worker processes | `4` | No |
| `THREADS` | Threads per worker | `2` | No |
| `TIMEOUT` | Request timeout (seconds) | `30` | No |
| `KEEPALIVE` | Keep-alive timeout (seconds) | `5` | No |
| `MAX_REQUESTS` | Max requests per worker | `1000` | No |

### Feature Flags

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENABLE_METRICS` | Export Prometheus metrics | `true` | No |
| `ENABLE_TRACING` | Enable distributed tracing | `false` | No |
| `ENABLE_PROFILING` | Enable performance profiling | `false` | No |
| `ENABLE_CORS` | Enable CORS | `true` | No |

### Metrics & Monitoring

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `METRICS_PORT` | Metrics endpoint port | `9090` | No |
| `METRICS_PATH` | Metrics endpoint path | `/metrics` | No |

### Security Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | API authentication key | - | Yes (prod) |
| `JWT_SECRET` | JWT signing secret | - | Yes (if using JWT) |
| `ALLOWED_HOSTS` | Allowed host headers | `*` | No |
| `CORS_ORIGINS` | Allowed CORS origins | `*` | No |

## Environment-Specific Values

### Development
```bash
APP_ENV=development
LOG_LEVEL=DEBUG
DEBUG_MODE=true
WORKERS=1
ENABLE_METRICS=false
ENABLE_PROFILING=true
```

### Staging
```bash
APP_ENV=staging
LOG_LEVEL=INFO
DEBUG_MODE=false
WORKERS=4
ENABLE_METRICS=true
ENABLE_TRACING=true
```

### Production
```bash
APP_ENV=production
LOG_LEVEL=WARNING
DEBUG_MODE=false
WORKERS=8
THREADS=4
ENABLE_METRICS=true
ENABLE_TRACING=true
ENABLE_PROFILING=false
```

## Setting Environment Variables

### Local Development

#### Using .env File
```bash
# .env
APP_ENV=development
PORT=8080
LOG_LEVEL=DEBUG
```

Load with python-dotenv:
```python
from dotenv import load_dotenv
load_dotenv()
```

#### Export in Shell
```bash
export APP_ENV=development
export PORT=8080
export LOG_LEVEL=DEBUG
```

#### Using direnv
```bash
# .envrc
export APP_ENV=development
export PORT=8080
export LOG_LEVEL=DEBUG
```
```bash
# Allow direnv
direnv allow
```

### Docker

#### Dockerfile
```dockerfile
ENV APP_ENV=production
ENV PORT=8080
ENV LOG_LEVEL=INFO
```

#### Docker Run
```bash
docker run \
  -e APP_ENV=production \
  -e PORT=8080 \
  -e LOG_LEVEL=INFO \
  python-app-0:latest
```

#### Docker Compose
```yaml
version: '3.8'
services:
  app:
    image: python-app-0:latest
    environment:
      APP_ENV: production
      PORT: 8080
      LOG_LEVEL: INFO
    env_file:
      - .env
```

### Kubernetes

#### Via ConfigMap
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    envFrom:
    - configMapRef:
        name: python-app-0-config
```

#### Via Secret
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    envFrom:
    - secretRef:
        name: python-app-0-secret
```

#### Individual Variables
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    env:
    - name: APP_ENV
      value: "production"
    - name: PORT
      value: "8080"
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: python-app-0-secret
          key: API_KEY
```

## Accessing Variables in Code

### Python
```python
import os

# Get with default
app_env = os.getenv('APP_ENV', 'development')

# Get required variable
api_key = os.environ['API_KEY']  # Raises KeyError if missing

# Parse boolean
debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

# Parse integer
port = int(os.getenv('PORT', '8080'))

# Parse list
allowed_hosts = os.getenv('ALLOWED_HOSTS', '').split(',')
```

### Using Pydantic Settings
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"
    port: int = 8080
    log_level: str = "INFO"
    debug_mode: bool = False
    workers: int = 4
    
    class Config:
        env_file = '.env'
        case_sensitive = False

settings = Settings()
```

## Validation

### Startup Validation
```python
import os
import sys

def validate_environment():
    """Validate required environment variables on startup"""
    required = ['APP_ENV', 'PORT']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        print(f"ERROR: Missing required variables: {', '.join(missing)}")
        sys.exit(1)
    
    # Validate specific values
    valid_envs = ['development', 'staging', 'production']
    app_env = os.getenv('APP_ENV')
    if app_env not in valid_envs:
        print(f"ERROR: APP_ENV must be one of: {', '.join(valid_envs)}")
        sys.exit(1)

validate_environment()
```

### Type Validation
```python
def get_int_env(key: str, default: int) -> int:
    """Get integer environment variable with validation"""
    value = os.getenv(key, str(default))
    try:
        return int(value)
    except ValueError:
        print(f"ERROR: {key} must be an integer, got: {value}")
        sys.exit(1)

port = get_int_env('PORT', 8080)
```

## Security Best Practices

### 1. Never Commit Secrets
```bash
# .gitignore
.env
.env.*
*.secret.yaml
secrets/
```

### 2. Use Secret Management
```bash
# AWS Secrets Manager
aws secretsmanager get-secret-value \
  --secret-id python-app-0/api-key \
  --query SecretString \
  --output text

# HashiCorp Vault
vault kv get -field=api-key secret/python-app-0
```

### 3. Rotate Secrets Regularly
```bash
# Update secret
kubectl create secret generic python-app-0-secret \
  --from-literal=API_KEY=new-api-key \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart pods
kubectl rollout restart deployment/python-app-0
```

### 4. Principle of Least Privilege

Only expose necessary variables:
```yaml
env:
- name: APP_ENV
  value: "production"
# Don't expose internal secrets unnecessarily
```

## Troubleshooting

### Variable Not Set
```bash
# Check if variable is set
echo $APP_ENV

# List all environment variables
env | grep APP_

# Check in container
kubectl exec <pod-name> -- env | grep APP_
```

### Wrong Value
```bash
# Verify ConfigMap
kubectl get configmap python-app-0-config -o yaml

# Verify Secret
kubectl get secret python-app-0-secret -o jsonpath='{.data.API_KEY}' | base64 -d

# Check pod environment
kubectl describe pod <pod-name> | grep -A 20 "Environment:"
```

### Variable Not Updating
```bash
# Update ConfigMap/Secret
kubectl apply -f k8s/configmap.yaml

# Force pod restart
kubectl delete pod -l app=python-app-0
```

## Reference Configuration

### Complete .env Template
```bash
# Application Settings
APP_ENV=development
APP_NAME=python-app-0
PORT=8080
HOST=0.0.0.0
DEBUG_MODE=false

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_OUTPUT=stdout

# Performance
WORKERS=4
THREADS=2
TIMEOUT=30
KEEPALIVE=5
MAX_REQUESTS=1000

# Features
ENABLE_METRICS=true
ENABLE_TRACING=false
ENABLE_PROFILING=false
ENABLE_CORS=true

# Metrics
METRICS_PORT=9090
METRICS_PATH=/metrics

# Security (DO NOT COMMIT REAL VALUES)
API_KEY=your-api-key-here
JWT_SECRET=your-jwt-secret-here
ALLOWED_HOSTS=*
CORS_ORIGINS=*
```

## Next Steps

- [Configuration Management](configuration.md)
- [Kubernetes Deployment](kubernetes.md)
- [Monitoring Setup](../operations/monitoring.md)