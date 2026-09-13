#!/usr/bin/env python3
"""Run bundled reciprocal-delegation fan-out companion fixtures."""
from __future__ import annotations

import json
from pathlib import Path

from validate import validate

ROOT = Path(__file__).resolve().parent
CASES = {
    "examples/parallel_disjoint_children.json": True,
    "examples/complete_handback_with_receipts.json": True,
    "examples/authority_multiplied_by_parallelism.json": False,
    "examples/child_scope_and_subdelegation_escape.json": False,
    "examples/overlapping_mutators.json": False,
    "examples/handback_without_child_receipts.json": False,
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
