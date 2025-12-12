# Dockerfile Best Practices

Writing efficient, maintainable Dockerfiles for DS01.

---

## Basic Structure

```dockerfile
# Start from AIME base
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04

# Set working directory
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

# Copy configuration (optional)
COPY config/ /workspace/config/
```

---

## Layer Optimisation

### Combine Commands

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

```dockerfile
# Rarely changes (cache hit)
FROM base-image
RUN apt-get install system-deps

# Sometimes changes
RUN pip install requirements

# Frequently changes (put last)
COPY src/ /workspace/src/
```

---

## Reducing Image Size

### Clean Up in Same Layer

```dockerfile
# Bad: Cleanup in separate layer (doesn't reduce size)
RUN apt-get update && apt-get install -y build-essential
RUN rm -rf /var/lib/apt/lists/*

# Good: Clean in same layer
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*
```

### Use --no-cache-dir

```dockerfile
RUN pip install --no-cache-dir transformers
```

### Don't Copy Unnecessary Files

Create `.dockerignore`:
```
data/
models/
*.csv
*.pt
__pycache__/
.git/
```

---

## Multi-Stage Builds

For packages that need compilation:

```dockerfile
# Build stage
FROM python:3.10 AS builder
RUN pip wheel --no-deps --wheel-dir /wheels some-package

# Final stage
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
```

---

## Caching Strategies

### Requirements File

```dockerfile
# Copy requirements first (caches if unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy code (changes often)
COPY src/ /workspace/src/
```

### requirements.txt

```
# Pin versions for reproducibility
torch==2.0.1
transformers==4.30.0
datasets==2.14.0
```

---

## Common Patterns

### Installing PyPI Packages

```dockerfile
RUN pip install --no-cache-dir \
    package1==1.0.0 \
    package2>=2.0.0
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
    && rm -rf /var/lib/apt/lists/*
```

### Environment Variables

```dockerfile
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0
```

---

## Debugging Builds

### Build with Progress

```bash
docker build --progress=plain -f my-project.Dockerfile .
```

### Interactive Debugging

```bash
# Build up to failing layer
docker build -t debug-image .

# Enter and debug
docker run -it debug-image /bin/bash
```

### Check Layer Sizes

```bash
docker history ds01-user/my-project:latest
```

---

## DS01 Base Images

Available bases:
```
henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04
henrycgbaker/aime-tensorflow:2.16-cuda12.4-ubuntu22.04
henrycgbaker/aime-jax:0.4.23-cuda12.4-ubuntu22.04
```

These include:

- **CUDA drivers:** The GPU drivers and CUDA toolkit are pre-installed and version-matched. You don't need to figure out which CUDA version works with which driver version - it's already configured and tested.

- **cuDNN:** NVIDIA's deep learning primitives library for GPU-accelerated neural network operations. Required by PyTorch and TensorFlow for GPU training. Version-matched to the CUDA version in the image.

- **ML framework:** PyTorch, TensorFlow, or JAX depending on which base you choose. Pre-compiled with GPU support, so `torch.cuda.is_available()` returns `True` immediately - no wrestling with CUDA compilation.

- **Jupyter Lab:** Pre-installed and configured to work with the ML framework's kernel. Run `jupyter lab --ip=0.0.0.0` and you're ready for notebook-based development with GPU access.

- **Common tools:** Git, wget, curl, vim, htop, and other utilities you'd otherwise need to install yourself. Plus Python package managers (pip, conda) ready to use.

---

## Example: ML Project

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

```dockerfile
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04

WORKDIR /workspace

# Visualisation dependencies
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
    plotly
```

---

## See Also

- [Custom Images Guide](../core-guides/custom-images.md)
- [Image Commands](../reference/commands/image-commands.md)
- [Docker Direct](docker-direct.md)
