#!/usr/bin/env python3
"""Exact byte and semantic contract checks for Local Continuity Capsule v1.

This validates research artifacts only. It does not observe the live host, publish,
call a model, use credentials, spend, or grant authority.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "research" / "LOCAL_CONTINUITY_CAPSULE_V1_SCHEMA_20260902.json"
PROFILE_PATH = ROOT / "research" / "LOCAL_CONTINUITY_CAPSULE_V1_PROFILE_20260902.json"
FIXTURES_PATH = ROOT / "research" / "LOCAL_CONTINUITY_CAPSULE_V1_FIXTURES_20260903.json"

EXPECTED_SCHEMA_SHA256 = "3183838ba182388dee0fe62ed4c533bf3ebafe3bb6d44e802163e658a82769fe"
EXPECTED_PROFILE_SHA256 = "bdf07c294b49af6adc0b1345d6ebeac20f0287a8542cfd483197a111b7e6eb08"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> tuple[bytes, dict]:
    raw = path.read_bytes()
    return raw, json.loads(raw)


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_profile_schema_parity(schema: dict, profile: dict) -> None:
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

    schema_dwell = {}
    for option in schema["$defs"]["dwell_entry"]["oneOf"]:
        props = option["properties"]
        schema_dwell[props["state_id"]["const"]] = {
            "threshold_id": props["threshold_id"]["const"],
            "seconds": props["expected_max_dwell_seconds"]["const"],
            "authority": props["threshold_authority"]["const"],
        }
    profile_dwell = {
        row["state_id"]: {
            "threshold_id": row["threshold_id"],
            "seconds": row["expected_max_dwell_seconds"],
            "authority": row["authority"],
        }
        for row in profile["dwell_thresholds"]
    }
    assert profile_dwell == schema_dwell, "profile/schema dwell threshold tuples differ"

    rule_map = {
        row["state_id"]: row["active_condition_code"]
        for row in profile["active_condition_rules"]["specific_state_mapping"]
    }
    assert set(rule_map) == set(schema_dwell), "specific active-condition map does not cover every dwell state"
    assert set(rule_map.values()) <= profile_active
    assert profile["active_condition_rules"]["breach_mapping"]["any_breached_dwell_requires"] == (
        "STATE_UNCHANGED_BEYOND_EXPECTED_DWELL"
    )
    assert profile["active_condition_rules"]["breach_mapping"][
        "state_unchanged_beyond_expected_dwell_requires_any_breached_dwell"
    ] is True


def validate_capsule_semantics(capsule: dict, profile: dict) -> None:
    if capsule["profile_sha256"] != EXPECTED_PROFILE_SHA256:
        raise ValueError("capsule profile_sha256 does not bind the exact profile bytes")

    observed = parse_utc(capsule["observation"]["observed_at_utc"])
    next_due = parse_utc(capsule["observation"]["next_publication_due_utc"])
    if next_due <= observed:
        raise ValueError("next_publication_due_utc must be after observed_at_utc")

    rule_map = {
        row["state_id"]: row["active_condition_code"]
        for row in profile["active_condition_rules"]["specific_state_mapping"]
    }
    expected_active = set()
    any_breached = False

    for dwell in capsule["observation"]["dwell"]:
        since = parse_utc(dwell["unchanged_since_utc"])
        if since > observed:
            raise ValueError(f"{dwell['state_id']} unchanged_since_utc is after observation")
        expected_breached = (observed - since).total_seconds() >= dwell["expected_max_dwell_seconds"]
        if dwell["breached"] is not expected_breached:
            raise ValueError(
                f"{dwell['state_id']} breached={dwell['breached']} but recomputation is {expected_breached}"
            )
        expected_active.add(rule_map[dwell["state_id"]])
        any_breached = any_breached or dwell["breached"]

    if any_breached:
        expected_active.add("STATE_UNCHANGED_BEYOND_EXPECTED_DWELL")

    actual_active = set(capsule["active_conditions"]["codes"])
    if actual_active != expected_active:
        raise ValueError(
            f"active_conditions do not equal dwell-derived conditions: expected={sorted(expected_active)} "
            f"actual={sorted(actual_active)}"
        )
    if capsule["active_conditions"]["present"] is not bool(expected_active):
        raise ValueError("active_conditions.present disagrees with derived condition set")


def main() -> None:
    schema_bytes, schema = load(SCHEMA_PATH)
    profile_bytes, profile = load(PROFILE_PATH)
    _, fixture_bundle = load(FIXTURES_PATH)

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
    assert fixture_bundle["profile_sha256"] == profile_sha

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    validate_profile_schema_parity(schema, profile)

    for vector in profile["canonicalization_test_vectors"]:
        observed_vector_sha = sha256_bytes(vector["canonical_json"].encode("utf-8"))
        assert observed_vector_sha == vector["sha256"], (
            f"canonicalization vector {vector['name']} digest mismatch: {observed_vector_sha}"
        )

    # Digest arithmetic negative: changed schema bytes must not retain a valid profile binding.
    mutated_schema_sha = sha256_bytes(schema_bytes + b"\n")
    assert mutated_schema_sha != schema_sha
    assert profile["capsule_schema_sha256"] != mutated_schema_sha

    failures = []
    for fixture in fixture_bundle["fixtures"]:
        valid = True
        detail = ""
        try:
            validator.validate(fixture["capsule"])
            validate_capsule_semantics(fixture["capsule"], profile)
        except (ValidationError, ValueError, AssertionError) as exc:
            valid = False
            detail = str(exc).splitlines()[0]
        if valid != fixture["expected_valid"]:
            failures.append((fixture["name"], valid, detail))
            print(f"FAIL {fixture['name']}: observed_valid={valid} {detail}")
        else:
            suffix = "" if valid else f" ({detail})"
            print(f"PASS {fixture['name']}: observed_valid={valid}{suffix}")

    if failures:
        raise SystemExit(1)

    print(f"PASS exact schema sha256: {schema_sha}")
    print(f"PASS exact profile sha256: {profile_sha}")
    print(f"PASS capsule fixture bundle: {len(fixture_bundle['fixtures'])} cases")
    print("PASS profile/schema vocabulary, dwell tuple and condition-rule parity")
    print("PASS stale-schema/profile byte-binding mutation refused")


if __name__ == "__main__":
    main()
