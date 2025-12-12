# System Commands

Commands for system status, user setup, and configuration.

---

## Quick Reference

```bash
# System dashboard
dashboard

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

## dashboard

**System status dashboard**

```bash
dashboard [SECTION] [OPTIONS]
```

View GPU availability, container status, and system resources.

**Options:**
| Option | Description |
|--------|-------------|
| `--watch`, `-w` | Watch mode (2s refresh) |
| `--full` | Show all sections expanded |
| `--json` | JSON output for scripting |

**Modular Sections:**
| Section | Description |
|---------|-------------|
| `gpu` | GPU/MIG utilization diagram |
| `cpu` | CPU usage by user diagram |
| `system` | CPU, Memory, Disk bars |
| `mig-config` | MIG partition configuration |
| `containers` | All containers with stats |
| `users` | Per-user resource summary |
| `temp` | GPU temperatures and power |

**Additional Views:**
| Command | Description |
|---------|-------------|
| `allocations [N]` | Recent N GPU allocations (default: 10) |
| `alerts` | Active alerts and warnings (idle containers, etc.) |

**Examples:**
```bash
dashboard                    # Default compact view (GPU, CPU by user, system)
dashboard --full             # All sections expanded
dashboard --watch            # Live monitoring
dashboard --json             # JSON output for scripting

# Individual sections
dashboard gpu                # GPU/MIG utilization
dashboard cpu                # CPU usage by user
dashboard system             # System resources
dashboard containers         # All containers
dashboard users              # Per-user summary
dashboard temp               # GPU temperatures

# Additional views
dashboard alerts             # Check for issues
dashboard allocations 20     # Last 20 GPU allocations
```

---

## user-setup

**Complete onboarding wizard** (L4 wizard)

```bash
user-setup [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--quick` | Expert mode: skip skill assessment, minimal prompts |

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

## ssh-config

**SSH configuration utility**

```bash
ssh-config <command>
```

**Commands:**
| Command | Description |
|---------|-------------|
| `generate` | Generate new SSH keys (ed25519) |
| `test` | Test SSH connection to localhost |
| `show` | Display public key and connection info |
| `vscode` | Show VS Code Remote-SSH setup instructions |

**Examples:**
```bash
ssh-config generate    # Create new SSH keys
ssh-config test        # Test if SSH is working
ssh-config show        # Display your public key
ssh-config vscode      # Get VS Code setup instructions
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
| `--guided` | Show detailed explanations for beginners |
| `--force` | Regenerate keys even if they exist |
| `--verify` | Just verify existing setup |

**Examples:**
```bash
ssh-setup              # Interactive setup
ssh-setup --guided     # With explanations
ssh-setup --verify     # Check existing setup
```

**What it does:**
1. Generates SSH key pair (ed25519)
2. Displays public key (add to GitHub/GitLab)
3. Verifies configuration

---

## vscode-setup

**Configure VSCode Remote** (L2 atomic)

```bash
vscode-setup [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--project=NAME` | Project-specific instructions |
| `--container=NAME` | Container-specific instructions |
| `--guided` | Educational mode |

**Examples:**
```bash
vscode-setup                        # General setup guide
vscode-setup --project=my-thesis    # Project-specific instructions
vscode-setup --guided               # With explanations
```

**See:** [VSCode Remote Guide](../../core-guides/vscode-remote.md)

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
| `--force` | Reconfigure even if PATH already correct |
| `--guided` | Educational mode |

**Examples:**
```bash
shell-setup --check   # Verify PATH
shell-setup           # Fix PATH
shell-setup --guided  # With explanations
```

**Use when:** DS01 commands not found in PATH

---

## jupyter-setup

**Configure Jupyter Lab access**

```bash
jupyter-setup [OPTIONS]
```

Configures Jupyter Lab access for the DS01 server.

**Options:**
| Option | Description |
|--------|-------------|
| `--guided` | Full setup with detailed explanations |
| `--port-forward` | Show SSH port forwarding commands only |
| `--brief` | Minimal output (for orchestrators) |

**Examples:**
```bash
jupyter-setup                 # Quick VS Code Jupyter extension setup
jupyter-setup --guided        # Full guided setup
jupyter-setup --port-forward  # Just port forwarding commands
```

**Use when:** Setting up Jupyter Lab access from your local machine.

---

## help

**Show all available commands**

```bash
help [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--atomic` | Show atomic container commands (advanced) |
| `--admin` | Show admin commands (ds01-* prefix) |
| `--inside` | Show inside-container commands |
| `--full` | Show everything |

**Alias:** `commands` (identical functionality)

**Examples:**
```bash
help              # Show main commands
help --atomic     # Show advanced L2 commands
help --admin      # Show admin tools
help --full       # Show all commands
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
