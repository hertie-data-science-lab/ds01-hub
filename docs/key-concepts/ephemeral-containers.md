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
# Need GPU? Spin up a container
project launch my-thesis --open

# Do your compute-intensive work
# (files saved to /workspace/)

# Done? Clean up
exit
container retire my-thesis    # Frees GPU for others
```

```bash
# Need GPU again later? Spin up another container
project launch my-thesis --open
# All your files are exactly where you left them
```

**Container is new. Workspace files persist.**

---

## What's Temporary vs Permanent

### Temporary (lost on retire)

- **Container instance:** The running container itself - its process ID, network identity, mounted filesystems. Like a browser tab: close it and it's gone, but your bookmarks (workspace) remain.

- **Running processes:** Your Python script, Jupyter server, training loop - all terminate when the container stops. Any in-memory state (variables, model weights in RAM) is lost.

- **`pip install` packages:** Packages installed at runtime live only in that container's filesystem layer. The layer is discarded on removal. Put packages in your Dockerfile to make them permanent.

- **Files outside `/workspace/`:** Anything saved to `/tmp/`, `/root/`, `/home/` inside the container exists only in the container's writable layer. Container removed = files gone.

- **GPU allocation:** Your GPU reservation is released immediately when you retire. Someone else can use that GPU within seconds.

### Permanent (always safe)

- **Files in `/workspace/`:** This directory is a mount point - it's actually your host directory `~/workspace/<project>/` appearing inside the container. The container can vanish, but these files live on the host's disk.

- **Dockerfile:** Stored in your workspace (`~/workspace/<project>/Dockerfile`). It's a text file on the host, completely independent of any container.

- **Docker image:** Stored in Docker's image cache on the host. Images persist until you explicitly delete them with `image-delete` or `docker rmi`.

- **Git history:** If you've pushed to a remote (GitHub, GitLab), your code exists on external servers. Even local commits are in `~/workspace/<project>/.git/` - on the host, not in the container.

---

## Why This Design?

### 1. Resource fairness

DS01 has limited GPUs shared among many users. If containers persisted indefinitely, users who finish their work but forget to clean up would block GPUs for days. With ephemeral containers, retiring frees your GPU immediately - someone else can start training within seconds. The system stays usable for everyone.

### 2. Clean state

Every container launch gives you a fresh environment that matches your image exactly. No leftover processes from last week consuming memory. No mystery files in `/tmp/` causing disk-full errors. No half-installed packages from a failed `pip install`. When something breaks, `container retire` + `project launch` gives you a known-good state.

### 3. Industry standard

This is how production systems work:

- **AWS:** You spin up an EC2 instance, do your compute, terminate it to stop paying. Your data lives on S3 or EBS, not on the instance's ephemeral storage. Leaving instances running = burning money.

- **Kubernetes:** Pods are ephemeral by design - they can be killed and rescheduled to different nodes at any time. Persistent data goes on PersistentVolumes. Your code must handle pod restarts gracefully.

- **HPC:** You submit a job, it runs on allocated nodes, it completes, nodes are freed for the next job. Jobs don't "own" nodes permanently - that would defeat the purpose of a shared cluster.

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

*NB: DS01 applies user-specific `max_runtime` limits. You can check these at any point with the `check limits` command. Should you need more runtime that currently provided, just [raise a ticket](https://github.com/hertie-data-science-lab/ds01-hub/issues) on the ds01 hub repo (ideally in advance!).

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
project launch my-project 

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
> Raise a ticket in advance to the DSL to change your default configs. Then just keep the container running. Retire when actually done.

**"What if container stops unexpectedly?"**
> Load your checkpoint and resume. This is why checkpointing matters.

---

## Next Steps

- [Workspaces and Persistence](workspaces-persistence.md) - Where to save files
- [Containers and Images](containers-and-images.md) - How images work
- [Long-Running Jobs](../core-guides/long-running-jobs.md) - Multi-day training

**Want to understand the industry context?** See [Ephemeral Philosophy](../background/ephemeral-philosophy.md) in Educational Computing Context.
