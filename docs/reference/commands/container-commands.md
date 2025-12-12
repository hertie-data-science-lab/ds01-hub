# Container Commands

Commands for container lifecycle management.

---

## Getting Help

All container commands support these flags:

| Flag | Purpose |
|------|---------|
| `--help` | Quick reference (usage, main options) |
| `--info` | Full reference (all options, examples) |
| `--concepts` | Pre-run education (what is a container?) |
| `--guided` | Interactive learning (explanations during) |

```bash
container-deploy --concepts   # Learn before deploying
container-stop --info         # See all stop options
```

---

## Quick Reference

```bash
# Deploy (create + start)
container-deploy my-project --open

# Retire (stop + remove + free GPU)
container-retire my-project

# List containers
container-list

# Resource usage
container-stats
```

---

## container-deploy

**Create and start a container** (L3 orchestrator)

```bash
container-deploy <project-name> [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--open` | Create and enter terminal immediately |
| `--background` | Create and start in background |
| `--framework=NAME` | Use AIME base framework (pytorch, tensorflow) |
| `--image=NAME` | Use specific Docker image |
| `--cpu-only` | Create CPU-only container (no GPU) |
| `-w, --workspace` | Mount custom workspace directory |
| `--project=NAME` | Mount ~/workspace/NAME as workspace |
| `-d, --data` | Additional data directory to mount |
| `--dry-run` | Preview without executing |
| `--guided` | Educational mode |

**Examples:**
```bash
container-deploy my-project              # Interactive (requires custom image)
container-deploy my-project --open       # Create and enter terminal
container-deploy my-project --background # Start in background

# Using base frameworks (no custom image needed)
container-deploy test --framework=pytorch     # Quick test with PyTorch
container-deploy test --framework=tensorflow  # Quick test with TensorFlow

# Other options
container-deploy data-prep --cpu-only    # CPU only (no GPU)
container-deploy my-project --dry-run    # Preview what would happen
```

**What it does:**
1. Checks resource availability
2. Runs `container-create` (allocates GPU unless --cpu-only)
3. Runs `container-start` or `container-run` based on flags

**Note:** By default, requires a custom image (`ds01-{uid}/{name}:latest`). Use `--framework` or `--image` to bypass.

---

## container-retire

**Stop and remove a container, free GPU** (L3 orchestrator)

```bash
container-retire <project-name> [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --force` | Skip confirmation prompts |
| `--save-packages` | Automatically save new packages to image (no prompt) |
| `--images` | Also remove the Docker image after retiring |
| `--dry-run` | Show what would be done |
| `--guided` | Educational mode |

**Examples:**
```bash
container-retire my-project              # Interactive
container-retire my-project --force      # Skip confirmations
container-retire my-project --images     # Also remove Docker image
container-retire my-project --save-packages  # Auto-save new packages
```

**What it does:**
1. Stops container (if running)
2. Detects new packages and prompts to save (or auto-saves with --save-packages)
3. Removes container (frees GPU)
4. Optionally prompts to remove Docker image (or auto-removes with --images)

---

## container-create

**Create container with GPU allocation** (L2 atomic)

```bash
container-create <project-name> [image] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--cpu-only` | CPU-only container (no GPU) |
| `--num-migs=N` | Request N MIG partitions (default: 1) |
| `--prefer-full` | Prefer full GPU over MIG partitions |
| `-w, --workspace` | Custom workspace directory |
| `-d, --data` | Additional data directory to mount |
| `--dry-run` | Preview without executing |
| `--guided` | Educational mode |

**Examples:**
```bash
container-create my-project              # Create from custom image
container-create my-project pytorch      # Create with PyTorch framework
container-create data-prep --cpu-only    # CPU only
```

**Note:** Does not start the container. Use `container-start` or `container-run` after.

---

## container-start

**Start container in background** (L2 atomic)

```bash
container-start <project-name>
```

**Example:**
```bash
container-start my-project
container-list  # Check it's running
```

Container runs in background. Use `container-run` to enter.

---

## container-run

**Start (if stopped) and enter container** (L2 atomic)

```bash
container-run <project-name>
```

**Example:**
```bash
container-run my-project
# Now inside container
user@my-project:/workspace$
```

Exit with `exit` or Ctrl+D. Container keeps running after you exit.

---

## container-pause

**Freeze container processes** (L2 atomic)

```bash
container-pause [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Pause all your running containers |
| `--guided` | Educational mode |

**Examples:**
```bash
container-pause my-project    # Pause specific container
container-pause --all         # Pause all your containers
container-pause               # Interactive selection
```

Freezes all processes (SIGSTOP). GPU stays allocated, memory preserved. Use `container-unpause` to resume.

---

## container-unpause

**Resume frozen container** (L2 atomic)

```bash
container-unpause [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Unpause all your paused containers |
| `--guided` | Educational mode |

**Examples:**
```bash
container-unpause my-project  # Unpause specific container
container-unpause --all       # Unpause all your containers
container-unpause             # Interactive selection
```

Resumes all frozen processes. Container continues where it left off.

---

## container-stop

**Stop a running container** (L2 atomic)

```bash
container-stop [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --force` | Force stop (kill immediately) |
| `-t, --timeout SECS` | Timeout in seconds before force kill (default: 10) |
| `-a, --all` | Stop all your containers |
| `-v, --verbose` | Show detailed shutdown process |
| `--keep-container` | Don't prompt to remove container |
| `--guided` | Educational mode |

**Examples:**
```bash
container-stop my-project              # Graceful stop
container-stop my-project --force      # Force stop immediately
container-stop --all                   # Stop all your containers
container-stop my-project -t 30        # Wait 30 seconds before force kill
```

Container stopped but not removed. GPU held for configured duration.

**To free GPU immediately:** Use `container-retire` instead.

---

## container-remove

**Remove container and free GPU** (L2 atomic)

```bash
container-remove [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Remove all your stopped containers |
| `-i, --images` | Also remove associated Docker images |
| `-v, --volumes` | Also remove anonymous volumes |
| `-f, --force` | Skip all prompts |
| `--skip-removal-confirm` | Skip removal confirmation only |
| `--dry-run` | Show what would be removed |
| `--guided` | Educational mode |

**Examples:**
```bash
container-remove my-project              # Remove specific container
container-remove my-project --images     # Also remove Docker image
container-remove --all                   # Remove all stopped containers
container-remove --all --images --dry-run  # Preview bulk removal
```

Workspace files remain safe.

---

## container-list

**List your containers** (L2 atomic)

```bash
container-list [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Include stopped containers |
| `-d, --detailed` | Show detailed information |
| `--format FORMAT` | Output format (table, simple, json) |
| `--guided` | Educational mode |

**Examples:**
```bash
container-list              # Running containers
container-list --all        # Include stopped
container-list --detailed   # Show detailed info
```

**Example output:**
```
NAME            STATUS      GPU     UPTIME
my-project      Running     0:1     2h 34m
experiment-1    Running     0:2     45m
```

---

## container-stats

**Show resource usage** (L2 atomic)

```bash
container-stats [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-w, --watch` | Continuous monitoring (refresh every 2s) |
| `-g, --gpu` | Include GPU statistics |
| `--no-trunc` | Don't truncate output |
| `--guided` | Educational mode |

**Examples:**
```bash
container-stats             # All your containers
container-stats my-project  # Specific container
container-stats --watch     # Live monitoring
container-stats --gpu       # Include GPU usage
```

**Example output:**
```
CONTAINER      CPU %   MEM USAGE/LIMIT     MEM %   GPU MEM
my-project     245%    12.5GB / 64GB       19.5%   18.2GB
```

---

## container-attach

**Attach to running container** (L2 atomic)

```bash
container-attach <project-name>
```

**Alias:** `container-open`

Similar to `container-run` but doesn't start the container if it's stopped.

**Example:**
```bash
container-attach my-project
# Now inside container
user@my-project:/workspace$
```

Exit with `exit` or Ctrl+D. Container keeps running after you exit.

**Use when:** You want to enter a container that's already running, without auto-starting stopped containers.

---

## container-exit

**Information about exiting containers**

```bash
container-exit [--guided]
```

Displays information about how to exit containers. This is an informational command, not an action.

**Key points:**
- Type `exit` or press Ctrl+D to leave a container
- The container **keeps running** after you exit
- Your processes continue in the background
- Use `container-retire` to fully stop and free GPU

**Options:**
| Option | Description |
|--------|-------------|
| `--info` | Show exit information (default) |
| `--guided` | Show detailed explanations |

---

## Common Patterns

### Typical Workflow
```bash
container-deploy my-project --open   # Spin up for GPU work
# Work...
exit
container-retire my-project          # Done, free GPU
```

### Parallel Experiments
```bash
container-deploy exp-1 --background
container-deploy exp-2 --background
container-deploy exp-3 --background

# Later
container-retire exp-1
container-retire exp-2
container-retire exp-3
```

### Debugging
```bash
container-list                            # Check status
container-stats <project-name>            # Resource usage
docker logs <project-name>._.$(whoami)    # View logs (replace <project-name>)
```

---

## See Also

- [Image Commands](image-commands.md)
- [Daily Workflow Guide](../../core-guides/daily-workflow.md)
- [Troubleshooting](../../troubleshooting/)
