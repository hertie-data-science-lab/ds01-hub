# Container Issues

Solutions for container startup, runtime, and lifecycle problems.

---

## Container Won't Start {#wont-start}

**Symptoms:**
```bash
$ container-start my-project
Error: Container failed to start
```

**Causes:**
- GPU no longer exists (was reallocated)
- Resource limits exceeded
- Container configuration issue

**Solutions:**

1. **Check container status:**
   ```bash
   docker ps -a | grep my-project
   docker logs my-project._.$(whoami)
   ```

2. **Recreate container:**
   ```bash
   container-remove my-project
   container-create my-project
   ```

3. **Check resource limits:**
   ```bash
   check-limits
   ```

---

## Container Stopped Unexpectedly {#stopped-unexpectedly}

**Symptoms:**
- Container was running, now shows as stopped
- Processes terminated

**Causes:**
1. **Idle timeout reached** (typically 48 hours of low CPU)
2. **Out of memory** (OOM killer)
3. **Max runtime exceeded**
4. **Code crashed**

**Solutions:**

1. **Check logs:**
   ```bash
   docker logs my-project._.$(whoami) | tail -100
   ```

2. **Check for OOM:**
   ```bash
   docker inspect my-project._.$(whoami) | grep OOMKilled
   ```

3. **Prevent idle timeout:**
   ```bash
   touch ~/workspace/my-project/.keep-alive
   ```

4. **Restart container:**
   ```bash
   container-start my-project
   ```
   Or recreate:
   ```bash
   container-retire my-project
   container-deploy my-project
   ```

---

## Can't Find Container {#not-found}

**Symptoms:**
```bash
$ container-run my-project
Error: Container not found
```

**Causes:**
- Container was removed
- Wrong project name
- Container never created

**Solutions:**

1. **List containers:**
   ```bash
   container-list --all
   docker ps -a --filter "name=._.$(whoami)"
   ```

2. **Recreate if needed:**
   ```bash
   container-deploy my-project
   ```

3. **Check project name spelling**

---

## Container Performance {#performance}

**Symptoms:**
- Container running slowly
- High latency

**Solutions:**

1. **Check resource usage:**
   ```bash
   container-stats my-project
   ```

2. **Check if swapping:**
   ```bash
   docker exec my-project._.$(whoami) free -h
   ```

3. **Check GPU utilisation:**
   ```bash
   docker exec my-project._.$(whoami) nvidia-smi
   ```

4. **Reduce memory pressure:**
   - Close unused processes
   - Use smaller batch sizes
   - Process data in chunks

---

## Container Won't Stop {#wont-stop}

**Symptoms:**
- `container-stop` hangs
- Container stuck in stopping state

**Solutions:**

1. **Force stop:**
   ```bash
   docker stop -t 1 my-project._.$(whoami)
   ```

2. **Force kill:**
   ```bash
   docker kill my-project._.$(whoami)
   ```

3. **Remove forcefully:**
   ```bash
   container-remove my-project --force
   ```

---

## Maximum Containers Reached {#max-containers}

**Symptoms:**
```bash
$ container-deploy new-project
Error: Maximum containers reached (3/3)
```

**Solution:**
```bash
# Check current containers
container-list

# Retire unused containers
container-retire old-project-1
container-retire old-project-2

# Now can deploy new one
container-deploy new-project
```

---

## General Recovery

When in doubt, recreate:
```bash
container-retire my-project
container-deploy my-project --open
```

Your workspace files are **always safe** - recreating won't lose data.

---

## See Also

- [GPU Issues](gpu-issues.md)
- [Container Commands](../reference/commands/container-commands.md)
- [Daily Workflow](../guides/daily-workflow.md)
