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

For ongoing collaboration on the **same files** - a shared codebase, a common dataset,
joint results - ask an admin for a **shared project**.

### Shared projects

A shared project lives at `/home/shared/<name>` and works just like your own
`~/workspace/<project>`, except several people have read/write access to it - both on the
host and inside their containers.

**Getting one** - ask an admin to create it with the members:

```bash
# (an admin runs this)
sudo shared-workspace create pragmata-workspace \
    h.baker@hertie-school.lan d.dimmery@hertie-school.lan l.ruiz@hertie-school.lan
```

**Finding one** - any member can list shared projects without sudo:

```bash
shared-workspace list                        # every shared project + member counts
shared-workspace list pragmata-workspace     # who's a member of one
```

**Working in it** (any member):

```bash
cd /home/shared/pragmata-workspace
git status            # it's an ordinary git repo - edit, commit, push as usual
```

**Using it in a container** - mount it as your workspace when you launch:

```bash
container-deploy pragmata --workspace /home/shared/pragmata-workspace
# inside the container it appears at /workspace, read/write
```

Any file a member creates is automatically read/write for the other members - no need to
fix permissions by hand. To add or remove a collaborator later, an admin runs
`shared-workspace add-member <name> <user>` or `remove-member <name> <user>`.

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
- → [Project Structure](../core-guides/creating-projects.md)
