# Workspaces and Persistence

**Where your files live and what survives container removal.**

---

## The Golden Rule

**Save everything important to `/workspace/`**

Everything else in the container is temporary.

---

## Two Filesystems

> NB: DS01 automatically mounts the project dir as its `workspace/` and then opens up at that location, so you do not nee to worry too much about managing this distinction!

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
├── Dockerfile
└── requirements.txt
```

**Maps to:** `~/workspace/<container-name>/` on the host

**Survives:** Container removal, system reboots, everything

> **Why project-specific?** DS01 containers are designed to be project-associated. Each container maps to one project directory. This keeps projects isolated and encourages good organisation. If you need different behaviour, use the `--workspace` flag (see below).

---

## How It Works

Your project directory is "mounted" into the container as `/workspace`:

```
Host Machine                    Container
────────────                    ─────────
~/workspace/my-project/    ←→   /workspace/
```

**Same files, different path.** Changes in one appear in the other.

This means when you're inside a container called `my-project`:
- `/workspace/train.py` in the container = `~/workspace/my-project/train.py` on the host
- `/workspace/data/` in the container = `~/workspace/my-project/data/` on the host

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
torch.save(model, '/workspace/models/checkpoint.pt')
```

### Downloading datasets

**Wrong (re-download every time):**
```bash
cd /tmp
wget https://example.com/data.tar.gz
```

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

Notebooks auto-save to the current directory.

---

## Checking Where You Are

```bash
# Where am I?
pwd
# /workspace ← Good
# /root ← Bad (temporary!)

# Is this file safe?
realpath my-file.txt
# /workspace/... ← Permanent
# /root/... ← Temporary
```

---

## Workspace Structure

Recommended layout for your project (shown as seen on the host):

```
~/workspace/my-project/       # On host (= /workspace/ inside container)
├── Dockerfile                # Environment definition
├── requirements.txt          # Python packages
├── README.md
├── .gitignore
├── data/                     # Datasets
├── notebooks/                # Jupyter notebooks
├── src/                      # Source code
├── models/                   # Saved checkpoints
└── results/                  # Outputs, logs, plots
```

---

## Quick Reference

| Location | Inside Container | Permanent? | Use For |
|----------|-----------------|-----------|---------|
| `/workspace/` | Yes | **Yes** | All important work |
| `/root/` (home) | Yes | No | Temporary config |
| `/tmp/` | Yes | No | Scratch space |
| `~/workspace/<project>/` | Host only | **Yes** | Maps to /workspace/ in container |

---

## Common Questions

**"Where did my files go?"**
> Check if they were in `/workspace/`. If not, they're gone with the container.

**"Can I access workspace outside the container?"**
> Yes. It's at `~/workspace/<project>/` on the host.

**"Can I share files between projects?"**
> Yes. Use the `--workspace` flag to mount a different directory, or access other projects via symlinks.

**"Can I mount my entire ~/workspace/ instead of one project?"**
> Yes. Use `container-create my-container --workspace ~/workspace` to mount all projects at once.

**"How much space do I have?"**
> Check with `du -sh ~/workspace/*`

---

## Troubleshooting

### Files disappeared

```bash
# Were they in workspace?
ls /workspace/

# Or somewhere temporary?
# If temporary → they're gone
```

**Prevention:** Always `cd /workspace` before working.

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
- [Creating Projects](../core-guides/creating-projects.md) - Set up a new project

**Want deeper understanding?** See [Workspaces & Persistence](../background/workspaces-and-persistence.md) in Educational Computing Context.
