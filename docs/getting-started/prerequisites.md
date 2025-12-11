# Prerequisites

What you need before using DS01.

---

## Required

### 1. Hertie Email Account
- Username and password for SSH access

### 2. SSH Client
- **macOS:** Built-in terminal
- **Windows:** PowerShell, WSL, or PuTTY

### 3. Docker Group Membership
DSL administrator (currently Henry Baker) needs to have added you to the `docker` group.

**Check:**
```bash
groups | grep docker
```

If `docker` not shown, contact DSL administrator.

---

## Connecting

```bash
ssh <student-id>@students.hertie-school.org@10.1.23.20
```

You may see:
```
The authenticity of host 'ds01-server' can't be established.
Are you sure you want to continue connecting (yes/no)?
```

Type `yes` and press Enter.

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
Not in docker group. Contact DSL administrator.

### Commands not found
```bash
shell-setup
source ~/.bashrc
```

### Can't connect via SSH
- Check server address
- Check username
- Check network (VPN is required off-campus)

---

## Next Steps

- → [First Container](first-container.md) - Deploy in <30 minutes
