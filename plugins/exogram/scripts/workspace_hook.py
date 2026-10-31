#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


def workspace() -> Path | None:
    start = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
    return next((directory for directory in (start, *start.parents) if (directory / "exogram" / "scripts").is_dir()), None)


def main() -> int:
    root = workspace()
    if root is None:
        return 0
    return subprocess.run([sys.executable, str(root / "exogram" / "scripts" / sys.argv[1])], stdin=sys.stdin).returncode


if __name__ == "__main__":
    sys.exit(main())
