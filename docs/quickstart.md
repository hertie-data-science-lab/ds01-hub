# 30-Minute Quickstart

---

## Step 1: Connect via SSH

From your laptop terminal:

```bash
ssh <student-id>@students.hertie-school.org@10.1.23.20
```

If you don't have SSH keys set up, you'll be prompted for your usual Hertie Microsoft password.

---

## Step 2: Run First-Time Setup

Once connected, run:

```bash
user-setup
```

This interactive GUI will:
- Generate & configure SSH keys (for DS01 & GitHub)
- Configure VS Code (necessary extensions & auto-SSH)

--- 

Then run:

```bash
project-init --guided
```
This interactive GUI will: 
- Create your first project workspace 
- Setup best-practice DS directory structure
- Auto-build project docs (README.md, requirements.txt, Dockerfile, pyproject.toml)
- Initialise git 
- Build a custom Docker image1
- Deploy your first container

---

Then run:

```bash
project-launch --guided
```

This interactive GUI will: 
- Scan available projects
- Build an executable Docker image from the project's Dockerfile (or otherwise first define a Dockerfile)
- Deploy a container instance of the image onto a GPU/MIG
- Either attach the terminal to running container, or start in background

---

**You have successfully deployed a container!**

---

## Step 3: Start Working

After setup completes, you'll be inside a container. Check that GPU is available:

```bash
nvidia-smi
```

You should see GPU information. Now you can:

```bash
# Check Python
python --version

# Check PyTorch (or TensorFlow)
python -c "import torch; print(torch.cuda.is_available())"

# Navigate to your workspace (if not already)
cd /workspace

# Start running scripts in your project directory!
```
*NB: `/workspace` inside the container is your project directory on the host (`~/workspace/<project-name>/`). This is a bind mount; your files persist even after retiring the container.* 

---

### Step 3.5: Attach Terminal/IDE to Running Container

If you are comfortable with working from the terminal `project launch` will offer you the option to directly attach your terminal to the deployed container (or add `--open` flag to the launch command).

If you are more comfortable working in an IDE you will need the following 3 extensions in your IDE (here, presuming VS Code)
- SSH Remote
- Dev Containers 
- Container Tools 

Once installed: Cmd + Shift + P to open the Command Pallete, and type `Dev Containers: Attach to Running Container...`. This will open up a new window attached to the running container!

*NB: this ^^^ is all walked through by `user setup` CLI.*

## Step 4: Exit and Retire Container

When done with the current job:

```bash
# To exit the container from inside an attached terminal:
exit

# If you have a container running in background (terminal not attached):
container retire --guided
```
---

**That's it**. Files saved in `/workspace` are permanent.

---

## Daily Routine

**Containers = disposable; Images & `~/workspace` = persistent.**

- Deploy containers to run computationally-expensive jobs. 
- Retire containers when job is done.
- Regularly push/pull work between server-local computer: 
    - Configure a GitHub remote (automated in `project-init`) → quickly move files to/from the server/local computer 
    - Git workflow is better practice than manually downloading/uploading files to ds01!
    - Your files (code, models, logs, Dockerfiles) are version controlled and accessible from any computer.
    - You can work on computationally-cheap tasks locally, without the need for a GPU.

```bash
# To run a specific job
project launch my-project 

# Pull latest work from remote repo
git pull --rebase

# ... Work...

# Push progress back to remote repo
git add <files> 
git commit -m "commit message"
git push origin <branch>

# When job completed
container retire my-project
```

---

## Essential Commands

```bash
# Getting started
user setup              # First-time setup GUI (run once)
project init            # Project setup GUI (run for each new project)

# Daily workflow - Project-oriented (default)
project launch          # Start working (incl: image-create > container-deploy)
exit                    # Run inside container-attached terminal

# Daily workflow - Container-oriented (control)
image create            # Define a custom Dockerfile & build image executable
image update            # Add/remove pkgs in Dockerfile, rebuild image executable
container deploy        # Deploy container from existing image
container attach        # Attach terminal to running container
container retire        # Destroys container instance & frees GPU

# Status
container list          # Your containers
dashboard               # System status, GPU availability
check-limits            # Your current resource quotas

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

---

## Next Steps

**I want to...**

→ [Set up DS01 for the first time](getting-started/first-time.md) - Run `user setup`

→ [First Container Guide](getting-started/first-container.md) for step-by-step

→ [Understand the daily workflow](getting-started/daily-workflow.md) - Deploying & retiring containerised compute environments with ease

→ [Create additional projects](guides/creating-projects.md) - `project init`

→ [Build a custom environment](guides/custom-environments.md) - Add packages to your Dockerfile

→ [Set up Jupyter notebooks](guides/jupyter-notebooks.md) - JupyterLab setup

→ [Connect VS Code](guides/vscode-remote.md) - Connect your IDE

→ [Fix a problem](troubleshooting/) - Common errors and solutions

---

## Further Refs:

[Quick Reference](quick-reference.md) for all commands