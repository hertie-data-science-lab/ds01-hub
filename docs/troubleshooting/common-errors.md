# Common Errors

Solutions for files, permissions, network, and other common issues.

---

## File Issues

### Can't Find My Files {#files-missing}

**Symptoms:**
- Files missing from container
- Workspace appears empty

**Solutions:**

1. **Check both locations:**
   ```bash
   # On host
   ls ~/workspace/my-project/

   # In container
   docker exec my-project._.$(whoami) ls /workspace/
   ```

2. **Remember the mapping:**
   ```
   Host:      ~/workspace/my-project/
   Container: /workspace/
   ```

3. **Verify workspace mount:**
   ```bash
   docker inspect my-project._.$(whoami) | grep -A 5 "Mounts"
   ```

---

### Permission Denied on Files {#permission-denied}

**Symptoms:**
```bash
$ touch /workspace/file.txt
Permission denied
```

**Solutions:**

1. **Check ownership:**
   ```bash
   ls -ld ~/workspace/my-project/
   # Should be owned by you
   ```

2. **Fix permissions (on host):**
   ```bash
   sudo chown -R $(whoami):$(whoami) ~/workspace/my-project/
   ```

3. **Check disk space:**
   ```bash
   df -h | grep home
   ```

---

### Out of Disk Space {#disk-space}

**Symptoms:**
```bash
No space left on device
```

**Solutions:**

1. **Check usage:**
   ```bash
   # Workspace
   du -sh ~/workspace/*

   # Docker
   docker system df
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

---

## Permission Issues

### Docker Permission Denied {#docker-permission}

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

### Commands Not Found {#commands-not-found}

**Symptoms:**
```bash
$ container-deploy my-project
bash: container-deploy: command not found
```

**Solutions:**

1. **Check PATH:**
   ```bash
   echo $PATH | grep ds01
   ```

2. **Use full path:**
   ```bash
   /opt/ds01-infra/scripts/user/orchestrators/container-deploy my-project
   ```

3. **Fix PATH:**
   ```bash
   shell-setup
   source ~/.bashrc
   ```

---

## Network Issues

### Can't Access Jupyter {#jupyter-access}

**Symptoms:**
- Jupyter running but can't access in browser

**Solutions:**

1. **Check Jupyter is running:**
   ```bash
   docker exec my-project._.$(whoami) ps aux | grep jupyter
   ```

2. **Check port:**
   ```bash
   docker port my-project._.$(whoami)
   ```

3. **Set up SSH tunnel:**
   ```bash
   # On your laptop
   ssh -L 8888:localhost:8888 user@ds01-server

   # Then access: http://localhost:8888
   ```

4. **Start Jupyter correctly:**
   ```bash
   jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
   ```

---

### Can't Download Datasets

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

2. **Try alternative download:**
   ```bash
   # Instead of wget
   curl -O https://example.com/data.zip

   # Or Python
   python -c "import urllib.request; urllib.request.urlretrieve('url', 'file')"
   ```

---

## Git Issues

### Can't Push to GitHub

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

## Resource Limits

### Memory Limit Exceeded

**Symptoms:**
- Container killed
- OOMKilled in logs

**Solutions:**

1. **Check limits:**
   ```bash
   check-limits
   ```

2. **Reduce memory usage:**
   - Process data in chunks
   - Use data generators
   - Clear variables when done

---

## Error Message Reference

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

## Emergency Recovery

### "I Lost All My Work!"

**Don't panic. Check:**

1. **Workspace (most likely safe):**
   ```bash
   ls ~/workspace/my-project/
   ```

2. **Git (if you pushed):**
   ```bash
   cd ~/workspace/my-project
   git log
   git pull
   ```

3. **Previous checkpoints:**
   ```bash
   ls ~/workspace/my-project/models/
   ```

---

### "System Seems Broken"

**Steps:**

1. **Check system status:**
   ```bash
   ds01-dashboard
   ```

2. **Check your account:**
   ```bash
   groups
   df -h
   ```

3. **Try minimal operation:**
   ```bash
   docker ps
   ```

4. **Contact administrator** with details

---

## See Also

- [Container Issues](container-issues.md)
- [GPU Issues](gpu-issues.md)
- [Image Issues](image-issues.md)
