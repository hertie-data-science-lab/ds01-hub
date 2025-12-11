# Intermediate Users Guide

**For users who've got the basics and want more control.**

---

## Who This Is For

**You're ready for intermediate docs if:**
- You've used DS01 for a few weeks
- You're comfortable with `project launch` / `container deploy|retire`
- You understand ephemeral containers and workspaces
- You want more granular control
- You're interested in CLI efficiency and scripting

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
container deploy|retire my-project  # One command, cleanup
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

→ [Atomic Commands Reference](atomic-commands.md)

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

→ [CLI Flags Reference](cli-flags.md)

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

→ [Container States](container-states.md)

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

→ [Scripting (Bash)](scripting-bash.md) | [Scripting (Python)](scripting-python.md)

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
- `container create` = create only
- `container start` = start only
- `container stop` = stop only
- `container remove` = remove only

### L1: Docker (Advanced)

**Direct Docker commands:**
- `docker run` (with DS01 enforcement)
- `docker exec` for direct access
- `docker logs` for debugging

---

## Quick Comparison

| Feature | Beginner (L3) | Intermediate (L2) | Advanced (L1) |
|---------|---------------|-------------------|---------------|
| **Commands** | `project launch` | `container-create` | `docker run` |
| **Mode** | Interactive | CLI flags | Scripted |
| **Control** | Simple | Granular | Full |
| **State model** | 2 states | 4 states | Docker native |
| **Use case** | Beginner | Advanced users | Automation |

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
---

## Documentation Structure & Next Steps

### Start here: 
**Core References**

1. **[Atomic Commands](atomic-commands.md)** - Learn L2 commands
    - `container-create`, `start`, `stop`, `remove`, `run`, `attach`, `exit`
    - `image-create`, `update`, `list`, `delete`
    - All flags and options

2. **[CLI Flags](cli-flags.md)** - Efficient command-line usage -> ditch interactive mode
    - Common flags across commands
    - Flag combinations
    - Non-interactive usage

3. **[Container States](container-states.md)** - Full lifecycle model
    - Created vs running vs stopped vs removed
    - GPU hold timeout behavior
    - State transitions

### Then: 
**Practical Guides**

4. **Scripting** - Automation patterns
    - [Bash](scripting-bash.md) - Native shell scripting (simple, fast)
    - [Python](scripting-python.md) - Structured automation (complex workflows)

5. **[Efficiency Tips](efficiency-tips.md)** - Speed up your work w/ shortcuts
    - Keyboard shortcuts
    - Workflow optimizations

6. **[Shell Aliases](shell-aliases.md)** - Command shortcuts for your `~/.bashrc`
    - Short aliases (`pl`, `ca`, `cr`, etc.)
    - Common patterns (`plo`, `crf`)

### Finally:
**Beyond intermediate**

7. [Advanced Guide](../advanced/) - Docker interface, terminal workflows