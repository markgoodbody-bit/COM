#!/usr/bin/env python3
"""Run bundled recovery companion fixtures."""
from __future__ import annotations
import json
from pathlib import Path
from validate import validate

ROOT = Path(__file__).resolve().parent
CASES = {
    "examples/clean_handoff_exact_head.json": True,
    "examples/stalled_lane_named_transfer.json": True,
    "examples/double_mutator_same_object.json": False,
    "examples/takeover_from_stale_head.json": False,
    "examples/success_widens_scope_implicitly.json": False,
}

def main() -> int:
    bad = False
    for relative, expected in CASES.items():
        doc = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        errors = validate(doc)
        actual = not errors
        if actual != expected:
            bad = True
            print(f"MISMATCH {relative}: expected {'PASS' if expected else 'FAIL'}, got {'PASS' if actual else 'FAIL'}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {relative}: {'PASS' if actual else 'FAIL as expected'}")
    return 1 if bad else 0

if __name__ == "__main__":
    raise SystemExit(main())
