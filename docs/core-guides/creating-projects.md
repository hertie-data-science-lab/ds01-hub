# Creating Projects

How to set up new data science projects on DS01.

---

## Quick Start

```bash
# Interactive wizard
project init

# Or specify name directly
project init my-new-project

# With framework type hint
project init my-thesis --type=rl
```

---

## What is a Project?

A project in DS01 includes:

**On disk:**
- Workspace directory (`~/workspace/my-project/`)
- Git repository
- requirements.txt (used to build the Dockerfile)
- Dockerfile (defines environment)
- README, .gitignore, directory structure

**In Docker:**
- Custom image (`ds01-username/my-project:latest`)
- Built from your Dockerfile
- Contains your chosen packages and tools

**The workflow:**
- Create project once (`project init`)
- Launch containers from it anytime (`project launch`)

---

## Interactive Mode (Recommended)

```bash
project init # also --guided (Guided Mode available)
```

**The GUI asks:**

### 1. Project Name
```
What would you like to name your project?
Example: my-thesis, research-2024, cv-experiments
```

**Rules:**
- Lowercase letters, numbers, hyphens
- No spaces or special characters
- Short and memorable

### 2. Project Type
```
Select project type:
  1) Machine Learning (general)
  2) Computer Vision (CV)
  3) Natural Language Processing (NLP)
  4) Reinforcement Learning (RL)
  5) Time Series Analysis
  6) Large Language Models (LLM)
  7) Custom
```

**What this does:** Pre-selects common packages for that domain.

Example: CV includes OpenCV, Pillow, torchvision

### 3. Framework
```
Select framework:
  1) PyTorch 2.8.0 (recommended for research)
  2) TensorFlow 2.16.1
  3) JAX 0.4.23
```

**Not sure?** Choose PyTorch.

### 4. Additional Packages
```
Common data science packages: [y/n]
  pandas, numpy, matplotlib, scipy

Jupyter Lab: [y/n]

Project-specific packages: [package names or Enter to skip]
```

**Tip:** You can add more packages later with `image-update`.

### 5. Build Image Now?
```
Build Docker image now? [Y/n]:
```

Initial build of cache takes 5-10 minutes but subsequent builds faster.

---

## Direct Mode (Faster)

**If you know what you want:**

```bash
# Create with defaults
project init my-thesis

# Specify type
project init my-thesis --type=cv

# Skip interactive questions
project init my-thesis --type=ml --quick
```

**Defaults:**
- Framework: PyTorch
- Packages: pandas, numpy, matplotlib, scikit-learn, jupyter
- Builds image automatically

---

## What Gets Created

After `project init my-thesis` completes:

### On DS01 Host

```
~/workspace/my-thesis/
├── Dockerfile              Environment definition
├── requirements.txt        Python packages (optional)
├── pyproject.toml          Project metadata
├── README.md               Project documentation
├── .git/                   Git repository
├── .gitignore              Ignore data, models, etc.
├── .gitattributes          Git LFS for large files
├── data/                   Datasets
├── notebooks/              Jupyter notebooks
├── src/                    Source code
├── tests/                  Unit tests
└── models/                 Saved models
```

### In Docker

```
Docker image: ds01-username/my-thesis:latest
```

Built from `Dockerfile`, includes:
- Base image with CUDA
- Framework (PyTorch/TensorFlow/JAX)
- Your selected packages
- Jupyter Lab (if selected)

---

## Editing the Dockerfile

**The Dockerfile lives in your project:**
```bash
vim ~/workspace/my-thesis/Dockerfile
```

**Example Dockerfile:**
```dockerfile
FROM aime/pytorch:2.8.0-cuda12.4

# Install additional packages
RUN pip install --no-cache-dir \
    transformers>=4.30.0 \
    datasets>=2.12.0 \
    accelerate>=0.20.0

# Install system packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Configure Jupyter (if needed)
RUN pip install jupyterlab ipywidgets

WORKDIR /workspace
```

**After editing:**
```bash
# Rebuild image after manual Dockerfile edit
image-update my-thesis --rebuild

# Recreate containers
project launch my-thesis
# Or
container-deploy my-thesis
```

> **Tip:** For simpler package management, use `image-update` (no arguments) to open the interactive GUI.

→ [Custom environments guide](custom-environments.md) for details

---

## Creating Multiple Projects

**You can have many projects:**

```bash
# Different research areas
project init thesis-cv --type=cv
project init thesis-nlp --type=nlp

# Different experiments
project init baseline-model
project init improved-model

# Teaching vs research
project init cs231n-homework
project init research-2024
```

**Each project has:**
- Own workspace directory
- Own Docker image
- Own git repository
- Own environment/packages

**Switching between projects:**
```bash
# Work on project A
project launch thesis-cv --open
# ... work ...
exit # keep running in background, or retire

# Switch to project B
project launch thesis-nlp --open
# ... work ...
exit # keep running in background, or retire
```

---

## Project Metadata (pyproject.toml)

**DS01 uses `pyproject.toml` for project metadata:**

```toml
[project]
name = "my-thesis"
description = "Computer vision thesis project"
version = "0.1.0"
authors = [{name = "Your Name", email = "you@example.com"}]

[tool.ds01]
type = "cv"
created = "2024-12-09"
author = "h_baker"
image = "ds01-12345/my-thesis:latest"
framework = "pytorch"
```

**Automatically created** during `project init`.

**Why this matters:**
- Tracks project metadata
- Stores image name for `project launch`
- Version-controlled with your code
- Python ecosystem standard

---

## Git Integration

**Projects automatically initialise git:**

```bash
cd ~/workspace/my-thesis

# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Initial project setup"
```

**Pre-configured `.gitignore`:**
```
# Ignore large files
data/
models/
*.pt
*.pth
*.h5
*.ckpt

# Ignore outputs
outputs/
__pycache__/
*.pyc
```

**Git LFS for large files:**
```
# Automatically configured for:
*.pt
*.pth
*.h5
*.safetensors
*.ckpt
*.bin
```

**Add remote (optional):**
```bash
cd ~/workspace/my-thesis
git remote add origin git@github.com:username/my-thesis.git
git push -u origin main
```

→ Requires SSH keys from `user-setup`

---

## Building Images Later

**Skipped image build during init?**

```bash
# Build it now
image-create my-thesis

# Or build when first launching
project launch my-thesis
# Detects missing image and offers to build
```

---

## Project Templates

**Different project types include different packages:**

*NB: this may change in future!!*

- **Machine Learning (General):** scikit-learn, xgboost, lightgbm, pandas, numpy, matplotlib, seaborn, plotly

- **Computer Vision**: torchvision, Pillow, OpenCV, albumentations (augmentation), timm (model zoo)

- **NLP:** transformers, datasets, tokenizers, sentencepiece,  spacy

- **Reinforcement Learning:** gym, stable-baselines3, tensorboard

- **Time Series:** statsmodels, prophet, pmdarima, tslearn

- **LLM:** transformers, accelerate, bitsandbytes, peft, flash-attention

- **Custom:** Only base packages; add your own in Dockerfile

---

## Troubleshooting

### "Project already exists"

```
Error: Directory ~/workspace/my-thesis already exists
```

**Fix:** Choose a different name or remove old project:
```bash
# Back up if needed
mv ~/workspace/my-thesis ~/workspace/my-thesis-old

# Then create new
project init my-thesis
```

### "Image build failed"

**Common causes:**
- Network timeout
- Package version conflict
- Invalid Dockerfile syntax

**Debug:**
```bash
# Check Dockerfile
cat ~/workspace/my-thesis/Dockerfile

# Try building manually
cd ~/workspace/my-thesis
docker build -t ds01-$(id -u)/my-thesis:latest .
```

### "Cannot push - no remote"

```bash
# Add GitHub remote first
cd ~/workspace/my-thesis
git remote add origin git@github.com:username/my-thesis.git
git push -u origin main
```

Requires SSH keys configured during `user-setup`.

---

## Best Practices

### 1. Meaningful Names
```bash
# Good
project init thesis-chapter3
project init baseline-resnet50
project init ablation-study

# Less helpful
project init project1
project init test
project init asdf
```

### 2. One Project Per Research Question
```bash
# Separate experiments
project init baseline-model
project init improved-model
project init final-model
```

Each has own environment, easier to track.

### 3. Version Control from Day 1
```bash
# Commit early and often
git add .
git commit -m "Initial setup"

git add train.py
git commit -m "Add training script"

git push
```

### 4. Document in README
```bash
# Edit README immediately
vim ~/workspace/my-thesis/README.md
```

Suggested to include:
- What this project does
- How to reproduce experiments
- Dataset locations
- Key results

### 5. Keep Dockerfiles Simple
```dockerfile
# Good - clear, minimal
RUN pip install transformers datasets

# Avoid - overly complex
RUN pip install transformers && \
    wget https://... && \
    tar -xzf ... && \
    cd ... && \
    python setup.py install && \
    ...
```

---

## Next Steps

**Launch your project:**
```bash
project launch my-thesis --open
```

- → [Custom Environments Guide](custom-environments.md)
- → [Jupyter Setup](jupyter-notebooks.md)
- → [VS Code Remote](vscode-remote.md)
- → [Containers and Images](../key-concepts/containers-and-images.md)
- → [Workspaces and Persistence](../key-concepts/workspaces-persistence.md)
