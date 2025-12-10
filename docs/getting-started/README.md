# Welcome to DS01 - Getting Started

## What is DS01?

DS01 is a **shared computing environment** that gives you:
- **GPUs** for training models and running compute-intensive workloads
- **Isolated containers** so your work doesn't conflict with others
- **Pre-built environments** with popular ML frameworks (PyTorch, TensorFlow, JAX)
- **Persistent workspaces** where your code and data are always safe
- **Fair resource sharing** so everyone gets their turn

Think of it as a **data science lab** where you have your own workbench (container), access to powerful equipment (GPUs), but share the facility with colleagues.

## Why Containers?

### The Problem Without Containers

Imagine 20 data scientists sharing one computer:
- Alice needs PyTorch 2.8.0 with CUDA 12.4
- Bob needs TensorFlow 2.16 with different CUDA drivers
- Charlie's experiment crashes and affects everyone else
- GPU conflicts when multiple people want the same GPU

### The Container Solution

Containers give you:
- **Isolation**: Your environment is separate from everyone else's -> you can't break the system or affect others. Worst case: delete your container and start fresh. Your workspace is always safe.
- **Consistency & Reproducibility**: "Works on my machine" actually means something; same env every time

DS01 makes containers easy - you don't need to be a Docker expert.

## How Industry Uses This

**This isn't just for learning - this is how production systems work:**

### Cloud Platforms + MLOps +
- **AWS, Google Cloud, Azure**: Deploy apps in containers (ECS, GKE, AKS) -> each request runs in an isolated container
- **CI/CD pipelines**: Build and test in containers (GitHub Actions, GitLab CI)
- **Model Training & Serving**:  
    - **Training** Spin up GPU containers, train, shut down (save $$$), 
    - **Serving**: Deploy models in containerised APIs that can scale elsstically (Kubernetes)
    - **MLOps platforms**: SageMaker, Vertex AI, Databricks - all use containers
- **Software Engineering**
    - **Microservices**: Each service runs in its own container
    - **Dev envs**: Dev containers (VSCode Remote)
    - **Testing**: Spin up test databases in containers

**Learning DS01 = Learning industry-standard practices**

## Design Philosophy: Ephemeral Containers

DS01 embraces an **ephemeral container model** (familiar to cloud computing, HPC clusters, and Kubernetes):

### Core Principle
```
Containers = Temporary compute sessions
Workspaces = Permanent storage
```

### What's Persistent (Permanent)
- Workspace files (`~/workspace/<project>/`)
- Dockerfiles (image blueprints)
- Docker images (can recreate containers)
- Git repositories

---

## About DS01's Design

DS01 is built on a modular, layered architecture:
- **L0**: Docker - Foundational container runtime
- **L1**: MLC (AIME ML Containers) - 150+ pre-built images (hidden from users, but called internally)
- **L2**: Atomic commands - Single-purpose, composable tools (for adv users)
- **L3**: Orchestrators - Common workflows (deploy, retire)
- **L4**: Setups - Complete onboarding (user-setup, project-init)

### Layered Command System

**L2: Atomic Commands (Manual Control)**
- `container-{create|start|run|stop|remove}`
- `image-{create|list|update|delete}`
- `{dir|git|readme}-{create|init}`

**L3: Orchestrators**
- `container-deploy` = create + start
- `container-retire` = stop + remove

**L4: Wizards**
- `user-setup` = complete onboarding wizard
- `project-init` = create workspace + Dockerfile + requirements
- `project-launch` = check image + build if needed + deploy container