# Servers & High-Performance Computing

**Understanding shared computing environments and how they prepare you for the cloud.**

> **Part of [Educational Computing Context](README.md)** - Career-relevant knowledge beyond DS01 basics.
>
> **Just want to use DS01?** Skip to [First Container](../getting-started/first-container.md).

Understanding servers and shared computing prepares you for cloud platforms, HPC clusters, and production ML systems.

**Reading time:** 30 minutes

---

## What is a Server?

**A server is a powerful computer designed to run 24/7 and serve multiple users simultaneously.**

Think of it like:
- **Your laptop** = your car (personal, customizable, turn off when done)
- **A server** = a bus (shared, runs all day, serves many people)

---

## Why Use a Server Instead of Your Laptop?

### Computing Power

```
Your Laptop          DS01 Server
-----------          -----------
8-16 CPU cores       128+ cores
8-32 GB RAM          2TB+ RAM
Consumer GPU         NVIDIA A100/H100 data center GPUs
256GB-1TB storage    Tens of terabytes
```

**Real impact:** Training a large transformer:
- Your laptop: 2 weeks (if it fits in memory)
- DS01: 8 hours

### Cost Efficiency

Buying equivalent hardware: $100,000+
Sharing among 20 users: $5,000 worth of access per person

Plus: IT maintenance, electricity, cooling included.

### Always Available

- Run experiments overnight without leaving your laptop at the office
- Redundant power, enterprise storage, professional maintenance
- Access from anywhere via SSH

---

## Key Differences from Your Laptop

| Aspect | Laptop | Server |
|--------|--------|--------|
| Users | One (you) | 20-100+ |
| Interface | Desktop GUI | Command line |
| Access | Physical | Remote (SSH) |
| Software | Install globally | Use containers |
| Resources | All yours | Fair sharing |

### Multi-User Environment

You share resources. Limits prevent any one user from monopolizing the system.

**Analogy:** Your apartment vs a shared lab facility.

### Command Line Interface

Servers skip the desktop to maximize compute power. You'll learn essential commands quickly, and most tasks are actually *faster* via CLI.

### Remote Access

SSH lets you connect from anywhere. Leave experiments running, check from home.

---

## High-Performance Computing (HPC) Concepts

**HPC** = Using powerful, shared computing resources for intensive workloads.

DS01 is an HPC system specialised for data science and ML.

### Core HPC Principles

**1. Resource Scheduling**
- Multiple users want GPUs, limited availability
- Priority and queuing ensure fairness
- Time limits prevent monopolisation

**2. Fair Share**
- Resources distributed fairly among users
- Per-user limits (GPUs, containers, memory)
- Idle timeouts free unused resources

**3. Resource Limits (Quotas)**
```bash
# Check your limits
check-limits

# Example output:
Max GPUs: 2
Max Containers: 3
Memory per container: 64GB
Max Runtime: 24h (varies by user)
Idle Timeout: 0.5h (varies by user)
```

### HPC Terminology → DS01

| HPC Term | DS01 Equivalent |
|----------|----------------|
| Node | DS01 server |
| Job | Container |
| Queue | Resource allocation waiting |
| Walltime | Max runtime limit |
| Scheduler | GPU allocator |
| Allocation | Resource limits |

---

## Be a Good Citizen

### Do:
- Retire containers when done (`container-retire`)
- Use appropriate resources (don't request max if you need less)
- Monitor your usage (`container-stats`)
- Plan for wait times during peak hours

### Don't:
- Leave containers idle for days
- Monopolise all GPUs
- Ignore resource limit warnings

### Efficient Resource Use

```python
# Load data efficiently
dataset = LazyDataset(...)  # Don't load everything into RAM

# Use appropriate batch sizes
batch_size = 32  # Don't use 1 if 32 works

# Checkpoint regularly (system may need to stop your job)
torch.save(checkpoint, 'latest.pt')
```

---

## What You Might Encounter

### Waiting for Resources
```
Info: No GPUs currently available
Info: 3 users ahead in queue
```
Normal in shared systems. Plan alternative tasks.

### Time Limits
```
Your container has been running for 22h (max: 24h)
Warning: Will be stopped in 2 hours
```
Checkpoint your work. Run `check-limits` to see your max runtime.

### Idle Timeouts
```
Container idle for 25min (limit: 30min)
Warning: Will be stopped if idle continues
```
Frees unused resources for others.

---

## Common Misconceptions

**"If I break something, I'll crash the server for everyone"**

False. Containers provide isolation. You can crash your container but cannot affect others or the host system.

**"My files disappear when container stops"**

Partially true. Files in `/workspace` (inside container) are persistent. Everything else in the container is temporary.

**"I need admin/root access"**

Mostly false. With containers you can install packages, modify your environment, run any software within your limits.

---

## Industry Context

### This is How Production Works

**Cloud providers (AWS, GCP, Azure):**
- EC2 instances = renting servers
- Cloud GPUs = server GPU access
- Containers = server containerisation

**Companies use servers for:**
- Training ML models (too large for laptops)
- Serving applications (handle millions of requests)
- Data processing (petabytes of data)

### DS01 vs Cloud

```bash
# AWS
aws ec2 run-instances --instance-type p3.2xlarge
# Pay per hour, terminate when done

# DS01
container-deploy my-project --gpu 1
# Free (included in allocation), retire when done
```

Same workflow, different billing model.

---

## Skills You're Developing

**Technical:**
- Linux command line
- SSH and remote connections
- Understanding resource constraints
- Container workflows

**Professional:**
- Working in shared environments
- Resource management and efficiency
- Production-like workflows
- Cloud-readiness (AWS/GCP work similarly)

---

## Summary

1. **Servers = Powerful shared computers** running 24/7
2. **Remote access** via SSH - work from anywhere
3. **Fair sharing** via limits and scheduling
4. **Containers** give you isolated, customizable environments
5. **Skills transfer** to cloud platforms and production systems

---

## Next Steps

**Continue learning:**
- [Linux Basics](linux-basics.md) - Command line essentials
- [Containers & Docker](containers-and-docker.md) - Why containers?

**Start using DS01:**
- [First Container](../getting-started/first-container.md) - Deploy in 5 minutes
- [Daily Workflow](../core-guides/daily-workflow.md) - Common patterns
