# Linux Basics

**Essential command line skills for servers and cloud computing.**

> **Part of [Educational Computing Context](README.md)** - Career-relevant knowledge beyond DS01 basics.

If you're new to Linux, this guide will get you productive quickly. These skills transfer to any server, cloud platform, or production system.

---

## Why Command Line?

**Advantages over GUI:**
- **Faster**: Type commands vs click through menus
- **Scriptable**: Automate repetitive tasks
- **Remote**: Works over SSH (servers often have no GUI)
- **Powerful**: Combine commands, process thousands of files
- **Universal**: Skills transfer across all Linux systems

**Don't worry!** You only need ~20 commands for 90% of tasks.

---

## Essential Concepts

### The Shell

**What it is:** Program that interprets your commands (like `bash` or `zsh`)

```bash
your-username@ds01:~$
```

Breaking down the prompt:
- `your-username`: Your username
- `ds01`: Server hostname
- `~`: Current directory (~ means home)
- `$`: Regular user (# would mean root)

### File System Structure

Linux uses `/` as root (top) of filesystem:

```
/                           # Root directory
├── home/                   # User home directories
│   └── your-username/      # Your home (~)
│       ├── workspace/      # Your projects
│       └── dockerfiles/    # Image blueprints
├── opt/                    # Optional software
│   └── ds01-infra/         # DS01 installation
├── tmp/                    # Temporary files
└── var/                    # Variable data (logs)
```

**Key paths:**
- `~` or `/home/your-username/`: Your home directory
- `~/workspace/`: Your persistent project files
- `/opt/ds01-infra/`: System scripts
- `/tmp/`: Temporary files (cleared on reboot)

---

## Navigation Commands

### `pwd` - Print Working Directory

**Shows where you are:**
```bash
pwd
# Output: /home/your-username
```

### `ls` - List Files

**Basic usage:**
```bash
ls                          # List files in current directory
ls -l                       # Long format (permissions, size, date)
ls -lh                      # Human-readable sizes (KB, MB, GB)
ls -a                       # Show hidden files (starting with .)
ls -lah                     # Combine all options
```

**Examples:**
```bash
ls ~/workspace              # List workspace projects
ls -lh ~/dockerfiles        # List Dockerfiles with sizes
```

### `cd` - Change Directory

**Navigation:**
```bash
cd ~/workspace              # Go to workspace
cd my-project               # Go to subdirectory
cd ..                       # Go up one level
cd                          # Go to home directory
cd -                        # Go to previous directory
```

**Shortcuts:**
- `~`: Home directory (`/home/your-username/`)
- `.`: Current directory
- `..`: Parent directory
- `/`: Root directory

**Example workflow:**
```bash
cd ~/workspace              # Go to workspace
ls                          # See projects
cd my-project               # Enter project
pwd                         # Check location
cd ..                       # Go back to workspace
```

---

## File Management

### `mkdir` - Make Directory

```bash
mkdir new-project                           # Create directory
mkdir -p projects/experiment-1/data         # Create nested directories
```

**Options:**
- `-p`: Create parent directories if needed

### `touch` - Create Empty File

```bash
touch README.md                             # Create file
touch file1.txt file2.txt file3.txt         # Create multiple
```

### `cp` - Copy Files

```bash
cp source.txt destination.txt               # Copy file
cp -r directory/ backup/                    # Copy directory (-r = recursive)
cp *.py backup/                             # Copy all Python files
```

**Options:**
- `-r`: Recursive (for directories)
- `-i`: Interactive (ask before overwrite)
- `-v`: Verbose (show what's being copied)

### `mv` - Move/Rename Files

```bash
mv old-name.txt new-name.txt                # Rename file
mv file.txt ~/workspace/project/            # Move file
mv *.csv data/                              # Move all CSV files
```

### `rm` - Remove Files

**⚠️ WARNING: No trash/recycle bin! Deletions are permanent.**

```bash
rm file.txt                                 # Delete file
rm -r directory/                            # Delete directory
rm -i *.txt                                 # Interactive (ask for each)
```

**Options:**
- `-r`: Recursive (for directories)
- `-i`: Interactive (confirm each deletion)
- `-f`: Force (skip confirmations) **DANGEROUS!**

**NEVER run:** `rm -rf /` or `rm -rf /*` (deletes everything)

**Best practice:** Test with `ls` first:
```bash
ls *.txt                    # Check what matches
rm *.txt                    # Then delete
```

---

## Viewing Files

### `cat` - Display File

```bash
cat README.md               # Show entire file
cat file1.txt file2.txt     # Show multiple files
```

### `less` - Page Through File

```bash
less large-file.log         # View file page by page
```

**Navigation in less:**
- `Space`: Next page
- `b`: Previous page
- `/pattern`: Search forward
- `q`: Quit

### `head` and `tail`

```bash
head -n 20 file.txt         # First 20 lines
tail -n 20 file.txt         # Last 20 lines
tail -f logfile.log         # Follow file (watch new lines)
```

---

## File Permissions

### Understanding Permissions

```bash
ls -l file.txt
# Output: -rw-r--r-- 1 user group 1234 Nov 21 10:00 file.txt
```

Breaking down `-rw-r--r--`:
- `-`: File type (- = file, d = directory, l = link)
- `rw-`: Owner permissions (read, write, no execute)
- `r--`: Group permissions (read only)
- `r--`: Others permissions (read only)

**Permissions:**
- `r` (read): View file contents
- `w` (write): Modify file
- `x` (execute): Run as program

### `chmod` - Change Permissions

```bash
chmod +x script.sh          # Make executable
chmod 755 script.sh         # rwxr-xr-x (owner: all, others: read+execute)
chmod 644 file.txt          # rw-r--r-- (owner: read+write, others: read)
```

**Common patterns:**
- `755`: Scripts (owner can modify, all can read/execute)
- `644`: Data files (owner can modify, all can read)
- `600`: Private files (only owner can access)

---

## Searching

### `grep` - Search Text

```bash
grep "error" logfile.log                    # Find lines with "error"
grep -i "error" logfile.log                 # Case-insensitive
grep -r "TODO" ~/workspace/project/         # Search recursively in directory
grep -n "import torch" *.py                 # Show line numbers
```

**Options:**
- `-i`: Case-insensitive
- `-r`: Recursive (search directories)
- `-n`: Show line numbers
- `-v`: Invert (show lines that DON'T match)

### `find` - Find Files

```bash
find ~/workspace -name "*.py"               # Find Python files
find . -type d -name "data"                 # Find directories named "data"
find ~/workspace -mtime -7                  # Files modified in last 7 days
```

---

## Environment & Variables

### Environment Variables

```bash
echo $HOME                  # Your home directory
echo $PATH                  # Command search paths
echo $USER                  # Your username
```

**Setting variables:**
```bash
export MY_VAR="value"       # Set for current session
echo $MY_VAR                # Use variable
```

### `which` - Find Command Location

```bash
which python                # Show where python command is
which container-deploy      # Find DS01 command
```

---

## Process Management

### `ps` - List Processes

```bash
ps aux                      # All processes
ps aux | grep python        # Find Python processes
```

### `top` and `htop`

```bash
top                         # Interactive process monitor
htop                        # Better version (if installed)
```

**Navigation in top:**
- `q`: Quit
- `k`: Kill process
- `M`: Sort by memory
- `P`: Sort by CPU

### `kill` - Stop Process

```bash
kill 12345                  # Send TERM signal to PID 12345
kill -9 12345               # Force kill (SIGKILL)
```

**Get PID:**
```bash
ps aux | grep python
# Or use:
pidof python
```

---

## System Information

### Check Disk Space

```bash
df -h                       # Disk space (human-readable)
du -sh ~/workspace/*        # Size of each project
du -h --max-depth=1         # Size of directories (one level)
```

### Check Memory

```bash
free -h                     # RAM usage
```

### Check System Info

```bash
uname -a                    # System information
hostname                    # Server name
whoami                      # Your username
```

---

## Text Processing

### `wc` - Word Count

```bash
wc file.txt                 # Lines, words, characters
wc -l file.txt              # Just line count
```

### `sort` and `uniq`

```bash
sort file.txt               # Sort lines
sort -r file.txt            # Reverse sort
sort file.txt | uniq        # Remove duplicates
```

### Pipes `|` - Chain Commands

```bash
ls -l | grep "\.py$"                        # List only Python files
cat file.txt | grep "error" | wc -l         # Count error lines
ps aux | grep python | wc -l                # Count Python processes
```

**Concept:** Output of first command → input of second command

---

## File Transfer

### `scp` - Secure Copy (from your laptop)

```bash
# Upload to server
scp local-file.txt user@ds01:~/workspace/project/

# Download from server
scp user@ds01:~/workspace/project/results.csv ./

# Copy directory
scp -r local-dir/ user@ds01:~/workspace/
```

### `rsync` - Better Copying

```bash
# Sync directory to server
rsync -avz local-dir/ user@ds01:~/workspace/project/

# Download from server
rsync -avz user@ds01:~/workspace/project/ ./local-backup/
```

**Advantages over scp:**
- Resumes interrupted transfers
- Only transfers changed files
- Shows progress

---

## Shortcuts & Productivity

### Tab Completion

**Press Tab to auto-complete:**
```bash
cd ~/work<Tab>              # Completes to: cd ~/workspace/
ls my-pr<Tab>               # Completes to: ls my-project/
```

### Command History

```bash
history                     # Show command history
!123                        # Run command #123 from history
!!                          # Run last command
!cat                        # Run last command starting with "cat"
```

**Navigate history:**
- `↑` (up arrow): Previous command
- `↓` (down arrow): Next command
- `Ctrl+R`: Search history (type to search, Enter to run)

### Keyboard Shortcuts

**Essential:**
- `Ctrl+C`: Cancel current command
- `Ctrl+D`: Logout (or EOF)
- `Ctrl+L`: Clear screen (like `clear` command)
- `Ctrl+A`: Move to start of line
- `Ctrl+E`: Move to end of line
- `Ctrl+U`: Delete to start of line
- `Ctrl+K`: Delete to end of line
- `Ctrl+R`: Search history

### Command Chaining

```bash
command1 && command2        # Run command2 only if command1 succeeds
command1 ; command2         # Run both regardless
command1 || command2        # Run command2 only if command1 fails
```

**Examples:**
```bash
mkdir project && cd project                 # Create and enter
cd ~/workspace ; ls                         # Go and list
rm file.txt && echo "Deleted successfully"  # Delete and confirm
```

---

## DS01-Specific Paths

### Your Important Directories

```bash
~/workspace/                # Your persistent projects
~/dockerfiles/              # Image blueprints
~/.ssh/                     # SSH keys
~/.ds01-limits              # Your resource quotas
```

### System Directories

```bash
/opt/ds01-infra/            # DS01 installation
/opt/aime-ml-containers/    # Base container system
/var/lib/ds01/              # State files
/var/log/ds01/              # System logs
```

---

## Common Workflows

### Starting a New Project

```bash
cd ~/workspace
mkdir my-project
cd my-project
git init
cat > README.md << 'EOF'
# My Project
EOF
```

### Checking Disk Usage

```bash
du -sh ~/workspace/*                        # Size of each project
df -h | grep home                           # Total home directory usage
```

### Finding Large Files

```bash
find ~/workspace -type f -size +1G          # Files over 1GB
du -ah ~/workspace | sort -hr | head -20    # 20 largest items
```

### Cleaning Up

```bash
# Find old files
find ~/workspace -mtime +90                 # Not modified in 90 days

# Remove temporary files
rm -rf ~/workspace/*/tmp
rm -f ~/workspace/*/*.tmp

# Clean Python cache
find ~/workspace -type d -name __pycache__ -exec rm -rf {} +
```

---

## Helpful Aliases

Add to `~/.bashrc`:

```bash
# Navigation
alias ws='cd ~/workspace'
alias df='cd ~/dockerfiles'

# Shortcuts
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'

# Safety
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# DS01
alias containers='container-list'
alias gpu='nvidia-smi'
```

Apply changes:
```bash
source ~/.bashrc
```

---

## Practice Exercises

### Exercise 1: Navigation

```bash
# 1. Go to your home directory
cd ~

# 2. List all files including hidden
ls -lah

# 3. Create workspace if it doesn't exist
mkdir -p ~/workspace

# 4. Go to workspace
cd ~/workspace

# 5. Check current location
pwd
```

### Exercise 2: File Management

```bash
# 1. Create project directory
mkdir ~/workspace/practice-project
cd ~/workspace/practice-project

# 2. Create some files
touch README.md train.py test.py
mkdir data models

# 3. List structure
ls -lh

# 4. Copy file
cp train.py train_backup.py

# 5. Remove backup
rm train_backup.py
```

### Exercise 3: Viewing & Searching

```bash
# 1. Create sample file
cat > ~/workspace/practice-project/sample.txt << 'EOF'
Line 1: Hello
Line 2: World
Line 3: Hello again
EOF

# 2. View file
cat sample.txt

# 3. Search for "Hello"
grep "Hello" sample.txt

# 4. Count lines
wc -l sample.txt
```

---

## Getting Help

### Command Help

```bash
man ls                      # Manual page (detailed)
ls --help                   # Quick help
```

**Navigate man pages:**
- `Space`: Next page
- `b`: Previous page
- `/pattern`: Search
- `q`: Quit

### Quick Reference

```bash
# Most commands support --help
container-deploy --help
docker --help
```

---

## Common Mistakes to Avoid

### 1. Dangerous Commands

**DON'T run these:**
```bash
rm -rf /                    # Deletes everything
rm -rf /*                   # Also deletes everything
rm -rf ~/*                  # Deletes all your files
chmod -R 777 ~/             # Makes everything world-writable
```

### 2. Case Sensitivity

Linux is case-sensitive:
- `README.md` ≠ `readme.md` ≠ `ReadMe.md`
- `myproject/` ≠ `MyProject/`

### 3. Spaces in Names

**Avoid spaces in file names:**
- Bad: `my project/`
- Good: `my-project/` or `my_project/`

**If you must use spaces, quote:**
```bash
cd "my project"
```

### 4. Hidden Files

Files starting with `.` are hidden:
```bash
ls                          # Won't show .bashrc
ls -a                       # Shows .bashrc
```

---

## Next Steps

### Practice Daily

**Use these commands daily:**
- `cd`, `ls`, `pwd` (navigation)
- `cat`, `less` (viewing)
- `mkdir`, `cp`, `mv`, `rm` (file management)

**Within a week, they'll be second nature.**

### Learn More

**Container workflows:**
- → [Containers Explained](containers-explained.md)

**DS01 usage:**
- → [Daily Usage Patterns](../core-guides/daily-workflow.md)

**Advanced topics:**
→ 

---

## Quick Reference Card

```bash
# Navigation
pwd                         # Current directory
ls -lah                     # List files
cd ~/workspace              # Change directory

# Files
mkdir project               # Create directory
touch file.txt              # Create file
cp source dest              # Copy
mv old new                  # Move/rename
rm file.txt                 # Delete

# Viewing
cat file.txt                # Show file
less file.txt               # Page through
head -n 20 file.txt         # First 20 lines
tail -n 20 file.txt         # Last 20 lines

# Searching
grep "pattern" file         # Search in file
find . -name "*.py"         # Find files

# System
df -h                       # Disk space
du -sh ~/workspace/*        # Directory sizes
ps aux                      # Processes
top                         # Process monitor

# Help
man command                 # Manual
command --help              # Quick help
```

---

**Practice these commands and you'll be productive on DS01 quickly!**

**Ready to understand containers?** → [Containers Explained](containers-explained.md)

**Want to start using DS01?** → [Quick Start](../getting-started/quick-start.md)
