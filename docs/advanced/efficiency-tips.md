# Efficiency Tips

Speed up your DS01 workflow with keyboard shortcuts and workflow optimizations.

---

## Keyboard Shortcuts

### Inside Containers

| Shortcut | Action |
|----------|--------|
| `Ctrl+D` | Exit container (same as `exit`) |
| `Ctrl+C` | Cancel current command |
| `Ctrl+Z` | Suspend current process |
| `Ctrl+L` | Clear terminal |
| `Ctrl+R` | Search command history |

### Terminal Navigation

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Jump to line start |
| `Ctrl+E` | Jump to line end |
| `Ctrl+W` | Delete word backward |
| `Ctrl+U` | Delete to line start |
| `Ctrl+K` | Delete to line end |
| `Alt+B` | Move word backward |
| `Alt+F` | Move word forward |

### Tmux (if using)

| Shortcut | Action |
|----------|--------|
| `Ctrl+B D` | Detach session |
| `Ctrl+B C` | New window |
| `Ctrl+B N` | Next window |
| `Ctrl+B P` | Previous window |
| `Ctrl+B %` | Split vertical |
| `Ctrl+B "` | Split horizontal |

---

## Command History

### Search History

```bash
# Search backward
Ctrl+R
# Type partial command, press Ctrl+R again for older matches

# Search forward (after Ctrl+R)
Ctrl+S
```

### History Shortcuts

```bash
!!          # Repeat last command
!$          # Last argument of previous command
!*          # All arguments of previous command
!-2         # Run command 2 back
!container  # Run last command starting with "container"
```

**Examples:**
```bash
container-deploy my-thesis
container-attach !$           # Uses "my-thesis"

vim ~/workspace/project/train.py
python !$                     # Runs the same file
```

---

## Tab Completion

DS01 commands support tab completion:

```bash
container-<TAB>
# Shows: container-create  container-start  container-stop ...

container-deploy my-<TAB>
# Completes project name if unique
```
---

## Time-Saving Patterns

### Pattern 1: Quick Restart

```bash
# Restart container (retire + deploy)
container retire my-project --force && container deploy my-project --open
```

### Pattern 2: Image Rebuild Cycle

```bash
# Interactive: Use GUI to add packages then recreate
image-update && container retire my-project --force && container deploy my-project --open

# Advanced: Manual Dockerfile edit, rebuild, recreate
vim ~/workspace/my-project/Dockerfile
image-update my-project --rebuild && container retire my-project --force && container deploy my-project --open
```

### Pattern 3: Multi-Container Cleanup

```bash
# Remove all stopped containers
container-list --all | grep stopped | awk '{print $1}' | xargs -I {} container-remove {} --force
```

---

## Environment Customisation

### Bashrc Additions

Add to `~/.bashrc`:

```bash
# DS01 status on prompt (optional)
export PS1='[\u@ds01 \W]$ '

# Quick project navigation
alias cdw='cd ~/workspace'
alias cdp='cd ~/workspace/$(ls ~/workspace | fzf)'  # requires fzf
```

### Container Environment

Add to your Dockerfile:

```dockerfile
# Useful aliases inside container
RUN echo 'alias ll="ls -la"' >> ~/.bashrc
RUN echo 'alias ..="cd .."' >> ~/.bashrc
```
Many others possible - depends on your workflow

---

## Next Steps

- [Shell Aliases](shell-aliases.md) - Command shortcuts
- [Scripting (Bash)](scripting-bash.md) - Automate workflows
- [CLI Flags](cli-flags.md) - All available flags
