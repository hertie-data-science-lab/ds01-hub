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

# If you have a remote repo you wish to clone (otherwise project-init configures for you)
git clone your-repo

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

## Next Steps

See [Index & Learning Paths](index.md) for entry points, or jump right in:

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