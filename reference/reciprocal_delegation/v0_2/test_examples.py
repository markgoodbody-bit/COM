#!/usr/bin/env python3
"""Run the bundled reciprocal-delegation/0.2 field-repair examples."""
from __future__ import annotations
import json
from pathlib import Path
from validator import validate

ROOT = Path(__file__).resolve().parent
CASES = {
    "examples/d046_publication_event_bound.json": True,
    "examples/public_without_correction_bound.json": False,
}

def main() -> int:
    failed = False
    for relative, expected_pass in CASES.items():
        doc = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        errors = validate(doc)
        actual_pass = not errors
        if actual_pass != expected_pass:
            failed = True
            print(f"MISMATCH {relative}: expected {'PASS' if expected_pass else 'FAIL'}, got {'PASS' if actual_pass else 'FAIL'}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {relative}: {'PASS' if actual_pass else 'FAIL as expected'}")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
