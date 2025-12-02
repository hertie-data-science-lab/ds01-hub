# SSH Advanced

Advanced SSH configuration for DS01 access.

---

## SSH Config File

Create `~/.ssh/config` on your laptop:

```
Host ds01
    HostName ds01-server.example.com
    User your-username
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
```

Now connect with:
```bash
ssh ds01
```

---

## Key Management

### Generate Key

```bash
# Recommended: Ed25519
ssh-keygen -t ed25519 -C "your-email@example.com"

# Alternative: RSA
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

### Copy to DS01

```bash
ssh-copy-id user@ds01-server
```

Or manually:
```bash
cat ~/.ssh/id_ed25519.pub | ssh user@ds01-server "cat >> ~/.ssh/authorized_keys"
```

### Agent Forwarding

On your laptop:
```bash
# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Connect with forwarding
ssh -A user@ds01-server
```

This lets you use your local key for Git inside DS01.

---

## Port Forwarding (Tunnels)

### Jupyter

```bash
# Forward port 8888
ssh -L 8888:localhost:8888 user@ds01-server

# Access at http://localhost:8888
```

### TensorBoard

```bash
# Forward port 6006
ssh -L 6006:localhost:6006 user@ds01-server

# Access at http://localhost:6006
```

### Multiple Ports

```bash
ssh -L 8888:localhost:8888 -L 6006:localhost:6006 user@ds01-server
```

### In SSH Config

```
Host ds01
    HostName ds01-server.example.com
    User your-username
    LocalForward 8888 localhost:8888
    LocalForward 6006 localhost:6006
```

---

## Persistent Connections

### ControlMaster

Add to `~/.ssh/config`:

```
Host ds01
    HostName ds01-server.example.com
    User your-username
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

Create socket directory:
```bash
mkdir -p ~/.ssh/sockets
```

First connection is slow, subsequent connections are instant.

### Keep Alive

```
Host ds01
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

Prevents disconnection on idle.

---

## Multiplexing (tmux/screen)

### tmux on DS01

```bash
# Create session
tmux new -s work

# Detach: Ctrl+B, D

# List sessions
tmux ls

# Reattach
tmux attach -t work
```

### Disconnect-Safe Workflow

```bash
# Connect
ssh ds01

# Start tmux
tmux new -s training

# Run training
python train.py

# Detach (Ctrl+B, D)

# Disconnect SSH (safe to close laptop)

# Later, reconnect
ssh ds01
tmux attach -t training
```

---

## SCP and rsync

### Copy Files to DS01

```bash
# Single file
scp local-file.txt ds01:~/workspace/project/

# Directory
scp -r local-dir/ ds01:~/workspace/project/

# rsync (better for large transfers)
rsync -avz local-dir/ ds01:~/workspace/project/
```

### Copy Files from DS01

```bash
scp ds01:~/workspace/project/results.csv .
rsync -avz ds01:~/workspace/project/models/ ./models/
```

---

## VS Code Remote

### Setup

1. Install "Remote - SSH" extension
2. Open Command Palette (Cmd/Ctrl + Shift + P)
3. Select "Remote-SSH: Connect to Host"
4. Enter `user@ds01-server` or select from config

### Config for VS Code

```
Host ds01
    HostName ds01-server.example.com
    User your-username
    ForwardAgent yes
```

---

## Troubleshooting

### Connection Refused

```bash
# Check SSH is running
ssh -v user@ds01-server
```

### Permission Denied

```bash
# Check key permissions
ls -la ~/.ssh/
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# Test key
ssh -i ~/.ssh/id_ed25519 user@ds01-server
```

### Host Key Changed

```bash
# Remove old key (only if expected)
ssh-keygen -R ds01-server
```

### Slow Connection

Add to config:
```
Host ds01
    Compression yes
    TCPKeepAlive yes
```

---

## Security Best Practices

1. **Use Ed25519 keys** (more secure than RSA)
2. **Use passphrase** on keys
3. **Don't share private keys**
4. **Use agent forwarding** instead of copying keys to server
5. **Keep SSH config in ~/.ssh/** (proper permissions)

---

## See Also

- [Prerequisites](../getting-started/prerequisites.md)
- [Jupyter Setup](../guides/jupyter-setup.md)
- [VSCode Remote](../guides/vscode-remote.md)
