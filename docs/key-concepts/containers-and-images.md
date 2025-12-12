# Containers and Images

**The most important concept for using DS01 effectively.**

---

## The Key Insight

- **Image = Blueprint (permanent)**
- **Container = Instance (temporary)**

Changing the blueprint doesn't change existing instances.

---

## Quick Analogy

| Concept | Image | Container |
|---------|-------|-----------|
| Cooking | Recipe | Meal |
| Programming | Class | Object |
| Documents | Template | Document |

You can make many meals from one recipe. Changing the recipe doesn't change already-cooked meals.

---

## What This Means for You

### Why packages disappear

```bash
# Inside container
pip install transformers

# Later...
container retire my-project
project launch my-project

import transformers  # ModuleNotFoundError!
```

**Why?** The container was temporary. The image didn't change.

### How to make packages permanent

```bash
# Use the interactive package manager
image-update                  # Select image, add "transformers"

# Recreate container from new image
container retire my-project
project launch my-project

import transformers  # Works!
```

**Why?** Now the package is in the image (blueprint).

**Advanced:** Edit Dockerfile directly, then rebuild:
```bash
vim ~/workspace/my-project/Dockerfile
image-update my-project --rebuild
```

---

## The DS01 Workflow

```
┌─────────────┐
│  Dockerfile │  ← Edit this to change your environment
└──────┬──────┘
       │ image-create / image-update
       ▼
┌─────────────┐
│    Image    │  ← Blueprint (permanent)
└──────┬──────┘
       │ project launch / container deploy
       ▼
┌─────────────┐
│  Container  │  ← Instance (temporary)
└─────────────┘
```

**To change your environment:**
1. Run `image-update` (interactive GUI to add/remove packages)
2. Recreate container (`container retire` + `project launch`)

---

## Common Scenarios

### Adding a package

**Temporary (for testing):**
```bash
pip install new-package  # Works now, gone after retire
```

**Permanent (recommended):**
```bash
image-update                  # Interactive GUI to add packages
```

**Alternative:** If you prefer `requirements.txt`-based workflows, keep your `requirements.txt` as the single source of truth - `image-update` can import packages directly from it.

**Advanced:** Edit Dockerfile directly:
```bash
vim ~/workspace/my-project/Dockerfile
image-update my-project --rebuild
```

### Multiple projects

Each project gets its own:
- Dockerfile (in `~/workspace/<project>/Dockerfile`)
- Image (`ds01-<user>/<project>:latest`)
- Container (when deployed)

Different projects = different environments = no conflicts.

---

## Quick Reference

| What | Where | Permanent? |
|------|-------|-----------|
| Dockerfile | `~/workspace/<project>/Dockerfile` | Yes |
| Image | Docker storage | Yes (until deleted) |
| Container | Docker runtime | No (temporary) |
| Workspace files | `~/workspace/<project>/` | Yes |
| pip install | Container only | No |

---

## Common Questions

**"Can I modify an image directly?"**
> No. Use `image-update` to add packages, or edit the Dockerfile then rebuild.

**"Do changes in container affect the image?"**
> No. Container changes are isolated and temporary.

**"Why not just keep containers running forever?"**
> Resources (GPU) stay allocated. Other users can't use them. See [Ephemeral Containers](ephemeral-containers.md).

---

## Next Steps

- [Ephemeral Containers](ephemeral-containers.md) - Why containers are temporary
- [Workspaces and Persistence](workspaces-persistence.md) - Where files are saved
- [Custom Images Guide](../core-guides/custom-images.md) - Practical how-to

**Want deeper Docker knowledge?** See [Containers & Docker](../background/containers-and-docker.md) in Educational Computing Context.
