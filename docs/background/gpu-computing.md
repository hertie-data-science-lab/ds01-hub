# GPU Computing

Understanding GPUs, CUDA, and MIG partitioning for DS01.

## Why GPUs for Machine Learning?

**CPUs:** General-purpose, serial processing
**GPUs:** Specialized for parallel operations (matrix multiplications)

**ML workloads are highly parallel:**
- Matrix multiplications (core of neural networks)
- Thousands of operations simultaneously
- GPUs are 10-100x faster than CPUs for training

## DS01 GPUs

**Hardware:** NVIDIA A100/H100 data center GPUs
- 40-80GB GPU memory
- Tensor cores for ML acceleration
- MIG partitioning support

## MIG (Multi-Instance GPU)

**What is MIG?**
- Partitions single GPU into multiple instances
- Each instance = isolated GPU with own memory
- Enables fair sharing

**DS01 MIG configuration:**
- A100 GPU → 3 MIG instances
- Each instance: ~20GB memory
- Tracked as `gpu:instance` (e.g., `0:0`, `0:1`, `0:2`)

## Checking GPU Usage

**Inside container:**
```bash
# Basic info
nvidia-smi

# Continuous monitoring
watch -n 1 nvidia-smi

# GPU memory
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

## CUDA

**CUDA:** NVIDIA's parallel computing platform
- Required for GPU acceleration
- Included in DS01 images
- Version must match PyTorch/TensorFlow requirements

**Check CUDA:**
```bash
nvcc --version  # CUDA compiler
nvidia-smi      # Driver version
```

## Next Steps

→ [Working with GPUs](../guides/gpu-usage.md)
→ [Resource Management](../background/resource-management.md)
