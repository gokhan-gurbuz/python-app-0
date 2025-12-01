# Local Development

Learn how to set up and run python-app-0 on your local machine.

## Clone the Repository
```bash
git clone 
cd python-app-0
```

## Setup Python Environment

### Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:
```bash
APP_ENV=development
PORT=8080
LOG_LEVEL=DEBUG
```

### Load Environment Variables
```bash
# On macOS/Linux:
export $(cat .env | xargs)

# Or use python-dotenv in your code
```

## Run the Application

### Direct Python Execution
```bash
python app.py
```

The application will start on `http://localhost:8080`

### Using Docker
```bash
# Build the image
docker build -t python-app-0:dev .

# Run the container
docker run -p 8080:8080 --env-file .env python-app-0:dev
```

## Verify Installation

Test the endpoints:
```bash
# Health check
curl http://localhost:8080/api/v1/healthz

# System info
curl http://localhost:8080/api/v1/info
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-01T10:30:00Z"
}
```

## Development Workflow

### Hot Reload (Development Mode)
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run with auto-reload
flask run --reload
# or
uvicorn app:app --reload
```

### Code Formatting
```bash
# Format code
black .

# Sort imports
isort .
```

### Linting
```bash
# Run linter
flake8 .

# Type checking
mypy .
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>
```

### Module Not Found
```bash
# Ensure virtual environment is activated
which python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

- [Explore API Endpoints](../api/overview.md)
- [Run Tests](../development/testing.md)
- [Deploy to Kubernetes](../deployment/kubernetes.md)