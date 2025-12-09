# Choosing Your Learning Path

The DS01 documentation is modular - you don't need to read everything linearly. Choose the path that matches your background and goals.

---

## Quick Assessment

**Answer these questions to find your path:**

### 1. What's your background?

**A) I'm new to Linux and command line**
→ Start with [Fundamentals Path](#path-1-fundamentals-first)

**B) I know Linux but new to containers/Docker**
→ Start with [Container Concepts Path](#path-2-container-concepts)

**C) I know Docker but new to HPC/shared resources**
→ Start with [HPC & Resource Management Path](#path-3-hpc--resource-management)

**D) I'm experienced with everything, just need DS01 specifics**
→ Jump to [Task-Oriented Path](#path-4-task-oriented)

### 2. What's your goal?

**A) Get started ASAP**
→ [Quick Start Guide](quick-start.md)

**B) Understand the system deeply**
→ [Comprehensive Learning Path](#path-5-comprehensive-understanding)

**C) Solve a specific problem**
→ [Problem-Based Path](#path-6-problem-based)

**D) Prepare for industry/production work**
→ [Industry Practices Path](#path-7-industry-practices)

---

## Learning Paths

### Path 1: Fundamentals First
**For: Students new to Linux, command line, or servers**

**Goal:** Build foundational knowledge before diving into containers.

**Estimated time:** 4-6 hours of reading + practice

#### Week 1: Understanding the Environment
1. [What is a Server?](../background/servers-and-hpc.md) (20 min)
   - Shared computing resources
   - Multi-user environments
   - Why not just use your laptop?

2. [Linux Basics](../background/linux-basics.md) (45 min)
   - Directory structure
   - Essential commands
   - File permissions
   - Practice exercises

3. [Understanding HPC](../background/servers-and-hpc.md) (30 min)
   - High-performance computing concepts
   - Clusters and nodes
   - Job scheduling basics

**Practice:** Log in, navigate directories, create files, check permissions.

#### Week 2: Containers and Workflows
4. [Containers Explained](../background/containers-and-docker.md) (40 min)
   - What are containers?
   - Why use them?
   - Containers vs virtual machines

5. [Docker Images](../background/containers-and-docker.md) (30 min)
   - Images vs containers
   - Building images
   - Dockerfiles basics

6. [First-Time Setup](first-time-setup.md) (45 min + practice)
   - Complete onboarding
   - Deploy first container
   - Hands-on practice

**Practice:** Run `user-setup`, create a container, explore inside it.

#### Week 3: Working Effectively
7. [Workspaces & Persistence](../background/workspaces-and-persistence.md) (25 min)
   - What's saved vs temporary
   - File organization
   - Backup strategies

8. [Ephemeral Containers](../background/ephemeral-philosophy.md) (30 min)
   - DS01's philosophy
   - Daily workflows
   - Resource sharing

9. [Daily Usage Patterns](../guides/daily-workflow.md) (35 min)
   - Common workflows
   - Best practices
   - Time-saving tips

**Practice:** Use daily workflow for a week, build muscle memory.

#### Ongoing
- [Command Reference](../reference/command-reference.md) - As needed
- [Troubleshooting](../reference/troubleshooting.md) - When stuck

---

### Path 2: Container Concepts
**For: Linux users new to Docker/containers**

**Goal:** Understand containerization and DS01's container philosophy.

**Estimated time:** 2-3 hours

#### Start Here
1. [Containers Explained](../background/containers-and-docker.md) (40 min)
   - Container fundamentals
   - Docker basics
   - Isolation and security

2. [Docker Images](../background/containers-and-docker.md) (30 min)
   - Image layers
   - Building images
   - Best practices

3. [Ephemeral Containers](../background/ephemeral-philosophy.md) (30 min)
   - Why ephemeral?
   - Persistent vs temporary
   - Industry parallels (EC2, Kubernetes)

#### DS01 Specifics
4. [Workspaces & Persistence](../background/workspaces-and-persistence.md) (25 min)
   - File organization
   - What's mounted where

5. [Quick Start](quick-start.md) (20 min)
   - DS01 command overview
   - First container deployment

6. [Managing Containers](../guides/daily-workflow.md) (30 min)
   - Container lifecycle
   - Deploy/retire workflows
   - Monitoring

#### Deep Dive
7. [Building Custom Images](../guides/custom-images.md) (45 min)
   - 4-phase image creation
   - Adding packages
   - Optimization tips

8. [Dockerfile Guide](../advanced/dockerfile-guide.md) (60 min)
   - Advanced Dockerfile techniques
   - Multi-stage builds
   - Caching strategies

---

### Path 3: HPC & Resource Management
**For: Docker users new to shared HPC resources**

**Goal:** Understand fair sharing, resource limits, and GPU allocation.

**Estimated time:** 2 hours

#### Start Here
1. [Understanding HPC](../background/servers-and-hpc.md) (30 min)
   - Shared computing concepts
   - Fair scheduling
   - Priority systems

2. [Resource Management](../background/resource-management.md) (40 min)
   - Resource limits and quotas
   - Priority allocation
   - Systemd cgroups

3.  (35 min)
   - Why GPUs for ML?
   - MIG partitioning (A100)
   - GPU monitoring

#### DS01 Specifics
4. [Ephemeral Containers](../background/ephemeral-philosophy.md) (30 min)
   - Why stop containers when idle?
   - Resource sharing etiquette

5. [Working with GPUs](../guides/gpu-usage.md) (40 min)
   - GPU allocation
   - Monitoring usage
   - Troubleshooting

6. [Resource Limits Reference](../reference/resource-limits.md) (20 min)
   - Understanding your quotas
   - Timeout policies
   - Priority tiers

#### Best Practices
7.  (30 min)
   - Resource efficiency
   - Being a good citizen
   - Performance tips

---

### Path 4: Task-Oriented
**For: Experienced users who just need to get things done**

**Goal:** Quickly accomplish specific tasks.

#### Essential Reading (15 min)
1. [Quick Start](quick-start.md) (10 min)
2. [Ephemeral Containers](../background/ephemeral-philosophy.md) (5 min - skim)

#### Task Guides (As Needed)

**Starting a new project:**
→ [Creating Projects](../guides/creating-projects.md)

**Daily work:**
→ [Daily Usage Patterns](../guides/daily-workflow.md)

**Custom packages:**
→ [Building Custom Images](../guides/custom-images.md)

**GPU work:**
→ [Working with GPUs](../guides/gpu-usage.md)

**Collaboration:**
→ [Collaboration Guide](../guides/collaboration.md)

**Problems:**
→ [Troubleshooting](../reference/troubleshooting.md)

#### Keep Handy
- [Command Reference](../reference/command-reference.md) - Quick lookup
- [Resource Limits](../reference/resource-limits.md) - Know your quotas

---

### Path 5: Comprehensive Understanding
**For: Those who want deep understanding of the entire system**

**Goal:** Master DS01 architecture, design philosophy, and best practices.

**Estimated time:** 6-8 hours

#### Phase 1: Foundations (2 hours)
1. [Welcome to DS01](welcome.md)
2. [What is a Server?](../background/servers-and-hpc.md)
3. [Understanding HPC](../background/servers-and-hpc.md)
4. [Containers Explained](../background/containers-and-docker.md)
5. [Docker Images](../background/containers-and-docker.md)

#### Phase 2: DS01 Philosophy (1.5 hours)
6. [Ephemeral Containers](../background/ephemeral-philosophy.md)
7. [Resource Management](../background/resource-management.md)
8. [Project Structure](../guides/creating-projects.md)
9. [Industry Practices](../background/industry-parallels.md)

#### Phase 3: Practical Skills (2 hours)
10. [First-Time Setup](first-time-setup.md)
11. [Daily Usage Patterns](../guides/daily-workflow.md)
12. [Managing Containers](../guides/daily-workflow.md)
13. [Building Custom Images](../guides/custom-images.md)
14. [Working with GPUs](../guides/gpu-usage.md)

#### Phase 4: Advanced Topics (2 hours)
15. [Dockerfile Guide](../advanced/dockerfile-guide.md)
16. [SSH Setup](../advanced/ssh-setup.md)
17. [VSCode Remote](../advanced/vscode-remote.md)
18. 

#### Phase 5: Reference (As needed)
19. [Command Reference](../reference/command-reference.md)
20. [Troubleshooting](../reference/troubleshooting.md)
21. [Resource Limits](../reference/resource-limits.md)

---

### Path 6: Problem-Based
**For: Learning by solving specific problems**

**Goal:** Hands-on learning through practical challenges.

#### Challenge 1: First Container (30 min)
**Problem:** Get a PyTorch container running with GPU access.

**Resources:**
- [Quick Start](quick-start.md)
- [First-Time Setup](first-time-setup.md)

**Validation:**
```bash
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

#### Challenge 2: Custom Environment (60 min)
**Problem:** Build a container with specific packages:
- PyTorch 2.8.0
- transformers
- datasets
- Your favorite tools

**Resources:**
- [Building Custom Images](../guides/custom-images.md)
- [Dockerfile Guide](../advanced/dockerfile-guide.md)

**Validation:**
```bash
python -c "import transformers; print(transformers.__version__)"
```

#### Challenge 3: Persistent Workflow (45 min)
**Problem:** Train a model, retire container, restart, and continue training.

**Resources:**
- [Workspaces & Persistence](../background/workspaces-and-persistence.md)
- [Daily Usage Patterns](../guides/daily-workflow.md)

**Validation:** Training checkpoint loads correctly after container recreation.

#### Challenge 4: GPU Optimization (60 min)
**Problem:** Monitor GPU usage and understand MIG allocation.

**Resources:**
- 
- [Working with GPUs](../guides/gpu-usage.md)

**Validation:** Can explain your GPU allocation and monitor usage.

#### Challenge 5: Remote Development (90 min)
**Problem:** Set up VSCode to develop locally with remote compute.

**Resources:**
- [VSCode Remote](../advanced/vscode-remote.md)
- [SSH Setup](../advanced/ssh-setup.md)

**Validation:** Edit code locally, run on DS01 GPU.

#### Challenge 6: Collaboration (45 min)
**Problem:** Share a reproducible project with a colleague.

**Resources:**
- [Collaboration Guide](../guides/collaboration.md)
- [Project Structure](../guides/creating-projects.md)

**Validation:** Colleague can clone repo and recreate environment.

---

### Path 7: Industry Practices
**For: Preparing for production ML/data science roles**

**Goal:** Understand how DS01 mirrors industry workflows.

**Estimated time:** 3 hours

#### Cloud-Native Computing
1. [Industry Practices](../background/industry-parallels.md) (45 min)
   - How AWS/GCP use containers
   - Kubernetes parallels
   - MLOps workflows

2. [Ephemeral Containers](../background/ephemeral-philosophy.md) (30 min)
   - Stateless compute
   - Persistent storage separation
   - Spot instances analogy

3. [Resource Management](../background/resource-management.md) (40 min)
   - Cost optimization
   - Resource quotas
   - Priority scheduling

#### Production Best Practices
4. [Project Structure](../guides/creating-projects.md) (30 min)
   - Organizing production projects
   - Reproducibility
   - Version control

5.  (45 min)
   - Security considerations
   - Performance optimization
   - Cost-efficient workflows

#### Advanced Skills
6. [Dockerfile Guide](../advanced/dockerfile-guide.md) (60 min)
   - Production-ready images
   - Multi-stage builds
   - Security scanning

7. [Collaboration](../guides/collaboration.md) (30 min)
   - Team workflows
   - Shared resources
   - Documentation

---

## Mixing Paths

**You don't have to stick to one path!** Mix and match based on your needs:

### Example: Data Science Student
**Week 1:** Fundamentals Path (Linux basics, containers)
**Week 2:** Task-Oriented Path (get projects working)
**Week 3:** Problem-Based Path (challenges for practice)
**Ongoing:** Reference as needed

### Example: CS Student with Docker Experience
**Day 1:** Container Concepts Path (understand DS01's approach)
**Day 2:** Task-Oriented Path (start working)
**Week 1:** Industry Practices Path (understand context)
**Ongoing:** Advanced topics as needed

### Example: Research Scientist
**Day 1:** Quick Start → jump in
**As needed:** Task guides for specific problems
**Eventually:** Comprehensive Understanding for mastery

---

## Progress Tracking

### Beginner → Intermediate
You're intermediate when you can:
- [ ] Deploy and retire containers independently
- [ ] Understand persistent vs ephemeral storage
- [ ] Build custom images with your packages
- [ ] Monitor GPU usage
- [ ] Troubleshoot common issues

### Intermediate → Advanced
You're advanced when you can:
- [ ] Write efficient Dockerfiles with multi-stage builds
- [ ] Optimize resource usage
- [ ] Set up remote development workflows
- [ ] Help others troubleshoot
- [ ] Understand resource allocation algorithms

### Advanced → Expert
You're an expert when you can:
- [ ] Contribute to system documentation
- [ ] Design project structures for teams
- [ ] Implement production-ready workflows
- [ ] Understand system architecture deeply
- [ ] Mentor others effectively

---

## Recommended Next Steps

Based on your starting point:

### After Quick Start
→ Read [Ephemeral Containers](../background/ephemeral-philosophy.md) to understand philosophy
→ Explore [Daily Usage Patterns](../guides/daily-workflow.md) for efficiency

### After First-Time Setup
→ Practice daily workflow for a week
→ Read [Workspaces & Persistence](../background/workspaces-and-persistence.md)
→ Try [Building Custom Images](../guides/custom-images.md)

### After Fundamentals
→ Dive into [Background](../background/) section
→ Practice with [Guides](../guides/)
→ Explore [Advanced](../advanced/) topics

---

## Getting Help Along the Way

### Built-in Help
```bash
# Command help
<command> --help

# Educational mode
<command> --guided
```

### Documentation
- **Stuck?** → [Troubleshooting](../reference/troubleshooting.md)
- **Need syntax?** → [Command Reference](../reference/command-reference.md)
- **Understanding concepts?** → [Background](../background/) section

### Community
- Ask your system administrator
- Help fellow users (teaching reinforces learning)
- Contribute documentation improvements

---

## Create Your Own Path

**The best path is the one that works for you.** Use this as a guide, not a prescription.

**Suggested approach:**
1. Skim this guide
2. Pick a starting point based on your background
3. Read 2-3 docs
4. Get hands-on with actual work
5. Return to docs when you need clarification
6. Gradually fill knowledge gaps

**Learning by doing is often more effective than reading everything first.**

---

## Quick Decision Tree

```
┌─ Are you NEW to Linux/servers?
│  └─ YES → Fundamentals Path
│  └─ NO → Continue
│
├─ Are you NEW to Docker/containers?
│  └─ YES → Container Concepts Path
│  └─ NO → Continue
│
├─ Are you NEW to shared resources/HPC?
│  └─ YES → HPC & Resource Management Path
│  └─ NO → Continue
│
├─ Do you want DEEP understanding?
│  └─ YES → Comprehensive Understanding Path
│  └─ NO → Continue
│
├─ Do you learn best by DOING?
│  └─ YES → Problem-Based Path
│  └─ NO → Continue
│
├─ Do you want INDUSTRY context?
│  └─ YES → Industry Practices Path
│  └─ NO → Continue
│
└─ Just want to GET THINGS DONE?
   └─ Task-Oriented Path
```

---

**Ready to start?** Pick your path and dive in!

**Still unsure?** Start with [Quick Start](quick-start.md) and see what questions arise.
