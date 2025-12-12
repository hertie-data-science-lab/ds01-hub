# First Container

Deploy your first container in <30 minutes.

---

## Quick Start

```bash
# 1. First-time setup (run once)
user-setup

# 2. Setup Project (per project)
project-init --guided

# 3a. Launch project (every login)
project launch --guided

#3b OR container-oriented workflow
image-create           # Once (then image-update for adding packages)
container-deploy my-project --open # Every login

# 3. You're now inside the container
# Work in /workspace - files here are persistent

# 4. When done
exit
container-retire my-project
```

---


## Work Inside Container

```bash
# You're now inside the container
user@my-project:/workspace$

# Check GPU is available
nvidia-smi

# Start Python
python
>>> import torch
>>> torch.cuda.is_available()
True
```

**Important:** Save files in `/workspace` - this is your persistent storage.

---

## Key Concepts

### Files

```
/workspace/              Your persistent files (always safe)
Everything else          Temporary (lost on container removal)
```

### Container States

```
container-deploy   →   Container running, GPU allocated
container-retire   →   Container removed, GPU freed
```

Your workspace files survive both states.

---

## Getting Help

Every command has built-in help:

```bash
<command> --help        # Quick reference
<command> --info        # Full reference (all options)
<command> --concepts    # Learn concepts before running
<command> --guided      # Step-by-step with explanations
```

**Example:** If you're new to images:
```bash
image-create --concepts   # Understand what images are
image-create --guided     # Create with explanations
```

--

### NB: Container Naming
- **Images**: `ds01-<user>/<project>:latest`
- **Containers**: `<project>._.<user>` (AIME convention)

---

## Bonus?

**Understand why:**
- [Containers & Docker](../background/containers-and-docker.md)
- [Ephemeral Philosophy](../background/ephemeral-philosophy.md)

**Do more:**
- [Daily Workflow](../core-guides/daily-workflow.md)
- [Custom Images](../core-guides/custom-images.md)

---

## Troubleshooting

### "No GPUs available/Resource limits reached"
```bash
ds01-dashboard      # Check availability
container-retire old-project  # Free your old containers
```

### "Container not found"
```bash
container-list          # Check what's running
container-list --all    # Check all containers (incl those not in running state - advanced)
container-deploy my-project  # Recreate
```

### Commands not found
```bash
shell-setup
source ~/.bashrc
```

---

## Next Steps

- → [Daily Workflow Guide](../core-guides/daily-workflow.md)
- → [Custom Images Guide](../core-guides/custom-images.md)
- → [Quick Reference](../quick-reference.md)
