# Resource Management

Understanding DS01's resource allocation and limits.

## Your Resource Limits

```bash
cat ~/.ds01-limits
```

**Typical limits:**
- Max GPUs: 1-2
- Max Containers: 2-3
- Memory: 64-128GB per container
- Idle Timeout: 48 hours
- Max Runtime: 168 hours (1 week)

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

→ [Ephemeral Containers](ephemeral-containers.md)
→ [Resource Limits Reference](../reference/resource-limits.md)
