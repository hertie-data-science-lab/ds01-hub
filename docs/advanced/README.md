# Advanced Topics

For power users who want deeper control over their environment.

---

## Contents

- [Dockerfile Best Practices](dockerfile-best-practices.md) - Multi-stage builds, caching, optimization
- [Docker Direct](docker-direct.md) - When and how to use docker commands directly
- [SSH Advanced](ssh-advanced.md) - Key management, config files, tunnels

---

## Prerequisites

These guides assume familiarity with:
- Basic DS01 usage ([Getting Started](../getting-started/))
- Docker concepts ([Containers & Docker](../background/containers-and-docker.md))

---

## When to Use These

**Dockerfile Best Practices:**
- Your images are slow to build
- You want smaller images
- You need complex build logic

**Docker Direct:**
- DS01 commands don't cover your use case
- You need fine-grained container control
- You're debugging container issues

**SSH Advanced:**
- You manage multiple servers
- You want passwordless access
- You need SSH tunnels for Jupyter/TensorBoard
