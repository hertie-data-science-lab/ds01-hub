# Containers & Docker

**Deep dive into container technology and its role in modern computing.**

> **Part of [Educational Computing Context](README.md)** - Career-relevant knowledge beyond DS01 basics.
>
> **Just want to use DS01?** See [Key Concepts: Containers and Images](../key-concepts/containers-and-images.md) for a shorter overview, or skip to [First Container](../getting-started/first-container.md).

Containers are the foundation of DS01 and modern cloud computing. This guide explains what they are, why we use them, and how they work.

**Reading time:** 12 minutes

---

## The Problem Containers Solve

**Scenario: 20 Data Scientists, One Server**

Without containers:
- Alice installs PyTorch 2.8.0 → breaks Bob's code (needs 2.5.0)
- Charlie's experiment uses 100% RAM → crashes everyone's work
- GPU conflicts when multiple people want GPU:0

**This is chaos.** You can't have 20 people modifying one shared environment.

**The Solution - Containers provide:**
- **Isolated environments**: Your packages don't affect others
- **Resource limits**: Your code can't monopolise CPU/RAM
- **Reproducibility**: Same environment every time
- **GPU sharing**: Fair allocation without conflicts

**Think of containers like apartments in a building:**
- Each apartment (container) is isolated
- Shared utilities (power, water) = shared hardware (CPU, GPU)
- Can't affect neighbours
- Building manager (DS01) ensures fair resource usage

---

## What is a Container?

**A container is a lightweight, isolated environment that runs your code with its own libraries, dependencies, and filesystem - without needing a separate operating system.**

### Key Characteristics

**Isolation:**
- Your own filesystem (can't see others' files)
- Your own processes (can't interfere with others)
- Shared kernel (Linux kernel used by all)

**Lightweight:**
- Starts in seconds (vs minutes for VMs)
- Uses MBs of overhead (vs GBs for VMs)

**Portable:**
- Same container runs on your laptop, DS01, AWS, anywhere
- "Works on my machine" → "Works everywhere"

---

## Containers vs Virtual Machines

```
Virtual Machines                     Containers
─────────────────                    ──────────
┌─────────┐ ┌─────────┐             ┌────┐ ┌────┐ ┌────┐
│  VM 1   │ │  VM 2   │             │App1│ │App2│ │App3│
├─────────┤ ├─────────┤             │Libs│ │Libs│ │Libs│
│Guest OS │ │Guest OS │             └────┘ └────┘ └────┘
│(Linux)  │ │(Windows)│             ───────────────────────
└─────────┘ └─────────┘             Container Runtime (Docker)
────────────────────────            ───────────────────────
    Hypervisor                           Host OS (Linux)
────────────────────────
    Host OS                         Shared kernel
```

| Feature | Virtual Machines | Containers |
|---------|-----------------|-----------|
| Startup time | Minutes | Seconds |
| Size | GBs (5-20GB) | MBs (100-500MB) |
| Performance | Slower | Near-native |
| Isolation | Full (separate OS) | Process-level |

**For DS01:** Containers are perfect - lightweight, fast, isolated enough.

---

## Docker: The Container Platform

**Docker** is the most popular container platform:
- **Engine**: Runs containers
- **Images**: Blueprints for containers
- **Registry**: Store and share images
- **Tools**: Build, manage, deploy

### Images vs Containers

**Docker Image (Blueprint):**
- Contains: OS base, Python, libraries, your code
- Stored on disk, read-only
- Can create many containers from one image

**Docker Container (Instance):**
- Running instance of an image
- Has running processes, writable filesystem
- Ephemeral (temporary)

```
Image (blueprint)                    Containers (instances)
─────────────────                    ────────────────────
ds01-alice/my-project:latest    →    my-project._.alice (running)
├── Ubuntu 22.04                      experiment-1._.alice (stopped)
├── Python 3.10
├── PyTorch 2.8.0                    Same image, separate instances
└── My packages
```

**Analogy:** Image = Class definition, Container = Object instance

---

## How Containers Provide Isolation

### 1. Filesystem Isolation
Each container has its own filesystem. Container A cannot see Container B's files.

**Exception:** Mounted volumes (intentional sharing)
- DS01 mounts `~/workspace/<project>/` → `/workspace` in container
- This is your persistent storage

### 2. Process Isolation
Each container sees only its own processes. Can't see or kill other containers' processes.

### 3. Resource Limits (Cgroups)
Linux control groups limit resources:
```bash
# DS01 configures for each container:
--memory="64g"          # Max 64GB RAM
--cpus="16"             # Max 16 CPU cores
--gpus="device=0:1"     # Specific GPU allocation
```

Your container can't use more than allocated.

---

## DS01's Container Architecture

### Three Layers

**Layer 1: AIME ML Containers (Base)**
- 150+ pre-built images with ML frameworks
- PyTorch, TensorFlow, JAX with CUDA

**Layer 2: DS01 Management**
- GPU allocation and scheduling
- Resource limit enforcement
- User isolation, automated cleanup

**Layer 3: Your Custom Images**
- Built on top of AIME images
- Your additional packages

### Container Lifecycle

```
1. Build Custom Image              2. Deploy Container
   (image-create)                     (container-deploy)
   - Choose base: PyTorch 2.8        - Allocate GPU
   - Add packages                     - Set resource limits
   - Result: ds01-alice/proj         - Mount workspace
              │                                │
              ↓                                ↓
3. Work Inside Container           4. Retire Container
   - Train models                     (container-retire)
   - Run experiments                  - Stop container
   - Files saved to /workspace        - Release GPU
                                      - Workspace files remain safe
```

---

## Docker Images Explained

### Images vs Containers (Detailed)

**Image = Blueprint**
- Contains: OS, Python, packages, your setup
- Immutable (read-only)
- Can create many containers from one image

**Container = Instance**
- Running instance of an image
- Writable filesystem layer
- Ephemeral (temporary)

### DS01 Image Hierarchy

```
┌────────────────────────────────────┐
│ Base AIME Image                    │
│ (PyTorch 2.8.0 + CUDA + Ubuntu)    │
└──────────────┬─────────────────────┘
               │ FROM
               ↓
┌────────────────────────────────────┐
│ Your Custom Image                  │
│ + Data science packages            │
│ + Your requirements                │
└────────────────────────────────────┘
```

### Image Layers

Images are built in layers:
```
Layer 5: Your packages      (50 MB)
Layer 4: Data science pkgs  (500 MB)
Layer 3: Jupyter Lab        (200 MB)
Layer 2: PyTorch            (2 GB)
Layer 1: Base OS            (1 GB)
────────────────────────────────────
Total: ~3.75 GB
```

**Benefits:**
- **Caching**: Rebuild only changed layers
- **Sharing**: Layers shared between images

### Building Images

**Interactive (recommended):**
```bash
image-create <my-project>
```

**Manual (Dockerfile):**
```dockerfile
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04
WORKDIR /workspace
RUN pip install transformers datasets
```

---

## Inside a Container

When you enter a container:
```bash
$ container-run my-project

# Now inside container
alice@my-project:/workspace$ pwd
/workspace

alice@my-project:/workspace$ nvidia-smi
# Shows your allocated GPU

alice@my-project:/workspace$ python
>>> import torch
>>> torch.cuda.is_available()
True
```

**You have:**
- Linux shell, Python with packages
- GPU access (nvidia-smi works)
- Workspace at `/workspace`
- Network access (download datasets)
- Can pip install (temporary)

**You don't have:**
- Access to host system files (except workspace)
- Access to other containers
- GPUs not allocated to you

---

## Why Containers Matter for Data Science

### 1. Reproducibility
Same container runs everywhere. Dockerfile = reproducible recipe.

### 2. Dependency Management
Each container has its own dependencies. Project A can use TensorFlow 2.16, Project B can use 2.10.

### 3. Resource Management
Container limited to allocated resources. Runaway process can't crash everyone's work.

### 4. GPU Sharing
Container gets dedicated GPU allocation. No conflicts.

### 5. Experiment Tracking
```bash
# Tag image for experiment
docker tag ds01-alice/project:latest ds01-alice/project:experiment-42

# Later: Recreate exact environment
```

---

## Industry Use of Containers

### Production ML Systems

**Model Training (AWS SageMaker):**
- Spin up container with PyTorch
- Train model
- Save weights to S3
- Terminate container

**Model Serving (Kubernetes):**
- Deploy model in container
- Scale to 100 replicas
- Load balance requests

### Software Development

- **Microservices:** Each service runs in container
- **CI/CD:** Tests run in containers (GitHub Actions)

**DS01 experience = Industry-relevant skills**

---

## DS01 vs Standard Docker

| Standard Docker | DS01 |
|----------------|------|
| `docker run ...` | `container-deploy` (handles GPU allocation) |
| Manual GPU flags | Automatic GPU scheduling |
| No resource limits | Enforced limits |
| Manual volume mounts | Auto-mount workspace |

**DS01 commands handle complexity for you.** You can still use Docker directly when needed.

---

## Common Questions

### "Do I need to learn Docker?"

**Basic DS01 usage:** No, use `container-deploy` and `image-create`
- **Custom images:** Basic Dockerfile knowledge helpful
- **Advanced:** Docker knowledge useful for debugging

### "Can I run Docker commands directly?"

Yes! DS01 doesn't restrict Docker access.
```bash
docker ps                   # List containers
docker logs container-name  # View logs
```
Prefer DS01 commands for creation/management.

### "Are containers secure?"

Sufficient isolation for shared academic environment:
- Can't access other users' files
- Can't interfere with other processes
- Resource limits prevent monopolisation

### "What happens to my files?"

- **Container filesystem:** Ephemeral (deleted on removal)
- **Mounted workspace (`/workspace`):** Persistent, survives removal

**Always save important work in /workspace**

### "Can I have multiple containers?"

Yes, within your resource limits:
```bash
check-limits  # See your limits
```

---

## Best Practices

### 1. Save Everything in Workspace
```bash
# Good
/workspace/code/
/workspace/data/
/workspace/models/

# Bad - lost when container removed
/tmp/important-results.csv
```

### 2. Build Custom Images
```bash
# Don't: Install packages every time
container-run my-project
pip install transformers  # Slow, non-reproducible

# Do: Build custom image
image-create  # Add packages to image
```

### 3. Retire Containers When Done
```bash
container-retire my-project  # Free GPU for others
```

### 4. Use Tags for Experiments
```bash
docker tag ds01-alice/project:latest ds01-alice/project:working-baseline
```

---

## Managing Images

```bash
# List images
image-list

# Update image (interactive GUI - recommended)
image-update                  # Select image, add/remove packages

# Rebuild after manual Dockerfile edit (advanced)
image-update my-project --rebuild

# Remove image
image-delete my-project

# Docker commands
docker images
docker rmi <image>
```

---

## Next Steps

- [Workspaces & Persistence](workspaces-and-persistence.md) - What's saved vs temporary
- [Ephemeral Philosophy](ephemeral-philosophy.md) - Why containers are temporary
- [Custom Images Guide](../core-guides/custom-images.md) - Build your environment
- [First Container](../getting-started/first-container.md) - Deploy now
