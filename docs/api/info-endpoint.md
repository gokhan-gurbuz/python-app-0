# System Info Endpoint

The `/api/v1/info` endpoint provides detailed system information.

## Endpoint Details

- **URL**: `/api/v1/info`
- **Method**: `GET`
- **Auth Required**: No

## Request

### Example Request
```bash
curl https://python-app-0-dev.roofstacks.com/api/v1/info
```

### Request Headers
```http
GET /api/v1/info HTTP/1.1
Host: python-app-0-dev.roofstacks.com
Accept: application/json
```

## Response

### Success Response (200 OK)
```json
{
  "hostname": "python-app-pod-abc123",
  "current_time": "2025-12-01T10:30:00Z",
  "message": "Keep pushing forward!",
  "environment": "dev",
  "version": "1.0.0",
  "uptime": 3600,
  "python_version": "3.11.5"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `hostname` | string | Container/pod hostname identifier |
| `current_time` | string | Current server time in ISO 8601 format |
| `message` | string | Random motivational message |
| `environment` | string | Deployment environment (dev/staging/prod) |
| `version` | string | Application version number |
| `uptime` | integer | Application uptime in seconds (optional) |
| `python_version` | string | Python runtime version (optional) |

## Use Cases

### 1. Service Discovery

Identify which instance is responding:
```bash
curl https://python-app-0-dev.roofstacks.com/api/v1/info | jq '.hostname'
```

### 2. Environment Verification

Verify deployment environment:
```bash
curl https://python-app-0-dev.roofstacks.com/api/v1/info | jq '.environment'
```

### 3. Version Check

Check deployed version:
```bash
curl https://python-app-0-dev.roofstacks.com/api/v1/info | jq '.version'
```

### 4. Time Synchronization

Verify server time:
```bash
curl https://python-app-0-dev.roofstacks.com/api/v1/info | jq '.current_time'
```

## Code Examples

### Python
```python
import requests

def get_system_info():
    url = "https://python-app-0-dev.roofstacks.com/api/v1/info"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Hostname: {data['hostname']}")
        print(f"Environment: {data['environment']}")
        print(f"Version: {data['version']}")
    else:
        print(f"Error: {response.status_code}")

get_system_info()
```

### JavaScript/Node.js
```javascript
const axios = require('axios');

async function getSystemInfo() {
  try {
    const response = await axios.get(
      'https://python-app-0-dev.roofstacks.com/api/v1/info'
    );
    
    console.log('Hostname:', response.data.hostname);
    console.log('Environment:', response.data.environment);
    console.log('Version:', response.data.version);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

getSystemInfo();
```

### Go
```go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

type SystemInfo struct {
    Hostname    string `json:"hostname"`
    CurrentTime string `json:"current_time"`
    Message     string `json:"message"`
    Environment string `json:"environment"`
    Version     string `json:"version"`
}

func main() {
    url := "https://python-app-0-dev.roofstacks.com/api/v1/info"
    
    resp, err := http.Get(url)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    defer resp.Body.Close()
    
    var info SystemInfo
    json.NewDecoder(resp.Body).Decode(&info)
    
    fmt.Printf("Hostname: %s\n", info.Hostname)
    fmt.Printf("Environment: %s\n", info.Environment)
    fmt.Printf("Version: %s\n", info.Version)
}
```

## Error Responses

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "Unable to retrieve system information",
  "timestamp": "2025-12-01T10:30:00Z"
}
```

## Next Steps

- [Health Check Endpoint](health-endpoint.md)
- [API Overview](overview.md)