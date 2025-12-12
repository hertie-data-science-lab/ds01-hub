# Complete Dockerfile Guide

Advanced Docker image building for DS01. This guide covers everything from basic Dockerfiles to optimization strategies.

---

## Basic Dockerfile Structure

```dockerfile
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04

WORKDIR /workspace

# Install system packages
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    transformers \
    datasets \
    wandb

# Optional: Copy configuration
COPY config/ /workspace/config/

CMD ["/bin/bash"]
```

---

## Layer Optimization

### Combine Commands

Each `RUN` instruction creates a layer. Combining commands into single `RUN` statements reduces layer count and final image size.

```dockerfile
# Bad: Multiple layers
RUN pip install numpy
RUN pip install pandas
RUN pip install scikit-learn

# Good: Single layer
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scikit-learn
```

### Order by Change Frequency

Place rarely-changing commands early (they cache), frequently-changing commands late:

```dockerfile
# Rarely changes (cache hit)
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04
RUN apt-get update && apt-get install -y system-deps \
    && rm -rf /var/lib/apt/lists/*

# Sometimes changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Frequently changes (put last)
COPY src/ /workspace/src/
```

---

## Reducing Image Size

### Clean Up in Same Layer

Package manager caches only disappear if cleanup is in the same `RUN` layer:

```dockerfile
# Bad: Cleanup in separate layer (doesn't reduce size)
RUN apt-get update && apt-get install -y build-essential
RUN rm -rf /var/lib/apt/lists/*

# Good: Clean in same layer
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*
```

### Use --no-cache-dir

Pip caches downloaded wheels. Disabling this saves space in the image (packages are already installed):

```dockerfile
RUN pip install --no-cache-dir transformers
```

### Exclude Unnecessary Files with .dockerignore

Create `.dockerignore` in the same directory as your Dockerfile:

```
# Large files that don't belong in image
data/
models/
*.csv
*.pt
*.zip

# Development artifacts
__pycache__/
.git/
.pytest_cache/
*.pyc
```

---

## Multi-Stage Builds

For packages requiring compilation, use multi-stage builds to keep final image small:

```dockerfile
# Build stage: Compile packages
FROM python:3.10 AS builder
RUN pip wheel --no-deps --wheel-dir /wheels some-compiled-package

# Final stage: Use pre-built wheels
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
```

**Benefit:** Final image only contains compiled wheels, not build tools.

---

## Caching & Performance

### Requirements File Strategy

```dockerfile
# Copy requirements first (caches if unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy code (changes often, doesn't invalidate pip cache)
COPY src/ /workspace/src/
```

This way, if only your code changes, Docker reuses the pip-install layer from cache.

### Pin Versions for Reproducibility

```
# requirements.txt
torch==2.0.1
transformers==4.30.0
datasets==2.14.0
```

Pinned versions ensure:
- Same image every time you rebuild
- Other team members get identical environment
- Production deployments are reproducible

---

## Common Installation Patterns

### Installing PyPI Packages

```dockerfile
RUN pip install --no-cache-dir \
    package1==1.0.0 \
    package2>=2.0.0 \
    package3
```

### Installing from Git

```dockerfile
RUN pip install --no-cache-dir \
    git+https://github.com/user/repo.git@v1.0.0
```

### System Dependencies

```dockerfile
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
```

### Environment Variables

```dockerfile
# Prevent Python buffering (see logs immediately)
ENV PYTHONUNBUFFERED=1

# Disable parallel tokenization (can cause issues with large files)
ENV TOKENIZERS_PARALLELISM=false

# Specify GPU (optional, can override at runtime)
ENV CUDA_VISIBLE_DEVICES=0
```

---

## Debugging Builds

### Build with Progress Output

```bash
docker build --progress=plain -f my-project.Dockerfile .
```

Shows all build steps and output in real-time (useful for debugging).

### Interactive Debugging

```bash
# Build up to failing layer
docker build -t debug-image .

# Enter container and debug interactively
docker run -it debug-image /bin/bash

# Try commands until you find fix
pip install fixed-package
```

Once you find the fix, add it to your Dockerfile.

### Check Layer Sizes

```bash
docker history ds01-user/my-project:latest
```

Shows size of each layer, helps identify which layers are bloated.

---

## DS01 Base Images

### Available Bases

```
henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04
henrycgbaker/aime-tensorflow:2.16-cuda12.4-ubuntu22.04
henrycgbaker/aime-jax:0.4.23-cuda12.4-ubuntu22.04
```

### What's Included

- **CUDA drivers & toolkit:** GPU drivers pre-installed and version-matched. You don't need to figure out CUDA compatibility - it's already tested and working.

- **cuDNN:** NVIDIA's deep learning library for GPU operations. Required by PyTorch/TensorFlow for GPU training. Version-matched to CUDA.

- **ML framework:** PyTorch, TensorFlow, or JAX pre-compiled with GPU support. `torch.cuda.is_available()` returns `True` immediately.

- **Jupyter Lab:** Pre-installed and configured. Run `jupyter lab --ip=0.0.0.0` for notebook-based development with GPU access.

- **Common tools:** Git, wget, curl, vim, htop, and utilities. Plus pip and conda ready to use.

---

## Example: ML Project

Training models with transformers, datasets, wandb tracking:

```dockerfile
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04

WORKDIR /workspace

# System dependencies
RUN apt-get update && apt-get install -y \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Environment
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=false
```

---

## Example: Data Science

Analysis and visualization with pandas, scikit-learn, plotting libraries:

```dockerfile
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04

WORKDIR /workspace

# Visualization system dependencies
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Data science stack
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    matplotlib \
    seaborn \
    plotly \
    jupyter
```

---

## Building & Testing

### Build Your Image

```bash
# Basic build
docker build -t ds01-$(whoami)/my-project:latest -f ~/dockerfiles/my-project.Dockerfile .

# Rebuild from scratch (ignore cache)
docker build --no-cache -t ds01-$(whoami)/my-project:latest -f ~/dockerfiles/my-project.Dockerfile .
```

### Test the Image

```bash
# Run container to test
docker run -it ds01-$(whoami)/my-project:latest

# Inside container, verify packages installed
python -c "import torch; print(torch.cuda.is_available())"
pip list | grep transformers
```

---

## See Also

- [Custom Images Guide](../core-guides/custom-images.md) - User workflow for building images
- [Custom Environments](../core-guides/custom-environments.md) - Interactive installation methods
- [Image Commands](../reference/commands/image-commands.md) - `image-create`, `image-update`, `image-delete`
- [Docker Direct](docker-direct.md) - Using Docker commands directly
