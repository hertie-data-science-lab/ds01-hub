# First-Time Setup

Complete onboarding for new DS01 users.

**Time:** 15-20 minutes

**What you'll do:** Set up SSH, create your first project, build a custom image, deploy a container.

---

## Prerequisites

**You need:**
- DS01 account (provided by your administrator)
- Terminal access (Terminal on Mac/Linux, PowerShell/WSL on Windows)
- Internet connection

**Don't have an account yet?** Contact your system administrator.

---

## Step 1: Connect via SSH

From your laptop terminal:

```bash
ssh your-username@ds01-server-address
```

**First time?** You may see:
```
The authenticity of host 'ds01-server' can't be established.
Are you sure you want to continue connecting (yes/no)?
```

Type `yes` and press Enter.

**Password:** Use the temporary password provided by your administrator.

---

## Step 2: Run Setup Wizard

Once connected to DS01, run:

```bash
user-setup
```

**What this does:**

1. **SSH Key Setup** - Creates keys for GitHub authentication
2. **Project Creation** - Sets up your first project workspace
3. **Image Build** - Builds a custom Docker image with your chosen framework
4. **Container Deploy** - Launches your first container with GPU
5. **VS Code Setup** - (Optional) Instructions for remote development

**Interactive:** The wizard asks questions and explains as it goes.

**Want more explanations?** Use guided mode:
```bash
user-setup --guided
```

---

## Step 3: Follow the Prompts

The wizard will ask you to make choices:

### 3.1 Project Name
```
What would you like to name your project?
```

**Example:** `my-thesis`, `research-2024`, `cv-experiments`

**Rules:**
- Lowercase letters, numbers, hyphens only
- No spaces
- Short and memorable

### 3.2 Framework Selection
```
Select a framework:
  1) PyTorch
  2) TensorFlow
  3) JAX
```

**Not sure?** Choose PyTorch (most popular for research).

**What this does:** Sets up your base environment with CUDA support.

### 3.3 Additional Packages
```
Common data science packages:
  [x] pandas, numpy, matplotlib
  [x] scikit-learn
  [ ] HuggingFace transformers
  [ ] OpenCV
```

**Tip:** You can always add more packages later with `image-update`.

### 3.4 GPU Request
```
Request GPU for initial deployment? [Y/n]:
```

**Recommended:** Say yes to verify GPU works.

**No GPUs available?** The system will let you know. You can deploy later with `project launch`.

---

## Step 4: Wait for Image Build

```
Building Docker image...
────────────────────────────────────────────────
  [Step 1/4] Downloading base image...
  [Step 2/4] Installing system packages...
  [Step 3/4] Installing Python packages...
  [Step 4/4] Configuring environment...
────────────────────────────────────────────────
✓ Build complete
```

**Time:** 5-10 minutes (depends on packages selected)

**Behind the scenes:** DS01 is creating a custom image with exactly the software you need.

---

## Step 5: You're Inside!

Once setup completes, you'll be inside your container:

```bash
user@my-thesis:/workspace$
```

**Verify GPU access:**
```bash
nvidia-smi
```

You should see GPU information with available memory.

**Check your environment:**
```bash
# Python version
python --version

# PyTorch (or TensorFlow)
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

---

## Step 6: Explore Your Workspace

```bash
# You're already in your workspace
pwd
# /workspace

# See what's here
ls -la
```

You'll see:
```
/workspace/
├── README.md           Your project documentation
├── Dockerfile          Defines your environment
├── requirements.txt    Python packages (optional)
├── .git/               Git repository
├── data/               For datasets
├── notebooks/          For Jupyter notebooks
├── src/                For Python code
└── models/             For saved models
```

**Everything here is permanent** - survives container removal.

---

## Step 7: Try It Out

**Start Python:**
```bash
python
```

```python
>>> import torch
>>> print(f"CUDA available: {torch.cuda.is_available()}")
>>> print(f"GPU count: {torch.cuda.device_count()}")
>>> quit()
```

**Or create a test file:**
```bash
echo 'print("Hello from DS01!")' > test.py
python test.py
```

---

## Step 8: Exit When Done

```bash
# Exit the container
exit
```

You're now back on the DS01 host machine (outside the container).

**Free the GPU:**
```bash
container retire my-thesis
```

**What just happened:**
- Container stopped and removed
- GPU freed for others
- **Your workspace files are safe** in `~/workspace/my-thesis/`

---

## Verification

Check that everything worked:

```bash
# Your workspace still exists on the host
ls ~/workspace/
# Should show: my-thesis/

# Your image exists
image-list
# Should show: ds01-username/my-thesis:latest

# No running containers (you retired it)
container-list
# Should be empty or show other projects
```

**All good!** You're ready to use DS01.

---

## Tomorrow: Daily Workflow

Now that setup is complete, your daily routine is simple:

```bash
# Morning - start working
project launch my-thesis --open

# Work on your research...

# Evening - done for the day
exit
container retire my-thesis
```

→ [Learn the daily workflow](daily-workflow.md)

---

## Optional: Set Up Development Tools

### Jupyter Notebooks
```bash
# Already done! Just run inside container:
jupyter lab --ip=0.0.0.0
```

→ [Jupyter setup guide](../guides/jupyter-notebooks.md)

### VS Code Remote
The setup wizard showed instructions. Lost them?

→ [VS Code remote guide](../guides/vscode-remote.md)

---

## Troubleshooting

### "Command not found: user-setup"

**Fix:**
```bash
/opt/ds01-infra/scripts/user/helpers/shell-setup
source ~/.bashrc
```

Then try `user-setup` again.

### "No GPUs available"

**What happened:** All GPUs currently in use.

**Options:**
1. **Wait and retry** - Check availability:
   ```bash
   dashboard
   ```

2. **Skip GPU for now** - Complete setup without deploying:
   ```bash
   user-setup
   # When asked "Deploy container now?", say no
   ```

   Deploy later when GPUs available:
   ```bash
   project launch my-thesis
   ```

3. **Join the queue**:
   ```bash
   gpu-queue join
   ```

### "Image build failed"

**Likely cause:** Network timeout or package unavailable.

**Fix:** Try again - builds are usually network issues:
```bash
project init my-thesis
# Rebuild the image
```

### More Help

→ [Troubleshooting guide](../troubleshooting/)

→ Run `ds01-health-check` for diagnostics

→ Contact your administrator

---

## What You Just Did

**Created:**
- ✓ SSH keys (`~/.ssh/id_ed25519`)
- ✓ Project workspace (`~/workspace/my-thesis/`)
- ✓ Git repository (with `.gitignore`, `README.md`)
- ✓ Custom Docker image (`ds01-username/my-thesis:latest`)
- ✓ Dockerfile (`~/workspace/my-thesis/Dockerfile`)

**Learned:**
- ✓ How to deploy containers
- ✓ How to work inside containers
- ✓ How to retire containers
- ✓ Where your files live

**Ready for:**
- Daily research workflow
- Creating additional projects
- Customizing environments
- Running experiments

---

## Next Steps

**Learn your daily workflow:** → [Daily Workflow](daily-workflow.md)

**Create more projects:** → [Creating Projects](../guides/creating-projects.md)

**Customize your environment:** → [Custom Environments](../guides/custom-environments.md)

**Set up Jupyter:** → [Jupyter Setup](../guides/jupyter-notebooks.md)

**Set up VS Code:** → [VS Code Remote](../guides/vscode-remote.md)
