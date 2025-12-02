# Creating Projects

Step-by-step guide to starting new DS01 projects.

## Quick Start

```bash
# All-in-one wizard
project-init my-new-project
```

**What it does:**
1. Creates `~/workspace/my-new-project/`
2. Initializes Git repository
3. Generates README.md
4. Builds custom image
5. Deploys first container

## Manual Method

### 1. Create Workspace

```bash
mkdir -p ~/workspace/my-project
cd ~/workspace/my-project
```

### 2. Initialize Git

```bash
git init
cat > .gitignore << 'IGNORE'
__pycache__/
*.pyc
.ipynb_checkpoints/
data/
models/*.pt
.DS_Store
IGNORE
git add .gitignore
git commit -m "Initial commit"
```

### 3. Create Project Structure

```bash
mkdir -p {data,notebooks,src,models,results}
touch README.md requirements.txt
```

### 4. Build Image

```bash
image-create my-project
```

### 5. Deploy Container

```bash
container-deploy my-project --open
```

## Recommended Structure

```
my-project/
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── .gitignore             # Git exclusions
├── data/                  # Datasets
│   ├── raw/
│   └── processed/
├── notebooks/             # Jupyter notebooks
├── src/                   # Source code
│   ├── __init__.py
│   ├── data.py
│   ├── model.py
│   └── train.py
├── models/                # Trained models
├── results/               # Outputs
└── tests/                 # Unit tests
```

## Next Steps

→ [Daily Usage Patterns](daily-usage.md)
→ [Building Custom Images](custom-images.md)
