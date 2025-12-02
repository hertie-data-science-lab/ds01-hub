# Welcome to DS01

Welcome to DS01 Infrastructure - a GPU-enabled container platform designed for data science, machine learning, and scientific computing.

## What is DS01?

DS01 is a **shared computing environment** that gives you:
- **Powerful GPUs** for training models and running compute-intensive workloads
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

**This is chaos.**

### The Container Solution

Containers give you:
- **Isolation**: Your environment is separate from everyone else's
- **Consistency**: "Works on my machine" actually means something
- **Reproducibility**: Same environment every time
- **Efficiency**: Share hardware without conflicts

DS01 makes containers easy - you don't need to be a Docker expert.

## How Industry Uses This

**This isn't just for learning - this is how production systems work:**

### Cloud Platforms
- **AWS, Google Cloud, Azure**: Deploy apps in containers (ECS, GKE, AKS)
- **Serverless functions**: Each request runs in an isolated container
- **CI/CD pipelines**: Build and test in containers (GitHub Actions, GitLab CI)

### Data Science in Production
- **Model training**: Spin up GPU containers, train, shut down (save $$$)
- **Model serving**: Deploy models in containerized APIs (Kubernetes)
- **Jupyter notebooks**: JupyterHub runs each user in a container
- **MLOps platforms**: SageMaker, Vertex AI, Databricks - all use containers

### Software Engineering
- **Microservices**: Each service runs in its own container
- **Development environments**: Dev containers (VSCode Remote)
- **Testing**: Spin up test databases in containers

**Learning DS01 = Learning industry-standard practices**

## The DS01 Philosophy: Ephemeral Containers

DS01 embraces an **ephemeral container model** - inspired by cloud computing, HPC clusters, and Kubernetes:

### Core Principle
```
Containers = Temporary compute sessions
Workspaces = Permanent storage
```

### Think of It Like...

**Your laptop:**
- When done working: shut down laptop (free RAM/battery)
- When you reboot: files are still there
- You don't leave laptop running 24/7

**DS01 containers:**
- When done working: `container-retire` (free GPU for others)
- When you restart: files are still in workspace
- You don't leave containers running when idle

### What's Ephemeral (Temporary)
- ❌ Container instance (can be recreated anytime)
- ❌ GPU allocation (freed immediately on retire)
- ❌ Processes running in container

### What's Persistent (Permanent)
- ✅ Workspace files (`~/workspace/<project>/`)
- ✅ Dockerfiles (image blueprints)
- ✅ Docker images (can recreate containers)
- ✅ Git repositories

### Why This Matters

**For you:**
- Simple mental model: "Shut down when done"
- Learn cloud-native practices (AWS spot instances, Kubernetes pods)
- No complex state management

**For the community:**
- GPUs freed immediately for others
- No stale allocations or "stopped but allocated" limbo
- Fair resource sharing

**For your career:**
- Matches AWS/GCP workflows (terminate EC2 instances, delete GKE pods)
- Prepares you for production MLOps (ephemeral training jobs)
- Industry best practice

## Your First Day: What to Expect

### 1. First-Time Setup (~10 minutes)
Run `user-setup` to configure:
- SSH keys for remote access
- Your first project workspace
- A custom Docker image
- Your first container

**See**: [First-Time Setup Guide](first-time-setup.md)

### 2. Daily Workflow (~2 minutes to start working)
```bash
# Morning: Start working
container-deploy my-project --open      # Create + start + enter

# (Do your work: code, train models, experiment)

# Evening: Done for the day
container-retire my-project             # Stop + remove + free GPU
```

**See**: [Daily Usage Patterns](../guides/daily-workflow.md)

### 3. Customize Your Environment
Build custom images with your packages:
```bash
image-create                            # Interactive builder
# Choose PyTorch 2.8.0, add scikit-learn, pandas, your favorite tools
```

**See**: [Building Custom Images](../guides/custom-images.md)

## Key Concepts You'll Learn

As you use DS01, you'll gain practical experience with:

### Technical Skills
- **Linux command line**: Navigate directories, manage files
- **Docker containers**: Images, containers, lifecycle management
- **GPU computing**: CUDA, GPU monitoring, MIG partitioning
- **Version control**: Git workflows in a team environment
- **Remote development**: SSH, VSCode Remote, Jupyter

### Professional Skills
- **Resource management**: Working within limits, fair sharing
- **Infrastructure thinking**: Separate compute from storage
- **Cloud-native practices**: Stateless compute, persistent storage
- **Collaboration**: Shared resources, communication, good citizenship

### Industry Practices
- **Container orchestration**: Deploy/retire workflows (like Kubernetes)
- **Infrastructure as code**: Dockerfiles, reproducible environments
- **MLOps**: Training jobs, model serving, resource optimization
- **Cost optimization**: Shut down resources when not in use

## Common Questions

### "Do I lose my work when I retire a container?"
**No!** Your workspace files are always safe. Think of it like shutting down your laptop - files persist.

### "How is this different from my laptop?"
Your laptop has ~8GB RAM and maybe a consumer GPU. DS01 has 2TB RAM and professional data center GPUs (A100, H100). Plus, your files are backed up.

### "What if I need my environment to persist?"
Your Docker **image** persists - that's your environment blueprint. Containers are instances created from images. You can recreate containers instantly.

### "Can I keep a container running overnight?"
Yes, for active workloads (long training jobs). But idle containers may be auto-stopped after your idle timeout (typically 48 hours). Use `.keep-alive` files for long-running jobs.

### "How many GPUs can I use?"
Depends on your user group. Most users get 1-2 GPUs. Run `cat ~/.ds01-limits` to check your quotas.

### "What if I mess something up?"
Containers are isolated - you can't break the system or affect others. Worst case: delete your container and start fresh. Your workspace is always safe.

## Next Steps

### For Beginners
1. Read [First-Time Setup](first-time-setup.md) - Complete onboarding guide
2. Explore [Background](../background/) - Build foundational knowledge
3. Try [Daily Usage Patterns](../guides/daily-workflow.md) - Common workflows

### For Experienced Users
1. Run [Quick Start](quick-start.md) - Get started in 5 minutes
2. Check [Command Reference](../reference/command-reference.md) - All commands
3. Read [Ephemeral Containers](../background/ephemeral-philosophy.md) - DS01's philosophy

### Want to Understand More?
- [What is a Server?](../background/servers-and-hpc.md) - Shared computing explained
- [Containers Explained](../background/containers-and-docker.md) - Docker fundamentals
- [Understanding HPC](../background/servers-and-hpc.md) - High-performance computing

---

**Ready to start?** Let's get you set up: [First-Time Setup Guide](first-time-setup.md)

**Have questions?** Check the [Troubleshooting Guide](../reference/troubleshooting.md) or ask your system administrator.

---

## About DS01's Design

DS01 is built on a modular, layered architecture:
- **L0**: Docker - Foundational container runtime
- **L1**: MLC (AIME ML Containers) - 150+ pre-built images (hidden)
- **L2**: Atomic commands - Single-purpose, composable tools
- **L3**: Orchestrators - Common workflows (deploy, retire)
- **L4**: Wizards - Complete onboarding (user-setup, project-init)

This design means:
- **Beginner-friendly**: Guided modes and wizards
- **Expert-efficient**: Direct atomic commands for power users
- **Educational**: Learn by doing, grow into advanced usage
- **Production-ready**: Matches industry practices

Welcome to the community!
