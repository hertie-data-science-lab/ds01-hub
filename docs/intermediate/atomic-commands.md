# Atomic Commands Reference

Complete reference for DS01's L2 atomic interface - single-purpose container and image commands.

---

## Overview

**Atomic commands = single-purpose operations.**

**Orchestrators (L3) do multiple steps:**
```bash
container deploy = create + start
container retire = stop + remove
```

**Atomic (L2) do one step:**
```bash
container-create   # Just create
container-start    # Just start
container-pause    # Freeze processes (GPU stays allocated)
container-unpause  # Resume frozen container
container-stop     # Just stop
container-remove   # Just remove
```

**Why use atomic:**
- Granular control
- Better debugging
- Required for scripting
- Understand system internals

---

## Container Lifecycle Commands

### `container-create` - Create Container

**Creates container from image without starting it.**

**Syntax:**
```bash
container-create <name> [options]
container-create                    # Interactive
```

**Common flags:**
```bash
--image=<name>          # Use specific Docker image
--project=<name>        # Mount specific project workspace
--workspace=<path>      # Mount custom path
--gpu=<count>           # Request GPUs (default: 1)
--guided                # Show explanations
-h, --help              # Show help
```

**Examples:**
```bash
# Create from project image
container-create my-thesis

# Create with specific image
container-create test --image=aime/pytorch:2.8.0-cuda12.4

# Create with 2 GPUs
container-create training --gpu=2

# Create with custom workspace
container-create analysis --workspace=/data/shared/dataset
```

**What it does:**
1. Allocates GPU(s) based on your limits
2. Creates Docker container (not started)
3. Saves metadata to `/var/lib/ds01/container-metadata/`
4. Sets up workspace mount (not active until start)

**Container state after:** `created` (not running)

**Next step:** `container-start <name>`

---

### `container-start` - Start Existing Container

**Starts a created or stopped container in background.**

**Syntax:**
```bash
container-start <name> [options]
container-start                     # Interactive
```

**Common flags:**
```bash
--guided                # Show explanations
-h, --help              # Show help
```

**Examples:**
```bash
# Start container in background
container-start my-thesis

# Interactive selection
container-start
```

**What it does:**
1. Validates GPU still available (if allocated)
2. Starts Docker container
3. Container runs in background
4. Clears any "stopped" timestamp

**Container state after:** `running` (detached)

**To connect:** `container-attach <name>`

---

### `container-run` - Start and Enter Container

**Starts container AND opens terminal (combined start + attach).**

**Syntax:**
```bash
container-run <name> [options]
container-run                       # Interactive
```

**Common flags:**
```bash
--guided                # Show explanations
-h, --help              # Show help
```

**Examples:**
```bash
# Start and enter
container-run my-thesis

# Interactive selection
container-run
```

**What it does:**
1. Starts container (like `container-start`)
2. Attaches terminal automatically
3. You're inside container ready to work

**Container state after:** `running` (attached)

**Difference from `container-start`:**
- `container-start` → background, requires `container-attach`
- `container-run` → foreground, terminal opens immediately

---

### `container-attach` - Connect to Running Container

**Opens terminal to running container.**

**Syntax:**
```bash
container-attach <name> [options]
container-attach                    # Interactive
```

**Common flags:**
```bash
--guided                # Show explanations
-h, --help              # Show help
```

**Examples:**
```bash
# Attach to container
container-attach my-thesis

# Interactive selection (shows only running containers)
container-attach
```

**What it does:**
1. Validates container is running
2. Opens bash shell inside container
3. You're at prompt in container

**Requirements:**
- Container must be in `running` state
- If stopped, use `container-start` first

**To exit without stopping:** Type `exit` or Ctrl+D

---

### `container-exit` - Exit Container Gracefully

**Exits container terminal cleanly.**

**Syntax:**
```bash
container-exit          # Run inside container
exit                    # Standard shell exit also works
```

**What it does:**
1. Closes current shell session
2. Container keeps running (unless it was the last process)
3. Returns you to host shell

**Common usage:**
```bash
# Inside container
container-exit

# Or just
exit

# Or
Ctrl+D
```

**Container state after:** Still `running` (if other processes exist)

---

### `container-pause` - Pause Container

**Freezes all container processes without stopping.**

**Syntax:**
```bash
container-pause <name> [options]
container-pause                      # Interactive
```

**Common flags:**
```bash
--all, -a               # Pause all running containers
--guided                # Show explanations
-h, --help              # Show help
```

**Examples:**
```bash
# Pause container
container-pause my-thesis

# Pause all containers
container-pause --all
```

**What it does:**
1. Sends SIGSTOP to all processes
2. Processes frozen in place
3. GPU remains allocated
4. Memory state preserved

**Container state after:** `paused`

**Use case:** Free CPU temporarily while keeping GPU and state

**To resume:** `container-unpause <name>`

---

### `container-unpause` - Resume Container

**Resumes frozen container processes.**

**Syntax:**
```bash
container-unpause <name> [options]
container-unpause                    # Interactive
```

**Examples:**
```bash
# Resume paused container
container-unpause my-thesis
```

**What it does:**
1. Sends SIGCONT to all processes
2. Processes continue where they left off

**Container state after:** `running`

---

### `container-stop` - Stop Container

**Stops running container without removing it.**

**Syntax:**
```bash
container-stop <name> [options]
container-stop                      # Interactive
```

**Common flags:**
```bash
--force                 # Force stop (don't prompt)
--guided                # Show explanations
-h, --help              # Show help
```

**Examples:**
```bash
# Stop container
container-stop my-thesis

# Force stop (skip confirmations)
container-stop my-thesis --force

# Interactive selection
container-stop
```

**What it does:**
1. Stops Docker container
2. Records stopped timestamp
3. Keeps GPU allocated (for `gpu_hold_after_stop` duration)
4. Container still exists (can restart)

**Container state after:** `stopped`

**GPU behavior:**
- GPU held temporarily (check your limits: `check-limits`)
- After timeout, GPU freed automatically
- To free immediately, use `container-remove`

**To restart:** `container-start <name>` or `container-run <name>`

**Note:** DS01 encourages `container-remove` instead of `container-stop` for resource efficiency.

---

### `container-remove` - Remove Container

**Removes stopped or created container.**

**Syntax:**
```bash
container-remove <name> [options]
container-remove                    # Interactive
```

**Common flags:**
```bash
--force                 # Skip confirmations
--stop                  # Stop first if running
--guided                # Show explanations
-h, --help              # Show help
```

**Examples:**
```bash
# Remove stopped container
container-remove my-thesis

# Stop and remove in one command
container-remove my-thesis --stop

# Force remove (skip prompts)
container-remove my-thesis --force

# Interactive selection
container-remove
```

**What it does:**
1. Removes Docker container
2. Frees GPU immediately
3. Deletes container metadata
4. Workspace files SAFE (on host)

**Container state after:** `removed` (doesn't exist)

**Cannot remove running container** - stop first or use `--stop` flag.

**Note:** Prefer `container retire` (orchestrator) which stops + removes in one step.

---

## Container Query Commands

### `container-list` - List Containers

**Shows all your containers.**

**Syntax:**
```bash
container-list [options]
```

**Common flags:**
```bash
--all                   # Include stopped containers
--format=<type>         # Output format (table, json, simple)
-h, --help              # Show help
```

**Examples:**
```bash
# List running containers
container-list

# List all (including stopped)
container-list --all

# JSON output (for scripting)
container-list --format=json
```

**Output:**
```
NAME           STATUS    IMAGE                          GPU      UPTIME
my-thesis      running   ds01-12345/my-thesis:latest    GPU-0    2h 15m
experiment     stopped   ds01-12345/experiment:latest   GPU-1    -
```

---

### `container-stats` - Resource Usage

**Shows resource usage for running containers.**

**Syntax:**
```bash
container-stats [options]
```

**Common flags:**
```bash
--watch                 # Continuous updates
--format=<type>         # Output format
-h, --help              # Show help
```

**Examples:**
```bash
# One-time stats
container-stats

# Continuous (like top)
container-stats --watch
```

**Output:**
```
NAME        CPU %    MEM USAGE     MEM %    GPU MEM    GPU %
my-thesis   125%     8.2GB/32GB    25%      12GB/40GB  85%
```

---

## Image Commands

### `image-create` - Build Docker Image

**Builds Docker image from project Dockerfile.**

**Syntax:**
```bash
image-create <project> [options]
image-create                        # Interactive
```

**Common flags:**
```bash
--no-cache              # Build from scratch (ignore cache)
--base=<image>          # Override base image
--guided                # Show explanations
-h, --help              # Show help
```

**Examples:**
```bash
# Build from ~/workspace/my-thesis/Dockerfile
image-create my-thesis

# Force rebuild (no cache)
image-create my-thesis --no-cache

# Interactive selection
image-create
```

**What it does:**
1. Reads `~/workspace/<project>/Dockerfile`
2. Builds Docker image
3. Tags as `ds01-<uid>/<project>:latest`
4. Image available for `container-create`

**Time:** 2-10 minutes depending on packages.

---

### `image-update` - Rebuild Image

**Rebuilds existing image (alias for `image-create`).**

**Syntax:**
```bash
image-update <project> [options]
```

**Use when:**
- Modified Dockerfile
- Want newer package versions
- Previous build had errors

**Example:**
```bash
# Edit Dockerfile
vim ~/workspace/my-thesis/Dockerfile

# Rebuild
image-update my-thesis

# Recreate containers to use new image
container-remove my-thesis
container-create my-thesis
```

---

### `image-list` - List Images

**Shows your Docker images.**

**Syntax:**
```bash
image-list [options]
```

**Common flags:**
```bash
--all                   # Include system images
--format=<type>         # Output format
-h, --help              # Show help
```

**Examples:**
```bash
# Your images
image-list

# All images (including AIME base images)
image-list --all
```

**Output:**
```
REPOSITORY                    TAG      SIZE     CREATED
ds01-12345/my-thesis          latest   8.2GB    2 days ago
ds01-12345/experiment         latest   6.5GB    1 week ago
```

---

### `image-delete` - Delete Image

**Removes Docker image.**

**Syntax:**
```bash
image-delete <name> [options]
image-delete                        # Interactive
```

**Common flags:**
```bash
--force                 # Skip confirmations
-h, --help              # Show help
```

**Examples:**
```bash
# Delete image
image-delete my-thesis

# Force delete
image-delete my-thesis --force

# Interactive selection
image-delete
```

**Warning:** Cannot delete if containers exist using this image. Remove containers first.

---

## State Transitions

**Full container lifecycle:**

```
                container-create
                    ↓
              ┌──────────┐
              │ created  │
              └──────────┘
                    ↓
          container-start / container-run
                    ↓
              ┌──────────┐
          ┌──→│ running  │←──┐
          │   └──────────┘   │
          │         ↓         │
          │  container-stop   │
          │         ↓         │
          │   ┌──────────┐   │
          │   │ stopped  │   │
          │   └──────────┘   │
          │         ↓         │
          │  container-start  │
          └──────────────────-┘
                    ↓
            container-remove
                    ↓
              ┌──────────┐
              │ removed  │
              └──────────┘
```

**GPU allocation:**
- Allocated: `created`, `running`, `stopped` (temporarily)
- Freed: `removed` or after `gpu_hold_after_stop` timeout

---

## Comparison: Orchestrators vs Atomic

| Task | Orchestrator (L3) | Atomic (L2) |
|------|-------------------|-------------|
| **Create and start** | `container deploy` | `container-create` + `container-start` |
| **Start and enter** | `container deploy --open` | `container-run` |
| **Stop and remove** | `container retire` | `container-stop` + `container-remove` |
| **Just create** | N/A | `container-create` |
| **Just stop** | N/A | `container-stop` |

**Orchestrators = convenience**

**Atomic = control**

---

## Common Workflows

### Workflow 1: Debug Container Creation

```bash
# Create container (test GPU allocation, image exists)
container-create my-project

# Check it was created
container-list --all

# Try starting
container-start my-project

# Success! Now use it
container-attach my-project
```

### Workflow 2: Pause Work Briefly

```bash
# Stop container, keep GPU allocation temporarily
exit
container-stop my-project

# Resume within GPU hold timeout
container-start my-project
container-attach my-project
```

### Workflow 3: Create Multiple Containers

```bash
# Create 3 containers
container-create exp-1
container-create exp-2
container-create exp-3

# Start all
container-start exp-1
container-start exp-2
container-start exp-3

# Work in one
container-attach exp-1

# When done, clean up
container-stop exp-1 && container-remove exp-1
container-stop exp-2 && container-remove exp-2
container-stop exp-3 && container-remove exp-3
```

### Workflow 4: Rebuild and Recreate

```bash
# Modify environment
vim ~/workspace/my-thesis/Dockerfile

# Rebuild image
image-update my-thesis

# Remove old container
container-remove my-thesis --stop

# Create new container from updated image
container-create my-thesis
container-run my-thesis
```

---

## Scripting Examples

### Script 1: Parallel Experiments

```bash
#!/bin/bash
# run-experiments.sh

for config in configs/*.yaml; do
  name=$(basename $config .yaml)

  # Create and start container
  container-create exp-$name --background
  container-start exp-$name

  # Run experiment
  container-attach exp-$name <<EOF
cd /workspace/experiments
python train.py --config $config
exit
EOF

  # Cleanup
  container-stop exp-$name
  container-remove exp-$name
done
```

### Script 2: Automated Testing

```bash
#!/bin/bash
# test-image.sh

PROJECT=$1

# Build image
image-create $PROJECT || exit 1

# Create test container
container-create test-$PROJECT || exit 1
container-start test-$PROJECT || exit 1

# Run tests
container-attach test-$PROJECT <<EOF
cd /workspace/$PROJECT
pytest tests/
EXIT_CODE=$?
exit $EXIT_CODE
EOF

TEST_RESULT=$?

# Cleanup
container-remove test-$PROJECT --stop

# Report
if [ $TEST_RESULT -eq 0 ]; then
  echo "Tests passed!"
else
  echo "Tests failed!"
  exit 1
fi
```

---

## Best Practices

### 1. Use Orchestrators for Daily Work

```bash
# Simple daily workflow - use orchestrators
project launch my-thesis --open    # Not container-create + container-start
container retire my-thesis         # Not container-stop + container-remove
```

**Reserve atomic for:**
- Debugging
- Scripting
- Special workflows

### 2. Don't Leave Containers Stopped

```bash
# Bad - wastes allocation
container-stop my-project
# ... forget about it for days

# Good - free resources
container-retire my-project
```

**Stopped containers hold GPU temporarily** - remove when done.

### 3. Check State Before Commands

```bash
# Before starting
container-list
# Is it created? running? stopped?

# Then choose correct command
container-start <name>    # If created or stopped
container-attach <name>   # If already running
```

### 4. Clean Up After Scripting

```bash
# At end of script
container-remove $CONTAINER_NAME --stop --force

# Or trap errors
trap "container-remove $CONTAINER_NAME --stop --force" EXIT
```

---

## Flags Reference

### Common Across Commands

```bash
--help, -h              Quick reference
--info                  Full reference
--concepts              Learn concepts first
--guided                Interactive learning
--force                 Skip confirmations
```

### Container Create

```bash
--image=<name>          Docker image to use
--project=<name>        Project workspace to mount
--workspace=<path>      Custom workspace path
--gpu=<count>           Number of GPUs (default: 1)
```

### Container Remove

```bash
--stop                  Stop before removing (if running)
--force                 Skip confirmations
```

### List Commands

```bash
--all                   Include stopped/all items
--format=<type>         Output format (table, json, simple)
```

### Image Build

```bash
--no-cache              Build from scratch (no layer cache)
--base=<image>          Override Dockerfile base image
```

---

## Next Steps

**Learn CLI efficiency:**

- → [CLI Flags Guide](cli-flags.md) - Use flags instead of interactive mode

**Understand state model:**

- → [Container States](container-states.md) - Full lifecycle explained

**Automate workflows:**

- → [Scripting Guide](scripting.md) - Write scripts with atomic commands

**Go deeper:**

- → [Advanced Guide](../advanced/) - Docker-native workflows
