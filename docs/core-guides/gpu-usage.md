# Working with GPUs

Practical guide to GPU usage on DS01.

## Requesting GPUs

*NB: this is mostly applicable to PhDs, PostDocs, Researchers and studetns who have been given access to more than 1 full GPU. Most MDS students by default, do NOT have access to multiple full GPUs.*

```bash
# Request 1 GPU (default)
container-deploy my-project

# Request multiple GPUs
container-deploy my-project --gpu 2
```

## Monitoring GPU Usage

**Inside container:**
```bash
# Basic info
nvidia-smi

# Continuous monitoring
watch -n 1 nvidia-smi

# Memory usage
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

## Using GPUs in Code

**PyTorch:**
```python
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
data = data.to(device)
```

**TensorFlow:**
```python
import tensorflow as tf

# List GPUs
print(tf.config.list_physical_devices('GPU'))

# Use GPU
with tf.device('/GPU:0'):
    # Your code
```

## Optimising GPU Usage

**Use mixed precision:**
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
with autocast():
    output = model(input)
```

**Batch size tuning:**
- Start small, increase until GPU memory ~80% full
- Monitor with nvidia-smi

## Next Steps

- → [Custom Environments](custom-environments.md)
- → [Dockerfile Best Practices](../advanced/dockerfile-best-practices.md)
