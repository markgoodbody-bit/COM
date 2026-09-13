#!/usr/bin/env python3
"""Validate Reciprocal Delegation bounded fan-out/0.1 records.

Stdlib only. Structural/coordination checks, not an authorization or IAM service.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

FORMAT = "reciprocal-delegation-fanout/0.1"
CONSEQUENCES = {"routine_reversible", "consequential"}
PARENT_STATES = {"active", "revoked", "stopped", "handback"}
CHILD_STATES = {"planned", "active", "returned", "failed", "revoked"}
TERMINAL_CHILD_STATES = {"returned", "failed", "revoked"}
LIVE_CHILD_STATES = {"planned", "active"}


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def norm(path: str) -> str | None:
    p = path.rstrip("/")
    if not p or p.startswith("/") or ".." in p.split("/") or re.search(r"[\\:*?\[\]]", p):
        return None
    return p.casefold()


def covers(parent: str, child: str) -> bool:
    return child == parent or child.startswith(parent + "/")


def overlaps(a: str, b: str) -> bool:
    return covers(a, b) or covers(b, a)


def list_text(value: Any, label: str, errors: list[str], *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{label}: must be array")
        return []
    if nonempty and not value:
        errors.append(f"{label}: must not be empty")
    out: list[str] = []
    for i, item in enumerate(value):
        if not text(item):
            errors.append(f"{label}[{i}]: must be non-empty text")
        else:
            out.append(item)
    if len(out) != len(set(out)):
        errors.append(f"{label}: duplicates not allowed")
    return out


def paths(value: Any, label: str, errors: list[str]) -> list[str]:
    raw = list_text(value, label, errors, nonempty=True)
    out: list[str] = []
    for i, item in enumerate(raw):
        n = norm(item)
        if n is None:
            errors.append(f"{label}[{i}]: invalid repository-relative path")
        else:
            out.append(n)
    return out


def positive_int(value: Any, label: str, errors: list[str], *, allow_zero: bool = False) -> int | None:
    minimum = 0 if allow_zero else 1
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        errors.append(f"{label}: must be integer >= {minimum}")
        return None
    return value


def validate(doc: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["root: must be object"]
    if doc.get("format") != FORMAT:
        errors.append(f"format: expected {FORMAT}")
    if not text(doc.get("fanout_id")):
        errors.append("fanout_id: required")

    parent = doc.get("parent")
    if not isinstance(parent, dict):
        errors.append("parent: must be object")
        parent = {}
    if not text(parent.get("delegation_id")):
        errors.append("parent.delegation_id: required")
    if not text(parent.get("role")):
        errors.append("parent.role: required")
    parent_aperture = parent.get("aperture")
    if not text(parent_aperture):
        errors.append("parent.aperture: required")
        parent_aperture = ""
    parent_state = parent.get("state")
    if parent_state not in PARENT_STATES:
        errors.append(f"parent.state: must be one of {sorted(PARENT_STATES)}")
    parent_scope = paths(parent.get("write_scope"), "parent.write_scope", errors)
    parent_no_touch = list_text(parent.get("no_touch"), "parent.no_touch", errors)
    parent_consequence = parent.get("consequence_class")
    if parent_consequence not in CONSEQUENCES:
        errors.append(f"parent.consequence_class: must be one of {sorted(CONSEQUENCES)}")
    parent_max = positive_int(parent.get("max_unreviewed_actions"), "parent.max_unreviewed_actions", errors)
    parent_handback = parent.get("handback_event")
    if not text(parent_handback):
        errors.append("parent.handback_event: required")

    auth = doc.get("fanout_authorization")
    if not isinstance(auth, dict):
        errors.append("fanout_authorization: must be object")
        auth = {}
    if auth.get("allowed") is not True:
        errors.append("fanout_authorization.allowed: must be true; runtime ability to spawn is not delegation authority")
    if not text(auth.get("source_ref")):
        errors.append("fanout_authorization.source_ref: legible fan-out authority source required")
    if auth.get("one_hop_only") is not True:
        errors.append("fanout_authorization.one_hop_only: companion v0.1 requires true")
    max_children = positive_int(auth.get("max_active_children"), "fanout_authorization.max_active_children", errors)
    family_ceiling = positive_int(auth.get("family_action_ceiling"), "fanout_authorization.family_action_ceiling", errors)
    parent_reserve = positive_int(auth.get("parent_direct_action_reserve"), "fanout_authorization.parent_direct_action_reserve", errors, allow_zero=True)
    parent_mutates = auth.get("parent_mutates_while_children_active")
    if not isinstance(parent_mutates, bool):
        errors.append("fanout_authorization.parent_mutates_while_children_active: must be boolean")

    children = doc.get("children")
    if not isinstance(children, list) or not children:
        errors.append("children: must be a non-empty array")
        children = []

    child_ids: set[str] = set()
    apertures: set[str] = set()
    seen_receipts: set[str] = set()
    child_budget_sum = 0
    child_actions_sum = 0
    live_children = 0
    live_mutators: list[tuple[str, list[str]]] = []
    child_receipts: list[str] = []

    for i, child in enumerate(children):
        prefix = f"children[{i}]"
        if not isinstance(child, dict):
            errors.append(f"{prefix}: must be object")
            continue
        child_id = child.get("child_id")
        if not text(child_id):
            errors.append(f"{prefix}.child_id: required")
            child_id = f"<missing-{i}>"
        elif child_id in child_ids:
            errors.append(f"{prefix}.child_id: duplicate {child_id}")
        else:
            child_ids.add(child_id)

        actor = child.get("actor")
        if not isinstance(actor, dict):
            errors.append(f"{prefix}.actor: must be object")
            actor = {}
        if not text(actor.get("role")):
            errors.append(f"{prefix}.actor.role: required")
        aperture = actor.get("aperture")
        if not text(aperture):
            errors.append(f"{prefix}.actor.aperture: required")
        else:
            if aperture == parent_aperture:
                errors.append(f"{prefix}.actor.aperture: child must have distinct aperture identity from parent")
            if aperture in apertures:
                errors.append(f"{prefix}.actor.aperture: duplicate child aperture {aperture}")
            apertures.add(aperture)

        consequence = child.get("consequence_class")
        if consequence not in CONSEQUENCES:
            errors.append(f"{prefix}.consequence_class: must be one of {sorted(CONSEQUENCES)}")
        if parent_consequence == "routine_reversible" and consequence == "consequential":
            errors.append(f"{prefix}.consequence_class: child cannot escalate routine parent to consequential")
        if consequence == "consequential" and not text(child.get("authorization_ref")):
            errors.append(f"{prefix}.authorization_ref: consequential child requires legible request-specific authorization reference")

        mutates = child.get("mutates")
        if not isinstance(mutates, bool):
            errors.append(f"{prefix}.mutates: must be boolean")
            mutates = False

        child_scope = paths(child.get("write_scope"), f"{prefix}.write_scope", errors)
        for p in child_scope:
            if not any(covers(parent_path, p) for parent_path in parent_scope):
                errors.append(f"{prefix}.write_scope: path exceeds parent scope: {p}")

        child_no_touch = list_text(child.get("no_touch"), f"{prefix}.no_touch", errors)
        missing = sorted(set(parent_no_touch) - set(child_no_touch))
        if missing:
            errors.append(f"{prefix}.no_touch: missing inherited constraints: {', '.join(missing)}")

        budget = positive_int(child.get("max_unreviewed_actions"), f"{prefix}.max_unreviewed_actions", errors)
        if budget is not None:
            child_budget_sum += budget
        actions_used = positive_int(child.get("actions_used"), f"{prefix}.actions_used", errors, allow_zero=True)
        if actions_used is not None:
            child_actions_sum += actions_used
            if budget is not None and actions_used > budget:
                errors.append(f"{prefix}.actions_used: {actions_used} exceeds child max_unreviewed_actions {budget}")

        if child.get("may_subdelegate") is not False:
            errors.append(f"{prefix}.may_subdelegate: companion v0.1 requires false")
        state = child.get("state")
        if state not in CHILD_STATES:
            errors.append(f"{prefix}.state: must be one of {sorted(CHILD_STATES)}")
        if child.get("receipt_required") is not True:
            errors.append(f"{prefix}.receipt_required: must be true")
        receipt_ref = child.get("receipt_ref")
        if receipt_ref is not None and not text(receipt_ref):
            errors.append(f"{prefix}.receipt_ref: must be non-empty text or null")
        if text(receipt_ref):
            if receipt_ref in seen_receipts:
                errors.append(f"{prefix}.receipt_ref: duplicate receipt reference {receipt_ref}")
            seen_receipts.add(receipt_ref)
            child_receipts.append(receipt_ref)
        if state in TERMINAL_CHILD_STATES and not text(receipt_ref):
            errors.append(f"{prefix}.receipt_ref: terminal child requires concrete receipt reference")

        if state in LIVE_CHILD_STATES:
            live_children += 1
            if parent_state != "active":
                errors.append(f"{prefix}.state: planned/active child requires parent.state=active")
            if mutates:
                live_mutators.append((str(child_id), child_scope))

    if max_children is not None and live_children > max_children:
        errors.append(f"children: {live_children} planned/active children exceeds max_active_children={max_children}")

    if parent_reserve is not None and family_ceiling is not None:
        reserved = parent_reserve + child_budget_sum
        if reserved > family_ceiling:
            errors.append(
                "fanout_authorization.family_action_ceiling: parent reserve + child reservations "
                f"({reserved}) exceeds family ceiling ({family_ceiling})"
            )
    if family_ceiling is not None and parent_max is not None and family_ceiling > parent_max:
        errors.append(
            "fanout_authorization.family_action_ceiling: family ceiling "
            f"({family_ceiling}) exceeds parent max_unreviewed_actions ({parent_max})"
        )

    if live_mutators and parent_mutates is not False:
        errors.append("fanout_authorization.parent_mutates_while_children_active: must be false while any child mutator is planned/active")

    for left in range(len(live_mutators)):
        left_id, left_scope = live_mutators[left]
        for right in range(left + 1, len(live_mutators)):
            right_id, right_scope = live_mutators[right]
            collisions = [(a, b) for a in left_scope for b in right_scope if overlaps(a, b)]
            if collisions:
                errors.append(
                    f"children: simultaneous mutators {left_id} and {right_id} have overlapping scope: "
                    + ", ".join(f"{a}<->{b}" for a, b in collisions)
                )

    revocation = doc.get("revocation")
    if not isinstance(revocation, dict):
        errors.append("revocation: must be object")
        revocation = {}
    if revocation.get("parent_revocation_propagates") is not True:
        errors.append("revocation.parent_revocation_propagates: must be true")
    if revocation.get("children_must_stop_before_parent_handback") is not True:
        errors.append("revocation.children_must_stop_before_parent_handback: must be true")

    handback = doc.get("handback")
    if not isinstance(handback, dict):
        errors.append("handback: must be object")
        handback = {}
    handback_event = handback.get("event")
    if not text(handback_event):
        errors.append("handback.event: required")
    elif text(parent_handback) and handback_event != parent_handback:
        errors.append("handback.event: must equal parent.handback_event")
    status = handback.get("status")
    if status not in {"pending", "complete"}:
        errors.append("handback.status: must be pending or complete")

    parent_actions_used = positive_int(handback.get("parent_direct_actions_used"), "handback.parent_direct_actions_used", errors, allow_zero=True)
    aggregate_actions_used = positive_int(handback.get("aggregate_actions_used"), "handback.aggregate_actions_used", errors, allow_zero=True)
    receipt_refs = list_text(handback.get("child_receipt_refs"), "handback.child_receipt_refs", errors)

    if parent_actions_used is not None and parent_reserve is not None and parent_actions_used > parent_reserve:
        errors.append(
            "handback.parent_direct_actions_used: "
            f"{parent_actions_used} exceeds parent_direct_action_reserve {parent_reserve}"
        )
    if parent_actions_used is not None and aggregate_actions_used is not None:
        expected_actions = parent_actions_used + child_actions_sum
        if aggregate_actions_used != expected_actions:
            errors.append(
                "handback.aggregate_actions_used: must equal parent_direct_actions_used + sum(child.actions_used); "
                f"expected {expected_actions}, got {aggregate_actions_used}"
            )
    if aggregate_actions_used is not None and family_ceiling is not None and aggregate_actions_used > family_ceiling:
        errors.append(
            f"handback.aggregate_actions_used: {aggregate_actions_used} exceeds family_action_ceiling {family_ceiling}"
        )

    unknown_receipts = sorted(set(receipt_refs) - set(child_receipts))
    if unknown_receipts:
        errors.append("handback.child_receipt_refs: references not present on any child: " + ", ".join(unknown_receipts))

    if status == "complete":
        for i, child in enumerate(children):
            if isinstance(child, dict) and child.get("state") not in TERMINAL_CHILD_STATES:
                errors.append(f"children[{i}].state: parent handback cannot complete while child remains non-terminal")
        if set(receipt_refs) != set(child_receipts) or len(receipt_refs) != len(children):
            errors.append("handback.child_receipt_refs: complete handback must name exactly one concrete receipt for every child")

    if parent_state in {"revoked", "stopped", "handback"}:
        for i, child in enumerate(children):
            if isinstance(child, dict) and child.get("state") in LIVE_CHILD_STATES:
                errors.append(f"children[{i}].state: parent {parent_state} cannot retain planned/active child authority")

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
