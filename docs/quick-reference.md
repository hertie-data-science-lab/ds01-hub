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
ds01-dashboard                          # System overview
check-limits                            # Your quotas
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

## Help

```bash
<command> --help                        # Command help
<command> --guided                      # Educational mode
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

**Detailed docs:** See [Command Reference](reference/commands/) | [Troubleshooting](troubleshooting/)
