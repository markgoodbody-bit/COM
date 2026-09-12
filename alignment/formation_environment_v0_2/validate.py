"""Offline Formation Environment v0.2 candidate checks.

Representation consistency only: never truth, permission, standing, goodness or alignment.
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUPPORTED_SCHEMA_KEYS = {
    "$schema", "title", "$defs", "$ref", "type", "additionalProperties",
    "required", "properties", "enum", "minLength", "minItems",
    "uniqueItems", "items",
}
SUPPORTED_TYPES = {"object", "array", "string", "boolean"}


def pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise ValueError("duplicate key: " + key)
        out[key] = value
    return out


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs)


def schema_contract(rule, root, at="schema", errors=None):
    if errors is None:
        errors = []
    if not isinstance(rule, dict):
        errors.append(f"{at}: schema rule must be an object")
        return errors
    unknown = set(rule) - SUPPORTED_SCHEMA_KEYS
    if unknown:
        errors.append(f"{at}: unsupported schema keyword(s): {', '.join(sorted(unknown))}")
    if "$ref" in rule:
        siblings = set(rule) - {"$ref"}
        if siblings:
            errors.append(f"{at}: assertion/metadata siblings beside $ref are unsupported")
        ref = rule["$ref"]
        parts = ref.split("/") if isinstance(ref, str) else []
        if len(parts) != 3 or parts[:2] != ["#", "$defs"] or not parts[2]:
            errors.append(f"{at}: only exact local #/$defs/<name> references are supported")
        elif parts[2] not in root.get("$defs", {}):
            errors.append(f"{at}: unresolved local reference {ref}")
        return errors
    kind = rule.get("type")
    if kind is not None and kind not in SUPPORTED_TYPES:
        errors.append(f"{at}: unsupported schema type {kind!r}")
    props = rule.get("properties")
    if props is not None:
        if not isinstance(props, dict):
            errors.append(f"{at}.properties: expected object")
        else:
            for key, child in props.items():
                schema_contract(child, root, f"{at}.properties.{key}", errors)
    defs = rule.get("$defs")
    if defs is not None:
        if not isinstance(defs, dict):
            errors.append(f"{at}.$defs: expected object")
        else:
            for key, child in defs.items():
                schema_contract(child, root, f"{at}.$defs.{key}", errors)
    if "items" in rule:
        schema_contract(rule["items"], root, f"{at}.items", errors)
    return errors


def resolve_ref(rule, root):
    if set(rule) != {"$ref"}:
        raise ValueError("$ref rule has unsupported siblings")
    ref = rule["$ref"]
    parts = ref.split("/") if isinstance(ref, str) else []
    if len(parts) != 3 or parts[:2] != ["#", "$defs"] or parts[2] not in root.get("$defs", {}):
        raise ValueError("unsupported or unresolved $ref: " + repr(ref))
    return root["$defs"][parts[2]]


def shape(value, rule, root, at, errors):
    if "$ref" in rule:
        return shape(value, resolve_ref(rule, root), root, at, errors)
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


def references_exist(refs, name, evidence_ids, errors):
    for ref in refs:
        if ref not in evidence_ids:
            errors.append(f"{name}: missing evidence {ref}")


def known_evidence_refs(refs, evidence_by_id):
    return [ref for ref in refs if ref in evidence_by_id and evidence_by_id[ref]["kind"] != "unknown"]


def check_bound(bound, name, evidence_ids, errors):
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
    if kind != "unknown" and not bound["basis_evidence"]:
        errors.append(f"{name}: non-unknown bound needs referenced basis evidence")
    references_exist(bound["basis_evidence"], name, evidence_ids, errors)


def check_definite_assessment(item, name, unknown_value, evidence_by_id, errors):
    assessment = item["assessment"]
    refs = item["basis_evidence"]
    if assessment != unknown_value and not refs:
        errors.append(f"{name}: definite assessment needs referenced evidence")
    references_exist(refs, name, set(evidence_by_id), errors)
    if assessment != unknown_value and refs and not known_evidence_refs(refs, evidence_by_id):
        errors.append(f"{name}: definite assessment cannot rest only on evidence marked unknown")


def normalise_text(value):
    return " ".join(value.split())


def validate(record, previous=None):
    schema = read(HERE / "episode.schema.json")
    errors = ["schema: " + e for e in schema_contract(schema, schema)]
    if errors:
        return errors
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
    evidence_by_id = {x["id"]: x for x in record["evidence"]}

    references_exist(record["authority"]["basis_evidence"], "authority", ids["evidence"], errors)

    for uncertainty in record["uncertainties"]:
        if uncertainty["status"] == "resolved" and not uncertainty["resolution_evidence"]:
            errors.append(uncertainty["id"] + ": resolution requires evidence")
        references_exist(uncertainty["resolution_evidence"], uncertainty["id"], ids["evidence"], errors)

    for challenge in record["challenges"]:
        references_exist(challenge["evidence"], challenge["id"], ids["evidence"], errors)
        if challenge["status"] != "open" and not challenge["disposition"].strip():
            errors.append(challenge["id"] + ": disposition missing")

    for party in record["affected"]:
        if party["voice"] != "direct" and not party["representation_limit"].strip():
            errors.append(party["id"] + ": non-direct voice needs representation limit")

    if record["action"]["mode"] == "ACT" and record["action"]["scope"] not in record["authority"]["granted_scopes"]:
        errors.append("ACT scope not in recorded grant (record check, not permission)")

    for name in ("detection", "routing", "correction", "hardening"):
        check_bound(record["clocks"][name]["bound"], "clocks." + name, ids["evidence"], errors)

    usability = record["clocks"]["routing"]["usability"]
    check_definite_assessment(usability, "clocks.routing.usability", "unknown", evidence_by_id, errors)

    window = record["clocks"]["window"]
    check_bound(window["assessment_as_of"], "clocks.window.assessment_as_of", ids["evidence"], errors)
    check_definite_assessment(window, "clocks.window", "unknown", evidence_by_id, errors)
    if window["assessment"] in {"open", "closed"} and window["assessment_as_of"]["kind"] == "unknown":
        errors.append("clocks.window: open/closed assessment needs a non-unknown assessment_as_of anchor")
    if record["clocks"]["hardening"]["status"] == "occurred" and window["assessment"] != "closed":
        errors.append("clocks.window: occurred hardening requires a closed window for the same preventive_remedy")

    for residue in record["residue"]:
        references_exist(residue["repair_evidence"], residue["id"] + ".repair_evidence", ids["evidence"], errors)
        if residue["status"] == "repaired":
            if not residue["repair_evidence"]:
                errors.append(residue["id"] + ": repaired residue requires referenced evidence")
            elif not known_evidence_refs(residue["repair_evidence"], evidence_by_id):
                errors.append(residue["id"] + ": repaired residue cannot rest only on evidence marked unknown")

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
            if normalise_text(record["authority"]["basis"]) == normalise_text(previous["authority"]["basis"]):
                errors.append("wider recorded grant needs materially changed authority basis, not whitespace or prior success")
            prior_evidence_ids = {x["id"] for x in previous["evidence"]}
            newly_grounded = [
                ref for ref in record["authority"]["basis_evidence"]
                if ref not in prior_evidence_ids and ref in evidence_by_id and evidence_by_id[ref]["kind"] != "unknown"
            ]
            if not newly_grounded:
                errors.append("wider recorded grant needs newly represented non-unknown evidence; evidence reference is traceability, not authority")

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
    print("STRUCTURE VALID ONLY: clocks/routes not proven or current; no permission, standing, goodness or alignment verdict.")


if __name__ == "__main__":
    main()
