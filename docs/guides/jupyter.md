# Jupyter Notebooks

Run Jupyter notebooks on DS01 with GPU access.

---

## Two Ways to Use Jupyter

| Method | Best For | GPU Access | Setup Time |
|--------|----------|------------|------------|
| **Browser Jupyter Lab** | Full Jupyter experience, extensions | ✓ | 2 minutes |
| **VS Code Notebooks** | Integrated development, debugging | ✓ | 1 minute |

---
# Quick start

### Quick Start: Browser Jupyter Lab

```bash
# 1. Launch container
project launch my-project --open

# 2. Inside container: Start Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# 3. On laptop: Create SSH tunnel (new terminal)
ssh -L 8888:localhost:8888 ds01
# Without SSH keys: ssh -L 8888:localhost:8888 <student-id>@students.hertie-school.org@10.1.23.20

# 4. Open browser: http://localhost:8888
# Copy token from step 2
```

---

### Quick Start: VS Code Notebooks

```bash
# 1. Launch container
project launch my-project --background

# 2. In VS Code: Connect to DS01 (Remote-SSH extension)
# 3. Attach VS Code to running container (Dev Containers extension)
# 4. Open .ipynb file
# 5. Select kernel: /usr/bin/python (see below)
# 6. Start coding!
```

- → [Full VS Code setup guide](vscode-remote.md) | [Kernel selection details](vscode-remote.md#selecting-a-kernel)

---
# Detailed Walkthroughs:

### Browser Jupyter Lab (Detailed)

### Step 1: Launch Container

```bash
project launch my-project --open
```

**Make sure Jupyter is installed:**
```bash
# Inside container
pip list | grep jupyter

# If not installed
pip install jupyterlab
```

**Add to Dockerfile permanently:**
```dockerfile
RUN pip install jupyterlab ipywidgets
```

### Step 2: Start Jupyter

```bash
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

**Output:**
```
[I 2024-12-09 10:30:15.123 ServerApp] Jupyter Server 2.12.1 is running at:
[I 2024-12-09 10:30:15.123 ServerApp] http://localhost:8888/lab?token=abc123def456...
[I 2024-12-09 10:30:15.123 ServerApp]     http://127.0.0.1:8888/lab?token=abc123def456...
```

**Copy the token** (everything after `token=`).

**Keep this terminal open** - Jupyter runs in foreground.

### Step 3: SSH Tunnel from Laptop

**On your laptop** (new terminal):

```bash
ssh -L 8888:localhost:8888 ds01
# Without SSH keys: ssh -L 8888:localhost:8888 <student-id>@students.hertie-school.org@10.1.23.20
```

**What this does:** Forwards port 8888 from DS01 to your laptop.

**Keep this tunnel open** while using Jupyter.

### Step 4: Access in Browser

Open: **http://localhost:8888**

**First time:** Paste token when prompted.

**You're in!** Create notebooks, access GPU, work normally.

### Step 5: Verify GPU Access

**In a notebook cell:**
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
print(f"GPU name: {torch.cuda.get_device_name(0)}")
```

**Expected output:**
```
CUDA available: True
GPU count: 1
GPU name: NVIDIA A100-SXM4-40GB
```

**Monitor GPU:**
```python
!nvidia-smi
```

---

## Running Jupyter in Background

**Problem:** When you close terminal, Jupyter stops.

**Solutions:**

### Option 1: tmux (Recommended)

```bash
# Inside container: Start tmux session
tmux new -s jupyter

# Start Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# Detach: Press Ctrl+B, then D
# Jupyter keeps running!

# Exit container
exit

# Later: Reconnect
container-attach my-project
tmux attach -t jupyter
```

**Benefits:**
- Jupyter survives disconnect
- Easy to reattach
- Can see output

### Option 2: nohup

```bash
# Inside container
nohup jupyter lab --ip=0.0.0.0 --port=8888 --no-browser > jupyter.log 2>&1 &

# Get token
cat jupyter.log | grep token

# Exit container - Jupyter still running
exit
```

**To stop Jupyter later:**
```bash
pkill jupyter
```

### Option 3: Systemd Service (Advanced)

Create `~/jupyter.service` inside container:

```ini
[Unit]
Description=Jupyter Lab

[Service]
Type=simple
ExecStart=/usr/local/bin/jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
Restart=always

[Install]
WantedBy=default.target
```

Start with systemd (if enabled in container).

---

## Understanding Kernels in DS01

- Your container has one Python environment (containers provide complete isolation)
- Jupyter uses that environment as the kernel
- All packages installed in container are available
- **You don't need venv or conda** - the container IS your environment

→ See [Python Environments in Containers](../concepts/python-environments.md) for details

**Check available kernels:**
```bash
jupyter kernelspec list
```

**Example output:**
```
Available kernels:
  python3    /usr/local/share/jupyter/kernels/python3
```

**Install additional kernels (rare):**
```bash
# If you need multiple Python versions
python -m ipykernel install --user --name=python39 --display-name="Python 3.9"
```

**Most users:** One container = one environment = one kernel. Simple!

---

## VS Code Notebooks (Detailed)

### Setup

**1. Install VS Code extensions (on laptop):**
- Remote - SSH
- Jupyter
- Python

**2. Connect to DS01:**
```
VS Code → Remote Explorer → SSH → ds01-server
```

**3. Launch container:**
```bash
project launch my-project --background
```

**4. Attach VS Code to container:**
```
VS Code → Remote Explorer / Container Tools / Dev Containers → Attach
```

**5. Open notebook:**
```
File → Open → /workspace/my-project/notebooks/experiment.ipynb
```

**6. Select kernel:**
- Click "Select Kernel" (top right)
- Choose: Python 3.x in container

**7. Run cells!**

### Kernel Selection in VS Code

**When you open a notebook, VS Code asks for kernel:**

**Options shown:**
1. **Python 3.x (/usr/bin/python3)** ← Choose this (your container Python)
2. Python environments (if any)

**Choose the container Python** - it has your packages and GPU access.

**Verify GPU works:**
```python
import torch
torch.cuda.is_available()  # Should be True
```

---

## Jupyter Configuration

**Save settings in container:**

Create `~/.jupyter/jupyter_lab_config.py`:

```python
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True
c.ServerApp.token = ''  # Disable token (use only on trusted network)
```

**Then just run:**
```bash
jupyter lab
```

**Add to Dockerfile to persist:**
```dockerfile
RUN mkdir -p /root/.jupyter
COPY jupyter_lab_config.py /root/.jupyter/
```

---

## Password Authentication

**Instead of copying tokens:**

```bash
# Inside container
jupyter lab password

# Enter password (prompted)

# Start Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# Access via http://localhost:8888
# Login with password
```

**Password persists in container** - no need to set again.

**To persist across recreates, add to Dockerfile:**
```dockerfile
RUN jupyter lab password <<EOF
your-password-here
your-password-here
EOF
```

---

## Custom Ports

**If port 8888 is busy:**

```bash
# Use different port
jupyter lab --ip=0.0.0.0 --port=8889 --no-browser

# Update SSH tunnel
ssh -L 8889:localhost:8889 ds01
# Without SSH keys: ssh -L 8889:localhost:8889 <student-id>@students.hertie-school.org@10.1.23.20

# Access via http://localhost:8889
```

**Check what ports are in use:**
```bash
netstat -tuln | grep LISTEN
```

---

## Jupyter Extensions

**Install extensions:**

```bash
# Popular extensions
pip install jupyterlab-git
pip install jupyterlab-lsp python-lsp-server
pip install jupyterlab-execute-time

# Restart Jupyter to see them
```

**Via Jupyter UI:**
```
Settings → Enable Extension Manager
Extensions tab → Search → Install 
```

**Recommended extensions:**
- **jupyterlab-git** - Git integration in Jupyter
- **jupyterlab-lsp** - Code completion, linting
- **jupyterlab-execute-time** - Show cell execution time
- **jupyterlab-toc** - Table of contents
- **jupyterlab-system-monitor** - CPU/RAM/GPU monitoring

**Add to Dockerfile:**
```dockerfile
RUN pip install jupyterlab-git jupyterlab-lsp python-lsp-server
```

---

## Saving Your Work

**Notebooks auto-save** to `/workspace/notebooks/` - they persist across container recreates.

**Before retiring container:**
```bash
# Make sure notebooks are saved
jupyter notebook list

# Files are in /workspace? Safe to retire
exit
container retire my-project
```

---

## Common Workflows

### Exploratory Analysis

```bash
# Quick start
project launch analysis --open

# Start Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# On laptop: SSH tunnel
ssh -L 8888:localhost:8888 ds01

# Work in notebooks...

# Done for the day
exit
container retire analysis
```

### Long Training Run

```bash
# Launch in background
project launch training --background

# Start Jupyter with tmux
container-attach training
tmux new -s jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# In browser: Start training in notebook
# Detach tmux: Ctrl+B, D

# Training runs
exit

# Check progress
container-attach training
tmux attach -t jupyter
```

### Rapid Prototyping (VS Code)

```bash
# Launch container
project launch prototype --background

# In VS Code: Attach to container
# Open .ipynb files
# Iterate quickly with debugging

# Done
container retire prototype
```

---

## Troubleshooting

### Cannot Connect to Jupyter

**Checklist:**

1. **Is Jupyter running?**
   ```bash
   ps aux | grep jupyter
   ```

2. **Is SSH tunnel active?**
   ```bash
   # On laptop
   ps aux | grep "ssh.*8888"
   ```

3. **Correct port?**
   ```bash
   jupyter server list
   ```

4. **Firewall blocking?**
   ```bash
   # Try different port
   jupyter lab --port=8889
   ssh -L 8889:localhost:8889 ds01
   ```

### "Token Invalid" Error

**Get current token:**
```bash
jupyter server list
```

**Or set password:**
```bash
jupyter lab password
```

### Kernel Dies / Restarts

**Causes:**
1. Out of memory
2. GPU OOM
3. Segmentation fault in code

**Check:**
```bash
# Inside container
dmesg | tail
docker logs $(hostname)
```

**Reduce memory usage:**
```python
# Clear variables
del large_variable
import gc
gc.collect()

# Use smaller batch size
batch_size = 16  # Was 256
```

### Slow Notebook Performance

**Check GPU utilisation:**
```bash
nvidia-smi
```

**If GPU not used:**
```python
# Move model to GPU
device = torch.device("cuda")
model = model.to(device)
data = data.to(device)
```

### SSH Tunnel Disconnects

**Use autossh:**
```bash
# On laptop
autossh -M 0 -L 8888:localhost:8888 ds01
```

**Or create alias in `~/.ssh/config`:**
```
Host ds01-jupyter
    HostName 10.1.23.20
    User <student-id>@students.hertie-school.org
    LocalForward 8888 localhost:8888
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**Then:**
```bash
ssh ds01-jupyter
```

### Can't Install Packages in Notebook

**Temporary (current session only):**
```python
!pip install package-name
```

**Permanent (add to Dockerfile):**
```bash
# Exit Jupyter
# Edit Dockerfile
vim ~/workspace/my-project/Dockerfile

# Add: RUN pip install package-name
# Rebuild
image-update my-project

# Recreate container
container retire my-project
project launch my-project
```

---

## Best Practices: Save Checkpoints 
In case you loose ssh connection / container crashes. Remember: containers are disposable, your files in workspace are persistent. This way you persist progress.

```python
# In training notebook
if epoch % 5 == 0:
    torch.save(model.state_dict(), f'/workspace/models/checkpoint_{epoch}.pt')
```

---

## Next Steps

- → [VS Code Remote Guide](vscode-remote.md)
- → [Long-Running Jobs](long-running-jobs.md)
- → [Daily Workflow](../getting-started/daily-workflow.md)
- → [Containers and Images](../concepts/containers-and-images.md)
