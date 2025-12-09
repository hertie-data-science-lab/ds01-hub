# 5-Minute Quickstart

Get from zero to working in <30 minutes.

---

## Step 1: Connect via SSH

From your laptop terminal:

```bash
ssh <student-id>@students.hertie-school.org@10.1.23.20
```

If you don't have SSH keys set up, you'll be prompted for your usual Hertie Microsoft password.

---

## Step 2: Run First-Time Setup

**Time:** ~20 minutes (incl initial image cache build)

**Interactive:** Just answer the prompts - it walks you through everything.

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
project-init
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
project-launch
```

This interactive GUI will: 
- Scan available projects
- Build an executable Docker image from the project's Dockerfile (or otherwise first define a Dockerfile)
- Deploy a container instance of the image onto a GPU/MIG
- Either attach the terminal to running container, or start in background

**Now you are have a fully deployed container!**

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
*NB: `/workspace` inside the container is your project directory on the host (`~/workspace/<project-name>/`). This is a bind mount; files you save here persist even after retiring the container.* 

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

When done working:

```bash
# Exit the container
exit
# This will prompt to retire container (freeing GPU for others) or keep it running in background

# If you keep it running, but later are finished with it:
container retire my-project
```

**Your files in `~/workspace/` persist (logs, checkpoints, code)** - the container is just the temporary computing environment.

---

## Future Routine

In cloud computing platforms such as Hertie's DS01, **containers should be treated as ephemeral**. 
- You deploy containers when you need to run a computationally-expensive job.
- By setting up git with a GitHub remote in `project-init`, you are able to quickly push and pull work to/from the server and back to your personal computer (better practice than manually downloading/uploading files!)
- This way, your files (code, models, logs, but also Dockerfile for reproducible environment) are version controlled and accessible from any computer.

**Containers (and to some extent images) should be considered disposable; dockerfiles and mounted directories are where your project progress is stored.**


```bash
# To run a specific job
project launch my-project 

# Work...

# When job completed
exit
container retire my-project
```

That's it!

---

## Next Steps

→ [Understand the daily workflow](getting-started/daily-workflow.md)

→ [Create additional projects](guides/creating-projects.md)

→ [Set up Jupyter notebooks](guides/jupyter-notebooks.md)

→ [Connect VS Code](guides/vscode-remote.md)

---

## Getting Help

Every command has built-in help:

```bash
<command> --help        # Quick reference
<command> --info        # Comprehensive reference
<command> --concepts    # Learn before running
<command> --guided      # Step-by-step mode
```

**Show all available commands:**
```bash
commands
```

**Check system status:**
```bash
dashboard
```

**See your resource limits:**
```bash
check-limits
```

Further Refs:
- → [First Container Guide](getting-started/first-container.md) for step-by-step
- → [Quick Reference](quick-reference.md) for all commands