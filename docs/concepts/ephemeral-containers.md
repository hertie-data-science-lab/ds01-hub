# Ephemeral Container Model

**Why containers are temporary, and why that's a feature.**

---

## The Core Idea

**Containers = temporary compute sessions**
**Workspaces = permanent storage**

Like shutting down your laptop when done - your files are safe on the disk.

---

## The DS01 Workflow

```bash
# Morning: Start working
project launch my-thesis --open

# During the day: Work
# (files saved to /workspace/)

# Evening: Done for the day
exit
container retire my-thesis    # Frees GPU for others
```

```bash
# Next morning: Resume
project launch my-thesis --open
# All your files are exactly where you left them
```

**Container is new. Workspace files persist.**

---

## What's Temporary vs Permanent

### Temporary (lost on retire)
- Container instance
- Running processes
- `pip install` packages (if not in Dockerfile)
- Files outside `/workspace/`
- GPU allocation

### Permanent (always safe)
- Files in `/workspace/<project>/`
- Dockerfile
- Docker image
- Git history

---

## Why This Design?

### 1. Resource fairness

DS01 has limited GPUs. If everyone leaves containers running:

```
Monday 5pm: Alice, Bob, Charlie go home (containers idle)
Tuesday 9am: Dana wants GPU - none available!
            (All "allocated" but not being used)
```

With ephemeral model:
```
Monday 5pm: Everyone retires containers
Tuesday 9am: GPUs available for anyone who needs them
```

### 2. Clean state

Every container launch:
- Fresh environment
- No stale processes
- No mysterious state from last week
- Matches your image exactly

### 3. Industry standard

This is how production systems work:
- AWS: Terminate instances to stop paying
- Kubernetes: Pods are ephemeral, volumes persist
- HPC: Jobs complete, resources freed

**You're learning cloud-native patterns.**

---

## "But What About..."

### Long-running jobs

**Containers can run for days.** The point is to remove them when actually done, not to stop them mid-work.

```bash
# Start training (runs overnight)
container-deploy training --background

# Next day: check on it
container-attach training

# When training completes: retire
container retire training
```

### Checkpointing

Save progress frequently so you can resume:

```python
# Save every N epochs
if epoch % 10 == 0:
    torch.save({
        'epoch': epoch,
        'model': model.state_dict(),
    }, '/workspace/models/checkpoint.pt')
```

If container stops unexpectedly: load checkpoint, resume.

### "I forget what packages I had"

**Your Dockerfile remembers:**
```bash
cat ~/workspace/my-project/Dockerfile
```

Everything in the image is reproducible.

---

## Quick Commands

```bash
# Deploy (create + start)
project launch my-project --open

# Retire (stop + remove + free GPU)
container retire my-project

# Check what you have running
container-list
```

---

## Mental Model

Think of it like a laptop:

| Laptop | DS01 |
|--------|------|
| Shut down when done | `container retire` |
| Files on SSD | Files in `/workspace/` |
| Boot takes 30 sec | Deploy takes 30 sec |
| Don't leave running 24/7 | Don't leave containers idle |

---

## Common Questions

**"Will I lose work?"**
> No, if you save to `/workspace/`. That's the whole point of the workspace.

**"How long does recreating take?"**
> About 30 seconds. Image is already built.

**"What if I need a GPU for 3 days?"**
> Keep the container running. Retire when actually done.

**"What if container stops unexpectedly?"**
> Load your checkpoint and resume. This is why checkpointing matters.

---

## Next Steps

- [Workspaces and Persistence](workspaces-persistence.md) - Where to save files
- [Containers and Images](containers-and-images.md) - How images work
- [Long-Running Jobs](../guides/long-running-jobs.md) - Multi-day training

**Want to understand the industry context?** See [Ephemeral Philosophy](../background/ephemeral-philosophy.md) in Educational Computing Context.
