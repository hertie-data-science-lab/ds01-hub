# First-Time Setup Guide

Welcome! This guide walks you through setting up your DS01 account from scratch. By the end, you'll have:
- SSH keys configured for secure access
- Your first project workspace
- A custom Docker image with your chosen ML framework
- Your first running container

**Estimated time:** 15-20 minutes

---

## Prerequisites

Before you begin:
- [ ] You have an account on the DS01 server (created by admin)
- [ ] You can log in via SSH: `ssh your-username@ds01-server`
- [ ] You're a member of the `docker` group (check: `groups | grep docker`)

If anything is missing, contact your system administrator.

---

## Method 1: Automated Setup (Recommended)

### Run the Setup Wizard

The `user-setup` command guides you through complete onboarding:

```bash
user-setup
```

or

```bash
user setup
```

or

```bash
new-user
```

### What the Wizard Does

**Step 1: SSH Key Setup**
```
Setting up SSH keys for secure access...

Do you have an existing SSH key? (y/n): n

Generating new SSH key...
✓ Created ~/.ssh/id_ed25519

Your public key (add this to GitHub, GitLab, etc.):
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJq... user@ds01
```

**What this means:** SSH keys let you access Git repositories and remote services without typing passwords. The wizard creates a secure key pair for you.

**Step 2: Project Initialization**
```
Creating your first project...

Project name: my-first-project
Description: My first DS01 project

✓ Created ~/workspace/my-first-project/
✓ Initialized Git repository
✓ Created README.md
```

**What this means:** Your workspace is where all your code and data live. It's permanent storage - even when containers are removed, workspace files remain.

**Step 3: Custom Image**
```
Building your custom Docker image...

Choose ML framework:
1) PyTorch 2.8.0 (CUDA 12.4)
2) TensorFlow 2.16.1 (CUDA 12.3)
3) JAX 0.4.23 (CUDA 12.3)

Selection: 1

Additional packages (comma-separated):
Examples: scikit-learn, pandas, matplotlib
> scikit-learn, transformers, datasets

Building image (this takes 5-10 minutes)...
Phase 1/4: Base framework... ✓
Phase 2/4: Jupyter Lab... ✓
Phase 3/4: Data science packages... ✓
Phase 4/4: Custom packages... ✓

✓ Image built: ds01-your-username/my-first-project:latest
```

**What this means:** A Docker image is like a blueprint for your computing environment. It contains Python, CUDA drivers, ML frameworks, and all your packages. You're building a custom environment tailored to your needs.

**Step 4: Container Deployment**
```
Deploying your first container...

Allocating GPU resources...
✓ Allocated GPU 0:1 (MIG instance)

Creating container...
✓ Container created: my-first-project._.your-username

Start container now? (y/n): y

Starting container and opening terminal...

Welcome to your DS01 container!
Workspace: /workspace
GPU: Available (check with nvidia-smi)

your-username@my-first-project:/workspace$
```

**What this means:** You now have a running container - an isolated computing environment with GPU access. Your workspace is mounted at `/workspace`.

### Inside Your Container

Try these commands to explore:

```bash
# Check your workspace
ls /workspace
pwd                             # Should show: /workspace

# Verify GPU access
nvidia-smi                      # Shows GPU info

# Check Python and packages
python --version
python -c "import torch; print(torch.cuda.is_available())"

# Start Jupyter (optional)
jupyter lab --ip=0.0.0.0 --port=8888
```

### When You're Done

Exit the container:
```bash
exit
```

Your container is still running. To free the GPU for others:
```bash
container-retire my-first-project
```

**Don't worry!** Your workspace files are safe in `~/workspace/my-first-project/`. You can recreate the container anytime with `container-deploy my-first-project`.

---

## Method 2: Manual Setup (Step-by-Step)

Prefer to understand each step? Here's the manual approach.

### Step 1: SSH Key Setup (2 minutes)

**Why:** SSH keys provide secure, password-less authentication for Git and remote services.

```bash
# Generate SSH key
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""

# Display public key (copy this)
cat ~/.ssh/id_ed25519.pub
```

**Add to GitHub/GitLab:**
1. Copy the public key output
2. Go to GitHub → Settings → SSH Keys → Add SSH key
3. Paste and save

**Learn more:** [SSH Setup Guide](../advanced/ssh-setup.md)

### Step 2: Create Workspace (1 minute)

**Why:** Workspaces are permanent storage for your code and data.

```bash
# Create project directory
mkdir -p ~/workspace/my-first-project
cd ~/workspace/my-first-project

# Initialize Git
git init

# Create README
cat > README.md << 'EOF'
# My First DS01 Project

## Overview
This is my first project on DS01.

## Getting Started
```bash
container-deploy my-first-project --open
```
EOF

git add README.md
git commit -m "Initial commit"
```

**Where are my files?**
- Host system: `~/workspace/my-first-project/`
- Inside container: `/workspace/` (automatically mounted)

### Step 3: Create Dockerfile (5 minutes)

**Why:** Dockerfiles define your computing environment - what packages are installed.

```bash
# Create Dockerfiles directory
mkdir -p ~/dockerfiles

# Create your Dockerfile
cat > ~/dockerfiles/my-first-project.Dockerfile << 'EOF'
# Phase 1: Base framework
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04

# Set working directory
WORKDIR /workspace

# Phase 2: Jupyter Lab
RUN pip install --no-cache-dir \
    jupyterlab \
    ipywidgets \
    matplotlib

# Phase 3: Data science packages
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    seaborn

# Phase 4: Your custom packages
RUN pip install --no-cache-dir \
    transformers \
    datasets \
    accelerate

# Expose Jupyter port
EXPOSE 8888

# Default command
CMD ["/bin/bash"]
EOF
```

**Customize this!** Add packages you need:
- Computer vision: `opencv-python`, `torchvision`, `albumentations`
- NLP: `transformers`, `tokenizers`, `spacy`
- Data: `polars`, `dask`, `pyarrow`
- Plotting: `plotly`, `bokeh`, `altair`

**Learn more:** [Dockerfile Guide](../advanced/dockerfile-guide.md)

### Step 4: Build Image (7-10 minutes)

**Why:** Building creates a Docker image from your Dockerfile - your environment blueprint.

```bash
# Build image (this takes time - downloads base image and installs packages)
docker build \
  -t ds01-$(whoami)/my-first-project:latest \
  -f ~/dockerfiles/my-first-project.Dockerfile \
  .

# Verify image
docker images | grep ds01-$(whoami)
```

**What's happening:**
1. Downloads base image (~5GB, one-time download)
2. Installs Jupyter and extensions
3. Installs data science packages
4. Installs your custom packages
5. Tags image with your username

**Tip:** This is slow the first time (downloading base image). Subsequent builds reuse cached layers.

### Step 5: Deploy Container (1 minute)

**Why:** Containers are instances of your image - your actual computing environment.

```bash
# Deploy container with GPU
container-deploy my-first-project --open
```

**Or manually:**
```bash
# Create container (allocates GPU, mounts workspace)
container-create my-first-project

# Start and enter
container-run my-first-project
```

### Step 6: Verify Setup

Inside your container, run:

```bash
# Check location
pwd                             # Should show: /workspace
ls                              # Should show: README.md

# Check GPU
nvidia-smi                      # Should show GPU details

# Check Python environment
python --version                # Should be 3.10+
pip list | grep torch           # Should show PyTorch 2.8.0

# Quick test
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
python -c "import torch; print(f'GPU count: {torch.cuda.device_count()}')"
```

Expected output:
```
CUDA available: True
GPU count: 1
```

---

## Understanding Your Setup

### File Organization

```
~/ (your home directory)
├── workspace/
│   └── my-first-project/           # ← Your code and data (PERSISTENT)
│       ├── README.md
│       ├── data/
│       ├── notebooks/
│       └── src/
├── dockerfiles/
│   └── my-first-project.Dockerfile # ← Environment blueprint (PERSISTENT)
└── .ds01-limits                    # ← Your resource quotas
```

**Inside container:**
```
/ (container filesystem)
└── workspace/                      # ← Mounted from ~/workspace/my-first-project/
    ├── README.md
    └── (your files)
```

### What's Persistent vs Ephemeral

| Location | Persistent? | Notes |
|----------|-------------|-------|
| `~/workspace/` | ✅ Yes | Always safe, even after `container-retire` |
| `~/dockerfiles/` | ✅ Yes | Image blueprints |
| Docker images | ✅ Yes | Can recreate containers |
| Container instance | ❌ No | Removed with `container-retire` |
| Files in `/tmp` | ❌ No | Inside container, not workspace |
| GPU allocation | ❌ No | Released when container stops |

**Golden rule:** Save everything important in `/workspace` (inside container) = `~/workspace/<project>/` (on host).

### Resource Limits

Check your quotas:
```bash
cat ~/.ds01-limits
```

Typical limits:
- **Max GPUs:** 1-2 (or MIG instances)
- **Max Containers:** 2-3 simultaneously
- **Memory:** 64-128GB per container
- **CPUs:** 16-32 cores per container
- **Idle Timeout:** 48 hours (auto-stop if idle)

**What this means:** You can't use unlimited resources. Fair sharing ensures everyone gets a turn.

---

## Next Steps

### Learn the Daily Workflow

Now that you're set up, practice the daily workflow:

1. **Morning:** `container-deploy my-first-project --open`
2. **Work:** Code, train models, experiment
3. **Evening:** `container-retire my-first-project`

**Read:** [Daily Usage Patterns](../guides/daily-workflow.md)

### Customize Your Environment

Want to add more packages?

```bash
# Update your Dockerfile
nano ~/dockerfiles/my-first-project.Dockerfile

# Rebuild image
image-update my-first-project

# Recreate container
container-retire my-first-project
container-deploy my-first-project --open
```

**Read:** [Building Custom Images](../guides/custom-images.md)

### Understand the Fundamentals

New to Linux or containers? Build foundational knowledge:
- [Linux Basics](../background/linux-basics.md)
- [Containers Explained](../background/containers-and-docker.md)
- [Workspaces & Persistence](../background/workspaces-and-persistence.md)

### Learn DS01 Concepts

Understand the philosophy and design:
- [Ephemeral Containers](../background/ephemeral-philosophy.md)
- [Resource Management](../background/resource-management.md)
- [Industry Practices](../background/industry-parallels.md)

### Explore Advanced Topics

Ready to level up?
- [VSCode Remote Setup](../advanced/vscode-remote.md) - Develop locally with remote compute
-  - Performance and security tips
- [Dockerfile Guide](../advanced/dockerfile-guide.md) - Advanced image building

---

## Troubleshooting

### "Command not found: user-setup"

**Solution:** Commands may not be in your PATH. Try:
```bash
/opt/ds01-infra/scripts/user/wizards/user-setup
```

Or ask admin to run:
```bash
sudo /opt/ds01-infra/scripts/system/deploy-commands.sh
```

### "Permission denied" for Docker

**Cause:** Not in `docker` group.

**Solution:** Ask admin to run:
```bash
sudo /opt/ds01-infra/scripts/system/add-user-to-docker.sh your-username
```

Then log out and back in.

### Image Build Fails

**Common causes:**
- Network issues (downloading base image)
- Typo in package name
- Package incompatibility

**Debug:**
```bash
# Check Dockerfile syntax
cat ~/dockerfiles/my-first-project.Dockerfile

# Try building with output
docker build -f ~/dockerfiles/my-first-project.Dockerfile .
```

**Learn more:** [Troubleshooting Guide](../reference/troubleshooting.md)

### Container Won't Start

**Check:**
```bash
# Are GPUs available?
nvidia-smi

# Do you have quota?
cat ~/.ds01-limits

# Are you at max containers?
container-list
```

### Can't Find My Files

**Remember:**
- Host: `~/workspace/<project>/`
- Container: `/workspace/`

**Check:**
```bash
# On host
ls ~/workspace/my-first-project/

# In container
ls /workspace/
```

---

## Quick Reference

### Essential Commands

```bash
# Container lifecycle
container-deploy <project> --open    # Create + start + enter
container-retire <project>           # Stop + remove + free GPU
container-list                       # View containers

# Image management
image-create                         # Build custom image
image-list                           # View images
image-update <project>               # Rebuild

# Workspace
cd ~/workspace/<project>/            # Your files
ls ~/dockerfiles/                    # Image blueprints

# Status
cat ~/.ds01-limits                   # Your quotas
nvidia-smi                           # GPU status (in container)
```

### Getting Help

```bash
# Command help
container-deploy --help

# Guided mode (educational)
container-deploy --guided

# System status
ds01-dashboard                       # If enabled
```

---

## Congratulations!

You're now set up on DS01! You have:
- ✅ SSH keys for secure access
- ✅ A project workspace (persistent storage)
- ✅ A custom Docker image (your environment)
- ✅ Your first container (compute environment)

**Ready to work:**
```bash
container-deploy my-first-project --open
```

**Questions?** Check [Troubleshooting](../reference/troubleshooting.md) or ask your admin.

**Want to learn more?** Choose your path: [Learning Path Guide](choosing-your-path.md)
