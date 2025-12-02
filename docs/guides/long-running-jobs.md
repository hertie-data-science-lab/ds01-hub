# Long-Running Jobs

Running overnight training, preventing timeouts, and managing extended workloads.

---

## Quick Start

```bash
# Deploy in background
container-deploy my-project --background

# Inside container, use nohup or tmux
nohup python train.py > training.log 2>&1 &

# Prevent idle timeout
touch /workspace/.keep-alive
```

---

## Running Training Overnight

### Method 1: nohup (Simple)

```bash
# Start training that continues after disconnect
nohup python train.py > training.log 2>&1 &

# Check progress
tail -f training.log

# Exit container safely
exit
```

### Method 2: tmux (Recommended)

```bash
# Create named session
tmux new -s training

# Run training
python train.py

# Detach: Ctrl+B, then D

# Later, reattach
tmux attach -t training
```

### Method 3: Screen

```bash
# Create session
screen -S training

# Run training
python train.py

# Detach: Ctrl+A, then D

# Reattach
screen -r training
```

---

## Preventing Idle Timeout

DS01 stops containers idle for too long (typically 48 hours of low CPU).

### Option 1: .keep-alive File

```bash
touch /workspace/.keep-alive
```

This tells DS01 your job is intentionally long-running.

### Option 2: Active Training

Active GPU/CPU usage doesn't count as idle. Training jobs naturally prevent timeout.

---

## Monitoring Progress

### From Outside Container

```bash
# Check container is running
container-list

# View logs
docker logs my-project._.$(whoami) --tail 100

# Follow logs
docker logs my-project._.$(whoami) -f
```

### Inside Container

```bash
# Attach to running container
container-run my-project

# Check GPU
nvidia-smi

# Check training logs
tail -f /workspace/training.log
```

---

## Checkpointing

Save progress regularly so you can resume if interrupted:

### PyTorch

```python
# Save checkpoint
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, f'/workspace/checkpoints/checkpoint_{epoch}.pt')

# Load checkpoint
checkpoint = torch.load('/workspace/checkpoints/checkpoint_latest.pt')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
start_epoch = checkpoint['epoch']
```

### TensorFlow/Keras

```python
# Save callback
checkpoint = tf.keras.callbacks.ModelCheckpoint(
    '/workspace/checkpoints/model_{epoch:02d}.keras',
    save_best_only=True
)

model.fit(x, y, callbacks=[checkpoint])

# Resume
model = tf.keras.models.load_model('/workspace/checkpoints/model_10.keras')
```

---

## Resource Limits

Check your limits before long runs:

```bash
check-limits
```

Key limits:
- **Max Runtime:** Typically 168h (1 week)
- **Idle Timeout:** Typically 48h
- **Memory:** Per-container limit

---

## Best Practices

### 1. Checkpoint Early and Often

```python
# Every N epochs
if epoch % checkpoint_interval == 0:
    save_checkpoint(model, optimizer, epoch)
```

### 2. Log to File

```python
import logging
logging.basicConfig(
    filename='/workspace/training.log',
    level=logging.INFO
)
```

### 3. Monitor GPU Memory

```python
# In training loop
if epoch % 10 == 0:
    print(f"GPU Memory: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
```

### 4. Set Up Alerts (Optional)

```python
# At end of training
import os
os.system('echo "Training complete" | mail -s "DS01 Alert" you@email.com')
```

---

## Troubleshooting

### Job Stopped Unexpectedly

1. Check logs:
   ```bash
   docker logs my-project._.$(whoami) | tail -100
   ```

2. Check for OOM:
   ```bash
   docker inspect my-project._.$(whoami) | grep OOMKilled
   ```

3. Resume from checkpoint:
   ```bash
   container-deploy my-project --open
   python train.py --resume /workspace/checkpoints/latest.pt
   ```

### Container Removed

Your workspace is safe. Recreate and resume:
```bash
container-deploy my-project --open
# Resume training from checkpoint
```

---

## See Also

- [GPU Usage](gpu-usage.md)
- [Daily Workflow](daily-workflow.md)
- [Troubleshooting](../troubleshooting/)
