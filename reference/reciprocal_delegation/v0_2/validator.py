#!/usr/bin/env python3
"""Validate reciprocal-delegation/0.2 field-repair envelopes.

Stdlib only. Non-production reference validator; not an authorization service.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Any

FORMAT = "reciprocal-delegation/0.2"
GENERIC_ROUTINE_TOKENS = {"proceed", "ok", "okay", "yes", "continue", "go", "go ahead"}
BOUND_MODES = {"time_bound", "event_bound", "time_and_event"}
TOP_REQUIRED = (
    "format", "delegation_id", "object", "actor", "consequence_class",
    "write_scope", "no_touch", "evidence_obligation", "closer",
    "authorization", "claim_binding", "mutation_controls", "repair_controls",
    "restoration", "witness", "human_correction", "initiative",
)

def text(v: Any) -> bool:
    return isinstance(v, str) and bool(v.strip())

def posint(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and v > 0

def obj(doc: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    v = doc.get(key)
    if not isinstance(v, dict):
        errors.append(f"{key}: must be an object")
        return {}
    return v

def arr(doc: dict[str, Any], key: str, errors: list[str], nonempty: bool = False) -> list[Any]:
    v = doc.get(key)
    if not isinstance(v, list):
        errors.append(f"{key}: must be an array")
        return []
    if nonempty and not v:
        errors.append(f"{key}: must not be empty")
    return v

def validate(doc: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["root: must be a JSON object"]
    for key in TOP_REQUIRED:
        if key not in doc:
            errors.append(f"{key}: missing required field")
    if doc.get("format") != FORMAT:
        errors.append(f"format: expected {FORMAT!r}")
    if not text(doc.get("delegation_id")):
        errors.append("delegation_id: must be non-empty text")

    consequence = doc.get("consequence_class")
    if consequence not in {"routine_reversible", "consequential"}:
        errors.append("consequence_class: must be routine_reversible or consequential")

    target = obj(doc, "object", errors)
    if not text(target.get("kind")): errors.append("object.kind: must be non-empty text")
    if not text(target.get("ref")): errors.append("object.ref: must be non-empty text")

    actor = obj(doc, "actor", errors)
    if not text(actor.get("role")): errors.append("actor.role: must be non-empty text")
    if not text(actor.get("aperture")): errors.append("actor.aperture: must be non-empty text")

    write_scope = arr(doc, "write_scope", errors, True)
    no_touch = arr(doc, "no_touch", errors)
    evidence = arr(doc, "evidence_obligation", errors, True)
    for name, values in (("write_scope", write_scope), ("no_touch", no_touch), ("evidence_obligation", evidence)):
        for i, value in enumerate(values):
            if not text(value): errors.append(f"{name}[{i}]: must be non-empty text")
        strings = [v for v in values if isinstance(v, str)]
        if len(strings) != len(set(strings)): errors.append(f"{name}: duplicate entries are not allowed")
    overlap = sorted(set(v for v in write_scope if isinstance(v, str)) & set(v for v in no_touch if isinstance(v, str)))
    if overlap: errors.append(f"scope: write_scope overlaps no_touch: {', '.join(overlap)}")

    closer = obj(doc, "closer", errors)
    if closer.get("kind") not in {"human", "named_event", "named_role"}:
        errors.append("closer.kind: must be human, named_event, or named_role")
    if not text(closer.get("ref")): errors.append("closer.ref: must be non-empty text")

    auth = obj(doc, "authorization", errors)
    required = auth.get("required")
    if not isinstance(required, bool):
        errors.append("authorization.required: must be boolean")
        required = False
    if not isinstance(auth.get("approval_received"), bool):
        errors.append("authorization.approval_received: must be boolean")
    if consequence == "consequential":
        if required is not True:
            errors.append("authorization: consequential work requires explicit authorization")
        if auth.get("routine_phrase_is_not_authorization") is not True:
            errors.append("authorization.routine_phrase_is_not_authorization: must be true for consequential work")
    if required:
        request_id, token, value = auth.get("request_id"), auth.get("approval_token"), auth.get("approval_value")
        if not text(request_id): errors.append("authorization.request_id: required when authorization is required")
        if not text(token):
            errors.append("authorization.approval_token: required when authorization is required")
        elif token.strip().lower() in GENERIC_ROUTINE_TOKENS:
            errors.append("authorization.approval_token: generic routine phrase is not legible consequential authorization")
        if auth.get("approval_received") is not True:
            errors.append("authorization.approval_received: must be true before authorized execution")
        if value != token:
            errors.append("authorization.approval_value: must exactly match approval_token")

    claim = obj(doc, "claim_binding", errors)
    if claim.get("moved_head_becomes_historical") is not True:
        errors.append("claim_binding.moved_head_becomes_historical: must be true")

    mutation = obj(doc, "mutation_controls", errors)
    mutates = mutation.get("mutates")
    if not isinstance(mutates, bool):
        errors.append("mutation_controls.mutates: must be boolean")
        mutates = False
    if mutates:
        if not text(claim.get("target_head")): errors.append("claim_binding.target_head: required for mutation")
        if mutation.get("claim_before_build") is not True: errors.append("mutation_controls.claim_before_build: must be true for mutation")
        if mutation.get("exact_head_before_push") is not True: errors.append("mutation_controls.exact_head_before_push: must be true for mutation")
        if mutation.get("single_mutator") is not True: errors.append("mutation_controls.single_mutator: must be true for mutation")

    repair = obj(doc, "repair_controls", errors)
    is_repair = repair.get("is_repair")
    if not isinstance(is_repair, bool):
        errors.append("repair_controls.is_repair: must be boolean")
        is_repair = False
    if is_repair:
        if not text(repair.get("defect_id")): errors.append("repair_controls.defect_id: required for repair")
        if not text(repair.get("matching_failure_control")):
            errors.append("repair_controls.matching_failure_control: repair needs a control that can reproduce the failure class")

    restoration = obj(doc, "restoration", errors)
    strategy = restoration.get("strategy")
    if strategy not in {"forward_commit", "not_applicable"}:
        errors.append("restoration.strategy: must be forward_commit or not_applicable")
    if strategy == "forward_commit" and restoration.get("history_preserved") is not True:
        errors.append("restoration.history_preserved: forward restoration must preserve history")
    if mutates and strategy != "forward_commit":
        errors.append("restoration.strategy: mutation must use forward_commit in this reference model")

    witness = obj(doc, "witness", errors)
    if not isinstance(witness.get("required"), bool): errors.append("witness.required: must be boolean")
    if witness.get("required") is True and witness.get("name_delivery_plainly") is not True:
        errors.append("witness.name_delivery_plainly: required witness must NAME the delivery plainly")

    human = obj(doc, "human_correction", errors)
    initiative = obj(doc, "initiative", errors)
    mode = human.get("bound_mode")
    if mode not in BOUND_MODES:
        errors.append("human_correction.bound_mode: must be time_bound, event_bound, or time_and_event")
    public = initiative.get("public_or_consequential")
    if not isinstance(public, bool):
        errors.append("initiative.public_or_consequential: must be boolean")
        public = False
    if not posint(initiative.get("max_unreviewed_actions")):
        errors.append("initiative.max_unreviewed_actions: must be a positive integer")

    needs_bound = public or consequence == "consequential"
    needs_time = mode in {"time_bound", "time_and_event"}
    needs_event = mode in {"event_bound", "time_and_event"}
    expected = human.get("expected_max_minutes")
    unreviewed = initiative.get("max_unreviewed_minutes")
    handback = human.get("handback_event")

    if needs_bound and mode not in BOUND_MODES:
        errors.append("human_correction: public/consequential initiative requires a declared correction bound")
    if needs_time:
        if not posint(expected): errors.append("human_correction.expected_max_minutes: required for time-bounded correction")
        if not posint(unreviewed): errors.append("initiative.max_unreviewed_minutes: required for time-bounded initiative")
        if posint(expected) and posint(unreviewed) and unreviewed > expected:
            errors.append("initiative.max_unreviewed_minutes: cannot exceed declared human correction/check-in window")
    else:
        if expected is not None: errors.append("human_correction.expected_max_minutes: must be null when bound_mode is event_bound")
        if unreviewed is not None: errors.append("initiative.max_unreviewed_minutes: must be null when bound_mode is event_bound")
    if needs_event:
        if not text(handback): errors.append("human_correction.handback_event: required for event-bounded correction")
        elif handback.strip().lower() in {"when appropriate", "when needed", "later", "event"}:
            errors.append("human_correction.handback_event: must name an inspectable hand-back event")
    elif handback is not None:
        errors.append("human_correction.handback_event: must be null when bound_mode is time_bound")

    return errors

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} DELEGATION.json", file=sys.stderr)
        return 2
    try:
        doc = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(doc)
    if errors:
        print("FAIL")
        for error in errors: print(f"- {error}")
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
