# Scripting with Bash

Automate DS01 workflows with bash scripts.

---

## Why Bash?

| Advantages | Disadvantages |
|------------|---------------|
| Native to DS01 commands | Complex string manipulation |
| No dependencies | Error handling is verbose |
| Fast for simple tasks | Harder to debug |
| Direct shell integration | Limited data structures |

**Best for:** Simple workflows, quick automation, cron jobs.

---

## Why Script?

**Manual (tedious):**
```bash
# Run 10 experiments
container deploy exp-1 --open
python train.py --lr=0.001
exit
container retire exp-1

container deploy exp-2 --open
python train.py --lr=0.01
exit
container retire exp-2
# ... 8 more times
```

**Scripted (efficient):**
```bash
./run-experiments.sh
# Runs all 10 automatically
```

---

## Basic Script Template

```bash
#!/bin/bash
# my-workflow.sh

set -e  # Exit on error

PROJECT=$1
GPU_COUNT=${2:-1}

# Deploy container
container-create $PROJECT --gpu=$GPU_COUNT
container-start $PROJECT

# Run work
container-attach $PROJECT <<EOF
cd /workspace/$PROJECT
python train.py
exit
EOF

# Cleanup
container-stop $PROJECT
container-remove $PROJECT --force

echo "Done!"
```

**Usage:**
```bash
chmod +x my-workflow.sh
./my-workflow.sh my-thesis 2
```

---

## Pattern 1: Parallel Experiments

```bash
#!/bin/bash
# parallel-experiments.sh

for lr in 0.001 0.01 0.1; do
  NAME="exp-lr-$lr"

  container-create $NAME --background
  container-start $NAME

  docker exec $NAME._.$(id -u) \
    python /workspace/train.py --lr=$lr &
done

wait  # Wait for all to finish

# Cleanup
for lr in 0.001 0.01 0.1; do
  container-retire "exp-lr-$lr" --force
done
```

**Usage:**
```bash
chmod +x parallel-experiments.sh
./parallel-experiments.sh
```

---

## Pattern 2: Sequential Pipeline

```bash
#!/bin/bash
# ml-pipeline.sh

PROJECT=$1

# Stage 1: Data prep
container deploy data-prep --open <<EOF
python preprocess.py
exit
EOF

# Stage 2: Training
container deploy training --gpu=2 --open <<EOF
python train.py
exit
EOF

# Stage 3: Evaluation
container deploy eval --open <<EOF
python evaluate.py
exit
EOF

# Cleanup
container retire data-prep --force
container retire training --force
container retire eval --force
```

**Usage:**
```bash
chmod +x ml-pipeline.sh
./ml-pipeline.sh my-thesis
```

---

## Pattern 3: Hyperparameter Grid Search

```bash
#!/bin/bash
# grid-search.sh

for lr in 0.001 0.01 0.1; do
  for batch_size in 16 32 64; do
    NAME="exp-lr${lr}-bs${batch_size}"

    echo "Running: $NAME"

    container-create $NAME --background
    container-start $NAME

    docker exec $NAME._.$(id -u) bash -c "
      cd /workspace/experiments
      python train.py --lr=$lr --batch-size=$batch_size
    "

    container-retire $NAME --force
  done
done
```

**Usage:**
```bash
chmod +x grid-search.sh
./grid-search.sh
```

---

## Error Handling

```bash
#!/bin/bash
# robust-script.sh

set -e  # Exit on error

PROJECT=$1
CONTAINER_NAME="script-$PROJECT"

# Cleanup on exit or error
cleanup() {
  echo "Cleaning up..."
  container-remove $CONTAINER_NAME --stop --force 2>/dev/null || true
}
trap cleanup EXIT

# Main workflow
container-create $CONTAINER_NAME
container-start $CONTAINER_NAME

docker exec $CONTAINER_NAME._.$(id -u) \
  python /workspace/train.py

echo "Success!"
```

---

## Checking Container State

```bash
#!/bin/bash

CONTAINER=$1

# Check if running
if container-list | grep -q "$CONTAINER.*running"; then
  echo "Container is running"
  container-attach $CONTAINER
else
  echo "Container not running, creating..."
  project launch $CONTAINER --open
fi
```

---

## Parsing JSON Output

```bash
#!/bin/bash

# Get container info as JSON
CONTAINERS=$(container-list --format=json)

# Parse with jq
echo "$CONTAINERS" | jq -r '.[] | select(.gpu_count > 0) | .name'

# Or iterate
echo "$CONTAINERS" | jq -r '.[].name' | while read container; do
  echo "Processing $container"
done
```

---

## Best Practices

1. **Always use `set -e`:** Without this, bash continues executing after errors. Your script creates a container, the creation fails, but the script still tries to start and attach to a non-existent container - generating confusing cascading errors. With `set -e`, the script stops at the first failure with a clear error message.

2. **Add cleanup traps:** If your script fails mid-execution, you've left a container running and a GPU allocated. Use `trap "container-remove $NAME --stop --force 2>/dev/null" EXIT` at the start - this runs automatically whether the script succeeds, fails, or is interrupted with Ctrl+C. No orphaned resources.

3. **Use `--force` flags:** DS01 commands prompt for confirmation by default ("Are you sure you want to remove this container?"). Interactive prompts break scripts - they hang waiting for input that never comes. `--force` skips all confirmations, making commands scriptable.

4. **Log progress:** Scripts that run silently for 20 minutes leave you wondering "is it stuck or working?" Add `echo "Starting container $NAME..."` before significant operations. When something fails at 3am, you'll know exactly which step it was on.

5. **Validate inputs:** If your script expects `./run.sh my-project 2` but someone runs `./run.sh`, the script will create containers named "" with undefined GPU counts. Check early: `[ -z "$1" ] && echo "Usage: $0 <project> [gpus]" && exit 1`.

---

## Next Steps

- [Scripting with Python](scripting-python.md) - Alternative approach
- [Advanced](../advanced/) - Docker-native scripting
