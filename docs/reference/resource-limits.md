# Resource Limits Reference

Complete reference for DS01 resource limits and quotas.

## Your Limits

```bash
cat ~/.ds01-limits
```

## Limit Types

### GPU Limits

**max_mig_instances:** Maximum GPUs/MIG instances
- Typical: 1-2
- Admins: unlimited (null)

### Compute Limits

**max_cpus:** CPU cores per container
**memory:** RAM per container
**shm_size:** Shared memory (for PyTorch DataLoader)

### Container Limits

**max_containers_per_user:** Simultaneous containers

### Time Limits

**idle_timeout:** Auto-stop if idle (e.g., "48h")
**max_runtime:** Maximum container lifetime
**gpu_hold_after_stop:** Hold GPU after stop
**container_hold_after_stop:** Auto-remove after stop

### Priority

**priority:** Allocation priority (1-100)
- Higher = allocated first when scarce

## Checking Limits

```bash
# Your limits
cat ~/.ds01-limits

# Current usage
container-list
container-stats
```

## Next Steps

→ [Resource Management](../background/resource-management.md)
→ [Command Reference](command-reference.md)
