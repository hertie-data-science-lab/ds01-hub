# DS01 User Documentation

## Documentation Structure

```
docs/
├── getting-started/    Start here
├── guides/             Task-focused how-tos
├── intermediate/       Atomic commands, CLI flags, scripting
├── advanced/           Docker direct, terminal workflows, batch jobs
├── concepts/           Key Concepts to Understand (DS01-specific)
├── background/         Educational Computing Context (career skills)
├── reference/          Command quick reference
└── troubleshooting/    Fix problems
```

### Separation of Concerns

>-  **Practical:** [Getting Started](getting-started/) → [Guides](guides/) → [Intermediate](intermediate/) → [Advanced](advanced/)
>- **Conceptual:** [Key Concepts](concepts/) (DS01-specific) | [Background](background/) (career skills)
>- **Reference:** [Commands Ref](reference/) | [Troubleshooting](troubleshooting/)

---

## Learning Paths

### Path 1: Beginner (Students, First-Time Users)
**"I just want to work on my thesis"**

1. [First-Time Setup](getting-started/first-time.md) - 15 minutes
2. [Daily Workflow](getting-started/daily-workflow.md) - Core routine
3. [Jupyter Setup](guides/jupyter.md) - If using notebooks
4. [VS Code Remote](guides/vscode-remote.md) - If using VS Code

**Commands:** `project launch`, `exit`, `container deploy`, `container retire`

**Skip the background reading** - learn as you go with `--guided` mode.

### Path 2: Intermediate (Want More Control)
**"I want more control and efficiency"**

1. [Atomic Commands](intermediate/atomic-commands.md) - Granular control
2. [CLI Flags](intermediate/cli-flags.md) - Faster than interactive mode
3. [Scripting](intermediate/scripting.md) - Automate workflows

**Commands:** `container-create`, `container-start`, `container-stop`, `container-remove`

### Path 3: Advanced (Terminal & DevOps Native)
**"I prefer Docker commands and terminal workflows"**

1. [Docker Direct](advanced/docker-direct.md) - Standard Docker commands
2. [Terminal Workflows](advanced/terminal-workflows.md) - vim/tmux development
3. [Batch Jobs](advanced/batch-jobs.md) - Non-interactive execution

**Commands:** `docker run`, `docker exec`, direct container access

---

## Conceptual Documentation

DS01 has two types of conceptual documentation with different purposes:

### Key Concepts to Understand
**DS01-specific mental models for effective usage** — [Overview](concepts/) (30-45 min total)

| Topic | What It Answers |
|-------|----------------|
| [Containers and Images](concepts/containers-and-images.md) | Why do packages disappear? Why rebuild images? |
| [Ephemeral Containers](concepts/ephemeral-containers.md) | Why are containers temporary? Will I lose work? |
| [Workspaces and Persistence](concepts/workspaces-persistence.md) | Where are my files? What persists? |
| [Python Environments](concepts/python-environments.md) | Do I need venv/conda? |

**Read these:** When something confuses you, or before first use.

### Educational Computing Context
**Deeper knowledge for career development** — [Overview](background/) (2-3 hours total)

| Topic | Career Relevance |
|-------|-----------------|
| [Servers & HPC](background/servers-and-hpc.md) | AWS, GCP, cloud computing |
| [Linux Basics](background/linux-basics.md) | Any server/cloud work |
| [Containers & Docker](background/containers-and-docker.md) | Kubernetes, CI/CD, microservices |
| [Industry Parallels](background/industry-parallels.md) | Direct cloud platform preparation |

**Read these:** When you want to understand the technology deeply, or prepare for industry.

---

## Practical Guides

Step-by-step instructions for common tasks:

- [Daily Workflow](guides/daily-workflow.md) - Core routine
- [Custom Images](guides/custom-images.md) - Install your own packages
- [GPU Usage](guides/gpu-usage.md) - Request, monitor, release GPUs
- [Long-Running Jobs](guides/long-running-jobs.md) - Overnight training
- [Jupyter Setup](guides/jupyter.md) - Jupyter Lab with SSH tunnels
- [VSCode Remote](guides/vscode-remote.md) - Remote development

[All guides →](guides/)

---

## Reference

Quick lookups:

- **Commands:** [Container](reference/commands/container-commands.md) | [Image](reference/commands/image-commands.md) | [Project](reference/commands/project-commands.md) | [System](reference/commands/system-commands.md)
- [Resource Limits](reference/resource-limits.md) - Your quotas
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
| Understand why packages disappear | [Containers and Images](concepts/containers-and-images.md) |
| Understand why containers are temporary | [Ephemeral Containers](concepts/ephemeral-containers.md) |
| Build a custom image | [Custom Images](guides/custom-images.md) |
| Run Jupyter | [Jupyter Setup](guides/jupyter.md) |
| Fix an error | [Troubleshooting](troubleshooting/) |
| Learn industry practices | [Industry Parallels](background/industry-parallels.md) |
| Learn Linux commands | [Linux Basics](background/linux-basics.md) |
