# Background Knowledge

> **Just want to deploy containers?** You can skip this entire section.
> Go to [First Container](../getting-started/first-container.md) instead.

---

## Why Learn This?

DS01 uses the same technologies as AWS, Google Cloud, and Kubernetes. Understanding these concepts gives you:

1. **Transferable skills** - Same patterns used at tech companies
2. **Better debugging** - Understand errors instead of just googling them
3. **Career preparation** - Container skills are highly valued in industry
4. **Efficiency** - Work faster when you understand the system

**Time investment:** 2-3 hours to read everything
**Payoff:** Skills that transfer to any cloud platform

---

## Contents

### Computing Fundamentals
- [Servers & HPC](servers-and-hpc.md) - What is a server? Shared computing environments (30 min)
- [Linux Basics](linux-basics.md) - Essential command line skills (45 min)
- [GPU Computing](gpu-computing.md) - MIG, CUDA, nvidia-smi explained (25 min)

### Container Technology
- [Containers & Docker](containers-and-docker.md) - Why containers exist, Docker fundamentals (40 min)
- [Workspaces & Persistence](workspaces-and-persistence.md) - What's saved vs temporary (20 min)

### DS01 Design
- [Ephemeral Philosophy](ephemeral-philosophy.md) - Why containers are temporary (20 min)
- [Resource Management](resource-management.md) - Fair sharing and limits (15 min)

### Industry Context
- [Industry Parallels](industry-parallels.md) - How DS01 maps to AWS/GCP/Kubernetes (45 min)

---

## Reading Suggestions

**Complete beginner (new to servers):**
Servers & HPC → Linux Basics → Containers & Docker → Ephemeral Philosophy

**Know Linux, new to Docker:**
Containers & Docker → Workspaces & Persistence → Ephemeral Philosophy

**Know Docker, new to HPC/shared resources:**
Servers & HPC → Resource Management → GPU Computing

**Want industry context only:**
Industry Parallels (standalone, references other topics as needed)

---

## Put This Into Practice

After reading, try these guides:
- [Daily Workflow](../guides/daily-workflow.md) - Apply container lifecycle knowledge
- [Custom Images](../guides/custom-images.md) - Apply Docker image knowledge
- [GPU Usage](../guides/gpu-usage.md) - Apply GPU computing knowledge
