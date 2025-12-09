# DS01 Documentation

GPU-enabled container infrastructure for data science and machine learning.

---

## Get Started in 5 Minutes

```bash
# First time only
user-setup                    # Interactive setup wizard

# Create and launch a project
project init                  # Create project (interactive)
project launch                # Start working (interactive)

# ... work ...

exit
container retire              # Done for the day (interactive)
```

**That's it.** Your files in `/workspace` are always saved.

New to containers? Add `--guided` to any command for step-by-step explanations.

> **Prefer containers?** Use `container-deploy` for more direct control.
> See [Quick Reference](quick-reference.md) for both approaches.

→ [First Container Guide](getting-started/first-container.md) for step-by-step
→ [Quick Reference](quick-reference.md) for all commands

---

## Documentation Structure

```
docs/
├── getting-started/   Start here
├── guides/            How to do things (practical)
├── background/        Why things work (theory, skippable)
├── reference/         Command documentation
├── troubleshooting/   Fix problems
└── advanced/          Power user topics
```

---

## Practical Guides

Step-by-step instructions for common tasks:

- [Daily Workflow](guides/daily-workflow.md) - Morning startup, work, evening cleanup
- [Custom Images](guides/custom-images.md) - Install your own packages
- [GPU Usage](guides/gpu-usage.md) - Request, monitor, release GPUs
- [Long-Running Jobs](guides/long-running-jobs.md) - Overnight training
- [Jupyter Setup](guides/jupyter-setup.md) - Jupyter Lab with SSH tunnels
- [VSCode Remote](guides/vscode-remote.md) - Remote development

[All guides →](guides/)

---

## Background Knowledge

*Optional but valuable* - understand why DS01 works this way:

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

---

## Essential Commands

```bash
# Project workflow (recommended)
user-setup                    # First-time setup
project init                  # Create new project
project launch                # Start working

# Container workflow (more control)
container-deploy              # Create + start container
container-retire              # Stop + remove + free GPU

# Images
image-create                  # Build custom image

# Status
container-list                # Your containers
dashboard                     # System overview
check-limits                  # Your quotas
```

For all options: `<command> --help` or `<command> --guided`

---

## Getting Help

1. Check [Troubleshooting](troubleshooting/)
2. Run `ds01-health-check`
3. Contact your system administrator

---

*New to servers and containers?* Start with [Prerequisites](getting-started/prerequisites.md)
*Experienced user?* Jump to [Quick Reference](quick-reference.md)
