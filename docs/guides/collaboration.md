# Collaboration

Working with others on DS01.

## Sharing Code

**Use Git (basic):**

*NB: git configuration and connectiong to a remote is automatically configured as standard in `project init`*

```bash
cd ~/workspace/my-project
git init
git remote add origin <repo-url>
git push -u origin main
```

**Colleagues can:**
```bash
cd ~/workspace
git clone <repo-url>
image-create my-project  # Build same image
container-deploy my-project
```

## Sharing Data

DS01 will be developing collaborative shared-access directories for data-sharing.

## Reproducibility

**Essential files:**
- `requirements.txt` - Python packages *(the basis for `image create` to build a Dockerfile with)*
- `Dockerfile` - Environment setup for containers *(built with `image create` or directly edit)*
- `README.md` - Instructions for users, displays on GitHub repos
- `.gitignore` - Exclude large files

### A note on `README.md`

`project init` creates a `README.md` on your behalf, but it is recommended to edit it immediately and iteratively.
```bash
# Edit README immediately
vim ~/workspace/my-thesis/README.md
```

Suggested to include:
- What this project does
- How to reproduce experiments
- Dataset locations
- Key results

### A note on Dockerfiles

Keep Dockerfiles simple

```dockerfile
# Good - clear, minimal
RUN pip install transformers datasets

# Avoid - overly complex
RUN pip install transformers && \
    wget https://... && \
    tar -xzf ... && \
    cd ... && \
    python setup.py install && \
    ...
```

## Next Steps
- → [Creating Projects](creating-projects.md)
- → [Project Structure](../guides/creating-projects.md)
