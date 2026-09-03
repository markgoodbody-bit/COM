#!/usr/bin/env python3
"""Exact byte-binding and vocabulary checks for Local Continuity Capsule v1.

Stdlib-only by design. This validates the research contract; it does not publish,
observe the live host, call a model, or grant authority.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "research" / "LOCAL_CONTINUITY_CAPSULE_V1_SCHEMA_20260902.json"
PROFILE_PATH = ROOT / "research" / "LOCAL_CONTINUITY_CAPSULE_V1_PROFILE_20260902.json"

EXPECTED_SCHEMA_SHA256 = "3b04b38ee35cb4076f18f20a8e5d01ee414e1773d81ec2c52774e7052a9b4ed3"
EXPECTED_PROFILE_SHA256 = "756e77f3dbd7ce9baad84503447e41ddec42dfcae96d77c81b23a35455b60ef5"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> tuple[bytes, dict]:
    raw = path.read_bytes()
    return raw, json.loads(raw)


def main() -> None:
    schema_bytes, schema = load(SCHEMA_PATH)
    profile_bytes, profile = load(PROFILE_PATH)

    schema_sha = sha256_bytes(schema_bytes)
    profile_sha = sha256_bytes(profile_bytes)

    assert schema_sha == EXPECTED_SCHEMA_SHA256, (
        f"schema digest moved: expected {EXPECTED_SCHEMA_SHA256}, observed {schema_sha}"
    )
    assert profile_sha == EXPECTED_PROFILE_SHA256, (
        f"profile digest moved: expected {EXPECTED_PROFILE_SHA256}, observed {profile_sha}"
    )
    assert profile["capsule_schema_sha256"] == schema_sha, (
        "profile capsule_schema_sha256 does not bind the exact current schema bytes"
    )

    schema_material = set(
        schema["properties"]["material_delta"]["properties"]["codes"]["items"]["enum"]
    )
    profile_material = set(profile["material_delta_codes"])
    assert profile_material == schema_material, (
        f"material delta vocabulary mismatch: profile={sorted(profile_material)} "
        f"schema={sorted(schema_material)}"
    )
    assert profile["cardinality"]["material_delta_codes_max"] == len(schema_material)

    schema_active = set(
        schema["properties"]["active_conditions"]["properties"]["codes"]["items"]["enum"]
    )
    profile_active = set(profile["active_condition_codes"])
    assert profile_active == schema_active, (
        f"active condition vocabulary mismatch: profile={sorted(profile_active)} "
        f"schema={sorted(schema_active)}"
    )
    assert profile["cardinality"]["active_condition_codes_max"] == len(schema_active)

    # Negative fixture: a schema byte change with an unchanged profile binding must refuse.
    mutated_schema_bytes = schema_bytes + b"\n"
    mutated_schema_sha = sha256_bytes(mutated_schema_bytes)
    assert mutated_schema_sha != schema_sha
    assert profile["capsule_schema_sha256"] != mutated_schema_sha, (
        "negative fixture failed: stale profile binding accepted changed schema bytes"
    )

    print(f"PASS exact schema sha256: {schema_sha}")
    print(f"PASS exact profile sha256: {profile_sha}")
    print(f"PASS material delta vocabulary: {len(schema_material)} codes")
    print(f"PASS active condition vocabulary: {len(schema_active)} codes")
    print("PASS negative stale-schema/profile binding fixture refused")


if __name__ == "__main__":
    main()
