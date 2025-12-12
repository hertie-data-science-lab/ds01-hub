# Python Environments in Containers

**Why you don't need venv/conda in DS01.**

---

## The Key Insight

**DS01 containers ARE your Python environment.**

Each container provides complete isolation - you don't need venv, conda, or virtualenv inside containers.

---

## Containers vs Virtual Environments

| Traditional Setup | DS01 Approach |
|-------------------|---------------|
| Create venv/conda env | Container provides isolation |
| `pip install` in venv | Packages installed at image build time |
| Activate environment | Just select the container's Python |
| Manage multiple Python versions | Each project has its own container/image |
| requirements.txt + manual setup | Dockerfile defines everything |

---

## What You DON'T Need

**Inside DS01 containers, you don't need to:**

- **Create virtual environments (`python -m venv`):** The container itself is your isolated environment. There's no system Python to protect, no other projects to conflict with. Every package you install affects only this container.

- **Use conda environments (`conda create`):** Conda's main value is managing Python versions and compiled dependencies. Your container already has a specific Python version and pre-compiled CUDA libraries. Adding conda just adds complexity.

- **Worry about environment activation:** No `source venv/bin/activate`, no `conda activate myenv`. When you enter a container, you're already in the environment. `python` just works.

- **Manage multiple Python versions:** Your image specifies the Python version. Different project needs Python 3.10 while another needs 3.11? Different images, different containers. No pyenv, no version conflicts.

- **Deal with PATH issues:** No more "which python am I using?" confusion. The container has one Python at `/usr/bin/python`. Your packages are in the system site-packages. Everything is where you expect it.

---

## Installing Packages

### At Image Build Time (Recommended)

Use the interactive package manager:

```bash
image-update                  # Select image, add packages
container-deploy
```

**Advanced:** Edit Dockerfile directly:
```bash
vim ~/workspace/<project-name>/Dockerfile
# Add: RUN pip install transformers datasets torch
image-update <project-name> --rebuild
```

**Benefits:**

- **Packages persist across container restarts:** When packages are baked into the image, they're there every time you deploy a new container. No reinstalling transformers for the 50th time.

- **Reproducible environment:** Your Dockerfile is a complete specification. Run `image-create` on any machine with Docker and you get the identical environment - same Python version, same package versions, same CUDA setup.

- **Fast container startup:** Packages are already installed in the image. Container deployment takes 30 seconds, not 10 minutes of `pip install`. You're working immediately.

### At Runtime (Temporary)

For quick experiments:

```bash
# Inside container
pip install package-name
```

Or in Jupyter notebooks:

```python
# Use %pip (Jupyter magic), not !pip
%pip install package-name
```

> **Why `%pip`?** The `%pip` magic ensures the running kernel can find newly installed packages. Using `!pip` may require a kernel restart.

**Note:** Runtime installs are lost when container is removed. Add frequently-used packages to your Dockerfile.

> `container retire` offers you the option to write newly-installed pkgs back into the image. This is only a half-way house, as the underlying Dockerfile remains unchanged. 
---

## Selecting Python in VS Code

When working with notebooks in VS Code:

1. Click "Select Kernel" or the kernel indicator
2. Choose "Python Environments"
3. Select `/usr/bin/python`

> **Note:** You may see both `/usr/bin/python` and `/bin/python` listed - they're identical (symlinks). Either works.

---

## Troubleshooting

### "Module not found" after pip install

**In Jupyter:**
- If you used `!pip install`, restart the kernel
- Better: use `%pip install` next time

**In terminal:**
- Verify you're inside the container, not on the host
- Check with `which python` - should be `/usr/bin/python`

### Package installed but not importable

**Check you're in the right environment:**
```bash
# Inside container
which python    # Should be /usr/bin/python
pip list | grep <package-name>
```

### Kernel won't connect (VS Code)

- Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"
- Check Jupyter output: `Ctrl+Shift+P` → "Jupyter: Show Output"

---

## Why This Approach?

### Industry Standard

This is how production ML works:

- **Docker**: Standard for ML deployment
- **Kubernetes**: Containers are the unit of deployment
- **Cloud ML**: SageMaker, Vertex AI, etc. use containers

### Reproducibility

```dockerfile
# This Dockerfile IS your environment
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
RUN pip install transformers==4.30.0 datasets==2.13.0
```

Share the Dockerfile, anyone can recreate your exact environment.

### Isolation

Each project gets its own container:
- No package conflicts between projects
- No "it works on my machine" problems
- Clean separation of concerns

---

## Common Patterns

### Per-Project Environments

```
~/workspace/
├── thesis/
│   ├── Dockerfile          # PyTorch + transformers
│   └── ...
├── course-ml/
│   ├── Dockerfile          # sklearn + pandas
│   └── ...
└── experiment/
    ├── Dockerfile          # JAX + optax
    └── ...
```

Each project has its own Dockerfile = its own environment.

### Sharing Environments

**Same base, different projects:**
```dockerfile
# Both projects can use same base
FROM aime/pytorch:24.09
```

**Exact reproduction:**
```bash
# Share your Dockerfile
cp ~/workspace/project/Dockerfile ~/shared/
```

---

## Next Steps

- [Custom Environments](../core-guides/custom-environments.md) - Practical how-to
- [Dockerfile Guide](../advanced/dockerfile-guide.md) - Advanced patterns
- [Containers and Images](containers-and-images.md) - Why this works
