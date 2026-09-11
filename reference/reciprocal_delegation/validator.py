#!/usr/bin/env python3
"""Validate the reciprocal-delegation/0.1 reference envelope.

Stdlib only. This is a non-production reference validator: structural and
cross-field integrity checks, not an authorization service.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

FORMAT = "reciprocal-delegation/0.1"
GENERIC_ROUTINE_TOKENS = {"proceed", "ok", "okay", "yes", "continue", "go", "go ahead"}

TOP_REQUIRED = (
    "format",
    "delegation_id",
    "object",
    "actor",
    "consequence_class",
    "write_scope",
    "no_touch",
    "evidence_obligation",
    "closer",
    "authorization",
    "claim_binding",
    "mutation_controls",
    "repair_controls",
    "restoration",
    "witness",
    "human_correction",
    "initiative",
)


def present_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def require_dict(doc: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = doc.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key}: must be an object")
        return {}
    return value


def require_list(doc: dict[str, Any], key: str, errors: list[str], *, nonempty: bool = False) -> list[Any]:
    value = doc.get(key)
    if not isinstance(value, list):
        errors.append(f"{key}: must be an array")
        return []
    if nonempty and not value:
        errors.append(f"{key}: must not be empty")
    return value


def validate(doc: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["root: must be a JSON object"]

    for key in TOP_REQUIRED:
        if key not in doc:
            errors.append(f"{key}: missing required field")

    if doc.get("format") != FORMAT:
        errors.append(f"format: expected {FORMAT!r}")

    if not present_text(doc.get("delegation_id")):
        errors.append("delegation_id: must be non-empty text")

    consequence = doc.get("consequence_class")
    if consequence not in {"routine_reversible", "consequential"}:
        errors.append("consequence_class: must be routine_reversible or consequential")

    obj = require_dict(doc, "object", errors)
    if not present_text(obj.get("kind")):
        errors.append("object.kind: must be non-empty text")
    if not present_text(obj.get("ref")):
        errors.append("object.ref: must be non-empty text")

    actor = require_dict(doc, "actor", errors)
    if not present_text(actor.get("role")):
        errors.append("actor.role: must be non-empty text")
    if not present_text(actor.get("aperture")):
        errors.append("actor.aperture: must be non-empty text")

    write_scope = require_list(doc, "write_scope", errors, nonempty=True)
    no_touch = require_list(doc, "no_touch", errors)
    evidence = require_list(doc, "evidence_obligation", errors, nonempty=True)

    for field_name, values in (("write_scope", write_scope), ("no_touch", no_touch), ("evidence_obligation", evidence)):
        for i, value in enumerate(values):
            if not present_text(value):
                errors.append(f"{field_name}[{i}]: must be non-empty text")
        strings = [v for v in values if isinstance(v, str)]
        if len(strings) != len(set(strings)):
            errors.append(f"{field_name}: duplicate entries are not allowed")

    overlap = sorted(set(v for v in write_scope if isinstance(v, str)) & set(v for v in no_touch if isinstance(v, str)))
    if overlap:
        errors.append(f"scope: write_scope overlaps no_touch: {', '.join(overlap)}")

    closer = require_dict(doc, "closer", errors)
    if closer.get("kind") not in {"human", "named_event", "named_role"}:
        errors.append("closer.kind: must be human, named_event, or named_role")
    if not present_text(closer.get("ref")):
        errors.append("closer.ref: must be non-empty text")

    auth = require_dict(doc, "authorization", errors)
    auth_required = auth.get("required")
    if not isinstance(auth_required, bool):
        errors.append("authorization.required: must be boolean")
        auth_required = False
    if not isinstance(auth.get("approval_received"), bool):
        errors.append("authorization.approval_received: must be boolean")
    if auth.get("routine_phrase_is_not_authorization") is not True and consequence == "consequential":
        errors.append("authorization.routine_phrase_is_not_authorization: must be true for consequential work")

    # A consequential action must have legible, request-specific authorization.
    if consequence == "consequential" and auth_required is not True:
        errors.append("authorization: consequential work requires explicit authorization")

    if auth_required:
        request_id = auth.get("request_id")
        token = auth.get("approval_token")
        value = auth.get("approval_value")
        if not present_text(request_id):
            errors.append("authorization.request_id: required when authorization is required")
        if not present_text(token):
            errors.append("authorization.approval_token: required when authorization is required")
        elif token.strip().lower() in GENERIC_ROUTINE_TOKENS:
            errors.append("authorization.approval_token: generic routine phrase is not legible consequential authorization")
        if auth.get("approval_received") is not True:
            errors.append("authorization.approval_received: must be true before authorized execution")
        if value != token:
            errors.append("authorization.approval_value: must exactly match approval_token")

    claim = require_dict(doc, "claim_binding", errors)
    if claim.get("moved_head_becomes_historical") is not True:
        errors.append("claim_binding.moved_head_becomes_historical: must be true")

    mutation = require_dict(doc, "mutation_controls", errors)
    mutates = mutation.get("mutates")
    if not isinstance(mutates, bool):
        errors.append("mutation_controls.mutates: must be boolean")
        mutates = False
    if mutates:
        if not present_text(claim.get("target_head")):
            errors.append("claim_binding.target_head: required for mutation")
        if mutation.get("claim_before_build") is not True:
            errors.append("mutation_controls.claim_before_build: must be true for mutation")
        if mutation.get("exact_head_before_push") is not True:
            errors.append("mutation_controls.exact_head_before_push: must be true for mutation")
        if mutation.get("single_mutator") is not True:
            errors.append("mutation_controls.single_mutator: must be true for mutation")

    repair = require_dict(doc, "repair_controls", errors)
    is_repair = repair.get("is_repair")
    if not isinstance(is_repair, bool):
        errors.append("repair_controls.is_repair: must be boolean")
        is_repair = False
    if is_repair:
        if not present_text(repair.get("defect_id")):
            errors.append("repair_controls.defect_id: required for repair")
        if not present_text(repair.get("matching_failure_control")):
            errors.append("repair_controls.matching_failure_control: repair needs a control that can reproduce the failure class")

    restoration = require_dict(doc, "restoration", errors)
    strategy = restoration.get("strategy")
    if strategy not in {"forward_commit", "not_applicable"}:
        errors.append("restoration.strategy: must be forward_commit or not_applicable")
    if strategy == "forward_commit" and restoration.get("history_preserved") is not True:
        errors.append("restoration.history_preserved: forward restoration must preserve history")
    if mutates and strategy != "forward_commit":
        errors.append("restoration.strategy: mutation must use forward_commit in this reference model")

    witness = require_dict(doc, "witness", errors)
    if not isinstance(witness.get("required"), bool):
        errors.append("witness.required: must be boolean")
    if witness.get("required") is True and witness.get("name_delivery_plainly") is not True:
        errors.append("witness.name_delivery_plainly: required witness must NAME the delivery plainly")

    human = require_dict(doc, "human_correction", errors)
    initiative = require_dict(doc, "initiative", errors)
    public_or_consequential = initiative.get("public_or_consequential")
    if not isinstance(public_or_consequential, bool):
        errors.append("initiative.public_or_consequential: must be boolean")
        public_or_consequential = False

    max_actions = initiative.get("max_unreviewed_actions")
    if not positive_int(max_actions):
        errors.append("initiative.max_unreviewed_actions: must be a positive integer")

    if public_or_consequential or consequence == "consequential":
        expected = human.get("expected_max_minutes")
        unreviewed = initiative.get("max_unreviewed_minutes")
        if not positive_int(expected):
            errors.append("human_correction.expected_max_minutes: required for public/consequential initiative")
        if not positive_int(unreviewed):
            errors.append("initiative.max_unreviewed_minutes: required for public/consequential initiative")
        if positive_int(expected) and positive_int(unreviewed) and unreviewed > expected:
            errors.append(
                "initiative.max_unreviewed_minutes: cannot exceed declared human correction/check-in window"
            )

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} DELEGATION.json", file=sys.stderr)
        return 2

    path = Path(argv[1])
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
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
