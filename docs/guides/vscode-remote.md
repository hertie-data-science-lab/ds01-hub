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

## Running Notebooks in VS Code

### Selecting a Kernel

When opening a notebook, VS Code prompts you to select a kernel:

1. Click "Select Kernel" or the kernel indicator in the top-right
2. Choose "Python Environments"
3. Select `/usr/bin/python` (Python 3.10.12)

> **Note:** You may see both `/usr/bin/python` and `/bin/python` listed - they're identical (symlinks). Either works.

### Container as Your Python Environment

**DS01 containers replace virtual environments.** The container provides complete isolation:

| Traditional Setup | DS01 Approach |
|-------------------|---------------|
| Create venv/conda env | Container provides isolation |
| `pip install` in venv | Packages installed at image build time |
| Activate environment | Just select the container's Python |

**You don't need to:**
- Create virtual environments inside containers
- Worry about environment activation
- Manage multiple Python versions

### Installing Additional Packages

**At image build time (recommended):**
- Use `image-create` to include packages in your image
- Packages persist across container restarts

**At runtime (temporary experiments):**
```python
# In notebook cell - use %pip (Jupyter magic), not !pip
%pip install package-name
```

> **Why `%pip`?** The `%pip` magic ensures the running kernel can find newly installed packages. Using `!pip` may require a kernel restart.

### Troubleshooting Notebooks

**"Module not found" after pip install:**
- If you used `!pip install`, restart the kernel
- Better: use `%pip install` next time

**Kernel won't connect:**
- Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"
- Check Jupyter output: `Ctrl+Shift+P` → "Jupyter: Show Output"

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

→ [SSH Setup](ssh-setup.md)
→ [Daily Usage Patterns](../guides/daily-workflow.md)
