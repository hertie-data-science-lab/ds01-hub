# Quick Reference

One-page cheat sheet for DS01 commands. This covers the most common workflows; for the complete list of all available commands and options, see the [Command Reference](reference/commands/).

---

## Daily Workflow

### Project-Oriented (Recommended)

Familiar if you're used to local Python/Jupyter development.

```bash
# First time
user setup                           # Complete setup wizard

# New project
project init my-thesis --type=llm    # Create project
project launch my-thesis --open      # Start working

# Resume work
project launch my-thesis --open

# Done 
exit
```

### Container-Oriented (More Control)

Cloud-native style, closer to Docker/Kubernetes.

```bash
# Deploy container directly
container-deploy my-project --background

# Attach terminal 
container-attach my-project

# Done
container-retire my-project
```

---

## Help Commands
```bash
# List available aliases
commands                            # lists all commands

# Return to workspace 
home                                # = cd /home/<user-id>/
```

---

## Project Commands

```bash
# Create new project
project init [name]                  # Interactive if no name
project init my-project              # Named project
project init my-project --type=cv    # With template (ml/cv/nlp/rl/audio/ts/llm/custom)
project init --guided                # With explanations

# Launch project (builds image if needed)
project launch [name]                # Interactive if no name
project launch my-project            # Named project
project launch my-project --open     # Launch and enter terminal
project launch my-project --background  # Start in background
project launch my-project --rebuild  # Force image rebuild
```

---

## Container Commands

```bash
# Create + start (orchestrator)
container-deploy [name] [image]      # Interactive if no args
container-deploy my-project          # Default base image
container-deploy my-project pytorch  # Specify base image
container-deploy my-project --open   # Create and enter
container-deploy my-project --background  # Start in background
container-deploy my-project --cpu-only    # No GPU
container-deploy my-project -w /path/to/dir   # Custom workspace
container-deploy my-project --dry-run     # Show what would happen

# Stop + remove + free GPU
container-retire [name]              # Interactive if no name
container-retire my-project          # Named container (prompts to save new packages)
container-retire my-project --force  # Skip confirmation

# Status
container-list                       # Your containers
container-list --all                 # Include stopped
container-stats                      # Resource usage

# Individual steps (atomic - for advanced users)
container-create my-project          # Create container (& allocate resources)
container-start my-project           # Start in background
container-run my-project             # Start + enter
container-attach my-project          # Enter running container
container-pause my-project           # Freeze processes (GPU stays allocated)
container-unpause my-project         # Resume frozen container
container-stop my-project            # Stop only
container-remove my-project          # Remove only
```

---

## Image Commands

```bash
image-create [name]                  # Interactive wizard
image-create my-project              # Named image
image-create my-project -f pytorch   # Specify framework (pytorch, tensorflow, jax)

image-list                           # Your images
image-update                         # Interactive GUI to add/remove packages
image-update my-project --rebuild    # Rebuild after manual Dockerfile edit
image-delete my-project              # Remove image
```

---

## System Status

```bash
dashboard                    # System overview
dashboard gpu                # GPU/MIG utilisation
dashboard cpu                # CPU by user
dashboard --watch            # Live monitoring (2s refresh)
dashboard --full             # All sections expanded
check-limits                 # Your quotas and usage
```

---

## Inside Container

```bash
# Check GPU
nvidia-smi

# Python with GPU
python
>>> import torch
>>> torch.cuda.is_available()
True

# Files location
/workspace/                  # Your persistent files
```

---

## File Locations

```
Host                                   Container
----                                   ---------
~/workspace/my-project/            ->  /workspace/
~/workspace/my-project/Dockerfile      (image build source)
```

---

## Getting Help

Every command supports 4 help modes:

| Flag | Type | Purpose |
|------|------|---------|
| `--help`, `-h` | Reference | Quick reference (usage, main options) |
| `--info` | Reference | Full reference (all options, examples) |
| `--concepts` | Education | Pre-run learning (what is X?) |
| `--guided` | Education | Interactive learning (explanations during) |

**Examples:**
```bash
project init --concepts       # Learn about projects before creating one
container-deploy --info       # See all deploy options
image-create --guided         # Step-by-step with explanations
```

---

## Common Patterns

```bash
# Multiple experiments
container-deploy exp-1 --background
container-deploy exp-2 --background

# View logs
docker logs <project-name>._.$(whoami)

# Enter running container
container-attach my-project

# Recreate with fresh image
container-retire my-project
project launch my-project --rebuild
```

---

## Troubleshooting

```bash
# Check status
container-list
dashboard

# View logs
docker logs <project-name>._.$(whoami)

# Recreate (fixes most issues)
container-retire my-project
project launch my-project
```

---

## Alternative Syntax

Commands also work with spaces instead of hyphens:

```bash
container deploy my-project    # Same as container-deploy
image create my-project        # Same as image-create
project init my-project        # Same as project-init
```

See [Dispatcher Commands](reference/commands/dispatcher-commands.md) for details.

---

## Docker Commands (Advanced Users)

If you prefer working directly with Docker, these commands are still subject to DS01 resource limits and GPU allocation:

```bash
# List containers
docker ps                                # Running containers
docker ps -a                             # All containers (including stopped)

# Inspect containers
docker logs <container-id>               # View container output
docker logs -f <container-id>            # Follow logs (live)
docker inspect <container-id>            # Full container details (JSON)

# Execute commands
docker exec <container-id> ls /workspace # Run command in container
docker exec -it <container-id> bash      # Interactive shell

# Manage images
docker images                            # List images
docker build -t my-image .               # Build image from Dockerfile
docker rmi <image-id>                    # Remove image

# Resource info
docker stats                             # CPU, memory, GPU usage
docker stats --no-stream                 # Single snapshot
```

**Note:** All Docker commands run through DS01's enforcement system:
- Resource limits (CPU, memory, GPU) are enforced via cgroups
- GPU allocations are tracked and validated
- Containers are organized in DS01 systemd slices

---

**Detailed docs:** See [Command Reference](reference/commands/) | [Troubleshooting](troubleshooting/)
