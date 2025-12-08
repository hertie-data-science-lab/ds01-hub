# Project Commands

Commands for project initialization and setup.

---

## Quick Reference

```bash
# Create new project (wizard)
project init my-project

# Launch existing project (smart - builds image if needed)
project launch my-project

# Individual steps
dir-create my-project
git-init my-project
readme-create my-project
```

---

## Recommended Workflow

```bash
# One-time: Create project
project init my-thesis --type=cv

# Daily: Launch project
project launch my-thesis

# When done: Retire container
container retire my-thesis
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

## project-launch

**Launch container for existing project** (L4 wizard)

```bash
project-launch [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--guided` | Educational mode |
| `--open` | Start and enter terminal |
| `--background` | Start in background |
| `--rebuild` | Force rebuild image |

**Examples:**
```bash
project-launch              # Interactive (select from list)
project-launch my-thesis    # Launch specific project
project-launch my-thesis --open  # Launch and enter
```

**What it does:**
1. Shows menu of projects in `~/workspace/` (if no name given)
2. Checks if Docker image exists
3. If no image: runs `image-create` automatically
4. Runs `container-deploy` to start container

**Key difference from container-deploy:**
- `project-launch` = Smart (handles image creation automatically)
- `container-deploy` = Direct (requires image to exist)

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
