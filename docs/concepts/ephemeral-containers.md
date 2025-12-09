# Ephemeral Container Model

Why DS01 treats containers as temporary compute sessions, and why this prepares you for the cloud.

---

## The Core Philosophy

**Containers are temporary compute sessions. Your workspace is permanent storage.**

Like renting a workstation:
- Check out a configured machine → work → return it → your files remain safe
- Next day: check out a fresh machine → continue where you left off

**DS01 encourages:**
```bash
project launch my-thesis --open    # Create fresh container
# Work for the day...
exit
container retire my-thesis         # Remove container, free GPU
```

**Not:**
```bash
container-stop my-thesis           # Don't just pause
# Container sits idle, holding GPU
```

---

## Why This Matters for Your Career

**DS01's ephemeral model is the industry standard.**

Every major cloud platform, container orchestrator, and HPC system uses this pattern. By learning DS01, you're learning skills that transfer directly to:

- **AWS** (ECS, Batch, Lambda)
- **Google Cloud Platform** (Cloud Run, Kubernetes Engine)
- **Microsoft Azure** (Container Instances, Batch)
- **Kubernetes** (Jobs, Pods)
- **HPC clusters** (SLURM, PBS, batch jobs)

**This is not academic toy software** - this is how professionals work in industry.

---

## Industry Parallels

### AWS ECS (Elastic Container Service)

**AWS pattern:**
```bash
# Define task (like DS01 image)
aws ecs register-task-definition --file task.json

# Run task (like project launch)
aws ecs run-task --task-definition my-task

# Task completes, container removed automatically
# Output saved to S3 (like DS01 workspace)
```

**DS01 equivalent:**
```bash
image-create my-project
project launch my-project
# Work...
container retire my-project
# Files in ~/workspace/ persist
```

**Same model:** Task definition (image) → temporary execution (container) → persistent storage (workspace/S3).

### Kubernetes Jobs

**Kubernetes pattern:**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: training-job
spec:
  template:
    spec:
      containers:
      - name: pytorch
        image: my-org/pytorch-training:latest
        command: ["python", "train.py"]
      restartPolicy: Never
```

**Key similarity:**
- Image defines environment
- Job creates pod (container)
- Pod runs, completes, terminates
- Results written to persistent volume
- Pod is ephemeral, volume is permanent

**DS01 equivalent:**
```bash
project launch training --open
python train.py
# Checkpoints saved to /workspace/
exit
container retire training
```

### HPC Batch Jobs (SLURM)

**SLURM pattern:**
```bash
#!/bin/bash
#SBATCH --job-name=training
#SBATCH --gres=gpu:1
#SBATCH --output=results.log

module load pytorch/2.8.0
python train.py
```

Submit: `sbatch job.sh`

**Job lifecycle:**
1. Submitted to queue
2. Resources allocated
3. Job runs on compute node
4. Job completes, resources freed
5. Output saved to shared filesystem

**DS01 equivalent:**
```bash
project launch training --background
container-attach training
python train.py  # Output to ~/workspace/
exit
container retire training  # GPU freed
```

**Same model:** Job definition → temporary allocation → persistent results.

### Google Cloud Run

**Cloud Run pattern:**
```bash
# Deploy container image
gcloud run deploy my-service \
  --image gcr.io/my-project/my-image

# Cloud Run creates container instances on demand
# Scales to zero when idle
# Each request = new temporary container
```

**Key insight:** Cloud Run can scale to **zero containers** when idle because containers are stateless and ephemeral.

**DS01 parallel:** Your container can be removed (scale to zero) because workspace persists.

---

## Why Ephemeral Wins

### 1. Resource Efficiency

**Traditional model (bad):**
```
User A: Container running 24/7, GPU allocated
  ├─ Active work: 2 hours/day
  ├─ Idle: 22 hours/day (GPU wasted!)
  └─ Other users blocked

Result: 90% waste, poor sharing
```

**Ephemeral model (good):**
```
User A: Container 2 hours/day, GPU freed immediately
User B: Container 3 hours/day, same GPU
User C: Container 4 hours/day, same GPU

Result: 3 users share 1 GPU efficiently
```

**Cloud parallel:** AWS charges per container-second. Ephemeral = lower cost.

### 2. Reproducibility

**Problem with long-lived containers:**
```bash
# Day 1
pip install torch==2.0.0

# Day 5
pip install some-package
# (accidentally upgrades torch to 2.1.0)

# Day 10
# Code breaks, can't remember what changed
```

**Solution with ephemeral containers:**
```dockerfile
# Dockerfile (version controlled)
RUN pip install torch==2.0.0
RUN pip install some-package==1.5.0
```

**Every container launch:**
- Starts from known state (image)
- Reproducible environment
- No "works on my machine" problems

**Cloud parallel:** Infrastructure as Code (Terraform, CloudFormation) - declare desired state, not manual changes.

### 3. Scalability

**Ephemeral containers enable:**

```bash
# Run 10 experiments in parallel (if resources available)
for i in {1..10}; do
  project launch experiment-$i --background
  container-attach experiment-$i
  python train.py --config config-$i.yaml &
done

# All from same image
# Each with isolated workspace
# Each gets GPU when available
```

**Cloud parallel:** Kubernetes can scale to 1000s of pods from one image.

### 4. Clean State

**Every container launch:**
- Fresh environment
- No leftover processes
- No stale cache
- No hidden state

**Benefits:**
- Debugging easier (can reproduce from scratch)
- Testing reliable (no contamination)
- Collaboration smoother (same environment guaranteed)

**Cloud parallel:** Netflix Chaos Monkey randomly kills instances - forces ephemeral design.

---

## What Persists, What's Ephemeral

### Ephemeral (Removed Daily)

```
Container instance
  ├─ Running processes
  ├─ /tmp/ files
  ├─ Installed packages (if not in image)
  ├─ Shell history (if not in /workspace)
  ├─ GPU allocation
  └─ Network state
```

**All reset on `container retire`.**

### Persistent (Survives Forever)

```
~/workspace/<project>/
  ├─ Code (Python scripts, notebooks)
  ├─ Data (datasets, csvs)
  ├─ Models (checkpoints, weights)
  ├─ Results (logs, plots, papers)
  ├─ Configuration (config files)
  └─ Dockerfile (environment definition)

Docker images
  └─ ds01-<user>/<project>:latest
```

**Safe across container recreates.**

---

## Real-World Workflows

### Research Workflow (Academia)

```bash
# Morning - Start fresh container
project launch my-thesis --open

# Day's work - Results saved to workspace
python experiments/train.py
# Checkpoints → /workspace/models/
# Logs → /workspace/results/
# Plots → /workspace/figures/

# Evening - Remove container
exit
container retire my-thesis

# Next week - Continue exactly where you left off
project launch my-thesis --open
ls /workspace/models/  # All checkpoints present
```

### Industry Workflow (Production ML)

```bash
# Data scientist develops model
project launch model-dev --open
# Iterate on model architecture
# Save final model to /workspace/models/final.pt

# MLOps engineer deploys to production
# Uses same Docker image as data scientist
docker run ds01-123/model-dev:latest \
  python serve.py --model /workspace/models/final.pt

# Same environment, guaranteed reproducibility
```

### Cloud Migration Story

**Student today (DS01):**
```bash
project init my-model
project launch my-model
python train.py
container retire my-model
```

**Same student, industry job (AWS):**
```bash
# Push image to AWS
docker tag ds01-123/my-model:latest 123456.ecr.aws.com/my-model
docker push 123456.ecr.aws.com/my-model

# Run on AWS Batch
aws batch submit-job \
  --job-name training \
  --job-definition my-job \
  --container-overrides '{"image": "123456.ecr.aws.com/my-model"}'

# Same workflow, same skills
```

---

## Common Questions

### "Won't I lose work if container is removed?"

**No.** Only if you save to the wrong place.

**Safe:**
```bash
# Inside container
echo "results" > /workspace/output.txt
```

**Unsafe:**
```bash
# Inside container
echo "results" > ~/output.txt  # NOT in /workspace!
```

**Rule:** Always work in `/workspace/<project>/`.

### "Why not just keep containers running?"

**Three reasons:**

1. **Resource fairness** - GPU freed for others
2. **Cost efficiency** - In cloud, you pay per hour
3. **Clean state** - No hidden bugs from accumulated state

**Industry parallel:** Cloud auto-scaling terminates idle instances.

### "What if my experiment takes 3 days?"

**That's fine!** Container can run for days.

**The difference:**
- **Don't just pause** (container-stop) when done
- **Actually remove** (container retire) to free GPU

**Long-running best practices:**
```bash
# Inside container
nohup python train.py > /workspace/training.log 2>&1 &

# Or use tmux
tmux new -s training
python train.py  # Ctrl+B D to detach

# Can disconnect, reconnect anytime
exit
container-attach my-project
tmux attach -s training
```

### "Can I save a container's state?"

**Yes, but not recommended.**

```bash
# Quick save (non-reproducible)
container retire my-project --save-changes

# Better: Document in Dockerfile
vim ~/workspace/my-project/Dockerfile
# Add changes
image-update my-project
```

**Why Dockerfile better:**
- Version controlled
- Reproducible
- Shareable
- Industry standard

---

## Skills You're Learning

By using DS01's ephemeral model, you're learning:

### 1. Infrastructure as Code

**DS01:**
```dockerfile
FROM aime/pytorch:2.8.0-cuda12.4
RUN pip install transformers datasets
WORKDIR /workspace
```

**Industry (Terraform):**
```hcl
resource "aws_instance" "training" {
  ami           = "ami-pytorch-cuda"
  instance_type = "p3.2xlarge"
}
```

**Same principle:** Declare infrastructure in code, not manual setup.

### 2. Stateless Architecture

**DS01:** Container = stateless compute, workspace = stateful storage

**Industry:** Containers = stateless apps, databases = stateful storage

**Example (web service):**
```
Load Balancer → [Container 1] → Database
            → [Container 2] ↗
            → [Container 3] ↗

Containers are ephemeral, interchangeable
Database persists state
```

### 3. Immutable Infrastructure

**DS01:** Don't modify running container, rebuild image

**Industry:** Don't patch running servers, deploy new ones

**Benefits:**
- No configuration drift
- Rollbacks easy (old image still exists)
- Identical environments guaranteed

### 4. Containerization Best Practices

**DS01 teaches:**
- Dockerfiles for reproducibility
- Layered images for efficiency
- Volume mounts for persistence
- Resource limits (GPU, CPU, memory)

**All directly applicable to:**
- Docker in production
- Kubernetes deployments
- Cloud container services

---

## Industry Testimonials (Hypothetical)

> "Learning DS01 in grad school made my transition to AWS seamless. The ephemeral container model was already second nature."
> — Data Scientist, Amazon

> "DS01's project-based workflow is exactly how we structure our ML pipelines at work. Same concepts, bigger scale."
> — ML Engineer, Google

> "Understanding image layers from DS01 helped me optimize our Docker builds, saving us thousands in cloud costs."
> — DevOps Engineer, Startup

---

## The Big Picture

**DS01 is not just a lab system. It's a training ground for cloud-native computing.**

**Skills learned:**
- ✅ Container orchestration patterns
- ✅ Infrastructure as Code
- ✅ Stateless/stateful separation
- ✅ Reproducible environments
- ✅ Resource efficiency mindset
- ✅ Cloud-native workflows

**Career impact:**
- More productive in industry ML roles
- Comfortable with modern DevOps tools
- Understanding of cloud architecture
- Valuable skills for data science jobs

**Bottom line:** DS01's ephemeral model isn't arbitrary - it's how the industry works.

---

## Comparing Systems

| Feature | DS01 | AWS Batch | Kubernetes | HPC SLURM |
|---------|------|-----------|------------|-----------|
| **Compute unit** | Container | Task | Pod | Job |
| **Lifecycle** | Ephemeral | Ephemeral | Ephemeral | Ephemeral |
| **Definition** | Image | Task def | Image | Job script |
| **Storage** | Workspace | S3/EFS | PV/PVC | Shared FS |
| **Resource mgmt** | Cgroups | ECS | Kubelet | cgroups |
| **Scheduling** | Manual | Queue | Scheduler | Queue |

**Pattern is universal: ephemeral compute + persistent storage.**

---

## Next Steps

**Understand the technical details:**

→ [Containers and Images](containers-and-images.md) - How images/containers work

→ [Workspaces and Persistence](workspaces-persistence.md) - Where files actually live

**See DS01 in broader context:**

→ [Industry Parallels](../background/industry-parallels.md) - Detailed cloud comparisons

**Apply this knowledge:**

→ [Daily Workflow](../getting-started/daily-workflow.md) - Put ephemeral model into practice

→ [Long-Running Jobs](../guides/long-running-jobs.md) - Multi-day experiments

---

**Remember: By learning DS01's ephemeral model, you're learning how the cloud works. This is a career skill.**
