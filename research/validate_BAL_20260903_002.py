#!/usr/bin/env python3
"""Validate the first real bounded-adaptation v0 cycle receipt against its exact contract."""

import json
from pathlib import Path

import validate_bounded_adaptation_v0_fixtures as v

ROOT = Path(__file__).resolve().parent
RECEIPT_PATH = ROOT / "adaptation_cycles" / "BAL_20260903_002.json"

schema_bytes = v.SCHEMA_PATH.read_bytes()
schema = json.loads(schema_bytes)
profile_bytes = v.PROFILE_PATH.read_bytes()
profile = json.loads(profile_bytes)
constitution_bytes = v.CONSTITUTION_PATH.read_bytes()
_, pd, cd = v.contract_bindings(schema_bytes, profile, profile_bytes, constitution_bytes)
receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))

v.validate_receipt(receipt, schema, profile, pd, cd)
print(f"PASS real cycle receipt {receipt['cycle_id']} against exact current v0 contract")
