#!/usr/bin/env python3
import hashlib
import json
import re
import sys
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
