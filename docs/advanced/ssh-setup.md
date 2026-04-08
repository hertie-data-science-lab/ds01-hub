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
    HostName 10.1.23.20
    User <your-username>@hertie-school.lan
    IdentityFile ~/.ssh/id_ed25519
```

Replace `<your-username>` with your Hertie username (e.g. `212345` for students, `j.smith` for staff). Your email domain (e.g. `@students.hertie-school.org`, `@phd.hertie-school.org`) also works — it resolves to `@hertie-school.lan` automatically.

**Usage:**
```bash
ssh ds01  # Instead of the full format below
```

**Without SSH config:**
```bash
ssh <your-username>@hertie-school.lan@10.1.23.20
```

## Next Steps

- → [First-Time Setup](../getting-started/first-time-setup.md)
- → [VSCode Remote](vscode-remote.md)
