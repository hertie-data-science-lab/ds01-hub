# Custom Environments

Build and customise Docker images for your specific research needs.

> **Key concept:** DS01 containers ARE your Python environment - you don't need venv or conda inside containers. See [Python Environments in Containers](../key-concepts/python-environments.md) for why.

---

## Two Approaches

DS01 supports two ways to customise your environment:

| Approach | Speed | Reproducibility | Version Controlled | Best For |
|----------|-------|-----------------|-------------------|----------|
| **Edit Dockerfile** | Slower (rebuild) | ✓ Full | ✓ Yes | Research, collaboration, long-term projects |
| **Quick install** | Fast (pip in running container)* | Partial | Limited | Quick experiments, testing packages |

The '*Quick Install' method involves adding new pkgs to your running container using pip/apt, then saving the pkg changes back into your image when you retire the container. This is offered by default in the `container retiree` workflow, which uses `docker commit` under the hood. This is fine for adding new packages, but not recommended for ongoing projects.


**Recommendation:** Use Dockerfiles for research work - they're shareable, reproducible, and version-controlled. `image update` will handle this for you.

---

# Best Practice
Simplest, most robust:
```
Keep `requirements.txt` file up to date with any new pkg requirements, then use `image update` CLI to scan that and update.

DS01 has developed this CLI for you that handles all of the below on your behalf. 

The below, is just what is being done under the hood, or if you want more granular control.
```
---

## Dockerfile Method (Recommended)

**Best practice for reproducible research.**

### Where Dockerfiles Live

```bash
~/workspace/my-project/Dockerfile
```

**Each project has its own Dockerfile** - version controlled with your code.

### Step 1: Edit Dockerfile

```bash
# Edit your project's Dockerfile
vim ~/workspace/my-thesis/Dockerfile
```

**Example: Add Transformers packages**

```dockerfile
FROM aime/pytorch:2.8.0-cuda12.4

# Install Python packages
RUN pip install --no-cache-dir \
    transformers>=4.30.0 \
    datasets>=2.12.0 \
    accelerate>=0.20.0 \
    bitsandbytes>=0.41.0

# Install system packages if needed
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Configure Jupyter (optional)
RUN pip install jupyterlab ipywidgets

WORKDIR /workspace
```

### Step 2: Rebuild Image

```bash
image-update my-thesis --rebuild   # Rebuild without prompts
# Or use: docker build -t ds01-<uid>/my-thesis:latest ~/workspace/my-thesis/
```

**What happens:**
- Reads `~/workspace/my-thesis/Dockerfile`
- Builds new Docker image
- Tags as `ds01-username/my-thesis:latest`
- Old image replaced

**Time:** 5-10 minutes (depends on packages)

> **Note:** Most users should use `image-update` (interactive GUI) instead of editing Dockerfiles directly. See [Option 2](#option-2-use-image-update) below.

### Step 3: Recreate Container

```bash
# Launch with new image
project launch my-thesis --open
```

**Your workspace files are safe** - only container is recreated.

### Step 4: Verify Packages

```bash
# Inside container
python -c "import transformers; print(transformers.__version__)"
```

---

## Quick Install Method (quick fix during experimentation)

**For rapid experimentation** - install packages into running container, save later.

### Install in Running Container

```bash
# Launch container
project launch my-project --open

# Inside container: Install packages
pip install transformers datasets

# Use them immediately
python
>>> import transformers
>>> # Works!
```

### Option 1: Save to Image (Quick, Non-Reproducible)

When you retire a container, DS01 automatically detects newly installed packages and offers to save them via docker commit:

```bash
# Exit container
exit

# Retire - will prompt to save if new packages detected
container retire my-project
```
*The interactive prompt offers to commit changes to the image*

**What happens:**
- If new packages detected, prompts to commit container changes to image
- New containers get these packages
- **BUT:** Not in Dockerfile, not version-controlled, not shareable

**Trade-offs:**
- Fast - no rebuild needed
- Not reproducible - colleagues don't know what's installed
- Not version-controlled - can't track changes
- Image bloat - auto-cleanup may remove dangling layers

### Option 2: Use `image-update` (Recommended)

**Best Approach:**

```bash
# 1. Note what you installed
pip list | grep transformers
# transformers==4.30.2

# 2. Exit and use interactive package manager
exit
image-update                  # Select image, add "transformers==4.30.2"

# 3. Recreate container
project launch my-project
```

**Trade-offs:**
- ✓ Reproducible - changes saved to Dockerfile
- ✓ Version controlled - tracked in git
- ✓ Shareable - colleagues can rebuild
- ✓ User-friendly - no manual Dockerfile editing
- ✗ Slower - requires rebuild

### Option 3: Edit Dockerfile Directly (Advanced)

**For advanced users who prefer manual control:**

```bash
# 1. Note what you installed
pip list | grep transformers
# transformers==4.30.2

# 2. Exit and edit Dockerfile
exit
vim ~/workspace/my-project/Dockerfile
# Add: RUN pip install transformers>=4.30.0

# 3. Rebuild image
image-update my-project --rebuild
# Or: docker build -t ds01-<uid>/my-project:latest ~/workspace/my-project/

# 4. Recreate container
project launch my-project
```

---

## Common Customisation Patterns

### Adding ML Libraries

```dockerfile
# Computer Vision
RUN pip install --no-cache-dir \
    opencv-python \
    Pillow \
    albumentations \
    timm

# NLP
RUN pip install --no-cache-dir \
    transformers \
    datasets \
    tokenizers \
    sentencepiece \
    spacy

# General ML
RUN pip install --no-cache-dir \
    scikit-learn \
    xgboost \
    lightgbm \
    catboost
```

### Adding System Packages

```dockerfile
RUN apt-get update && apt-get install -y \
    vim \
    tmux \
    htop \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*
```

**Note:** Always clean up apt cache (`rm -rf /var/lib/apt/lists/*`) to keep images small.

### Installing from Requirements File

```dockerfile
# Copy requirements into image
COPY requirements.txt /tmp/requirements.txt

# Install from file
RUN pip install --no-cache-dir -r /tmp/requirements.txt
```

**On host, create `requirements.txt`:**
```bash
echo "transformers>=4.30.0" > ~/workspace/my-project/requirements.txt
echo "datasets>=2.12.0" >> ~/workspace/my-project/requirements.txt
```

### Pinning Package Versions

```dockerfile
# Exact version (most reproducible)
RUN pip install torch==2.0.1

# Minimum version (more flexible)
RUN pip install torch>=2.0.0

# Version range
RUN pip install "torch>=2.0.0,<2.2.0"
```

**Best practice:** Use `>=` for research (get bug fixes), exact versions for production.

### Installing from GitHub

```dockerfile
# Install specific commit/branch
RUN pip install git+https://github.com/huggingface/transformers.git@main

# Or specific tag
RUN pip install git+https://github.com/huggingface/transformers.git@v4.30.0
```

---

## Managing Multiple Environments

**Each project can have different packages:**

```bash
# Project 1: PyTorch + Vision
~/workspace/cv-project/
  └── Dockerfile  # torchvision, OpenCV, Pillow

# Project 2: TensorFlow + NLP
~/workspace/nlp-project/
  └── Dockerfile  # transformers, spacy

# Project 3: Reinforcement Learning
~/workspace/rl-project/
  └── Dockerfile  # gym, stable-baselines3
```

**Switching is seamless:**
```bash
project launch cv-project       # Uses CV environment
exit
project launch nlp-project      # Uses NLP environment
```

---

## Viewing Current Packages

```bash
# Inside container
pip list

# Specific package
pip show transformers

# Packages not in base image
pip list --not-required
```

---

## Troubleshooting

### "Package not found" After Rebuild

**Symptom:** Added package to Dockerfile, rebuilt, but `import` fails in container.

**Causes:**
1. **Using old container** - need to recreate
2. **Typo in package name**
3. **Package installation failed** (check build logs)

**Fix:**
```bash
# Always recreate after rebuild
container retire my-project
project launch my-project --open

# Check build logs if package missing
image-update my-project 2>&1 | grep -A 5 "ERROR"
```

### "Build failed: No space left"

**Cause:** Docker images filling disk.

**Fix:**
```bash
# Remove unused images
docker image prune -a

# Remove specific old image
image-delete old-project-name
```

### "Cannot import package installed with pip"

**Inside container, you used `pip install foo`, but after recreating, it's gone.**

**Cause:** Package not in Dockerfile - only existed in removed container.

**Fix:** Use `image-update` to add the package permanently:
```bash
image-update                  # Select image, add "foo"
```

**Advanced:** Edit Dockerfile directly:
```bash
vim ~/workspace/my-project/Dockerfile
# Add: RUN pip install foo
image-update my-project --rebuild
```

### "Package conflict" During Build

**Symptom:**
```
ERROR: transformers 4.35.0 requires tokenizers>=0.14, but you have tokenizers 0.13.0
```

**Fix:** Specify compatible versions:
```dockerfile
RUN pip install --no-cache-dir \
    transformers>=4.35.0 \
    tokenizers>=0.14.0
```

Or let pip resolve:
```dockerfile
RUN pip install --no-cache-dir transformers
# Automatically installs compatible tokenizers
```

---

## Base Images

**DS01 provides AIME base images:**

| Base Image | Framework | CUDA | Python |
|------------|-----------|------|--------|
| `aime/pytorch:2.8.0-cuda12.4` | PyTorch 2.8.0 | 12.4 | 3.11 |
| `aime/tensorflow:2.16.1-cuda12.3` | TensorFlow 2.16.1 | 12.3 | 3.11 |
| `aime/jax:0.4.23-cuda12.3` | JAX 0.4.23 | 12.3 | 3.11 |

**What's included in base images:**
- CUDA + cuDNN
- Framework (PyTorch/TensorFlow/JAX)
- Basic tools (git, vim, wget, curl)
- Common libraries (numpy, pandas, matplotlib)

**Check what's in your base:**
```bash
# Inside container from fresh image
pip list
dpkg -l  # System packages
```

---

## Image Commands Reference

```bash
# Create new image
image-create my-project

# List your images
image-list

# Update image (interactive GUI - recommended)
image-update                  # Select image, add/remove packages

# Rebuild image after manual Dockerfile edit (advanced)
image-update my-project --rebuild

# Delete image
image-delete old-project
```

**Quick package update:**
```bash
# Add packages to image (updates Dockerfile and rebuilds)
image-update my-project --add "transformers datasets"
```

---

## Best Practices

### 1. Keep Dockerfiles in Version Control

```bash
cd ~/workspace/my-project
git add Dockerfile
git commit -m "Add transformers for BERT experiments"
git push
```

**Benefits:**
- Colleagues can reproduce your environment
- Track what changed over time
- Rollback if package breaks something

### 2. Comment Your Dockerfile

```dockerfile
# Fine-tuning BERT models
RUN pip install transformers datasets

# Data augmentation for images
RUN pip install albumentations

# Experiment tracking
RUN pip install wandb tensorboard
```

**Future you will thank present you.**

### 3. Group Related Packages

```dockerfile
# Bad - many RUN commands (slow, large image)
RUN pip install transformers
RUN pip install datasets
RUN pip install tokenizers

# Good - one RUN command (fast, smaller image)
RUN pip install --no-cache-dir \
    transformers \
    datasets \
    tokenizers
```

### 4. Use `--no-cache-dir`

```dockerfile
RUN pip install --no-cache-dir transformers
```

**Why:** Saves ~50MB per image - pip cache not needed in container.

### 5. Clean Up After apt-get

```dockerfile
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

**Why:** Removes package cache, keeps image smaller.

### 6. Test Locally First

```bash
# Install in running container
project launch test-env --open
pip install some-new-package

# Test it works
python -c "import some_new_package"

# Then add to Dockerfile
exit
vim ~/workspace/test-env/Dockerfile
```

---

## Workflow Comparison

### Dockerfile Workflow (Reproducible)
```
Edit Dockerfile → Rebuild image → Recreate container → Use new packages
```

**Time:** 10-15 minutes total

**When:** Research work, collaboration, long-term projects

### Quick Install Workflow (Fast)
```
Install in container → Save to image → Done
```

**Time:** 1 minute

**When:** Quick experiments, testing packages, one-off needs

**Convert to Dockerfile later:**
```bash
# After quick install testing, make it permanent
pip list | grep package-name  # Check version
image-update                  # Add package to image via GUI
```

---

## Advanced Topics

### Multi-Stage Builds

**Build tools in one stage, copy results to another (smaller final image):**

```dockerfile
# Build stage
FROM aime/pytorch:2.8.0-cuda12.4 AS builder
RUN pip install --no-cache-dir transformers
RUN pip download --dest /packages some-large-package

# Final stage
FROM aime/pytorch:2.8.0-cuda12.4
COPY --from=builder /packages /packages
RUN pip install --no-cache-dir /packages/*
```

**Rarely needed for DS01** - only if building from source.

### Environment Variables

```dockerfile
# Set environment variables
ENV TRANSFORMERS_CACHE=/workspace/.cache/transformers
ENV HF_HOME=/workspace/.cache/huggingface

# Use in Python
# Cache stored in workspace (persistent)
```

### Custom Jupyter Extensions

```dockerfile
# Install Jupyter extensions
RUN pip install jupyterlab ipywidgets jupyter-book

# Enable extensions
RUN jupyter nbextension enable --py widgetsnbextension
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

---

## Next Steps

**Launch with your custom environment:**
```bash
project launch my-project --open
```

**Learn more Docker:**

- → [Complete Dockerfile Guide](../advanced/dockerfile-complete-guide.md)

**Set up development tools:**

- → [Jupyter Setup](jupyter.md)

- → [VS Code Remote](vscode-remote.md)

**Understand the concepts:**

- → [Containers and Images](../key-concepts/containers-and-images.md)
