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

# Recreate container
project launch my-project

import transformers  # Works!
```

**Why?** Now the package is in the image (blueprint).

---

## The DS01 Workflow

```
┌─────────────┐
│  Dockerfile │  ← Edit this to change your environment
└──────┬──────┘
       │ image-update
       ▼
┌─────────────┐
│    Image    │  ← Blueprint (permanent)
└──────┬──────┘
       │ project launch
       ▼
┌─────────────┐
│  Container  │  ← Instance (temporary)
└─────────────┘
```

**To change your environment:** Run `image-update`, then recreate container.

---

## Quick Reference

| What | Where | Permanent? |
|------|-------|-----------|
| Dockerfile | `~/workspace/<project>/Dockerfile` | Yes |
| Image | Docker storage | Yes |
| Container | Docker runtime | No |
| Workspace files | `~/workspace/<project>/` | Yes |
| pip install in container | Container only | No |

---

## Common Questions

**"Can I modify an image directly?"**
> No. Use `image-update` to add packages.

**"Do changes in container affect the image?"**
> No. Container changes are isolated and temporary.

**"Why not just keep containers running forever?"**
> Resources (GPU) stay allocated. Other users can't use them. See [Ephemeral Containers](ephemeral-containers.md).

---

## Want Deeper Understanding?

For comprehensive explanation of:
- **How Docker layers work**
- **Image vs container architecture**
- **Advanced image management**
- **Industry Docker practices**

See [Containers & Docker](../background/containers-and-docker.md) in Educational Computing Context (20 min read).

---

## Next Steps

- [Ephemeral Containers](ephemeral-containers.md) - Why containers are temporary
- [Workspaces and Persistence](workspaces-persistence.md) - Where files are saved
- [Custom Images Guide](../core-guides/custom-images.md) - Practical how-to
