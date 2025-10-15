# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a learning repository focused on Docker containerization, Docker Compose orchestration, and Kubernetes deployment. The repository contains multiple projects demonstrating different aspects of containerized Python web services using Sanic framework.

## Project Structure

- **bge_web/**: BGE (BAAI General Embedding) model deployed as a web service using Sanic
- **build_image_1/**: Basic Docker image building examples with Sanic
- **build_image_2/**: Alternative approach using `docker run` for dependency installation
- **docker-compose/**: Docker Compose configurations for GPU-enabled services
- **k8s_learn/**: Kubernetes cluster learning materials (Ubuntu 22.04 on 3 Tencent Cloud servers)
- **k8s_sanic/**: Sanic application deployed on Kubernetes with GitHub Actions CI/CD

## Common Development Commands

### Python Environment Setup
This project uses `uv` for dependency management:

```bash
# Initialize new project (if no pyproject.toml exists)
uv init
uv venv .venv --python 3.11
uv add sanic

# For existing projects with pyproject.toml
pip install uv
uv sync
```

### Docker Operations
```bash
# Build Docker image
docker build -t <image_name>:<tag> .

# Run Docker Compose services
docker-compose -f <compose_file>.yml up -d

# View logs
docker-compose -f <compose_file>.yml logs -f
```

### Kubernetes Operations
```bash
# Apply configurations
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml

# Restart deployment
kubectl rollout restart deployment/sanic-app-deployment

# Check status
kubectl get pods,svc,ingress
```

## Architecture Overview

### GPU-Enabled Services
- **BGE Service** (`docker-compose/bge.yml`): Runs BGE embedding model with GPU support on port 8011
- **Qwen3-30B Service** (`docker-compose/qwen3-30b.yml`): Runs Qwen3-30B LLM with 4 GPUs on port 8010

### CI/CD Pipeline
- **GitHub Actions** (`.github/workflows/deploy.yml`): Automated build and deployment to Kubernetes
- Triggers on pushes to main branch affecting `k8s_sanic/` directory
- Builds Docker image, pushes to DockerHub, and deploys to K8s cluster

### K8s Components
- **Deployment**: Manages Sanic application pods
- **Service**: Exposes application within cluster
- **Ingress**: External access with nginx ingress controller
- **MetalLB**: Load balancer for bare-metal clusters

## Key Configuration Files

### Python Requirements
- Main dependencies: `sanic>=25.3.0` (pyproject.toml:8)
- BGE-specific requirements in `bge_web/requirements.txt`: flagembedding, modelscope, torch
- K8s Sanic requirements in `k8s_sanic/requirements.txt`

### GPU Configuration
All GPU-enabled services use:
```yaml
runtime: nvidia
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          device_ids: ['0']  # or specific GPU IDs
          capabilities: [gpu]
```

### Shared Memory and Logging
Standard configuration for performance services:
```yaml
shm_size: '50g'  # or '100g' for large models
logging:
  driver: "json-file"
  options:
    max-size: "500m"
    max-file: "5"
```

## Development Workflow

1. **Local Development**: Use `uv` for dependency management
2. **Docker Testing**: Build images locally with Dockerfiles in respective directories
3. **Compose Testing**: Use Docker Compose files for multi-service testing
4. **K8s Deployment**: Push to main branch triggers automatic deployment via GitHub Actions

## Environment Variables

Common environment variables across services:
- `TZ: Asia/Shanghai`
- `ENVIRONMENT: production`
- `PYTHONPATH`: Set appropriately for each service
- `PYTHONDONTWRITEBYTECODE=1` (Docker optimization)
- `PYTHONUNBUFFERED=1` (Real-time logging)

## Port Mapping

- BGE Service: 8011:8011
- Qwen3-30B Service: 8010:8000
- Sanic Demo: 8011:8011
- K8s Sanic: 8000 (internal), exposed via Ingress

## Model Paths (GPU Services)

Services expect models at these host paths:
- `/home/models/bge_m3` → `/models/bge_m3` (container)
- `/home/models/bge-reranker-v2-m3` → `/models/bge-reranker-v2-m3` (container)
- `/home/models/qwen3_30b_a3b` → `/models/qwen3_30b_a3b` (container)