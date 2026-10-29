#!/usr/bin/env python3
"""Offline, author-supplied clock comparison; not a legal or remedy determination."""

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

MAX_BYTES = 128 * 1024
STAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})$")
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,39}$")
BAD_TEXT = re.compile(r"[\x00-\x09\x0b-\x1f\x7f-\x9f\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069\ufeff]")
EVENT_KINDS = frozenset({"notice", "challenge", "response", "hardening", "other"})
EVIDENCE = frozenset({"reported", "observed", "inferred", "disputed", "unknown"})
PRECISION = frozenset({"exact", "approximate", "unknown"})
ROOT_FIELDS = frozenset({"title", "scope", "events", "comparisons"})
EVENT_FIELDS = frozenset({"id", "kind", "at", "precision", "evidence", "source", "note"})
PAIR_FIELDS = frozenset({"challenge", "hardening", "response"})


class LedgerError(ValueError):
    """Invalid or unsupported evidence data."""


def _pairs_unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise LedgerError("duplicate JSON object key: " + repr(key))
        out[key] = value
    return out


def _reject_constant(value):
    raise LedgerError("invalid JSON number: " + value)


def _object(obj, allowed, required, where):
    if type(obj) is not dict:
        raise LedgerError(where + " must be an object")
    extra = set(obj) - allowed
    missing = required - set(obj)
    if extra or missing:
        raise LedgerError(where + " unknown or missing fields: " + repr(sorted(extra | missing)))


def _text(value, where, max_length, required=True):
    if type(value) is not str or len(value) > max_length or (required and not value.strip()):
        raise LedgerError(where + " must be a bounded nonempty string")
    if BAD_TEXT.search(value) or any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        raise LedgerError(where + " contains unsupported controls or surrogate characters")
    return value


def _stamp(value, where):
    if type(value) is not str or not STAMP_RE.fullmatch(value):
        raise LedgerError(where + " requires ISO 8601 time with explicit UTC offset or Z")
    try:
        instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
        offset = instant.utcoffset()
        if offset is None or abs(offset) > timedelta(hours=14):
            raise ValueError("invalid UTC offset")
        return instant.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise LedgerError(where + " invalid calendar instant or offset") from exc


def read_document(payload):
    """Parse UTF-8 bytes and validate exactly the supported user-authored schema."""
    if type(payload) is not bytes or len(payload) > MAX_BYTES:
        raise LedgerError("input is not UTF-8 bytes within 128 KiB")
    try:
        obj = json.loads(payload.decode("utf-8"), object_pairs_hook=_pairs_unique, parse_constant=_reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise LedgerError("malformed UTF-8 JSON") from exc
    _object(obj, ROOT_FIELDS, {"title", "events", "comparisons"}, "document")
    _text(obj["title"], "title", 160)
    if "scope" in obj:
        _text(obj["scope"], "scope", 500)
    events = obj["events"]
    comparisons = obj["comparisons"]
    if type(events) is not list or not 2 <= len(events) <= 24:
        raise LedgerError("events must be 2..24 entries")
    if type(comparisons) is not list or not 1 <= len(comparisons) <= 12:
        raise LedgerError("comparisons must be 1..12 entries")
    seen = {}
    for i, event in enumerate(events):
        where = "events[" + str(i) + "]"
        _object(event, EVENT_FIELDS, {"id", "kind", "at", "precision", "evidence"}, where)
        event_id = _text(event["id"], where + ".id", 40)
        if not ID_RE.fullmatch(event_id) or event_id in seen:
            raise LedgerError(where + " id is duplicated or not a supported ASCII id")
        seen[event_id] = event
        if type(event["kind"]) is not str or event["kind"] not in EVENT_KINDS:
            raise LedgerError(where + " invalid kind")
        if type(event["evidence"]) is not str or event["evidence"] not in EVIDENCE:
            raise LedgerError(where + " invalid author evidence label")
        if type(event["precision"]) is not str or event["precision"] not in PRECISION:
            raise LedgerError(where + " invalid time precision")
        if event["precision"] == "unknown":
            if event["at"] is not None:
                raise LedgerError(where + " unknown clock must have null at")
        else:
            _stamp(event["at"], where + ".at")
        for field in ("source", "note"):
            if field in event:
                _text(event[field], where + "." + field, 600 if field == "source" else 1200)
    for i, pair in enumerate(comparisons):
        where = "comparisons[" + str(i) + "]"
        _object(pair, PAIR_FIELDS, {"challenge", "hardening"}, where)
        for key in pair:
            val = _text(pair[key], where + "." + key, 40)
            if val not in seen or seen[val]["kind"] != key:
                raise LedgerError(where + " reference must name a matching " + key + " event")
    return obj


def _compare(first, hardening):
    if first["precision"] != "exact" or hardening["precision"] != "exact":
        return {"relation": "indeterminate", "reason": "non_exact_or_unknown_clock"}
    a = _stamp(first["at"], "event.at")
    b = _stamp(hardening["at"], "hardening.at")
    diff = int((a - b).total_seconds())
    return {"relation": "before" if diff < 0 else "after" if diff > 0 else "same_instant", "seconds": abs(diff)}


def build_report(doc):
    """Calculates conditional UTC relations, never whether a remedy truly existed."""
    events = {e["id"]: e for e in doc["events"]}
    pairs = []
    for p in doc["comparisons"]:
        challenge = events[p["challenge"]]
        hardening = events[p["hardening"]]
        response = events[p["response"]] if "response" in p else None
        pairs.append({
            "challenge": p["challenge"], "hardening": p["hardening"],
            **({"response": p["response"]} if response else {}),
            "challenge_to_hardening": _compare(challenge, hardening),
            "response_to_hardening": _compare(response, hardening) if response else {"relation": "not_supplied"}
        })
    return {"title": doc["title"], "scope": doc.get("scope"), "events": doc["events"], "comparisons": pairs,
            "limits": ["Author-supplied clocks, precision and evidence labels; no independent verification.",
                       "Temporal order is not proof that a remedy was available, effective or accessible.",
                       "Do not substitute this for legal deadlines, specialist records or affected-party testimony."]}


def _quote(value):
    return json.dumps(value, ensure_ascii=False)


def _duration(seconds):
    if seconds == 0:
        return "0s"
    units = ((86400, "d"), (3600, "h"), (60, "m"), (1, "s"))
    bits = []
    for amount, suffix in units:
        qty, seconds = divmod(seconds, amount)
        if qty:
            bits.append(str(qty) + suffix)
    return " ".join(bits)


def _comparison_text(result):
    if result["relation"] == "not_supplied":
        return "response not supplied (not evidence that no response occurred)"
    if result["relation"] == "indeterminate":
        return "INDETERMINATE (approximate or unknown entered time)"
    if result["relation"] == "same_instant":
        return "same entered instant"
    return _duration(result["seconds"]) + " " + result["relation"] + " entered hardening instant"


def render_text(report):
    lines = ["CLOCK LEDGER — " + _quote(report["title"])]
    if report["scope"] is not None:
        lines.append("Scope: " + _quote(report["scope"]))
    lines.extend(("", "Events (all author-provided; observed is a label, not authenticated):"))
    for e in report["events"]:
        lines.append("  " + _quote(e["id"]) + " kind=" + e["kind"] + " at=" + _quote(e["at"]) +
                     " precision=" + e["precision"] + " evidence=" + e["evidence"] +
                     (" source=" + _quote(e["source"]) if "source" in e else " source=NOT_SUPPLIED") +
                     (" note=" + _quote(e["note"]) if "note" in e else ""))
    lines.append("")
    for i, p in enumerate(report["comparisons"], 1):
        lines.append("Comparison " + str(i) + ": challenge=" + _quote(p["challenge"]) +
                     " hardening=" + _quote(p["hardening"]) +
                     " response=" + (_quote(p["response"]) if "response" in p else "NOT_SUPPLIED"))
        lines.append("  Challenge relative to hardening: " + _comparison_text(p["challenge_to_hardening"]))
        lines.append("  Response relative to hardening: " + _comparison_text(p["response_to_hardening"]))
    lines.append("")
    lines.append("Limits:")
    lines.extend("  - " + x for x in report["limits"])
    lines.append("Question to investigate: could affected parties actually obtain a meaningful change before hardening?")
    return "\n".join(lines) + "\n"


def _write_atomic(path, contents):
    destination = Path(path)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=destination.parent,
                                         prefix="." + destination.name + ".", suffix=".tmp", delete=False) as out:
            temp = out.name
            out.write(contents)
        os.replace(temp, destination)
    finally:
        if temp and os.path.exists(temp):
            os.unlink(temp)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only comparison of author-supplied correction clocks; no network")
    parser.add_argument("input", nargs="?", default="-", help="JSON file, or - for stdin")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", help="write atomically to this local path after validation")
    args = parser.parse_args(argv)
    try:
        payload = (sys.stdin.buffer.read(MAX_BYTES + 1) if args.input == "-" else Path(args.input).open("rb").read(MAX_BYTES + 1))
        report = build_report(read_document(payload))
        out = render_text(report) if args.format == "text" else json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            _write_atomic(args.output, out)
        else:
            sys.stdout.write(out)
        return 0
    except (LedgerError, OSError, UnicodeError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
