# Daily Workflow

Your standard routine for working with DS01.

**Summary:** Launch → Work → Retire

---

## The Standard Day

### Morning: Start Working

```bash
# Launch your project
project launch my-thesis --open
```

**What this does:**
- Checks if image exists (builds if needed)
- Creates a container
- Allocates GPU
- Opens terminal inside container

**Time:** ~10 seconds (if image already built)

**Already have a container running?** Use `container-attach`:
```bash
container list           # See what's running
container-attach my-thesis
```

---

### During the Day: Work

You're now inside the container:

```bash
user@my-thesis:/workspace$
```

**Your workspace:**
```bash
# Navigate to workspace (already there by default)
cd /workspace

# Pull latest code
git pull

# Work on your code
vim train.py
# or: nano, emacs, etc.

# Run experiments
python train.py

# Or start Jupyter
jupyter lab --ip=0.0.0.0
```

**Important:** Save everything to `/workspace` - this is your persistent storage.

---

### Evening: Done for the Day

```bash
# Make sure work is committed
git status
git add .
git commit -m "Today's progress"
git push

# Exit container
exit

# Free GPU for others
container retire my-thesis
```

**What happens:**
- Container stops and is removed
- GPU freed immediately
- **Your files in `~/workspace/my-thesis/` are safe**

---

## Alternative Workflows

### Quick Experiment (30 min - 2 hours)

```bash
# Deploy for quick test
container deploy experiment --open

# Run your test
python quick_test.py

# Save results if good
cp results.csv /workspace/results/

# Done
exit
container retire experiment
```

#### Workspace Mounting with `container deploy`

The `/workspace` path inside your container depends on how you launch:

| Command | `/workspace` maps to |
|---------|---------------------|
| `project launch my-proj` | `~/workspace/my-proj/` |
| `container deploy my-proj --project=my-proj` | `~/workspace/my-proj/` |
| `container deploy my-proj` (no flags) | `~/workspace/` (root) |
| `container deploy my-proj --workspace=~/custom/path` | `~/custom/path/` |

**Recommendation:** Use `project launch` or `--project=NAME` to keep each container's workspace isolated to its project directory.

---

### Long-Running Training (Overnight)

```bash
# Deploy in background
project launch training --background

# Attach to container
container-attach training

# Start training with nohup (survives disconnect)
nohup python train.py > /workspace/logs/training.log 2>&1 &

# Check it started
tail -f /workspace/logs/training.log
# Press Ctrl+C to stop watching

# Exit (training continues)
exit

# Later: Check progress
container-attach training
tail /workspace/logs/training.log

# Or monitor from outside
docker logs training._.$(id -u) --tail 50

# Training done? Retire
container-attach training
# Verify results, commit code
exit
container retire training
```

**Prevent auto-stop for long jobs:**
```bash
# Inside container, create keep-alive file
touch ~/.keep-alive
```

This prevents idle timeout - container stays running even without CPU activity.

---

### Multiple Projects Same Day

```bash
# Morning: Project A
project launch project-a --open
# Work...
exit

# Afternoon: Switch to Project B
container retire project-a      # Free GPU
project launch project-b --open
# Work...
exit

# Evening: Cleanup
container retire project-b
```

**Check your limits:**
```bash
check-limits
# Shows max containers you can run simultaneously
```

If within limits, you can run multiple containers at once (each gets a GPU).

---

### Interactive Development with Jupyter

```bash
# Deploy container
project launch analysis --open

# Start Jupyter
cd /workspace
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# On your laptop: Create SSH tunnel
ssh -L 8888:localhost:8888 user@ds01-server

# Open browser: http://localhost:8888
# Work in notebooks...

# Done: Ctrl+C to stop Jupyter
exit
container retire analysis
```

→ [Full Jupyter setup guide](../guides/jupyter-notebooks.md)

---

### VS Code Remote Development

```bash
# Deploy in background
project launch my-thesis --background

# In VS Code on your laptop:
# 1. Open Remote-SSH extension
# 2. Connect to DS01
# 3. Attach to running container
# 4. Start coding!

# End of day
container retire my-thesis
```

→ [VS Code remote guide](../guides/vscode-remote.md)

---

## Checking Status

### See Your Containers

```bash
container list
```

Shows:
- Container name
- Status (running/stopped)
- GPU allocated
- Runtime
- Created date

### Check System Availability

```bash
# System overview
dashboard

# Detailed GPU info
dashboard gpu

# Your resource limits
check-limits
```

### Monitor Resource Usage

```bash
# Inside container: GPU usage
nvidia-smi

# Continuous monitoring
watch -n 1 nvidia-smi

# Outside container: All containers
container-stats
```

---

## Common Tasks

### Reconnect to Running Container

```bash
# List running containers
container list

# Attach to one
container-attach my-thesis
```

**Note:** `container-attach` for **running** containers. Use `project launch` if container doesn't exist.

### Update Your Environment

```bash
# Edit Dockerfile
vim ~/workspace/my-thesis/Dockerfile

# Add packages, e.g.:
# RUN pip install transformers datasets

# Rebuild image
image-update my-thesis

# Recreate container with new image
container retire my-thesis
project launch my-thesis --open
```

→ [Custom environments guide](../guides/custom-environments.md)

### Save Package Installations (Quick Method)

```bash
# Inside container: Install packages
pip install some-package

# Exit
exit

# Save to image (without editing Dockerfile)
container retire my-thesis --save-packages

# Next deploy will include the package
project launch my-thesis
```

**Trade-off:** Quick but not version-controlled. For reproducibility, edit Dockerfile instead.

---

## Time-Saving Tips

### Aliases

Add to `~/.bashrc` on DS01:

```bash
# Quick commands
alias pl='project launch'
alias cr='container retire'
alias ca='container-attach'
alias cl='container list'

# Navigation
alias ws='cd ~/workspace'

# Git
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
```

Reload: `source ~/.bashrc`

Usage:
```bash
pl my-thesis --open      # Instead of: project launch my-thesis --open
cr my-thesis             # Instead of: container retire my-thesis
```

---

### Background Startup

```bash
# Start container in background
project launch my-thesis --background &

# Do something else for 10 seconds...

# Attach when ready
container-attach my-thesis
```

Container is already running when you attach - saves time.

---

### tmux for Persistent Sessions

```bash
# Inside container: Start tmux
tmux new -s work

# Run long command
python train.py

# Detach: Press Ctrl+B, then D

# Exit container (training continues)
exit

# Later: Reattach
container-attach my-thesis
tmux attach -t work
```

**Survives SSH disconnects!** Your training keeps running even if you lose connection.

---

## Daily Checklist

**Morning:**
- [ ] `project launch` your project
- [ ] `git pull` latest code
- [ ] Check GPU available: `nvidia-smi`

**During Work:**
- [ ] Save files to `/workspace`
- [ ] Commit code at logical points
- [ ] Monitor resources if training: `nvidia-smi`

**Evening:**
- [ ] `git status` - commit any changes
- [ ] `git push` - backup to remote
- [ ] `exit` container
- [ ] `container retire` - free GPU

---

## Troubleshooting

### "No GPUs available"

```bash
# Check availability
dashboard

# See who's using GPUs
dashboard gpu

# Join queue
gpu-queue join

# Or work on something else
project launch other-project --cpu-only
```

### "Container not found"

Container was removed (expected after `container retire`). Just launch again:

```bash
project launch my-thesis --open
```

Your workspace files are safe - container recreates from image.

### "Files disappeared"

**Did you save to `/workspace`?**

```bash
# Inside container - files here are TEMPORARY
/tmp/myfile.txt              # LOST on retire
~/myfile.txt                 # LOST on retire

# Files here are PERMANENT
/workspace/myfile.txt        # SAFE
```

Only `/workspace` is mounted from host - everything else is ephemeral.

**Recovery:** Check host workspace:
```bash
# On DS01 host (outside container)
ls ~/workspace/my-thesis/
```

---

## Understanding the Workflow

**Why launch → retire instead of keeping containers running?**

**Efficiency:**
- Containers idle >2 hours auto-stop (configurable)
- GPUs freed immediately for others
- No stale allocations

**Cloud-native skills:**
- AWS/GCP/Kubernetes work this way
- Ephemeral compute is industry standard
- Stateless containers, persistent storage

**Simplicity:**
- Clear state: running or removed
- No "stopped but holding GPU" limbo
- Easy to reason about

→ [Learn more about ephemeral containers](../concepts/ephemeral-containers.md)

---

## Next Steps

**Create more projects:** → [Creating Projects](../guides/creating-projects.md)

**Customize environments:** → [Custom Environments](../guides/custom-environments.md)

**Set up Jupyter:** → [Jupyter Setup](../guides/jupyter-notebooks.md)

**Advanced techniques:** → [Long-Running Jobs](../guides/long-running-jobs.md)

**Understand concepts:** → [Concepts](../concepts/)
