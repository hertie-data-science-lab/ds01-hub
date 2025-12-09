# Advanced Users Guide

**For terminal-native users who want Docker-level control and non-interactive workflows.**

---

## Who This Is For

**You're ready for advanced docs if:**
- ✓ You're comfortable in terminal (vim, tmux, bash scripting)
- ✓ You've used Docker before
- ✓ You prefer CLI tools over IDE/GUI
- ✓ You want direct container access
- ✓ You're building batch job pipelines
- ✓ You need non-interactive workflows

**Not there yet?**
- [Getting Started](../getting-started/) - Basics
- [Intermediate](../intermediate/) - Atomic commands, scripting

**This section assumes:**
- Strong Linux/bash knowledge
- Docker familiarity
- Terminal-first mindset

---

## What You'll Learn

### 1. Direct Docker Commands

**Move beyond DS01 wrappers:**

```bash
# DS01 commands (beginner/intermediate)
container-deploy my-project
container-attach my-project

# Docker commands (advanced)
docker run -it --gpus device=0 ds01-12345/my-project:latest
docker exec -it my-project._.12345 bash
```

**Why:**
- Full Docker control
- Standard industry commands
- Works anywhere (not DS01-specific)
- Required for complex workflows

→ [Docker Direct Guide](docker-direct.md)

→ [Terminal Workflows](terminal-workflows.md)

### 2. Batch Jobs and Background Processing

**Submit jobs, check results later:**

```bash
# Submit training job
docker exec -d my-project._.$(id -u) \
  nohup python train.py > /workspace/output.log 2>&1

# Check later
tail -f ~/workspace/my-project/output.log
```

→ [Batch Jobs Guide](batch-jobs.md)

### 3. Build Optimization

**Faster, smaller images:**

- Multi-stage builds
- Layer caching strategies
- Minimal base images

→ [Dockerfile Best Practices](dockerfile-best-practices.md)

### 4. Advanced SSH and Remote Access

**Efficient remote workflows:**

- SSH config files
- Key-based authentication
- Port forwarding for Jupyter/TensorBoard

→ [SSH Advanced Guide](ssh-advanced.md)

### 5. Multi-GPU Training

**Distributed training across multiple MIG instances:**

→ [Multi-MIG Training](multi-mig-training.md)

---

## DS01 Docker Enforcement

**Important: Direct Docker commands still subject to DS01 enforcement.**

**What's enforced:**
- ✓ Resource limits (CPU, memory, GPU)
- ✓ Systemd cgroup placement (`ds01-<group>-<user>.slice`)
- ✓ GPU allocation tracking
- ✓ Container labeling (DS01_USER, DS01_MANAGED)

**What's not enforced:**
- ✗ Interactive wizards/menus
- ✗ Automatic workspace mounting (you configure it)
- ✗ Project metadata tracking

**You get:**
- Full Docker flexibility
- DS01 resource fairness
- Standard Docker commands

---

## Contents

### Core Guides

- **[Docker Direct](docker-direct.md)** - Using Docker commands directly
- **[Terminal Workflows](terminal-workflows.md)** - CLI-native development patterns
- **[Batch Jobs](batch-jobs.md)** - Non-interactive job submission

### Optimization

- **[Dockerfile Best Practices](dockerfile-best-practices.md)** - Build optimization
- **[SSH Advanced](ssh-advanced.md)** - Remote access efficiency

### Specialized

- **[Multi-MIG Training](multi-mig-training.md)** - Distributed GPU training
- **[VS Code Remote](vscode-remote.md)** - Advanced VS Code setup

---

## Prerequisites

**Before diving into advanced docs:**

1. **Docker knowledge:**
   - [ ] Understand `docker run` flags
   - [ ] Familiar with `docker exec`, `docker logs`
   - [ ] Know about volumes, networks, labels

2. **Linux proficiency:**
   - [ ] Comfortable with vim/nano
   - [ ] Use tmux or screen
   - [ ] Write bash scripts confidently

3. **DS01 experience:**
   - [ ] Used DS01 for several weeks
   - [ ] Understand ephemeral model
   - [ ] Know atomic commands

**Need to level up?**
- Docker: [Official Docker Docs](https://docs.docker.com)
- Linux: [Linux Basics](../background/linux-basics.md)
- DS01: [Intermediate Guide](../intermediate/)

---

## When to Use Advanced Techniques

### Use Docker Direct When:
- DS01 commands don't cover your use case
- You need custom container configuration
- You're submitting non-interactive batch jobs
- You want industry-standard commands

### Use Terminal Workflows When:
- You work primarily via SSH
- You prefer vim/tmux over IDE
- You're on a headless server
- You want maximum efficiency

### Use Batch Jobs When:
- Training runs for days
- You don't need interactive access
- You want to submit and forget
- You're running parameter sweeps

---

## Next Steps

**Terminal-native users:**

1. [Docker Direct](docker-direct.md)
2. [Terminal Workflows](terminal-workflows.md)
3. [Batch Jobs](batch-jobs.md)

**Build optimization:**

1. [Dockerfile Best Practices](dockerfile-best-practices.md)

**Remote access:**

1. [SSH Advanced](ssh-advanced.md)
2. [VS Code Remote](vscode-remote.md)
