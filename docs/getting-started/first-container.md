# First Container

Deploy your first container in 5 minutes.

---

## Quick Start

```bash
# 1. First-time setup (run once)
user-setup

# 2. Deploy container
container-deploy my-project --open

# 3. You're now inside the container
# Work in /workspace - files here are persistent

# 4. When done
exit
container-retire my-project
```

That's it. Your files in `/workspace` are always saved.

---

## Step by Step

### Step 1: First-Time Setup (Once)

If this is your first time on DS01:

```bash
user-setup
```

This wizard:
- Creates SSH keys (for GitHub)
- Sets up your first workspace
- Builds a custom image
- Deploys your first container

**Time:** 15-20 minutes

### Step 2: Deploy Container

```bash
container-deploy my-project --open
```

This:
- Allocates a GPU for you
- Creates a container with PyTorch/TensorFlow
- Enters the container terminal

### Step 3: Work Inside Container

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

### Step 4: Exit and Retire

When done for the day:

```bash
# Exit container
exit

# Free GPU for others
container-retire my-project
```

---

## Daily Workflow

After initial setup, your daily pattern is:

```bash
# Morning
container-deploy my-project --open

# Work...

# Evening
exit
container-retire my-project
```

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

## Want to Learn More?

**Understand why:**
- [Containers & Docker](../background/containers-and-docker.md)
- [Ephemeral Philosophy](../background/ephemeral-philosophy.md)

**Do more:**
- [Daily Workflow](../guides/daily-workflow.md)
- [Custom Images](../guides/custom-images.md)

---

## Troubleshooting

### "No GPUs available"
```bash
ds01-dashboard      # Check availability
container-retire old-project  # Free your old containers
```

### "Container not found"
```bash
container-list      # Check what's running
container-deploy my-project  # Recreate
```

### Commands not found
```bash
shell-setup
source ~/.bashrc
```

---

## Next Steps

→ [Daily Workflow Guide](../guides/daily-workflow.md)
→ [Custom Images Guide](../guides/custom-images.md)
→ [Quick Reference](../quick-reference.md)
