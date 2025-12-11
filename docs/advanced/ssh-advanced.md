# SSH Advanced

Advanced SSH configuration for DS01 access.

---

## SSH Config File

Create `~/.ssh/config` on your laptop:

```
Host ds01
    HostName 10.1.23.20
    User <student-id>@students.hertie-school.org
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
```

Now connect with:
```bash
ssh ds01
```

Without SSH config, use the full format:
```bash
ssh <student-id>@students.hertie-school.org@10.1.23.20
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
ssh-copy-id ds01
# Without SSH config: ssh-copy-id <student-id>@students.hertie-school.org@10.1.23.20
```

Or manually:
```bash
cat ~/.ssh/id_ed25519.pub | ssh ds01 "cat >> ~/.ssh/authorized_keys"
```

### Agent Forwarding

On your laptop:
```bash
# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Connect with forwarding
ssh -A ds01
```

This lets you use your local key for Git inside DS01.

---

## Port Forwarding (Tunnels)

### Jupyter

```bash
# Forward port 8888
ssh -L 8888:localhost:8888 ds01
# Without SSH keys: ssh -L 8888:localhost:8888 <student-id>@students.hertie-school.org@10.1.23.20

# Access at http://localhost:8888
```

### TensorBoard

```bash
# Forward port 6006
ssh -L 6006:localhost:6006 ds01

# Access at http://localhost:6006
```

### Multiple Ports

```bash
ssh -L 8888:localhost:8888 -L 6006:localhost:6006 ds01
```

### In SSH Config

```
Host ds01
    HostName 10.1.23.20
    User <student-id>@students.hertie-school.org
    LocalForward 8888 localhost:8888
    LocalForward 6006 localhost:6006
```

---

## Persistent Connections

### ControlMaster

Add to `~/.ssh/config`:

```
Host ds01
    HostName 10.1.23.20
    User <student-id>@students.hertie-school.org
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
    HostName 10.1.23.20
    User <student-id>@students.hertie-school.org
    ForwardAgent yes
```

---

## Troubleshooting

### Connection Refused

```bash
# Check SSH is running
ssh -v ds01
# Without SSH config: ssh -v <student-id>@students.hertie-school.org@10.1.23.20
```

### Permission Denied

```bash
# Check key permissions
ls -la ~/.ssh/
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# Test key
ssh -i ~/.ssh/id_ed25519 ds01
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
- [Jupyter Setup](../guides/jupyter.md)
- [VSCode Remote](../guides/vscode-remote.md)
