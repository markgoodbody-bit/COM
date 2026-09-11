"""Offline, stdlib-only structural and ownership checks. No network or execution."""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
ACTIVE = {"building", "waiting"}


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def structure(value, rule, root, at, errors):
    """Implements only the documented schema keywords used by this schema."""
    supported = {"$schema", "title", "$defs", "$ref", "type", "required",
                 "properties", "additionalProperties", "const", "enum", "items",
                 "minItems", "uniqueItems", "minLength", "pattern", "format"}
    if set(rule) - supported:
        raise ValueError(f"unsupported schema keywords at {at}: {set(rule) - supported}")
    if "$ref" in rule:
        ref = rule["$ref"]
        if not ref.startswith("#/$defs/"):
            raise ValueError("only local $defs references supported")
        return structure(value, root["$defs"][ref[8:]], root, at, errors)
    checks = {"object": lambda x: isinstance(x, dict),
              "array": lambda x: isinstance(x, list),
              "string": lambda x: isinstance(x, str),
              "boolean": lambda x: type(x) is bool, "null": lambda x: x is None}
    kinds = rule.get("type", [])
    kinds = [kinds] if isinstance(kinds, str) else kinds
    if kinds and not any(checks[k](value) for k in kinds):
        errors.append(f"{at}: expected {kinds}")
        return
    if "const" in rule and value != rule["const"]:
        errors.append(f"{at}: expected {rule['const']!r}")
    if "enum" in rule and value not in rule["enum"]:
        errors.append(f"{at}: not in {rule['enum']}")
    if isinstance(value, dict):
        for key in rule.get("required", []):
            if key not in value:
                errors.append(f"{at}.{key}: missing")
        props = rule.get("properties", {})
        for key, item in value.items():
            if key in props:
                structure(item, props[key], root, f"{at}.{key}", errors)
            elif rule.get("additionalProperties") is False:
                errors.append(f"{at}.{key}: unknown field")
    elif isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            errors.append(f"{at}: too few items")
        if rule.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            errors.append(f"{at}: duplicate items")
        for i, item in enumerate(value):
            structure(item, rule.get("items", {}), root, f"{at}[{i}]", errors)
    elif isinstance(value, str):
        if len(value.strip()) < rule.get("minLength", 0):
            errors.append(f"{at}: empty text")
        if "pattern" in rule and not re.search(rule["pattern"], value):
            errors.append(f"{at}: invalid pattern")
        if rule.get("format") == "date-time":
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})", value):
                    raise ValueError("use ISO seconds with timezone")
                timestamp(value)
            except ValueError as exc:
                errors.append(f"{at}: invalid timestamp ({exc})")
        if rule.get("format") == "uri":
            parsed = urlsplit(value)
            if parsed.scheme != "https" or not parsed.netloc or any(c.isspace() or c in '<>"' for c in value):
                errors.append(f"{at}: expected absolute HTTPS evidence URL")


def scope_path(value):
    # Files or directory prefixes only. No glob, traversal or ambiguous root claim.
    path = value.rstrip("/")
    if not path or path.startswith("/") or re.search(r"[\\:*?\[\]]", path):
        return None
    if any(p in {"", ".", ".."} for p in path.split("/")):
        return None
    return path.casefold()


def overlaps(a, b):
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def validate(data, schema=None):
    schema = schema if schema is not None else read_json(HERE / "schema.json")
    errors = []
    structure(data, schema, schema, "ledger", errors)
    if errors:
        return errors
    ids, claims = set(), []
    for lane in data["lanes"]:
        work = lane["work_id"]
        if work in ids:
            errors.append(f"{work}: duplicate work_id")
        ids.add(work)
        if timestamp(lane["observed_at"]) > timestamp(data["recorded_at"]):
            errors.append(f"{work}: observation later than snapshot")
        if lane["state"] == "waiting":
            if not lane["blocker"] or not lane["unblocks_when"]:
                errors.append(f"{work}: waiting needs blocker and unblocks_when")
        elif lane["blocker"] is not None or lane["unblocks_when"] is not None:
            errors.append(f"{work}: blockers only belong to waiting state")
        if lane["state"] in {"handback", "closed"} and not lane["receipt"]:
            errors.append(f"{work}: handback/closed requires receipt")
        if lane["mutates"] and not lane["write_scope"]:
            errors.append(f"{work}: mutating lane needs concrete write scope")
        if not lane["mutates"] and lane["write_scope"]:
            errors.append(f"{work}: read-only lane cannot claim write scope")
        for entry in lane["write_scope"]:
            normalized = scope_path(entry)
            if normalized is None:
                errors.append(f"{work}: invalid scope {entry!r}")
            elif lane["mutates"] and lane["state"] in ACTIVE:
                claims.append((lane["repository"].casefold(), normalized, work))
    for i, (repo, path, work) in enumerate(claims):
        for other_repo, other_path, other_work in claims[i + 1:]:
            if work != other_work and repo == other_repo and overlaps(path, other_path):
                errors.append(f"{work}/{other_work}: overlapping active ownership: {path} / {other_path}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", nargs="?", type=Path, default=HERE / "ledger.json")
    args = parser.parse_args()
    try:
        errors = validate(read_json(args.ledger))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f"INVALID: {exc}\n")
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("VALID SNAPSHOT: structure and ownership only; not current truth or authority.")


if __name__ == "__main__":
    main()
