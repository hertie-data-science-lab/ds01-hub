# Docker Direct

When and how to use Docker commands directly on DS01.

---

## When to Use Docker Directly

**Use DS01 commands for:**
- Creating/deploying containers (`container-deploy`)
- Retiring containers (`container-retire`)
- Building images (`image-create`)

**Use Docker directly for:**
- Debugging containers
- Inspecting logs
- Advanced operations
- One-off tasks

---

## Common Docker Commands

### Container Inspection

```bash
# List all containers (including stopped)
docker ps -a

# Your containers only
docker ps -a --filter "name=._.$(whoami)"

# Container details
docker inspect my-project._.$(whoami)

# Container logs
docker logs my-project._.$(whoami)
docker logs my-project._.$(whoami) --tail 100
docker logs my-project._.$(whoami) -f  # Follow
```

### Container Interaction

```bash
# Execute command in container
docker exec my-project._.$(whoami) nvidia-smi
docker exec my-project._.$(whoami) pip list

# Enter container (alternative to container-run)
docker exec -it my-project._.$(whoami) /bin/bash
```

### Image Management

```bash
# List images
docker images

# Your images only
docker images | grep ds01-$(whoami)

# Remove image
docker rmi ds01-$(whoami)/my-project:latest

# Prune unused images
docker image prune
```

### System Cleanup

```bash
# Show disk usage
docker system df

# Clean up everything unused
docker system prune

# Remove all stopped containers
docker container prune
```

---

## DS01 Container Naming

Container names follow the pattern:
```
<project-name>._.$(whoami)
```

Example:
```bash
my-project._.alice
experiment-1._.bob
```

---

## Inspecting Resource Limits

```bash
# Check memory limit
docker inspect my-project._.$(whoami) --format '{{.HostConfig.Memory}}'

# Check CPU limit
docker inspect my-project._.$(whoami) --format '{{.HostConfig.NanoCpus}}'

# Check GPU allocation
docker inspect my-project._.$(whoami) | grep -i gpu
```

---

## Debugging

### Container Won't Start

```bash
# Check last exit code
docker inspect my-project._.$(whoami) --format '{{.State.ExitCode}}'

# Check OOM killed
docker inspect my-project._.$(whoami) --format '{{.State.OOMKilled}}'

# View full state
docker inspect my-project._.$(whoami) --format '{{json .State}}' | jq
```

### Network Issues

```bash
# Check network settings
docker inspect my-project._.$(whoami) --format '{{json .NetworkSettings}}'

# Check exposed ports
docker port my-project._.$(whoami)
```

---

## Manual Container Operations

### Force Stop

```bash
docker stop -t 1 my-project._.$(whoami)
```

### Force Kill

```bash
docker kill my-project._.$(whoami)
```

### Force Remove

```bash
docker rm -f my-project._.$(whoami)
```

---

## Manual Image Building

```bash
# Build from Dockerfile
docker build -t ds01-$(whoami)/my-project:latest \
    -f ~/dockerfiles/my-project.Dockerfile .

# Build with no cache
docker build --no-cache -t ds01-$(whoami)/my-project:latest \
    -f ~/dockerfiles/my-project.Dockerfile .
```

---

## Tagging Images

```bash
# Tag for version control
docker tag ds01-alice/project:latest ds01-alice/project:v1.0

# Tag as backup
docker tag ds01-alice/project:latest ds01-alice/project:backup-$(date +%Y%m%d)
```

---

## Caution

**Don't bypass DS01 for:**
- Container creation (use `container-deploy`)
- GPU allocation (use DS01 commands)
- Resource limits (enforced by DS01)

Direct Docker bypasses:
- GPU allocation tracking
- Resource limit enforcement
- Event logging

---

## See Also

- [Container Commands](../reference/commands/container-commands.md)
- [Dockerfile Best Practices](dockerfile-best-practices.md)
- [Troubleshooting](../troubleshooting/)
