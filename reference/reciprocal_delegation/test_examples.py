#!/usr/bin/env python3
"""Run the bundled reciprocal-delegation/0.1 example expectations."""

from __future__ import annotations

import json
from pathlib import Path

from validator import validate

ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"

EXPECTED = {
    "routine_source_build.json": True,
    "consequential_with_legible_authorization.json": True,
    "consequential_account_change_missing_authorization.json": False,
    "publication_outpaces_human.json": False,
    "repair_without_matching_control.json": False,
}


def main() -> int:
    failed = False
    for name, should_pass in EXPECTED.items():
        doc = json.loads((EXAMPLES / name).read_text(encoding="utf-8"))
        errors = validate(doc)
        passed = not errors
        status = "PASS" if passed else "FAIL"
        expectation = "PASS" if should_pass else "FAIL"
        print(f"{name}: {status} (expected {expectation})")
        if passed != should_pass:
            failed = True
            for error in errors:
                print(f"  - {error}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
