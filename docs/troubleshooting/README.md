# Troubleshooting

Find your problem below and jump to the solution.

---

## Quick Symptom Index

### Container Problems
| Symptom | Go to |
|---------|-------|
| Container won't start | [container-issues.md#wont-start](container-issues.md#wont-start) |
| Container stopped unexpectedly | [container-issues.md#stopped-unexpectedly](container-issues.md#stopped-unexpectedly) |
| Can't find my container | [container-issues.md#not-found](container-issues.md#not-found) |
| Container is slow | [container-issues.md#performance](container-issues.md#performance) |

### GPU Problems
| Symptom | Go to |
|---------|-------|
| "No GPUs available" | [gpu-issues.md#no-gpus](gpu-issues.md#no-gpus) |
| "CUDA out of memory" | [gpu-issues.md#cuda-oom](gpu-issues.md#cuda-oom) |
| nvidia-smi not found | [gpu-issues.md#nvidia-smi-not-found](gpu-issues.md#nvidia-smi-not-found) |
| GPU not detected in PyTorch/TensorFlow | [gpu-issues.md#framework-detection](gpu-issues.md#framework-detection) |

### Image Problems
| Symptom | Go to |
|---------|-------|
| Image build fails | [image-issues.md#build-fails](image-issues.md#build-fails) |
| Package not found | [image-issues.md#package-not-found](image-issues.md#package-not-found) |
| Image too large | [image-issues.md#image-size](image-issues.md#image-size) |

### File & Permission Problems
| Symptom | Go to |
|---------|-------|
| Can't find my files | [common-errors.md#files-missing](common-errors.md#files-missing) |
| Permission denied | [common-errors.md#permission-denied](common-errors.md#permission-denied) |
| Out of disk space | [common-errors.md#disk-space](common-errors.md#disk-space) |

### Network & Access Problems
| Symptom | Go to |
|---------|-------|
| Can't access Jupyter | [common-errors.md#jupyter-access](common-errors.md#jupyter-access) |
| Commands not found | [common-errors.md#commands-not-found](common-errors.md#commands-not-found) |
| Docker permission denied | [common-errors.md#docker-permission](common-errors.md#docker-permission) |

---

## General Recovery Steps

If you're stuck, try these in order:

```bash
# 1. Check what's running
container-list

# 2. Check container logs
docker logs my-project._.$(whoami)

# 3. Check system status
ds01-health-check

# 4. Recreate container
container-retire my-project
container-deploy my-project
```

Your workspace files are **always safe** - recreating a container won't lose data.

---

## Still Stuck?

Raise an issue ticket in [ds01-hub repo](https://github.com/hertie-data-science-lab/ds01-hub/issues)
