# Command Hierarchy

DS01 has three interface levels, from simple to powerful.

---

## Overview

```
┌─────────────────────────────────────────────────────────┐
│  L3: Orchestrators (Beginner)                          │
│  └── project launch, container deploy, container retire │
├─────────────────────────────────────────────────────────┤
│  L2: Atomic (Intermediate)  ← You are here             │
│  └── container-create, -start, -stop, -remove          │
├─────────────────────────────────────────────────────────┤
│  L1: Docker (Advanced)                                  │
│  └── docker run, docker exec, docker logs               │
└─────────────────────────────────────────────────────────┘
```

---

## L3: Orchestrators (Beginner)

**Multi-step operations in one command.**

```bash
project launch my-thesis    # create image (if needed) + create container + start
container deploy my-project # create container + start
container retire my-project # stop + remove
```

**Characteristics:**
- Interactive by default
- Guides you through options
- Hides complexity
- Binary state model (running ↔ removed)

**Best for:** Daily interactive use, getting started.

---

## L2: Atomic (Intermediate)

**Single-step operations.**

```bash
container-create my-project  # Just create
container-start my-project   # Just start
container-stop my-project    # Just stop
container-remove my-project  # Just remove
```

**Characteristics:**
- One action per command
- CLI flags over prompts
- Full state model (created → running → stopped → removed)
- Required for scripting

**Best for:** Debugging, scripting, fine-grained control.

---

## L1: Docker (Advanced)

**Direct Docker commands.**

```bash
docker run -it --gpus device=0 ds01-$(id -u)/my-project:latest bash
docker exec -it my-project._.$(id -u) bash
docker logs my-project._.$(id -u)
```

**Characteristics:**
- Standard Docker commands
- Full Docker flexibility
- Still subject to DS01 enforcement (cgroups, limits)
- No DS01 conveniences (auto-mounting, metadata)

**Best for:** Complex workflows, Docker experts, batch jobs.

---

## Quick Comparison

| Feature | L3 Orchestrators | L2 Atomic | L1 Docker |
|---------|------------------|-----------|-----------|
| **Commands** | `project launch` | `container-create` | `docker run` |
| **Mode** | Interactive | CLI flags | Scripted |
| **Control** | Simple | Granular | Full |
| **State model** | 2 states | 4 states | Docker native |
| **Learning curve** | Easy | Medium | Advanced |
| **Use case** | Daily work | Debugging/scripting | Automation |

---

## When to Use Each

### Use Orchestrators (L3) When

- Starting GPU work: `project launch my-thesis --open`
- Finishing GPU work: `container retire my-thesis`
- Don't need fine control
- Learning DS01

### Use Atomic (L2) When

- Debugging: "Which step failed?"
- Scripting: Need programmatic control
- Pausing work: Stop without removing
- Creating multiple containers

### Use Docker (L1) When

- Building batch job pipelines
- Need Docker-specific features
- Integrating with external tools
- You're a Docker expert

---

## Command Mapping

| Task | L3 (Orchestrator) | L2 (Atomic) | L1 (Docker) |
|------|-------------------|-------------|-------------|
| Create + start | `container deploy` | `container-create` + `container-start` | `docker run -d` |
| Start + enter | `container deploy --open` | `container-run` | `docker run -it` |
| Enter running | - | `container-attach` | `docker exec -it` |
| Stop | - | `container-stop` | `docker stop` |
| Stop + remove | `container retire` | `container-stop` + `container-remove` | `docker stop` + `docker rm` |
| View logs | - | - | `docker logs` |

---

## Mixing Levels

You can mix levels as needed:

```bash
# Start with orchestrator
container deploy my-project

# Use atomic to stop (without removing)
container-stop my-project

# Restart with atomic
container-start my-project

# Debug with Docker
docker logs my-project._.$(id -u)

# Clean up with orchestrator
container retire my-project
```

---

## Next Steps

- [Atomic Commands](atomic-commands.md) - L2 command reference
- [Container States](container-states.md) - Full state model
- [Advanced Guide](../advanced/) - L1 Docker interface
