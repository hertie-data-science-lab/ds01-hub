# Prerequisites

What you need before using DS01.

---

## Required

### 1. DS01 Account
- Provided by your administrator
- Username and password for SSH access

### 2. SSH Client
- **macOS/Linux:** Built-in terminal
- **Windows:** PowerShell, WSL, or PuTTY

### 3. Docker Group Membership
Your administrator should have added you to the `docker` group.

**Check:**
```bash
groups | grep docker
```

If `docker` not shown, contact your administrator.

---

## Connecting

```bash
ssh your-username@ds01-server
```

Replace `ds01-server` with the actual server address provided by your administrator.

---

## First Time?

After connecting, run:
```bash
user-setup
```

This walks you through complete setup including SSH keys and your first project.

---

## Verify Setup

```bash
# Check Docker access
docker ps

# Check DS01 commands
container-list

# Check your limits
check-limits
```

---

## Troubleshooting

### "Permission denied" for Docker
Not in docker group. Contact administrator.

### Commands not found
```bash
shell-setup
source ~/.bashrc
```

### Can't connect via SSH
- Check server address
- Check username
- Check network (VPN if required)

---

## Next Steps

→ [First Container](first-container.md) - Deploy in 5 minutes
