# DS01 User Documentation

## Understand What's Here
**The [Index & Learning Paths](index.md) doc covers everything you need to navigate this repo**: incl documentations structure, reading paths, and section overviews.

> Documentation content ranges from practical basics of deploying a container, advanced scripting and automation patterns, all the way through to explanations of core CS concepts behind DS01's architecture, and bridges to parallel industry practices.

---

## Get Started in <30 Minutes

**Never used DS01 before, but want to dive right in with minimal setup overhead?** See [quickstart](quickstart.md)

> This walks you through everything: SSH keys, connecting from your laptop, and deploying your first containerised project - all with minimal fuss.

---

## Build a Daily Routine

**Already setup?** Here's how to use DS01


> Basic principle:
> - Containers = disposable
> - Images, `~/workspace` = persistent



Deploy containers to run computationally-expensive workloads

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

You can continue to work on computationally-**in**expensive tasks locally without a GPU, then spin up a new container when needed.

*A proper Git workflow is better practice than manually downloading/uploading files to ds01. Your files will be version controlled and accessible from any computer!*

---

## Essential Commands

> See [quick references](quick-reference.md) for more usage and [Command Reference directory](reference/commands/) for full usage.

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

## Understanding Key Concepts

**New to containerised workflows?** We've put together quick mental models for the core concepts you need to know:
- [Containers and Images](key-concepts/containers-and-images.md) - Understand the blueprint/instance distinction
- [Workspaces and Persistence](key-concepts/workspaces-persistence.md) - Where your files live
- [Ephemeral Containers](key-concepts/ephemeral-containers.md) - Why containers are temporary

See [Key Concepts Overview](key-concepts/) for all topics (~20 min read total).
