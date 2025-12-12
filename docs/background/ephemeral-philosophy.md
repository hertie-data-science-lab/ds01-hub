# Ephemeral Container Philosophy

**Why temporary containers are the industry standard.**

> **Part of [Educational Computing Context](README.md)** - Career-relevant knowledge beyond DS01 basics.
>
> **Just want the essentials?** See [Key Concepts: Ephemeral Containers](../key-concepts/ephemeral-containers.md) for a shorter overview.

DS01 embraces an **ephemeral container model** - a philosophy that containers are temporary compute sessions, not permanent fixtures. This guide explains why this approach is the industry standard and how to work effectively with it.

---

## The Core Principle

```
Containers = Temporary compute sessions (like EC2 instances)
Workspaces = Permanent storage (like EBS volumes)
```

**Key insight:** Separate compute from storage. Compute is ephemeral, storage is persistent.

---

## The Philosophy

### Think of It Like...

**Your Laptop:**
- When done working: Shut down to save battery/free RAM
- When you reboot: Files are still there (on SSD)
- You don't leave it running 24/7 when idle

**DS01 Containers:**
- When done working: `container-retire` to free GPU for others
- When you restart: Workspace files still there
- You don't leave containers running when idle

**Cloud Compute (AWS, GCP):**
- Spin up EC2 instance when needed
- Do compute work
- Terminate instance to stop paying
- Your data persists on S3/EBS

---

## What's Ephemeral vs Persistent

### Ephemeral (Removed on Retire)

**Container instance:**
- Running processes (Python, Jupyter, etc.)
- Writable filesystem layer
- GPU allocation
- Memory state (RAM)

**Can be recreated instantly from:**
- Docker image (environment blueprint)
- Workspace (your code and data)

### Persistent (Always Safe)

**Storage:**
- Workspace files (`~/workspace/<project>/` on host → `/workspace/` in container)
- Dockerfiles (image blueprints)
- Docker images

**Can recreate environment:**
- Same packages (from image)
- Same code (from workspace)
- Same GPU access (re-allocated)

---

## Workflow with Ephemeral Containers

### Spin Up: Start GPU Work

```bash
container-deploy my-project --open
```

**What happens:**
1. Creates container from your image
2. Allocates available GPU
3. Mounts your workspace
4. Starts shell

**Time:** ~30 seconds

### Work: Run Compute-Intensive Tasks

```bash
# Inside container
cd /workspace
python train.py                     # Train models
jupyter lab                         # Run notebooks
git commit -m "Update model"        # Save progress
```

**Your work is saved to workspace** - persistent storage.

### Clean Up: Done with GPU

```bash
# Exit container
exit

# Retire (stop + remove + free GPU)
container-retire my-project
```

**What happens:**
1. Container stopped
2. Container removed
3. GPU freed for others
4. **Workspace files remain safe**

**Time:** ~5 seconds

### Later: Resume When Needed

```bash
container-deploy my-project --open
```

**What happens:**
1. New container created (from same image)
2. New GPU allocated (might be different GPU)
3. Same workspace mounted
4. **Your files are exactly as you left them**

**Time:** ~30 seconds

---

## Why Ephemeral?

### 1. Resource Efficiency

**Problem:** Limited GPUs, many users

**Without ephemeral model:**
```
Alice finishes training, leaves container idle
Bob finishes training, leaves container idle
Dana wants GPU - none available!
    (All "allocated" but idle)
```

**With ephemeral model:**
```
Alice finishes training → retires container
Bob finishes training → retires container
Dana needs GPU → available immediately
```

**Result:** Higher utilisation, fairer access.

### 2. Simpler State Management

**Without ephemeral model:**
- Container states: created, running, stopped, paused, restarting
- GPU states: allocated, idle, reserved-but-stopped
- Timeout policies: When to release GPU? Container? Both?
- User confusion: "Why is my stopped container using GPU?"

**With ephemeral model:**
- Container states: running or removed (simple!)
- GPU states: allocated or free (simple!)
- No complex timeout policies needed
- Clear mental model: "Running? Using GPU. Stopped? Recreate."

### 3. Industry Alignment

**This is how production systems work:**

**AWS EC2:**
- Spin up instance when needed
- Do work
- Terminate to save costs
- Data on EBS/S3 persists

**Kubernetes:**
- Deploy pod when needed
- Pod runs workload
- Pod deleted when done
- PersistentVolumes remain

**SageMaker:**
- Launch training job
- Job creates ephemeral compute
- Job completes, compute destroyed
- Model saved to S3

**DS01 prepares you for these workflows.**

### 4. Cost Consciousness

**Cloud costs:**
- Running instance: $$$ per hour
- Stopped instance: Still allocating resources
- Terminated instance: $0

**DS01 equivalent:**
- Running container: GPU allocated (scarce resource)
- Stopped container: GPU still held (wasteful)
- Removed container: GPU freed (good citizenship)

**Learning to `container-retire` = Learning cost-efficient cloud practices.**

---

## Common Concerns Addressed

### "But I lose my work!"

**False!** Let's break down what you actually care about:

**What you NEED to keep:**
- ✅ Code you wrote → Saved in `/workspace`
- ✅ Data you downloaded → Saved in `/workspace`
- ✅ Models you trained → Saved in `/workspace/models/`
- ✅ Experiment results → Saved in `/workspace/results/`
- ✅ Environment setup → Saved in Docker image

**What you DON'T need:**
- ❌ The specific running container instance
- ❌ The specific GPU (any GPU works)
- ❌ RAM state (reload from checkpoint)

**Reality:** You lose nothing important. Everything valuable persists.

### "What if I have a long-running job?"

> **⚠️ Contact DSL First**
>
> The workarounds below (`.keep-alive`, `nohup`, etc.) are available but should be **last resorts** as they can disrupt the system for other users by holding GPUs longer than necessary.
>
> **Please [open an issue on DS01 Hub](https://github.com/hertie-data-science-lab/ds01-hub/issues) first** to discuss your requirements. We can often find better solutions together (adjusted limits, scheduled runs, checkpointing strategies).

**Solution 1: Keep container running**
```bash
# Deploy in background
container-deploy training --background

# Prevent idle timeout (last resort - see warning above)
touch ~/workspace/training/.keep-alive

# Monitor remotely
container-stats
```

**Solution 2: Checkpointing**
```python
# Save progress frequently
for epoch in range(100):
    train_epoch(model)

    # Save every 10 epochs
    if epoch % 10 == 0:
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
        }, f'/workspace/models/checkpoint-{epoch:03d}.pt')
```

**Even if container stops:**
- Load latest checkpoint
- Resume training
- No work lost

### "Recreating containers is slow"

**Actually very fast:**
```bash
# Typical container deployment
$ time container-deploy my-project --background

Real: 28 seconds
- Image already built (0s)
- GPU allocation (2s)
- Container creation (3s)
- Workspace mounting (1s)
- Container start (2s)
```

**Compared to:**
- Laptop boot: 30-60 seconds
- VM start: 2-5 minutes
- Installing packages from scratch: 10-30 minutes

**Image already has your environment - just creating instance.**

### "I forget what packages I had"

**Docker image remembers:**
```bash
# View your Dockerfile
cat ~/dockerfiles/my-project.Dockerfile

# Or check in container
pip list
conda list
```

**Everything in image is reproducible.**

---

## Best Practices

### 1. Retire When Done

**Good citizenship:**
```bash
# Finished your GPU task?
container-retire my-project

# Stepping away for a while?
container-retire my-project

# Switching to different project?
container-retire old-project
container-deploy new-project
```

**Benefits:**
- Frees GPU for others
- No idle timeout worries
- Clean state when you return

### 2. Save Frequently

**In your code:**
```python
# Save checkpoints
torch.save(model, '/workspace/models/checkpoint.pt')

# Log metrics
with open('/workspace/results/log.txt', 'a') as f:
    f.write(f'{epoch}, {loss}, {acc}\n')

# Commit code
# (run on host or in container)
git add .
git commit -m "Update training loop"
```

**Frequency:**
- Code: After each feature
- Checkpoints: Every N epochs
- Logs: Real-time

### 3. Use Background Mode for Long Jobs

```bash
# Start training in background
container-deploy training --background

# Later: Attach to check progress
container-run training
# Or
docker exec -it training._.$(whoami) bash

# View logs without entering
docker logs training._.$(whoami)
```

### 4. Keep Environment in Images

**Don't:**
```bash
# Every time
container-run my-project
pip install transformers datasets  # Slow, non-reproducible
```

**Do:**
```bash
# Once: Build image with packages
image-create  # Add packages to Dockerfile

image-update # Update as needed

# Many times: Deploy instantly
container-deploy my-project  # Packages already installed
```

---

## Workflows with Ephemeral Containers

### Quick Experiment

```bash
# First experiment
container-deploy experiment-1 --open
python run.py
# Results saved to /workspace
exit

# Try different approach
container-retire experiment-1
container-deploy experiment-2 --open
python run2.py
exit
```

**Time:** 2 minutes overhead, unlimited experiments

### Multi-Day Training

```bash
# Day 1
container-deploy training --background
# Training runs overnight

# Day 2: Check progress
container-run training
tensorboard --logdir /workspace/logs
# Still training...
exit

# Day 3: Complete
container-run training
# Training done, test model
python evaluate.py
# Retire when done
exit
container-retire training
```

### Parallel Experiments

```bash
# Start multiple containers (within limits)
container-deploy exp-baseline --background
container-deploy exp-variant-a --background
container-deploy exp-variant-b --background

# All run in parallel
# Check status
container-list

# When done
container-retire exp-baseline
container-retire exp-variant-a
container-retire exp-variant-b
```

---

## Industry Parallels

### AWS EC2

```bash
# DS01
container-deploy my-project
# Work
container-retire my-project

# AWS
aws ec2 run-instances --image-id ami-12345
# Work
aws ec2 terminate-instances --instance-ids i-12345
```

**Same workflow, different scale.**

### Kubernetes Pods

```yaml
# Kubernetes Job
apiVersion: batch/v1
kind: Job
metadata:
  name: training-job
spec:
  template:
    spec:
      containers:
      - name: trainer
        image: my-training-image
        volumeMounts:
        - name: data
          mountPath: /data  # Like /workspace
      restartPolicy: Never  # Ephemeral!
```

**Pod runs, completes, deleted. Data on PersistentVolume.**

### HPC Batch Systems

```bash
# SLURM (HPC scheduler)
sbatch train.sh        # Submit job
# Job runs on allocated nodes
# Job completes, nodes freed

# Same as DS01's ephemeral model
```

---

## Troubleshooting

### "I forgot to save before retiring"

**Prevention:**
- Always save to `/workspace`
- Use Git (push regularly)
- Checkpoint during long runs

**If it happens:**
- Unfortunately, unsaved work in RAM is lost
- Load most recent checkpoint
- Resume from there

### "Container was auto-stopped"

**Cause:** Idle timeout (30min-2h of low CPU/GPU usage, varies by user group)

**Solution:**
- For active work: `.keep-alive` file prevents auto-stop
- For idle: Just recreate container

```bash
container-deploy my-project
# Your workspace files are still there
```

### "Different GPU after recreate"

**Expected behavior:**
- GPU allocation is dynamic
- You might get GPU 0 today, GPU 1 tomorrow
- Your code should not assume specific GPU

**Best practice:**
```python
# Don't hardcode GPU
device = torch.device('cuda:0')  # Bad if GPU changes

# Use first available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

---

## Next Steps

### Understand Persistence

**Critical knowledge:**
- → [Workspaces & Persistence](../background/workspaces-and-persistence.md)

### Learn Daily Workflows

**Put philosophy into practice:**
- → [Daily Usage Patterns](../core-guides/daily-workflow.md)
- → [Managing Containers](../core-guides/daily-workflow.md)

### Understand Resources

**Fair sharing:**
- → [Resource Management](resource-management.md)

---
