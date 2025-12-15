# DS01 User Documentation

## Documentation Structure

```
docs/
├── getting-started/          Start here
├── core-guides/              Task-focused how-tos
├── intermediate/             Atomic commands, CLI flags, scripting
├── advanced/                 Docker direct, terminal workflows, batch jobs
├── key-concepts/             Key Concepts to Understand (DS01-specific)
├── background/               Educational Computing Context (career skills)
├── reference/                Command quick reference
└── troubleshooting/          Fix problems
```

### Separation of Concerns

>-  **Practical:** [Getting Started](getting-started/) → [Core Guides](core-guides/) → [Intermediate](intermediate/) → [Advanced](advanced/)
>- **Conceptual:** [Key Concepts](key-concepts/) (DS01-specific) | [Background](background/) (industry parallels)
>- **Reference:** [Commands Ref](reference/) | [Troubleshooting](troubleshooting/)

---

## Suggested Learning Paths

### Path 1: Beginner (Students, First-Time Users)
**"I just want to work on my thesis"**

> **⏱ In a hurry?** Try the [Quickstart](quickstart.md) for a condensed intro (~30 min).

**Essential (do these first):**
1. [Prerequisites](getting-started/prerequisites.md) - Check what you need
2. [First-Time Setup](getting-started/first-time-setup.md) - SSH keys, accounts (~15 min)
3. [Containers & Images](key-concepts/containers-and-images.md) - Mental model (~5 min)
4. [Workspaces & Persistence](key-concepts/workspaces-persistence.md) - Where files live (~5 min)
5. [First Container](getting-started/first-container.md) - Get hands-on experience
6. [Daily Workflow](core-guides/daily-workflow.md) - Your regular routine
7. [Help System](getting-started/help-system.md) - How to get unstuck

**IDE Setup (optional, choose one):**
- [Jupyter Setup](core-guides/jupyter.md) - For notebook users
- [VS Code Remote](core-guides/vscode-remote.md) - For code editors
- [Launching Containers](core-guides/launching-containers.md) - Terminal-only workflows

**Commands:** `user setup`, `project init`, `project launch`, `container deploy`, `container retire`

**Pro tip:** Use `--guided` and `--concepts` flags while learning, they explain each step.

### Path 2: Intermediate (Want More Control)
**"I want more control and efficiency"** - you're comfortable with containers and want to automate repetitive tasks or understand system internals.

**Core Understanding:**
1. [Command Hierarchy](intermediate/command-hierarchy.md) - How commands are organised
2. [Container States](intermediate/container-states.md) - created, running, stopped, removed
3. [Atomic Commands](intermediate/atomic-commands.md) - Single-purpose fine-grained control

**Practical Skills:**
1. [CLI Flags & Options](intermediate/cli-flags.md) - Faster than interactive mode
2. [Shell Aliases](intermediate/shell-aliases.md) - Custom command shortcuts
3. [Bash Scripting](intermediate/scripting-bash.md) - Automate container workflows
4. [Python Scripting](intermediate/scripting-python.md) - Programmatic container management

**Commands:** `container-create`, `container-start`, `container-stop`, `container-remove`, `image-update`, `image-delete`

### Path 3: Advanced (Terminal & DevOps Native)
**"I prefer Docker commands and terminal workflows"** - you're comfortable with Linux/Docker, want maximum flexibility, or have specialized workload needs.

**Docker & Container Mastery:**
1. [Docker Direct](advanced/docker-direct.md) - Using native Docker commands
2. [Complete Dockerfile Guide](advanced/dockerfile-complete-guide.md) - Advanced layering, optimization
3. [Container States Deep Dive](intermediate/container-states.md) - Full lifecycle understanding

**Terminal & Development:**
1. [Terminal Workflows](advanced/terminal-workflows.md) - vim/tmux development patterns
2. [Advanced SSH](advanced/ssh-advanced.md) - SSH tunneling, X11 forwarding, port mapping
3. [Shell Aliases & Custom Commands](intermediate/shell-aliases.md) - Personalize your workflow

**Specialized Workloads:**
1. [Batch Jobs & Non-Interactive Execution](advanced/batch-jobs.md) - Training scripts, cron jobs
2. [Multi-MIG GPU Training](advanced/multi-mig-training.md) - Parallel training on MIG instances
3. [Efficiency Tips](advanced/efficiency-tips.md) - Performance optimization, resource tricks

---

## Conceptual Documentation

DS01 has two types of conceptual documentation with different purposes:
1. **Key Concepts** - these are practical DS01-specific guides 
2. **Background Knowledge** - these are more theoretically-oriented  primers on basic CS principles & industry parallels informaing DS01's design

| Key Concepts | Background Knowledge |
|---|---|
| **~20 min total** | **~1+ hour total** |
| [Containers and Images](key-concepts/containers-and-images.md) — Why do packages disappear? Why rebuild images? | [Containers & Docker](background/containers-and-docker.md) — Kubernetes, CI/CD, microservices |
| [Ephemeral Containers](key-concepts/ephemeral-containers.md) — Why are containers temporary? Will I lose work? | [Servers & HPC](background/servers-and-hpc.md) — AWS, GCP, cloud computing |
| [Workspaces and Persistence](key-concepts/workspaces-persistence.md) — Where are my files? What persists? | [Linux Basics](background/linux-basics.md) — Any server/cloud work |
| [Python Environments](key-concepts/python-environments.md) — Do I need venv/conda? | [Industry Parallels](background/industry-parallels.md) — Direct cloud platform preparation |


See full overviews: [Key Concepts](key-concepts/) | [Background](background/)

---

## Practical Guides

Step-by-step instructions for common tasks:

- [Daily Workflow](core-guides/daily-workflow.md) - Core routine
- [Custom Images](core-guides/custom-images.md) - Install your own packages
- [GPU Usage](core-guides/gpu-usage.md) - Request, monitor, release GPUs
- [Long-Running Jobs](core-guides/long-running-jobs.md) - Overnight training
- [Jupyter Setup](core-guides/jupyter.md) - Jupyter Lab with SSH tunnels
- [VSCode Remote](core-guides/vscode-remote.md) - Remote development

[All guides →](core-guides/)

---

## Reference

Quick lookups:

- **Commands:** [Container](reference/commands/container-commands.md) | [Image](reference/commands/image-commands.md) | [Project](reference/commands/project-commands.md) | [System](reference/commands/system-commands.md)
- [File Locations](reference/file-locations.md) - Where things are stored
- [Glossary](reference/glossary.md) - Key terms defined

[All reference →](reference/)

---

## Troubleshooting

Find your problem:

- [Container Issues](troubleshooting/container-issues.md) - Won't start, stopped unexpectedly
- [GPU Issues](troubleshooting/gpu-issues.md) - Not available, CUDA out of memory
- [Image Issues](troubleshooting/image-issues.md) - Build fails, package not found
- [Common Errors](troubleshooting/common-errors.md) - Files, permissions, network

[All troubleshooting →](troubleshooting/)

---

## Quick Links

| I want to... | Go to... |
|--------------|----------|
| Start my first container | [First Container](getting-started/first-container.md) |
| See all commands | [Quick Reference](quick-reference.md) |
| Understand why packages disappear | [Containers and Images](key-concepts/containers-and-images.md) |
| Understand why containers are temporary | [Ephemeral Containers](key-concepts/ephemeral-containers.md) |
| Build a custom image | [Custom Images](core-guides/custom-images.md) |
| Run Jupyter | [Jupyter Setup](core-guides/jupyter.md) |
| Fix an error | [Troubleshooting](troubleshooting/) |
| Learn industry practices | [Industry Parallels](background/industry-parallels.md) |
| Learn Linux commands | [Linux Basics](background/linux-basics.md) |
