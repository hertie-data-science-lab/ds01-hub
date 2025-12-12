# Project Commands

Commands for project initialisation and setup.

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

**Complete project initialisation** (L4 wizard)

```bash
project-init [project-name] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--type=TYPE` | Project type: ml, cv, nlp, rl, audio, ts, llm, custom |
| `--quick` | Skip interactive prompts, use defaults (type=ml) |
| `--no-git` | Skip Git initialization |
| `--guided` | Educational mode |

**Examples:**
```bash
project-init                      # Interactive
project-init my-research          # Specify name
project-init my-thesis --type=cv  # Computer vision project
project-init test --quick         # Quick setup with defaults
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
dir-create <project-name> [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--type=TYPE` | Structure type: data-science (default), blank |
| `--force` | Overwrite existing directory |
| `--guided` | Educational mode |

**Examples:**
```bash
dir-create my-project               # Create with data-science structure
dir-create my-project --type=blank  # Create empty directory
dir-create my-project --guided      # With explanations
```

Creates standard directory structure:
```
~/workspace/my-project/
├── data/{raw,processed,external}/
├── models/checkpoints/
├── notebooks/
├── scripts/
├── configs/
├── outputs/{logs,figures}/
└── tests/
```

---

## git-init

**Initialize Git repository** (L2 atomic)

```bash
git-init <project-name> [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--user=NAME` | Git user name (prompts if not set) |
| `--email=EMAIL` | Git user email (prompts if not set) |
| `--remote=URL` | Add remote repository URL |
| `--no-lfs` | Skip Git LFS setup |
| `--guided` | Educational mode |

**Examples:**
```bash
git-init my-project                           # Initialize Git
git-init my-project --user="Jane" --email="jane@example.com"
git-init my-project --remote=git@github.com:user/repo.git
git-init my-project --guided                  # With explanations
```

**Features:**
- Comprehensive ML/DS `.gitignore`
- Git LFS for large model files (`.pth`, `.pt`, `.h5`, `.ckpt`, `.bin`)
- User config setup
- Optional remote repository

---

## readme-create

**Generate README.md** (L2 atomic)

```bash
readme-create <project-name> [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--type=TYPE` | Project type: ml (default), cv, nlp, rl |
| `--desc="TEXT"` | Project description |
| `--structure=TYPE` | Structure: data-science (default), blank |
| `--commit` | Create initial Git commit (requires Git repo) |
| `--guided` | Educational mode |

**Examples:**
```bash
readme-create my-project                                # Basic README
readme-create cv-project --type=cv --desc="Image classification"
readme-create my-project --commit                       # Create and commit
readme-create my-project --guided                       # With explanations
```

Creates a template README with sections for project description, setup, usage, and license.

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
- [Creating Projects Guide](../../core-guides/creating-projects.md)
