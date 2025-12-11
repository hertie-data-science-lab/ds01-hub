# System Commands

Commands for system status, user setup, and configuration.

---

## Quick Reference

```bash
# System dashboard
dashboard                # Or: ds01-dashboard

# First-time setup
user-setup

# Check your limits
check-limits

# SSH and VSCode setup
ssh-setup
vscode-setup

# Help and info
help                     # List all commands
version                  # Show version
```

---

## ds01-dashboard

**System status dashboard**

```bash
ds01-dashboard [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--watch` | Continuous monitoring |
| `--json` | JSON output |

**Examples:**
```bash
ds01-dashboard           # View status
ds01-dashboard --watch   # Live monitoring
```

**Shows:**
- GPU availability and allocation
- System resource usage
- Active containers
- User quotas

---

## dashboard

**User-friendly system dashboard** (alias for ds01-dashboard)

```bash
dashboard [OPTIONS]
```

Same as `ds01-dashboard` but shorter to type.

**Options:**
| Option | Description |
|--------|-------------|
| `--watch`, `-w` | Continuous monitoring (2s refresh) |
| `--full` | Show all sections expanded |
| `--json` | JSON output for scripting |
| `gpu` | GPU/MIG utilisation only |
| `system` | System resources only |
| `containers` | Container list only |
| `users` | Per-user breakdown |

**Examples:**
```bash
dashboard              # Default view
dashboard --watch      # Live monitoring
dashboard gpu          # GPU section only
dashboard users        # User resource summary
```

---

## user-setup

**Complete onboarding wizard** (L4 wizard)

```bash
user-setup
```

**Aliases:** `user setup`, `new-user`

**What it does:**
1. `ssh-setup` - Creates SSH keys
2. `project-init` - Initializes first project
3. `vscode-setup` - Configures VSCode Remote (optional)

**Time:** 15-20 minutes

**See:** [First-Time Setup Guide](../../getting-started/first-time-setup.md)

---

## check-limits

**View your resource limits and usage**

```bash
check-limits
```

**Example output:**
```
=== Your Resource Limits ===
Max GPUs:       2
Max Containers: 3
Memory/Container: 64GB
Max Runtime:    24h (varies by user)
Idle Timeout:   0.5h (varies by user)

=== Current Usage ===
GPUs:       1 / 2
Containers: 2 / 3
```

---

## ssh-setup

**Configure SSH keys** (L2 atomic)

```bash
ssh-setup [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--key-type <type>` | Key type (default: ed25519) |
| `--no-passphrase` | Create without passphrase |

**Examples:**
```bash
ssh-setup                              # Interactive
ssh-setup --key-type ed25519           # Specify key type
```

**What it does:**
1. Generates SSH key pair
2. Displays public key (add to GitHub/GitLab)
3. Configures SSH agent (optional)

---

## vscode-setup

**Configure VSCode Remote** (L2 atomic)

```bash
vscode-setup
```

**Example:**
```bash
vscode-setup
# Generates VSCode config for remote development
```

**See:** [VSCode Remote Guide](../../guides/vscode-remote.md)

---

## shell-setup

**Fix PATH configuration**

```bash
shell-setup [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--check` | Verify PATH only |
| `--force` | Overwrite existing config |

**Examples:**
```bash
shell-setup --check   # Verify PATH
shell-setup           # Fix PATH
```

**Use when:** DS01 commands not found in PATH

---

## ds01-health-check

**System health diagnostics**

```bash
ds01-health-check
```

**Checks:**
- Docker daemon status
- GPU driver availability
- Systemd slices
- Network connectivity

**Use when:** Troubleshooting system issues

---

## gpu-queue

**GPU queue management**

```bash
gpu-queue [subcommand] [args]
```

**Subcommands:**
| Command | Description |
|---------|-------------|
| `position <user>` | Check queue position for user |
| `status` | View overall queue status |
| `list` | List all queued requests |

**Examples:**
```bash
gpu-queue position $USER   # Check your queue position
gpu-queue status           # View queue status
```

**Use when:** All GPUs are allocated and you're waiting for availability.

---

## help

**Show all available commands**

```bash
help
```

Lists all DS01 commands organised by category (containers, images, system, etc.).

**Alias:** `commands` (identical functionality)

**Example:**
```bash
help
# Shows categorised list of all DS01 commands
```

---

## version

**Show DS01 version information**

```bash
version
```

Displays the current DS01 infrastructure version and build information.

---

## Getting Help

### Command Help
All commands support `--help`:
```bash
container-deploy --help
image-create --help
```

### Guided Mode
Most commands support `--guided`:
```bash
container-deploy my-project --guided
image-create --guided
```

**Guided mode:**
- Explains each step
- Educational prompts
- Recommended for beginners

---

## Environment Variables

### DS01 Variables
```bash
DS01_LIMITS_FILE=~/.ds01-limits
DS01_INSTALL_DIR=/opt/ds01-infra
DS01_WORKSPACE=~/workspace
```

### Docker Variables
```bash
DOCKER_HOST=unix:///var/run/docker.sock
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Resource unavailable (no GPUs, quota exceeded) |
| 4 | Container/image not found |
| 5 | Permission denied |

**Check exit code:**
```bash
container-deploy my-project
echo $?
```

---

## See Also

- [Container Commands](container-commands.md)
- [Getting Started](../../getting-started/)
- [Troubleshooting](../../troubleshooting/)
