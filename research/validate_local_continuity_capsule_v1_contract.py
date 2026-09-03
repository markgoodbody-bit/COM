#!/usr/bin/env python3
"""Exact byte, hash, state and transition checks for Local Continuity Capsule v1.

Research contract only: no live-host observation, publishing, credentials, models,
spend, external actuation or authority grant.
"""
from __future__ import annotations
import copy, hashlib, json
from datetime import datetime
from pathlib import Path
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "research" / "LOCAL_CONTINUITY_CAPSULE_V1_SCHEMA_20260902.json"
PROFILE_PATH = ROOT / "research" / "LOCAL_CONTINUITY_CAPSULE_V1_PROFILE_20260902.json"
FIXTURES_PATH = ROOT / "research" / "LOCAL_CONTINUITY_CAPSULE_V1_FIXTURES_20260903.json"
EXPECTED_SCHEMA_SHA256 = "18e52c4c2746998db23f17c39ceb9aa4a055342991bdef83614399bd5e3fc932"


def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def load(path: Path):
    raw = path.read_bytes(); return raw, json.loads(raw)
def utc(value: str) -> datetime: return datetime.fromisoformat(value.replace("Z", "+00:00"))
def canon(value) -> str: return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def merge(base: dict, patch: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in patch.items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else copy.deepcopy(v)
    return out


def comparison_state(c):
    return {
        "producer_build_sha256": c["producer"]["build_sha256"],
        "evidence": c["evidence"],
        "dwell": c["observation"]["dwell"],
        "active_conditions": c["active_conditions"],
    }


def source_hash(c): return sha(canon(comparison_state(c)).encode())
def capsule_id(c):
    payload = copy.deepcopy(c); payload.pop("capsule_id", None)
    return "sha256:" + sha(canon(payload).encode())


def seal(c, profile_sha):
    c = copy.deepcopy(c)
    c["profile_sha256"] = profile_sha
    c["observation"]["source_state_hash"] = source_hash(c)
    c["capsule_id"] = capsule_id(c)
    return c


def parity(schema, profile):
    sm = set(schema["properties"]["material_delta"]["properties"]["codes"]["items"]["enum"])
    sa = set(schema["properties"]["active_conditions"]["properties"]["codes"]["items"]["enum"])
    assert set(profile["material_delta_codes"]) == sm
    assert set(profile["active_condition_codes"]) == sa
    assert profile["cardinality"]["material_delta_codes_max"] == len(sm)
    assert profile["cardinality"]["active_condition_codes_max"] == len(sa)

    sd = {}
    for option in schema["$defs"]["dwell_entry"]["oneOf"]:
        p = option["properties"]
        sd[p["state_id"]["const"]] = (p["threshold_id"]["const"], p["expected_max_dwell_seconds"]["const"], p["threshold_authority"]["const"])
    pd = {r["state_id"]: (r["threshold_id"], r["expected_max_dwell_seconds"], r["authority"]) for r in profile["dwell_thresholds"]}
    assert sd == pd
    rules = {r["state_id"]: r["active_condition_code"] for r in profile["active_condition_rules"]["specific_state_mapping"]}
    assert set(rules) == set(sd)
    assert profile["active_condition_rules"]["breach_mapping"]["any_breached_dwell_requires"] == "STATE_UNCHANGED_BEYOND_EXPECTED_DWELL"
    return rules


def validate_capsule(c, profile, profile_sha, rules):
    if c["profile_sha256"] != profile_sha: raise ValueError("profile_sha256 does not bind exact profile")
    observed, due = utc(c["observation"]["observed_at_utc"]), utc(c["observation"]["next_publication_due_utc"])
    if due <= observed: raise ValueError("publication deadline must follow observation")
    if c["evidence"] != sorted(c["evidence"], key=lambda r: r["source_id"]): raise ValueError("evidence ordering")
    if c["observation"]["dwell"] != sorted(c["observation"]["dwell"], key=lambda r: r["state_id"]): raise ValueError("dwell ordering")
    if c["active_conditions"]["codes"] != sorted(c["active_conditions"]["codes"]): raise ValueError("active-condition ordering")
    if c["material_delta"]["codes"] != sorted(c["material_delta"]["codes"]): raise ValueError("delta ordering")

    expected = set(); any_breached = False
    for d in c["observation"]["dwell"]:
        since = utc(d["unchanged_since_utc"])
        if since > observed: raise ValueError("dwell begins after observation")
        breach = (observed - since).total_seconds() >= d["expected_max_dwell_seconds"]
        if d["breached"] is not breach: raise ValueError(f"{d['state_id']} false breached flag")
        expected.add(rules[d["state_id"]]); any_breached |= breach
    if any_breached: expected.add("STATE_UNCHANGED_BEYOND_EXPECTED_DWELL")
    actual = set(c["active_conditions"]["codes"])
    if actual != expected: raise ValueError("active conditions differ from dwell-derived conditions")
    if c["active_conditions"]["present"] is not bool(expected): raise ValueError("active_conditions.present mismatch")
    if c["observation"]["source_state_hash"] != source_hash(c): raise ValueError("source_state_hash mismatch")
    if c["capsule_id"] != capsule_id(c): raise ValueError("capsule_id mismatch")


def delta_codes(a, b):
    codes = []
    if a["producer"]["build_sha256"] != b["producer"]["build_sha256"]: codes.append("PRODUCER_BUILD_CHANGED")
    if a["evidence"] != b["evidence"]: codes.append("EVIDENCE_CHANGED")
    if a["observation"]["dwell"] != b["observation"]["dwell"]: codes.append("DWELL_STATE_CHANGED")
    if a["active_conditions"] != b["active_conditions"]: codes.append("ACTIVE_CONDITION_SET_CHANGED")
    return sorted(codes)


def validate_transition(prev, cur):
    if cur["previous_capsule_id"] != prev["capsule_id"]: raise ValueError("wrong predecessor")
    if cur["profile_sha256"] != prev["profile_sha256"]: raise ValueError("profile changed in chain")
    if cur["producer"]["instance_id_sha256"] != prev["producer"]["instance_id_sha256"]: raise ValueError("producer instance changed in chain")
    if utc(cur["observation"]["observed_at_utc"]) < utc(prev["observation"]["observed_at_utc"]): raise ValueError("backward observation")
    derived = delta_codes(prev, cur)
    if derived:
        if cur["observation"]["source_state_hash"] == prev["observation"]["source_state_hash"]: raise ValueError("delta without comparison-hash change")
        if cur["transition_claim"] != "DELTA": raise ValueError("derived delta requires DELTA")
        if cur["material_delta"] != {"present": True, "codes": derived}: raise ValueError("material_delta differs from derived delta")
    else:
        if cur["observation"]["source_state_hash"] != prev["observation"]["source_state_hash"]: raise ValueError("hash changed without derived delta")
        if cur["transition_claim"] != "NO_DELTA": raise ValueError("unchanged state requires NO_DELTA")
        if cur["material_delta"] != {"present": False, "codes": []}: raise ValueError("NO_DELTA requires empty material_delta")


def expect_reject(label, fn):
    try: fn()
    except (ValueError, ValidationError, AssertionError) as exc:
        print(f"PASS {label}: {str(exc).splitlines()[0]}"); return
    print(f"FAIL {label}"); raise SystemExit(1)


def main():
    schema_bytes, schema = load(SCHEMA_PATH); profile_bytes, profile = load(PROFILE_PATH); _, bundle = load(FIXTURES_PATH)
    schema_sha, profile_sha = sha(schema_bytes), sha(profile_bytes)
    assert schema_sha == EXPECTED_SCHEMA_SHA256
    assert profile["capsule_schema_sha256"] == schema_sha
    Draft202012Validator.check_schema(schema); js = Draft202012Validator(schema)
    rules = parity(schema, profile)
    for v in profile["canonicalization_test_vectors"]:
        c = canon(json.loads(v["input_json"])); assert c == v["canonical_json"] and sha(c.encode()) == v["sha256"]

    alias = bundle["profile_sha256"]; base = copy.deepcopy(bundle["base_capsule"])
    if base["profile_sha256"] == alias: base["profile_sha256"] = profile_sha
    for f in bundle["fixtures"]:
        c = seal(merge(base, f["patch"]), profile_sha); valid = True; detail = ""
        try: js.validate(c); validate_capsule(c, profile, profile_sha, rules)
        except (ValueError, ValidationError, AssertionError) as exc: valid = False; detail = str(exc).splitlines()[0]
        if valid != f["expected_valid"]: print(f"FAIL {f['name']}: {valid} {detail}"); raise SystemExit(1)
        print(f"PASS {f['name']}: observed_valid={valid}" + ("" if valid else f" ({detail})"))

    valid_base = seal(base, profile_sha); js.validate(valid_base); validate_capsule(valid_base, profile, profile_sha, rules)
    bad_source = copy.deepcopy(valid_base); bad_source["evidence"][0]["digest"] = "9"*64
    expect_reject("reject_stale_source_state_hash", lambda: validate_capsule(bad_source, profile, profile_sha, rules))
    bad_id = copy.deepcopy(valid_base); bad_id["proposal"]["next_action_code"] = "REVIEW_LOCAL_STATE"
    expect_reject("reject_stale_capsule_id", lambda: validate_capsule(bad_id, profile, profile_sha, rules))
    bad_profile = copy.deepcopy(valid_base); bad_profile["profile_sha256"] = "0"*64; bad_profile["observation"]["source_state_hash"] = source_hash(bad_profile); bad_profile["capsule_id"] = capsule_id(bad_profile)
    expect_reject("reject_stale_profile_binding", lambda: validate_capsule(bad_profile, profile, profile_sha, rules))

    prev = valid_base
    same = copy.deepcopy(prev); same["previous_capsule_id"] = prev["capsule_id"]; same["observation"]["observed_at_utc"] = "2026-09-03T09:00:00Z"; same["observation"]["next_publication_due_utc"] = "2026-09-03T21:00:00Z"; same["transition_claim"] = "NO_DELTA"; same["material_delta"] = {"present":False,"codes":[]}; same = seal(same, profile_sha)
    validate_capsule(same, profile, profile_sha, rules); validate_transition(prev, same); print("PASS exact predecessor NO_DELTA transition")
    changed = copy.deepcopy(same); changed["previous_capsule_id"] = same["capsule_id"]; changed["producer"]["build_sha256"] = "e"*64; changed["observation"]["observed_at_utc"] = "2026-09-03T10:00:00Z"; changed["observation"]["next_publication_due_utc"] = "2026-09-03T22:00:00Z"; changed["transition_claim"] = "DELTA"; changed["material_delta"] = {"present":True,"codes":["PRODUCER_BUILD_CHANGED"]}; changed = seal(changed, profile_sha)
    validate_capsule(changed, profile, profile_sha, rules); validate_transition(same, changed); print("PASS producer build change is derivable DELTA")
    lied = copy.deepcopy(changed); lied["transition_claim"] = "NO_DELTA"; lied["material_delta"] = {"present":False,"codes":[]}; lied = seal(lied, profile_sha)
    expect_reject("reject_build_change_as_no_delta", lambda: validate_transition(same, lied))
    wrong = copy.deepcopy(same); wrong["previous_capsule_id"] = "sha256:" + "f"*64; wrong = seal(wrong, profile_sha)
    expect_reject("reject_wrong_predecessor", lambda: validate_transition(prev, wrong))

    print(f"PASS exact schema sha256: {schema_sha}"); print(f"PASS exact profile sha256: {profile_sha}")
    print("PASS comparison-state hash, capsule-id and predecessor transition semantics")

if __name__ == "__main__": main()
