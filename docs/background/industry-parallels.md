# Industry Parallels

**How DS01 prepares you for AWS, Kubernetes, and production ML.**

> **Part of [Educational Computing Context](README.md)** - Career-relevant knowledge beyond DS01 basics.

DS01 is designed around industry-standard practices used in production ML systems, cloud platforms, and enterprise software. This guide shows how your DS01 skills transfer to professional work.

---

## The Big Picture

**DS01 skills transfer directly to:**
- Cloud platforms (AWS, Google Cloud, Azure)
- Container orchestration (Kubernetes, Docker Swarm)
- ML platforms (SageMaker, Vertex AI, Databricks)
- Production ML systems (MLOps, model serving)
- Software engineering (microservices, CI/CD)

---

## Core Industry Concepts in DS01

### 1. Containerization (Docker)

**Industry usage:**
- **Development:** Dev containers, consistent environments
- **CI/CD:** Build and test in containers
- **Production:** Deploy applications in containers
- **ML:** Training jobs, model serving APIs

**DS01 parallel:**
```bash
# DS01
container-deploy my-project

# AWS Elastic Container Service
aws ecs run-task --task-definition my-task

# Kubernetes
kubectl run my-pod --image=my-image
```

**Skills you're learning:**
- Docker images and containers
- Dockerfiles (reproducible environments)
- Container lifecycle management
- Volume mounts (persistent storage)
- Resource limits (CPU, memory, GPU)

**Where you'll use this:**
- **Data Scientist:** Deploy models as containerized APIs
- **ML Engineer:** Build training pipelines in containers
- **Software Engineer:** Microservices architecture
- **DevOps:** Container orchestration

---

### 2. Ephemeral Compute

**Industry principle:** Compute is temporary and cheap, storage is permanent

**DS01:**
```bash
container-deploy my-project  # Spin up compute
# Do work
container-retire my-project  # Terminate compute
# Workspace persists
```

**AWS EC2:**
```bash
aws ec2 run-instances        # Launch instance
# Do work
aws ec2 terminate-instances  # Stop paying
# EBS volumes persist
```

**Kubernetes:**
```yaml
kind: Job                    # Ephemeral pod
spec:
  restartPolicy: Never       # Run once, terminate
  volumes:
    - persistentVolumeClaim  # Data persists
```

**Industry applications:**
- **Spot instances:** Save 70% by using temporary compute
- **Auto-scaling:** Scale up for load, scale down to save $$
- **Batch jobs:** Process data, terminate when done
- **CI/CD:** Run tests, terminate runners

---

### 3. Infrastructure as Code

**Industry principle:** Define infrastructure in version-controlled files

**DS01 Dockerfile:**
```dockerfile
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04
WORKDIR /workspace
RUN pip install transformers datasets accelerate
EXPOSE 8888
```

**This is exactly what you'd use in:**
- AWS ECS task definitions
- Kubernetes pod specs
- Google Cloud Run
- Azure Container Instances

**Benefits:**
- **Reproducible:** Same Dockerfile = same environment
- **Version controlled:** Track changes in Git
- **Collaborative:** Share with team
- **Automated:** CI/CD can rebuild automatically

**Skills transferring:**
- Writing Dockerfiles
- Multi-stage builds
- Layer caching
- Build optimization

---

### 4. Resource Management & Fair Scheduling

**DS01 quotas:**
```yaml
# config/resource-limits.yaml
defaults:
  max_gpus: 2
  max_cpus: 16
  memory: 64GB
  priority: 50
```

**Kubernetes equivalent:**
```yaml
# ResourceQuota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: user-quota
spec:
  hard:
    requests.nvidia.com/gpu: "2"
    requests.cpu: "16"
    requests.memory: "64Gi"
```

**AWS equivalent:**
- Service quotas (max instances, max vCPUs)
- Budget alerts
- Cost allocation tags

**Industry applications:**
- **Cost control:** Prevent runaway spending
- **Fair sharing:** Multi-tenant platforms
- **Capacity planning:** Ensure resources available
- **Priority scheduling:** Critical workloads first

---

### 5. Separation of Concerns

**DS01 architecture:**
```
├── Compute (Container)     ← Ephemeral, scalable
├── Storage (Workspace)     ← Persistent, backed up
├── Images (Environment)    ← Versioned, reproducible
└── Orchestration (DS01)    ← Scheduling, limits
```

**Cloud architecture:**
```
├── Compute (EC2, Lambda)   ← Ephemeral, scalable
├── Storage (S3, EBS)       ← Persistent, backed up
├── Images (ECR, Artifact Registry) ← Versioned
└── Orchestration (ECS, K8s) ← Scheduling, auto-scaling
```

**Benefits:**
- **Scale independently:** Add storage without changing compute
- **Cost optimize:** Different tiers for compute vs storage
- **Resilience:** Compute fails? Recreate. Data always safe.

---

## Real-World Workflow Parallels

### ML Model Training

**DS01 workflow:**
```bash
# 1. Build environment
image-create

# 2. Launch training container
container-deploy training --background

# 3. Monitor progress
container-stats
docker logs training._.$(whoami)

# 4. Training complete, free resources
container-retire training

# 5. Model saved to workspace
ls ~/workspace/training/models/
```

**AWS SageMaker workflow:**
```python
# 1. Define environment
estimator = PyTorch(
    image_uri="pytorch-training-image",
    ...
)

# 2. Launch training job
estimator.fit(inputs)
# Job runs on ephemeral instances

# 3. Monitor
estimator.logs()

# 4. Training complete, instances terminated
# (automatic)

# 5. Model saved to S3
model_artifacts = estimator.model_data
```

**Same conceptual workflow!**

---

### Model Serving (API Deployment)

**DS01 approach (simplified):**
```bash
# Build image with model serving code
docker build -t model-api .

# Run API container
container-deploy model-api --background

# Inside container
python api.py  # Flask/FastAPI app
```

**Production (Kubernetes):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-api
spec:
  replicas: 3  # Auto-scaling
  template:
    spec:
      containers:
      - name: api
        image: model-api:latest
        resources:
          limits:
            nvidia.com/gpu: 1
```

**Concepts:**
- Containerized service
- Resource limits
- Health checks
- Scaling (manual on DS01, auto in production)

---

### CI/CD Pipeline

**DS01 testing:**
```bash
# Build test environment
docker build -f test.Dockerfile .

# Run tests in container
docker run test-image pytest
```

**GitHub Actions (Production):**
```yaml
name: Test
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: pytorch:2.8.0
    steps:
      - uses: actions/checkout@v2
      - run: pip install -r requirements.txt
      - run: pytest
```

**Same principle:** Isolated test environment, reproducible results

---

## Industry Tools & Platforms

### Cloud Platforms

**Amazon Web Services (AWS):**
- **ECS/EKS:** Container orchestration (like DS01 + Kubernetes)
- **SageMaker:** ML platform (training, serving, monitoring)
- **EC2 + GPUs:** Elastic compute (on-demand, spot instances)
- **S3:** Object storage (like persistent workspace)

**Google Cloud Platform (GCP):**
- **GKE:** Kubernetes engine
- **Vertex AI:** ML platform
- **Compute Engine + GPUs:** VM instances
- **Cloud Storage:** Object storage

**Microsoft Azure:**
- **AKS:** Azure Kubernetes Service
- **Azure ML:** ML platform
- **Azure VMs + GPUs:** Compute
- **Blob Storage:** Object storage

**DS01 skills apply to all of them.**

---

### Container Orchestration

**Kubernetes:**
- Most popular container orchestrator
- Runs in production at Google, Amazon, Microsoft, etc.
- Concepts directly map to DS01:
  - Pods = Containers
  - PersistentVolumes = Workspace
  - ResourceQuotas = DS01 limits
  - Jobs = Ephemeral compute

**Docker Swarm:**
- Simpler orchestrator
- Good for smaller deployments
- Docker compose for multi-container apps

**Learning DS01 = Foundation for Kubernetes**

---

### ML Platforms

**AWS SageMaker:**
- Managed ML platform
- Notebook instances (like Jupyter containers)
- Training jobs (ephemeral compute)
- Model registry (like Docker images)
- Endpoints (model serving)

**Google Vertex AI:**
- Similar to SageMaker
- Training jobs in containers
- Model deployment
- Feature store

**Databricks:**
- Data + ML platform
- Notebooks in containers
- Spark clusters (ephemeral)
- MLflow integration

**Azure ML:**
- Microsoft's ML platform
- Compute instances/clusters
- Training jobs
- Model deployment

**All use containerization and ephemeral compute.**

---

### MLOps Tools

**Experiment Tracking:**
- **Weights & Biases:** Log metrics from containers
- **MLflow:** Track experiments, models, parameters
- **TensorBoard:** Visualize training

**Model Serving:**
- **TorchServe:** PyTorch model serving
- **TensorFlow Serving:** TensorFlow models
- **Seldon Core:** Multi-framework serving on K8s
- **BentoML:** Package models as APIs

**Workflow Orchestration:**
- **Airflow:** Data pipeline orchestration
- **Kubeflow:** ML workflows on Kubernetes
- **Prefect:** Modern workflow engine

**All deploy workloads in containers.**

---

## Career-Relevant Skills

### Data Scientist

**DS01 teaches:**
- Containerized environments
- Reproducible experiments
- GPU resource management
- Cloud-native workflows

**You'll use:**
- SageMaker training jobs
- Vertex AI notebooks
- Databricks clusters
- Containerized model serving

### ML Engineer

**DS01 teaches:**
- Docker image building
- CI/CD concepts
- Resource optimization
- Production workflows

**You'll use:**
- Kubernetes for model serving
- Docker for reproducibility
- GPU optimization
- Auto-scaling systems

### Data Engineer

**DS01 teaches:**
- Containerized pipelines
- Resource limits
- Workflow automation
- Monitoring

**You'll use:**
- Airflow in containers
- Spark on Kubernetes
- Data pipeline orchestration
- Containerized ETL jobs

### Software Engineer

**DS01 teaches:**
- Microservices (containerized services)
- Infrastructure as code
- CI/CD pipelines
- Resource management

**You'll use:**
- Kubernetes deployments
- Docker compose
- Service mesh (Istio, Linkerd)
- Container security

---

## Best Practices from Industry

### 1. Immutable Infrastructure

**Principle:** Never modify running systems. Replace with new version.

**DS01:**
```bash
# Don't: Modify running container
container-run my-project
pip install new-package  # Bad: Not reproducible

# Do: Update image, recreate container
image-update my-project  # Add package to Dockerfile
container-retire my-project
container-deploy my-project
```

**Production:**
- Blue/green deployments
- Rolling updates
- No SSH into production servers

### 2. Everything in Version Control

**DS01:**
```bash
~/workspace/my-project/
├── .git/               # Code in Git
├── Dockerfile          # Environment in Git
├── requirements.txt    # Dependencies in Git
├── src/                # Source code in Git
└── README.md           # Documentation in Git
```

**Production equivalent:**
- Application code in Git
- Infrastructure as code (Terraform, CloudFormation)
- CI/CD configs
- Documentation

### 3. Observability

**DS01:**
```bash
# Logs
docker logs container-name

# Metrics
container-stats

# GPU monitoring
nvidia-smi
```

**Production:**
- Logging (ELK stack, CloudWatch)
- Metrics (Prometheus, Datadog)
- Tracing (Jaeger, X-Ray)
- Alerting (PagerDuty, Opsgenie)

### 4. Least Privilege

**DS01:**
- User namespace isolation (not root on host)
- Resource limits (can't monopolize)
- GPU pinning (can't access others' GPUs)

**Production:**
- IAM roles (minimal permissions)
- Network policies (limit connectivity)
- Pod security policies
- Secrets management

### 5. Cost Optimization

**DS01 equivalent:**
```bash
# Free resources when done
container-retire my-project

# Use appropriate resources
# (Don't request max if you need less)
```

**Production:**
- Spot instances (70% savings)
- Auto-scaling (pay for what you use)
- Reserved instances (commitment discounts)
- S3 lifecycle policies (move to cheaper tiers)

---

## Bridging to Production

### From DS01 to AWS

**Training job:**
```bash
# DS01
container-deploy training --background

# AWS SageMaker
import sagemaker
estimator = sagemaker.estimator.Estimator(...)
estimator.fit()
```

**Model serving:**
```bash
# DS01 (simple API)
container-deploy api
# Inside: Flask app

# AWS
# Deploy to SageMaker Endpoint or ECS
```

**Skills transfer:**
- Dockerfile → SageMaker image
- Workspace → S3 bucket
- container-deploy → boto3 API calls

### From DS01 to Kubernetes

**Single container:**
```bash
# DS01
container-deploy my-app

# Kubernetes
kubectl run my-app --image=my-image
```

**With resources:**
```bash
# DS01 (configured in YAML)
# max_gpus: 1, memory: 64GB

# Kubernetes
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: my-app
    image: my-image
    resources:
      limits:
        nvidia.com/gpu: 1
        memory: "64Gi"
```

**Concepts map directly.**

---

## Learning Path to Production

### Phase 1: DS01 (You are here)
- Learn containerization
- Practice resource management
- Build reproducible environments
- Understand ephemeral compute

### Phase 2: Cloud Fundamentals
- AWS/GCP free tier accounts
- Deploy simple container to ECS/Cloud Run
- Use S3/GCS for storage
- Try SageMaker/Vertex AI free tier

### Phase 3: Kubernetes
- Local K8s (minikube, kind)
- Deploy pods, services
- Learn resource management
- Try managed K8s (EKS, GKE)

### Phase 4: MLOps
- Experiment tracking (W&B, MLflow)
- Model serving (TorchServe, Seldon)
- CI/CD (GitHub Actions)
- Monitoring (Prometheus, Grafana)

### Phase 5: Production Scale
- Multi-region deployments
- Auto-scaling
- Cost optimization
- Security hardening

**DS01 is your foundation for all of this.**

---

## Industry Jargon Decoder

**Terms you'll hear in jobs:**

| Industry Term | DS01 Equivalent |
|--------------|----------------|
| Container orchestration | DS01 management layer |
| Pod (K8s) | Container |
| Persistent Volume | Workspace |
| Job (K8s) | Ephemeral container |
| Image registry (ECR, GCR) | Docker images |
| Resource quota | Resource limits YAML |
| Node (K8s) | DS01 server |
| Deployment | Container deploy/retire |
| Service mesh | (Advanced, not in DS01) |
| Ingress | (Network routing, not in DS01) |

---

## Summary

**Key Takeaways:**

1. **DS01 uses industry-standard tools** (Docker, YAML configs, GPU management)
2. **Workflows mirror production** (ephemeral compute, persistent storage, IaC)
3. **Skills transfer directly** to AWS, GCP, Azure, Kubernetes
4. **Core concepts are universal** (containerization, resource limits, fair sharing)
5. **Career preparation** for data science, ML engineering, software engineering

**DS01 isn't just for learning - it's training you for production ML systems.**

**Learning DS01 = Learning industry best practices**

**Next Steps:**

- → [Ephemeral Containers](ephemeral-containers.md) - Understand the philosophy
→  - Production-ready habits
- → [Daily Usage Patterns](../guides/daily-workflow.md) - Put skills into practice

---

**You're not just learning a system - you're learning an industry.**
