# Container Commands

Commands for container lifecycle management.

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
| `--gpu <N>` | Request N GPUs |
| `--framework <name>` | Specify framework (pytorch, tensorflow, jax) |
| `--image <name>` | Use specific image |
| `--guided` | Educational mode |

**Examples:**
```bash
container-deploy my-project              # Interactive
container-deploy my-project --open       # Create and enter
container-deploy my-project --background # Background mode
container-deploy my-project --gpu 2      # Multiple GPUs
```

**What it does:**
1. Checks resource availability
2. Runs `container-create` (allocates GPU)
3. Runs `container-start` or `container-run` based on flags

---

## container-retire

**Stop and remove a container, free GPU** (L3 orchestrator)

```bash
container-retire <project-name> [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--force` | Skip confirmation prompts |
| `--images` | Also remove Docker image |

**Examples:**
```bash
container-retire my-project           # Interactive
container-retire my-project --force   # Skip confirmations
container-retire my-project --images  # Also remove image
```

**What it does:**
1. Stops container
2. Removes container (frees GPU)
3. Optionally removes image

---

## container-create

**Create container with GPU allocation** (L2 atomic)

```bash
container-create <project-name> [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--gpu <N>` | Request N GPUs (default: 1) |
| `--framework <name>` | Base framework |
| `--image <name>` | Specific Docker image |

**Examples:**
```bash
container-create my-project            # Default settings
container-create my-project --gpu 2    # Multiple GPUs
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

## container-stop

**Stop a running container** (L2 atomic)

```bash
container-stop <project-name>
```

**Example:**
```bash
container-stop my-project
```

Container stopped but not removed. GPU held for configured duration.

**To free GPU immediately:** Use `container-retire` instead.

---

## container-remove

**Remove container and free GPU** (L2 atomic)

```bash
container-remove <project-name> [--force]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--force` | Remove even if running |

**Example:**
```bash
container-remove my-project
```

Workspace files remain safe.

---

## container-list

**List your containers** (L2 atomic)

```bash
container-list [--all]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--all` | Include stopped containers |

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
container-stats [project-name]
```

**Example output:**
```
CONTAINER      CPU %   MEM USAGE/LIMIT     MEM %   GPU MEM
my-project     245%    12.5GB / 64GB       19.5%   18.2GB
```

---

## Common Patterns

### Daily Workflow
```bash
container-deploy my-project --open   # Morning
# Work...
exit
container-retire my-project          # Evening
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
container-list                        # Check status
container-stats my-project            # Resource usage
docker logs my-project._.$(whoami)    # View logs
```

---

## See Also

- [Image Commands](image-commands.md)
- [Daily Workflow Guide](../../guides/daily-workflow.md)
- [Troubleshooting](../../troubleshooting/)
