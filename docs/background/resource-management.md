# Resource Management

**Understanding quotas, fair sharing, and resource allocation in shared computing.**

> **Part of [Educational Computing Context](README.md)** - Career-relevant knowledge beyond DS01 basics.

Resource management is a core concept in cloud computing, HPC, and multi-tenant systems. This guide explains DS01's resource allocation and how these patterns apply to production systems.

## Your Resource Limits

```bash
cat ~/.ds01-limits
```

**Typical limits:**
- Max GPUs: 1-2
- Max Containers: 2-3
- Memory: 32-128GB per container
- Idle Timeout: 30min-2h (varies by user)
- Max Runtime: 24h-72h (varies by user)

Run `check-limits` to see your current values.

## How Limits Work

**Per-user limits prevent:**
- One user monopolizing all GPUs
- Resource exhaustion
- Unfair allocation

**System enforcement:**
- GPU allocation (via gpu_allocator.py)
- Memory limits (via systemd cgroups)
- Automatic cleanup (cron jobs)

## Priority System

**Priority levels (1-100):**
- Default users: 50
- Power users: 75
- Admins: 100

**Higher priority:**
- Allocated GPUs first when scarce
- May pre-empt lower priority (rarely)

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
- → [Resource Limits Reference](../reference/resource-limits.md)
