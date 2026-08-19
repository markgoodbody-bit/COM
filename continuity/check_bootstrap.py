#!/usr/bin/env python3
"""Fail-closed structural check for the bounded Framework bootstrap.

This validates carrier shape only. A successful check does not establish that
HEAD is current, that its claims are true, or that any action is authorised.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST_PATH = HERE / "BOOT_MANIFEST.json"


def fail(message: str) -> None:
    raise RuntimeError(message)


def resolve_repo_path(value: str) -> Path:
    path = (ROOT / value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise RuntimeError(f"path escapes repository root: {value}") from exc
    return path


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        if manifest.get("schema") != "framework-bootstrap-manifest-v1":
            fail("unexpected bootstrap manifest schema")

        entry = manifest["entrypoint"]
        eager = manifest["eager_sequence"]
        conditional = manifest["conditional"]

        declared = [entry, *eager, *conditional]
        eager_total = 0

        for spec in declared:
            rel = spec["path"]
            max_bytes = int(spec["max_bytes"])
            path = resolve_repo_path(rel)
            if not path.is_file():
                fail(f"missing bootstrap file: {rel}")
            size = len(path.read_bytes())
            if size > max_bytes:
                fail(f"bootstrap file exceeds bound: {rel} {size}>{max_bytes}")
            if spec is entry or spec in eager:
                eager_total += size

        max_eager = int(manifest["max_eager_bytes_including_entrypoint"])
        if eager_total > max_eager:
            fail(f"eager bootstrap exceeds bound: {eager_total}>{max_eager}")

        required_markers = manifest.get("required_markers", {})
        for rel, markers in required_markers.items():
            text = resolve_repo_path(rel).read_text(encoding="utf-8")
            for marker in markers:
                if marker not in text:
                    fail(f"required marker missing from {rel}: {marker}")

        kernel = resolve_repo_path("continuity/KERNEL.md").read_text(encoding="utf-8")
        for marker in manifest.get("kernel_forbidden_markers", []):
            if marker in kernel:
                fail(f"fast-changing marker leaked into KERNEL.md: {marker}")

        boot = resolve_repo_path("continuity/BOOT.md").read_text(encoding="utf-8")
        order = [
            "continuity/KERNEL.md",
            "continuity/FRAMEWORK_HEAD.md",
            "continuity/OMISSION_MAP.md",
        ]
        positions = [boot.find(item) for item in order]
        if any(position < 0 for position in positions):
            fail("BOOT.md does not reference every required boot object")
        if positions != sorted(positions):
            fail("BOOT.md required-object references are not in KERNEL -> HEAD -> OMISSION order")

        print(
            "BOOTSTRAP_STRUCTURE_OK "
            f"eager_bytes={eager_total} "
            f"eager_limit={max_eager}"
        )
        print(
            "CEILING: structure/current-size checks only; "
            "HEAD freshness, truth, authority and world correspondence remain unestablished"
        )
        return 0

    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"BOOTSTRAP_STRUCTURE_FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
