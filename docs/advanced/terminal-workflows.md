# Terminal-Native Workflows

CLI-focused development patterns for users who prefer terminal over IDE.

> **Note:** In examples below, replace `<project-name>` with your actual project name. The `$(id -u)` part auto-substitutes your user ID.

---

## Philosophy

**Everything via terminal:**
- Edit code: vim/nano
- Run code: docker exec
- Debug: logs and print statements
- Version control: command-line git
- Sessions: tmux/screen

**No IDE required.**

---

## Basic Pattern

```bash
# Edit code on host
vim ~/workspace/my-project/train.py

# Run in container (non-interactive)
docker exec <project-name>._.$(id -u) \
  python /workspace/train.py

# Check output
tail -f ~/workspace/my-project/output.log
```

---

## Vim-Based Development

**Edit on host, run in container:**

```bash
# Open project in vim
cd ~/workspace/my-project
vim src/model.py

# Test changes
docker exec <project-name>._.$(id -u) \
  python /workspace/src/model.py

# Or enter container for interactive testing
docker exec -it <project-name>._.$(id -u) bash
>>> python
>>> from src.model import MyModel
>>> model = MyModel()
```

**Benefits:**
- No IDE overhead
- Fast editing
- Works over slow SSH

---

## tmux Session Management

**Persistent terminal sessions:**

```bash
# Create session
tmux new -s dev

# Split for editing + running
Ctrl+B %    # Split vertical
Ctrl+B "    # Split horizontal

# Left pane: vim
vim ~/workspace/my-project/train.py

# Right pane: container shell
docker exec -it <project-name>._.$(id -u) bash

# Detach
Ctrl+B D

# Reattach later
tmux attach -s dev
```

---

## Non-Interactive Execution

**Run commands without entering container:**

```bash
# Single command
docker exec <project-name>._.$(id -u) \
  python /workspace/train.py

# Multiple commands
docker exec <project-name>._.$(id -u) bash -c "
  cd /workspace
  python preprocess.py
  python train.py
  python evaluate.py
"

# With environment variables
docker exec -e CUDA_VISIBLE_DEVICES=0 <project-name>._.$(id -u) \
  python /workspace/train.py
```

---

## Log Monitoring

**Follow logs in real-time:**

```bash
# Container logs
docker logs -f <project-name>._.$(id -u)

# Application logs
tail -f ~/workspace/my-project/training.log

# With grep filter
tail -f ~/workspace/my-project/training.log | grep "epoch"

# Multiple logs
tail -f ~/workspace/my-project/*.log
```

---

## Command-Line Git

**Version control without IDE:**

```bash
cd ~/workspace/my-project

# Check status
git status

# Stage changes
git add src/model.py

# Commit
git commit -m "Improve model architecture"

# Push
git push

# View history
git log --oneline --graph

# Diff changes
git diff src/model.py
```

---

## Process Management

**Background jobs:**

```bash
# Start in background
docker exec -d <project-name>._.$(id -u) \
  nohup python /workspace/train.py > /workspace/output.log 2>&1

# Check running processes
docker exec <project-name>._.$(id -u) ps aux | grep python

# Kill process
docker exec <project-name>._.$(id -u) pkill -f train.py
```

---

## File Transfer

**Copy files between host and container:**

```bash
# Host to container
docker cp local-file.txt <project-name>._.$(id -u):/workspace/

# Container to host
docker cp <project-name>._.$(id -u):/workspace/results.txt ~/

# Entire directory
docker cp ~/data/ <project-name>._.$(id -u):/workspace/data/
```

**Usually not needed** - use workspace mount instead.

---

## Shell Aliases

**Speed up common tasks:**

```bash
# Add to ~/.bashrc
alias dex='docker exec -it <project-name>._.$(id -u) bash'
alias drun='docker exec <project-name>._.$(id -u)'
alias dlogs='docker logs -f <project-name>._.$(id -u)'

# Usage
dex                           # Enter container
drun python /workspace/train.py   # Run command
dlogs                         # Follow logs
```

---

## See Also

- → [Docker Direct](docker-direct.md) - Docker command reference

- → [Batch Jobs](batch-jobs.md) - Long-running jobs

- → [SSH Advanced](ssh-advanced.md) - Remote access
