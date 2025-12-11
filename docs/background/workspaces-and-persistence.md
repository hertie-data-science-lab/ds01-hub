# Workspaces & Persistence

**Deep dive into stateless compute, persistent storage, and cloud architecture patterns.**

> **Part of [Educational Computing Context](README.md)** - Career-relevant knowledge beyond DS01 basics.
>
> **Just want the essentials?** See [Key Concepts: Workspaces and Persistence](../concepts/workspaces-persistence.md) for a shorter overview.

Understanding stateless/stateful separation is critical for cloud computing. This guide explains persistence patterns, file organisation, and how these concepts transfer to AWS, Kubernetes, and production systems.

---

## The Golden Rule

**Everything in `/workspace` (inside container) = Safe and permanent**
**Everything else = Temporary and will be lost**

---

## What's Persistent vs Ephemeral

### Persistent (Always Safe) ✅

| Location | What It Is | Survives Container Removal? |
|----------|-----------|---------------------------|
| `~/workspace/<project>/` | Your code, data, results | ✅ Yes |
| `~/dockerfiles/` | Image blueprints | ✅ Yes |
| Docker images | Environment blueprints | ✅ Yes |
| `~/.ssh/` | SSH keys | ✅ Yes |
| `~/.ds01-limits` | Resource quotas | ✅ Yes |

### Ephemeral (Temporary) ❌

| Location | What It Is | Survives Container Removal? |
|----------|-----------|---------------------------|
| Container instance | Running container | ❌ No |
| `/tmp` (in container) | Temporary files | ❌ No |
| `/home/<user>` (in container, outside `/workspace`) | Container home dir | ❌ No |
| Container processes | Running Python, Jupyter, etc. | ❌ No |
| GPU allocation | Assigned GPU | ❌ No |

---

## Understanding DS01 File Locations

### On the Host (DS01 Server)

```
/home/your-username/          # Your home directory
├── workspace/                # ← PERSISTENT: Your projects
│   ├── project-1/
│   │   ├── data/
│   │   ├── notebooks/
│   │   ├── models/
│   │   └── README.md
│   ├── project-2/
│   └── experiment-3/
├── dockerfiles/              # ← PERSISTENT: Image blueprints
│   ├── project-1.Dockerfile
│   └── project-2.Dockerfile
├── .ssh/                     # ← PERSISTENT: SSH keys
│   ├── id_ed25519
│   └── id_ed25519.pub
└── .ds01-limits              # ← PERSISTENT: Your quotas
```

### Inside a Container

```
/                             # Container root
├── workspace/                # ← MOUNTED from ~/workspace/<project>/
│   ├── data/                 #    Files here = PERSISTENT
│   ├── notebooks/
│   └── train.py
├── tmp/                      # ← EPHEMERAL: Deleted on container removal
├── home/
│   └── your-username/        # ← EPHEMERAL (except /workspace mount)
└── opt/
    └── conda/                # ← EPHEMERAL (but can rebuild from image)
```

**Key insight:** `/workspace` in container is actually `~/workspace/<project>/` on host, mounted into the container.

---

## How Workspace Mounting Works

### The Mount

When you create a container:
```bash
container-deploy my-project
```

DS01 automatically runs (internally):
```bash
docker run \
  -v ~/workspace/my-project:/workspace \  # ← This line
  ...
```

**This means:**
- Files you save to `/workspace` (inside container)
- Actually saved to `~/workspace/my-project/` (on host)
- Survive container removal

### Visualisation

```
┌─────────────────────────────────────────┐
│         DS01 Host (Persistent)          │
│                                         │
│  ~/workspace/my-project/                │
│  ├── data/                              │
│  ├── models/                            │
│  └── train.py                           │
│         ↕                                │
│     (mounted)                           │
│         ↕                                │
│  ┌────────────────────────────────┐    │
│  │  Container (Ephemeral)         │    │
│  │                                │    │
│  │  /workspace/  ← mounted        │    │
│  │  ├── data/                     │    │
│  │  ├── models/                   │    │
│  │  └── train.py                  │    │
│  │                                │    │
│  │  /tmp/  ← NOT mounted          │    │
│  │  └── temp.txt  ❌ LOST         │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

## Best Practices for File Organisation

### Recommended Structure

```
~/workspace/<project>/
├── README.md                 # Project documentation
├── requirements.txt          # Python packages (for Dockerfile)
├── .gitignore                # Git ignored files
├── .keep-alive               # Prevent auto-stop (optional)
│
├── data/                     # Datasets
│   ├── raw/                  # Original data
│   ├── processed/            # Cleaned data
│   └── README.md             # Data documentation
│
├── notebooks/                # Jupyter notebooks
│   ├── 01-exploration.ipynb
│   ├── 02-training.ipynb
│   └── 03-analysis.ipynb
│
├── src/                      # Source code
│   ├── __init__.py
│   ├── data.py               # Data loading
│   ├── model.py              # Model definition
│   └── train.py              # Training script
│
├── models/                   # Trained models
│   ├── checkpoint-001.pt
│   ├── checkpoint-002.pt
│   └── best-model.pt
│
├── results/                  # Experiment outputs
│   ├── metrics.json
│   ├── plots/
│   └── logs/
│
└── tests/                    # Unit tests
    └── test_model.py
```

### Why This Structure?

**Separation of concerns:**
- `data/`: Input
- `src/`: Code
- `models/`: Outputs (trained weights)
- `results/`: Analysis
- `notebooks/`: Exploration

**Reproducibility:**
- `README.md`: How to use
- `requirements.txt`: What packages needed
- `src/`: Reusable code
- `tests/`: Verify correctness

**Collaboration:**
- Clear organisation
- Easy to navigate
- Standard structure

---

## Working Inside Containers

### Always Start in Workspace

```bash
# Inside container
alice@my-project:~$ pwd
/workspace

# If not, go there
cd /workspace
```

### Save Everything to Workspace

**Good:**
```python
# Save model to workspace
torch.save(model.state_dict(), '/workspace/models/model.pt')

# Log to workspace
with open('/workspace/results/log.txt', 'a') as f:
    f.write(f'Epoch {epoch}: Loss {loss}\n')

# Cache to workspace
cache_dir = '/workspace/.cache'
```

**Bad:**
```python
# DON'T save to /tmp
torch.save(model.state_dict(), '/tmp/model.pt')  # ❌ LOST on container removal

# DON'T save to home (outside workspace)
torch.save(model.state_dict(), '~/model.pt')  # ❌ LOST

# DON'T save to root
torch.save(model.state_dict(), '/model.pt')  # ❌ LOST
```

### Environment Variables for Common Paths

Set in your code or shell:
```bash
# Inside container
export DATA_DIR="/workspace/data"
export MODEL_DIR="/workspace/models"
export RESULTS_DIR="/workspace/results"

# Use in Python
import os
data_dir = os.environ['DATA_DIR']
```

---

## Docker Images vs Containers vs Workspaces

### Three Layers of Persistence

**1. Docker Image (Persistent Blueprint)**
- Contains: OS, Python, packages, Dockerfile instructions
- Created with: `image-create` or `docker build`
- Survives: Container removal, system reboot
- Location: Docker storage (`/var/lib/docker/`)
- Purpose: Environment reproducibility

**2. Container Instance (Ephemeral)**
- Contains: Running processes, writable filesystem layer
- Created with: `container-deploy` or `docker run`
- Survives: Stop/start (unless removed)
- Does NOT survive: `container-retire` or `docker rm`
- Purpose: Temporary compute environment

**3. Workspace (Persistent Data)**
- Contains: Your code, data, results
- Created with: `mkdir ~/workspace/<project>`
- Survives: Everything (container removal, image deletion, reboots)
- Location: `~/workspace/<project>/` on host, `/workspace` in container
- Purpose: Permanent storage

### Lifecycle Example

```bash
# Day 1: Setup
image-create                          # Create image (PERSISTENT)
container-deploy my-project           # Create container (EPHEMERAL)
cd /workspace
echo "Hello" > file.txt               # Save to workspace (PERSISTENT)
exit

# Day 1 Evening: Free GPU
container-retire my-project           # Container DELETED
                                      # Image STILL EXISTS
                                      # Workspace STILL EXISTS

# Day 2: Resume work
container-deploy my-project           # New container from same image
cd /workspace
cat file.txt                          # "Hello" - file persists!
```

---

## Common Scenarios

### Scenario 1: Container Crashed

**What happens:**
- Container stops unexpectedly
- GPU released
- Container instance still exists (stopped state)

**Your files:**
- ✅ Workspace files: Safe
- ✅ Image: Safe
- ❌ Running processes: Terminated
- ❌ Unsaved work (RAM): Lost

**Recovery:**
```bash
# Restart container
container-start my-project
# Or
container-run my-project

# Your files are there
ls /workspace
```

### Scenario 2: Container Retired

**What happens:**
- Container stopped
- Container removed
- GPU released

**Your files:**
- ✅ Workspace files: Safe
- ✅ Image: Safe
- ❌ Container instance: Deleted

**Recovery:**
```bash
# Recreate from same image
container-deploy my-project

# Same environment, same files
```

### Scenario 3: Image Deleted

**What happens:**
- Image removed from Docker storage
- Containers from this image can't be created

**Your files:**
- ✅ Workspace files: Safe
- ❌ Image: Deleted
- ❌ Packages installed: Need to reinstall

**Recovery:**
```bash
# Rebuild image
image-create                          # Reinstall packages

# Or use base image temporarily
container-deploy my-project --framework pytorch

# Your workspace files unaffected
```

### Scenario 4: Accidentally Deleted Workspace

**What happens:**
- Workspace directory deleted
- Your code, data, results LOST

**Your files:**
- ❌ Workspace files: DELETED
- ✅ Image: Safe (can recreate environment)
- ❌ Data: Lost (unless in Git or backups)

**Prevention:**
```bash
# Use Git for code
cd ~/workspace/my-project
git init
git remote add origin <your-repo>
git push

# Backup data regularly
rsync -avz ~/workspace/my-project/ backup-location/

# Don't run rm -rf in workspace!
```

---

## Backup Strategies

### 1. Version Control (Git)

**For code:**
```bash
cd ~/workspace/my-project
git init
git add src/ notebooks/ README.md requirements.txt
git commit -m "Initial commit"
git remote add origin git@github.com:your-username/project.git
git push -u origin main
```

**Advantages:**
- Version history
- Collaboration
- Remote backup
- Reproducibility

**What to commit:**
- ✅ Source code (`src/`)
- ✅ Notebooks (`notebooks/`)
- ✅ Documentation (`README.md`)
- ✅ Configuration (`requirements.txt`, configs)
- ❌ Data files (too large)
- ❌ Model weights (too large)
- ❌ Results (generated)

### 2. Data Storage

**For datasets:**
- Store on DS01's shared data directory (if available)
- Download from source (reproducible)
- Use dataset management tools (DVC, LFS)

**Don't:**
- Commit large datasets to Git (slow, bloated)
- Store only in container (temporary)

### 3. Model Checkpoints

**During training:**
```python
# Save checkpoints periodically
for epoch in range(epochs):
    train(...)
    if epoch % 10 == 0:
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
        }, f'/workspace/models/checkpoint-{epoch:03d}.pt')
```

**Final models:**
- Save to workspace (`/workspace/models/`)
- Copy to permanent storage
- Upload to model registry (Hugging Face Hub, etc.)

### 4. Results and Logs

**Experiment tracking:**
- Weights & Biases, MLflow, TensorBoard
- Automatically backs up metrics to cloud
- Survives workspace deletion

```python
import wandb
wandb.init(project="my-project")
wandb.log({"loss": loss, "accuracy": acc})
# Logged to cloud, safe even if workspace deleted
```

---

## Monitoring Disk Usage

### Check Workspace Size

```bash
# Total size of all projects
du -sh ~/workspace

# Size of each project
du -sh ~/workspace/*

# Detailed breakdown
du -h ~/workspace/my-project | sort -hr | head -20
```

### Find Large Files

```bash
# Files over 1GB
find ~/workspace -type f -size +1G -exec ls -lh {} \;

# Largest files
find ~/workspace -type f -exec ls -s {} \; | sort -nr | head -20
```

### Clean Up

```bash
# Remove temporary files
rm -rf ~/workspace/*/tmp
rm -f ~/workspace/*/*.tmp

# Remove old checkpoints
find ~/workspace/models -name "checkpoint-*.pt" -mtime +30 -delete

# Clean Python cache
find ~/workspace -type d -name __pycache__ -exec rm -rf {} +
```

### Check Your Quota

```bash
# Your disk quota (if enforced)
quota -s

# Total disk usage
df -h | grep home
```

---

## Docker Image Storage

### Images Take Disk Space

```bash
# List images with sizes
docker images

# Total size
docker system df

# Detailed breakdown
docker system df -v
```

### Clean Up Old Images

```bash
# Remove unused images
docker image prune

# Remove all unused (careful!)
docker image prune -a

# Remove specific image
docker rmi ds01-$(whoami)/old-project:latest
```

---

## Troubleshooting

### "Where are my files?"

**Check both locations:**
```bash
# On host
ls ~/workspace/<project-name>/

# Inside container (should match) - replace <project-name>
docker exec <project-name>._.$(whoami) ls /workspace/
```

### "Files disappeared after container removal"

**Likely saved outside workspace:**
```bash
# Check if files in workspace
ls ~/workspace/<project-name>/

# If empty, check container (if still exists) - replace <project-name>
docker exec <project-name>._.$(whoami) ls /tmp/
docker exec <project-name>._.$(whoami) ls ~/
```

**Prevention:** Always save to `/workspace`

### "Can't write to workspace"

**Check permissions:**
```bash
# On host
ls -ld ~/workspace/my-project/

# Should be owned by you
# If not, fix:
sudo chown -R $(whoami):$(whoami) ~/workspace/my-project/
```

### "Out of disk space"

**Check usage:**
```bash
du -sh ~/workspace/*            # Workspace
docker system df                # Images/containers

# Clean up
rm -rf ~/workspace/old-project/
docker image prune
```

---

## Best Practices Summary

### ✅ Do This

1. **Save everything to `/workspace`**
2. **Use Git for code** (push regularly)
3. **Organise projects** (data/, src/, models/, etc.)
4. **Save checkpoints frequently**
5. **Clean up old data** periodically
6. **Use experiment tracking** (W&B, MLflow)

### ❌ Avoid This

1. **Don't save to `/tmp` or `~` (outside workspace)**
2. **Don't commit large files** to Git
3. **Don't leave containers running** with unsaved work
4. **Don't delete workspace** without backups
5. **Don't fill disk** - clean up regularly

---

## Next Steps

### Understand Containers

**Learn how containers work:**
- → [Containers Explained](containers-explained.md)

### Learn Daily Workflow

**Put knowledge into practice:**
- → [Daily Usage Patterns](../guides/daily-workflow.md)

### Advanced Organisation

**Project structure:**
- → [Project Structure](../guides/creating-projects.md)

---

## Summary

**Key Takeaways:**

1. **Workspace (`~/workspace/`) = PERSISTENT** - Always safe
2. **Container filesystem = EPHEMERAL** - Lost on removal
3. **Images = PERSISTENT** - Can recreate containers
4. **Always save to `/workspace`** inside containers
5. **Use Git for code**, backups for data
6. **Organise projects** for collaboration and reproducibility

**The golden rule: If it's important, save it to `/workspace`!**

**Ready to start working?** → [Daily Usage Patterns](../guides/daily-workflow.md)

**Want to understand the philosophy?** → [Ephemeral Containers](../background/ephemeral-philosophy.md)
