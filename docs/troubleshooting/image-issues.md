# Image Issues

Solutions for Docker image building and package problems.

---

## Image Build Fails {#build-fails}

**Symptoms:**
```bash
$ image-create my-project
Error: Failed to build image
```

**Common causes and solutions:**

### Network Issues
```bash
# Retry build
image-create my-project

# Check if base image cached
docker images | grep aime-pytorch
```

### Package Installation Fails
```bash
# Check Dockerfile
cat ~/dockerfiles/my-project.Dockerfile

# Fix package name/version
vim ~/dockerfiles/my-project.Dockerfile
image-update my-project
```

### Disk Space

Best to notify DSL admin by raising an issue ticket in [ds01-hub repo](https://github.com/hertie-data-science-lab/ds01-hub/issues). Most user permissions are restricted so you will not be able to do a full clean of docker except from those files related to you (limited). 

```bash
df -h
docker system df
docker system prune  # Free space
```

### Invalid Dockerfile Syntax
```bash
# Validate Dockerfile
docker build --no-cache -f ~/dockerfiles/my-project.Dockerfile . 2>&1 | less
```

---

## Package Not Found {#package-not-found}

**Symptoms:**
```python
ModuleNotFoundError: No module named 'transformers'
```

**Causes:**
- Package not in image
- Package name typo

> **Note:** DS01 containers ARE your Python environment - you don't need venv or conda. See [Python Environments](../concepts/python-environments.md).

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
   image-update <project-name>
   container-retire <project-name>
   container-deploy <project-name>
   ```
---

## Image Too Large {#image-size}

**Symptoms:**
- Build takes very long
- "No space left on device"

**Solutions:**

1. **Check image size:**
   ```bash
   docker images | grep my-project
   ```

2. **Use .dockerignore:**
   ```bash
   echo "data/" >> ~/workspace/<my-project>/.dockerignore
   echo "*.csv" >> ~/workspace/<my-project>/.dockerignore
   echo "models/" >> ~/workspace/<my-project>/.dockerignore
   ```

3. **Combine RUN commands:**
   ```dockerfile
   # Bad (creates extra layers)
   RUN pip install package1
   RUN pip install package2

   # Good (single layer)
   RUN pip install package1 package2
   ```

4. **Clean up in same layer:**
   ```dockerfile
   RUN pip install --no-cache-dir packages && \
       apt-get clean && \
       rm -rf /var/lib/apt/lists/*
   ```

---

## Image Won't Update {#wont-update}

**Symptoms:**
- Changes to Dockerfile not reflected
- Old packages still installed

**Solutions:**

1. **Rebuild without cache:**
   ```bash
   image-update my-project --no-cache
   ```
2. **Recreate container after rebuild:**
   ```bash
   container-deploy my-project
   ```
---

## Base Image Not Found {#base-not-found}

**Symptoms:**
```
Error: manifest for henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04 not found
```

**Solutions:**

1. **Check available base images:**
   ```bash
   docker images | grep aime
   ```

2. **Pull base image:**
   ```bash
   docker pull henrycgbaker/aime-pytorch:2.8.0-cuda12.4-ubuntu22.04
   ```

3. **Use different base image version:**
   ```bash
   # Edit Dockerfile
   vim ~/workspace/my-project/Dockerfile
   # Change FROM line to available image
   ```

---

## Dependency Conflicts {#conflicts}

**Symptoms:**
```
ERROR: Cannot install package-a and package-b because these package versions have conflicting dependencies
```

**Solutions:**

1. **Pin specific versions:**
   ```dockerfile
   RUN pip install transformers==4.30.0 datasets==2.14.0
   ```

2. **Install in order:**
   ```dockerfile
   RUN pip install torch==2.0.0 && \
       pip install transformers
   ```

3. **Create fresh environment:**
   ```dockerfile
   RUN pip install --upgrade pip && \
       pip install package1 package2
   ```

---

## See Also

- [Container Issues](container-issues.md)
- [Custom Images Guide](../guides/custom-images.md)
- [Dockerfile Best Practices](../advanced/dockerfile-best-practices.md)
