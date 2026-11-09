import subprocess
import sys
import tempfile
import os
import json

def main():
    result = subprocess.run([sys.executable, "task_app.py", "--help"], capture_output=True, text=True)
    if result.returncode != 0:
        print("--help failed")
        return 1

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        path = tmp.name
    try:
        result = subprocess.run(
            [sys.executable, "task_app.py", "--data", path, "add", "Smoke task"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("add task failed:", result.stderr)
            return 1
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not any(t.get("title") == "Smoke task" for t in data):
            print("task not found")
            return 1
    finally:
        os.unlink(path)
    print("Smoke test passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())