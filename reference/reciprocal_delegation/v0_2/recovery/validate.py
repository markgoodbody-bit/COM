#!/usr/bin/env python3
"""Validate reciprocal-delegation recovery/0.1 records.

Stdlib only. Structural/coordination checks, not an authorization service.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from typing import Any

FORMAT = "reciprocal-delegation-recovery/0.1"
TRANSFERABLE = {"stopped", "stalled_named", "narrowed", "handback", "partial_failure"}
CONSEQUENCES = {"routine_reversible", "consequential"}
GENERIC_TOKENS = {"proceed", "ok", "okay", "yes", "continue", "go", "go ahead"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def text(v: Any) -> bool:
    return isinstance(v, str) and bool(v.strip())


def sha(v: Any) -> bool:
    return isinstance(v, str) and bool(SHA40.fullmatch(v))


def norm(path: str) -> str | None:
    p = path.rstrip("/")
    if not p or p.startswith("/") or ".." in p.split("/") or re.search(r"[\\:*?\[\]]", p):
        return None
    return p.casefold()


def covers(parent: str, child: str) -> bool:
    return child == parent or child.startswith(parent + "/")


def list_text(doc: dict[str, Any], key: str, errors: list[str], *, nonempty: bool = False) -> list[str]:
    value = doc.get(key)
    if not isinstance(value, list):
        errors.append(f"{key}: must be array")
        return []
    if nonempty and not value:
        errors.append(f"{key}: must not be empty")
    out: list[str] = []
    for i, item in enumerate(value):
        if not text(item):
            errors.append(f"{key}[{i}]: must be non-empty text")
        else:
            out.append(item)
    if len(out) != len(set(out)):
        errors.append(f"{key}: duplicates not allowed")
    return out


def authorization_errors(auth: Any, consequential: bool, widening: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(auth, dict):
        return ["authorization: must be object"]
    required = auth.get("required")
    if not isinstance(required, bool):
        errors.append("authorization.required: must be boolean")
        required = False
    needs = consequential or widening
    if needs and required is not True:
        errors.append("authorization: consequential work or scope/no-touch widening requires explicit authorization")
    if required:
        request_id = auth.get("request_id")
        token = auth.get("approval_token")
        value = auth.get("approval_value")
        if not text(request_id):
            errors.append("authorization.request_id: required")
        if not text(token):
            errors.append("authorization.approval_token: required")
        elif token.strip().lower() in GENERIC_TOKENS:
            errors.append("authorization.approval_token: generic routine phrase is not legible authorization")
        if auth.get("approval_received") is not True:
            errors.append("authorization.approval_received: must be true")
        if value != token:
            errors.append("authorization.approval_value: must exactly match approval_token")
    return errors


def validate(doc: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["root: must be object"]
    if doc.get("format") != FORMAT:
        errors.append(f"format: expected {FORMAT}")
    if not text(doc.get("transfer_id")):
        errors.append("transfer_id: required")

    obj = doc.get("object")
    if not isinstance(obj, dict):
        errors.append("object: must be object")
        obj = {}
    if not text(obj.get("repository")):
        errors.append("object.repository: required")
    if not text(obj.get("ref")):
        errors.append("object.ref: required")
    transferred = list_text(obj, "transferred_write_scope", errors, nonempty=True)
    old_no_touch = list_text(obj, "inherited_no_touch", errors)
    norm_transferred: list[str] = []
    for i, path in enumerate(transferred):
        n = norm(path)
        if n is None:
            errors.append(f"object.transferred_write_scope[{i}]: invalid path")
        else:
            norm_transferred.append(n)

    prev = doc.get("previous_lane")
    if not isinstance(prev, dict):
        errors.append("previous_lane: must be object")
        prev = {}
    if not text(prev.get("owner")):
        errors.append("previous_lane.owner: required")
    state = prev.get("state")
    if state not in TRANSFERABLE:
        errors.append(f"previous_lane.state: must be one of {sorted(TRANSFERABLE)}; active/building cannot transfer same scope")
    if not text(prev.get("reason")):
        errors.append("previous_lane.reason: named stop/stall/narrow/handback/failure reason required")
    last_head = prev.get("last_claimed_head")
    if not sha(last_head):
        errors.append("previous_lane.last_claimed_head: must be 40-char lowercase SHA")
    if prev.get("mutating_transferred_scope") is not False:
        errors.append("previous_lane.mutating_transferred_scope: must be false before takeover")

    transfer = doc.get("transfer")
    if not isinstance(transfer, dict):
        errors.append("transfer: must be object")
        transfer = {}
    if not text(transfer.get("decision_source")):
        errors.append("transfer.decision_source: required")
    current_head = transfer.get("current_head")
    if not sha(current_head):
        errors.append("transfer.current_head: must be 40-char lowercase SHA")
    if not text(transfer.get("new_owner")):
        errors.append("transfer.new_owner: required")
    consequence = transfer.get("consequence_class")
    if consequence not in CONSEQUENCES:
        errors.append(f"transfer.consequence_class: must be one of {sorted(CONSEQUENCES)}")

    historical = transfer.get("old_claim_historical")
    if not isinstance(historical, bool):
        errors.append("transfer.old_claim_historical: must be boolean")
    if sha(last_head) and sha(current_head) and last_head != current_head and historical is not True:
        errors.append("transfer.old_claim_historical: must be true when head moved")

    new_scope = list_text(transfer, "new_write_scope", errors, nonempty=True)
    new_no_touch = list_text(transfer, "new_no_touch", errors)
    norm_new: list[str] = []
    for i, path in enumerate(new_scope):
        n = norm(path)
        if n is None:
            errors.append(f"transfer.new_write_scope[{i}]: invalid path")
        else:
            norm_new.append(n)

    widened_paths = [child for child in norm_new if not any(covers(parent, child) for parent in norm_transferred)]
    missing_no_touch = sorted(set(old_no_touch) - set(new_no_touch))
    widening = bool(widened_paths or missing_no_touch)

    explicit_scope_change = transfer.get("explicit_scope_change_authorized")
    if not isinstance(explicit_scope_change, bool):
        errors.append("transfer.explicit_scope_change_authorized: must be boolean")
        explicit_scope_change = False
    if widening and explicit_scope_change is not True:
        if widened_paths:
            errors.append("transfer.new_write_scope: exceeds transferred scope without separately authorized widening: " + ", ".join(widened_paths))
        if missing_no_touch:
            errors.append("transfer.new_no_touch: inherited no-touch constraints removed without separately authorized change: " + ", ".join(missing_no_touch))
        errors.append("transfer.explicit_scope_change_authorized: must be true for widening/no-touch relaxation")

    errors.extend(authorization_errors(doc.get("authorization"), consequence == "consequential", widening))

    new_lane = doc.get("new_lane")
    if not isinstance(new_lane, dict):
        errors.append("new_lane: must be object")
        new_lane = {}
    start_head = new_lane.get("start_head")
    if not sha(start_head):
        errors.append("new_lane.start_head: must be 40-char lowercase SHA")
    if sha(start_head) and sha(current_head) and start_head != current_head:
        errors.append("new_lane.start_head: must equal reacquired transfer.current_head")
    if new_lane.get("history_preserved") is not True:
        errors.append("new_lane.history_preserved: must be true")
    if state == "partial_failure" and new_lane.get("recovery_strategy") != "forward_commit":
        errors.append("new_lane.recovery_strategy: partial failure requires forward_commit")
    if state != "partial_failure" and new_lane.get("recovery_strategy") not in {"forward_commit", "not_applicable"}:
        errors.append("new_lane.recovery_strategy: must be forward_commit or not_applicable")

    handback = doc.get("handback")
    if not isinstance(handback, dict):
        errors.append("handback: must be object")
        handback = {}
    if not text(handback.get("event")):
        errors.append("handback.event: required")
    if handback.get("receipt_is_review") is not False:
        errors.append("handback.receipt_is_review: must be false")
    if handback.get("success_widens_authority") is not False:
        errors.append("handback.success_widens_authority: must be false")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} RECORD.json", file=sys.stderr)
        return 2
    try:
        doc = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(doc)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
