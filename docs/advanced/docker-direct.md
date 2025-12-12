# Docker Direct

When and how to use Docker commands directly on DS01.

---

## When to Use Docker Directly

**Use DS01 commands for:**
- Creating/deploying containers (`container-deploy`)
- Retiring containers (`container-retire`)
- Building images (`image-create`)

**Use Docker directly for:**

- **Debugging containers:** `docker inspect` shows the full container config - memory limits, GPU assignment, environment variables, mount points. `docker logs` shows stdout/stderr even if the process crashed. `docker exec` lets you poke around inside a running container without going through DS01 wrappers.

- **Inspecting logs:** DS01 commands don't expose container logs directly. `docker logs my-project._.$(id -u)` shows everything your process printed. Add `-f` to follow in real-time, `--tail 100` to see the last 100 lines, or `--since 1h` to filter by time.

- **Advanced operations:** Need to copy a file into a running container? `docker cp`. Want to commit the current container state as a new image? `docker commit`. Need to export a container filesystem for inspection? `docker export`. These aren't common, but when you need them, only Docker provides them.

- **One-off tasks:** Quick sanity checks like `docker exec my-project._.$(id -u) nvidia-smi` or `docker exec my-project._.$(id -u) pip list` don't need DS01 wrappers. For ad-hoc commands where you know exactly what you want, Docker is faster than navigating interactive menus.

---

## Common Docker Commands

> **Note:** In examples below, replace `<project-name>` with your actual project name. The `$(whoami)` part auto-substitutes your username.

### Container Inspection

```bash
# List all containers (including stopped)
docker ps -a

# Your containers only
docker ps -a --filter "name=._.$(whoami)"

# Container details
docker inspect <project-name>._.$(whoami)

# Container logs
docker logs <project-name>._.$(whoami)
docker logs <project-name>._.$(whoami) --tail 100
docker logs <project-name>._.$(whoami) -f  # Follow
```

### Container Interaction

```bash
# Execute command in container
docker exec <project-name>._.$(whoami) nvidia-smi
docker exec <project-name>._.$(whoami) pip list

# Enter container (alternative to container-run)
docker exec -it <project-name>._.$(whoami) /bin/bash
```

### Image Management

```bash
# List images
docker images

# Your images only
docker images | grep ds01-$(whoami)

# Remove image
docker rmi ds01-$(whoami)/<project-name>:latest

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
docker inspect <project-name>._.$(whoami) --format '{{.HostConfig.Memory}}'

# Check CPU limit
docker inspect <project-name>._.$(whoami) --format '{{.HostConfig.NanoCpus}}'

# Check GPU allocation
docker inspect <project-name>._.$(whoami) | grep -i gpu
```

---

## Debugging

### Container Won't Start

```bash
# Check last exit code
docker inspect <project-name>._.$(whoami) --format '{{.State.ExitCode}}'

# Check OOM killed
docker inspect <project-name>._.$(whoami) --format '{{.State.OOMKilled}}'

# View full state
docker inspect <project-name>._.$(whoami) --format '{{json .State}}' | jq
```

### Network Issues

```bash
# Check network settings
docker inspect <project-name>._.$(whoami) --format '{{json .NetworkSettings}}'

# Check exposed ports
docker port <project-name>._.$(whoami)
```

---

## Manual Container Operations

### Force Stop

```bash
docker stop -t 1 <project-name>._.$(whoami)
```

### Force Kill

```bash
docker kill <project-name>._.$(whoami)
```

### Force Remove

```bash
docker rm -f <project-name>._.$(whoami)
```

---

## Manual Image Building

```bash
# Build from Dockerfile
docker build -t ds01-$(whoami)/<project-name>:latest \
    -f ~/dockerfiles/<project-name>.Dockerfile .

# Build with no cache
docker build --no-cache -t ds01-$(whoami)/<project-name>:latest \
    -f ~/dockerfiles/<project-name>.Dockerfile .
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

## DS01 Enforcement

**Important:** Direct Docker commands are still subject to DS01 enforcement.

### What's Enforced (Always)

Even with direct Docker commands:

| Enforcement | Mechanism |
|-------------|-----------|
| CPU/Memory limits | Systemd cgroups (`ds01-<group>-<user>.slice`) |
| GPU limits | Docker wrapper injects constraints |
| Container labeling | Auto-added: `DS01_USER`, `DS01_MANAGED` |
| Event logging | Container lifecycle tracked |

### What's NOT Enforced

When bypassing DS01 commands:

| Feature | Impact |
|---------|--------|
| Interactive wizards | You configure everything manually |
| Auto workspace mounting | You specify `-v` flags yourself |
| Project metadata | Not tracked in DS01 metadata |
| GPU allocation tracking | May conflict with other users |

### Best Practice

```bash
# Use DS01 for creation (gets enforcement + convenience)
container deploy my-project

# Use Docker for inspection/debugging
docker logs my-project._.$(id -u)
docker exec my-project._.$(id -u) nvidia-smi

# Use DS01 for cleanup
container retire my-project
```

---

## See Also

- [Container Commands](../reference/commands/container-commands.md)
- [Dockerfile Best Practices](dockerfile-best-practices.md)
- [Troubleshooting](../troubleshooting/)
