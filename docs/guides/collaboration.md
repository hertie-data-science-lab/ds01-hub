# Collaboration

Working with others on DS01.

## Sharing Code

**Use Git:**
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

**Options:**
1. Shared data directory (if available)
2. Download from common source
3. Small data: Include in Git repo

## Reproducibility

**Essential files:**
- `requirements.txt` - Python packages
- `Dockerfile` - Environment setup
- `README.md` - Instructions
- `.gitignore` - Exclude large files

**Example README:**
```markdown
# My Project

## Setup
\`\`\`bash
image-create my-project
container-deploy my-project --open
\`\`\`

## Running
\`\`\`bash
python src/train.py
\`\`\`
```

## Next Steps

→ [Creating Projects](creating-projects.md)
→ [Project Structure](../guides/creating-projects.md)
