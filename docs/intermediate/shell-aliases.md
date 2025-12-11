# Shell Aliases

Speed up your workflow with these handy aliases.

## Setup

Add these to your `~/.bashrc`:

```bash
# Short aliases
alias pl='project launch'
alias pd='project deploy'
alias ca='container-attach'
alias cr='container retire'
alias cl='container-list'

# Common patterns
alias plo='project launch --open'
alias plb='project launch --background'
alias crf='container retire --force'
```

Then reload your shell:

```bash
source ~/.bashrc
```

## Usage

```bash
plo my-thesis          # project launch my-thesis --open
plb my-thesis          # project launch my-thesis --background
crf my-thesis          # container retire my-thesis --force
cl                     # container-list
ca my-thesis           # container-attach my-thesis
```

## More Aliases

Feel free to add your own based on your workflow:

```bash
# Project shortcuts
alias pi='project init'
alias pig='project init --guided'

# Container inspection
alias cs='container-stats'

# Quick checks
alias limits='check-limits'
alias gpus='dashboard'
```
