# Natural Language Dispatchers

DS01 supports natural language command syntax using dispatchers.

---

## Overview

Instead of hyphenated commands like `container-deploy`, you can use space-separated syntax:

```bash
container deploy my-project    # Same as container-deploy my-project
image create my-project        # Same as image-create my-project
```

Both syntaxes work identically and support all the same options.

---

## Why Both Syntaxes?

| Syntax | Best For |
|--------|----------|
| `container deploy` | Typing at terminal (feels natural) |
| `container-deploy` | Scripts, tab completion, muscle memory |

Both work identically - use whichever you prefer.

---

## Available Dispatchers

### container

Dispatch container lifecycle commands.

```bash
container <subcommand> [args] [options]
```

**Subcommands:**

| Subcommand | Equivalent | Description |
|------------|------------|-------------|
| `deploy` | `container-deploy` | Create + start container |
| `retire` | `container-retire` | Stop + remove + free GPU |
| `create` | `container-create` | Create container only |
| `start` | `container-start` | Start in background |
| `run` | `container-run` | Start and enter |
| `attach` | `container-attach` | Attach to running |
| `stop` | `container-stop` | Stop container |
| `remove` | `container-remove` | Remove container |
| `pause` | `container-pause` | Pause processes |
| `list` | `container-list` | List containers |
| `stats` | `container-stats` | Resource usage |
| `exit` | `container-exit` | Exit info |
| `help` | `container --help` | Show help |

**Examples:**
```bash
container deploy my-project --open
container list
container stats my-project
container retire my-project --force
```

---

### image

Dispatch image management commands.

```bash
image <subcommand> [args] [options]
```

**Subcommands:**

| Subcommand | Equivalent | Description |
|------------|------------|-------------|
| `create` | `image-create` | Build custom image |
| `update` | `image-update` | Rebuild image |
| `list` | `image-list` | List images |
| `delete` | `image-delete` | Remove image |
| `help` | `image --help` | Show help |

**Examples:**
```bash
image create my-project
image list
image update my-project --no-cache
image update my-project --add "pandas numpy"
```

---

### project

Dispatch project setup commands.

```bash
project <subcommand> [args] [options]
```

**Subcommands:**

| Subcommand | Equivalent | Description |
|------------|------------|-------------|
| `init` | `project-init` | Initialize new project |
| `help` | `project --help` | Show help |

**Examples:**
```bash
project init my-thesis
project init my-experiment --guided
```

---

### user

Dispatch user setup commands.

```bash
user <subcommand> [args] [options]
```

**Subcommands:**

| Subcommand | Equivalent | Description |
|------------|------------|-------------|
| `setup` | `user-setup` | Complete onboarding |
| `help` | `user --help` | Show help |

**Examples:**
```bash
user setup
user setup --guided
```

---

### check

Dispatch resource checking commands.

```bash
check <subcommand> [args]
```

**Subcommands:**

| Subcommand | Equivalent | Description |
|------------|------------|-------------|
| `limits` | `check-limits` | Show your resource limits and usage |
| `help` | `check --help` | Show help |

**Aliases:** `get limits` also works (routes to same command).

**Examples:**
```bash
check limits           # Show your resource limits and current usage
check-limits           # Same as above (hyphenated version)
```

---

## Getting Help

Each dispatcher shows available subcommands:

```bash
container help       # or: container --help
image help          # or: image --help
project help        # or: project --help
user help           # or: user --help
```

---

## See Also

- [Container Commands](container-commands.md) - Full container command reference
- [Image Commands](image-commands.md) - Full image command reference
- [Project Commands](project-commands.md) - Full project command reference
- [System Commands](system-commands.md) - System and user setup commands
