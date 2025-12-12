# VSCode Remote Development

Setting up VSCode for remote development on DS01.

## Prerequisites

- VS Code installed locally
- Remote-SSH extension
- SSH key configured

## Setup

### 1. Install Extension

- Open VS Code
- Extensions → Search "Remote - SSH"
- Install "Remote - SSH" by Microsoft

### 2. Configure SSH

Add to `~/.ssh/config` (on your laptop):
```
Host ds01
    HostName 10.1.23.20
    User <student-id>@students.hertie-school.org
    IdentityFile ~/.ssh/id_ed25519
```

### 3. Connect

- VS Code: Command Palette (Cmd+Shift+P or Ctrl+Shift+P)
- "Remote-SSH: Connect to Host"
- Select "ds01"

### 4. Open Workspace

- File → Open Folder
- Navigate to `/home/your-username/workspace/my-project`

## Working with Containers

> **⚠️ Container must be running first.** Start your container via terminal before connecting:
> ```bash
> ssh ds01
> container-deploy <project-name> --background
> ```

**Option 1: SSH into container**

Add to `~/.ssh/config`:
```
Host ds01-container
    HostName 10.1.23.20
    User <student-id>@students.hertie-school.org
    RemoteCommand docker exec -it <project-name>._.<user-id> bash
    RequestTTY yes
```

Replace `<project-name>` and `<user-id>` with your actual values (e.g., `my-thesis._.12345`).

**Option 2: Dev Containers extension**

- Install "Dev Containers" extension
- Use attach to running container

## Running Notebooks in VS Code

### Selecting a Kernel

When opening a notebook, VS Code prompts you to select a kernel:

1. Click "Select Kernel" or the kernel indicator in the top-right
2. Choose "Python Environments"
3. Select `/usr/bin/python` (Python 3.10.12)

> **Note:** You may see both `/usr/bin/python` and `/bin/python` listed - they're identical (symlinks). Either works.

### Python Environment

**DS01 containers replace virtual environments** - you don't need venv or conda inside containers.

For details on installing packages and environment management:
- → [Python Environments in Containers](../key-concepts/python-environments.md)

---

## Tips

### Python Extension

- Install Python extension on remote
- Select interpreter: `/usr/bin/python`

### Git Integration

- Works automatically if SSH keys set up
- Can commit/push from VS Code

### Port Forwarding

- Jupyter running? VS Code auto-forwards ports
- Or manually: Ports tab → Forward Port

## Next Steps

- → [SSH Setup](ssh-setup.md)
- → [Daily Usage Patterns](../core-guides/daily-workflow.md)
