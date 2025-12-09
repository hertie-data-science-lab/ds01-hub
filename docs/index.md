# DS01 - GPU Container Platform

**GPU-enabled container infrastructure for data science and machine learning research.**

Think of DS01 as your personal data science workstation in the cloud - you can create isolated work environments, request GPUs when you need them, and your files are always safe.

---

## Get Started in 5 Minutes

**Never used DS01 before?** Run this once:

```bash
user-setup
```

This walks you through everything: SSH keys, your first project, and connecting from your laptop.

**Already set up?** Your daily workflow is simple:

```bash
# Morning - start working
project launch my-thesis --open

# Work on your code, train models...

# Evening - done for the day
exit
container retire my-thesis
```

**Your files in `~/workspace/` are always saved** - containers are temporary, your work is permanent.

---

## Quick Navigation

**I want to...**

→ [Set up DS01 for the first time](getting-started/first-time.md) - Run `user-setup`

→ [Understand the daily workflow](getting-started/daily-workflow.md) - What to do each day

→ [Create a new project](guides/creating-projects.md) - `project init my-project`

→ [Build a custom environment](guides/custom-environments.md) - Add packages to your Dockerfile

→ [Run Jupyter notebooks](guides/jupyter-notebooks.md) - JupyterLab setup

→ [Use VS Code remotely](guides/vscode-remote.md) - Connect your IDE

→ [Fix a problem](troubleshooting/) - Common errors and solutions

---

## Essential Commands

```bash
# Getting started
user-setup              # First-time setup wizard (run once)
commands                # Show all available commands

# Daily workflow
project launch          # Start working on a project
container retire        # Done for the day (frees GPU)
container list          # See your containers

# Status
dashboard               # System status, GPU availability
check-limits            # Your resource quotas

# Help
<command> --help        # Quick reference
<command> --guided      # Step-by-step with explanations
<command> --concepts    # Learn what something is
```

---

## How DS01 Works

**Containers = Temporary Work Sessions**
- Like turning on a laptop when you arrive, turning it off when you leave
- Create them when you need to work, remove them when you're done
- GPUs are allocated when container starts, freed when you retire it

**Workspaces = Your Permanent Storage**
- Everything in `~/workspace/` survives container removal
- Save your code, data, models here - they're always safe
- Think of it like files on a network drive

**Images = Recipes for Environments**
- Define what software is installed (PyTorch, pandas, etc.)
- Stored in Dockerfiles - version controlled, shareable
- Rebuild containers from images anytime

**Why this model?**
- **Efficient**: GPUs freed immediately for others
- **Reproducible**: Same environment every time
- **Cloud-native**: Same workflow as AWS/GCP/Kubernetes
- **Flexible**: Multiple projects with different environments

→ [Learn more about containers](concepts/containers-and-images.md) *(optional)*

---

## Getting Help

**Built-in help system:**
- `<command> --help` - Quick reference
- `<command> --info` - Full reference with all options
- `<command> --concepts` - Explain concepts before running
- `<command> --guided` - Interactive mode with explanations

**Examples:**
```bash
# New to containers? Learn first, then run
image-create --concepts
image-create --guided

# Just need syntax? Quick reference
container-deploy --help
```

**Stuck?**
1. Check [troubleshooting docs](troubleshooting/)
2. Run `ds01-health-check` for diagnostics
3. Contact your system administrator

---

## Learning Paths

### Path 1: Beginner (Students, First-Time Users)
**"I just want to work on my thesis"**

1. [First-Time Setup](getting-started/first-time.md) - 15 minutes
2. [Daily Workflow](getting-started/daily-workflow.md) - Your routine
3. [Jupyter Setup](guides/jupyter-notebooks.md) - If using notebooks
4. [VS Code Remote](guides/vscode-remote.md) - If using VS Code

**Use:** `project launch`, `container retire`

**Skip the background reading** - learn as you go with `--guided` mode.

### Path 2: Intermediate (Power Users)
**"I want more control and efficiency"**

1. [Atomic Commands](intermediate/atomic-commands.md) - Granular control
2. [CLI Flags](intermediate/cli-flags.md) - Ditch interactive mode
3. [Scripting](intermediate/scripting.md) - Automate workflows

**Use:** `container-create`, `container-start`, `container-stop`

**Goal:** CLI-efficient, scriptable workflows.

### Path 3: Advanced (Terminal-Native, DevOps)
**"I prefer Docker commands and terminal workflows"**

1. [Docker Direct](advanced/docker-direct.md) - Standard Docker commands
2. [Terminal Workflows](advanced/terminal-workflows.md) - vim/tmux development
3. [Batch Jobs](advanced/batch-jobs.md) - Non-interactive execution

**Use:** `docker run`, `docker exec`, direct container access

**Goal:** Cloud-native skills, production-ready patterns.

### Path 4: Understanding First (Engineers, Curious Learners)
**"I want to know how this works"**

1. [What are containers?](concepts/containers-and-images.md)
2. [Why are containers temporary?](concepts/ephemeral-containers.md)
3. [Where are my files?](concepts/workspaces-persistence.md)
4. [Cloud skills you're learning](concepts/ephemeral-containers.md#industry-parallels)

Then proceed to practical guides.

---

## Documentation Structure

```
docs/
├── getting-started/    Day 1, Day 2+ workflows (beginners)
├── guides/             Task-focused how-tos (all users)
├── intermediate/       Atomic commands, CLI flags, scripting (power users)
├── advanced/           Docker direct, terminal workflows, batch jobs (experts)
├── concepts/           Understanding DS01's design (optional reading)
├── reference/          Command quick reference
└── troubleshooting/    Fix problems
```

**Navigate by experience level:**
- **Beginner** → getting-started/ + guides/
- **Intermediate** → intermediate/ + guides/
- **Advanced** → advanced/
- **Curious** → concepts/

---

## Key Principles

**Commands without arguments = interactive mode**
```bash
# These all open friendly wizards
project init
container deploy
image create
```

**Use `--guided` while learning**
```bash
# Explains each step as it happens
project init --guided
container deploy --guided
```

**Containers are ephemeral, files are permanent**
- Safe to remove containers anytime
- Your workspace files always survive
- Recreate containers from images instantly

**Run `commands` to see everything available**
```bash
commands  # Full list of what you can do
```

---

## What's Next?

**First time here?** → [First-Time Setup](getting-started/first-time.md)

**Already set up?** → [Daily Workflow](getting-started/daily-workflow.md)

**Experienced user?** → [Command Reference](reference/command-quick-ref.md)
