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

### Best Practice
Simplest, most robust:
```
Keep `requirements.txt` file up to date with any new pkg requirements, then use `image update` CLI to scan that and update. DS01 has developed this CLI abstrats this complexity layer away.
```

**Edit Dockerfile:**
```bash
vim ~/dockerfiles/my-project.Dockerfile
```

**Add packages:**
```dockerfile
RUN pip install transformers datasets accelerate
```

**Rebuild:**
```bash
image-update my-project            # Interactive mode
image-update my-project --rebuild  # Rebuild without prompts
```

## Base Images

**Available frameworks:**
- PyTorch 2.8.0 (CUDA 12.4)
- TensorFlow 2.16.1 (CUDA 12.3)
- JAX 0.4.23 (CUDA 12.3)

## Next Steps

- → [Dockerfile Guide](../advanced/dockerfile-guide.md)
- → [Daily Usage Patterns](daily-usage.md)
