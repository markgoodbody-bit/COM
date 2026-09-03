#!/usr/bin/env python3
"""Exercise the v0 deletion refusal without an unrelated temporary-adaptation failure."""

import copy
import json
from pathlib import Path

import validate_bounded_adaptation_v0_fixtures as v

ROOT = Path(__file__).resolve().parent

schema_bytes = v.SCHEMA_PATH.read_bytes()
schema = json.loads(schema_bytes)
profile_bytes = v.PROFILE_PATH.read_bytes()
profile = json.loads(profile_bytes)
constitution_bytes = v.CONSTITUTION_PATH.read_bytes()
bundle = json.loads(v.FIXTURES_PATH.read_text(encoding="utf-8"))
_, pd, cd = v.contract_bindings(schema_bytes, profile, profile_bytes, constitution_bytes)

source = next(item["receipt"] for item in bundle["fixtures"] if item["expected_valid"])
receipt = copy.deepcopy(source)
if receipt.get("profile_sha256") == bundle["profile_sha256"]:
    receipt["profile_sha256"] = pd

# Remove the positive fixture's reprioritisation record so the probe reaches the
# deletion gate itself rather than failing on an unrelated adaptation mismatch.
receipt["moves_selected"] = ["DELETE_RECOVERABLE_CANDIDATE"]
receipt["temporary_adaptations"] = []

try:
    v.validate_receipt(receipt, schema, profile, pd, cd)
except ValueError as exc:
    message = str(exc)
    expected = "DELETE_RECOVERABLE_CANDIDATE has no typed recovery/target/receipt proof surface in v0"
    if expected not in message:
        raise SystemExit(f"FAIL clean deletion probe reached wrong refusal: {message}")
    print(f"PASS clean deletion probe reached intended refusal: {message}")
else:
    raise SystemExit("FAIL clean deletion probe was accepted")
