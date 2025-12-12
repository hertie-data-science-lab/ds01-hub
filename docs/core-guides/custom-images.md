# Building Custom Images

Guide to creating and managing custom Docker images on DS01.

## Quick Build

```bash
image-create my-project
```

**Interactive wizard guides you through:**
1. Phase 1: Choose framework (PyTorch, TensorFlow, JAX)
2. Phase 2: Add Jupyter Lab
3. Phase 3: Add data science packages
4. Phase 4: Add custom packages

## Dockerfile Location

```bash
~/dockerfiles/my-project.Dockerfile
```

## Adding Packages

### Recommended: Interactive GUI

```bash
image-update                  # Select image, add/remove packages
```

The interactive GUI lets you:
- View current packages
- Add Python packages (pip)
- Add system packages (apt)
- Import from requirements.txt
- Rebuild automatically

### Advanced: Edit Dockerfile Directly

```bash
vim ~/dockerfiles/my-project.Dockerfile
# Add: RUN pip install transformers datasets accelerate

# Then rebuild:
image-update my-project --rebuild
# Or: docker build -t ds01-<uid>/my-project:latest -f ~/dockerfiles/my-project.Dockerfile ~/dockerfiles/
```

## Base Images

**Available frameworks:**
- PyTorch 2.8.0 (CUDA 12.4)
- TensorFlow 2.16.1 (CUDA 12.3)
- JAX 0.4.23 (CUDA 12.3)

## Next Steps

- → [Dockerfile Guide](../advanced/dockerfile-guide.md)
- → [Daily Usage Patterns](daily-usage.md)
