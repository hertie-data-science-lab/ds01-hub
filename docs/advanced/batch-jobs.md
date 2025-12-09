# Batch Jobs and Non-Interactive Execution

Submit long-running jobs and check results later - HPC-style workflows.

---

## Overview

**Batch job pattern:**
1. Submit job to container
2. Job runs in background
3. Results written to workspace
4. Check logs/results later

**No babysitting needed.**

---

## Basic Pattern

```bash
# Create container
container-create training --gpu=2

# Submit job (non-interactive)
docker exec -d training._.$(id -u) \
  nohup python /workspace/train.py > /workspace/training.log 2>&1

# Job runs for hours/days
# You can disconnect, container keeps running

# Check progress later
tail -f ~/workspace/training.log

# Or check GPU usage
nvidia-smi
```

---

## With nohup

**Standard approach:**

```bash
docker exec -d my-project._.$(id -u) \
  nohup python /workspace/train.py \
  > /workspace/output.log 2>&1 &
```

**Components:**
- `docker exec -d` - Detached mode (background)
- `nohup` - Ignore hangup signals (survives disconnects)
- `> /workspace/output.log` - Redirect stdout
- `2>&1` - Redirect stderr to stdout
- `&` - Run in background

---

## Parameter Sweep Example

**Run multiple experiments:**

```bash
#!/bin/bash
# sweep.sh

for lr in 0.001 0.01 0.1; do
  for batch_size in 16 32 64; do
    NAME="exp-lr${lr}-bs${batch_size}"

    # Create container
    container-create $NAME --gpu=1 --background

    # Submit job
    docker exec -d $NAME._.$(id -u) \
      nohup python /workspace/train.py \
      --lr=$lr \
      --batch-size=$batch_size \
      > /workspace/logs/${NAME}.log 2>&1

    echo "Submitted: $NAME"
  done
done

echo "All jobs submitted. Monitor with:"
echo "tail -f ~/workspace/logs/*.log"
```

---

## Monitoring Jobs

**Check running processes:**

```bash
# All your containers
docker ps --filter label=DS01_USER=$(id -u)

# Processes in specific container
docker exec my-project._.$(id -u) ps aux | grep python

# GPU usage
nvidia-smi

# Live monitoring
watch -n 1 nvidia-smi
```

**Check logs:**

```bash
# Follow log
tail -f ~/workspace/training.log

# Last 100 lines
tail -100 ~/workspace/training.log

# Search logs
grep "epoch" ~/workspace/training.log

# Multiple logs
tail -f ~/workspace/logs/*.log
```

---

## Job Completion Detection

**Wait for job to finish:**

```bash
#!/bin/bash

PROJECT=my-training

# Submit job
docker exec -d $PROJECT._.$(id -u) \
  nohup python /workspace/train.py > /workspace/output.log 2>&1

# Wait for completion
while docker exec $PROJECT._.$(id -u) pgrep -f train.py > /dev/null; do
  echo "Job still running..."
  sleep 60
done

echo "Job completed!"

# Collect results
cat ~/workspace/output.log
```

---

## Error Handling

**Check exit codes:**

```bash
# Run job
docker exec my-project._.$(id -u) \
  python /workspace/train.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "Success!"
else
  echo "Failed with code $EXIT_CODE"
  docker logs my-project._.$(id -u)
fi
```

---

## Checkpointing

**Save progress regularly:**

```python
# In train.py
for epoch in range(num_epochs):
    train_one_epoch()

    # Save checkpoint
    if epoch % 5 == 0:
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
        }, f'/workspace/checkpoints/epoch_{epoch}.pt')
```

**Resume if interrupted:**

```python
# Load checkpoint if exists
checkpoint_path = '/workspace/checkpoints/latest.pt'
if os.path.exists(checkpoint_path):
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    start_epoch = checkpoint['epoch'] + 1
else:
    start_epoch = 0
```

---

## Resource Alerts

**Email on completion (if configured):**

```bash
#!/bin/bash

docker exec -d my-project._.$(id -u) \
  bash -c "python /workspace/train.py; echo 'Training complete' | mail -s 'Job Done' user@example.com"
```

**Slack notification (if webhook configured):**

```python
# At end of train.py
import requests

webhook_url = "https://hooks.slack.com/..."
message = {"text": "Training completed!"}
requests.post(webhook_url, json=message)
```

---

## Best Practices

1. **Always write to `/workspace`** - Results must persist
2. **Use clear log names** - `exp-lr0.001-bs32.log` not `output.log`
3. **Save checkpoints frequently** - Every N epochs
4. **Log hyperparameters** - Record config in log file
5. **Clean up finished jobs** - Remove containers when done

---

## Example: Full Pipeline

```bash
#!/bin/bash
# pipeline.sh

set -e

PROJECT="my-training"
LOG_DIR=~/workspace/logs
CHECKPOINT_DIR=~/workspace/checkpoints

mkdir -p $LOG_DIR $CHECKPOINT_DIR

# Create container
container-create $PROJECT --gpu=2 || exit 1

# Submit job
docker exec -d $PROJECT._.$(id -u) bash -c "
  cd /workspace
  python train.py \
    --epochs=100 \
    --lr=0.001 \
    --batch-size=32 \
    --checkpoint-dir=/workspace/checkpoints \
    > /workspace/logs/training.log 2>&1
"

echo "Job submitted. Monitor with:"
echo "  tail -f $LOG_DIR/training.log"
echo ""
echo "Check GPU usage:"
echo "  nvidia-smi"
echo ""
echo "When complete, collect results from:"
echo "  $CHECKPOINT_DIR/"
```

---

## See Also

→ [Terminal Workflows](terminal-workflows.md) - CLI development patterns

→ [Docker Direct](docker-direct.md) - Docker commands

→ [Scripting](../intermediate/scripting.md) - Automation patterns
