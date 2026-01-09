# VS Code Dev Containers

> **Status: Experimental** - This workflow is in active development. Please report issues.

Use VS Code Dev Containers to launch DS01 GPU containers directly from your local machine.

## What are Dev Containers?

Dev containers are a VS Code feature that launches a container when you open a project folder. Instead of SSH-ing to DS01 and running `container deploy`, you:

1. Open a folder in VS Code
2. VS Code sees the `devcontainer.json` file
3. VS Code builds/starts the container and connects automatically

**Key difference from Remote-SSH:**
- **Remote-SSH**: You SSH to DS01, then start a container manually
- **Dev Containers**: VS Code handles the container lifecycle for you

## When to Use Dev Containers

| Use Case | Recommended Approach |
|----------|---------------------|
| GUI-heavy, edit-run-debug cycles | Dev Containers |
| Long-running training jobs | CLI (`container deploy`) |
| Quick SSH-based editing | Remote-SSH |
| Need terminal control | CLI (`container deploy`) |

Dev containers are ideal when you want VS Code to manage everything automatically.

## Quick Start

### 1. Prerequisites

- VS Code with [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- SSH access to DS01 configured
- Docker context set to DS01 (see Setup below)

### 2. Create Configuration

On DS01, navigate to your project and run:

```bash
# Interactive wizard
devcontainer init

# Or quick mode with defaults
devcontainer init --quick
```

This creates `.devcontainer/devcontainer.json` with DS01-optimised settings.

### 3. Open in VS Code

Locally:

1. Open the project folder in VS Code
2. VS Code prompts: "Reopen in Container" - click Yes
3. Wait for container to build and start
4. You're now working inside a DS01 GPU container

## The `devcontainer init` Command

The wizard creates devcontainer.json files optimised for DS01:

```bash
# Interactive mode (prompts for all options)
devcontainer init

# Quick mode (uses defaults)
devcontainer init --quick

# Specify framework
devcontainer init --framework=pytorch
devcontainer init --framework=tensorflow

# No GPU (for editing/git only)
devcontainer init --no-gpu

# Learn about dev containers first
devcontainer init --concepts

# Step-by-step with explanations
devcontainer init --guided
```

### Generated Configuration

The wizard generates a `devcontainer.json` like:

```json
{
  "name": "my-project",
  "image": "aime/pytorch:2.4-cuda12.4-nccl2.22-cudnn9-ubuntu22.04",
  "runArgs": ["--gpus", "all", "--shm-size", "8g"],
  "mounts": [
    "source=${localEnv:HOME},target=/home/${localEnv:USER},type=bind"
  ],
  "shutdownAction": "stopContainer"
}
```

Key settings:
- **image**: Uses same AIME base images as `container deploy`
- **runArgs**: GPU access via DS01's docker-wrapper
- **mounts**: Your home directory for persistent files
- **shutdownAction**: Auto-stops container when you close VS Code (releases GPU)

## GPU Allocation

Dev containers use the same GPU allocation system as CLI containers:

- **MIG instances** by default (shared GPU slices)
- **Full GPU** if your quota allows and you request it
- Same quotas and limits apply

### Dynamic Allocation

**Important**: The GPU is allocated **at container start time**, not when you create devcontainer.json.

```
devcontainer.json                    At container launch
─────────────────                    ───────────────────
"runArgs": ["--gpus", "all"]    →    docker-wrapper.sh intercepts
                                            │
                                            ▼
                                     gpu_allocator_v2.py
                                     "Give me an available GPU"
                                            │
                                            ▼
                                     Rewrites to: --gpus device=GPU-abc123
```

This means:
- **Each time you open VS Code**, a fresh GPU is allocated from the pool
- **Different GPU** may be assigned each time based on availability
- **Same allocation system** as `container deploy`

The `shutdownAction: "stopContainer"` setting is important - it releases your GPU when you close VS Code. Without this, your GPU stays allocated.

## Integration with project-init

When creating a new project, you can choose your workflow:

```bash
project init my-thesis --type=ml
```

At **Step 7**, you'll be asked:
```
How will you launch containers for this project?
  1) CLI (Recommended)
  2) VS Code Dev Container (experimental - in dev)
  3) Skip (decide later)
```

Choosing option 2 automatically creates `.devcontainer/devcontainer.json`.

### Adding Dev Containers to Existing Projects

For existing projects in `~/workspace/`:

```bash
# From anywhere - shows project dropdown
devcontainer init

# From within a project
cd ~/workspace/my-project
devcontainer init --quick
```

## Checking Your Configuration

Validate an existing devcontainer.json:

```bash
# Check current directory
devcontainer check

# Check specific project
devcontainer check ~/workspace/my-project

# Auto-fix issues
devcontainer check --fix
```

The checker validates:
- Base image (AIME catalog recommended)
- GPU configuration
- shutdownAction setting (critical for GPU release)
- Home directory mount (for persistence)

## Unified Container View

Dev containers appear in `container ls` alongside regular DS01 containers:

```
$ container ls

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Your Containers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. my-thesis
   Status: Running
   Image:  ds01-1000/my-thesis
   GPU:    Allocated (MIG 1g.10gb)

2. llm-finetuning (dev container)
   Status: Running
   Image:  aime/pytorch:2.4-cuda12.4
   GPU:    Allocated (MIG 1g.10gb)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 2 container(s)
```

All containers - whether created via CLI or VS Code - are subject to the same:
- Resource quotas
- Idle timeout enforcement
- GPU allocation tracking

## Setup: Docker Context

To have VS Code connect to DS01's Docker daemon:

### Option 1: SSH Context (Recommended)

```bash
# On your local machine
docker context create ds01 --docker "host=ssh://your-username@ds01.example.com"
docker context use ds01
```

Then in VS Code settings:
```json
{
  "dev.containers.dockerPath": "docker",
  "dev.containers.defaultExtensions": ["ms-python.python"]
}
```

### Option 2: TCP Socket (Advanced)

If SSH context is slow, you can use TCP:

1. On DS01, expose Docker socket (admin setup required)
2. Configure VS Code to connect via TCP

## Troubleshooting

### "Cannot connect to Docker daemon"

1. Check Docker context: `docker context show`
2. Test connection: `docker ps`
3. Verify SSH key is loaded: `ssh-add -l`

### Container won't start

1. Check GPU quota: `check-limits`
2. Verify image exists: `docker images | grep aime`
3. Check DS01 logs: `ds01-logs`

### GPU not available

1. Close other VS Code windows (releases GPUs)
2. Check allocation: `container ls --detailed`
3. Wait for GPU queue if full

### Changes not persisting

Ensure home directory mount is configured:
```json
"mounts": [
  "source=${localEnv:HOME},target=/home/${localEnv:USER},type=bind"
]
```

Files in `/home/username/workspace/` persist; files elsewhere in the container do not.

## Comparison: CLI vs Dev Containers

| Aspect | CLI (`container deploy`) | Dev Containers |
|--------|--------------------------|----------------|
| Start method | SSH + command | Open folder in VS Code |
| Lifecycle | Manual (`container retire`) | Automatic (close VS Code) |
| GPU release | Explicit command required | Auto on window close |
| Configuration | Dockerfile | devcontainer.json |
| Best for | Long jobs, tmux, scripts | Interactive editing, debugging |
| Setup effort | Per-project Dockerfile | One-time devcontainer.json |

Both use the same underlying system - same images, same GPU allocation, same quotas.

### When to Use Which

**Use CLI workflow when:**
- Running long training jobs (hours/days)
- Need multiple terminal sessions (tmux)
- Want explicit control over start/stop
- Running batch scripts
- Prefer terminal-based editing (vim, nano)

**Use Dev Containers when:**
- Interactive development with VS Code features
- Edit-run-debug cycles
- Need VS Code extensions (linting, debugging)
- Quick iterations on code
- Prefer IDE experience over terminal

## Next Steps

- [Daily Workflow](daily-workflow.md) - Regular patterns
- [GPU Usage](gpu-usage.md) - Understanding GPU allocation
- [Custom Images](custom-images.md) - Building your own images
- [VS Code Remote](vscode-remote.md) - Alternative: Remote-SSH approach
