# DS01 User Documentation

**→ [Index & Learning Paths](index.md)** - Documentation structure, reading paths, and section overview.

---

## Get Started in <30 Minutes

**Never used DS01 before?** See [quickstart](quickstart.md)

> This walks you through everything: SSH keys, connecting from your laptop, and deploying your first containerised project.

---

## Daily Routine

**Already setup?** Here's how to use DS01


> Basic principle:
> - Containers = disposable
> - Images, `~/workspace` = persistent



Deploy containers to run specific computationally-expensive jobs

```bash
project launch my-project
```

Pull your latest files from remote GitHub repo (automatically configured in `project-init`)

```bash
git pull --rebase
```

Regularly push/pull work between server-local computer as you work

```bash
git add <files>
git commit -m "commit message"
git push origin <branch>
```

Retire containers when job is done

```bash
container retire my-project
```

That's it!

You can continue to work on computationally-cheap tasks locally without a GPU, then spin up a new container when needed.

*A proper Git workflow is better practice than manually downloading/uploading files to ds01. Your files will be version controlled and accessible from any computer!*

---

## Essential Commands

> See [quick references](quick-reference.md) for full usage

```bash
# Getting started
user setup              # First-time setup GUI (run once)
project init            # Project setup GUI (run for each new project)

# Daily workflow - Project-oriented (default)
project launch          # Start working in a project (image-create -> container-deploy)
exit                    # Run inside container-attached terminal

# Daily workflow - Container-oriented (control)
image create            # Define custom Dockerfile, build image executable
image update            # Add/remove pkgs in Dockerfile, rebuild image executable
container deploy        # Deploy container from image
container retire        # Destroy container instance & free GPU

# Status
container list          # Your containers
dashboard               # System status, GPU availability

# Help
commands                # Full list of what you can do
home                    # Return to your workspace (`/home/<user-id/>)
```
---

## Getting Help

### Built-in help system:
- `<command> --help` - Quick reference
- `<command> --info` - Comprehensive usage documentation
- `<command> --concepts` - Explain concepts before running
- `<command> --guided` - Interactive mode with explanations

**Commands without arguments = interactive mode**
```bash
# These all open friendly GUIs
project init
container deploy
image create
```

**Additionally, use `--guided` while learning**
```bash
# Explains each step as it happens
project init --guided
container deploy --guided
```

**Examples:**
```bash
# New to containers? Learn first, then run
image-create --concepts
image-create --guided

# Just need syntax? Quick reference
container-deploy --help

# Want to learn how to skip interactive GUI? Understand full sub0command/flag structure
container-deploy --info
```

### Otherwise
1. Check [Troubleshooting](troubleshooting/)
2. Raise an issue ticket in [ds01-hub repo](https://github.com/hertie-data-science-lab/ds01-hub/issues)

---

## Cloud Computing Basic Concepts

**Containers = Temporary Work Sessions**
- Like turning on a laptop when you arrive, turning it off when you leave
- Create them when you need to do computationally-intensive work, remove them when you're done
- GPUs are allocated when container starts, freed when you retire it

**Workspaces = Your Permanent Storage**
- Everything in `~/workspace/` survives container removal
- Save your code, data, models (checkpoints & logs) here - they're always safe
- Think of it like files on your local computer

**Images = Recipes for Environments**
- Define what software is installed (PyTorch, pandas, etc.)
- Stored in Dockerfiles - version controlled, shareable, reproducible envs
- Dockerfiles are Single Source of Truth (STT) → stored in project dir & git repo
- Raw Dockerfiles > built into exectuable image files > deployed as container instances
- Rebuild containers from Dockerfiles anytime

**Why this model?**
- **Efficient**: GPUs freed immediately for others
- **Reproducible**: Same environment every time
- **Cloud-native**: Same workflow as AWS/GCP/Kubernetes
- **Flexible**: Multiple projects with different environments

→ [Learn more about containers](concepts/containers-and-images.md) *(optional)*
