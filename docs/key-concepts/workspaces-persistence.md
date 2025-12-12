# Workspaces and Persistence

**Where your files live and what survives container removal.**

---

## The Golden Rule

**Save everything important to `/workspace/`**

Everything else in the container is temporary.

---

## Two Filesystems

When you work in a container, there are two places files can be:

### 1. Container filesystem (temporary)

```
/root/              ← Home directory (temporary!)
/tmp/               ← Temp files (temporary!)
/usr/, /opt/        ← From image (reset on recreate)
```

**Lost when:** Container is removed (`container retire`)

### 2. Workspace (permanent)

```
/workspace/               ← Your project files (permanent!)
├── code/
├── data/
├── models/
└── Dockerfile
```

**Maps to:** `~/workspace/<project>/` on the host

**Survives:** Container removal, system reboots, everything

---

## How It Works

Your project directory is "mounted" into the container as `/workspace`:

```
Host Machine                    Container
────────────                    ─────────
~/workspace/my-project/    ←→   /workspace/
```

**Same files, different path.** Changes in one appear in the other.

---

## Common Scenarios

### Saving model checkpoints

**Right (files persist):**
```python
torch.save(model, '/workspace/models/checkpoint.pt')
```

### Downloading datasets

**Right (download once):**
```bash
cd /workspace/data
wget https://example.com/data.tar.gz
```

### Running Jupyter

**Always start from workspace:**
```bash
cd /workspace
jupyter lab
```

---

## Quick Reference

| Location | Permanent? | Use For |
|----------|-----------|---------|
| `/workspace/` | **Yes** | All important work |
| `/root/` (home) | No | Temporary config |
| `/tmp/` | No | Scratch space |

---

## Common Questions

**"Where did my files go?"**
> Check if they were in `/workspace/`. If not, they're gone with the container.

**"Can I access workspace outside the container?"**
> Yes. It's at `~/workspace/<project>/` on the host.

**"How much space do I have?"**
> Check with `du -sh ~/workspace/*`

---

## Want Comprehensive Understanding?

This is a brief guide covering the essentials. For deeper exploration of:
- **Backup strategies and data safety**
- **Disk quota management**
- **Advanced mounting options**
- **Troubleshooting persistence issues**
- **Industry best practices**

See [Workspaces & Persistence](../background/workspaces-and-persistence.md) in Educational Computing Context (20 min read).

---

## Next Steps

- [Containers and Images](containers-and-images.md) - Why containers are temporary
- [Ephemeral Containers](ephemeral-containers.md) - The design philosophy
- [Creating Projects](../core-guides/creating-projects.md) - Set up a new project
