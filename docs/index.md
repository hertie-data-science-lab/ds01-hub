# Index for DS01 - Hertie School Data Science Lab's GPU Container Platform

## Documentation Structure

```
docs/
├── getting-started/    Day 1, Day 2+ workflows (beginners)
├── guides/             Task-focused how-tos (all users)
├── intermediate/       Atomic commands, CLI flags, scripting 
├── advanced/           Docker direct, terminal workflows, batch jobs
├── concepts/           Understanding DS01's design (optional)
├── reference/          Command quick reference
└── troubleshooting/    Fix problems
```

---

## Learning Paths

### Path 1: Beginner (Students, First-Time Users)
**"I just want to work on my thesis"**

1. [First-Time Setup](getting-started/first-time.md) - 15 minutes
2. [Daily Workflow](getting-started/daily-workflow.md) - Your routine
3. [Jupyter Setup](guides/jupyter-notebooks.md) - If using notebooks
4. [VS Code Remote](guides/vscode-remote.md) - If using VS Code

**Use:** 
- Project-oriented: `project launch`, `exit`
- Container-oriented: `image create`,`container deploy`, `container retire`

**Skip the background reading** - learn as you go with `--guided` mode.

### Path 2: Intermediate (IDE)
**"I want more control and efficiency"**

1. [Atomic Commands](intermediate/atomic-commands.md) - Granular control
2. [CLI Flags](intermediate/cli-flags.md) - Faster than interactive mode
3. [Scripting](intermediate/scripting.md) - Automate workflows

**Use:** `container-create`, `container-start`, `container-stop`, `container-remove`

### Path 3: Advanced (Terminal & DevOps Native)
**"I prefer Docker commands and terminal workflows"**

1. [Docker Direct](advanced/docker-direct.md) - Standard Docker commands
2. [Terminal Workflows](advanced/terminal-workflows.md) - vim/tmux development
3. [Batch Jobs](advanced/batch-jobs.md) - Non-interactive execution

**Use:** `docker run`, `docker exec`, direct container access

### Bonus Path(!): Understanding First
**"I want to know how this works"**

1. [What are containers?](concepts/containers-and-images.md)
2. [Why are containers temporary?](concepts/ephemeral-containers.md)
3. [Where are my files?](concepts/workspaces-persistence.md)
4. [Cloud skills you're learning](concepts/ephemeral-containers.md#industry-parallels)

Then proceed to practical guides.