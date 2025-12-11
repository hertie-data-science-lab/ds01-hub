# Scripting with Python

Automate DS01 workflows with Python scripts.

---

## Why Python?

| Advantages | Disadvantages |
|------------|---------------|
| Better error handling | Extra subprocess overhead |
| Rich data structures | Requires Python installed |
| Easier debugging | More verbose for simple tasks |
| JSON parsing built-in | Not native shell integration |

**Best for:** Complex workflows, data processing, structured automation.

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
python run_experiments.py
# Runs all 10 automatically
```

---

## Basic Script Template

```python
#!/usr/bin/env python3
# my_workflow.py

import subprocess
import sys
import os

def run(cmd):
    """Run a command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout

def main():
    project = sys.argv[1] if len(sys.argv) > 1 else "my-project"
    gpu_count = sys.argv[2] if len(sys.argv) > 2 else "1"

    # Deploy container
    run(f"container-create {project} --gpu={gpu_count}")
    run(f"container-start {project}")

    # Run work
    user_id = os.getuid()
    run(f"docker exec {project}._.{user_id} python /workspace/{project}/train.py")

    # Cleanup
    run(f"container-stop {project}")
    run(f"container-remove {project} --force")

    print("Done!")

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
chmod +x my_workflow.py
./my_workflow.py my-thesis 2
```

---

## Pattern 1: Parallel Experiments

```python
#!/usr/bin/env python3
# parallel_experiments.py

import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

def run_experiment(lr):
    """Run a single experiment."""
    name = f"exp-lr-{lr}"
    user_id = os.getuid()

    subprocess.run(f"container-create {name} --background", shell=True)
    subprocess.run(f"container-start {name}", shell=True)
    subprocess.run(
        f"docker exec {name}._.{user_id} python /workspace/train.py --lr={lr}",
        shell=True
    )
    return name

def main():
    learning_rates = [0.001, 0.01, 0.1]

    # Run in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        containers = list(executor.map(run_experiment, learning_rates))

    # Cleanup
    for name in containers:
        subprocess.run(f"container-retire {name} --force", shell=True)

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
chmod +x parallel_experiments.py
./parallel_experiments.py
```

---

## Pattern 2: Sequential Pipeline

```python
#!/usr/bin/env python3
# ml_pipeline.py

import subprocess
import os
import sys

def run_stage(name, gpu=1, script=""):
    """Run a pipeline stage."""
    user_id = os.getuid()

    subprocess.run(f"container-create {name} --gpu={gpu}", shell=True, check=True)
    subprocess.run(f"container-start {name}", shell=True, check=True)
    subprocess.run(
        f"docker exec {name}._.{user_id} python /workspace/{script}",
        shell=True, check=True
    )
    subprocess.run(f"container-retire {name} --force", shell=True)

def main():
    stages = [
        ("data-prep", 0, "preprocess.py"),
        ("training", 2, "train.py"),
        ("eval", 1, "evaluate.py"),
    ]

    for name, gpu, script in stages:
        print(f"Running stage: {name}")
        run_stage(name, gpu, script)

    print("Pipeline complete!")

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
chmod +x ml_pipeline.py
./ml_pipeline.py
```

---

## Pattern 3: Hyperparameter Grid Search

```python
#!/usr/bin/env python3
# grid_search.py

import subprocess
import os
import itertools

def run_config(lr, batch_size):
    """Run a single configuration."""
    name = f"exp-lr{lr}-bs{batch_size}"
    user_id = os.getuid()

    print(f"Running: {name}")

    subprocess.run(f"container-create {name} --background", shell=True, check=True)
    subprocess.run(f"container-start {name}", shell=True, check=True)

    subprocess.run(
        f"docker exec {name}._.{user_id} bash -c "
        f"'cd /workspace/experiments && python train.py --lr={lr} --batch-size={batch_size}'",
        shell=True, check=True
    )

    subprocess.run(f"container-retire {name} --force", shell=True)

def main():
    learning_rates = [0.001, 0.01, 0.1]
    batch_sizes = [16, 32, 64]

    for lr, bs in itertools.product(learning_rates, batch_sizes):
        run_config(lr, bs)

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
chmod +x grid_search.py
./grid_search.py
```

---

## Error Handling

```python
#!/usr/bin/env python3
# robust_script.py

import subprocess
import sys
import atexit

container_name = None

def cleanup():
    """Cleanup on exit or error."""
    if container_name:
        print("Cleaning up...")
        subprocess.run(
            f"container-remove {container_name} --stop --force",
            shell=True, stderr=subprocess.DEVNULL
        )

def main():
    global container_name

    project = sys.argv[1] if len(sys.argv) > 1 else "my-project"
    container_name = f"script-{project}"

    # Register cleanup
    atexit.register(cleanup)

    try:
        subprocess.run(f"container-create {container_name}", shell=True, check=True)
        subprocess.run(f"container-start {container_name}", shell=True, check=True)

        user_id = __import__('os').getuid()
        subprocess.run(
            f"docker exec {container_name}._.{user_id} python /workspace/train.py",
            shell=True, check=True
        )

        print("Success!")

    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Checking Container State

```python
#!/usr/bin/env python3

import subprocess
import sys

def main():
    container = sys.argv[1] if len(sys.argv) > 1 else "my-project"

    result = subprocess.run(
        "container-list", shell=True, capture_output=True, text=True
    )

    if f"{container}" in result.stdout and "running" in result.stdout:
        print("Container is running")
        subprocess.run(f"container-attach {container}", shell=True)
    else:
        print("Container not running, creating...")
        subprocess.run(f"project launch {container} --open", shell=True)

if __name__ == "__main__":
    main()
```

---

## Parsing JSON Output

```python
#!/usr/bin/env python3

import subprocess
import json

def main():
    # Get container info as JSON
    result = subprocess.run(
        "container-list --format=json",
        shell=True, capture_output=True, text=True
    )
    containers = json.loads(result.stdout)

    # Filter containers with GPUs
    gpu_containers = [c['name'] for c in containers if c.get('gpu_count', 0) > 0]
    print("Containers with GPUs:", gpu_containers)

    # Process each
    for container in containers:
        print(f"Processing {container['name']}")

if __name__ == "__main__":
    main()
```

---

## Best Practices

1. **Use `check=True`** - raise exceptions on errors
2. **Register cleanup with `atexit`** - free resources on exit
3. **Use `--force` flags** - don't block on prompts
4. **Print progress** - `print()` statements for debugging
5. **Validate inputs** - check `sys.argv` early

---

## Next Steps

- [Scripting with Bash](scripting-bash.md) - Alternative approach
- [Atomic Commands](atomic-commands.md) - Commands for scripting
- [CLI Flags](cli-flags.md) - Non-interactive usage
- [Advanced](../advanced/) - Docker-native scripting
