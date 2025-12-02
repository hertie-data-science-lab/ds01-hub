# Best Practices

Production-ready habits for DS01 usage.

## Resource Management

### Retire Containers

```bash
# End of day
container-retire my-project

# Lunch break (>1 hour)
container-retire my-project
```

### Monitor Usage

```bash
# Before deploying
ds01-dashboard

# While running
container-stats
nvidia-smi  # Inside container
```

## Code Organization

### Save to Workspace

```python
# Good
model_path = '/workspace/models/model.pt'
torch.save(model, model_path)

# Bad
model_path = '/tmp/model.pt'  # Lost on retire!
```

### Use Version Control

```bash
git add .
git commit -m "Descriptive message"
git push  # Backup to remote
```

## Performance

### Optimize Batch Size

```python
# Find optimal batch size
# Start small, increase until GPU ~80% full
batch_size = 32  # Adjust based on nvidia-smi
```

### Use Mixed Precision

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
with autocast():
    output = model(input)
```

### Checkpoint Frequently

```python
if epoch % 10 == 0:
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, f'/workspace/models/checkpoint-{epoch:03d}.pt')
```

## Security

### Don't Store Secrets

```python
# Bad
api_key = "secret123"

# Good
import os
api_key = os.environ.get('API_KEY')
```

### Keep Packages Updated

```bash
# Update image periodically
image-update my-project
```

## Efficiency

### Clean Up Regularly

```bash
# Remove old checkpoints
find ~/workspace/my-project/models -name "checkpoint-*.pt" -mtime +30 -delete

# Clean Python cache
find ~/workspace -type d -name __pycache__ -exec rm -rf {} +
```

### Use Appropriate Resources

```bash
# Don't request more than you need
# If 1 GPU sufficient, don't request 2
container-deploy my-project --gpu 1
```

## Next Steps

→ [Daily Usage Patterns](../guides/daily-workflow.md)
→ [Industry Practices](../background/industry-parallels.md)
