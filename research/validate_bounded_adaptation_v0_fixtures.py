#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "BOUNDED_ADAPTATION_CYCLE_RECEIPT_SCHEMA_V0_20260902.json"
PROFILE_PATH = ROOT / "BOUNDED_ADAPTATION_PROFILE_V0_20260902.json"
FIXTURES_PATH = ROOT / "BOUNDED_ADAPTATION_V0_FIXTURES_20260902.json"


def fail(path, message):
    raise ValueError(f"{path}: {message}")


def type_ok(value, expected):
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    return False


def validate_schema(value, schema, path="$"):
    if "oneOf" in schema:
        matches = 0
        for option in schema["oneOf"]:
            try:
                validate_schema(value, option, path)
                matches += 1
            except ValueError:
                pass
        if matches != 1:
            fail(path, f"oneOf matched {matches} branches")
        return

    if "const" in schema and value != schema["const"]:
        fail(path, f"expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        fail(path, f"value {value!r} is not in enum")

    expected_type = schema.get("type")
    if expected_type and not type_ok(value, expected_type):
        fail(path, f"expected type {expected_type}")
    if expected_type == "object":
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                fail(path, f"missing required property {key}")
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                fail(path, f"unexpected properties {sorted(extra)}")
        for key, child in properties.items():
            if key in value:
                validate_schema(value[key], child, f"{path}.{key}")
    elif expected_type == "array":
        if "minItems" in schema and len(value) < schema["minItems"]:
            fail(path, f"has {len(value)} items; minimum is {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            fail(path, f"has {len(value)} items; maximum is {schema['maxItems']}")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            if len(encoded) != len(set(encoded)):
                fail(path, "items are not unique")
        if "items" in schema:
            for index, item in enumerate(value):
                validate_schema(item, schema["items"], f"{path}[{index}]")
    elif expected_type in {"integer", "number"}:
        if "minimum" in schema and value < schema["minimum"]:
            fail(path, f"value {value} is below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            fail(path, f"value {value} exceeds maximum {schema['maximum']}")
    elif expected_type == "string" and "pattern" in schema:
        if re.search(schema["pattern"], value) is None:
            fail(path, f"value does not match pattern {schema['pattern']}")


def parse_utc(value, path):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        fail(path, f"invalid timestamp: {exc}")
    if parsed.tzinfo is None:
        fail(path, "timestamp must be timezone-aware")
    return parsed


def validate_profile(receipt, profile, profile_bytes):
    digest = hashlib.sha256(profile_bytes).hexdigest()
    if receipt["profile_sha256"] != digest:
        fail("$.profile_sha256", f"does not match profile bytes {digest}")
    if receipt["constitution_sha256"] != profile["constitution_sha256"]:
        fail("$.constitution_sha256", "does not match profile constitution")

    budget_map = {
        "wall_clock_seconds": "max_wall_clock_seconds",
        "public_source_reads": "max_public_source_reads",
        "external_source_domains": "max_external_source_domains",
        "project_aperture_requests": "max_project_aperture_requests",
        "repo_mutating_calls": "max_repo_mutating_calls",
        "new_branches": "max_new_branches",
        "new_pull_requests": "max_new_pull_requests",
        "record_bytes": "max_cycle_record_bytes",
        "provider_spend_usd": "provider_spend_usd",
    }
    for field, profile_field in budget_map.items():
        if receipt["budget_used"][field] > profile["cycle_budget"][profile_field]:
            fail(f"$.budget_used.{field}", "exceeds profile budget")

    requirements = profile["temporary_move_requirements"]
    for index, adaptation in enumerate(receipt["temporary_adaptations"]):
        move = adaptation["move"]
        if move not in requirements:
            fail(f"$.temporary_adaptations[{index}].move", "is not adaptive in v0")
        rule = requirements[move]
        if rule.get("expires_at_utc_required") and not adaptation.get("expires_at_utc"):
            fail(f"$.temporary_adaptations[{index}].expires_at_utc", "is required by profile")
        if rule.get("default_reversion_required") and not adaptation.get("default_reversion_code"):
            fail(f"$.temporary_adaptations[{index}].default_reversion_code", "is required by profile")


def validate_semantics(receipt):
    if not receipt["source_refs"]:
        fail("$.source_refs", "must name at least one observed source basis")

    started = parse_utc(receipt["started_at_utc"], "$.started_at_utc")
    completed = parse_utc(receipt["completed_at_utc"], "$.completed_at_utc")
    if completed < started:
        fail("$.completed_at_utc", "may not precede started_at_utc")

    deltas = receipt["material_delta_codes"]
    if not deltas:
        fail("$.material_delta_codes", "must explicitly state a material delta or NO_MATERIAL_DELTA")
    if "NO_MATERIAL_DELTA" in deltas and deltas != ["NO_MATERIAL_DELTA"]:
        fail("$.material_delta_codes", "NO_MATERIAL_DELTA must be exclusive")

    unknowns = receipt["unknown_codes"]
    if not unknowns:
        fail("$.unknown_codes", "must explicitly state NONE or one or more unknowns")
    if "NONE" in unknowns and unknowns != ["NONE"]:
        fail("$.unknown_codes", "NONE must be exclusive")

    result = receipt["result"]
    moves = receipt["moves_selected"]
    if result == "MOVED":
        if not moves or moves == ["NO_MATERIAL_MOVE"]:
            fail("$.moves_selected", "MOVED requires at least one actual move")
        if deltas == ["NO_MATERIAL_DELTA"]:
            fail("$.material_delta_codes", "MOVED cannot claim NO_MATERIAL_DELTA")
    elif result == "NO_MATERIAL_MOVE":
        if moves != ["NO_MATERIAL_MOVE"]:
            fail("$.moves_selected", "NO_MATERIAL_MOVE result requires exactly the NO_MATERIAL_MOVE move")
        if deltas != ["NO_MATERIAL_DELTA"]:
            fail("$.material_delta_codes", "NO_MATERIAL_MOVE result requires NO_MATERIAL_DELTA")
    elif result == "PAUSED" and "PAUSE" not in moves:
        fail("$.moves_selected", "PAUSED result requires PAUSE")
    elif result == "ESCALATED" and "ESCALATE" not in moves:
        fail("$.moves_selected", "ESCALATED result requires ESCALATE")

    for index, adaptation in enumerate(receipt["temporary_adaptations"]):
        if adaptation["move"] not in moves:
            fail(f"$.temporary_adaptations[{index}].move", "must also appear in moves_selected")
        expires = parse_utc(adaptation["expires_at_utc"], f"$.temporary_adaptations[{index}].expires_at_utc")
        if expires <= completed:
            fail(f"$.temporary_adaptations[{index}].expires_at_utc", "must be after completed_at_utc")

    lane = receipt["oldest_unresolved_lane_code"]
    age = receipt["oldest_unresolved_lane_age_seconds"]
    if lane == "NONE" and age is not None:
        fail("$.oldest_unresolved_lane_age_seconds", "must be null when oldest_unresolved_lane_code is NONE")
    if lane != "NONE" and age is None:
        fail("$.oldest_unresolved_lane_age_seconds", "must be present when an unresolved lane is named")


def main():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    profile_bytes = PROFILE_PATH.read_bytes()
    profile = json.loads(profile_bytes)
    bundle = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))

    failures = []
    for fixture in bundle["fixtures"]:
        valid = True
        error = None
        try:
            validate_schema(fixture["receipt"], schema)
            validate_profile(fixture["receipt"], profile, profile_bytes)
            validate_semantics(fixture["receipt"])
        except ValueError as exc:
            valid = False
            error = str(exc)
        if valid != fixture["expected_valid"]:
            failures.append((fixture["name"], valid, error))
        status = "PASS" if valid == fixture["expected_valid"] else "FAIL"
        detail = "" if error is None else f" ({error})"
        print(f"{status} {fixture['name']}: observed_valid={valid}{detail}")

    if failures:
        return 1
    print(f"PASS all {len(bundle['fixtures'])} bounded-adaptation v0 fixtures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
