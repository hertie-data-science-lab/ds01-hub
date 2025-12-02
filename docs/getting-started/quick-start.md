# Quick Start Guide

**For experienced users familiar with Docker, HPC, or containers.** Get your first container running in 5 minutes.

---

## Prerequisites

- SSH access to DS01 server
- Account created by system administrator
- Member of `docker` group (check: `groups | grep docker`)

---

## 5-Minute Quickstart

### 1. First-Time Setup (2 min)
```bash
# Complete onboarding wizard
user-setup

# Or skip wizard and go manual:
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
mkdir -p ~/workspace ~/dockerfiles
```

### 2. Deploy Your First Container (1 min)
```bash
# Interactive mode - choose framework and start
container-deploy my-first-project

# Or specify everything:
container-deploy my-project \
  --gpu 1 \
  --framework pytorch \
  --open
```

This command:
- Creates a container with PyTorch/TensorFlow/JAX
- Allocates GPU(s) based on availability
- Mounts `~/workspace/my-project/` as `/workspace`
- Starts container and opens shell

### 3. Work Session
```bash
# Inside container
cd /workspace
git clone your-repo
python train.py

# Exit when done
exit
```

### 4. Retire Container (30 sec)
```bash
# Stop + remove + free GPU
container-retire my-project

# Your workspace files are safe in ~/workspace/my-project/
```

**Done!** You've learned the DS01 workflow.

---

## Essential Commands

### Container Lifecycle
```bash
# Deploy (create + start)
container-deploy <project>              # Interactive
container-deploy <project> --open       # Create and enter
container-deploy <project> --background # Create and start in background

# Retire (stop + remove + free GPU)
container-retire <project>              # Interactive confirmation
container-retire <project> --force      # Skip confirmations

# Manual control (advanced)
container-create <project>              # Create only
container-start <project>               # Start in background
container-run <project>                 # Start and enter
container-stop <project>                # Stop only
container-remove <project>              # Remove only

# Monitoring
container-list                          # View all containers
container-stats                         # Resource usage
```

### Custom Images
```bash
# Interactive builder
image-create                            # 4-phase wizard

# List your images
image-list

# Update existing image
image-update <project>

# Remove image
image-delete <project>
```

### Project Management
```bash
# Complete project initialization
project-init                            # dir + git + image + container

# Individual steps
dir-create <project>                    # Create workspace directory
git-init <project>                      # Initialize git repo
readme-create <project>                 # Generate README.md
```

---

## Key Concepts (1 min read)

### Ephemeral Container Model
```
Containers = temporary compute (like EC2 instances)
Workspaces = persistent storage (like EBS volumes)
```

**Daily workflow:**
1. Morning: `container-deploy` → Start working
2. Work: Code, train, experiment
3. Evening: `container-retire` → Free GPU for others

**What's saved:** `~/workspace/<project>/`, Dockerfiles, Docker images
**What's removed:** Container instance, GPU allocation

### Resource Limits
```bash
# Check your quotas
cat ~/.ds01-limits

# Typical limits:
# - Max GPUs: 1-2
# - Max containers: 2-3
# - Memory: 64-128GB per container
# - Idle timeout: 48h
```

### GPU Allocation
```bash
# Request GPUs
container-deploy my-project --gpu 2

# MIG instances (A100 partitioning)
# - 1 MIG instance = ~20GB GPU memory
# - Automatic allocation based on availability

# Check GPU usage
nvidia-smi                              # Inside container
ds01-dashboard                          # System-wide view
```

---

## Architecture Overview

### Layered Command System

**L3: Orchestrators (Most Common)**
- `container-deploy` = create + start
- `container-retire` = stop + remove

**L2: Atomic Commands (Manual Control)**
- `container-{create|start|run|stop|remove}`
- `image-{create|list|update|delete}`
- `{dir|git|readme}-{create|init}`

**L4: Wizards (Onboarding)**
- `user-setup` = complete onboarding wizard
- `project-init` = create workspace + image + container

### File Locations
```
~/workspace/<project>/          # Your persistent files
~/dockerfiles/<project>.Dockerfile  # Image blueprints
~/.ds01-limits                   # Your resource quotas
/opt/ds01-infra/                # System installation
```

### Container Naming
- **Images**: `ds01-<user>/<project>:latest`
- **Containers**: `<project>._.<user>` (AIME convention)

---

## Common Workflows

### Starting a New Project
```bash
# Quick: All-in-one wizard
project-init

# Manual: Step-by-step
mkdir -p ~/workspace/my-research
cd ~/workspace/my-research
git init
image-create                    # Build custom image
container-deploy my-research --open
```

### Daily Usage
```bash
# Morning
container-deploy active-project --open
cd /workspace
git pull

# Work session
python experiments/train.py
jupyter lab --ip=0.0.0.0        # If using Jupyter

# Evening
exit                            # Exit container
container-retire active-project # Free GPU
```

### Long Training Jobs
```bash
# Deploy in background
container-deploy training --background

# Attach to running container
container-run training          # Or: docker exec -it training... bash

# Prevent idle timeout
touch ~/workspace/training/.keep-alive

# Monitor
container-stats
nvidia-smi                      # Inside container
```

### Custom Image Workflow
```bash
# Build custom image
image-create
# → Choose: PyTorch 2.8.0
# → Add: scikit-learn, transformers, datasets
# → Phase 1: Framework (5 min)
# → Phase 2: Jupyter (1 min)
# → Phase 3: Data science packages (3 min)
# → Phase 4: Custom requirements (optional)

# Use custom image
container-deploy my-project
# (Automatically uses ds01-<user>/my-project:latest)
```

---

## System Status

### Check Available Resources
```bash
# Admin dashboard (if enabled)
ds01-dashboard

# GPU status
python3 /opt/ds01-infra/scripts/docker/gpu_allocator.py status

# Your containers
container-list
docker ps -a --filter "name=._.$(whoami)"

# Your resource usage
container-stats
```

### Check Your Limits
```bash
cat ~/.ds01-limits

# Example output:
# Max GPUs: 2
# Max CPUs: 32
# Memory: 128GB
# Max Containers: 3
# Idle Timeout: 48h
# Priority: 50
```

---

## Guided Mode

All commands support `--guided` flag for educational explanations:

```bash
container-deploy my-project --guided
# → Explains each step
# → Shows what's happening
# → Teaches Docker/GPU concepts
```

---

## Troubleshooting

### Container Won't Start
```bash
# Check if GPU exists
nvidia-smi

# Check if container was stopped
docker ps -a | grep "your-container"

# Recreate if GPU was reassigned
container-remove old-project
container-create old-project
```

### Out of Resources
```bash
# Check your limits
cat ~/.ds01-limits

# Stop idle containers
container-retire old-project

# Check system availability
ds01-dashboard
```

### Can't Access Files
```bash
# Workspaces are in ~/workspace/
ls ~/workspace/

# Inside container, mounted at /workspace
cd /workspace
```

### Image Build Failed
```bash
# Check Dockerfile
cat ~/dockerfiles/my-project.Dockerfile

# Rebuild
image-update my-project

# Or start fresh
image-delete my-project
image-create
```

---

## Differences from Standard Docker

### What's Different?

| Standard Docker | DS01 |
|----------------|------|
| `docker run` | `container-deploy` (handles GPU allocation) |
| Manual GPU flags | Automatic GPU allocation |
| No resource limits | Enforced limits via systemd cgroups |
| Root access inside | User isolation (UID mapping) |
| Manual volume mounts | Automatic workspace mounting |

### What's the Same?

- Docker images and Dockerfiles work normally
- `docker exec`, `docker logs`, `docker inspect` work
- Standard Docker commands available (but prefer DS01 commands)
- Container isolation and networking

### When to Use Docker Directly

**Use DS01 commands for:**
- Creating containers (handles GPU allocation)
- Checking status (user-friendly output)
- Resource management

**Use Docker directly for:**
- Debugging (`docker logs`, `docker inspect`)
- Advanced operations (`docker network`, `docker volume`)
- One-off commands (`docker exec <container> <command>`)

---

## Next Steps

### Learn More
- [Ephemeral Containers Concept](../background/ephemeral-philosophy.md) - Philosophy and best practices
- [Resource Management](../background/resource-management.md) - How limits work
- [Industry Practices](../background/industry-parallels.md) - Production relevance

### Advanced Topics
- [Dockerfile Guide](../advanced/dockerfile-guide.md) - Efficient image building
- [VSCode Remote](../advanced/vscode-remote.md) - Remote development setup
- [Best Practices](../advanced/best-practices.md) - Performance and security

### Complete Reference
- [Command Reference](../reference/command-reference.md) - All commands with options
- [Troubleshooting](../reference/troubleshooting.md) - Common issues
- [Resource Limits](../reference/resource-limits.md) - Quota details

---

## Cheat Sheet

```bash
# Daily workflow
container-deploy project --open          # Start working
container-retire project                 # Done for the day

# Container management
container-list                           # View containers
container-stats                          # Resource usage
container-run project                    # Attach to running

# Image management
image-create                             # Build custom image
image-list                               # View images
image-update project                     # Rebuild image

# System status
ds01-dashboard                           # System resources
cat ~/.ds01-limits                       # Your quotas
nvidia-smi                               # GPU status (in container)

# Help
<command> --help                         # Command options
<command> --guided                       # Educational mode
```

---

**Questions?** Check [Troubleshooting](../reference/troubleshooting.md) or contact your system administrator.

**Want deeper understanding?** Read [Welcome to DS01](welcome.md) for context and philosophy.
