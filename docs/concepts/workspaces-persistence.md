# Workspaces and Persistence

**Where your files live and what survives container removal.**

---

## The Golden Rule

**Save everything important to `/workspace/<project>/`**

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
/workspace/my-project/    ← Your files (permanent!)
├── code/
├── data/
├── models/
└── Dockerfile
```

**Maps to:** `~/workspace/my-project/` on the host

**Survives:** Container removal, system reboots, everything

---

## How It Works

Your workspace is "mounted" into the container:

```
Host Machine                Container
────────────                ─────────
~/workspace/my-project/ ←→ /workspace/my-project/
```

**Same files, different path.** Changes in one appear in the other.

---

## Common Scenarios

### Saving model checkpoints

**Wrong (files lost):**
```python
torch.save(model, 'checkpoint.pt')        # Saves to /root/
# or
torch.save(model, '/tmp/checkpoint.pt')   # Saves to /tmp/
```

**Right (files persist):**
```python
torch.save(model, '/workspace/my-project/models/checkpoint.pt')
```

### Downloading datasets

**Wrong (re-download every time):**
```bash
cd /tmp
wget https://example.com/data.tar.gz
```

**Right (download once):**
```bash
cd /workspace/my-project/data
wget https://example.com/data.tar.gz
```

### Running Jupyter

**Always start from workspace:**
```bash
cd /workspace/my-project
jupyter lab
```

Notebooks auto-save to the current directory.

---

## Checking Where You Are

```bash
# Where am I?
pwd
# /workspace/my-project ← Good
# /root ← Bad (temporary!)

# Is this file safe?
realpath my-file.txt
# /workspace/... ← Permanent
# /root/... ← Temporary
```

---

## Workspace Structure

Recommended layout:

```
~/workspace/my-project/
├── Dockerfile           # Environment definition
├── requirements.txt     # Python packages
├── README.md
├── .gitignore
├── data/                # Datasets
├── notebooks/           # Jupyter notebooks
├── src/                 # Source code
├── models/              # Saved checkpoints
└── results/             # Outputs, logs, plots
```

---

## Quick Reference

| Location | Inside Container | Permanent? | Use For |
|----------|-----------------|-----------|---------|
| `/workspace/` | Yes | **Yes** | All important work |
| `/root/` (home) | Yes | No | Temporary config |
| `/tmp/` | Yes | No | Scratch space |
| `~/workspace/` | Host only | **Yes** | Same as /workspace/ |

---

## Common Questions

**"Where did my files go?"**
> Check if they were in `/workspace/`. If not, they're gone with the container.

**"Can I access workspace outside the container?"**
> Yes. It's at `~/workspace/<project>/` on the host.

**"Can I share files between projects?"**
> Yes. All projects are in `~/workspace/`. You can symlink or reference paths.

**"How much space do I have?"**
> Check with `du -sh ~/workspace/*`

---

## Troubleshooting

### Files disappeared

```bash
# Were they in workspace?
ls /workspace/my-project/

# Or somewhere temporary?
# If temporary → they're gone
```

**Prevention:** Always `cd /workspace/my-project` before working.

### Workspace looks empty in container

```bash
# Check mount
ls /workspace/
mount | grep workspace

# If empty, restart container
exit
container retire my-project
project launch my-project
```

---

## Next Steps

- [Containers and Images](containers-and-images.md) - Why containers are temporary
- [Ephemeral Containers](ephemeral-containers.md) - The design philosophy
- [Creating Projects](../guides/creating-projects.md) - Set up a new project

**Want deeper understanding?** See [Workspaces & Persistence](../background/workspaces-and-persistence.md) in Educational Computing Context.
