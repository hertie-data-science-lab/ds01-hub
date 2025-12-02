# Image Commands

Commands for Docker image management.

---

## Quick Reference

```bash
# Build custom image
image-create my-project

# List your images
image-list

# Rebuild image
image-update my-project

# Delete image
image-delete my-project
```

---

## image-create

**Build custom Docker image** (L2 atomic)

```bash
image-create [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--framework <name>` | Base framework (pytorch, tensorflow, jax) |
| `--guided` | Educational mode |

**Examples:**
```bash
image-create                              # Interactive
image-create my-project --framework pytorch
```

**What it does (4 phases):**
1. Choose base framework (PyTorch, TensorFlow, JAX)
2. Add Jupyter Lab and extensions
3. Add data science packages
4. Add custom packages (optional)

**Result:** Image tagged as `ds01-<user>/<project>:latest`

**Time:** 5-15 minutes (first build), faster with cached layers

---

## image-list

**List your Docker images** (L2 atomic)

```bash
image-list [--all]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--all` | Include system images |

**Example output:**
```
REPOSITORY              TAG      SIZE     CREATED
ds01-alice/my-project   latest   8.2GB    2 days ago
ds01-alice/experiment   latest   7.9GB    1 week ago
```

---

## image-update

**Rebuild existing image** (L2 atomic)

```bash
image-update <project-name> [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--no-cache` | Force rebuild without cache |

**Examples:**
```bash
image-update my-project              # Rebuild with cache
image-update my-project --no-cache   # Force complete rebuild
```

**When to use:**
- Added packages to Dockerfile
- Updated base image
- Fixed image issues

**Note:** Uses existing Dockerfile at `~/dockerfiles/<project>.Dockerfile`

---

## image-delete

**Remove Docker image** (L2 atomic)

```bash
image-delete <project-name> [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--force` | Delete even if containers exist |

**Examples:**
```bash
image-delete my-project
image-delete my-project --force
```

**Note:** Containers using this image must be removed first (or use --force)

---

## Image Naming Convention

```
ds01-<username>/<project-name>:latest
      ↑              ↑           ↑
      Your user ID   Project     Tag
```

**Examples:**
- `ds01-alice/thesis:latest`
- `ds01-bob/experiment-42:latest`

---

## Image Tagging

Tag images to save working environments:

```bash
# Tag current state
docker tag ds01-alice/project:latest ds01-alice/project:working-v1

# List tags
docker images ds01-alice/project

# Use specific tag
container-deploy --image ds01-alice/project:working-v1
```

---

## Dockerfile Location

Images are built from Dockerfiles at:
```
~/dockerfiles/<project-name>.Dockerfile
```

Edit directly for advanced customization:
```bash
nano ~/dockerfiles/my-project.Dockerfile
image-update my-project
```

---

## See Also

- [Container Commands](container-commands.md)
- [Custom Images Guide](../../guides/custom-images.md)
- [Dockerfile Best Practices](../../advanced/dockerfile-best-practices.md)
