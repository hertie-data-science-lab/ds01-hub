# Glossary

Key terms used in DS01 documentation.

---

## Container Terms

**Container**
A lightweight, isolated environment that runs your code with its own libraries and filesystem. Containers are temporary - they can be created and destroyed easily.

**Image**
A read-only template (blueprint) used to create containers. Contains the OS, packages, and configuration. Images are permanent and stored on disk.

**Dockerfile**
A text file with instructions for building a Docker image. Located at `~/dockerfiles/<project>.Dockerfile`.

**Docker**
The platform that runs containers. DS01 uses Docker with additional management layers.

---

## DS01 Terms

**Deploy**
Create and start a container with GPU allocation. Command: `container-deploy`

**Retire**
Stop and remove a container, freeing the GPU. Command: `container-retire`

**Workspace**
Your persistent storage directory (`~/workspace/<project>/`). Files here survive container removal.

**Tier/Layer**
DS01 commands are organised in layers:
- **L2 (Atomic):** Single-purpose commands (`container-create`, `image-list`)
- **L3 (Orchestrators):** Multi-step workflows (`container-deploy`, `container-retire`)
- **L4 (Wizards):** Complete guided experiences (`user-setup`, `project-init`)

---

## GPU Terms

**GPU (Graphics Processing Unit)**
Specialised processor for parallel computing, essential for ML training. DS01 uses NVIDIA data center GPUs.

**CUDA**
NVIDIA's parallel computing platform. Required for GPU-accelerated ML frameworks.

**MIG (Multi-Instance GPU)**
Technology that partitions a single GPU into multiple isolated instances. Allows GPU sharing among users.

**nvidia-smi**
Command-line tool for monitoring GPU usage. Run inside containers.

---

## Resource Terms

**Allocation**
Resources assigned to you (GPUs, containers, memory). Checked via `check-limits`.

**Quota**
Maximum resources you can use. Configured per-user or per-group.

**Idle Timeout**
Time after which an idle container is automatically stopped. Typically 30min-2h (varies by user). Run `check-limits` to see your current value.

**Max Runtime**
Maximum time a container can run. Typically 24h-72h (varies by user). Run `check-limits` to see your current value.

---

## HPC Terms

**HPC (High-Performance Computing)**
Using powerful shared computing resources. DS01 is an HPC system for data science.

**Fair Share**
Resource scheduling principle that distributes resources fairly among users.

**Cgroups**
Linux feature that limits and isolates resource usage. DS01 uses cgroups to enforce limits.

---

## File Terms

**Host**
The main DS01 server, outside containers.

**Mount**
Connecting a host directory to appear inside a container. Your workspace is mounted at `/workspace`.

**Persistent**
Data that survives container removal. Your workspace is persistent.

**Ephemeral**
Data that's lost when container is removed. Container filesystem (except workspace) is ephemeral.

---

## Network Terms

**SSH (Secure Shell)**
Protocol for secure remote access. How you connect to DS01.

**SSH Tunnel**
Forwarding a port through SSH. Used for accessing Jupyter from your laptop.

---

## Quick Reference

| Term | Meaning |
|------|---------|
| Container | Running instance (temporary) |
| Image | Blueprint (permanent) |
| Workspace | Your files (permanent) |
| Deploy | Create + start |
| Retire | Stop + remove |
| GPU | Graphics processor for ML |
| MIG | GPU partitioning |
| Quota | Your resource limits |

---

## See Also

- [Containers & Docker](../background/containers-and-docker.md)
- [Servers & HPC](../background/servers-and-hpc.md)
- [Resource Management](../background/resource-management.md)
