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

### 1. Containerisation (Docker)

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
- **Data Scientist:** Deploy models as containerised APIs
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
- **Cost optimise:** Different tiers for compute vs storage
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

**All use containerisation and ephemeral compute.**

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

## Best Practices from Industry

### 1. Immutable Infrastructure

**Principle:** Never modify running systems. Replace with new version.

**DS01:**
```bash
# Don't: Modify running container
container-run my-project
pip install new-package  # Bad: Not reproducible

# Do: Update image, recreate container
image-update                  # Add package via interactive GUI
container-retire my-project
container-deploy my-project
```

**Production equivalent:**

- **Blue/green deployments:** Run two identical environments ("blue" = current, "green" = new). Deploy changes to green, test it, then switch traffic. If something breaks, instantly switch back to blue. You never modify blue while it's serving users.

- **Rolling updates:** Instead of updating all servers at once (risky), update them one-by-one. If server #3 fails after update, stop the rollout - servers #4-10 still run the old version. Users experience zero downtime.

- **No SSH into production:** Never log into a running server to "fix" something. That fix isn't reproducible, isn't tracked, and will vanish when the server restarts. Instead, fix it in code, build a new image, and deploy that image.

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

- **Application code in Git:** Every line of code is tracked. You can see who changed what, when, and why. You can revert bad changes. Multiple people can work on the same codebase without overwriting each other.

- **Infrastructure as Code (Terraform, CloudFormation):** Your servers, databases, and networks are defined in code files, not clicked together in a web console. Need 10 identical servers? Change `count = 10` and run `terraform apply`. The entire infrastructure is reproducible and auditable.

- **CI/CD configs:** Your build and deployment process is also in Git. A `.github/workflows/deploy.yml` file defines exactly how code goes from commit to production. No manual steps, no tribal knowledge, no "ask Dave how to deploy".

- **Documentation:** READMEs, architecture diagrams, and runbooks live alongside the code. When the code changes, the docs change in the same commit. Documentation that lives in a wiki gets stale; documentation in the repo stays current.

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

- **Logging (ELK stack, CloudWatch):** Every application writes structured logs (JSON, not plain text). These flow to a central system where you can search across thousands of containers: "show me all errors from the payment service in the last hour". ELK = Elasticsearch (storage) + Logstash (processing) + Kibana (visualisation).

- **Metrics (Prometheus, Datadog):** Numeric measurements collected every few seconds: request latency, error rates, CPU usage, queue depth. Displayed on dashboards so you can see trends. "Response time increased 50% after yesterday's deploy" - you'd never spot this in logs.

- **Tracing (Jaeger, X-Ray):** Follow a single request as it travels through multiple services. User clicks "buy" → API gateway → auth service → payment service → inventory service → notification service. Tracing shows you exactly where the 2-second delay is happening.

- **Alerting (PagerDuty, Opsgenie):** Automated systems that wake you up at 3am when something breaks. "Error rate > 5% for 5 minutes" → page the on-call engineer. Connects to your phone, escalates if you don't respond, tracks incident resolution.

### 4. Least Privilege

**DS01:**
- User namespace isolation (not root on host)
- Resource limits (can't monopolise)
- GPU pinning (can't access others' GPUs)

**Production:**

- **IAM roles (minimal permissions):** Your ML training job needs to read from S3 and write to a model registry - nothing else. It can't delete databases, can't access other teams' data, can't spin up Bitcoin miners. Every service gets exactly the permissions it needs and no more.

- **Network policies (limit connectivity):** Your frontend can talk to the API. The API can talk to the database. But the frontend cannot talk directly to the database. Even if an attacker compromises one service, they can't reach everything else.

- **Pod security policies:** Containers can't run as root, can't mount the host filesystem, can't use privileged mode. A compromised container is contained - it can't escape to the host machine or other containers.

- **Secrets management:** Database passwords, API keys, and certificates are never in code or environment variables. They're stored in a vault (HashiCorp Vault, AWS Secrets Manager) and injected at runtime. Secrets are rotated automatically. If someone leaks a config file, they don't get your credentials.

### 5. Cost Optimisation

**DS01 equivalent:**
```bash
# Free resources when done
container-retire my-project

# Use appropriate resources
# (Don't request max if you need less)
```

**Production:**

- **Spot instances (70% savings):** Cloud providers have spare capacity they sell at huge discounts (60-90% off). The catch: they can terminate your instance with 2 minutes notice. Perfect for training jobs - if interrupted, just restart from a checkpoint. Most ML teams use spot for training, on-demand only for serving.

- **Auto-scaling (pay for what you use):** At 3am, your API gets 10 requests/minute - you need 1 server. At 3pm, it gets 10,000 requests/minute - you need 50 servers. Auto-scaling adds/removes servers based on load. You pay for 1 server at night, 50 during peaks, not 50 all the time.

- **Reserved instances (commitment discounts):** If you know you'll need a GPU server for a year, pay upfront for 30-50% off. Like buying a gym membership vs paying per visit. Good for baseline capacity (the minimum you always need), bad for spiky workloads.

- **S3 lifecycle policies (move to cheaper tiers):** Data you access daily stays in "standard" storage ($0.023/GB/month). Data untouched for 30 days moves to "infrequent access" ($0.0125/GB). After 90 days, it moves to "glacier" ($0.004/GB). Old training runs don't need instant access - automatic tiering cuts storage costs 80%+.

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
- Learn containerisation
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
- Cost optimisation
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

## Next Steps

- → [Ephemeral Containers](ephemeral-philosophy.md) - Understand the philosophy
- → [Daily Usage Patterns](../core-guides/daily-workflow.md) - Put skills into practice
