# Daily Workflow

Your typical routine for working with DS01 containers.

---

## The Core Pattern

```bash
# Start your work session
project launch my-project --open

# ... do your work in the container ...

# End your session
exit
container retire my-project
```

That's it. Two commands to start, two to finish.

---

## Starting Your Session

### Option 1: project launch (Recommended)

```bash
project launch my-project --open
```

**Smart:** Checks if image exists, offers to build if needed, then launches.

### Option 2: container deploy (Direct)

```bash
container deploy my-project --open
```

**Direct:** Requires image to already exist.

**Difference:** Use `project launch` if you're not sure whether the image exists.

---

## Working in Your Container

Once inside your container:

```bash
# You're at /workspace - your project files
cd /workspace

# Run Python scripts
python train.py

# Start Jupyter
jlab

# Use Git normally
git status
git commit -m "progress"
```

**Your files are at `/workspace`** - this maps to `~/workspace/my-project/` on the host.

---

## Ending Your Session

### Exit the container

```bash
exit
# or press Ctrl+D
```

The container keeps running in the background.

### Choose what to do next

**Keep running** (default): Container stays active, GPU allocated
```bash
# Reconnect anytime
container-attach my-project
```

**Retire** (recommended when done): Frees GPU for others
```bash
container retire my-project
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start working | `project launch my-project --open` |
| Exit container | `exit` or Ctrl+D |
| Reconnect | `container-attach my-project` |
| Done for the day | `container retire my-project` |
| Check running containers | `container-list` |
| Check resource usage | `container-stats` |

---

## Tips

### Save work frequently
Files in `/workspace` persist. Container changes (pip installs) don't.

### Add packages permanently
```bash
image-update my-project --add "wandb optuna"
container retire my-project
project launch my-project --open
```

### Background mode
```bash
project launch my-project --background
# Access via VS Code Remote or container-attach
```

---

## Next Steps

- [Launching Containers](launching-containers.md) - Detailed command comparison
- [Long-Running Jobs](long-running-jobs.md) - Multi-day training
- [Custom Images](custom-images.md) - Adding packages permanently
