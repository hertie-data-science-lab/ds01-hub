# GPU Issues

Solutions for GPU allocation, availability, and CUDA problems.

---

## No GPUs Available {#no-gpus}

**Symptoms:**
```bash
$ container-deploy my-project
Error: No GPUs available for allocation
```

**Causes:**
- All GPUs currently allocated
- System maintenance
- GPU hardware issues

**Solutions:**

1. **Check availability:**
   ```bash
   ds01-dashboard
   ```

2. **Wait for GPU to free up** - Other users may be finishing soon

3. **Retire your idle containers:**
   ```bash
   container-list
   container-retire old-project
   ```

4. **Contact DSL admin** if GPUs show available but allocation fails

---

## CUDA Out of Memory {#cuda-oom}

**Symptoms:**
```bash
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

**Causes:**
- Model too large for GPU
- Batch size too large
- Memory leak in code

**Solutions:**

1. **Reduce batch size:**
   ```python
   batch_size = 32  # Try 16, 8, or smaller
   ```

2. **Use gradient accumulation:**
   ```python
   # Effective batch size = batch_size * accumulation_steps
   accumulation_steps = 4
   ```

3. **Use mixed precision:**
   ```python
   from torch.cuda.amp import autocast, GradScaler
   scaler = GradScaler()

   with autocast():
       output = model(input)
   ```

4. **Clear cache:**
   ```python
   import torch
   torch.cuda.empty_cache()
   ```

5. **Check for memory leaks:**
   ```python
   print(torch.cuda.memory_summary())
   ```
---

## GPU Not Detected by Framework {#framework-detection}

**Symptoms:**
```python
>>> torch.cuda.is_available()
False
```

**Solutions:**

1. **Check nvidia-smi first:**
   ```bash
   nvidia-smi
   ```

2. **Check CUDA version compatibility:**
   ```bash
   nvcc --version
   python -c "import torch; print(torch.version.cuda)"
   ```

3. **Reinstall PyTorch with correct CUDA:**
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cu124
   ```

4. **For TensorFlow:**
   ```python
   import tensorflow as tf
   print(tf.config.list_physical_devices('GPU'))
   ```

---

## GPU Shows No Devices {#no-devices}

**Symptoms:**
```bash
$ nvidia-smi
No devices found
```

**Causes:**
- Not allocated GPU
- Container created without GPU

**Solutions:**

1. **Check allocation:**
   ```bash
   python3 /opt/ds01-infra/scripts/docker/gpu_allocator.py status
   ```

2. **Recreate with GPU:**
   ```bash
   container-retire my-project
   container-deploy my-project --gpu 1
   ```

---

## GPU Memory Not Releasing {#memory-stuck}

**Symptoms:**
- nvidia-smi shows memory used even after training ends
- "CUDA out of memory" after successful run

**Solutions:**

1. **Delete tensors and clear cache:**
   ```python
   del model, optimizer
   torch.cuda.empty_cache()
   ```

2. **Exit Python and restart:**
   ```bash
   exit()  # Python
   python  # Restart
   ```

3. **Restart container:**
   ```bash
   exit
   container-stop my-project
   container-start my-project
   ```

---

## Multi-GPU Not Working

**Symptoms:**
- Only one GPU visible
- DataParallel/DistributedDataParallel fails

**Solutions:**

1. **Check allocation:**
   ```bash
   nvidia-smi  # Should show all allocated GPUs
   ```

2. **Verify all GPUs visible to PyTorch:**
   ```python
   import torch
   print(torch.cuda.device_count())
   for i in range(torch.cuda.device_count()):
       print(torch.cuda.get_device_name(i))
   ```

3. **Request more GPUs:**
   ```bash
   container-retire my-project
   container-deploy my-project --gpu 2
   ```

---

## See Also

- [Container Issues](container-issues.md)
- [GPU Usage Guide](../core-guides/gpu-usage.md)
