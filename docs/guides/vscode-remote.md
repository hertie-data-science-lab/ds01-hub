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
    HostName ds01-server.edu
    User your-username
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

**Option 1: SSH into container**

Add to `~/.ssh/config`:
```
Host ds01-container
    HostName ds01-server.edu
    User your-username
    RemoteCommand docker exec -it my-project._.your-username bash
    RequestTTY yes
```

**Option 2: Dev Containers extension**

- Install "Dev Containers" extension
- Use attach to running container

## Tips

### Python Extension

- Install Python extension on remote
- Select interpreter: `/opt/conda/bin/python`

### Git Integration

- Works automatically if SSH keys set up
- Can commit/push from VS Code

### Port Forwarding

- Jupyter running? VS Code auto-forwards ports
- Or manually: Ports tab → Forward Port

## Next Steps

→ [SSH Setup](ssh-setup.md)
→ [Daily Usage Patterns](../guides/daily-workflow.md)
