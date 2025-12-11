# Intermediate Users Guide

**For users who've mastered the basics and want more control.**

---

## Who This Is For

**You're ready for intermediate docs if:**
- ✓ You've used DS01 for a few weeks
- ✓ You're comfortable with `project launch` / `container retire`
- ✓ You understand ephemeral containers and workspaces
- ✓ You want more granular control
- ✓ You're interested in CLI efficiency and scripting

**Not there yet?** Start with:
- [Getting Started](../getting-started/) - Basics
- [Guides](../guides/) - Task-oriented workflows

**Beyond this?** See:
- [Advanced](../advanced/) - Direct Docker, terminal workflows

---

## What You'll Learn

### 1. Atomic Commands

**Move beyond orchestrators:**

**Beginner level:**
```bash
project launch my-project    # One command, multiple steps
container retire my-project  # One command, cleanup
```

**Intermediate level:**
```bash
container-create my-project  # Create only
container-start my-project   # Start separately
container-stop my-project    # Stop without removing
container-remove my-project  # Remove explicitly
```

**Why learn this:**
- Fine-grained control over container lifecycle
- Better debugging (isolate which step fails)
- Required for automation/scripting

- → [Atomic Commands Reference](atomic-commands.md)

### 2. CLI Flags and Efficiency

**Move beyond interactive mode:**

**Beginner level:**
```bash
container deploy            # Interactive menu
```

**Intermediate level:**
```bash
container-deploy my-project --open               # Direct
container-deploy my-project --background         # Background
container-deploy my-project --project=other      # Custom project
container-deploy my-project --gpu=2              # Multi-GPU
```

**Why learn this:**
- Faster workflows
- Scriptable commands
- Better for automation

- → [CLI Flags Reference](cli-flags.md)

### 3. Full Container State Model

**Understand all states:**

**Beginner model (L3 Orchestrators):**
```
running ←→ removed
```

**Intermediate model (L2 Atomic):**
```
created → running → stopped → removed
```

**Why learn this:**
- GPU hold timeout makes sense
- Can pause work without losing allocation
- Better control over resource usage

- → [Container States](container-states.md)

### 4. Scripting Workflows

**Automate repetitive tasks:**

**Manual (beginner):**
```bash
# Run 5 experiments manually
project launch exp-1
# work...
container retire exp-1

project launch exp-2
# work...
container retire exp-2
# ... repeat 3 more times
```

**Scripted (intermediate):**
```bash
# Script to run 5 experiments
for i in {1..5}; do
  container-deploy exp-$i --background
  container-attach exp-$i
  python train.py --config config-$i.yaml
  exit
  container-retire exp-$i
done
```

**Why learn this:**
- Run many experiments efficiently
- Reproducible workflows
- Save time on repetitive tasks

- → [Scripting Guide](scripting.md)

---

## The Command Hierarchy

DS01 has three interface levels:

### L3: Orchestrators (Beginner)

**Multi-step operations:**
- `project launch` = create + start
- `container deploy` = create + start
- `container retire` = stop + remove

**Best for:** Daily interactive use

### L2: Atomic (Intermediate) ← **You are here**

**Single-step operations:**
- `container-create` = create only
- `container-start` = start only
- `container-stop` = stop only
- `container-remove` = remove only

**Best for:**
- Power users who want control
- Debugging specific steps
- Automation and scripting
- Understanding system internals

### L1: Docker (Advanced)

**Direct Docker commands:**
- `docker run` (with DS01 enforcement)
- `docker exec` for direct access
- `docker logs` for debugging

**Best for:**
- Terminal-native workflows
- Advanced debugging
- Non-interactive batch jobs

---

## Learning Path

### Week 1-2: Master the Basics

**Start with beginner docs:**
1. [Getting Started](../getting-started/first-time.md)
2. [Daily Workflow](../getting-started/daily-workflow.md)
3. [Creating Projects](../guides/creating-projects.md)

**Goal:** Comfortable with `project launch` / `container retire`.

### Week 3-4: Explore Atomic Commands

**Graduate to intermediate:**
1. [Atomic Commands](atomic-commands.md) - Full L2 reference
2. [CLI Flags](cli-flags.md) - Stop using interactive mode
3. [Container States](container-states.md) - Understand lifecycle

**Goal:** Use atomic commands confidently, no interactive menus needed.

### Week 5+: Optimize Workflows

**Become a power user:**
1. [Scripting](scripting.md) - Automate experiments
2. [Efficiency Tips](efficiency-tips.md) - Keyboard shortcuts, aliases
3. [Advanced](../advanced/) - Terminal workflows

**Goal:** Fast, efficient, scriptable workflows.

---

## Quick Comparison

| Feature | Beginner (L3) | Intermediate (L2) | Advanced (L1) |
|---------|---------------|-------------------|---------------|
| **Commands** | `project launch` | `container-create` | `docker run` |
| **Mode** | Interactive | CLI flags | Scripted |
| **Control** | Simple | Granular | Full |
| **State model** | 2 states | 4 states | Docker native |
| **Use case** | Daily work | Power users | Automation |
| **Learning curve** | Easy | Moderate | Steep |

---

## When to Use Atomic Commands

### Scenario 1: Debugging Container Creation

**Problem:** `project launch` fails, not sure which step broke.

**Solution:** Use atomic commands to isolate:
```bash
# Try creating
container-create my-project
# Success? Image exists, GPU available

# Try starting
container-start my-project
# Success? Container created properly

# Try running
container-run my-project
# Success? No startup script issues
```

**Each step tested independently.**

### Scenario 2: Pausing Work Without Losing GPU

**Problem:** Need to step away for 30 minutes, don't want to lose GPU allocation.

**Beginner approach:**
```bash
# Leave container running (wastes GPU if idle)
# Or container retire (loses allocation)
```

**Intermediate approach:**
```bash
# Inside container
exit

# Stop container, keep GPU for brief period
container-stop my-project

# Resume later (within GPU hold timeout)
container-start my-project
container-attach my-project
```

**GPU held during stop period (configurable).**

### Scenario 3: Creating Containers in Background

**Problem:** Want to create multiple containers, open one to work in.

**Beginner approach:**
```bash
project launch exp-1 --open      # Work here
# Can't easily create others without leaving
```

**Intermediate approach:**
```bash
# Create all containers
container-create exp-1
container-create exp-2
container-create exp-3

# Start all
container-start exp-1
container-start exp-2
container-start exp-3

# Attach to one
container-attach exp-1
```

**More flexible workflow.**

---

## Prerequisites

**Before diving into intermediate docs:**

1. **Completed beginner tutorials:**
   - [ ] Used `project launch` successfully
   - [ ] Understand workspace persistence
   - [ ] Know how to edit Dockerfiles
   - [ ] Comfortable with `container-list` / `container-stats`

2. **Comfortable with Linux CLI:**
   - [ ] Navigate directories (`cd`, `ls`, `pwd`)
   - [ ] Edit files (`vim` or `nano`)
   - [ ] Understand flags/options (`--flag`, `-f`)
   - [ ] Basic shell scripting (`for`, `if`, variables)

3. **Understand DS01 concepts:**
   - [ ] Images vs containers
   - [ ] Ephemeral model
   - [ ] `/workspace/` persistence

**Need to review?**
- [Linux Basics](../background/linux-basics.md)
- [Containers and Images](../concepts/containers-and-images.md)
- [Ephemeral Containers](../concepts/ephemeral-containers.md)

---

## Documentation Structure

### Core References

- **[Atomic Commands](atomic-commands.md)** - Complete L2 command reference
  - `container-create`, `start`, `stop`, `remove`, `run`, `attach`, `exit`
  - `image-create`, `update`, `list`, `delete`
  - All flags and options

- **[CLI Flags](cli-flags.md)** - Efficient command-line usage
  - Common flags across commands
  - Flag combinations
  - Non-interactive usage

- **[Container States](container-states.md)** - Full lifecycle model
  - Created vs running vs stopped vs removed
  - GPU hold timeout behavior
  - State transitions

### Practical Guides

- **[Scripting](scripting.md)** - Automation patterns
  - Bash scripts for common tasks
  - Parallel experiments
  - Error handling

- **[Efficiency Tips](efficiency-tips.md)** - Power user shortcuts
  - Shell aliases
  - Keyboard shortcuts
  - Workflow optimizations

---

## Key Differences from Beginner Docs

| Aspect | Beginner Docs | Intermediate Docs |
|--------|---------------|-------------------|
| **Pace** | Slow, explanatory | Faster, assumes knowledge |
| **Commands** | Interactive mode | CLI flags emphasized |
| **Depth** | Essential features | All options covered |
| **Examples** | Copy-paste ready | Adapt to your needs |
| **Audience** | Never used DS01 | Used DS01 for weeks |

---

## Next Steps

**Start here:**

1. [Atomic Commands Reference](atomic-commands.md) - Learn L2 commands
2. [CLI Flags Guide](cli-flags.md) - Ditch interactive mode
3. [Container States](container-states.md) - Understand lifecycle

**Then:**

4. [Scripting Guide](scripting.md) - Automate workflows
5. [Efficiency Tips](efficiency-tips.md) - Speed up your work

**Beyond intermediate:**

6. [Advanced Guide](../advanced/) - Docker interface, terminal workflows

---

**Ready to level up? Start with [Atomic Commands](atomic-commands.md).**
