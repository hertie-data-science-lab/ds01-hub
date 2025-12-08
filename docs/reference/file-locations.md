# File Locations

Where things are stored on DS01.

---

## Your Files

### Workspace (Persistent)

```
~/workspace/
├── project-1/           # Project directory
│   ├── data/           # Data files
│   ├── notebooks/      # Jupyter notebooks
│   ├── src/            # Source code
│   └── models/         # Saved models
└── project-2/
    └── ...
```

**Inside container:** `/workspace/` maps to `~/workspace/<project>/`

### Dockerfiles

```
~/dockerfiles/
├── project-1.Dockerfile
└── project-2.Dockerfile
```

Custom image definitions. Edit these to change your environment.

---

## Mapping: Host ↔ Container

| Host Path | Container Path | Notes |
|-----------|---------------|-------|
| `~/workspace/my-project/` | `/workspace/` | Your files |
| `~/dockerfiles/` | (build only) | Image definitions |

**Important:** Only `/workspace` is mounted. Files outside `/workspace` in the container are temporary.

---

## DS01 System Paths

```
/opt/ds01-infra/                    # DS01 installation
├── scripts/user/                   # User commands
├── config/resource-limits.yaml     # System limits
└── docs-user/                     # User documentation

/var/lib/ds01/                      # State files
├── gpu-state.json                  # GPU allocations
└── container-metadata/             # Container tracking

/var/log/ds01/                      # Logs
├── events.jsonl                    # Event log
└── gpu-allocations.log            # GPU allocation history
```

---

## User Configuration

```
~/.ds01-limits                      # Your resource limits (read-only)
~/.bashrc                           # Shell configuration
~/.ssh/                            # SSH keys
```

---

## Container Internal Paths

Inside a container:

```
/workspace/                         # Your mounted workspace
/home/<user>/                       # User home (temporary)
/tmp/                              # Temporary files (temporary)
/opt/                              # Installed software
```

**Save important files to `/workspace`** - everything else is lost when container is removed.

---

## Docker Image Storage

```
/var/lib/docker/                    # Docker storage (system)
```

Your images are stored here automatically. Managed by Docker, not directly accessible.

---

## Quick Reference

| What | Where |
|------|-------|
| Your code | `~/workspace/<project>/` or `/workspace/` (in container) |
| Your Dockerfiles | `~/dockerfiles/` |
| Your limits | `~/.ds01-limits` |
| DS01 commands | `/opt/ds01-infra/scripts/user/` |
| Logs | `/var/log/ds01/` |

---

## See Also

- [Workspaces & Persistence](../background/workspaces-and-persistence.md)
- [Container Commands](commands/container-commands.md)
