# Command Quick Reference

One-page cheat sheet for DS01 commands.

---

## Typical Workflow

```bash
# Spin up container for GPU work
project launch my-project --open

# Reconnect if disconnected
container-attach my-project

# Done with GPU work
exit
container retire my-project
```

---

## First-Time Setup

```bash
# Complete onboarding (run once)
user-setup

# Create new project
project init my-thesis

# See all available commands
commands
```

---

## Project Management

```bash
# Create new project
project init <name>
project init <name> --type=cv
project init --guided

# Launch project
project launch <name>
project launch <name> --open
project launch <name> --background
project launch              # Interactive

# List projects
ls ~/workspace/
```

---

## Container Commands

### Daily Commands (L3 Orchestrators)

```bash
# Deploy container (create + start)
container deploy <name>
container deploy <name> --open
container deploy             # Interactive

# Retire container (stop + remove + free GPU)
container retire <name>
container retire <name> --force
container retire             # Interactive

# Connect to running container
container-attach <name>
container-attach             # Interactive

# List containers
container-list
container-list --all

# View resource usage
container-stats
```

### Advanced Commands (L2 Atomic)

```bash
# Granular control
container-create <name>      # Create only
container-start <name>       # Start existing
container-run <name>         # Start and enter
container-pause <name>       # Freeze processes (GPU stays allocated)
container-unpause <name>     # Resume frozen container
container-stop <name>        # Stop only
container-remove <name>      # Remove only
container-exit               # Exit gracefully
```

---

## Image Commands

```bash
# Create custom image
image-create <project>
image-create <project> --guided
image-create                 # Interactive

# Update image (interactive GUI - recommended)
image-update                  # Select image, add/remove packages

# Rebuild after manual Dockerfile edit (advanced)
image-update <project> --rebuild

# Quick install (non-reproducible)
image-install <packages>
image-install transformers datasets

# List images
image-list
image-list --all

# Delete image
image-delete <name>
```

---

## Monitoring & Status

```bash
# System dashboard
dashboard                    # Snapshot view
dashboard gpu                # GPU details
dashboard containers         # All containers
dashboard users              # Per-user breakdown
dashboard monitor            # Watch mode (1s refresh)
dashboard interfaces         # Group by interface

# Your resource limits
check-limits

# GPU queue
gpu-queue status
gpu-queue join
gpu-queue position $USER

# System health
ds01-health-check
ds01-events
ds01-events user <username>
```

---

## GPU Management

```bash
# Check GPU availability
nvidia-smi

# GPU utilisation dashboard
gpu-utilisation-monitor
mig-utilisation-monitor

# Continuous monitoring
watch -n 1 nvidia-smi
```

---

## Help System

```bash
# Quick reference
<command> --help
<command> -h

# Full reference (all options)
<command> --info

# Learn concepts first
<command> --concepts

# Interactive learning
<command> --guided

# Examples
container-deploy --help
image-create --concepts
project-init --guided
```

---

## Common Workflows

### New Project

```bash
project init my-thesis --type=cv
project launch my-thesis --open
# Work...
exit
container retire my-thesis
```

### Existing Project

```bash
project launch my-thesis --open
# Work...
exit
container retire my-thesis
```

### Quick Experiment

```bash
container deploy test --open
# Test something...
exit
container retire test
```

### Reconnect to Running Container

```bash
container-list
container-attach my-project
```

### Long-Running Job

```bash
project launch training --background
container-attach training
# Start training with nohup or tmux
exit
# Later: reconnect
container-attach training
```

---

## File Locations

```bash
# Your workspaces (persistent)
~/workspace/<project>/

# Project Dockerfiles
~/workspace/<project>/Dockerfile

# Project metadata
~/workspace/<project>/pyproject.toml

# State and logs (admin)
/var/lib/ds01/
/var/log/ds01/
```

---

## Git Commands (Reminder)

```bash
# Check status
git status

# Commit changes
git add .
git commit -m "message"
git push

# Pull updates
git pull

# View history
git log --oneline
```

---

## Jupyter Notebooks

```bash
# Inside container - Start Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# On laptop - Create SSH tunnel
ssh -L 8888:localhost:8888 ds01
# Without SSH keys: ssh -L 8888:localhost:8888 <student-id>@students.hertie-school.org@10.1.23.20

# Open browser
http://localhost:8888

# Background Jupyter with tmux
tmux new -s jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
# Ctrl+B, D to detach
```

---

## VS Code Remote

```bash
# Launch container in background
project launch my-project --background

# In VS Code:
# 1. Remote Explorer → SSH → Connect to ds01-server
# 2. Remote Explorer → Containers → Attach to container
# 3. Open /workspace/my-project
```

---

## Troubleshooting Quick Fixes

### Commands not found

```bash
/opt/ds01-infra/scripts/user/helpers/shell-setup
source ~/.bashrc
```

### No GPUs available

```bash
dashboard gpu
gpu-queue join
```

### Container not found

```bash
# Just relaunch
project launch my-project
```

### Image not found

```bash
# Build it
image-create my-project

# Or use project launch (auto-builds)
project launch my-project
```

### Container won't start

```bash
# Check logs
docker logs <container-name>._.$(id -u)

# Rebuild image (if package issue)
image-update                  # Fix packages via GUI
container retire my-project
project launch my-project
```

### Files disappeared

**Check: Did you save to `/workspace`?**

```bash
# Inside container - TEMPORARY
~/myfile.txt

# Inside container - PERMANENT
/workspace/myfile.txt
```

---

## Flags Quick Reference

### Common Flags (Most Commands)

```bash
--help, -h          Quick reference
--info              Full reference
--concepts          Learn concepts first
--guided            Interactive learning mode
```

### Container Launch Flags

```bash
--open              Create and open terminal
--background        Create but don't open
--project=<name>    Use specific project workspace
--image=<name>      Use specific Docker image
```

### Container Retire Flags

```bash
--force             Skip confirmations
--keep-image        Don't offer to remove image
```

### Project Init Flags

```bash
--type=<type>       Specify project type (ml, cv, nlp, rl, ts, llm)
--quick             Skip interactive questions
```

---

## Environment Variables

```bash
# Check container context
echo $DS01_CONTEXT

# Check orchestrator
echo $DS01_ORCHESTRATOR

# User info
whoami
id -u
```

---

## Useful Aliases

**Add to `~/.bashrc`:**

```bash
# DS01 commands
alias pl='project launch'
alias ca='container-attach'
alias cr='container retire'
alias cl='container-list'
alias dash='dashboard'

# Navigation
alias ws='cd ~/workspace'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline'

# System
alias gpu='nvidia-smi'
alias limits='check-limits'
```

**Reload:**
```bash
source ~/.bashrc
```

---

## Container Naming Convention

```bash
# Container name format
<project-name>._.{user-id}

# Example
my-thesis._.12345

# Docker commands use full name
docker ps | grep my-thesis
docker logs my-thesis._.$(id -u)
```

---

## Resource Limits

**Check your limits:**
```bash
check-limits
```

**Common limits:**
- Max GPUs per user total
- Max GPUs per container
- Max containers per user
- Max CPU/memory per container
- Idle timeout
- Max runtime

---

## Exit Codes

**Container commands:**
- `0` - Success
- `1` - Error
- `2` - Invalid arguments
- `130` - Interrupted (Ctrl+C)

**Check exit code:**
```bash
project launch my-project
echo $?
```

---

## Quick Diagnostics

```bash
# System status
dashboard

# Your limits and usage
check-limits

# Full health check
ds01-health-check

# Recent events
ds01-events | tail -20

# Container logs
docker logs <container>._.$(id -u)

# GPU status
nvidia-smi
```

---

## One-Liners

```bash
# Create, launch, open in one step
project init my-exp && project launch my-exp --open

# List all running containers with GPUs
container-list | grep running

# Check if Jupyter is running
ps aux | grep jupyter

# Find large files in workspace
du -sh ~/workspace/* | sort -h

# Count running containers
docker ps --filter "label=DS01_MANAGED=true" | wc -l

# Show your Docker images
docker images | grep $(id -u)
```

---

## Emergency Commands

```bash
# Kill all your containers (use with caution!)
docker ps -q --filter "label=DS01_USER=$(id -u)" | xargs -r docker stop

# Remove all stopped containers
docker ps -a -q --filter "label=DS01_USER=$(id -u)" | xargs -r docker rm

# Clean up Docker space
docker system prune -a
```

**Don't run these unless you know what you're doing!**

---

## Get More Help

```bash
# Show all commands
commands

# Command-specific help
<command> --help
<command> --info

# Learn a concept
<command> --concepts

# Guided walkthrough
<command> --guided

# Health check
ds01-health-check

# Documentation
ls /opt/ds01-infra/docs-user/
```

---

## Related Documentation

- → [Getting Started](../getting-started/first-time.md)

- → [Daily Workflow](../getting-started/daily-workflow.md)

- → [Creating Projects](../core-guides/creating-projects.md)

- → [Custom Environments](../core-guides/custom-environments.md)

- → [Jupyter Notebooks](../core-guides/jupyter.md)

- → [Troubleshooting](../troubleshooting/)

---

**Print this page for quick reference while learning DS01!**
