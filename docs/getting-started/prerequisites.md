# Prerequisites

Before you begin working with python-app-0, ensure you have the following tools and access.

## Required Software

### Python Environment

- **Python**: Version 3.11 or higher
- **pip**: Latest version
- **virtualenv** or **venv**: For isolated environments

Check your Python version:
```bash
python --version
```

### Container Tools

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher

Install Docker:
```bash
# macOS
brew install docker

# Ubuntu
sudo apt-get install docker.io
```

### Kubernetes Tools (Optional)

- **kubectl**: Latest stable version
- **helm**: Version 3.x
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## Access Requirements

### Repository Access

Ensure you have access to:

- Source code repository: 
- Container registry
- Kubernetes cluster (for deployment)

### Network Access

- VPN connection (if required)
- Access to internal services
- DNS configuration for `*.roofstacks.com`

## Development Tools (Recommended)

- **IDE**: VS Code, PyCharm, or similar
- **Git**: Version control
- **Postman/Insomnia**: API testing
- **k9s**: Kubernetes CLI management tool

## Next Steps

Once you have all prerequisites installed, proceed to [Local Development](local-development.md).