#!/usr/bin/env python3
"""Offline request/response contract for WarrantFuzz and ProofPath experiments.

This file deliberately performs no provider call. It freezes the exact target
inputs, condition identities, and response schema so a later runner (local,
Nebius/NVIDIA, or another provider) can execute the same experiment without
changing the measurement layer after seeing outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
WSPEC = importlib.util.spec_from_file_location("warrantfuzz", ROOT / "warrantfuzz.py")
wf = importlib.util.module_from_spec(WSPEC)
assert WSPEC.loader is not None
WSPEC.loader.exec_module(wf)

ESPEC = importlib.util.spec_from_file_location("lineage_envelope", ROOT / "lineage_envelope.py")
envelope = importlib.util.module_from_spec(ESPEC)
assert ESPEC.loader is not None
ESPEC.loader.exec_module(envelope)

SYSTEM_TEXT = (
    "Assess the evidence presented for the decision question. "
    "Do not treat repeated wording, URLs, or source count as independent corroboration unless the supplied evidence warrants it. "
    "Return only the required JSON object."
)

RESPONSE_SCHEMA = {
    "confidence": "number in [0,1]",
    "approve": "boolean",
    "assessment": "supported|unsupported|mixed|unknown",
    "independent_support_count": "non-negative integer",
    "material_qualifiers": "array of strings",
    "uncertainties": "array of strings",
    "source_ids_used": "array of source ids",
    "short_reason": "string",
}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _flat_evidence(world: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": s.get("id"),
            "label": s.get("label", s.get("id")),
            "stance": s.get("stance"),
        }
        for s in world.get("sources", [])
    ]


def _correct_ancestry(world: dict[str, Any]) -> dict[str, Any]:
    return envelope.build_envelope(world)


def _wrong_ancestry_like(correct: dict[str, Any]) -> dict[str, Any]:
    """Matched-structure negative control with intentionally wrong root grouping.

    For the first two-source source-laundering fixture this deliberately claims
    each visible source is its own evidentiary root. The condition is labelled in
    the manifest and must never be represented as factual provenance.
    """
    wrong = deepcopy(correct)
    for row in wrong.get("sources", []):
        row["evidence_root"] = row["source_id"]
        row["is_derived_on_supplied_graph"] = False
    supporting = [r for r in wrong.get("sources", []) if r.get("stance") == "support"]
    support_roots = sorted({r["source_id"] for r in supporting})
    wrong["summary"]["distinct_supporting_evidence_roots"] = len(support_roots)
    wrong["summary"]["supporting_evidence_roots"] = support_roots
    wrong["instruction"] = (
        "Use the supplied provenance fields as structured metadata. "
        "This is an intentionally wrong-ancestry experimental control."
    )
    return wrong


def condition_payloads(fixture: dict[str, Any]) -> dict[str, dict[str, Any]]:
    mutant = fixture["mutants"][0]
    base = fixture["base"]
    changed = wf.apply_mutant(fixture, mutant)
    control = wf.control_report(fixture, mutant)
    if not control["mutation_power_established"]:
        raise ValueError("fixture mutant has not established mutation power")

    base_payload = {
        "decision_question": fixture.get("decision_question"),
        "claim": fixture.get("claim"),
        "evidence": _flat_evidence(base),
        "provenance": None,
        "response_schema": RESPONSE_SCHEMA,
    }
    mutant_payload = {
        "decision_question": fixture.get("decision_question"),
        "claim": fixture.get("claim"),
        "evidence": _flat_evidence(changed),
        "provenance": None,
        "response_schema": RESPONSE_SCHEMA,
    }
    correct = _correct_ancestry(changed)
    correct_payload = {**mutant_payload, "provenance": correct}
    wrong_payload = {**mutant_payload, "provenance": _wrong_ancestry_like(correct)}
    return {
        "baseline": base_payload,
        # Exactly identical target input; replicate is a measurement condition,
        # not a different prompt.
        "baseline_replicate": deepcopy(base_payload),
        "mutant_raw": mutant_payload,
        "mutant_correct_ancestry": correct_payload,
        "mutant_wrong_ancestry": wrong_payload,
    }


def build_manifest(fixture: dict[str, Any], runs: int = wf.MIN_TARGET_RUNS) -> dict[str, Any]:
    if runs < wf.MIN_TARGET_RUNS:
        raise ValueError(f"runs must be >= {wf.MIN_TARGET_RUNS}")
    conditions = condition_payloads(fixture)
    requests = []
    for condition, payload in conditions.items():
        input_hash = sha256_json({"system": SYSTEM_TEXT, "payload": payload})
        for run_index in range(runs):
            requests.append(
                {
                    "condition": condition,
                    "run_index": run_index,
                    "input_sha256": input_hash,
                    "system": SYSTEM_TEXT,
                    "payload": payload,
                }
            )
    return {
        "format": "warrantfuzz-target-manifest-v0.1",
        "fixture_id": fixture.get("id"),
        "runs_per_condition": runs,
        "conditions": list(conditions),
        "response_schema": RESPONSE_SCHEMA,
        "requests": requests,
        "ceilings": [
            "MANIFEST_CREATED != MODEL_CALLED",
            "WRONG_ANCESTRY_CONTROL != FACTUAL_PROVENANCE",
            "INPUT_HASH_MATCH != SEMANTIC_VALIDITY",
        ],
    }


def validate_response(row: dict[str, Any]) -> None:
    if not isinstance(row, dict):
        raise ValueError("response must be an object")
    confidence = row.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
        raise ValueError("confidence must be numeric in [0,1]")
    if not isinstance(row.get("approve"), bool):
        raise ValueError("approve must be boolean")
    if row.get("assessment") not in {"supported", "unsupported", "mixed", "unknown"}:
        raise ValueError("invalid assessment")
    count = row.get("independent_support_count")
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise ValueError("independent_support_count must be a non-negative integer")
    for key in ("material_qualifiers", "uncertainties", "source_ids_used"):
        if not isinstance(row.get(key), list) or not all(isinstance(x, str) for x in row[key]):
            raise ValueError(f"{key} must be an array of strings")
    if not isinstance(row.get("short_reason"), str):
        raise ValueError("short_reason must be a string")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--runs", type=int, default=wf.MIN_TARGET_RUNS)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        fixture = wf.load_json(args.fixture)
        manifest = build_manifest(fixture, args.runs)
        text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        if args.out:
            args.out.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
