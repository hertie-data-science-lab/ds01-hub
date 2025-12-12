# Multi-MIG Training Guide

## The CUDA/MIG Limitation

When you request multiple MIG partitions for a container, you might expect PyTorch or TensorFlow to see multiple GPUs. **This is not how MIG works.**

### The Reality

| What you might expect | What actually happens |
|----------------------|----------------------|
| Request 4 MIGs → 4 GPUs in PyTorch | Request 4 MIGs → **1 GPU** in PyTorch |
| 4 × 10GB = 40GB usable VRAM | 1 × 10GB = **10GB** usable VRAM |
| Data parallel across 4 devices | Single device only |

### Why?

This is a **CUDA limitation**, not a bug in DS01, PyTorch, or TensorFlow.

From [NVIDIA's official documentation](https://forums.developer.nvidia.com/t/how-to-use-cuda-visible-devices-for-mig-instances/195069):

> **"CUDA can only enumerate a single compute instance."**

When you set `NVIDIA_VISIBLE_DEVICES` to multiple MIG UUIDs:
- `nvidia-smi` shows all MIG devices ✓
- `torch.cuda.device_count()` returns **1** ✗
- Accessing `cuda:1` fails ✗

Additionally, MIG mode **disables GPU-to-GPU P2P communication** (both NVLINK and PCIe), so even if CUDA could see multiple MIGs, NCCL distributed training would not work.

---

## When to Use Multi-MIG

Multi-MIG allocation **is still useful** for running multiple independent processes:

### Use Case 1: Hyperparameter Sweeps

Run 4 experiments in parallel, each on its own MIG:

```bash
#!/bin/bash
# hyperparameter_sweep.sh

LEARNING_RATES="0.001 0.0001 0.00001 0.000001"
MIG_DEVICES=$(echo $NVIDIA_VISIBLE_DEVICES | tr ',' ' ')

i=0
for lr in $LEARNING_RATES; do
    MIG=$(echo $MIG_DEVICES | cut -d' ' -f$((i+1)))
    echo "Starting training with lr=$lr on MIG $MIG"
    CUDA_VISIBLE_DEVICES=$MIG python train.py --lr=$lr --output=results_$lr.json &
    pids[$i]=$!
    i=$((i+1))
done

# Wait for all to complete
for pid in ${pids[@]}; do
    wait $pid
done

echo "All experiments complete!"
```

### Use Case 2: Ensemble Training

Train multiple models simultaneously:

```bash
#!/bin/bash
# ensemble_train.sh

MODELS="resnet50 efficientnet vgg16 densenet"
MIG_DEVICES=$(echo $NVIDIA_VISIBLE_DEVICES | tr ',' ' ')

i=0
for model in $MODELS; do
    MIG=$(echo $MIG_DEVICES | cut -d' ' -f$((i+1)))
    CUDA_VISIBLE_DEVICES=$MIG python train.py --model=$model &
    i=$((i+1))
done
wait
```

### Use Case 3: MPI-based Distributed Training

For advanced users who need true distributed training across MIG instances:

```python
# mpi_train.py
import os
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Each MPI rank gets one MIG
mig_devices = os.environ.get('NVIDIA_VISIBLE_DEVICES', '').split(',')
if rank < len(mig_devices):
    os.environ['CUDA_VISIBLE_DEVICES'] = mig_devices[rank]

import torch
# Now torch.cuda.device_count() == 1, but each rank has its own MIG

# Your training code here...
# Use MPI for gradient synchronisation instead of NCCL
```

Launch with:
```bash
mpirun -np 4 python mpi_train.py
```

---

## When to Use Full GPU Instead

If you need **more than 10GB VRAM** for a single model/batch:

| Your Need | Solution |
|-----------|----------|
| Large batch sizes | Request **full GPU** (40GB) |
| Large models (LLMs, ViTs) | Request **full GPU** (40GB) |
| Standard distributed training (DDP) | Request **full GPU** (40GB) |
| Multiple small experiments | Request **multiple MIGs** |

### Requesting a Full GPU

```bash
container-create my-project --num-migs=4 --prefer-full
```

With `--prefer-full`, DS01 will allocate an unpartitioned full GPU (40GB) if available, instead of 4 separate MIG partitions.

---

## Checking Your Allocation

Inside your container:

```python
import torch
import os

print("NVIDIA_VISIBLE_DEVICES:", os.environ.get('NVIDIA_VISIBLE_DEVICES'))
print("PyTorch sees:", torch.cuda.device_count(), "device(s)")

if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print(f"Device 0: {props.name}")
    print(f"Memory: {props.total_memory / 1024**3:.1f} GB")
```

**Expected output for MIG:**
```
NVIDIA_VISIBLE_DEVICES: MIG-xxxx-xxxx
PyTorch sees: 1 device(s)
Device 0: NVIDIA A100-PCIE-40GB MIG 1g.10gb
Memory: 9.6 GB
```

**Expected output for Full GPU:**
```
NVIDIA_VISIBLE_DEVICES: GPU-xxxx-xxxx
PyTorch sees: 1 device(s)
Device 0: NVIDIA A100-PCIE-40GB
Memory: 39.4 GB
```

---

## References

- [NVIDIA MIG User Guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/)
- [NVIDIA Forums: CUDA_VISIBLE_DEVICES with MIG](https://forums.developer.nvidia.com/t/how-to-use-cuda-visible-devices-for-mig-instances/195069)
- [PyTorch Forums: Multiple MIG Instances](https://discuss.pytorch.org/t/how-can-i-use-multiple-mig-instances-with-pytorch/190488)
- [GMU HPC: Slurm with Multiple MIG Devices](https://wiki.orc.gmu.edu/mkdocs/slurm_with_multiple_mig_devices/)
