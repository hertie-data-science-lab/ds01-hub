# Dockerfile Guide

Advanced Docker image building for DS01.

## Basic Dockerfile

```dockerfile
FROM henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04
WORKDIR /workspace

# Install packages
RUN pip install --no-cache-dir \
    transformers \
    datasets \
    accelerate

# Expose Jupyter port
EXPOSE 8888

CMD ["/bin/bash"]
```

## Best Practices

### Use --no-cache-dir

```dockerfile
RUN pip install --no-cache-dir package1 package2
```

**Why:** Reduces image size

### Combine RUN Commands

```dockerfile
# Good
RUN pip install pkg1 pkg2 pkg3

# Bad (creates more layers)
RUN pip install pkg1
RUN pip install pkg2
RUN pip install pkg3
```

### Pin Versions

```dockerfile
RUN pip install \
    torch==2.8.0 \
    transformers==4.30.0
```

**Why:** Reproducibility

## Multi-Stage Builds

```dockerfile
# Stage 1: Build
FROM python:3.10 as builder
RUN pip install --user package

# Stage 2: Runtime
FROM henrycgbaker/aime-pytorch:2.8.0
COPY --from=builder /root/.local /root/.local
```

**Benefit:** Smaller final image

## Building Images

```bash
# Build
docker build -t ds01-$(whoami)/my-project:latest -f ~/dockerfiles/my-project.Dockerfile .

# No cache (full rebuild)
docker build --no-cache -t ds01-$(whoami)/my-project:latest -f ~/dockerfiles/my-project.Dockerfile .
```

## Next Steps

→ [Building Custom Images](../guides/custom-images.md)
→ [Best Practices](best-practices.md)
