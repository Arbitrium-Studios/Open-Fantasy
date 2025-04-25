import subprocess
import os

def get_uninitialized_submodules():
    result = subprocess.run(['git', 'submodule', 'status'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    uninitialized = []
    for line in lines:
        if line.startswith('-'):
            parts = line.split(' ', 2)
            uninitialized.append(parts[2])
    return uninitialized

def init_submodules(submodules):
    for submodule in submodules:
        print(f"Initializing submodule: {submodule}")
        subprocess.run(['git', 'submodule', 'init', submodule], check=True)
        subprocess.run(['git', 'submodule', 'update', '--recursive', '--remote', submodule], check=True)

if __name__ == "__main__":
    uninitialized_submodules = get_uninitialized_submodules()
    if uninitialized_submodules:
        init_submodules(uninitialized_submodules)
    else:
        print("All submodules are initialized.")
