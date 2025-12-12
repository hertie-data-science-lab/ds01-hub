# Ephemeral Containers

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

**Temporary (lost on retire):**
- Container instance, running processes, pip packages, files outside `/workspace/`, GPU allocation

**Permanent (always safe):**
- Files in `/workspace/`, Dockerfile, Docker images, Git history on host

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

---

## Common Questions

**"Will I lose work?"**
> No, if you save to `/workspace/`. That's the whole point of the workspace.

**"How long does recreating take?"**
> About 30 seconds. Image is already built.

**"What if I need a GPU for 3 days?"**
> Keep the container running. Retire when actually done.

**"What if container stops unexpectedly?"**
> Load your checkpoint and resume. Save progress frequently.

---

## Want Deeper Understanding?

This is a brief introduction to the ephemeral model. For comprehensive explanation of:
- **Why** this design (fairness, reproducibility, industry standards)
- **How** to handle long-running jobs and checkpointing
- **When** to use different strategies
- **Industry context** (AWS, Kubernetes, HPC)

See [Ephemeral Philosophy](../background/ephemeral-philosophy.md) in Educational Computing Context (20 min read).

---

## Next Steps

- [Workspaces and Persistence](workspaces-persistence.md) - Where to save files
- [Containers and Images](containers-and-images.md) - How images work
- [Long-Running Jobs](../core-guides/long-running-jobs.md) - Multi-day training
