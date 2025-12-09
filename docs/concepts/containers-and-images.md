# Containers and Images

Understanding the relationship between Docker images and containers.

---

## The Cooking Analogy

**Image = Recipe**
- Written instructions (Dockerfile)
- Lists ingredients (base image, packages)
- Describes steps (RUN commands)
- Can share with others
- Version controlled

**Container = Meal**
- Created by following the recipe
- Temporary (eaten/removed)
- Can make many meals from one recipe
- Each meal is independent

**Key insight:** Changing the recipe doesn't change already-cooked meals.

---

## Technical Definitions

### Docker Image

**An image is:**
- A read-only template
- Contains operating system, libraries, and your code
- Built from a Dockerfile
- Stored on disk
- Can create many containers from one image

**Example:**
```
Image: ds01-12345/my-thesis:latest
  ├─ Ubuntu 22.04
  ├─ CUDA 12.4
  ├─ PyTorch 2.8.0
  ├─ Your packages (transformers, datasets, etc.)
  └─ Configuration
```

**Images are permanent** - stored until you delete them.

### Docker Container

**A container is:**
- A running instance of an image
- Has its own filesystem (mostly from image)
- Can read/write files
- Temporary - removed when you're done
- Isolated from other containers

**Example:**
```
Container: my-thesis._.12345
  ├─ Created from: ds01-12345/my-thesis:latest
  ├─ Status: Running
  ├─ GPU: GPU-0
  └─ Workspace: ~/workspace/my-thesis (mounted)
```

**Containers are ephemeral** - designed to be removed.

---

## The Relationship

```
                    ┌─────────────┐
                    │  Dockerfile │  Your recipe
                    └──────┬──────┘
                           │
                    docker build
                           │
                           ▼
                    ┌─────────────┐
                    │    Image    │  The blueprint
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    project launch    project launch    project launch
         │                 │                 │
         ▼                 ▼                 ▼
   ┌──────────┐      ┌──────────┐      ┌──────────┐
   │Container1│      │Container2│      │Container3│
   └──────────┘      └──────────┘      └──────────┘
    temporary         temporary         temporary
```

**One image** → **Many containers**

**Modify image** → **Rebuild** → **Recreate containers**

---

## Why This Matters

### Scenario 1: Adding a Package

**Wrong approach:**
```bash
# In container
pip install transformers

# Exit, remove container
exit
container retire my-project

# Launch new container
project launch my-project

# transformers is GONE!
```

**Why?** Changes inside container are lost when container is removed.

**Right approach:**
```bash
# Edit recipe (Dockerfile)
vim ~/workspace/my-project/Dockerfile
# Add: RUN pip install transformers

# Rebuild image
image-update my-project

# Recreate container from new image
container retire my-project
project launch my-project

# transformers is INSTALLED!
```

**Why?** Image contains the change, all new containers have it.

### Scenario 2: Multiple Containers from One Image

```bash
# Build image once
project init my-project
# Creates image: ds01-12345/my-project:latest

# Launch container 1
project launch my-project --background
# Creates: my-project._.12345

# Launch container 2 (different project name)
project launch my-project-test --background
# Can use same image!

# Both containers have same packages
# Both started from same blueprint
```

---

## Common Questions

### "Can I modify an image directly?"

**No.** Images are read-only.

**To change an image:**
1. Edit Dockerfile
2. Rebuild: `image-update my-project`

### "If I change files in a container, is the image changed?"

**No.** Container changes don't affect the image.

**Files in container:**
- `/workspace/*` - Mounted from host, persistent
- Everything else - Temporary, lost on removal

**To save changes to image:**
```bash
# Quick method (not recommended)
container retire my-project --save-changes

# Better method (reproducible)
# Edit Dockerfile, rebuild image
```

### "Why not just keep containers running?"

**Containers are meant to be ephemeral:**
- Resources freed immediately
- No stale state
- Clean start each time
- Industry best practice

**Your work is safe** - workspace files persist.

### "Do I need one image per container?"

**No!** One image can create many containers.

**Common pattern:**
```bash
# One image
image: ds01-12345/pytorch-thesis:latest

# Many containers (at different times)
container: thesis-experiment-1
container: thesis-experiment-2
container: thesis-baseline
```

All use the same image, different workspaces.

---

## The DS01 Workflow

### Initial Setup

```bash
# 1. Create project (creates Dockerfile)
project init my-thesis

# 2. Build image from Dockerfile
# (done automatically by project init)
# Creates: ds01-12345/my-thesis:latest
```

### Daily Use

```bash
# Morning: Create container from image
project launch my-thesis --open

# Work inside container...

# Evening: Remove container
exit
container retire my-thesis
```

**Image persists** - container is temporary.

### Modifying Environment

```bash
# Edit recipe
vim ~/workspace/my-thesis/Dockerfile

# Rebuild image
image-update my-thesis

# Recreate container
container retire my-thesis
project launch my-thesis
```

---

## Image Layers

**Images are built in layers:**

```dockerfile
FROM aime/pytorch:2.8.0-cuda12.4    # Layer 1: Base
RUN pip install pandas numpy         # Layer 2: Packages 1
RUN pip install transformers         # Layer 3: Packages 2
COPY config.yaml /etc/               # Layer 4: Config
```

**Benefits:**
- **Caching** - Unchanged layers reused (faster builds)
- **Sharing** - Multiple images share base layers (saves disk)
- **Efficiency** - Only changed layers rebuild

**Example rebuild:**
```bash
# Change Dockerfile: add datasets package
vim Dockerfile
# RUN pip install transformers datasets

# Rebuild
image-update my-project

# Only Layer 3 rebuilds
# Layers 1-2 reused from cache
```

---

## Practical Examples

### Example 1: Research Project

```bash
# Create project with CV packages
project init cv-research --type=cv

# Image created:
# ds01-12345/cv-research:latest
#   - PyTorch 2.8.0
#   - torchvision
#   - OpenCV
#   - Pillow

# Work for a week...
project launch cv-research --open
# (create, remove containers daily)

# Image unchanged all week
image-list
# ds01-12345/cv-research:latest (7 days old)
```

### Example 2: Adding Packages

```bash
# Realize you need transformers
vim ~/workspace/cv-research/Dockerfile
# Add: RUN pip install transformers

# Rebuild image
image-update cv-research

# New image replaces old
image-list
# ds01-12345/cv-research:latest (a few seconds old)

# Launch with new packages
project launch cv-research --open
import transformers  # Works!
```

### Example 3: Multiple Experiments

```bash
# One image
image-list
# ds01-12345/my-model:latest

# Many experiments from same image
project launch baseline --open
# Uses ds01-12345/my-model:latest

project launch improved --open
# Uses ds01-12345/my-model:latest

project launch ablation --open
# Uses ds01-12345/my-model:latest
```

---

## Images vs Containers: Quick Reference

| Feature | Image | Container |
|---------|-------|-----------|
| **What is it?** | Blueprint/recipe | Running instance |
| **Lifetime** | Permanent (until deleted) | Temporary (removed daily) |
| **Can modify?** | No (rebuild from Dockerfile) | Yes (but changes lost) |
| **Contains** | OS, packages, config | Image contents + your runtime changes |
| **Where stored** | Docker storage | Docker + workspace mount |
| **Command to create** | `image-create` | `project launch` |
| **Command to remove** | `image-delete` | `container retire` |

---

## Mental Models

### Model 1: Workstation

**Image** = Computer specification
- "Dell workstation with Ubuntu, CUDA, PyTorch"
- Blueprint for ordering more

**Container** = Actual workstation
- Physical machine you sit at
- Temporary (return at end of day)

### Model 2: Software Installation

**Image** = Installation media
- Windows installer DVD
- Can install multiple times

**Container** = Installed OS
- Running Windows on a machine
- Can reinstall anytime from media

### Model 3: Programming

**Image** = Class definition
```python
class DataScienceEnvironment:
    def __init__(self):
        self.os = "Ubuntu 22.04"
        self.cuda = "12.4"
        self.pytorch = "2.8.0"
```

**Container** = Class instance
```python
container1 = DataScienceEnvironment()
container2 = DataScienceEnvironment()
```

---

## Why Docker Uses This Model

**Reproducibility:**
- Image = exact specification
- Same image = same environment every time

**Efficiency:**
- Share images across users
- Reuse layers across images
- Fast container creation

**Isolation:**
- Each container independent
- Can't interfere with others
- Clean slate every time

**Scalability:**
- Create many containers from one image
- Automated deployment
- Cloud-native workflows

---

## Next Steps

**Understand why containers are temporary:**

→ [Ephemeral Container Model](ephemeral-containers.md)

**Learn where files are saved:**

→ [Workspaces and Persistence](workspaces-persistence.md)

**See DS01 in industry context:**

→ [Industry Parallels](../background/industry-parallels.md)

**Apply this knowledge:**

→ [Creating Projects](../guides/creating-projects.md)

→ [Custom Environments](../guides/custom-environments.md)
