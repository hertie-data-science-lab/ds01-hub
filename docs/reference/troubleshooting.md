# Troubleshooting Guide

Common issues and solutions for DS01. Check here before asking for help.

> **Note:** In examples below, replace `<project-name>` with your actual project name. The `$(whoami)` part auto-substitutes your username.

---

## Container Issues

### "No GPUs available"

**Symptoms:**
```bash
$ container-deploy my-project
Error: No GPUs available for allocation
```

**Causes:**
- All GPUs currently allocated
- System maintenance
- GPU hardware issues

**Solutions:**
1. **Check availability:**
   ```bash
   ds01-dashboard
   # or
   python3 /opt/ds01-infra/scripts/docker/gpu_allocator.py status
   ```

2. **Wait for GPU to free up** - Other users may be finishing soon

3. **Check for idle containers:**
   ```bash
   # Retire your idle containers
   container-list
   container-retire old-project
   ```

4. **Contact admin** if GPUs show available but allocation fails

---

### "Container won't start"

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
   docker logs <project-name>._.$(whoami)
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

### "Container stopped unexpectedly"

**Symptoms:**
- Container was running, now shows as stopped
- Processes terminated

**Causes:**
1. **Idle timeout reached** (30min-2h, varies by user)
2. **Out of memory** (OOM killer)
3. **Max runtime exceeded**
4. **Code crashed**

**Solutions:**
1. **Check logs:**
   ```bash
   docker logs <project-name>._.$(whoami) | tail -100
   ```

2. **Check for OOM:**
   ```bash
   docker inspect <project-name>._.$(whoami) | grep OOMKilled
   ```

3. **Prevent idle timeout:**
   ```bash
   touch ~/workspace/<project-name>/.keep-alive
   ```

   > **⚠️ Contact DSL First:** The `.keep-alive` workaround is available but should be a **last resort** as it can disrupt the system for other users. Please [open an issue on DS01 Hub](https://github.com/hertie-data-science-lab/ds01-hub/issues) first to find a better solution together.

4. **Restart container:**
   ```bash
   container-start my-project
   # or recreate
   container-retire my-project
   container-deploy my-project
   ```

---

### "Can't enter container"

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

## File & Storage Issues

### "Can't find my files"

**Symptoms:**
- Files missing from container
- Workspace appears empty

**Causes:**
- Looking in wrong location
- Files saved outside workspace
- Permissions issue

**Solutions:**
1. **Check both locations:**
   ```bash
   # On host
   ls ~/workspace/<project-name>/

   # In container
   docker exec <project-name>._.$(whoami) ls /workspace/
   ```

2. **Verify workspace mount:**
   ```bash
   docker inspect <project-name>._.$(whoami) | grep -A 5 "Mounts"
   ```

3. **Remember the mapping:**
   - Host: `~/workspace/<project-name>/`
   - Container: `/workspace/`

---

### "Permission denied" on files

**Symptoms:**
```bash
$ touch /workspace/file.txt
Permission denied
```

**Causes:**
- Directory ownership issue
- Incorrect mount
- Filesystem full

**Solutions:**
1. **Check ownership:**
   ```bash
   ls -ld ~/workspace/<project-name>/
   # Should be owned by you
   ```

2. **Fix permissions (on host):**
   ```bash
   sudo chown -R $(whoami):$(whoami) ~/workspace/<project-name>/
   ```

3. **Check disk space:**
   ```bash
   df -h | grep home
   ```

---

### "Out of disk space"

**Symptoms:**
```bash
$ cp large-file.dat /workspace/
No space left on device
```

**Causes:**
- Workspace full
- Docker images consuming space
- Quota exceeded

**Solutions:**
1. **Check usage:**
   ```bash
   # Workspace
   du -sh ~/workspace/*

   # Docker
   docker system df

   # Quota (if enforced)
   quota -s
   ```

2. **Clean up:**
   ```bash
   # Remove old projects
   rm -rf ~/workspace/old-project/

   # Clean Docker
   docker image prune
   docker system prune

   # Remove old checkpoints
   find ~/workspace -name "checkpoint-*.pt" -mtime +30 -delete
   ```

3. **Contact admin** if quota too small

---

## Image Issues

### "Image build fails"

**Symptoms:**
```bash
$ image-create my-project
Error: Failed to build image
```

**Common causes and solutions:**

**1. Network issues (downloading base image)**
```bash
# Retry build
image-create my-project

# Or use cached base
docker images | grep aime-pytorch
```

**2. Package installation fails**
```bash
# Use interactive GUI to fix packages
image-update                  # Select image, fix package names/versions

# Or check Dockerfile manually
cat ~/dockerfiles/my-project.Dockerfile
vim ~/dockerfiles/my-project.Dockerfile
image-update my-project --rebuild
```

**3. Disk space**
```bash
df -h
docker system df
docker system prune  # Free space
```

**4. Invalid Dockerfile syntax**
```bash
# Validate Dockerfile
docker build --no-cache -f ~/dockerfiles/my-project.Dockerfile . 2>&1 | less
```

---

### "Package not found in container"

**Symptoms:**
```bash
$ python -c "import transformers"
ModuleNotFoundError: No module named 'transformers'
```

**Causes:**
- Package not in image
- Package name typo

> **Note:** DS01 containers ARE your Python environment - you don't need venv or conda. See [Python Environments](../key-concepts/python-environments.md).

**Solutions:**
1. **Check if installed:**
   ```bash
   pip list | grep transformers
   ```

2. **Temporary install:**
   ```bash
   pip install transformers
   ```

3. **Permanent fix (add to image):**
   ```bash
   exit  # Exit container
   image-update                  # Select image, add package
   container-retire <project-name>
   container-deploy <project-name>
   ```

---

## GPU Issues

### "nvidia-smi: command not found"

**Symptoms:**
```bash
$ nvidia-smi
bash: nvidia-smi: command not found
```

**Cause:** Not inside container, or container not started with GPU

**Solutions:**
1. **Enter container:**
   ```bash
   container-run my-project
   nvidia-smi  # Should work now
   ```

2. **Check GPU allocation:**
   ```bash
   docker inspect <project-name>._.$(whoami) | grep -i gpu
   ```

3. **Recreate container:**
   ```bash
   container-retire my-project
   container-deploy my-project
   ```

---

### "CUDA out of memory"

**Symptoms:**
```bash
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

**Causes:**
- Model too large for GPU
- Batch size too large
- Memory leak in code

**Solutions:**
1. **Reduce batch size:**
   ```python
   batch_size = 32  # Try 16, 8, or smaller
   ```

2. **Use gradient accumulation:**
   ```python
   # Effective batch size = batch_size * accumulation_steps
   accumulation_steps = 4
   ```

3. **Use mixed precision:**
   ```python
   from torch.cuda.amp import autocast, GradScaler
   scaler = GradScaler()

   with autocast():
       output = model(input)
   ```

4. **Clear cache:**
   ```python
   import torch
   torch.cuda.empty_cache()
   ```

5. **Check for memory leaks:**
   ```python
   # Monitor memory usage
   print(torch.cuda.memory_summary())
   ```

---

### "GPU not showing in nvidia-smi"

**Symptoms:**
```bash
$ nvidia-smi
No devices found
```

**Causes:**
- Not allocated GPU
- Container created without GPU

**Solutions:**
1. **Check allocation:**
   ```bash
   python3 /opt/ds01-infra/scripts/docker/gpu_allocator.py status
   ```

2. **Recreate container:**
   ```bash
   container-retire my-project
   container-deploy my-project
   ```

---

## Network Issues

### "Can't access Jupyter"

**Symptoms:**
- Jupyter running but can't access in browser

**Solutions:**
1. **Check Jupyter is running:**
   ```bash
   docker exec <project-name>._.$(whoami) ps aux | grep jupyter
   ```

2. **Check port:**
   ```bash
   docker port <project-name>._.$(whoami)
   ```

3. **Set up SSH tunnel:**
   ```bash
   # On your laptop
   ssh -L 8888:localhost:8888 ds01
   # Without SSH keys: ssh -L 8888:localhost:8888 <student-id>@students.hertie-school.org@10.1.23.20

   # Then access: http://localhost:8888
   ```

4. **Start Jupyter correctly:**
   ```bash
   jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
   ```

---

### "Can't download datasets"

**Symptoms:**
```bash
$ wget https://example.com/data.zip
Connection refused
```

**Solutions:**
1. **Check network from container:**
   ```bash
   ping google.com
   curl https://google.com
   ```

2. **Check proxy settings** (if your network requires proxy)

3. **Try alternative download method:**
   ```bash
   # Instead of wget
   curl -O https://example.com/data.zip

   # Or Python
   python -c "import urllib.request; urllib.request.urlretrieve('url', 'file')"
   ```

---

## Permission Issues

### "Permission denied" for Docker

**Symptoms:**
```bash
$ docker ps
Permission denied while trying to connect to the Docker daemon socket
```

**Cause:** Not in `docker` group

**Solution:**
```bash
# Check groups
groups | grep docker

# If not in docker group, ask admin:
# sudo usermod -aG docker your-username
# Then log out and back in
```

---

### "Permission denied" for commands

**Symptoms:**
```bash
$ container-deploy my-project
bash: container-deploy: Permission denied
```

**Causes:**
- Commands not in PATH
- Commands not executable

**Solutions:**
1. **Check PATH:**
   ```bash
   echo $PATH | grep ds01
   ```

2. **Use full path:**
   ```bash
   /opt/ds01-infra/scripts/user/container-deploy.sh my-project
   ```

3. **Ask admin to update symlinks:**
   ```bash
   sudo /opt/ds01-infra/scripts/system/deploy-commands.sh
   ```

---

## Resource Limit Issues

### "At maximum container limit"

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

### "Memory limit exceeded"

**Symptoms:**
- Container killed
- OOMKilled in logs

**Solutions:**
1. **Check limits:**
   ```bash
   check-limits
   # Shows your memory limit and current usage
   ```

2. **Reduce memory usage:**
   - Process data in chunks
   - Use data generators
   - Clear variables when done

3. **Request limit increase** (contact admin)

---

## Git Issues

### "Can't push to GitHub"

**Symptoms:**
```bash
$ git push
Permission denied (publickey)
```

**Solutions:**
1. **Check SSH key:**
   ```bash
   ls ~/.ssh/
   cat ~/.ssh/id_ed25519.pub
   ```

2. **Add key to GitHub:**
   - Copy public key
   - GitHub → Settings → SSH Keys → Add

3. **Test connection:**
   ```bash
   ssh -T git@github.com
   ```

4. **Use HTTPS instead:**
   ```bash
   git remote set-url origin https://github.com/user/repo.git
   ```

---

## Getting Help

### Before Asking for Help

1. **Check this guide** - Most issues are common

2. **Check logs:**
   ```bash
   docker logs <project-name>._.$(whoami)
   ```

3. **Check system status:**
   ```bash
   ds01-dashboard
   container-list
   container-stats
   ```

4. **Try recreating:**
   ```bash
   container-retire my-project
   container-deploy my-project
   ```

---

### How to Ask for Help

**Include this information:**
1. **What you tried:**
   ```bash
   container-deploy my-project
   ```

2. **Error message:**
   ```
   Error: No GPUs available
   ```

3. **System state:**
   ```bash
   container-list
   check-limits
   ```

4. **Relevant logs:**
   ```bash
   docker logs <project-name>._.$(whoami) | tail -50
   ```

---

### Contact Points

- **System administrator** - Account issues, quotas, system problems
- **Documentation** - This guide, [Command Reference](command-reference.md)
- **Colleagues** - Often have encountered same issues

---

## Preventive Measures

### Best Practices to Avoid Issues

1. **Save frequently to workspace:**
   ```bash
   # Always work in /workspace (inside container)
   cd /workspace
   ```

2. **Commit code regularly:**
   ```bash
   git commit -m "Progress checkpoint"
   git push
   ```

3. **Retire containers when done:**
   ```bash
   container-retire my-project
   ```

4. **Monitor resource usage:**
   ```bash
   container-stats
   nvidia-smi  # Inside container
   ```

5. **Keep environments updated:**
   ```bash
   image-update                  # Add packages as needed
   ```

6. **Check limits before starting:**
   ```bash
   check-limits
   container-list  # How many running?
   ```

---

## Emergency Recovery

### "I lost all my work!"

**Don't panic. Check:**

1. **Workspace (most likely safe):**
   ```bash
   ls ~/workspace/<project-name>/
   ```

2. **Git (if you pushed):**
   ```bash
   cd ~/workspace/my-project
   git log
   git pull
   ```

3. **Previous checkpoints:**
   ```bash
   ls ~/workspace/<project-name>/models/
   ```

**If truly lost:**
- Learn from mistake
- Implement better backup strategy
- Use Git religiously going forward

---

### "Container won't stop"

**Symptoms:**
- `container-stop` hangs
- Container stuck in stopping state

**Solutions:**
1. **Force stop:**
   ```bash
   docker stop -t 1 <project-name>._.$(whoami)
   ```

2. **Force kill:**
   ```bash
   docker kill <project-name>._.$(whoami)
   ```

3. **Remove forcefully:**
   ```bash
   container-remove my-project --force
   ```

---

### "System seems broken"

**Symptoms:**
- Multiple commands failing
- Unusual errors

**Steps:**
1. **Check system status:**
   ```bash
   ds01-dashboard
   ```

2. **Check your account:**
   ```bash
   groups
   quota -s
   df -h
   ```

3. **Try minimal operation:**
   ```bash
   docker ps
   ```

4. **Contact administrator** with details

---

## Common Error Messages Decoded

| Error | Meaning | Solution |
|-------|---------|----------|
| `No GPUs available` | All GPUs allocated | Wait or retire old containers |
| `OOMKilled` | Out of memory | Reduce memory usage |
| `Permission denied` | Not in docker group or file permissions | Check groups, fix permissions |
| `Container not found` | Container removed or wrong name | Recreate or check name |
| `Image not found` | Image doesn't exist | Build image first |
| `Network unreachable` | Network issue | Check network, retry |
| `Quota exceeded` | Hit disk quota | Clean up old files |

---

## Next Steps

**Understand the system:**
- → [Containers Explained](../background/containers-and-docker.md)
- → [Workspaces & Persistence](../background/workspaces-and-persistence.md)

**Learn best practices:**
→ 
- → [Daily Usage Patterns](../core-guides/daily-workflow.md)

**Command reference:**
- → [Command Reference](command-reference.md)

---

**Most issues have simple solutions. Check logs, try recreating, and remember: your workspace is always safe!**
