# Workspaces and Persistence

Understanding what persists across container recreates and where your files actually live.

---

## The Two Filesystems

When you work in a DS01 container, you interact with **two different filesystems**:

### 1. Container Filesystem (Ephemeral)

```
Container: my-thesis._.12345
├─ /root/               # Home directory (temporary!)
├─ /tmp/                # Temp files (temporary!)
├─ /usr/bin/python      # From image (reset on recreate)
├─ /opt/conda/          # From image (reset on recreate)
└─ Everything else from image
```

**Lifetime:** Exists only while container exists. Removed with `container retire`.

**Use for:** Temporary computations, cache, intermediate files you don't need.

### 2. Workspace Filesystem (Persistent)

```
Host: /home/<username>/workspace/
├─ my-thesis/
│   ├─ data/
│   ├─ models/
│   ├─ notebooks/
│   ├─ results/
│   └─ Dockerfile
└─ other-project/
```

**Mounted into container as:** `/workspace/`

**Lifetime:** Permanent. Survives container removal, survives system reboots.

**Use for:** All your important work - code, data, models, results.

---

## How It Works

**When you run `project launch my-thesis`:**

```
Host Machine                Container
────────────                ─────────
/home/user/workspace/  ←→  /workspace/  (volume mount)
    └─ my-thesis/              └─ my-thesis/
```

**The mount is bidirectional:**
- Files created in `/workspace/` inside container appear in `~/workspace/` on host
- Files created in `~/workspace/` on host appear in `/workspace/` inside container
- **They're the same files** - not copies

**When you `container retire my-thesis`:**
- Container filesystem deleted
- `/workspace/` mount disconnected
- `~/workspace/` on host **untouched**

**Next `project launch my-thesis`:**
- New container created
- `~/workspace/` mounted again into new container
- All your files reappear

---

## The Golden Rule

**Save everything important to `/workspace/<project>/`**

```bash
# Inside container - GOOD
cd /workspace/my-thesis
python train.py
# Checkpoints saved to /workspace/my-thesis/models/

# Inside container - BAD
cd ~
python train.py
# Checkpoints saved to /root/ (temporary!)
```

---

## Common Scenarios

### Scenario 1: Saving Model Checkpoints

**Wrong (files lost):**
```python
# Inside container
import torch

model = MyModel()
torch.save(model.state_dict(), 'checkpoint.pt')
# Saved to /root/checkpoint.pt (ephemeral!)

# Exit, remove container
exit
container retire my-thesis

# Relaunch
project launch my-thesis
ls checkpoint.pt  # ERROR: No such file
```

**Right (files persist):**
```python
# Inside container
import torch

model = MyModel()
torch.save(model.state_dict(), '/workspace/my-thesis/models/checkpoint.pt')
# Saved to persistent storage

# Exit, remove container
exit
container retire my-thesis

# Relaunch
project launch my-thesis
ls /workspace/my-thesis/models/checkpoint.pt  # File exists!
```

### Scenario 2: Downloading Datasets

**Wrong (re-download every time):**
```bash
# Inside container
cd /tmp
wget https://example.com/dataset.tar.gz
tar -xzf dataset.tar.gz
# Extracted to /tmp/ (ephemeral!)

# Next launch - have to download again
```

**Right (download once):**
```bash
# Inside container
cd /workspace/my-thesis/data
wget https://example.com/dataset.tar.gz
tar -xzf dataset.tar.gz
# Extracted to /workspace/ (persistent!)

# Next launch - dataset already there
```

### Scenario 3: Jupyter Notebooks

**Default (safe):**
```bash
# Inside container
cd /workspace/my-thesis/notebooks
jupyter lab
# Notebooks auto-save to /workspace/ (persistent!)
```

**If you start Jupyter elsewhere (dangerous):**
```bash
# Inside container
cd ~
jupyter lab
# Notebooks save to /root/notebooks/ (ephemeral!)
```

**Always start Jupyter from `/workspace/`.**

---

## Checking Where Files Are

**Inside container, check your location:**
```bash
pwd
# /workspace/my-thesis ✓ Good
# /root ✗ Bad
```

**Check if file is in workspace:**
```bash
# Inside container
realpath my-file.txt
# /workspace/my-thesis/my-file.txt ✓ Persistent
# /root/my-file.txt ✗ Ephemeral
```

**List workspace projects:**
```bash
# Inside or outside container
ls ~/workspace/
# or
ls /workspace/
```

---

## Industry Parallel: Stateless Apps + Persistent Storage

DS01's model mirrors cloud architecture:

### AWS Example

```
EC2 Instance (ephemeral)          EFS/S3 (persistent)
────────────────────────          ───────────────────
Application code                  User data
Runtime state                     Uploaded files
Temporary cache                   Database backups
Logs (unless shipped out)         Long-term storage

Can terminate anytime    ←→       Survives termination
```

### Kubernetes Example

```
Pod (ephemeral)                   PersistentVolume
───────────────                   ────────────────
Container filesystem              Mounted at /data/
App runs from image               User uploads
Temporary processing              Database files
                                  Logs archive

Pod restarts frequently  ←→       Volume persists
```

### DS01 Example

```
Container (ephemeral)             Workspace (persistent)
─────────────────────             ──────────────────────
Python packages (from image)      Your code
Running processes                 Your data
/tmp/ files                       Your models
Temporary variables               Your results

Removed daily            ←→       Survives forever
```

**Pattern is universal: ephemeral compute + persistent storage.**

---

## Advanced: What About Home Directory?

**In DS01 containers, `/root/` is ephemeral.**

**But you can make configs persist:**

### Option 1: Symlink to Workspace

```bash
# Inside container
ln -sf /workspace/my-thesis/.bashrc ~/.bashrc
ln -sf /workspace/my-thesis/.vimrc ~/.vimrc

# Now edits persist
```

### Option 2: Add to Dockerfile

```dockerfile
COPY bashrc /root/.bashrc
COPY vimrc /root/.vimrc
```

**Rebuild image:**
```bash
image-update my-thesis
```

**Now configs baked into image** - every container has them.

---

## Package Installation Persistence

### Temporary (Lost on Remove)

```bash
# Inside container
pip install new-package

# Works this session
import new_package  # OK

# Exit and retire
exit
container retire my-thesis

# Relaunch - package gone
project launch my-thesis
import new_package  # ModuleNotFoundError
```

### Permanent (Add to Image)

```bash
# Edit Dockerfile
vim ~/workspace/my-thesis/Dockerfile
# Add: RUN pip install new-package

# Rebuild image
image-update my-thesis

# Recreate container
container retire my-thesis
project launch my-thesis

# Package present
import new_package  # Works forever
```

### Quick Install (Fast but Non-Reproducible)

```bash
# Inside container
image-install new-package

# Saves packages to image
# Faster than editing Dockerfile
# Less reproducible
```

---

## Cache Directories

Some tools cache to home directory. You might want persistence:

### Hugging Face Cache

```bash
# Default (ephemeral)
~/.cache/huggingface/

# Make persistent
export HF_HOME=/workspace/my-thesis/.cache/huggingface
```

**Add to Dockerfile:**
```dockerfile
ENV HF_HOME=/workspace/.cache/huggingface
```

### Pip Cache

```bash
# Default (ephemeral)
~/.cache/pip/

# Make persistent (optional)
export PIP_CACHE_DIR=/workspace/.cache/pip
```

**Note:** Caching can speed up package installs, but workspace caches take up your quota.

---

## Git Repositories in Workspace

**Your project workspace can be a git repo:**

```bash
# Outside or inside container
cd ~/workspace/my-thesis
git init
git add .
git commit -m "Initial commit"
git remote add origin <url>
git push
```

**Benefits:**
- Version control your code
- Backup to GitHub/GitLab
- Collaborate with others
- Track experiment history

**What to commit:**
- ✓ Code (.py files, notebooks)
- ✓ Dockerfile
- ✓ Configuration files
- ✓ README, documentation
- ✗ Large datasets (use .gitignore)
- ✗ Model checkpoints (too large)
- ✗ Generated results (can regenerate)

---

## Workspace Structure Best Practices

**Recommended structure:**

```
~/workspace/my-thesis/
├── Dockerfile           # Environment definition
├── requirements.txt     # Python packages
├── pyproject.toml       # Project metadata
├── README.md            # Project documentation
├── .gitignore           # Git exclusions
├── data/                # Datasets (add to .gitignore)
│   ├── raw/
│   └── processed/
├── notebooks/           # Jupyter notebooks
│   └── exploration.ipynb
├── src/                 # Source code
│   ├── __init__.py
│   ├── model.py
│   └── train.py
├── models/              # Saved checkpoints (add to .gitignore)
│   └── checkpoint_epoch_10.pt
├── results/             # Experiment outputs
│   ├── logs/
│   ├── plots/
│   └── metrics.csv
└── tests/               # Unit tests
    └── test_model.py
```

**Add to `.gitignore`:**
```
data/
models/*.pt
*.pyc
__pycache__/
.ipynb_checkpoints/
```

---

## Quota and Space Management

**Workspaces have storage quotas** - check your usage:

```bash
# Check workspace usage
du -sh ~/workspace/*

# Find large files
du -h ~/workspace/my-thesis | sort -h | tail -20
```

**Space-saving tips:**

1. **Don't duplicate datasets:**
   ```bash
   # Share datasets across projects
   ~/workspace/datasets/imagenet/
   ~/workspace/my-thesis/data -> ../datasets/imagenet  # Symlink
   ```

2. **Clean up old checkpoints:**
   ```bash
   # Keep only best checkpoints
   rm ~/workspace/my-thesis/models/checkpoint_epoch_{1..9}.pt
   ```

3. **Compress results:**
   ```bash
   tar -czf results.tar.gz results/
   rm -rf results/
   ```

4. **Archive finished projects:**
   ```bash
   tar -czf my-thesis-archive.tar.gz my-thesis/
   # Upload to external storage
   # rm -rf my-thesis/
   ```

---

## Filesystem Table

| Location | Persistent? | Visible Outside Container? | Use For |
|----------|-------------|----------------------------|---------|
| `/workspace/` | ✓ Yes | ✓ Yes (`~/workspace/`) | All important work |
| `/root/` | ✗ No | ✗ No | Temporary config |
| `/tmp/` | ✗ No | ✗ No | Scratch space |
| `/opt/conda/` | ✗ No (from image) | ✗ No | Python packages (baked in) |
| `/usr/bin/` | ✗ No (from image) | ✗ No | System binaries (baked in) |

**Rule of thumb:** If you want it next time, put it in `/workspace/`.

---

## Troubleshooting

### "Where did my files go?"

**Check if they were in workspace:**
```bash
# Were they here?
ls /workspace/my-thesis/

# Or here?
ls ~  # If so, they're gone
```

**Prevention:**
```bash
# Always work in workspace
cd /workspace/my-thesis
# Check before saving
pwd
```

### "Workspace is full"

**Check usage:**
```bash
du -sh ~/workspace/*
```

**Find space hogs:**
```bash
du -h ~/workspace/ | sort -h | tail -20
```

**Clean up:**
```bash
# Remove old checkpoints
# Compress datasets
# Archive finished projects
```

### "Can't see workspace files in container"

**Check mount:**
```bash
# Inside container
ls /workspace/
mount | grep workspace
```

**If empty, relaunch:**
```bash
exit
container retire my-project
project launch my-project
```

---

## Next Steps

**Understand why containers are temporary:**

→ [Ephemeral Container Model](ephemeral-containers.md)

**Learn about images vs containers:**

→ [Containers and Images](containers-and-images.md)

**Apply this knowledge:**

→ [Daily Workflow](../getting-started/daily-workflow.md)

→ [Creating Projects](../guides/creating-projects.md)

---

**Remember: `/workspace/` is permanent, everything else is temporary.**
