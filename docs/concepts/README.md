# Key Concepts to Understand

**The essential mental models for using DS01 effectively.**

---

## What This Section Is

These docs explain the **DS01-specific concepts** you need to understand to work productively. They're concise, practical, and focused on "just enough theory" to use the system well.

**Read these when:**
- You want to understand DS01 before diving in
- Something confuses you while using the system
- You need a quick mental model for how things work

**Time investment:** 30-45 minutes total (or read individual topics as needed)

---

## Core Concepts

### 1. Containers and Images

**The most important concept in DS01.**

- [Containers and Images](containers-and-images.md)

**Quick version:** Images are blueprints (permanent). Containers are instances (temporary). Changing the blueprint doesn't change existing instances.

**Read this if:** You're confused about why packages disappear, or why you need to rebuild images.

### 2. Ephemeral Containers

**Why containers are temporary, and why that's good.**

- [Ephemeral Container Model](ephemeral-containers.md)

**Quick version:** Containers = temporary compute sessions. Workspace = permanent storage. Remove containers when done to free resources.

**Read this if:** You're worried about losing work, or confused about container lifecycle.

### 3. Workspaces and Persistence

**Where your files actually live.**

- [Workspaces and Persistence](workspaces-persistence.md)

**Quick version:** `/workspace/` is permanent (survives container removal). Everything else in the container is temporary.

**Read this if:** You've lost files, or want to understand what persists.

### 4. Python Environments

**Why you don't need venv/conda.**

- [Python Environments](python-environments.md)

**Quick version:** Containers ARE your Python environment. Each project gets isolated packages via its Docker image.

**Read this if:** You're wondering where to create virtual environments (answer: you don't).

---

## Quick Answers

**"Where did my files go?"**
> Files outside `/workspace/` are lost when container is removed. Always save to `/workspace/<project>/`.

**"Why did my packages disappear?"**
> Packages installed with `pip install` are temporary. Add them to your Dockerfile and rebuild the image.

**"Why rebuild the image?"**
> Images are blueprints. Changing your Dockerfile changes the blueprint, but existing containers still use the old blueprint.

**"Why remove containers?"**
> Frees GPU for others. Your workspace files are safe. Recreating containers takes ~30 seconds.

**"Do I need virtual environments?"**
> No. Containers provide isolation. Each project has its own container with its own packages.

---

## How These Differ from Background

| This Section (Concepts) | Background Section |
|------------------------|-------------------|
| DS01-specific | General computing |
| "What you need to know" | "Why things work this way" |
| Practical focus | Educational focus |
| 30-45 min total | 2-3 hours total |
| Use DS01 effectively | Understand the technology |

**Want deeper understanding?** See [Educational Computing Context](../background/).

---

## Reading Order

**Before first use (recommended):**
1. [Containers and Images](containers-and-images.md) - 10 min
2. [Workspaces and Persistence](workspaces-persistence.md) - 8 min

**After first week:**
3. [Ephemeral Containers](ephemeral-containers.md) - 10 min
4. [Python Environments](python-environments.md) - 5 min

**Or:** Just start using DS01 and come back here when confused.

---

## Next Steps

**Ready to use DS01?**
- [Quickstart](../quickstart.md)
- [First Container](../getting-started/first-container.md)

**Want deeper knowledge?**
- [Educational Computing Context](../background/) - Linux, Docker, servers, industry practices
