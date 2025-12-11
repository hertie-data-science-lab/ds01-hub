# Intermediate Guide

**For users who want more control over container lifecycle and CLI efficiency.**

---

## You're Ready If

- You're comfortable with `project launch` and `container deploy|retire`
- You want fine-grained control (create/start/stop/remove separately)
- You're interested in scripting and automation

**Not there yet?** → [Getting Started](../getting-started/) | [Guides](../guides/)

**Beyond this?** → [Advanced](../advanced/)

---

## What's Here

### Core References

| Guide | What You'll Learn |
|-------|-------------------|
| [Command Hierarchy](command-hierarchy.md) | L3/L2/L1 interface levels explained |
| [Atomic Commands](atomic-commands.md) | Individual lifecycle commands (`container-create`, `start`, `stop`, `remove`) |
| [CLI Flags](cli-flags.md) | Non-interactive usage, common flags |
| [Container States](container-states.md) | Full 4-state lifecycle model |

### Practical Guides

| Guide | What You'll Learn |
|-------|-------------------|
| [Scripting (Bash)](scripting-bash.md) | Shell automation patterns |
| [Scripting (Python)](scripting-python.md) | Subprocess-based automation |
| [Efficiency Tips](efficiency-tips.md) | Keyboard shortcuts, workflow optimizations |
| [Shell Aliases](shell-aliases.md) | Shortcuts for your `~/.bashrc` |

---

## The Key Difference

**Beginner (Orchestrators):**
```bash
container deploy my-project   # Creates + starts
container retire my-project   # Stops + removes
```

**Intermediate (Atomic):**
```bash
container-create my-project   # Create only
container-start my-project    # Start only
container-stop my-project     # Stop only (keeps container)
container-remove my-project   # Remove only
```

**Why?** Debug issues step-by-step, pause without losing GPU, enable scripting.

---

## Suggested Path

1. **[Command Hierarchy](command-hierarchy.md)** - Understand L3/L2/L1 levels
2. **[Atomic Commands](atomic-commands.md)** - Learn the individual commands
3. **[Container States](container-states.md)** - Understand the full lifecycle
4. **[CLI Flags](cli-flags.md)** - Ditch interactive mode
5. **[Scripting](scripting-bash.md)** - Automate your workflows
