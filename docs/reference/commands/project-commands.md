# Project Commands

Commands for project initialization and setup.

---

## Quick Reference

```bash
# Complete project setup (wizard)
project-init my-project

# Individual steps
dir-create my-project
git-init my-project
readme-create my-project
```

---

## project-init

**Complete project initialization** (L4 wizard)

```bash
project-init [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--guided` | Educational mode |

**Examples:**
```bash
project-init                # Interactive
project-init my-research    # Specify name
```

**What it does:**
1. `dir-create` - Creates `~/workspace/<project>/`
2. `git-init` - Initializes Git repository
3. `readme-create` - Generates README.md
4. `image-create` - Builds custom Docker image
5. `container-deploy` - Deploys first container

**Equivalent to running all steps individually.**

---

## dir-create

**Create workspace directory** (L2 atomic)

```bash
dir-create <project-name>
```

**Example:**
```bash
dir-create my-project
# Created: ~/workspace/my-project/
```

Creates standard directory structure:
```
~/workspace/my-project/
├── data/
├── notebooks/
├── src/
└── models/
```

---

## git-init

**Initialize Git repository** (L2 atomic)

```bash
git-init <project-name>
```

**Example:**
```bash
git-init my-project
# Creates ~/workspace/my-project/.git/
# Adds .gitignore for Python/data science
```

**Created .gitignore includes:**
- `__pycache__/`, `*.pyc`
- `.env`, `*.log`
- `data/`, `models/` (large files)
- `.ipynb_checkpoints/`

---

## readme-create

**Generate README.md** (L2 atomic)

```bash
readme-create <project-name>
```

**Example:**
```bash
readme-create my-project
# Generates ~/workspace/my-project/README.md
```

Creates a template README with sections for:
- Project description
- Setup instructions
- Usage examples
- License

---

## Workflow Example

### Using project-init (recommended)
```bash
project-init my-thesis
# Handles everything automatically
```

### Manual setup
```bash
dir-create my-thesis
git-init my-thesis
readme-create my-thesis
image-create my-thesis
container-deploy my-thesis --open
```

---

## Project Structure

After `project-init`:
```
~/workspace/my-project/
├── .git/              # Git repository
├── .gitignore         # Python/DS ignores
├── README.md          # Project documentation
├── data/              # Data files (gitignored)
├── notebooks/         # Jupyter notebooks
├── src/               # Source code
└── models/            # Saved models (gitignored)

~/dockerfiles/
└── my-project.Dockerfile  # Custom image definition
```

---

## See Also

- [Container Commands](container-commands.md)
- [Image Commands](image-commands.md)
- [Creating Projects Guide](../../guides/creating-projects.md)
