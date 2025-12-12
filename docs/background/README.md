# Educational Computing Context

**Deeper knowledge for career development and technical understanding.**

> **Just want to use DS01?** Skip this section entirely.
> Go to [Quickstart](../quickstart.md) or [Key Concepts](../key-concepts/).

---

## What This Section Is

These docs provide **broader computing education** that goes beyond DS01. They explain the technology, industry practices, and transferable skills you're developing.

**Read these when:**
- You want to understand *why* things work the way they do
- You're preparing for industry roles (ML engineer, data scientist, DevOps)
- You want to connect DS01 to AWS, Kubernetes, and cloud platforms
- You're curious about the underlying technology

**Time investment:** 2-3 hours total (read based on interest)

---

## Contents

### Computing Fundamentals

These topics build foundational knowledge that transfers to any computing environment.

#### Servers & High-Performance Computing
- [Servers & HPC](servers-and-hpc.md) - 30 min

**What you'll learn:** What servers are, how shared computing works, HPC concepts, resource scheduling.

**Career relevance:** Cloud computing (AWS EC2, GCP), HPC clusters (SLURM, PBS), production ML infrastructure.

#### Linux Command Line
- [Linux Basics](linux-basics.md) - 45 min

**What you'll learn:** Essential commands, file system navigation, permissions, shell scripting basics.

**Career relevance:** Required for any server/cloud work. Linux runs 96% of cloud infrastructure.

### Container Technology

Understanding Docker deeply helps you work with any container platform.

#### Containers & Docker
- [Containers & Docker](containers-and-docker.md) - 40 min

**What you'll learn:** What containers are, how Docker works, images vs containers, layers, isolation.

**Career relevance:** Kubernetes, Docker Compose, CI/CD pipelines, microservices architecture.

#### Workspaces & Persistence
- [Workspaces & Persistence](workspaces-and-persistence.md) - 20 min

**What you'll learn:** Stateless vs stateful, volume mounts, persistent storage patterns.

**Career relevance:** Cloud storage (EBS, S3), Kubernetes PersistentVolumes, database architecture.

### DS01 Design Philosophy

Understand *why* DS01 works this way and how it prepares you for industry.

#### Ephemeral Container Philosophy
- [Ephemeral Philosophy](ephemeral-philosophy.md) - 20 min

**What you'll learn:** Why containers are temporary, benefits of stateless design, resource efficiency.

**Career relevance:** Cloud-native development, cost optimisation, infrastructure as code.

#### Resource Management
- [Resource Management](resource-management.md) - 15 min

**What you'll learn:** Fair sharing, quotas, cgroups, scheduling.

**Career relevance:** Kubernetes resource limits, cloud cost management, capacity planning.

### Industry Context

See how DS01 maps to production systems.

#### Industry Parallels
- [Industry Parallels](industry-parallels.md) - 45 min

**What you'll learn:** How DS01 compares to AWS, GCP, Kubernetes, HPC systems.

**Career relevance:** Direct preparation for cloud platforms and production ML.

---

## How These Differ from Concepts

| Background (This Section) | Concepts Section |
|--------------------------|------------------|
| General computing education | DS01-specific |
| "Why things work this way" | "What you need to know" |
| Transferable career skills | Practical usage |
| 2-3 hours total | 30-45 min total |
| Optional but valuable | Recommended |

**Just need to use DS01?** See [Key Concepts](../key-concepts/).

---

## Reading Paths

### Path A: Complete Beginner
**New to servers, Linux, and containers**

1. [Servers & HPC](servers-and-hpc.md) - Understand shared computing
2. [Linux Basics](linux-basics.md) - Essential commands
3. [Containers & Docker](containers-and-docker.md) - Container fundamentals
4. [Ephemeral Philosophy](ephemeral-philosophy.md) - DS01's design

**Time:** ~2.5 hours

### Path B: Know Linux, New to Containers
**Comfortable with command line, new to Docker**

1. [Containers & Docker](containers-and-docker.md) - Docker fundamentals
2. [Workspaces & Persistence](workspaces-and-persistence.md) - Storage patterns
3. [Ephemeral Philosophy](ephemeral-philosophy.md) - Ephemeral model

**Time:** ~1.5 hours

### Path C: Know Docker, Want Industry Context
**Understand containers, want career preparation**

1. [Servers & HPC](servers-and-hpc.md) - Shared computing context
2. [Resource Management](resource-management.md) - Quota systems
3. [Industry Parallels](industry-parallels.md) - AWS/GCP/K8s mapping

**Time:** ~1.5 hours

### Path D: Just Industry Context
**Want to understand how DS01 prepares you for work**

1. [Industry Parallels](industry-parallels.md) - Standalone overview

**Time:** 45 minutes

---

## Skills You're Developing

By using DS01 and reading these docs, you're learning:

### Technical Skills
- Linux command line proficiency
- Docker and containerisation
- GPU computing and resource management
- Infrastructure as code patterns

### Professional Skills
- Working in shared computing environments
- Resource efficiency and cost awareness
- Cloud-native workflows
- Production ML practices

### Career-Ready Knowledge
- AWS/GCP/Azure patterns (same concepts, different scale)
- Kubernetes fundamentals (pods, volumes, resource limits)
- HPC workflows (job scheduling, batch processing)
- DevOps practices (containers, CI/CD, infrastructure)

---

## Industry Testimonials (Illustrative)

> "Learning container workflows in grad school made my transition to AWS seamless."
> — Data Scientist

> "Understanding resource limits from shared computing helped me optimise our Kubernetes costs."
> — ML Engineer

> "The ephemeral container model is exactly how we work at scale."
> — Platform Engineer

---

## Next Steps

**Ready to use DS01?**
- [Quickstart](../quickstart.md) - Start immediately
- [Key Concepts](../key-concepts/) - Essential mental models

**Want practical guides?**
- [Daily Workflow](../core-guides/daily-workflow.md) - Common patterns
- [Custom Images](../core-guides/custom-images.md) - Build your environment

**Need reference?**
- [Command Reference](../reference/command-quick-ref.md) - All commands
- [Troubleshooting](../troubleshooting/) - Fix problems
