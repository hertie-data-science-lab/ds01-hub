# GPU Container Guide

This guide explains how GPU access works in DS01 and what to expect when running containers with GPU.

## Quick Summary

| Container Type | GPU? | Lifecycle |
|---------------|------|-----------|
| Dev container (no GPU) | No | **Permanent** - runs until you stop it |
| Dev container (with GPU) | Yes | **Ephemeral** - auto-stops when idle |
| ds01 container | Yes | **Ephemeral** - dedicated, auto-cleanup |
| docker-compose (with GPU) | Yes | **Ephemeral** - auto-stops when idle |
| docker run (with GPU) | Yes | **Ephemeral** - auto-stops when idle |

## The Golden Rule

**GPU access = ephemeral container**

If your container has GPU access, it WILL be stopped when:
- GPU is idle for 30 minutes (no GPU activity)
- Container exceeds its maximum runtime (varies by container type)

This ensures GPUs are available for all users and aren't hoarded by idle containers.

## Container Lifecycle by Type

### DS01 Native Containers (Recommended)

Created via `container deploy`:
- **Idle timeout**: 30 minutes (configurable by group)
- **Max runtime**: 24-72 hours (varies by user group)
- **Best for**: Training runs, batch jobs, GPU-intensive work

```bash
# Deploy a GPU container
container deploy myproject

# When done
container retire myproject
```

### Dev Containers (VS Code/Cursor)

Containers created by VS Code Remote Containers extension.

**With GPU (`--gpus` in devcontainer.json):**
- **Idle timeout**: 30 minutes
- **Max runtime**: 7 days
- **Lifecycle**: Ephemeral - will be auto-stopped

**Without GPU:**
- **Idle timeout**: None
- **Max runtime**: None
- **Lifecycle**: Permanent - runs until you stop it

### Docker Compose Containers

**With GPU:**
- **Idle timeout**: 30 minutes
- **Max runtime**: 3 days
- **Lifecycle**: Ephemeral

### Direct docker run

**With GPU:**
- **Idle timeout**: 30 minutes
- **Max runtime**: 2 days
- **Lifecycle**: Ephemeral

## Recommendations

### For Code Editing (No GPU Needed)

Use a dev container WITHOUT GPU:
- Remove `--gpus` from your `devcontainer.json`
- Container can run indefinitely
- Perfect for: editing, git operations, lightweight work

Example `devcontainer.json` for permanent dev environment:
```json
{
  "name": "My Project",
  "image": "python:3.11",
  "postCreateCommand": "pip install -r requirements.txt"
  // Note: No "runArgs": ["--gpus", "all"]
}
```

### For GPU Work

Use ds01 ephemeral containers for best experience:

```bash
# Launch GPU container for training
container deploy training-run

# Do your training/inference
# ...

# When done, release GPU for others
container retire training-run
```

### Data Safety

**Always mount volumes for important data:**

- Your home directory is automatically mounted at `/home/yourusername/`
- Work in your home directory to persist files
- Container contents outside mounted volumes are lost on stop

**Safe locations** (persist across container restarts):
- `/home/yourusername/` (your home directory)
- `/workspace/` (if using ds01 containers)

**Unsafe locations** (lost on container stop):
- `/tmp/`
- `/root/`
- Any path not mounted from host

## GPU Allocation

When you request a GPU container (via any method), DS01:

1. **Checks your quota** - You have a maximum number of GPUs based on your group
2. **Allocates a specific GPU** - You get a dedicated MIG instance, not "all GPUs"
3. **Tracks your container** - For quota enforcement and cleanup
4. **Enforces limits** - Idle timeout and max runtime

### If No GPU Available

If all GPUs are allocated:
- The system waits up to 3 minutes for one to become available
- If timeout is reached, container creation fails with a helpful message

```
GPU allocation failed after 3 minutes.

Suggestions:
  1. Stop an idle container: container stop <name>
  2. Wait for system cleanup (runs every 30 min)
  3. Check GPU status: gpu-status
```

### Checking GPU Status

```bash
# See current GPU allocations
gpu-status

# See your containers
docker ps

# See your GPU usage
container ls
```

## FAQ

### Q: My dev container keeps getting stopped

**A:** Your container has GPU access, which makes it ephemeral. Options:
1. Remove GPU access if you don't need it (edit `devcontainer.json`)
2. Keep your GPU active (training running)
3. Use ds01 containers for GPU work, dev containers for editing

### Q: How do I prevent idle timeout?

**A:** Keep your GPU active:
- Running training/inference
- Active CUDA processes

For ds01 containers, you can also:
```bash
# Create keep-alive file (prevents idle timeout)
touch /workspace/.keep-alive
```

### Q: Can I have multiple GPU containers?

**A:** Yes, up to your group limit:
- **Students**: 1-2 MIG instances total
- **Researchers/Faculty**: 2+ MIG instances (varies)
- **Admins**: Unlimited

### Q: What happens to my work when container stops?

**A:**
- **Persisted**: Files in `/home/yourusername/`, `/workspace/`
- **Lost**: Files elsewhere, running processes, container state

### Q: Why was my --gpus all rewritten?

**A:** DS01 allocates you a specific GPU/MIG instance instead of "all GPUs":
- Ensures fair resource sharing
- Enables quota tracking
- Prevents GPU hoarding

Your container still has full GPU access - just to your allocated device.

## Architecture Overview

```
                Container Creation
                       |
         +-------------+-------------+
         |                           |
    CLI-based                    API-based
    (docker run,                 (bypasses
     compose, etc.)               wrapper)
         |                           |
         v                           |
+------------------+                 |
| docker-wrapper   |                 |
| - Allocate GPU   |                 |
| - Inject labels  |                 |
| - Rewrite --gpus |                 |
+--------+---------+                 |
         |                           |
         +-------------+-------------+
                       |
                       v
              Docker Daemon
                       |
                       v
        +-----------------------------+
        | container-owner-tracker     |
        | - Track ALL containers      |
        | - Detect GPU usage          |
        | - Flag unmanaged containers |
        +-----------------------------+
                       |
                       v
        +-----------------------------+
        | Lifecycle Enforcement       |
        | - Idle timeout (cron)       |
        | - Max runtime (cron)        |
        | - Applies to ALL GPU        |
        |   containers                |
        +-----------------------------+
```

## Summary

1. **GPU access = ephemeral** - GPU containers will be auto-stopped when idle
2. **No GPU = permanent** - Non-GPU containers can run indefinitely
3. **Save work to mounted volumes** - Home directory always persists
4. **Use ds01 containers for GPU work** - Best experience and quota tracking
5. **Use dev containers for editing** - Without GPU for permanent workspace
