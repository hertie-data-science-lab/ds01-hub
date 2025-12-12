# CLI Flags and Efficiency

Stop using interactive mode - master CLI flags for fast, scriptable workflows.

---

## From Interactive to Flags

**Beginner (interactive):**
```bash
container deploy
# Menu appears, select project, options...
```

**Intermediate (flags):**
```bash
container deploy my-project --open
```

**10x faster when you know what you want.**

---

## Universal Flags

**Every DS01 command supports:**

```bash
--help, -h              Quick reference
--info                  Full documentation
--concepts              Learn concept first
--guided                Step-by-step walkthrough
```

**Examples:**
```bash
container-deploy --help
image-create --info
project-init --concepts
container-retire --guided
```

---

## Container Deployment Flags

```bash
container deploy <name> [flags]

--open                  Create and open terminal (default)
--background            Create but don't attach
--project=<name>        Mount specific project
--workspace=<path>      Custom workspace mount
--image=<name>          Use specific image
--gpu=<count>           Request N GPUs
```

**Examples:**
```bash
# Standard deploy
container deploy my-thesis --open

# Background deploy
container deploy training --background

# Custom workspace
container deploy analysis --workspace=/data/shared

# Multi-GPU
container deploy distributed --gpu=2
```

---

## Project Commands Flags

```bash
project init <name> [flags]

--type=<type>           ml, cv, nlp, rl, llm, ts, audio
--quick                 Skip interactive questions, use defaults
--no-git                Skip Git initialization
--blank                 Create blank directory (no structure)
```

```bash
project launch <name> [flags]

--open                  Launch and open (default)
--background            Launch without attaching
--rebuild               Force image rebuild
```

**Examples:**
```bash
# Quick project creation
project init cv-research --type=cv --quick

# Launch with rebuild
project launch cv-research --rebuild --open
```

---

## Container Atomic Flags

```bash
container-create <name> [flags]

--image=<name>          Docker image
--project=<name>        Project workspace
--gpu=<count>           GPU count
```

```bash
container-remove <name> [flags]

--force                 Skip confirmations
--stop                  Stop if running
```

**Examples:**
```bash
# Create with options
container-create exp-1 --image=aime/pytorch:2.8.0 --gpu=2

# Force remove
container-remove exp-1 --force --stop
```

---

## Image Flags

```bash
image-create <project> [flags]

-f, --framework <name>  Base framework (pytorch, tensorflow, jax)
-t, --type <type>       Use case type (cv, nlp, rl, ml, custom)
--no-cache              Rebuild from scratch
```

```bash
image-delete <name> [flags]

--force                 Skip confirmations
```

**Examples:**
```bash
# Fresh build
image-create my-project --no-cache

# Quick delete
image-delete old-project --force
```

---

## List/Query Flags

```bash
container-list [flags]

--all                   Include stopped
--format=<type>         table, json, simple
```

```bash
image-list [flags]

--all                   Include base images
--format=json           JSON output
```

**Examples:**
```bash
# All containers as JSON
container-list --all --format=json

# Parse with jq
container-list --format=json | jq '.[] | select(.status=="running")'
```

---

## Flag Combinations

**Multiple flags together:**

```bash
# Background deploy with custom project
container deploy training --background --project=research-2024

# Force stop and remove
container-remove old-container --stop --force

# Fresh image build with framework
image-create my-project --no-cache -f pytorch -t nlp
```

---

## Scripting with Flags

```bash
#!/bin/bash
# deploy-and-train.sh

PROJECT=$1
CONFIG=$2

# Deploy in background
container deploy $PROJECT --background --gpu=2 || exit 1

# Wait for startup
sleep 5

# Run training
docker exec $PROJECT._.$(id -u) python /workspace/train.py --config $CONFIG

# Check results
docker exec $PROJECT._.$(id -u) cat /workspace/results/metrics.txt

# Cleanup
container retire $PROJECT --force
```

---

## Next Steps

- → [Container States](container-states.md) - Understand full lifecycle

- → [Scripting Guide](scripting.md) - Automate with bash scripts

- → [Efficiency Tips](efficiency-tips.md) - More shortcuts
