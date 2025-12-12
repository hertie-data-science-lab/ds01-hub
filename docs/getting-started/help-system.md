# Using the Help System

DS01 commands have built-in help to guide you from beginner to expert.

---

## Four Help Modes

Every command supports **four help modes** - two for quick reference, two for learning:

| Flag | Type | When to Use | What You Get |
|------|------|-------------|--------------|
| `--help` or `-h` | **Quick Reference** | Know the command, need syntax | Usage, main options, examples |
| `--info` | **Full Reference** | Need all options | Complete documentation, all flags |
| `--concepts` | **Learn First** | New to this concept | Explains what something is before running |
| `--guided` | **Learn by Doing** | First time using command | Step-by-step with explanations |

---

## Quick Reference: `--help`

**When:** You know what the command does, just need the syntax.

**Example:**
```bash
container-deploy --help
```

**Shows:**
```
DS01 Container Deploy
L3 Orchestrator - Creates and starts containers in one command

Usage:
  container-deploy [name] [options]

Options:
  --guided          Show detailed explanations
  --background      Start without attaching
  --open            Start and open terminal
  -h, --help        Show this help

Examples:
  container-deploy                  # Interactive wizard
  container-deploy my-project       # Quick deploy
  container-deploy my-project --open
```

**Fast, concise, straight to the point.**

---

## Full Reference: `--info`

**When:** You need to see ALL options and detailed examples.

**Example:**
```bash
container-deploy --info
```

**Shows:**
- Complete option list
- All subcommands
- Multiple examples
- Advanced use cases
- Related commands

**Like a man page, but friendlier.**

---

## Learn the Concept: `--concepts`

**When:** You're new to containers, images, or DS01 concepts.

**Example:**
```bash
image-create --concepts
```

**Shows:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Understanding Docker Images
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What is a Docker Image?

An image is like a recipe for creating containers. It defines:
  • What software is installed (PyTorch, pandas, etc.)
  • What system libraries are included
  • How the environment is configured

Think of it as a snapshot of a configured system.

Container vs Image:
  Image     →  Recipe/Blueprint (stored, sharable)
  Container →  Running instance (temporary, for work)

You can create many containers from one image.

Why Images Matter:

1. Reproducibility - Same environment every time
2. Shareability - Give Dockerfile to colleagues
3. Version Control - Track changes in git
4. Efficiency - Rebuild containers instantly

[Press Enter to continue or Ctrl+C to exit]
```

**Read this BEFORE running the command** - builds understanding first.

---

## Learn by Doing: `--guided`

**When:** First time using a command or want explanations during execution.

**Example:**
```bash
image-create --guided
```

**What happens:**

### 1. Explains Before Each Choice

```
━━━ Framework Selection ━━━

PyTorch, TensorFlow, and JAX are deep learning frameworks.

PyTorch:
  • Most popular for research
  • Dynamic computation graphs
  • Great for experimentation

TensorFlow:
  • Industry standard for production
  • Static computation graphs
  • Extensive tooling

JAX:
  • Cutting-edge research
  • Fast on GPUs/TPUs
  • Functional programming style

Which framework do you want?
  1) PyTorch 2.8.0 (recommended for research)
  2) TensorFlow 2.16.1
  3) JAX 0.4.23

[Press Enter to see options]
```

### 2. Pauses for You to Read

```
Press Enter to continue...
```

Gives you time to understand before proceeding.

### 3. Shows What's Happening

```
Building Docker image...
────────────────────────────────────────────────
  [Step 1/4] Downloading PyTorch base image...
  [Step 2/4] Installing system packages...
  [Step 3/4] Installing Python packages...
  [Step 4/4] Configuring environment...
────────────────────────────────────────────────
```

### 4. Explains What Just Happened

```
━━━ What Just Happened? ━━━

Your Docker image was built with:
  • PyTorch 2.8.0 with CUDA 12.4
  • pandas, numpy, matplotlib
  • Jupyter Lab
  • Your custom packages

The image is stored as: ds01-username/my-project:latest

You can create containers from this image anytime with:
  project launch my-project
```

**Best for first-time users** - learn while doing.

---

## Interactive Mode (No Arguments)

**When:** You're not sure what arguments to provide.

**Just run the command without anything:**

```bash
# These all start interactive wizards
project init
container deploy
image create
```

**What happens:**
- Command asks questions
- Presents menus
- Guides you through options
- No need to memorise flags

**Example:**
```bash
container-deploy
```

**Shows:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DS01 Container Deploy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Select a project to deploy:

  1) my-thesis          (PyTorch 2.8.0)
  2) research-2024      (TensorFlow 2.16.1)
  3) experiments        (JAX 0.4.23)

Choice [1-3]:
```

**Friendly, menu-driven, no flags needed.**

---

## Quick Command Reference: `commands`

**See everything available:**

```bash
commands
```

**Shows:**
- All DS01 commands
- Organised by category
- Brief descriptions
- Common workflows

**Like a cheat sheet** - quick lookup of what's available.

---

## Combining Help Modes

### Pattern 1: Beginner Learning

```bash
# 1. Learn concept first
image-create --concepts

# 2. Run with guidance
image-create --guided

# 3. Second run: interactive
image-create

# 4. Later: Quick reference
image-create --help

# 5. Finally: experienced, run non-interactively as CLI
image-create my-project -f pytorch -t nlp
```
---

## Help for Subcommands

**Dispatchers have help too:**

```bash
# See all container commands
container help

# Help for specific subcommand
container deploy --help
container retire --help
```

**Also works:**
```bash
# Hyphenated form
container-deploy --help
```

Both formats are equivalent.