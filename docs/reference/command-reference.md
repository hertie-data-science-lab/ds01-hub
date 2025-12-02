# Command Reference

Complete reference for all DS01 commands with examples and options.

---

## Quick Index

**Container Lifecycle:**
- [container-deploy](#container-deploy) - Create and start container (L3)
- [container-retire](#container-retire) - Stop and remove container (L3)
- [container-create](#container-create) - Create container only (L2)
- [container-start](#container-start) - Start container in background (L2)
- [container-run](#container-run) - Start and enter container (L2)
- [container-stop](#container-stop) - Stop container (L2)
- [container-remove](#container-remove) - Remove container (L2)
- [container-list](#container-list) - List containers (L2)
- [container-stats](#container-stats) - Resource usage (L2)
- [container-exit](#container-exit) - Exit container (L2)

**Image Management:**
- [image-create](#image-create) - Build custom image (L2)
- [image-list](#image-list) - List images (L2)
- [image-update](#image-update) - Rebuild image (L2)
- [image-delete](#image-delete) - Remove image (L2)

**Project Setup:**
- [project-init](#project-init) - Complete project initialization (L4)
- [dir-create](#dir-create) - Create workspace directory (L2)
- [git-init](#git-init) - Initialize Git repository (L2)
- [readme-create](#readme-create) - Generate README (L2)

**User Setup:**
- [user-setup](#user-setup) - Complete onboarding wizard (L4)
- [ssh-setup](#ssh-setup) - Configure SSH keys (L2)
- [vscode-setup](#vscode-setup) - Configure VSCode Remote (L2)

**System:**
- [ds01-dashboard](#ds01-dashboard) - System status dashboard

---

## Container Lifecycle Commands

### container-deploy

**Create and start a container** (L3 orchestrator)

**Syntax:**
```bash
container-deploy <project-name> [OPTIONS]
```

**Options:**
- `--open` - Create and enter terminal immediately
- `--background` - Create and start in background
- `--gpu <N>` - Request N GPUs
- `--framework <name>` - Specify framework (pytorch, tensorflow, jax)
- `--image <name>` - Use specific image
- `--guided` - Educational mode with explanations
- `--help` - Show help message

**Examples:**
```bash
# Interactive mode
container-deploy my-project

# Create and enter
container-deploy my-project --open

# Background mode
container-deploy my-project --background

# Request specific GPU count
container-deploy my-project --gpu 2

# Use specific framework
container-deploy my-project --framework pytorch --open

# Guided mode
container-deploy my-project --guided
```

**What it does:**
1. Checks resource availability
2. Runs `container-create` (allocates GPU, creates container)
3. Prompts for startup mode or uses flags
4. Runs `container-start` or `container-run` based on choice

**Equivalent to:**
```bash
container-create my-project
container-run my-project  # or container-start
```

---

### container-retire

**Stop and remove a container, free GPU** (L3 orchestrator)

**Syntax:**
```bash
container-retire <project-name> [OPTIONS]
```

**Options:**
- `--force` - Skip confirmation prompts
- `--images` - Also remove Docker image
- `--help` - Show help message

**Examples:**
```bash
# Interactive mode (with confirmations)
container-retire my-project

# Skip confirmations
container-retire my-project --force

# Also remove image
container-retire my-project --images
```

**What it does:**
1. Confirms you want to retire (unless --force)
2. Runs `container-stop` (stops container)
3. Runs `container-remove` (removes container, frees GPU)
4. Optionally removes Docker image

**Equivalent to:**
```bash
container-stop my-project
container-remove my-project
# Optionally: image-delete my-project
```

---

### container-create

**Create a container with GPU allocation** (L2 atomic)

**Syntax:**
```bash
container-create <project-name> [OPTIONS]
```

**Options:**
- `--gpu <N>` - Request N GPUs (default: 1)
- `--framework <name>` - Base framework
- `--image <name>` - Specific Docker image
- `--guided` - Educational mode
- `--help` - Show help

**Examples:**
```bash
# Create with default settings
container-create my-project

# Request multiple GPUs
container-create my-project --gpu 2

# Use specific image
container-create my-project --image ds01-$(whoami)/custom:latest
```

**What it does:**
1. Checks resource limits
2. Allocates GPU via `gpu_allocator.py`
3. Creates container with resource limits
4. Mounts workspace
5. Container remains in created/stopped state

**Does not:** Start the container (use `container-start` or `container-run`)

---

### container-start

**Start container in background** (L2 atomic)

**Syntax:**
```bash
container-start <project-name>
```

**Examples:**
```bash
# Start container
container-start my-project

# Check it's running
container-list
```

**What it does:**
1. Starts the container
2. Container runs in background
3. Returns immediately

**To enter running container:** Use `container-run` or `docker exec`

---

### container-run

**Start (if stopped) and enter container** (L2 atomic)

**Syntax:**
```bash
container-run <project-name>
```

**Examples:**
```bash
# Enter running or start and enter stopped container
container-run my-project

# You're now inside container
user@my-project:/workspace$
```

**What it does:**
1. If stopped: Starts container
2. Opens interactive shell inside container
3. You can exit with `exit` or Ctrl+D

**Note:** Container keeps running after you exit (unless you stop it)

---

### container-stop

**Stop a running container** (L2 atomic)

**Syntax:**
```bash
container-stop <project-name>
```

**Examples:**
```bash
# Stop container
container-stop my-project

# Container stopped but not removed
# GPU held for configured duration (gpu_hold_after_stop)
```

**What it does:**
1. Stops container gracefully (SIGTERM)
2. GPU marked as stopped (timer starts)
3. Container still exists (can restart)

**To free GPU immediately:** Use `container-retire` instead

---

### container-remove

**Remove container and free GPU** (L2 atomic)

**Syntax:**
```bash
container-remove <project-name> [--force]
```

**Options:**
- `--force` - Remove even if running

**Examples:**
```bash
# Remove stopped container
container-remove my-project

# Force remove running container
container-remove my-project --force
```

**What it does:**
1. Removes container
2. Frees GPU immediately
3. Workspace files remain safe

**Warning:** Cannot be undone (but easy to recreate from image)

---

### container-list

**List your containers** (L2 atomic)

**Syntax:**
```bash
container-list [OPTIONS]
```

**Options:**
- `--all` - Include stopped containers (default: running only)

**Examples:**
```bash
# List running containers
container-list

# List all (including stopped)
container-list --all

# Example output:
# NAME                STATUS      GPU     UPTIME
# my-project         Running     0:1     2h 34m
# experiment-1       Running     0:2     45m
```

**What it shows:**
- Container names
- Status (Running, Stopped)
- Allocated GPU
- Uptime

---

### container-stats

**Show resource usage** (L2 atomic)

**Syntax:**
```bash
container-stats [project-name]
```

**Examples:**
```bash
# All your containers
container-stats

# Specific container
container-stats my-project

# Example output:
# CONTAINER      CPU %   MEM USAGE/LIMIT     MEM %   GPU MEM
# my-project     245%    12.5GB / 64GB      19.5%   18.2GB
```

**What it shows:**
- CPU usage (% across all cores)
- Memory usage and limit
- Memory percentage
- GPU memory usage (if available)

---

## Image Management Commands

### image-create

**Build custom Docker image** (L2 atomic)

**Syntax:**
```bash
image-create [project-name] [OPTIONS]
```

**Options:**
- `--framework <name>` - Base framework (pytorch, tensorflow, jax)
- `--guided` - Educational mode
- `--help` - Show help

**Examples:**
```bash
# Interactive mode
image-create

# Specify project and framework
image-create my-project --framework pytorch
```

**What it does:**
1. **Phase 1:** Choose base framework (PyTorch, TensorFlow, JAX)
2. **Phase 2:** Add Jupyter Lab and extensions
3. **Phase 3:** Add data science packages
4. **Phase 4:** Add custom packages (optional)
5. Builds image and tags as `ds01-<user>/<project>:latest`

**Time:** 5-15 minutes (first build), faster with cached layers

---

### image-list

**List your Docker images** (L2 atomic)

**Syntax:**
```bash
image-list [OPTIONS]
```

**Options:**
- `--all` - Include system images (default: user images only)

**Examples:**
```bash
# List your images
image-list

# Example output:
# REPOSITORY              TAG      SIZE     CREATED
# ds01-alice/my-project   latest   8.2GB    2 days ago
# ds01-alice/experiment   latest   7.9GB    1 week ago
```

---

### image-update

**Rebuild existing image** (L2 atomic)

**Syntax:**
```bash
image-update <project-name> [OPTIONS]
```

**Options:**
- `--no-cache` - Force rebuild without cache
- `--help` - Show help

**Examples:**
```bash
# Rebuild image
image-update my-project

# Force complete rebuild
image-update my-project --no-cache
```

**What it does:**
1. Finds existing Dockerfile (`~/dockerfiles/<project>.Dockerfile`)
2. Rebuilds image with same name
3. Uses layer cache for speed (unless --no-cache)

**When to use:**
- Added packages to Dockerfile
- Updated base image
- Fixed image issues

---

### image-delete

**Remove Docker image** (L2 atomic)

**Syntax:**
```bash
image-delete <project-name> [OPTIONS]
```

**Options:**
- `--force` - Delete even if containers exist
- `--help` - Show help

**Examples:**
```bash
# Delete image
image-delete my-project

# Force delete
image-delete my-project --force
```

**Warning:** Containers using this image must be removed first (or use --force)

---

## Project Setup Commands

### project-init

**Complete project initialization** (L4 wizard)

**Syntax:**
```bash
project-init [project-name] [OPTIONS]
```

**Options:**
- `--guided` - Educational mode
- `--help` - Show help

**Examples:**
```bash
# Interactive mode
project-init

# Specify project name
project-init my-research
```

**What it does:**
1. `dir-create` - Creates `~/workspace/<project>/`
2. `git-init` - Initializes Git repository
3. `readme-create` - Generates README.md
4. `image-create` - Builds custom Docker image
5. `container-deploy` - Deploys first container

**Equivalent to running all those commands individually**

---

### dir-create

**Create workspace directory** (L2 atomic)

**Syntax:**
```bash
dir-create <project-name>
```

**Examples:**
```bash
# Create project directory
dir-create my-project

# Created: ~/workspace/my-project/
```

---

### git-init

**Initialize Git repository** (L2 atomic)

**Syntax:**
```bash
git-init <project-name>
```

**Examples:**
```bash
# Initialize Git in workspace
git-init my-project

# Creates ~/workspace/my-project/.git/
# Adds .gitignore for Python/data science
```

---

### readme-create

**Generate README.md** (L2 atomic)

**Syntax:**
```bash
readme-create <project-name>
```

**Examples:**
```bash
# Create README
readme-create my-project

# Generates ~/workspace/my-project/README.md
# with project template
```

---

## User Setup Commands

### user-setup

**Complete onboarding wizard** (L4 wizard)

**Syntax:**
```bash
user-setup
```

**Aliases:** `user setup`, `new-user`

**Examples:**
```bash
# Run onboarding
user-setup
```

**What it does:**
1. `ssh-setup` - Creates SSH keys
2. `project-init` - Initializes first project
3. `vscode-setup` - Configures VSCode Remote (optional)

**Time:** 15-20 minutes

**See:** [First-Time Setup Guide](../getting-started/first-time-setup.md)

---

### ssh-setup

**Configure SSH keys** (L2 atomic)

**Syntax:**
```bash
ssh-setup [OPTIONS]
```

**Options:**
- `--key-type <type>` - Key type (default: ed25519)
- `--no-passphrase` - Create without passphrase
- `--help` - Show help

**Examples:**
```bash
# Interactive setup
ssh-setup

# Non-interactive
ssh-setup --key-type ed25519 --no-passphrase
```

**What it does:**
1. Generates SSH key pair
2. Displays public key (add to GitHub/GitLab)
3. Configures SSH agent (optional)

---

### vscode-setup

**Configure VSCode Remote** (L2 atomic)

**Syntax:**
```bash
vscode-setup [OPTIONS]
```

**Examples:**
```bash
# Interactive setup
vscode-setup

# Generates VSCode config for remote development
```

**See:** [VSCode Remote Guide](../advanced/vscode-remote.md)

---

## System Commands

### ds01-dashboard

**System status dashboard**

**Syntax:**
```bash
ds01-dashboard [OPTIONS]
```

**Options:**
- `--watch` - Continuous monitoring
- `--json` - JSON output
- `--help` - Show help

**Examples:**
```bash
# View system status
ds01-dashboard

# Continuous monitoring
ds01-dashboard --watch
```

**What it shows:**
- GPU availability and allocation
- System resource usage
- Active containers
- User quotas

---

## Common Patterns

### Complete Workflow

```bash
# First time setup
user-setup

# Daily workflow
container-deploy my-project --open
# Work...
exit
container-retire my-project

# Build custom environment
image-create my-project
container-deploy my-project --open

# Multiple containers (parallel experiments)
container-deploy exp-1 --background
container-deploy exp-2 --background
container-deploy exp-3 --background

# Clean up
container-retire exp-1
container-retire exp-2
container-retire exp-3
```

### Debugging

```bash
# Check container status
container-list
container-stats my-project

# View logs
docker logs my-project._.$(whoami)

# Enter container
container-run my-project

# Check GPU
nvidia-smi
```

---

## Getting Help

### Command Help

All commands support `--help`:
```bash
container-deploy --help
image-create --help
```

### Guided Mode

Most commands support `--guided`:
```bash
container-deploy my-project --guided
image-create --guided
```

**Guided mode:**
- Explains each step
- Educational prompts
- Recommended for beginners

---

## Environment Variables

### DS01 Variables

```bash
# Your resource limits file
DS01_LIMITS_FILE=~/.ds01-limits

# System installation
DS01_INSTALL_DIR=/opt/ds01-infra

# Workspace base
DS01_WORKSPACE=~/workspace
```

### Docker Variables

```bash
# Docker socket
DOCKER_HOST=unix:///var/run/docker.sock

# Default image registry
DOCKER_REGISTRY=<internal-registry>
```

---

## Exit Codes

**Standard exit codes:**
- `0` - Success
- `1` - General error
- `2` - Misuse of command (invalid arguments)
- `3` - Resource unavailable (no GPUs, quota exceeded)
- `4` - Container/image not found
- `5` - Permission denied

**Example:**
```bash
container-deploy my-project
echo $?  # Check exit code
```

---

## Tips & Tricks

### Tab Completion

Commands support tab completion:
```bash
container-de<Tab>     # Completes to: container-deploy
container-deploy my-<Tab>  # Completes project name (if exists)
```

### Command History

```bash
# Search history
Ctrl+R
# Type: container-deploy

# Recall last container-deploy command
!container-deploy
```

### Aliases

Create shortcuts in `~/.bashrc`:
```bash
alias cdeploy='container-deploy'
alias cretire='container-retire'
alias clist='container-list'
```

---

## Next Steps

### Learn Workflows

**Daily patterns:**
→ [Daily Usage Patterns](../guides/daily-workflow.md)

**Project setup:**
→ [Creating Projects](../guides/creating-projects.md)

**Container management:**
→ [Managing Containers](../guides/daily-workflow.md)

### Troubleshooting

**Common issues:**
→ [Troubleshooting Guide](troubleshooting.md)

**Best practices:**
→ [Best Practices](../advanced/best-practices.md)

---

## Summary

**Most Common Commands:**
```bash
# Container lifecycle
container-deploy <project> --open   # Create + start + enter
container-retire <project>          # Stop + remove + free GPU
container-list                      # View containers
container-stats                     # Resource usage

# Image management
image-create                        # Build custom image
image-update <project>              # Rebuild image

# System
ds01-dashboard                      # System status
<command> --help                    # Get help
<command> --guided                  # Educational mode
```

**Complete reference for all DS01 commands with examples!**

**Need examples?** → [Daily Usage Patterns](../guides/daily-workflow.md)

**Having issues?** → [Troubleshooting](troubleshooting.md)
