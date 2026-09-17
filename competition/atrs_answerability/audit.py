#!/usr/bin/env python3
"""Compatibility entrypoint for the version-aware ATRS audit core."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from audit_core import *  # noqa: F401,F403

if __name__ == "__main__":
    raise SystemExit(main())
