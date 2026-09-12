"""Offline Formation Environment v0.2 candidate checks.

Representation consistency only: never truth, permission, standing, goodness or alignment.
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise ValueError("duplicate key: " + key)
        out[key] = value
    return out


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs)


def shape(value, rule, root, at, errors):
    if "$ref" in rule:
        return shape(value, root["$defs"][rule["$ref"].split("/")[-1]], root, at, errors)
    kind = rule.get("type")
    checks = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "boolean": type(value) is bool,
    }
    if kind and not checks.get(kind, False):
        errors.append(f"{at}: expected {kind}")
        return
    if "enum" in rule and value not in rule["enum"]:
        errors.append(f"{at}: invalid enum")
    if isinstance(value, str) and len(value.strip()) < rule.get("minLength", 0):
        errors.append(f"{at}: empty text")
    if isinstance(value, dict):
        for key in rule.get("required", []):
            if key not in value:
                errors.append(f"{at}.{key}: missing")
        props = rule.get("properties", {})
        for key, item in value.items():
            if key not in props:
                if rule.get("additionalProperties") is False:
                    errors.append(f"{at}.{key}: unknown field")
            else:
                shape(item, props[key], root, f"{at}.{key}", errors)
    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            errors.append(f"{at}: too few items")
        if rule.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            errors.append(f"{at}: duplicate items")
        for i, item in enumerate(value):
            shape(item, rule.get("items", {}), root, f"{at}[{i}]", errors)


def check_bound(bound, name, errors):
    kind = bound["kind"]
    has_time = bool(bound["time_value"].strip())
    has_event = bool(bound["event"].strip())
    if kind == "time" and (not has_time or has_event):
        errors.append(f"{name}: time bound needs time_value and no event")
    elif kind == "event" and (has_time or not has_event):
        errors.append(f"{name}: event bound needs event and no time_value")
    elif kind == "time_and_event" and (not has_time or not has_event):
        errors.append(f"{name}: time_and_event needs both")
    elif kind == "unknown" and (has_time or has_event):
        errors.append(f"{name}: unknown must not invent time_value/event")


def validate(record, previous=None):
    schema = read(HERE / "episode.schema.json")
    errors = []
    shape(record, schema, schema, "episode", errors)
    if errors:
        return errors

    groups = ("evidence", "affected", "uncertainties", "challenges", "residue")
    ids = {}
    for group in groups:
        vals = [x["id"] for x in record[group]]
        if len(vals) != len(set(vals)):
            errors.append(group + ": duplicate ids")
        ids[group] = set(vals)

    for uncertainty in record["uncertainties"]:
        if uncertainty["status"] == "resolved" and not uncertainty["resolution_evidence"]:
            errors.append(uncertainty["id"] + ": resolution requires evidence")
        for ref in uncertainty["resolution_evidence"]:
            if ref not in ids["evidence"]:
                errors.append(uncertainty["id"] + ": missing evidence " + ref)

    for challenge in record["challenges"]:
        for ref in challenge["evidence"]:
            if ref not in ids["evidence"]:
                errors.append(challenge["id"] + ": missing evidence " + ref)
        if challenge["status"] != "open" and not challenge["disposition"].strip():
            errors.append(challenge["id"] + ": disposition missing")

    for party in record["affected"]:
        if party["voice"] != "direct" and not party["representation_limit"].strip():
            errors.append(party["id"] + ": non-direct voice needs representation limit")

    if record["action"]["mode"] == "ACT" and record["action"]["scope"] not in record["authority"]["granted_scopes"]:
        errors.append("ACT scope not in recorded grant (record check, not permission)")

    for name in ("detection", "routing", "correction", "hardening"):
        check_bound(record["clocks"][name]["bound"], "clocks." + name, errors)

    window = record["clocks"]["window"]
    if window["assessment"] in {"open", "closed"} and not window["basis_evidence"]:
        errors.append("clocks.window: open/closed assessment needs referenced evidence")
    for ref in window["basis_evidence"]:
        if ref not in ids["evidence"]:
            errors.append("clocks.window: missing evidence " + ref)

    if record["state"] == "closed" and not record["closure_receipt"].strip():
        errors.append("closed episode requires receipt; residue may remain")

    if previous is not None:
        prior_errors = validate(previous)
        if prior_errors:
            return errors + ["previous: " + e for e in prior_errors]
        if previous["episode_id"] != record["episode_id"]:
            errors.append("previous episode id differs")
        for group in groups:
            old = {x["id"] for x in previous[group]}
            now = {x["id"] for x in record[group]}
            missing = old - now
            if missing:
                errors.append(group + ": history removed: " + ", ".join(sorted(missing)))
        evidence_now = {x["id"]: x for x in record["evidence"]}
        for old in previous["evidence"]:
            if old["id"] in evidence_now and evidence_now[old["id"]] != old:
                errors.append(old["id"] + ": earlier evidence rewritten; append correction instead")
        if not set(previous["authority"]["granted_scopes"]).issuperset(record["authority"]["granted_scopes"]):
            if record["authority"]["basis"] == previous["authority"]["basis"]:
                errors.append("wider recorded grant needs changed authority basis, not prior success")

    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path)
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(read(args.episode), read(args.previous) if args.previous else None)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, "INVALID REPRESENTATION: " + str(exc) + "\n")
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("STRUCTURE VALID ONLY: clocks not proven; no permission, standing, goodness or alignment verdict.")


if __name__ == "__main__":
    main()
