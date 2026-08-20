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


def require_exact_contract_line(rel: str, contract: str) -> None:
    lines = resolve_repo_path(rel).read_text(encoding="utf-8").splitlines()
    expected = f"`{contract}`"
    matches = [line for line in lines if line == expected]
    if len(matches) != 1:
        fail(f"exact contract line missing or duplicated in {rel}: {contract}")


def require_head_sections(rel: str, headings: list[str]) -> None:
    lines = resolve_repo_path(rel).read_text(encoding="utf-8").splitlines()
    positions: list[int] = []
    for heading in headings:
        matches = [index for index, line in enumerate(lines) if line == heading]
        if len(matches) != 1:
            fail(f"HEAD section missing or duplicated: {heading}")
        positions.append(matches[0])
    if positions != sorted(positions):
        fail("HEAD required sections are not in declared order")

    for index, heading in enumerate(headings):
        start = positions[index] + 1
        end = positions[index + 1] if index + 1 < len(positions) else len(lines)
        body = [line for line in lines[start:end] if line.strip() and not line.startswith("#")]
        if not body:
            fail(f"HEAD required section is empty: {heading}")


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        if manifest.get("schema") != "framework-bootstrap-manifest-v1":
            fail("unexpected bootstrap manifest schema")

        front = manifest["front_door"]
        entry = manifest["entrypoint"]
        eager = manifest["eager_sequence"]
        conditional = manifest["conditional"]

        declared = [front, entry, *eager, *conditional]
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
            if spec is front or spec is entry or spec in eager:
                eager_total += size

        max_eager = int(manifest["max_eager_bytes_including_front_door"])
        if eager_total > max_eager:
            fail(f"eager bootstrap exceeds bound: {eager_total}>{max_eager}")

        required_markers = manifest.get("required_markers", {})
        for rel, markers in required_markers.items():
            text = resolve_repo_path(rel).read_text(encoding="utf-8")
            for marker in markers:
                if marker not in text:
                    fail(f"required marker missing from {rel}: {marker}")

        for rel, contract in manifest.get("exact_contract_lines", {}).items():
            require_exact_contract_line(rel, contract)

        require_head_sections(
            "continuity/FRAMEWORK_HEAD.md",
            list(manifest.get("head_required_sections", [])),
        )

        kernel = resolve_repo_path("continuity/KERNEL.md").read_text(encoding="utf-8")
        for marker in manifest.get("kernel_forbidden_markers", []):
            if marker in kernel:
                fail(f"fast-changing marker leaked into KERNEL.md: {marker}")

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
