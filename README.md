# Cloud-Native DevOps Lab

A small Python Flask application.

The application itself is intentionally simple: it exposes a single HTTP endpoint on port `5000`. The rest of the repository demonstrates how an application can be tested, containerized, built in CI, described for Kubernetes, provisioned alongside AWS infrastructure with Terraform, and prepared for basic monitoring and health checks.

## What the App Does

The Flask application is located in `src/app.py`.

It exposes:

```http
GET /
```

Example response:

```text
Cloud-Native DevOps Lab is running!
```

The application listens on:

```text
0.0.0.0:5000
```

## Project Architecture

```text
Developer
   |
   | push
   v
GitHub
   |
   v
GitHub Actions
   |-- install Python dependencies
   |-- run Pytest
   `-- build Docker image

Application
   |
   v
Python / Flask
   |
   v
Port 5000

Deployment / Operations
   |-- Docker + Docker Compose
   |-- Kubernetes manifests
   |-- Terraform configuration for AWS
   |-- Prometheus configuration
   `-- Shell health-check script
```

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI workflow
├── docker/
│   ├── .dockerignore
│   ├── Dockerfile              # Container image definition
│   └── docker-compose.yml      # Local container orchestration
├── infra/
│   └── main.tf                 # Basic AWS Terraform configuration
├── k8s/
│   ├── deployment.yaml         # Kubernetes Deployment
│   └── service.yaml            # Kubernetes LoadBalancer Service
├── monitor/
│   └── prometheus.yml          # Prometheus scrape configuration
├── scripts/
│   └── health_check.sh         # Basic HTTP availability check
├── src/
│   ├── __init__.py
│   ├── app.py                  # Flask application
│   └── requirements.txt        # Python dependencies
├── test/
│   └── test_app.py             # Pytest test
└── README.md
```

## Prerequisites

For local Python execution:

- Python 3
- `pip`

For containerized execution:

- Docker
- Docker Compose

Optional tools for the deployment/infrastructure examples:

- `kubectl`
- a Kubernetes cluster
- Terraform
- AWS credentials
- Prometheus

## Run Locally with Python

Clone the repository and enter it:

```bash
git clone https://github.com/PITA-OPS/cloud-native-devops-lab.git
cd cloud-native-devops-lab
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the application dependencies:

```bash
pip install -r src/requirements.txt
```

Run the Flask application:

```bash
python src/app.py
```

Open:

```text
http://localhost:5000
```

or test it from another terminal:

```bash
curl http://localhost:5000
```

## Run with Docker Compose

The Compose file is stored inside the `docker/` directory, so run it from the repository root with:

```bash
docker compose -f docker/docker-compose.yml up --build
```

The application will be available at:

```text
http://localhost:5000
```

Test it with:

```bash
curl http://localhost:5000
```

Stop the containers with:

```bash
docker compose -f docker/docker-compose.yml down
```

## Run the Tests

Install the application dependencies and Pytest:

```bash
pip install -r src/requirements.txt
pip install pytest
```

Run:

```bash
pytest test
```

The current test creates a Flask test client, sends a request to `/`, and verifies that the endpoint returns HTTP status `200`.

## GitHub Actions

The CI workflow is defined in:

```text
.github/workflows/ci.yml
```

It runs on pushes to the repository.

The workflow currently:

1. installs the Python dependencies;
2. runs the Pytest suite;
3. builds the Docker image.

This provides a basic CI gate for the application and container build.

## Docker

Container-related files are stored in:

```text
docker/
```

`docker/Dockerfile` packages the Flask application into a Python container.

`docker/docker-compose.yml` provides a convenient way to build and run the application locally while mapping container port `5000` to host port `5000`.

## Kubernetes

Kubernetes manifests are stored in:

```text
k8s/
```

The current configuration contains:

- `deployment.yaml` — a Deployment with two application replicas;
- `service.yaml` — a `LoadBalancer` Service on port `80` that forwards traffic to container port `5000`.

Before deploying, replace the placeholder image in `k8s/deployment.yaml`:

```yaml
image: your-dockerhub-username/devops-app:latest
```

with a real image from your container registry.

After configuring the image and connecting `kubectl` to a cluster:

```bash
kubectl apply -f k8s/
```

Check the resources with:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

## Terraform / AWS

Terraform configuration is stored in:

```text
infra/main.tf
```

The current configuration:

- uses the AWS provider;
- targets the `us-east-1` region;
- defines a single `t2.micro` EC2 instance.

It is a basic Infrastructure-as-Code example rather than a complete deployment of the Flask application.

To inspect it:

```bash
cd infra
terraform init
terraform plan
```

Only run:

```bash
terraform apply
```

after reviewing the plan and verifying the AWS configuration, AMI, credentials, and expected cost.

> AWS resources created by Terraform may incur charges.

## Prometheus

The Prometheus configuration is stored in:

```text
monitor/prometheus.yml
```

It defines a scrape target for the application on port `5000`.

However, the current Flask application does **not** expose a Prometheus `/metrics` endpoint, so this configuration alone does not yet provide working application metrics.

To make Prometheus monitoring functional, the application would need to expose Prometheus-formatted metrics and the scrape target would need to match the environment where the application is running.

## Health Check Script

A basic shell health check is available at:

```text
scripts/health_check.sh
```

It sends an HTTP request to:

```text
http://localhost:5000
```

If the request fails, it prints:

```text
App is down
```

Run it while the application is running:

```bash
bash scripts/health_check.sh
```

## Current Scope

This repository demonstrates the pieces of a DevOps workflow around a small Flask service:

```text
Code
  -> Test
  -> CI
  -> Containerize
  -> Deploy
  -> Provision
  -> Monitor
```

Some files are intentionally basic examples rather than production-ready configurations:

- the Flask application currently has one route;
- the test suite currently contains one endpoint test;
- the Kubernetes deployment uses a placeholder container image until configured;
- the Terraform file defines basic AWS infrastructure but does not deploy the application;
- the Prometheus configuration exists, but the application does not yet expose Prometheus metrics.
