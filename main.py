"""Compatibility script for running the CLI from the source tree."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from task_list_cli import main

if __name__ == "__main__":
    raise SystemExit(main())
