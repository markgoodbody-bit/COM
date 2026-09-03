#!/usr/bin/env python3
import copy
import hashlib
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "BOUNDED_ADAPTATION_CYCLE_RECEIPT_SCHEMA_V0_20260902.json"
PROFILE_PATH = ROOT / "BOUNDED_ADAPTATION_PROFILE_V0_20260902.json"
CONSTITUTION_PATH = ROOT / "BOUNDED_ADAPTATION_CONSTITUTION_V0_20260902.json"
FIXTURES_PATH = ROOT / "BOUNDED_ADAPTATION_V0_FIXTURES_20260902.json"


def fail(path, message): raise ValueError(f"{path}: {message}")
def digest(data): return hashlib.sha256(data).hexdigest()
def canonical_bytes(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def type_ok(value, expected):
    if expected == "object": return isinstance(value, dict)
    if expected == "array": return isinstance(value, list)
    if expected == "string": return isinstance(value, str)
    if expected == "integer": return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number": return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null": return value is None
    if expected == "boolean": return isinstance(value, bool)
    return False


def validate_schema(value, schema, path="$"):
    if "oneOf" in schema:
        matches = 0
        for option in schema["oneOf"]:
            try: validate_schema(value, option, path); matches += 1
            except ValueError: pass
        if matches != 1: fail(path, f"oneOf matched {matches} branches")
        return
    if "const" in schema and value != schema["const"]: fail(path, f"expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]: fail(path, f"value {value!r} is not in enum")
    t = schema.get("type")
    if t and not type_ok(value, t): fail(path, f"expected type {t}")
    if t == "object":
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value: fail(path, f"missing required property {key}")
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(props)
            if extra: fail(path, f"unexpected properties {sorted(extra)}")
        for key, child in props.items():
            if key in value: validate_schema(value[key], child, f"{path}.{key}")
    elif t == "array":
        if "minItems" in schema and len(value) < schema["minItems"]: fail(path, "too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]: fail(path, "too many items")
        if schema.get("uniqueItems"):
            enc = [json.dumps(x, sort_keys=True, separators=(",", ":")) for x in value]
            if len(enc) != len(set(enc)): fail(path, "items are not unique")
        if "items" in schema:
            for i, item in enumerate(value): validate_schema(item, schema["items"], f"{path}[{i}]")
    elif t in {"integer", "number"}:
        if "minimum" in schema and value < schema["minimum"]: fail(path, f"value {value} is below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]: fail(path, f"value {value} exceeds maximum {schema['maximum']}")
    elif t == "string" and "pattern" in schema and re.search(schema["pattern"], value) is None:
        fail(path, f"value does not match pattern {schema['pattern']}")


def parse_utc(value, path):
    try: parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc: fail(path, f"invalid timestamp: {exc}")
    if parsed.tzinfo is None: fail(path, "timestamp must be timezone-aware")
    return parsed


def contract_bindings(schema_bytes, profile, profile_bytes, constitution_bytes):
    sd, pd, cd = digest(schema_bytes), digest(profile_bytes), digest(constitution_bytes)
    if profile["receipt_schema_sha256"] != sd: fail("profile.receipt_schema_sha256", f"does not bind receipt schema {sd}")
    if profile["constitution_sha256"] != cd: fail("profile.constitution_sha256", f"does not bind constitution {cd}")
    return sd, pd, cd


def validate_profile(receipt, profile, profile_digest, constitution_digest):
    if receipt["profile_sha256"] != profile_digest: fail("$.profile_sha256", f"does not match profile bytes {profile_digest}")
    if receipt["constitution_sha256"] != constitution_digest: fail("$.constitution_sha256", f"does not match constitution bytes {constitution_digest}")

    budget_map = {
        "wall_clock_seconds":"max_wall_clock_seconds", "public_source_reads":"max_public_source_reads",
        "external_source_domains":"max_external_source_domains", "project_aperture_requests":"max_project_aperture_requests",
        "repo_mutating_calls":"max_repo_mutating_calls", "new_branches":"max_new_branches",
        "new_pull_requests":"max_new_pull_requests", "record_bytes":"max_cycle_record_bytes",
        "provider_spend_usd":"provider_spend_usd",
    }
    for field, pfield in budget_map.items():
        if receipt["budget_used"][field] > profile["cycle_budget"][pfield]: fail(f"$.budget_used.{field}", "exceeds profile budget")

    reqs = profile["temporary_move_requirements"]
    for i, adaptation in enumerate(receipt["temporary_adaptations"]):
        move = adaptation["move"]
        if move not in reqs: fail(f"$.temporary_adaptations[{i}].move", "is not adaptive in v0")
        if reqs[move].get("expires_at_utc_required") and not adaptation.get("expires_at_utc"): fail(f"$.temporary_adaptations[{i}].expires_at_utc", "required")
        if reqs[move].get("default_reversion_required") and not adaptation.get("default_reversion_code"): fail(f"$.temporary_adaptations[{i}].default_reversion_code", "required")


def validate_semantics(receipt, profile):
    if not receipt["source_refs"]: fail("$.source_refs", "must name at least one observed source basis")
    started, completed = parse_utc(receipt["started_at_utc"], "$.started_at_utc"), parse_utc(receipt["completed_at_utc"], "$.completed_at_utc")
    if completed < started: fail("$.completed_at_utc", "may not precede started_at_utc")

    elapsed = math.ceil((completed - started).total_seconds())
    if receipt["budget_used"]["wall_clock_seconds"] < elapsed:
        fail("$.budget_used.wall_clock_seconds", f"under-reports observable elapsed span {elapsed}")
    measured_bytes = len(canonical_bytes(receipt))
    if receipt["budget_used"]["record_bytes"] < measured_bytes:
        fail("$.budget_used.record_bytes", f"under-reports canonical receipt size {measured_bytes}")

    deltas = receipt["material_delta_codes"]
    if not deltas: fail("$.material_delta_codes", "must state a delta or NO_MATERIAL_DELTA")
    if "NO_MATERIAL_DELTA" in deltas and deltas != ["NO_MATERIAL_DELTA"]: fail("$.material_delta_codes", "NO_MATERIAL_DELTA must be exclusive")
    unknowns = receipt["unknown_codes"]
    if not unknowns: fail("$.unknown_codes", "must state NONE or unknowns")
    if "NONE" in unknowns and unknowns != ["NONE"]: fail("$.unknown_codes", "NONE must be exclusive")

    result, moves = receipt["result"], receipt["moves_selected"]
    if result == "MOVED":
        if not moves or moves == ["NO_MATERIAL_MOVE"]: fail("$.moves_selected", "MOVED requires an actual move")
        if deltas == ["NO_MATERIAL_DELTA"]: fail("$.material_delta_codes", "MOVED cannot claim NO_MATERIAL_DELTA")
    elif result == "NO_MATERIAL_MOVE":
        if moves != ["NO_MATERIAL_MOVE"]: fail("$.moves_selected", "NO_MATERIAL_MOVE result requires exactly that move")
        if deltas != ["NO_MATERIAL_DELTA"]: fail("$.material_delta_codes", "NO_MATERIAL_MOVE requires NO_MATERIAL_DELTA")
    elif result == "PAUSED" and "PAUSE" not in moves: fail("$.moves_selected", "PAUSED requires PAUSE")
    elif result == "ESCALATED" and "ESCALATE" not in moves: fail("$.moves_selected", "ESCALATED requires ESCALATE")

    adaptations = receipt["temporary_adaptations"]
    for i, adaptation in enumerate(adaptations):
        if adaptation["move"] not in moves: fail(f"$.temporary_adaptations[{i}].move", "must also appear in moves_selected")
        expires = parse_utc(adaptation["expires_at_utc"], f"$.temporary_adaptations[{i}].expires_at_utc")
        if expires <= completed: fail(f"$.temporary_adaptations[{i}].expires_at_utc", "must be after completed_at_utc")
    if "REPRIORITISE" in moves:
        reps = [a for a in adaptations if a["move"] == "REPRIORITISE"]
        if len(reps) != 1: fail("$.temporary_adaptations", "selected REPRIORITISE requires exactly one live expiry/reversion record")

    lane, age = receipt["oldest_unresolved_lane_code"], receipt["oldest_unresolved_lane_age_seconds"]
    if lane == "NONE" and age is not None: fail("$.oldest_unresolved_lane_age_seconds", "must be null when lane is NONE")
    if lane != "NONE" and age is None: fail("$.oldest_unresolved_lane_age_seconds", "must be present when lane is named")
    if "ACTIVE_LANE_STUCK" in deltas and (lane == "NONE" or age is None or age <= 0):
        fail("$.material_delta_codes", "ACTIVE_LANE_STUCK requires a named aged unresolved lane")

    # v0 has no typed proof surfaces for these conditional moves; refuse rather than infer proof from prose.
    if "DELETE_RECOVERABLE_CANDIDATE" in moves:
        fail("$.moves_selected", "DELETE_RECOVERABLE_CANDIDATE has no typed recovery/target/receipt proof surface in v0; RETIRE or ESCALATE")
    if "CONTACT_EXTERNAL_OWNER" in moves:
        fail("$.moves_selected", "CONTACT_EXTERNAL_OWNER has no typed standing-grant proof surface in v0")

    authority_order = {"NONE":0, "A":1, "B":2}
    required = 0
    for move in moves:
        cls = profile["move_classes"].get(move)
        if cls in authority_order: required = max(required, authority_order[cls])
        elif cls in {"GRANT_DEPENDENT", "RECOVERY_PROOF_REQUIRED"}: continue
        else: fail("$.moves_selected", f"unknown move class for {move}")
    if authority_order[receipt["authority_class_max"]] < required:
        fail("$.authority_class_max", f"understates selected move authority; requires class {['NONE','A','B'][required]}")


def validate_receipt(receipt, schema, profile, pd, cd):
    validate_schema(receipt, schema); validate_profile(receipt, profile, pd, cd); validate_semantics(receipt, profile)


def expect_reject(label, receipt, schema, profile, pd, cd):
    try: validate_receipt(receipt, schema, profile, pd, cd)
    except ValueError as exc: print(f"PASS {label}: {exc}"); return
    print(f"FAIL {label}: receipt was accepted"); raise SystemExit(1)


def main():
    schema_bytes = SCHEMA_PATH.read_bytes(); schema = json.loads(schema_bytes)
    profile_bytes = PROFILE_PATH.read_bytes(); profile = json.loads(profile_bytes)
    constitution_bytes = CONSTITUTION_PATH.read_bytes(); bundle = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    sd, pd, cd = contract_bindings(schema_bytes, profile, profile_bytes, constitution_bytes)
    alias = bundle["profile_sha256"]

    positive = None
    for fixture in bundle["fixtures"]:
        receipt = copy.deepcopy(fixture["receipt"])
        if receipt.get("profile_sha256") == alias: receipt["profile_sha256"] = pd
        valid, error = True, None
        try: validate_receipt(receipt, schema, profile, pd, cd)
        except ValueError as exc: valid, error = False, str(exc)
        if valid != fixture["expected_valid"]:
            print(f"FAIL {fixture['name']}: observed_valid={valid} {error or ''}"); raise SystemExit(1)
        print(f"PASS {fixture['name']}: observed_valid={valid}" + ("" if valid else f" ({error})"))
        if fixture["expected_valid"] and positive is None: positive = receipt

    if positive is None: raise SystemExit("no positive fixture")
    stale = copy.deepcopy(positive); stale["profile_sha256"] = alias
    expect_reject("reject_stale_profile_binding", stale, schema, profile, pd, cd)

    probes = []
    x = copy.deepcopy(positive); x["temporary_adaptations"] = []; probes.append(("reject_reprioritise_without_temporary_record", x))
    x = copy.deepcopy(positive); x["budget_used"]["wall_clock_seconds"] = 1; probes.append(("reject_underreported_wall_clock", x))
    x = copy.deepcopy(positive); x["budget_used"]["record_bytes"] = 1; probes.append(("reject_underreported_record_bytes", x))
    x = copy.deepcopy(positive); x["moves_selected"] = ["DELETE_RECOVERABLE_CANDIDATE"]; probes.append(("reject_unproved_delete", x))
    x = copy.deepcopy(positive); x["moves_selected"] = ["REQUEST_APERTURE"]; x["temporary_adaptations"] = []; x["authority_class_max"] = "NONE"; probes.append(("reject_understated_class_b", x))
    x = copy.deepcopy(positive); x["material_delta_codes"] = ["ACTIVE_LANE_STUCK"]; x["oldest_unresolved_lane_code"] = "NONE"; x["oldest_unresolved_lane_age_seconds"] = None; probes.append(("reject_stuck_without_aged_lane", x))
    x = copy.deepcopy(positive); x["moves_selected"] = ["CONTACT_EXTERNAL_OWNER"]; x["temporary_adaptations"] = []; probes.append(("reject_contact_without_typed_grant", x))
    for label, receipt in probes: expect_reject(label, receipt, schema, profile, pd, cd)

    print(f"PASS exact receipt schema sha256: {sd}")
    print(f"PASS exact profile sha256: {pd}")
    print(f"PASS exact constitution sha256: {cd}")
    print(f"PASS all {len(bundle['fixtures'])} committed fixtures plus {1+len(probes)} hostile binding/semantic probes")

if __name__ == "__main__": sys.exit(main())
