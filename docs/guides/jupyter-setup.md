# Jupyter Setup

Running Jupyter Lab in DS01 containers.

## Two Ways to Use Jupyter

| Method | Best For | Setup |
|--------|----------|-------|
| **VS Code Notebooks** | Quick editing, integrated workflow | Just open `.ipynb`, select kernel |
| **Browser Jupyter Lab** | Full Jupyter UI, extensions | Start server, SSH tunnel |

**Using VS Code?** See [VS Code Remote Guide](vscode-remote.md#running-notebooks-in-vs-code) - no server setup needed.

**Want browser-based Jupyter?** Continue below.

---

## Quick Start (Browser Jupyter Lab)

```bash
# 1. Deploy container
container-deploy my-project --open

# 2. Start Jupyter (inside container)
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# 3. On your laptop, create SSH tunnel
ssh -L 8888:localhost:8888 user@ds01-server

# 4. Open browser: http://localhost:8888
```

---

## Step by Step

### Step 1: Deploy Container

```bash
container-deploy my-project --open
```

### Step 2: Start Jupyter Lab

Inside the container:

```bash
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

You'll see output like:
```
    To access the server, open this file in a browser:
        file:///home/user/.local/share/jupyter/runtime/...
    Or copy and paste one of these URLs:
        http://localhost:8888/lab?token=abc123...
```

**Copy the token** (the part after `token=`).

### Step 3: Create SSH Tunnel

On your laptop (new terminal):

```bash
ssh -L 8888:localhost:8888 your-username@ds01-server
```

This forwards port 8888 from DS01 to your laptop.

### Step 4: Access Jupyter

Open browser: `http://localhost:8888`

Paste the token when prompted.

---

## Running in Background

To keep Jupyter running after you close the terminal:

### Option 1: nohup

```bash
nohup jupyter lab --ip=0.0.0.0 --port=8888 --no-browser > jupyter.log 2>&1 &

# View token
cat jupyter.log | grep token
```

### Option 2: tmux

```bash
tmux new -s jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
# Ctrl+B, D to detach
```

---

## Custom Port

If 8888 is in use:

```bash
# Use different port
jupyter lab --ip=0.0.0.0 --port=8889 --no-browser

# Tunnel that port
ssh -L 8889:localhost:8889 user@ds01-server

# Access
http://localhost:8889
```

---

## Password Authentication

Set up password instead of tokens:

```bash
# Inside container
jupyter lab password
# Enter password

# Now start without token
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

---

## Jupyter Configuration

Create `~/.jupyter/jupyter_lab_config.py`:

```python
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True
```

Then just run:
```bash
jupyter lab
```

---

## Installing Extensions

```bash
# Install extension
pip install jupyterlab-git

# Or via Jupyter
jupyter labextension install @jupyterlab/git
```

Common extensions:
- `jupyterlab-git` - Git integration
- `jupyterlab-lsp` - Language server
- `jupyterlab-execute-time` - Cell timing

---

## GPU in Notebooks

Verify GPU access:

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
```

Monitor GPU:
```python
!nvidia-smi
```

---

## Troubleshooting

### Can't Connect

1. Check Jupyter is running:
   ```bash
   ps aux | grep jupyter
   ```

2. Check SSH tunnel is active

3. Try different port:
   ```bash
   jupyter lab --port=8889
   ```

### Token Issues

Get token from running server:
```bash
jupyter server list
```

### Connection Reset

Restart Jupyter:
```bash
pkill jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

---

## See Also

- [VSCode Remote](vscode-remote.md)
- [Daily Workflow](daily-workflow.md)
- [SSH Advanced](../advanced/ssh-advanced.md)
