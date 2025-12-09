# Daily Usage Patterns

Common workflows and patterns for productive day-to-day use of DS01. Master these patterns and you'll be efficient and effective.

---

## The Standard Daily Workflow

### Morning: Start Working

```bash
# Deploy and enter container
container-deploy my-project --open

# Or if you prefer background start
container-deploy my-project --background
# Then attach later
container-run my-project
```

**Time:** ~30 seconds

### During the Day: Work

```bash
# Inside container
cd /workspace

# Pull latest code
git pull

# Activate environment (if using conda)
conda activate myenv

# Work on your project
python train.py
# or
jupyter lab --ip=0.0.0.0
# or
code .  # If using VSCode
```

**Save frequently:**
```bash
# Commit code changes
git add .
git commit -m "Update training script"
git push

# Models save automatically to /workspace/models/
```

### Evening: Done for the Day

```bash
# Make sure work is saved
git status
git push  # If any uncommitted work

# Exit container
exit

# Free GPU for others
container-retire my-project
```

**Time:** ~10 seconds

---

## Common Patterns

### Pattern 1: Quick Experiment

**Use case:** Test idea quickly

```bash
# Morning
container-deploy experiment --open

# Work
python quick_test.py

# Results look good? Save them
cp results.csv /workspace/experiments/test-$(date +%Y%m%d).csv

# Done
exit
container-retire experiment
```

**Duration:** 30 minutes to 2 hours

---

### Pattern 2: Long Training Job

**Use case:** Multi-hour or overnight training

```bash
# Start in background
container-deploy training --background

# Enter container
container-run training

# Start training with nohup (survives disconnect)
nohup python train.py > /workspace/logs/training.log 2>&1 &

# Check it started
tail -f /workspace/logs/training.log
# Ctrl+C to stop watching

# Exit (training continues)
exit

# Later: Check progress
container-run training
tail /workspace/logs/training.log
# or
python check_progress.py

# Training complete? Retire
exit
container-retire training
```

**Prevent auto-stop:**
```bash
# For jobs longer than idle timeout
touch ~/workspace/training/.keep-alive
```

---

### Pattern 3: Multiple Projects

**Use case:** Working on different projects same day

```bash
# Morning: Project A
container-deploy project-a --open
# Work on project A
exit

# Afternoon: Switch to project B
container-retire project-a  # Free GPU
container-deploy project-b --open
# Work on project B
exit

# Evening: Clean up
container-retire project-b
```

**Check limits:**
```bash
cat ~/.ds01-limits
# Max Containers: 3  # Can run multiple if within limit
```

---

### Pattern 4: Interactive Development

**Use case:** Iterative coding with frequent testing

```bash
# Deploy container
container-deploy dev --open

cd /workspace

# Edit-run cycle
vim train.py         # or nano, emacs, etc.
python train.py      # Test
# Iterate

# Or use Jupyter
jupyter lab --ip=0.0.0.0 --port=8888
# Access at http://ds01-server:8888
# (Set up SSH tunnel if needed)
```

**Pro tip:** Use VSCode Remote for better editing experience
→ See [VSCode Remote Guide](../advanced/vscode-remote.md)

---

### Pattern 5: Parallel Experiments

**Use case:** Test multiple hyperparameters simultaneously

```bash
# Check your limits
cat ~/.ds01-limits  # Max Containers: 3

# Start experiments (within limits)
container-deploy exp-lr-0.001 --background
container-deploy exp-lr-0.01 --background
container-deploy exp-lr-0.1 --background

# Each container runs in background
# Enter each to start training
container-run exp-lr-0.001
cd /workspace && nohup python train.py --lr 0.001 &
exit

container-run exp-lr-0.01
cd /workspace && nohup python train.py --lr 0.01 &
exit

container-run exp-lr-0.1
cd /workspace && nohup python train.py --lr 0.1 &
exit

# Monitor progress
container-stats  # Resource usage

# Later: Check results
container-run exp-lr-0.001
cat /workspace/results/metrics.json
exit

# Retire all when done
container-retire exp-lr-0.001
container-retire exp-lr-0.01
container-retire exp-lr-0.1
```

---

### Pattern 6: Data Exploration

**Use case:** Exploratory data analysis

```bash
# Deploy with Jupyter
container-deploy analysis --open

cd /workspace

# Start Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# Access via SSH tunnel (from your laptop):
# ssh -L 8888:localhost:8888 user@ds01-server

# Open browser: http://localhost:8888

# Work in notebooks
# Notebooks saved to /workspace/notebooks/

# Done exploring
# Ctrl+C to stop Jupyter
exit
container-retire analysis
```

---

### Pattern 7: Model Evaluation

**Use case:** Evaluate trained models

```bash
# Deploy container
container-deploy evaluation --open

cd /workspace

# Load model and test
python evaluate.py --model models/best-model.pt --data data/test.csv

# Generate visualizations
python plot_results.py

# Save results
# (Already in /workspace/results/ - persistent)

# Review and commit
git add results/
git commit -m "Add evaluation results"
git push

exit
container-retire evaluation
```

---

## Time-Saving Tips

### 1. Aliases

Add to `~/.bashrc`:
```bash
# Quick container management
alias cdeploy='container-deploy'
alias cretire='container-retire'
alias clist='container-list'
alias cstats='container-stats'
alias crun='container-run'

# Quick navigation
alias ws='cd ~/workspace'
alias proj='cd ~/workspace/my-main-project'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
```

Reload:
```bash
source ~/.bashrc
```

Usage:
```bash
cdeploy my-project --open  # Instead of container-deploy
```

---

### 2. Background Startup

Save time by deploying in background first:
```bash
# Start container while you get coffee
container-deploy my-project --background &

# 30 seconds later, attach
container-run my-project
# Container is already running
```

---

### 3. Tmux/Screen

Use terminal multiplexer for persistent sessions:
```bash
# Inside container
tmux new -s work

# Work in tmux
python train.py

# Detach: Ctrl+b then d
# Exit container (training continues)

# Later: Reattach
container-run my-project
tmux attach -t work
```

**Survives SSH disconnects!**

---

### 4. Git Workflow

Efficient Git usage:
```bash
# Morning: Pull latest
git pull

# Work on feature
# ... make changes ...

# Commit frequently
git add -A
git commit -m "Descriptive message"

# Push at logical points
git push

# Evening: Make sure pushed
git status
git push
```

---

### 5. Jupyter Startup Script

Create `~/workspace/my-project/start_jupyter.sh`:
```bash
#!/bin/bash
cd /workspace
jupyter lab \
  --ip=0.0.0.0 \
  --port=8888 \
  --no-browser \
  --allow-root \
  --ServerApp.token='' \
  --ServerApp.password=''
```

Usage:
```bash
chmod +x ~/workspace/my-project/start_jupyter.sh
container-run my-project
/workspace/start_jupyter.sh
```

---

## Monitoring & Debugging

### Check Container Status

```bash
# List your containers
container-list

# Detailed info
docker ps -a --filter "name=._.$(whoami)"

# Resource usage
container-stats
```

### Check GPU Usage

```bash
# Inside container
nvidia-smi

# Continuous monitoring
watch -n 1 nvidia-smi

# GPU memory usage
nvidia-smi --query-gpu=memory.used,memory.total --format=csv

# Process using GPU
nvidia-smi pmon
```

### View Logs

```bash
# From host (without entering container)
docker logs my-container._.$(whoami)

# Follow logs
docker logs -f my-container._.$(whoami)

# Last 100 lines
docker logs --tail 100 my-container._.$(whoami)
```

### Inspect Container

```bash
# Detailed container info
docker inspect my-container._.$(whoami)

# Check mounts
docker inspect my-container._.$(whoami) | grep -A 10 "Mounts"

# Check environment variables
docker inspect my-container._.$(whoami) | grep -A 10 "Env"
```

---

## Troubleshooting Common Issues

### Issue: "Can't deploy, no GPUs available"

**Check availability:**
```bash
ds01-dashboard  # If available
# Or
python3 /opt/ds01-infra/scripts/docker/gpu_allocator.py status
```

**Solutions:**
- Wait for GPU to free up
- Retire idle containers
- Check if someone forgot to retire

---

### Issue: "Container stopped unexpectedly"

**Check logs:**
```bash
docker logs my-container._.$(whoami)
```

**Common causes:**
- Out of memory (OOM killed)
- Idle timeout reached
- Code error/crash

**Recovery:**
```bash
# Restart container
container-start my-container

# Or recreate
container-retire my-container
container-deploy my-container
```

---

### Issue: "Can't find files"

**Remember paths:**
- Host: `~/workspace/my-project/`
- Container: `/workspace/`

**Check both:**
```bash
# On host
ls ~/workspace/my-project/

# In container
docker exec my-container._.$(whoami) ls /workspace/
```

---

### Issue: "Package not found in container"

**Temporary fix:**
```bash
container-run my-project
pip install missing-package
```

**Permanent fix:**
```bash
exit
image-update my-project  # Add to Dockerfile
container-retire my-project
container-deploy my-project
```

---

## Best Practices Checklist

### Daily Habits

- [ ] Start day: Deploy container
- [ ] Pull latest code: `git pull`
- [ ] Work and save frequently
- [ ] Commit at logical points
- [ ] Push before leaving
- [ ] End day: Retire container

### Weekly Habits

- [ ] Review disk usage: `du -sh ~/workspace/*`
- [ ] Clean up old experiments
- [ ] Update Docker images if needed
- [ ] Backup important results
- [ ] Check resource usage patterns

### Monthly Habits

- [ ] Archive completed projects
- [ ] Review and optimize workflows
- [ ] Update documentation
- [ ] Clean up old Docker images

---

## Example Full Day

**8:30 AM - Start**
```bash
ssh user@ds01-server
container-deploy research --open
cd /workspace
git pull
```

**9:00 AM - Morning work**
```bash
# Review yesterday's results
cat results/training-log.txt

# Continue training
python train.py --resume --checkpoint models/checkpoint-020.pt
```

**12:00 PM - Lunch break**
```bash
# Training will continue
# Ctrl+Z, bg  # Background the process
# Or use tmux/nohup
exit  # Container keeps running
```

**1:00 PM - Check progress**
```bash
container-run research
tail -n 50 /workspace/logs/training.log
# Looking good, let it run
exit
```

**3:00 PM - Analysis**
```bash
container-run research
# Training finished
python evaluate.py
python plot_results.py
# Review plots in /workspace/results/
```

**4:30 PM - Document and commit**
```bash
# Write up findings
vim /workspace/README.md

# Commit everything
git add .
git commit -m "Complete initial training runs, add evaluation"
git push

exit
container-retire research
```

**Done for the day! 🎉**

---

## Next Steps

### Learn More Workflows

**Project setup:**
→ [Creating Projects](creating-projects.md)

**Container management:**
→ [Managing Containers](managing-containers.md)

**Custom environments:**
→ [Building Custom Images](custom-images.md)

### Master Advanced Techniques

**Remote development:**
→ [VSCode Remote](../advanced/vscode-remote.md)

**Optimization:**
→ 

---

## Summary

**Key Workflows:**

1. **Standard daily:** Deploy → Work → Retire
2. **Long training:** Background + nohup + .keep-alive
3. **Multiple projects:** Deploy → Retire → Deploy next
4. **Parallel experiments:** Multiple containers within limits
5. **Interactive dev:** Jupyter or VSCode Remote

**Time-Savers:**
- Aliases for common commands
- Background container startup
- Tmux for persistent sessions
- Git workflows
- Startup scripts

**Best Practices:**
- Retire containers when done
- Save frequently to /workspace
- Commit code regularly
- Monitor resource usage
- Keep environments clean

**Master these patterns and DS01 becomes second nature!**

**Ready for more details?** → [Managing Containers](managing-containers.md)
