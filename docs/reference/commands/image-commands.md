# Image Commands

Commands for Docker image management.

---

## Getting Help

All image commands support these flags:

| Flag | Purpose |
|------|---------|
| `--help` | Quick reference (usage, main options) |
| `--info` | Full reference (all options, examples) |
| `--concepts` | Pre-run education (what is an image?) |
| `--guided` | Interactive learning (explanations during) |

```bash
image-create --concepts   # Learn about images before creating
image-update --info       # See all update options
```

---

## Quick Reference

```bash
# Build custom image
image-create my-project

# List your images
image-list

# Update image (interactive GUI - recommended)
image-update                  # Select image, add/remove packages

# Rebuild after manual Dockerfile edit (advanced)
image-update my-project --rebuild

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

**Update existing image with package management** (L2 atomic)

```bash
image-update [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--rebuild` | Rebuild image without modifying Dockerfile |
| `--no-cache` | Force rebuild without cache |
| `--add "pkg1 pkg2"` | Add packages directly |
| `-r, --requirements FILE` | Import from requirements.txt |
| `--edit` | Edit Dockerfile manually (advanced) |

**Examples:**
```bash
# Recommended: Interactive GUI
image-update                         # Select image, add/remove packages

# Advanced: After manual Dockerfile edit
image-update my-project --rebuild    # Rebuild without prompts
image-update my-project --no-cache   # Force complete rebuild
image-update my-project --add "wandb optuna"  # Quick add from CLI
```

**When to use:**
- **No arguments** (recommended): Interactive GUI to add/remove packages
- `--rebuild`: Dockerfile was edited manually, or base image updated
- `--add`: Quick package additions from command line

**Note:** Uses existing Dockerfile at `~/dockerfiles/<project>.Dockerfile` or `~/workspace/<project>/Dockerfile`

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

## image-install

**Install packages to existing image** (L2 atomic)

```bash
image-install <project-name> <package> [packages...]
```

Quickly add packages to an existing image without manually editing the Dockerfile.

**Options:**
| Option | Description |
|--------|-------------|
| `-r <file>` | Install from requirements.txt |

**Examples:**
```bash
image-install my-project pandas numpy scipy
image-install my-project -r requirements.txt
```

**What it does:**
1. Adds packages to the Dockerfile
2. Rebuilds the image
3. Preserves existing packages

**Use when:** You need to add a few packages quickly. For major changes, edit the Dockerfile directly.

**Note:** Faster than manually editing Dockerfile + running `image-update`.

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
# or
~/workspace/<project-name>/Dockerfile
```

**Recommended:** Use `image-update` interactive GUI to manage packages.

**Advanced:** Edit Dockerfile directly:
```bash
vim ~/dockerfiles/my-project.Dockerfile
image-update my-project --rebuild
```

---

## See Also

- [Container Commands](container-commands.md)
- [Custom Images Guide](../../core-guides/custom-images.md)
- [Complete Dockerfile Guide](../../advanced/dockerfile-complete-guide.md)
