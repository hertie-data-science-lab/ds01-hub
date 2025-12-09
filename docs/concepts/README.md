# Concepts

**Optional reading** - understand why DS01 works the way it does.

---

## Do I Need to Read This?

**No! You can use DS01 effectively without reading these docs.**

**Use the system first, come back here if curious:**
- Start with [Quickstart](../quickstart.md)
- Follow [Daily Workflow](../getting-started/daily-workflow.md)
- Read concepts when you wonder "why does it work this way?"

**These docs answer questions like:**
- Why are containers temporary but my files safe?
- What's the difference between an image and a container?
- Why do I need to rebuild images?
- How does this relate to AWS/GCP/Kubernetes?

---

## Core Concepts

### Containers and Images

→ [Containers and Images](containers-and-images.md) - What they are, how they relate

**Summary:** Images = recipes, containers = temporary instances created from recipes.

**Key insight:** Your code changes the recipe (Dockerfile), not the running instance.

### Ephemeral Containers

→ [Ephemeral Container Model](ephemeral-containers.md) - Why containers are temporary

**Summary:** Containers are like rented workstations - use them, return them, your files stay safe.

**Key insight:** This model is industry standard (AWS, GCP, Kubernetes all work this way).

**Career value:** By learning DS01's ephemeral model, you're learning cloud-native patterns used by every major tech company. This skill transfers directly to AWS, GCP, Azure, Kubernetes, and HPC systems.

### Workspaces and Persistence

→ [Workspaces and Persistence](workspaces-persistence.md) - Where your files live

**Summary:** `/workspace` is mounted from host - survives container removal.

**Key insight:** Only `/workspace` is permanent, everything else in container is temporary.

---

## Background Knowledge

### Linux Basics

→ [Linux Basics](../background/linux-basics.md) - Command line essentials

**For:** Users new to Linux terminals.

**Covers:** Files, directories, permissions, environment variables.

### Containers and Docker

→ [Containers Explained](../background/containers-and-docker.md) - Docker fundamentals

**For:** Users new to containers.

**Covers:** What Docker is, why we use it, basic concepts.

### Servers and HPC

→ [Remote Computing](../background/servers-and-hpc.md) - How HPC systems work

**For:** Understanding DS01 in context.

**Covers:** SSH, multi-user systems, resource sharing.

---

## DS01-Specific Concepts

### Resource Management

→ [Resource Limits](../background/resource-management.md) - Quotas and limits

**Covers:** Why limits exist, how they're enforced, checking your quotas.

### Ephemeral Philosophy

→ [Why Ephemeral?](../background/ephemeral-philosophy.md) - DS01's design philosophy

**Covers:** Benefits of stateless containers, industry alignment, best practices.

### Cloud Skills You're Learning

→ [Industry Parallels](../background/industry-parallels.md) - DS01 vs AWS/GCP/K8s

**For:** Seeing how DS01 teaches cloud-native skills.

**Covers:** Similarities to Docker, Kubernetes, cloud platforms.

---

## When to Read

### Before You Start (Optional)

**Want to understand first?**
1. [Containers and Images](containers-and-images.md)
2. [Ephemeral Containers](ephemeral-containers.md)
3. [Workspaces and Persistence](workspaces-persistence.md)

**Time:** 30 minutes total

### After First Week (Recommended)

**After using DS01, these make more sense:**
1. [Why Ephemeral?](../background/ephemeral-philosophy.md)
2. [Industry Parallels](../background/industry-parallels.md)

**Time:** 20 minutes

### When Troubleshooting

**When something confuses you:**
- Container disappeared? → [Ephemeral Containers](ephemeral-containers.md)
- Files disappeared? → [Workspaces and Persistence](workspaces-persistence.md)
- Why rebuild image? → [Containers and Images](containers-and-images.md)

---

## Learning Paths

### Path 1: Hands-On First (Recommended)

```
1. Quickstart → use system
2. Daily workflow → develop habits
3. Concepts → understand why (when curious)
```

**Best for:** Learning by doing, students

### Path 2: Theory First

```
1. Read concepts → understand model
2. Quickstart → apply knowledge
3. Daily workflow → build on understanding
```

**Best for:** Engineers, methodical learners

---

## Quick Answers

**"Why is my container gone?"**

→ Containers are ephemeral - designed to be removed. Your workspace files are safe.

**"Why do I need to rebuild images?"**

→ Images are blueprints. Changing the blueprint (Dockerfile) doesn't change existing containers.

**"Why can't I just pip install?"**

→ You can! But it's temporary. Add to Dockerfile for permanent changes.

**"Why does this feel like AWS?"**

→ Intentional! DS01 teaches cloud-native patterns used in industry.

**"Where are my files really?"**

→ `~/workspace/` on the host machine, mounted into containers.

---

## Related Documentation

**Practical guides:**
- [Getting Started](../getting-started/)
- [Guides](../guides/)
- [Reference](../reference/)

**Help:**
- [Troubleshooting](../troubleshooting/)
- [Command Reference](../reference/command-quick-ref.md)

---

**Remember: You don't need to read all of this to use DS01 effectively!**

**Start using the system, come back when curious.**
