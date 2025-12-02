# SSH Setup

Configuring SSH keys for Git and remote access.

## Generate SSH Key

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
```

## Add to GitHub/GitLab

```bash
# Display public key
cat ~/.ssh/id_ed25519.pub

# Copy the output
```

**GitHub:**
- Settings → SSH and GPG keys → New SSH key
- Paste and save

**GitLab:**
- Preferences → SSH Keys
- Paste and save

## Test Connection

```bash
# GitHub
ssh -T git@github.com

# GitLab
ssh -T git@gitlab.com
```

## SSH Config

Create `~/.ssh/config`:
```
Host ds01
    HostName ds01-server.edu
    User your-username
    IdentityFile ~/.ssh/id_ed25519
```

**Usage:**
```bash
ssh ds01  # Instead of ssh user@ds01-server.edu
```

## Next Steps

→ [First-Time Setup](../getting-started/first-time-setup.md)
→ [VSCode Remote](vscode-remote.md)
