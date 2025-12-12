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

DS01 auto-stops containers that are idle (low GPU activity). Timeout varies by user (typically **30min-2h**) and is dynamically adjusted. Run `check-limits` to see your current limits.

> **⚠️ Contact DSL First**
>
> The workarounds below (`.keep-alive`, `nohup`, etc.) are available but should be **last resorts** as they can disrupt the system for other users by holding GPUs longer than necessary.
>
> **Please [open an issue on DS01 Hub](https://github.com/hertie-data-science-lab/ds01-hub/issues) first** to discuss your requirements with the Data Science Lab team. We can often find better solutions together (adjusted limits, scheduled runs, checkpointing strategies).

### Option 1: .keep-alive File

```bash
touch /workspace/.keep-alive
```

This tells DS01 your job is intentionally long-running.

### Option 2: Active Training

Active GPU/CPU usage doesn't count as idle. Training jobs naturally prevent timeout.

---

## Pausing Jobs Temporarily

For short breaks, you can pause containers instead of stopping them.

### DS01 Commands (Recommended)

```bash
# Pause container (freeze all processes)
container-pause my-project

# Resume container
container-unpause my-project
```

### Docker Commands (L1)

> Replace `<project-name>` with your actual project name.

```bash
# Pause container
docker pause <project-name>._.$(id -u)

# Resume container
docker unpause <project-name>._.$(id -u)
```

**What happens when paused:**
- All processes freeze instantly (training pauses mid-batch)
- GPU remains allocated but idle
- Memory state preserved
- Resume instantly where you left off

**When to use pause:**
- Debugging (freeze state for inspection)
- Testing before checkpoints

**When NOT to use pause:**
- Long breaks (use `container-stop` instead) 
- Freeing GPU for others (pause keeps GPU allocated)

---

## Monitoring Progress

### From Outside Container

> Replace `<project-name>` with your actual project name.

```bash
# Check container is running
container-list

# View logs
docker logs <project-name>._.$(whoami) --tail 100

# Follow logs
docker logs <project-name>._.$(whoami) -f
```

### Inside Container

```bash
# Attach to running container
container-attach my-project

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
- **Max Runtime:** 24h-72h (varies by user)
- **Idle Timeout:** 30min-2h (varies by user)
- **Memory:** Per-container limit

Run `check-limits` to see your current values.

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

> Replace `<project-name>` with your actual project name in commands below.

### Job Stopped Unexpectedly

1. Check logs:
   ```bash
   docker logs <project-name>._.$(whoami) | tail -100
   ```

2. Check for OOM:
   ```bash
   docker inspect <project-name>._.$(whoami) | grep OOMKilled
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
