# Quick Reference

One-page cheat sheet for DS01 commands.

---

## Daily Workflow

```bash
# Morning: Start working
container-deploy my-project --open

# Evening: Done for the day
exit
container-retire my-project
```

---

## Container Commands

```bash
# Create + start (recommended)
container-deploy my-project --open      # Create and enter
container-deploy my-project --background # Start in background

# Stop + remove (free GPU)
container-retire my-project

# Status
container-list                          # Your containers
container-stats                         # Resource usage

# Individual steps
container-create my-project             # Create only
container-start my-project              # Start background
container-run my-project                # Start and enter
container-attach my-project             # Attach to running
container-stop my-project               # Stop only
container-remove my-project             # Remove only
```

---

## Image Commands

```bash
# Build custom image
image-create my-project

# Manage images
image-list                              # Your images
image-update my-project                 # Rebuild
image-install my-project pandas numpy   # Add packages
image-delete my-project                 # Remove
```

---

## Project Setup

```bash
# Complete wizard
project-init my-project

# Individual steps
dir-create my-project                   # Create directory
git-init my-project                     # Initialize git
readme-create my-project                # Generate README
```

---

## System Status

```bash
dashboard                               # System overview (or: ds01-dashboard)
check-limits                            # Your quotas
help                                    # List all commands
version                                 # Show version
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
/workspace/                             # Your persistent files
```

---

## File Locations

```
Host                          Container
----                          ---------
~/workspace/my-project/   →   /workspace/
~/dockerfiles/            →   (build context)
```

---

## Getting Help

Every command supports 4 help modes:

```bash
<command> --help        # Quick reference (usage, main options)
<command> --info        # Full reference (all options, examples)
<command> --concepts    # Pre-run education (what is X?)
<command> --guided      # Interactive learning (explanations during)
```

**Examples:**
```bash
image-create --concepts   # Learn about images before creating one
container-deploy --info   # See all deploy options
container-stop --help     # Quick reminder of stop syntax
```

---

## Common Patterns

```bash
# Multiple experiments
container-deploy exp-1 --background
container-deploy exp-2 --background

# View logs
docker logs my-project._.$(whoami)

# Enter running container
container-run my-project

# Fix GPU issue
container-retire my-project
container-deploy my-project --gpu 1
```

---

## Troubleshooting

```bash
# Check status
container-list
ds01-dashboard

# View logs
docker logs my-project._.$(whoami)

# Recreate (fixes most issues)
container-retire my-project
container-deploy my-project
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

**Detailed docs:** See [Command Reference](reference/commands/) | [Troubleshooting](troubleshooting/)
