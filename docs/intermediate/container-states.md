# Container States

Understanding the full DS01 container lifecycle.

---

## State Models

### Beginner Model (Orchestrators)

```
running ←→ removed
```

With orchestrators like `container deploy` and `container retire`, you only see two states.

### Intermediate Model (Atomic)

```
created → running → stopped → removed
```

With atomic commands, you have full control over each transition.

---

## State Diagram

```
                container-create
                      ↓
                ┌──────────┐
                │ created  │  GPU allocated, not running
                └──────────┘
                      ↓
            container-start / container-run
                      ↓
                ┌──────────┐
            ┌──→│ running  │←──┐  Active, GPU in use
            │   └──────────┘   │
            │         ↓         │
            │  container-stop   │
            │         ↓         │
            │   ┌──────────┐   │
            │   │ stopped  │   │  Paused, GPU held temporarily
            │   └──────────┘   │
            │         ↓         │
            │  container-start  │
            └───────────────────┘
                      ↓
              container-remove
                      ↓
                ┌──────────┐
                │ removed  │  Container deleted, GPU freed
                └──────────┘
```

---

## State Details

### Created

**What it means:** Container exists but hasn't started yet.

```bash
container-create my-project
container-list --all  # Shows "created"
```

**GPU:** Allocated (reserved for you)
**Processes:** None running
**Workspace:** Configured but not mounted

**Transitions:**
- → `running`: `container-start` or `container-run`
- → `removed`: `container-remove`

---

### Running

**What it means:** Container is active and usable.

```bash
container-start my-project
container-list  # Shows "running"
```

**GPU:** Allocated and in use
**Processes:** Active
**Workspace:** Mounted at `/workspace`

**Transitions:**
- → `stopped`: `container-stop`
- → `removed`: `container-remove --stop`

---

### Stopped

**What it means:** Container paused, can be restarted.

```bash
container-stop my-project
container-list --all  # Shows "stopped"
```

**GPU:** Held temporarily (see GPU Hold Timeout below)
**Processes:** None running
**Workspace:** Not mounted (files safe on host)

**Transitions:**
- → `running`: `container-start` or `container-run`
- → `removed`: `container-remove`

---

### Removed

**What it means:** Container no longer exists.

```bash
container-remove my-project
container-list --all  # Not shown
```

**GPU:** Freed immediately
**Processes:** N/A
**Workspace:** Files still safe in `~/workspace/<project>/`

**To recreate:** `container-create my-project`

---

## GPU Hold Timeout

When you stop a container, the GPU isn't freed immediately.

**Why?** So you can restart quickly without losing your allocation.

**How long?** Check your limits:
```bash
check-limits
# Shows: gpu_hold_after_stop: 15m
```

**What happens:**
1. `container-stop my-project` → GPU held
2. Within 15 minutes: `container-start` works, same GPU
3. After 15 minutes: GPU freed automatically

**To free GPU immediately:**
```bash
container-remove my-project
# Or
container retire my-project
```

---

## Pause vs Stop

Both pause work, but differently:

### Pause (container-pause)

```bash
container-pause my-project
```

- Freezes processes in place (SIGSTOP)
- GPU stays allocated (no timeout)
- Memory state preserved
- Processes resume exactly where they left off

**Use for:** Brief breaks, meetings, lunch

### Stop (container-stop)

```bash
container-stop my-project
```

- Terminates all processes
- GPU held temporarily (timeout applies)
- State lost (but files saved)
- Must restart from scratch

**Use for:** Longer breaks, overnight

---

## Common Scenarios

### Scenario 1: Quick Break (15 minutes)

```bash
# Pause - keeps everything frozen
container-pause my-project

# Resume
container-unpause my-project
container-attach my-project
```

### Scenario 2: Lunch Break (1 hour)

```bash
# Stop - processes end, GPU held briefly
exit
container-stop my-project

# Resume (if within gpu_hold_after_stop)
container-start my-project
container-attach my-project
```

### Scenario 3: Done with GPU Work

```bash
# Retire - clean up everything
container retire my-project

# Later when needed - fresh start
container deploy my-project --open
```

### Scenario 4: Debugging

```bash
# Check what state it's in
container-list --all

# If stuck in "created"
container-start my-project

# If stuck in "stopped"
container-start my-project
# or
container-remove my-project  # clean slate
```

---

## State vs Orchestrator Commands

| State Transition | Orchestrator | Atomic |
|------------------|--------------|--------|
| → created | N/A | `container-create` |
| → running | `container deploy` | `container-start` |
| → stopped | N/A | `container-stop` |
| → removed | `container retire` | `container-remove` |

**Orchestrators skip states:**
- `container deploy` = create + start (skips "created")
- `container retire` = stop + remove (skips "stopped")

---

## Next Steps

- [Atomic Commands](atomic-commands.md) - Commands for each transition
- [CLI Flags](cli-flags.md) - Non-interactive usage
