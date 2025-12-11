# Advanced Guide

**For terminal-native users who want Docker-level control.**

---

## You're Ready If

- You're comfortable with Docker (`docker run`, `docker exec`)
- You prefer CLI over IDE/GUI
- You want to build batch job pipelines
- You need custom container configuration

**Not there yet?** → [Intermediate](../intermediate/)

---

## What's Here

### Core Guides

| Guide | What You'll Learn |
|-------|-------------------|
| [Docker Direct](docker-direct.md) | Using Docker commands directly |
| [Terminal Workflows](terminal-workflows.md) | CLI-native development patterns |
| [Batch Jobs](batch-jobs.md) | Non-interactive job submission |

### Optimisation

| Guide | What You'll Learn |
|-------|-------------------|
| [Efficiency Tips](efficiency-tips.md) | Keyboard shortcuts, workflow patterns |
| [Dockerfile Best Practices](dockerfile-best-practices.md) | Build optimisation, layer caching |
| [SSH Advanced](ssh-advanced.md) | Config files, port forwarding |

### Specialized

| Guide | What You'll Learn |
|-------|-------------------|
| [Multi-MIG Training](multi-mig-training.md) | Distributed GPU training |
| [VS Code Remote](vscode-remote.md) | Advanced VS Code setup |

---

## The Key Difference

**Intermediate (DS01 commands):**
```bash
container-deploy my-project
container-attach my-project
```

**Advanced (Docker direct):**
```bash
docker exec -it my-project._.$(id -u) bash
docker logs my-project._.$(id -u)
```

**Note:** Direct Docker commands are still subject to DS01 resource enforcement (cgroups, GPU limits).

---

## Suggested Path

**Terminal workflows:**
1. [Docker Direct](docker-direct.md) → [Terminal Workflows](terminal-workflows.md) → [Batch Jobs](batch-jobs.md)

**Optimisation:**
1. [Efficiency Tips](efficiency-tips.md) → [Dockerfile Best Practices](dockerfile-best-practices.md)

**Remote access:**
1. [SSH Advanced](ssh-advanced.md) → [VS Code Remote](vscode-remote.md)

**Specialized:**
1. [Multi-MIG Training](multi-mig-training.md)
