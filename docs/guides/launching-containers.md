# Launching Containers

Understand when to use `project launch` vs `container deploy` and other container commands.

---

## Quick Answer

**Most of the time, use:**

```bash
project launch my-project --open
```

This is smart: checks if image exists, offers to build if needed, then launches.

---

## The Two Main Commands

### `project launch` - Smart Launcher (Recommended)

**What it does:**
1. Checks if project image exists
2. If missing, offers to build it
3. Creates container
4. Starts container
5. Optionally opens terminal

**When to use:** Daily workflow, any time you want to work.

**Example:**
```bash
# Smart - handles everything
project launch my-thesis --open

# Also works
project launch   # Interactive project selection
```

**Benefits:**
- Beginner-friendly
- Handles missing images
- One command to start working
- Matches "launch a project" mental model

### `container deploy` - Direct Deploy

**What it does:**
1. Creates container from existing image
2. Starts container
3. Optionally opens terminal

**When to use:**
- Image already exists
- You want fine-grained control
- Deploying AIME base images (not custom projects)

**Example:**
```bash
# Requires image to exist
container deploy my-thesis --open

# Interactive selection
container deploy
```

**Benefits:**
- Faster (no image check)
- Works with AIME base images
- Direct control

**Limitation:** Fails if image doesn't exist.

---

## Decision Tree

**Starting out?**
```bash
project launch my-project
```

**Image definitely exists?**
```bash
container deploy my-project
```

**Want AIME base image (not custom)?**
```bash
container deploy   # Select from AIME catalog
```

**Not sure?**
```bash
project launch     # Safer choice
```

---

## Detailed Comparison

| Feature | `project launch` | `container deploy` |
|---------|------------------|-------------------|
| **Checks image exists** | ✓ Yes | ✗ No |
| **Offers to build image** | ✓ Yes | ✗ No |
| **Works with custom projects** | ✓ Yes | ✓ Yes |
| **Works with AIME base images** | Limited | ✓ Yes |
| **Reads pyproject.toml** | ✓ Yes | ✗ No |
| **Interactive mode** | ✓ Yes | ✓ Yes |
| **Speed** | Slightly slower | Faster |
| **Best for** | Daily workflow | Power users |

---

## All Container Commands

### Creation & Starting

```bash
# L3 Orchestrators (Multi-step)
project launch <project>       # Smart: check + build + create + start
container deploy <name>        # Direct: create + start

# L2 Atomic (Single-step) - Advanced
container-create <name>        # Create only (not started)
container-start <name>         # Start existing stopped container
container-run <name>           # Start and enter terminal
```

### Connecting to Running Containers

```bash
container-attach <name>        # Connect to running container
```

**Note:** `container-attach` only works with **running** containers. Use `project launch` if container doesn't exist.

### Stopping & Removing

```bash
# L3 Orchestrator
container retire <name>        # Stop + remove + free GPU

# L2 Atomic - Advanced
container-stop <name>          # Stop only (holds GPU briefly)
container-remove <name>        # Remove only
```

### Information

```bash
container-list                 # List your containers
container-stats                # Resource usage
```

---

## When to Use Each Command

### Daily Workflow: `project launch`

```bash
# Morning
project launch my-thesis --open

# Afternoon (different project)
container retire my-thesis
project launch other-project --open

# Evening
container retire other-project
```

**Why:** Handles everything, beginner-friendly.

### Quick Deployment: `container deploy`

```bash
# You know image exists
container deploy my-project --open

# Testing AIME base image
container deploy   # Select from catalog
```

**Why:** Faster when image definitely exists.

### Reconnecting: `container-attach`

```bash
# Container already running
container-attach my-project

# Check what's running first
container-list
container-attach <name>
```

**Why:** Connect to existing session.

### Cleanup: `container retire`

```bash
# Done for the day
exit
container retire my-project
```

**Why:** Frees GPU immediately, removes container.

---

## Interactive Mode

**All main commands work without arguments:**

```bash
# These open friendly menus
project launch
container deploy
container-attach
container retire
```

**Example: `project launch`**
```
Select a project to launch:

  1) my-thesis          (PyTorch 2.8.0)
  2) research-2024      (TensorFlow 2.16.1)
  3) experiments        (JAX 0.4.23)

Choice [1-3]: _
```

**Beginner-friendly:** No need to remember project names.

---

## Common Patterns

### Pattern 1: New Project Start to Finish

```bash
# Create project
project init my-research

# Launch it (includes build)
project launch my-research --open

# Work...

# Done
exit
container retire my-research
```

### Pattern 2: Existing Project Daily Use

```bash
# Morning
project launch my-thesis --open

# Work all day...

# Evening
exit
container retire my-thesis
```

### Pattern 3: Quick Experiment

```bash
# Deploy fast
container deploy experiment --open

# Test idea...

# Cleanup
exit
container retire experiment
```

### Pattern 4: Background Work + Reconnect

```bash
# Launch in background
project launch training --background

# Later: attach
container-attach training

# Start training...

# Detach without stopping
exit  # Container keeps running

# Reconnect later
container-attach training
```

---

## Flags & Options

### `project launch` Options

```bash
project launch <name> [options]

Options:
  --open              Create and open terminal (default)
  --background        Create but don't open terminal
  --rebuild           Force rebuild image even if exists
  --guided            Show explanations
  -h, --help          Show help
```

**Examples:**
```bash
# Most common
project launch my-thesis --open

# Background startup
project launch my-thesis --background

# Force rebuild image
project launch my-thesis --rebuild
```

### `container deploy` Options

```bash
container deploy <name> [options]

Options:
  --open              Deploy and open terminal (default)
  --background        Deploy but don't open terminal
  --project=<name>    Use specific project workspace
  --image=<name>      Use specific Docker image
  --guided            Show explanations
  -h, --help          Show help
```

**Examples:**
```bash
# Standard deploy
container deploy my-project --open

# Background
container deploy my-project --background

# Custom image
container deploy test --image=aime/pytorch:2.8.0
```

### `container retire` Options

```bash
container retire <name> [options]

Options:
  --force             Skip confirmations
  --keep-image        Don't offer to remove image
  --guided            Show explanations
  -h, --help          Show help
```

---

## Advanced: L2 Atomic Commands

**Most users don't need these** - `project launch` and `container retire` cover daily workflow.

**Use atomic commands when:**
- You need granular control
- Building scripts/automation
- Debugging issues

### Creating Without Starting

```bash
# Create container (not started)
container-create my-project

# Later: start it
container-start my-project

# Or: start and enter
container-run my-project
```

**Workflow:**
```
container-create  → Container exists but stopped
container-start   → Container running in background
container-attach  → Connect to running container
```

### Stopping Without Removing

```bash
# Stop container (keeps container, holds GPU briefly)
container-stop my-project

# Later: restart
container-start my-project
```

**Note:** DS01 encourages ephemeral containers - `container retire` (stop + remove) is preferred.

---

## Understanding Container States

### With L3 Commands (Recommended)

**Simple two-state model:**
- **Running** - Created and started, ready to use
- **Removed** - Doesn't exist, can recreate anytime

**Transitions:**
```
project launch → Running
container retire → Removed
```

### With L2 Commands (Advanced)

**Full four-state model:**
- **Created** - Exists but not started
- **Running** - Active, can attach
- **Stopped** - Paused (holds GPU temporarily)
- **Removed** - Deleted

**Transitions:**
```
container-create → Created
container-start  → Running
container-stop   → Stopped
container-remove → Removed
```

**Most users:** Stick with L3 commands, simpler mental model.

---

## Troubleshooting

### "Image not found"

**Using `container deploy`:**
```
Error: Image ds01-username/my-project:latest not found
```

**Fix:** Use `project launch` instead (builds if needed):
```bash
project launch my-project
```

**Or build manually:**
```bash
image-create my-project
container deploy my-project
```

### "Container already exists"

**You ran `project launch` but container already running.**

**Fix:** Use `container-attach`:
```bash
# Check what's running
container-list

# Attach to it
container-attach my-project
```

**Or retire and relaunch:**
```bash
container retire my-project
project launch my-project
```

### "No GPUs available"

**All GPUs in use.**

**Options:**

1. **Wait and retry:**
   ```bash
   dashboard gpu    # Check availability
   ```

2. **Join queue:**
   ```bash
   gpu-queue join
   ```

3. **Work on something else:**
   ```bash
   project launch other-project
   ```

### Container Exits Immediately

**Symptom:** `project launch` succeeds but `container-attach` says "not running".

**Cause:** Container startup command failed.

**Debug:**
```bash
# Check logs
docker logs <container-name>._.$(id -u)

# Check image
docker images | grep my-project
```

**Common fixes:**
- Rebuild image: `image-update my-project`
- Check Dockerfile syntax
- Verify base image exists

---

## Best Practices

### 1. Use `project launch` for Daily Work

```bash
# Simpler, handles edge cases
project launch my-thesis
```

Instead of:
```bash
# More steps, can fail
image-create my-thesis   # Did you already build?
container deploy my-thesis
```

### 2. Always `container retire` When Done

```bash
# Frees GPU immediately
container retire my-project
```

Instead of:
```bash
# Holds GPU, clutters system
container-stop my-project  # Don't do this
```

### 3. Use Interactive Mode When Unsure

```bash
# Let the menu guide you
project launch
container-attach
container retire
```

### 4. Check Status Before Acting

```bash
# What's running?
container-list

# Then decide
container-attach <name>    # If running
project launch <name>      # If not running
```

---

## Command Cheat Sheet

**Start working:**
```bash
project launch my-project --open
```

**Reconnect:**
```bash
container-attach my-project
```

**Done for the day:**
```bash
exit
container retire my-project
```

**See what's running:**
```bash
container-list
```

**Check system status:**
```bash
dashboard
```

---

## Next Steps

**Learn the daily workflow:**

→ [Daily Workflow Guide](../getting-started/daily-workflow.md)

**Understand container lifecycle:**

→ [Ephemeral Containers Concept](../concepts/ephemeral-containers.md)

**Create new projects:**

→ [Creating Projects Guide](creating-projects.md)

**Advanced container management:**

→ [Container Management Reference](../reference/container-commands.md)
