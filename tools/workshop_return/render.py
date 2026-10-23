#!/usr/bin/env python3
"""Read-only, offline rendering of a *claimed* Workshop result and optional readback.

This is not an authority checker, worker, scheduler, network client, or VM interface.
It does not establish that the purported guest task ran or that an observer is
independent. Its single positive claim is bounded byte-hash consistency.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import stat
import sys

MAX_BYTES = 65536
TASK_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\\Z")
HEX40 = re.compile(r"[0-9a-f]{40}\\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\\Z")
UTC_TIME = re.compile(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z\\Z")
KINDS = {"FIXED_CHECK", "SOURCE_REVIEW", "LOCAL_TEST"}
OUTCOMES = {"PASS", "FAIL", "STOPPED", "UNKNOWN"}
CARRIERS = {"HOST_FILE", "OTHER"}


class InvalidInput(ValueError):
    """Invalid or unrenderable local input; no fallback to a trusted state."""


def _unique_keys(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            raise InvalidInput("duplicate JSON key")
        output[key] = value
    return output


def _read_json(path):
    path = Path(path)
    try:
        file_stat = path.lstat()
        if not stat.S_ISREG(file_stat.st_mode):
            raise InvalidInput("input must be an ordinary non-symlink file")
        if file_stat.st_size > MAX_BYTES:
            raise InvalidInput("input exceeds 65536-byte limit")
        raw = path.read_bytes()
        if len(raw) > MAX_BYTES:
            raise InvalidInput("input exceeds 65536-byte limit")
        decoded = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_keys)
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InvalidInput("file could not be read as bounded UTF-8 JSON") from exc
    if not isinstance(decoded, dict):
        raise InvalidInput("JSON root must be an object")
    return raw, decoded


def _field(obj, key, pattern=None, options=None, max_length=None):
    value = obj.get(key)
    if not isinstance(value, str):
        raise InvalidInput("required string field invalid: " + key)
    if pattern and not pattern.fullmatch(value):
        raise InvalidInput("field has invalid syntax: " + key)
    if options and value not in options:
        raise InvalidInput("field has unsupported value: " + key)
    if max_length is not None and len(value) > max_length:
        raise InvalidInput("field too long: " + key)
    return value


def _utc(obj, key):
    raw = _field(obj, key, UTC_TIME)
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError as exc:
        raise InvalidInput("invalid UTC date: " + key) from exc


def _result_validate(obj):
    if obj.get("schema") != "workshop.result.v0":
        raise InvalidInput("result schema must be workshop.result.v0")
    _field(obj, "task_id", TASK_ID)
    _field(obj, "source_sha", HEX40)
    _field(obj, "kind", options=KINDS)
    _field(obj, "outcome", options=OUTCOMES)
    _field(obj, "summary", max_length=240)
    code = obj.get("exit_code")
    if code is not None and (type(code) is not int or not 0 <= code <= 255):
        raise InvalidInput("exit_code must be 0..255 or null")
    if _utc(obj, "started_utc") > _utc(obj, "finished_utc"):
        raise InvalidInput("guest start later than finish")


def _readback_validate(obj):
    if obj.get("schema") != "workshop.readback.v0":
        raise InvalidInput("readback schema must be workshop.readback.v0")
    _field(obj, "task_id", TASK_ID)
    _field(obj, "source_sha", HEX40)
    _field(obj, "result_sha256", HEX64)
    _field(obj, "carrier", options=CARRIERS)
    _utc(obj, "observed_utc")


def report(result_path, readback_path=None):
    """Return (bounded projection, exit status). No writes, network or execution."""
    raw, result = _read_json(result_path)
    _result_validate(result)
    digest = hashlib.sha256(raw).hexdigest()
    conflicts = []
    if result["outcome"] == "PASS" and result.get("exit_code") != 0:
        conflicts.append("PASS_NONZERO_EXIT")
    observer = None
    if readback_path is not None:
        _, observer = _read_json(readback_path)
        _readback_validate(observer)
        if observer["result_sha256"] != digest:
            conflicts.append("DIGEST_MISMATCH")
        if observer["task_id"] != result["task_id"]:
            conflicts.append("TASK_ID_MISMATCH")
        if observer["source_sha"] != result["source_sha"]:
            conflicts.append("SOURCE_SHA_MISMATCH")
        if _utc(observer, "observed_utc") < _utc(result, "finished_utc"):
            conflicts.append("CLOCK_ORDER_CONFLICT")
    status = ("CONFLICT" if conflicts else
              "HASH_MATCH_UNAUTHENTICATED" if observer else "UNWITNESSED")
    projection = {
        "schema": "workshop.projection.v0",
        "task_id": result["task_id"],
        "source_sha": result["source_sha"],
        "declared_kind": result["kind"],
        "declared_outcome": result["outcome"],
        "declared_exit_code": result.get("exit_code"),
        "declared_summary": result["summary"],
        "guest_started_utc": result["started_utc"],
        "guest_finished_utc": result["finished_utc"],
        "result_sha256": digest,
        "readback_status": status,
        "readback_observed_utc": observer["observed_utc"] if observer else None,
        "readback_carrier_claim": observer["carrier"] if observer else None,
        "conflicts": conflicts,
        "verification_scope": "LOCAL_BYTES_ONLY",
        "execution_verified": False,
        "authenticated_witness": False,
        "freshness": "UNKNOWN",
        "live_vm_status": "NOT_ESTABLISHED",
    }
    return projection, 1 if conflicts else 0


def _quoted(value):
    # Quote single-line data, including newlines and markup-like strings.
    return json.dumps(value, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e")


def to_text(view):
    return "\n".join([
        "WORKSHOP RETURN / OFFLINE, UNAUTHENTICATED SOURCE PROJECTION",
        "Task: " + _quoted(view["task_id"]),
        "Source revision (declared): " + view["source_sha"],
        "Guest claim: " + view["declared_kind"] + " / " + view["declared_outcome"] +
          " / exit " + _quoted(view["declared_exit_code"]),
        "Guest interval (declared): " + view["guest_started_utc"] + " to " + view["guest_finished_utc"],
        "Guest summary (untrusted): " + _quoted(view["declared_summary"]),
        "Local result SHA256: " + view["result_sha256"],
        "Readback: " + view["readback_status"],
        "Readback timestamp (declared): " + _quoted(view["readback_observed_utc"]),
        "Readback carrier (declared): " + _quoted(view["readback_carrier_claim"]),
        "Conflicts: " + (", ".join(view["conflicts"]) if view["conflicts"] else "NONE DETECTED BY THIS ADAPTER"),
        "Limits: local bytes only; witness identity, VM execution, freshness and effects NOT VERIFIED.",
    ])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline read-only Workshop return projection")
    parser.add_argument("result", help="local result JSON (claim, not proof)")
    parser.add_argument("--readback", help="optional independently collected local readback JSON claim")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        view, code = report(args.result, args.readback)
    except InvalidInput as exc:
        print("INVALID_INPUT: " + str(exc), file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(view, ensure_ascii=True, indent=2, sort_keys=True))
    else:
        print(to_text(view))
    return code


if __name__ == "__main__":
    sys.exit(main())
