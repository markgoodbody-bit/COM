#!/usr/bin/env python3
"""Exact byte, hash, state and transition checks for Local Continuity Capsule v1.

Research contract only: no live-host observation, publishing, credentials, models,
spend, external actuation or authority grant.
"""

from __future__ import annotations

import copy
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

EXPECTED_SCHEMA_SHA256 = "18e52c4c2746998db23f17c39ceb9aa4a055342991bdef83614399bd5e3fc932"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> tuple[bytes, dict]:
    raw = path.read_bytes()
    return raw, json.loads(raw)


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def deep_merge(base: dict, patch: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def canonical_json(value) -> str:
    # Capsule v1's closed domain contains no floating-point values or free text.
    # For this ASCII/integer/bool/null domain, this matches the supplied RFC8785 vectors.
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def comparison_state(capsule: dict) -> dict:
    # Every frozen material-delta class must be represented here, otherwise a
    # declared delta can exist without being derivable from the comparison hash.
    return {
        "producer_build_sha256": capsule["producer"]["build_sha256"],
        "evidence": capsule["evidence"],
        "dwell": capsule["observation"]["dwell"],
        "active_conditions": capsule["active_conditions"],
    }


def compute_source_state_hash(capsule: dict) -> str:
    return sha256_bytes(canonical_json(comparison_state(capsule)).encode("utf-8"))


def compute_capsule_id(capsule: dict) -> str:
    payload = copy.deepcopy(capsule)
    payload.pop("capsule_id", None)
    return "sha256:" + sha256_bytes(canonical_json(payload).encode("utf-8"))


def seal_capsule(capsule: dict, profile_sha: str) -> dict:
    sealed = copy.deepcopy(capsule)
    sealed["profile_sha256"] = profile_sha
    sealed["observation"]["source_state_hash"] = compute_source_state_hash(sealed)
    sealed["capsule_id"] = compute_capsule_id(sealed)
    return sealed


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
    assert set(rule_map) == set(schema_dwell), "specific active-condition map misses dwell states"
    assert set(rule_map.values()) <= profile_active
    breach = profile["active_condition_rules"]["breach_mapping"]
    assert breach["any_breached_dwell_requires"] == "STATE_UNCHANGED_BEYOND_EXPECTED_DWELL"
    assert breach["state_unchanged_beyond_expected_dwell_requires_any_breached_dwell"] is True


def validate_capsule_semantics(capsule: dict, profile: dict, profile_sha: str) -> None:
    if capsule["profile_sha256"] != profile_sha:
        raise ValueError("capsule profile_sha256 does not bind the exact profile bytes")

    observed = parse_utc(capsule["observation"]["observed_at_utc"])
    next_due = parse_utc(capsule["observation"]["next_publication_due_utc"])
    if next_due <= observed:
        raise ValueError("next_publication_due_utc must be after observed_at_utc")

    if capsule["evidence"] != sorted(capsule["evidence"], key=lambda row: row["source_id"]):
        raise ValueError("evidence must be ordered by source_id")
    if capsule["observation"]["dwell"] != sorted(
        capsule["observation"]["dwell"], key=lambda row: row["state_id"]
    ):
        raise ValueError("dwell must be ordered by state_id")
    if capsule["active_conditions"]["codes"] != sorted(capsule["active_conditions"]["codes"]):
        raise ValueError("active condition codes must be lexicographically ordered")
    if capsule["material_delta"]["codes"] != sorted(capsule["material_delta"]["codes"]):
        raise ValueError("material delta codes must be lexicographically ordered")

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
        expected_breached = (
            observed - since
        ).total_seconds() >= dwell["expected_max_dwell_seconds"]
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
            "active_conditions do not equal dwell-derived conditions: "
            f"expected={sorted(expected_active)} actual={sorted(actual_active)}"
        )
    if capsule["active_conditions"]["present"] is not bool(expected_active):
        raise ValueError("active_conditions.present disagrees with derived condition set")

    expected_source_hash = compute_source_state_hash(capsule)
    if capsule["observation"]["source_state_hash"] != expected_source_hash:
        raise ValueError("source_state_hash does not match exact comparison state")
    expected_capsule_id = compute_capsule_id(capsule)
    if capsule["capsule_id"] != expected_capsule_id:
        raise ValueError("capsule_id does not hash the exact capsule payload")


def derive_delta_codes(previous: dict, current: dict) -> list[str]:
    codes = []
    if previous["producer"]["build_sha256"] != current["producer"]["build_sha256"]:
        codes.append("PRODUCER_BUILD_CHANGED")
    if previous["evidence"] != current["evidence"]:
        codes.append("EVIDENCE_CHANGED")
    if previous["observation"]["dwell"] != current["observation"]["dwell"]:
        codes.append("DWELL_STATE_CHANGED")
    if previous["active_conditions"] != current["active_conditions"]:
        codes.append("ACTIVE_CONDITION_SET_CHANGED")
    return sorted(codes)


def validate_transition(previous: dict, current: dict) -> None:
    if current["previous_capsule_id"] != previous["capsule_id"]:
        raise ValueError("current previous_capsule_id does not bind exact predecessor")
    if current["profile_sha256"] != previous["profile_sha256"]:
        raise ValueError("profile changed inside one v1 transition chain")
    if current["producer"]["instance_id_sha256"] != previous["producer"]["instance_id_sha256"]:
        raise ValueError("producer instance changed inside one transition chain")
    if parse_utc(current["observation"]["observed_at_utc"]) < parse_utc(
        previous["observation"]["observed_at_utc"]
    ):
        raise ValueError("current observation precedes predecessor observation")

    derived = derive_delta_codes(previous, current)
    if derived:
        if current["observation"]["source_state_hash"] == previous["observation"]["source_state_hash"]:
            raise ValueError("derived delta did not change comparison-state hash")
        if current["transition_claim"] != "DELTA":
            raise ValueError("derived delta requires DELTA transition_claim")
        if current["material_delta"] != {"present": True, "codes": derived}:
            raise ValueError(f"material_delta must equal derived codes {derived}")
    else:
        if current["observation"]["source_state_hash"] != previous["observation"]["source_state_hash"]:
            raise ValueError("no derived delta but comparison-state hash changed")
        if current["transition_claim"] != "NO_DELTA":
            raise ValueError("unchanged comparison state requires NO_DELTA")
        if current["material_delta"] != {"present": False, "codes": []}:
            raise ValueError("NO_DELTA requires empty material_delta")


def main() -> None:
    schema_bytes, schema = load(SCHEMA_PATH)
    profile_bytes, profile = load(PROFILE_PATH)
    _, fixture_bundle = load(FIXTURES_PATH)

    schema_sha = sha256_bytes(schema_bytes)
    profile_sha = sha256_bytes(profile_bytes)
    assert schema_sha == EXPECTED_SCHEMA_SHA256, (
        f"schema digest moved: expected {EXPECTED_SCHEMA_SHA256}, observed {schema_sha}"
    )
    assert profile["capsule_schema_sha256"] == schema_sha, "profile does not bind current schema bytes"

    Draft202012Validator.check_schema(schema)
    schema_validator = Draft202012Validator(schema)
    validate_profile_schema_parity(schema, profile)

    for vector in profile["canonicalization_test_vectors"]:
        canonical = canonical_json(json.loads(vector["input_json"]))
        assert canonical == vector["canonical_json"], f"canonicalization vector {vector['name']} differs"
        assert sha256_bytes(canonical.encode("utf-8")) == vector["sha256"]

    fixture_profile_alias = fixture_bundle["profile_sha256"]
    base_capsule = copy.deepcopy(fixture_bundle["base_capsule"])
    if base_capsule["profile_sha256"] == fixture_profile_alias:
        base_capsule["profile_sha256"] = profile_sha

    failures = []
    for fixture in fixture_bundle["fixtures"]:
        capsule = deep_merge(base_capsule, fixture["patch"])
        capsule = seal_capsule(capsule, profile_sha)
        valid = True
        detail = ""
        try:
            schema_validator.validate(capsule)
            validate_capsule_semantics(capsule, profile, profile_sha)
        except (ValidationError, ValueError, AssertionError) as exc:
            valid = False
            detail = str(exc).splitlines()[0]
        if valid != fixture["expected_valid"]:
            failures.append((fixture["name"], valid, detail))
            print(f"FAIL {fixture['name']}: observed_valid={valid} {detail}")
        else:
            suffix = "" if valid else f" ({detail})"
            print(f"PASS {fixture['name']}: observed_valid={valid}{suffix}")

    # Explicit hash refusal probes.
    valid_base = seal_capsule(base_capsule, profile_sha)
    schema_validator.validate(valid_base)
    validate_capsule_semantics(valid_base, profile, profile_sha)

    stale_source = copy.deepcopy(valid_base)
    stale_source["evidence"][0]["digest"] = "9" * 64
    try:
        validate_capsule_semantics(stale_source, profile, profile_sha)
        failures.append(("reject_stale_source_state_hash", True, ""))
        print("FAIL reject_stale_source_state_hash")
    except ValueError as exc:
        print(f"PASS reject_stale_source_state_hash: {exc}")

    stale_capsule = copy.deepcopy(valid_base)
    stale_capsule["proposal"]["next_action_code"] = "REVIEW_LOCAL_STATE"
    try:
        validate_capsule_semantics(stale_capsule, profile, profile_sha)
        failures.append(("reject_stale_capsule_id", True, ""))
        print("FAIL reject_stale_capsule_id")
    except ValueError as exc:
        print(f"PASS reject_stale_capsule_id: {exc}")

    stale_profile = copy.deepcopy(valid_base)
    stale_profile["profile_sha256"] = fixture_profile_alias
    stale_profile["observation"]["source_state_hash"] = compute_source_state_hash(stale_profile)
    stale_profile["capsule_id"] = compute_capsule_id(stale_profile)
    try:
        validate_capsule_semantics(stale_profile, profile, profile_sha)
        failures.append(("reject_stale_profile_binding", True, ""))
        print("FAIL reject_stale_profile_binding")
    except ValueError as exc:
        print(f"PASS reject_stale_profile_binding: {exc}")

    # Predecessor / transition probes.
    previous = valid_base
    no_delta = copy.deepcopy(previous)
    no_delta["previous_capsule_id"] = previous["capsule_id"]
    no_delta["observation"]["observed_at_utc"] = "2026-09-03T09:00:00Z"
    no_delta["observation"]["next_publication_due_utc"] = "2026-09-03T21:00:00Z"
    no_delta["transition_claim"] = "NO_DELTA"
    no_delta["material_delta"] = {"present": False, "codes": []}
    no_delta = seal_capsule(no_delta, profile_sha)
    validate_capsule_semantics(no_delta, profile, profile_sha)
    validate_transition(previous, no_delta)
    print("PASS exact predecessor NO_DELTA transition")

    build_delta = copy.deepcopy(no_delta)
    build_delta["previous_capsule_id"] = no_delta["capsule_id"]
    build_delta["producer"]["build_sha256"] = "e" * 64
    build_delta["observation"]["observed_at_utc"] = "2026-09-03T10:00:00Z"
    build_delta["observation"]["next_publication_due_utc"] = "2026-09-03T22:00:00Z"
    build_delta["transition_claim"] = "DELTA"
    build_delta["material_delta"] = {"present": True, "codes": ["PRODUCER_BUILD_CHANGED"]}
    build_delta = seal_capsule(build_delta, profile_sha)
    validate_capsule_semantics(build_delta, profile, profile_sha)
    validate_transition(no_delta, build_delta)
    print("PASS producer build change is derivable DELTA")

    false_no_delta = copy.deepcopy(build_delta)
    false_no_delta["transition_claim"] = "NO_DELTA"
    false_no_delta["material_delta"] = {"present": False, "codes": []}
    false_no_delta = seal_capsule(false_no_delta, profile_sha)
    try:
        validate_transition(no_delta, false_no_delta)
        failures.append(("reject_build_change_as_no_delta", True, ""))
        print("FAIL reject_build_change_as_no_delta")
    except ValueError as exc:
        print(f"PASS reject_build_change_as_no_delta: {exc}")

    wrong_predecessor = copy.deepcopy(no_delta)
    wrong_predecessor["previous_capsule_id"] = "sha256:" + "f" * 64
    wrong_predecessor = seal_capsule(wrong_predecessor, profile_sha)
    try:
        validate_transition(previous, wrong_predecessor)
        failures.append(("reject_wrong_predecessor", True, ""))
        print("FAIL reject_wrong_predecessor")
    except ValueError as exc:
        print(f"PASS reject_wrong_predecessor: {exc}")

    if failures:
        raise SystemExit(1)

    print(f"PASS exact schema sha256: {schema_sha}")
    print(f"PASS exact profile sha256: {profile_sha}")
    print(f"PASS capsule fixture bundle: {len(fixture_bundle['fixtures'])} cases")
    print("PASS comparison-state hash, capsule-id and predecessor transition semantics")


if __name__ == "__main__":
    main()
