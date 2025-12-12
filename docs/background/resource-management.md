# Resource Management

**Understanding quotas, fair sharing, and resource allocation in shared computing.**

> **Part of [Educational Computing Context](README.md)** - Career-relevant knowledge beyond DS01 basics.

Resource management is a core concept in cloud computing, HPC, and multi-tenant systems. This guide explains DS01's resource allocation and how these patterns apply to production systems.

## Your Resource Limits

```bash
check-limits
```

This command shows your current limits and resource usage. Typical limits:
- Max GPUs: 1-2
- Max Containers: 2-3
- Memory: 32-128GB per container
- Idle Timeout: 30min-2h (varies by user)
- Max Runtime: 24h-72h (varies by user)

## How Limits Work

**Per-user limits prevent:**

- **One user monopolising all GPUs:** Without limits, the first person to run `container-deploy --gpu=8` would grab all available GPUs. Everyone else waits indefinitely. Per-user caps (typically 1-2 GPUs) ensure resources are distributed across users.

- **Resource exhaustion:** A single runaway process could consume all system memory, crashing everyone's containers. Memory limits per container (cgroups) mean your container gets OOM-killed before it affects others.

- **Unfair allocation:** Users who request resources but don't use them (idle containers) block others. Idle timeouts automatically reclaim unused allocations, ensuring active users get priority over idle ones.

**System enforcement:**

- **GPU allocation (gpu_allocator.py):** When you request a container, the allocator checks your current usage against your limits. Already at your GPU cap? Request denied. The allocator also tracks which physical GPU (or MIG slice) each container uses.

- **Memory limits (systemd cgroups):** Every container runs inside a cgroup with hard memory limits. Request 64GB, use 65GB = OOM killer terminates your process. This isn't punitive - it's protecting other users' containers from your memory leak.

- **Automatic cleanup (cron jobs):** Background jobs check for idle containers (low CPU/GPU usage for extended periods) and containers exceeding max runtime. These get warnings, then automatic shutdown. Freed resources become available to waiting users.

## Priority System

**Priority levels (1-100):**
- Default users: 50
- Power users: 75
- Admins: 100

**Higher priority means:**

- **Allocated GPUs first when scarce:** If 3 users request GPUs simultaneously and only 2 are available, higher-priority users get them first. Lower-priority users queue until resources free up.

- **May pre-empt lower priority (rarely):** In extreme cases, a high-priority job can terminate a lower-priority idle container to claim its GPU. This is rare - DS01 prefers waiting to pre-emption. But it means admin maintenance tasks can always run.

## Resource Efficiency

**Be a good citizen:**
```bash
# Done working? Free GPU
container-retire my-project

# Idle for lunch? Retire
container-retire my-project

# Switching projects? Retire
container-retire old-project
container-deploy new-project
```

## Next Steps

- → [Ephemeral Containers](ephemeral-containers.md)
