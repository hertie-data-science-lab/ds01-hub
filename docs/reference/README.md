# Reference

Quick lookup documentation for commands, limits, and system details.

---

## Commands

Organised by category:
- [Container Commands](commands/container-commands.md) - deploy, retire, list, stats, etc.
- [Image Commands](commands/image-commands.md) - create, list, update, delete
- [Project Commands](commands/project-commands.md) - project-init, dir-create, etc.
- [System Commands](commands/system-commands.md) - dashboard, health-check

## System Reference

- [Resource Limits](resource-limits.md) - Quotas, timeouts, user tiers
- [File Locations](file-locations.md) - Where things are stored
- [Glossary](glossary.md) - Key terms defined

---

## Quick Command Reference

```bash
# Container lifecycle
container-deploy my-project     # Create + start
container-retire my-project     # Stop + remove + free GPU
container-list                  # View your containers

# Images
image-create                    # Build custom image
image-list                      # View your images

# Status
ds01-dashboard                  # System overview
container-stats                 # Your resource usage
check-limits                    # Your quotas
```

For detailed options, see the command pages or run `<command> --help`.
