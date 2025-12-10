# DS01 User Documentation - Index & Learning Paths

## Documentation Structure

```
docs/
├── getting-started/    Start here 
├── guides/             Task-focused how-tos (practical)
├── intermediate/       Atomic commands, CLI flags, scripting 
├── advanced/           Docker direct, terminal workflows, batch jobs
├── concepts/           Understanding DS01's design (theory, skippable)
├── reference/          Command quick reference
└── troubleshooting/    Fix problems
```

## Suggested Learning Paths

### Path 1: Beginner (Students, First-Time Users)
**"I just want to work on my thesis"**

1. [First-Time Setup](getting-started/first-time.md) - 15 minutes
2. [Daily Workflow](getting-started/daily-workflow.md) - Core routine
3. [Jupyter Setup](guides/jupyter-notebooks.md) - If using notebooks
4. [VS Code Remote](guides/vscode-remote.md) - If using VS Code

**Use:** 
- Project-oriented: `project launch`, `exit`
- Container-oriented: `image create`,`container deploy`, `container retire`

**Skip the background reading** - learn as you go with `--guided` mode.

### Path 2: Intermediate (IDE-based)
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

## Practical Guides

Step-by-step instructions for common tasks:

- [Daily Workflow](guides/daily-workflow.md) - This is the core workflow
- [Custom Images](guides/custom-images.md) - Install your own packages
- [GPU Usage](guides/gpu-usage.md) - Request, monitor, release GPUs
- [Long-Running Jobs](guides/long-running-jobs.md) - Overnight training
- [Jupyter Setup](guides/jupyter-setup.md) - Jupyter Lab with SSH tunnels
- [VSCode Remote](guides/vscode-remote.md) - Remote development

[All guides →](guides/)

---

## Background Knowledge

*Optional but useful to familiarise yourself with cloud-computing concepts*:

- [Servers & HPC](background/servers-and-hpc.md) - Shared computing environments
- [Containers & Docker](background/containers-and-docker.md) - Why containers exist
- [Ephemeral Philosophy](background/ephemeral-philosophy.md) - Why containers are temporary
- [Industry Parallels](background/industry-parallels.md) - How this maps to AWS/GCP/Kubernetes

> **Just want to deploy?** Skip background and go to [First Container](getting-started/first-container.md)

[All background →](background/)

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
| Understand containers | [Containers & Docker](background/containers-and-docker.md) |
| Build a custom image | [Custom Images](guides/custom-images.md) |
| Run Jupyter | [Jupyter Setup](guides/jupyter-setup.md) |
| Fix an error | [Troubleshooting](troubleshooting/) |
| Learn industry practices | [Industry Parallels](background/industry-parallels.md) |