# VS Code Remote Development

## Quick Start

1. Install **Remote - SSH** extension in VS Code
2. Connect to DS01: `Cmd+Shift+P` → "Remote-SSH: Connect to Host" → `ds01`
3. Open folder: File → Open Folder → `/home/your-username/workspace/project`

## SSH Configuration

Add to `~/.ssh/config` on your laptop:

```
Host ds01
    HostName ds01-server.edu
    User your-username
    IdentityFile ~/.ssh/id_ed25519
```

## Working with Containers

### Dev Containers Extension (Recommended)

1. Connect to DS01 via Remote-SSH first
2. Install "Dev Containers" extension
3. Command Palette → "Dev Containers: Attach to Running Container"
4. Select your container
5. VS Code reopens attached to the container

Now `code .` in the integrated terminal works normally.

## Running Notebooks in VS Code

When working inside containers:

**Kernel Selection:**
- Select the container's Python: `/usr/bin/python`
- The kernel uses packages installed in the container

**Installing Packages at Runtime:**
```python
# Use %pip (not !pip) for reliable installs
%pip install pandas matplotlib
```

**Troubleshooting:**
- "Kernel not found": Ensure you're attached to the container, not the host
- Packages not importing: Restart kernel after `%pip install`

## Tips

### Port Forwarding

- Jupyter running in container? VS Code auto-forwards ports
- Or manually: Ports tab → Forward Port

### Git Integration

- Works automatically if SSH keys are set up
- Can commit/push from VS Code

## See Also

- [SSH Setup](ssh-setup.md)
- [Daily Workflow](../guides/daily-workflow.md)
