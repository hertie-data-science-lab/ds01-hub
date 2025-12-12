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
| `-f, --framework NAME` | Base framework (pytorch, tensorflow, jax) |
| `-t, --type TYPE` | Use case type: ml, cv, nlp, rl, audio, ts, llm, custom |
| `-p, --packages "pkg1 pkg2"` | Additional Python packages |
| `-s, --system "pkg1 pkg2"` | System packages via apt |
| `-r, --requirements FILE` | Import from requirements.txt |
| `--dockerfile PATH` | Use existing Dockerfile (skip creation) |
| `--project-dockerfile` | Store Dockerfile in project dir |
| `--no-build` | Create Dockerfile only, don't build |
| `--guided` | Educational mode |

**Examples:**
```bash
image-create                                    # Interactive
image-create my-project -f pytorch -t cv        # CV project with PyTorch
image-create nlp-exp -t nlp -p "wandb optuna"   # NLP with extra packages
image-create my-proj -r ~/workspace/my-proj/requirements.txt  # From requirements
image-create custom --no-build                  # Just create Dockerfile
```

**Use case types:**
- `ml` - General ML (xgboost, lightgbm, shap, optuna)
- `cv` - Computer Vision (timm, ultralytics, kornia)
- `nlp` - NLP (transformers, peft, safetensors)
- `rl` - Reinforcement Learning (gymnasium, stable-baselines3)
- `audio` - Audio/Speech (librosa, soundfile)
- `ts` - Time Series (statsmodels, prophet, darts)
- `llm` - LLM/GenAI (vllm, bitsandbytes, langchain)
- `custom` - Specify packages manually

**Result:** Image tagged as `ds01-<user>/<project>:latest`

**Time:** 5-15 minutes (first build), faster with cached layers

---

## image-list

**List your Docker images** (L2 atomic)

```bash
image-list [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Show all images (not just yours) |
| `-s, --size` | Show image sizes |
| `-d, --detailed` | Show detailed info with Dockerfile locations |
| `--guided` | Educational mode |

**Examples:**
```bash
image-list              # List your images
image-list --all        # List all images on server
image-list --detailed   # Show detailed info with Dockerfile locations
image-list --size       # Include image sizes
```

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
| `--add "pkg1 pkg2"` | Add Python packages directly |
| `--add-system "pkg1"` | Add system packages via apt |
| `-r, --requirements FILE` | Import from requirements.txt |
| `--rebuild` | Rebuild image without modifying Dockerfile |
| `--no-cache` | Force rebuild without cache |
| `--edit` | Edit Dockerfile manually (advanced) |
| `--guided` | Educational mode |

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
image-delete [image-name...] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--all` | Delete all your images (with confirmation) |
| `-f, --force` | Force removal (stop/remove containers first) |
| `--keep-dockerfile` | Don't delete the associated Dockerfile |
| `--guided` | Educational mode |

**Examples:**
```bash
image-delete my-project                    # Remove image (with confirmation)
image-delete img1 img2 img3                # Bulk delete multiple images
image-delete --all                         # Remove all your images
image-delete my-project --force            # Force remove (stops containers first)
image-delete my-project --keep-dockerfile  # Keep Dockerfile for later rebuild
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
