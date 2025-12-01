# Troubleshooting

Common issues and solutions for python-app-0.

## Quick Diagnostic Commands
```bash
# Check pod status
kubectl get pods -n python-app-0

# View pod events
kubectl get events -n python-app-0 --sort-by='.lastTimestamp'

# Check pod logs
kubectl logs -f -l app=python-app-0 -n python-app-0

# Describe pod for details
kubectl describe pod <pod-name> -n python-app-0

# Check service endpoints
kubectl get endpoints -n python-app-0

# Test internal connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  wget -qO- http://python-app-0.python-app-0.svc.cluster.local/api/v1/healthz
```

## Common Issues

### 1. Pod Not Starting

#### Symptoms
- Pod status: `Pending`, `CrashLoopBackOff`, or `Error`
- Application not accessible

#### Diagnosis
```bash
# Check pod status
kubectl get pods -n python-app-0

# Describe pod
kubectl describe pod <pod-name> -n python-app-0

# Check logs
kubectl logs <pod-name> -n python-app-0

# Check previous logs if pod restarted
kubectl logs <pod-name> -n python-app-0 --previous
```

#### Common Causes & Solutions

**Image Pull Error:**
```bash
# Symptom in describe output
Events:
  Warning  Failed  2m   kubelet  Failed to pull image

# Solution: Check image name and registry access
kubectl get pod <pod-name> -n python-app-0 -o jsonpath='{.spec.containers[0].image}'

# Verify image exists
docker pull <image-name>

# Check image pull secrets
kubectl get secrets -n python-app-0
```

**Insufficient Resources:**
```bash
# Symptom in describe output
Events:
  Warning  FailedScheduling  2m   default-scheduler  0/3 nodes are available: insufficient memory

# Solution: Check and adjust resource requests
kubectl get pod <pod-name> -n python-app-0 -o yaml | grep -A 5 resources

# Edit deployment to reduce requests
kubectl edit deployment python-app-0 -n python-app-0
```

**Configuration Error:**
```bash
# Check ConfigMap
kubectl get configmap python-app-0-config -n python-app-0 -o yaml

# Check Secret
kubectl get secret python-app-0-secret -n python-app-0 -o yaml

# Validate environment variables
kubectl exec <pod-name> -n python-app-0 -- env
```

**Application Error:**
```bash
# Check application logs
kubectl logs <pod-name> -n python-app-0 --tail=100

# Common Python errors
# - ImportError: Check dependencies in requirements.txt
# - SyntaxError: Check Python version compatibility
# - ConnectionError: Check external service connectivity
```

### 2. Service Not Accessible

#### Symptoms
- HTTP 503 or connection timeout
- Cannot reach application endpoints

#### Diagnosis
```bash
# Check service
kubectl get svc python-app-0 -n python-app-0

# Check endpoints
kubectl get endpoints python-app-0 -n python-app-0

# Check ingress
kubectl get ingress python-app-0 -n python-app-0

# Describe service
kubectl describe svc python-app-0 -n python-app-0
```

#### Common Causes & Solutions

**No Endpoints:**
```bash
# Symptom
$ kubectl get endpoints python-app-0 -n python-app-0
NAME           ENDPOINTS   AGE
python-app-0   <none>      5m

# Cause: Selector mismatch
# Check service selector
kubectl get svc python-app-0 -n python-app-0 -o jsonpath='{.spec.selector}'

# Check pod labels
kubectl get pods -n python-app-0 --show-labels

# Solution: Fix selector in service.yaml
```

**Port Mismatch:**
```bash
# Check service ports
kubectl get svc python-app-0 -n python-app-0 -o yaml | grep -A 3 ports

# Check container ports
kubectl get pod <pod-name> -n python-app-0 -o yaml | grep -A 3 containerPort

# Solution: Ensure service targetPort matches container port
```

**Ingress Issues:**
```bash
# Check ingress configuration
kubectl describe ingress python-app-0 -n python-app-0

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# Test without ingress
kubectl port-forward svc/python-app-0 8080:80 -n python-app-0
curl http://localhost:8080/api/v1/healthz
```

### 3. Health Check Failures

#### Symptoms
- Pods restarting frequently
- `Liveness probe failed` in events

#### Diagnosis
```bash
# Check probe configuration
kubectl get pod <pod-name> -n python-app-0 -o yaml | grep -A 10 livenessProbe

# Check health endpoint
kubectl exec <pod-name> -n python-app-0 -- \
  curl -f http://localhost:8080/api/v1/healthz || echo "Health check failed"

# View events
kubectl describe pod <pod-name> -n python-app-0 | grep -A 10 Events
```

#### Common Causes & Solutions

**Slow Startup:**
```yaml
# Solution: Increase initialDelaySeconds
livenessProbe:
  httpGet:
    path: /api/v1/healthz
    port: 8080
  initialDelaySeconds: 30  # Increase this
  periodSeconds: 10
```

**Timeout Too Short:**
```yaml
# Solution: Increase timeout
livenessProbe:
  httpGet:
    path: /api/v1/healthz
    port: 8080
  timeoutSeconds: 10  # Increase this
```

**Application Actually Unhealthy:**
```bash
# Check application logs
kubectl logs <pod-name> -n python-app-0

# Check resource usage
kubectl top pod <pod-name> -n python-app-0

# Check dependencies
kubectl exec <pod-name> -n python-app-0 -- \
  curl -v http://external-dependency:port/health
```

### 4. High Memory Usage

#### Symptoms
- Pods being OOMKilled
- `OOMKilled` in pod status
- Memory limits exceeded

#### Diagnosis
```bash
# Check current memory usage
kubectl top pod -n python-app-0

# Check memory limits
kubectl get pod <pod-name> -n python-app-0 \
  -o jsonpath='{.spec.containers[0].resources}'

# View OOMKill events
kubectl get events -n python-app-0 --field-selector reason=OOMKilling
```

#### Solutions

**Increase Memory Limits:**
```yaml
resources:
  requests:
    memory: "256Mi"  # Increase from 128Mi
  limits:
    memory: "512Mi"  # Increase from 256Mi
```

**Profile Application:**
```python
# Add memory profiling
import tracemalloc

tracemalloc.start()

# ... application code ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

**Check for Memory Leaks:**
```bash
# Monitor memory over time
watch -n 5 'kubectl top pod -n python-app-0'

# Enable verbose GC logging
kubectl set env deployment/python-app-0 \
  PYTHONMALLOC=debug \
  -n python-app-0
```

### 5. High CPU Usage

#### Symptoms
- Slow response times
- CPU throttling
- High latency

#### Diagnosis
```bash
# Check CPU usage
kubectl top pod -n python-app-0

# Check CPU limits
kubectl get pod <pod-name> -n python-app-0 \
  -o jsonpath='{.spec.containers[0].resources}'
```

#### Solutions

**Increase CPU Limits:**
```yaml
resources:
  requests:
    cpu: "200m"  # Increase from 100m
  limits:
    cpu: "500m"  # Increase from 200m
```

**Profile Application:**
```python
# Add CPU profiling
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... application code ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

**Optimize Code:**
```python
# Use caching for expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(param):
    # ... computation ...
    return result
```

### 6. Slow Response Times

#### Symptoms
- High P95/P99 latencies
- Timeout errors
- Poor user experience

#### Diagnosis
```bash
# Check response times in Prometheus
# http_request_duration_seconds

# Test endpoint directly
time curl https://python-app-0-dev.roofstacks.com/api/v1/info

# Check application logs
kubectl logs -f -l app=python-app-0 -n python-app-0 | grep duration_ms
```

#### Solutions

**Add Caching:**
```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def get_cached_data(key):
    # Expensive operation
    return data
```

**Optimize Database Queries:**
```python
# Add indexes
# Use connection pooling
# Implement query caching
```

**Increase Worker Count:**
```yaml
env:
- name: WORKERS
  value: "8"  # Increase from 4
```

### 7. Configuration Issues

#### Symptoms
- Application behavior unexpected
- Features not working as expected

#### Diagnosis
```bash
# Check ConfigMap
kubectl get configmap python-app-0-config -n python-app-0 -o yaml

# Check environment variables in pod
kubectl exec <pod-name> -n python-app-0 -- env | sort

# Compare with expected configuration
```

#### Solutions

**Update ConfigMap:**
```bash
# Edit ConfigMap
kubectl edit configmap python-app-0-config -n python-app-0

# Or apply new configuration
kubectl apply -f k8s/configmap.yaml

# Restart pods to pick up changes
kubectl rollout restart deployment/python-app-0 -n python-app-0
```

**Validate Configuration:**
```python
# Add configuration validation
import os

required_vars = ['APP_ENV', 'PORT', 'LOG_LEVEL']
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    raise ValueError(f"Missing required configuration: {', '.join(missing)}")
```

### 8. Network Connectivity Issues

#### Symptoms
- Cannot connect to external services
- DNS resolution failures
- Timeout errors

#### Diagnosis
```bash
# Test DNS resolution
kubectl exec <pod-name> -n python-app-0 -- nslookup google.com

# Test external connectivity
kubectl exec <pod-name> -n python-app-0 -- \
  curl -v https://api.external-service.com

# Check network policies
kubectl get networkpolicies -n python-app-0

# Test internal service connectivity
kubectl exec <pod-name> -n python-app-0 -- \
  curl -v http://other-service.other-namespace.svc.cluster.local
```

#### Solutions

**DNS Issues:**
```bash
# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check DNS configuration
kubectl exec <pod-name> -n python-app-0 -- cat /etc/resolv.conf
```

**Network Policy:**
```yaml
# Allow egress to external services
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress
spec:
  podSelector:
    matchLabels:
      app: python-app-0
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
```

## Alert Runbooks

### High Error Rate Alert

**Alert:** `HighErrorRate`
**Severity:** Critical
**Threshold:** Error rate > 5% for 5 minutes

**Investigation Steps:**

1. Check recent deployments:
```bash
kubectl rollout history deployment/python-app-0 -n python-app-0
```

2. View error logs:
```bash
kubectl logs -l app=python-app-0 -n python-app-0 | grep ERROR
```

3. Check external dependencies:
```bash
# Test connectivity to dependencies
kubectl exec <pod-name> -n python-app-0 -- \
  curl -v http://dependency-service/health
```

4. If recent deployment, consider rollback:
```bash
kubectl rollout undo deployment/python-app-0 -n python-app-0
```

### Service Down Alert

**Alert:** `ServiceDown`
**Severity:** Critical
**Threshold:** Health check fails for 2 minutes

**Investigation Steps:**

1. Check pod status:
```bash
kubectl get pods -n python-app-0
```

2. Check recent events:
```bash
kubectl get events -n python-app-0 --sort-by='.lastTimestamp' | tail -20
```

3. Check logs:
```bash
kubectl logs -l app=python-app-0 -n python-app-0 --tail=50
```

4. Restart if necessary:
```bash
kubectl delete pod -l app=python-app-0 -n python-app-0
```

### Slow Response Time Alert

**Alert:** `SlowResponseTime`
**Severity:** Warning
**Threshold:** P95 > 1s for 10 minutes

**Investigation Steps:**

1. Check resource usage:
```bash
kubectl top pod -n python-app-0
```

2. Check for high load:
```bash
# View request rate in Prometheus
sum(rate(http_requests_total{job="python-app-0"}[5m]))
```

3. Check application logs for slow operations:
```bash
kubectl logs -l app=python-app-0 -n python-app-0 | grep duration_ms | sort -t: -k4 -n | tail -20
```

4. Consider scaling up:
```bash
kubectl scale deployment python-app-0 --replicas=5 -n python-app-0
```

## Debug Tools

### Ephemeral Debug Container
```bash
# Add debug container to running pod
kubectl debug <pod-name> -n python-app-0 \
  --image=busybox \
  --target=python-app-0 \
  -it -- sh
```

### Port Forwarding
```bash
# Forward pod port to local machine
kubectl port-forward <pod-name> 8080:8080 -n python-app-0

# Access at http://localhost:8080
```

### Execute Commands in Pod
```bash
# Run shell in pod
kubectl exec -it <pod-name> -n python-app-0 -- /bin/bash

# Run Python REPL
kubectl exec -it <pod-name> -n python-app-0 -- python

# Check Python packages
kubectl exec <pod-name> -n python-app-0 -- pip list
```

## Getting Help

### Support Channels

- **Slack**: #python-app-0-support
- **Email**: platform-team@roofstacks.com
- **On-Call**: PagerDuty rotation

### Escalation Process

1. Check this troubleshooting guide
2. Search existing issues in Slack
3. Create new support ticket with:
   - Problem description
   - Steps to reproduce
   - Pod logs
   - Recent changes

### Useful Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Application Logs](logging.md)
- [Monitoring Dashboards](monitoring.md)
- [API Documentation](../api/overview.md)

## Next Steps

- [Monitoring Setup](monitoring.md)
- [Logging Configuration](logging.md)
- [Deployment Guide](../deployment/kubernetes.md)