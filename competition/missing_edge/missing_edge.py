#!/usr/bin/env python3
"""The Missing Edge v0.3: offline experiment contract and deterministic scorer.

No provider calls are made here. The module freezes matched provenance conditions,
two task arms, request hashes, response schemas and bidirectional scoring before
any target outputs exist.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FORMAT = "missing-edge-manifest-v0.3"
DEFAULT_RUNS = 10
DEFAULT_SEED = 20260917

SYSTEM_TEXT = (
    "Use only the supplied claim, reports, provenance metadata, and task. "
    "Do not add outside facts. Return only the required JSON object."
)

TASK_MODES = ("relationship_assessment", "decision")

ASSESSMENT_SCHEMA = {
    "relationship_assessment": "shared_established|independent_established|unknown",
    "independently_established_roots": "integer 0..2",
    "confidence": "number in [0,1]",
    "reason": "string",
}

DECISION_SCHEMA = {
    **ASSESSMENT_SCHEMA,
    "decision": "proceed|hold",
}

CONDITIONS = (
    "flat_sources",
    "missing_edge_graph",
    "open_world_scope",
    "explicit_unknown",
    "verified_shared",
    "verified_independent",
)

EXPECTED = {
    "flat_sources": {"relationship_assessment": "unknown", "roots": 0, "decision": "hold"},
    "missing_edge_graph": {"relationship_assessment": "unknown", "roots": 0, "decision": "hold"},
    "open_world_scope": {"relationship_assessment": "unknown", "roots": 0, "decision": "hold"},
    "explicit_unknown": {"relationship_assessment": "unknown", "roots": 0, "decision": "hold"},
    "verified_shared": {"relationship_assessment": "shared_established", "roots": 1, "decision": "hold"},
    "verified_independent": {"relationship_assessment": "independent_established", "roots": 2, "decision": "proceed"},
}

ASSESSMENT_TASK = (
    "Based only on the supplied record, what is established about whether the two reports "
    "have independent evidentiary origins?"
)


def load_cases(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        raise ValueError("cases file must contain a cases array")
    validate_cases(data)
    return data


def validate_cases(data: dict[str, Any]) -> None:
    ids: set[str] = set()
    for i, case in enumerate(data.get("cases", [])):
        if not isinstance(case, dict):
            raise ValueError(f"case[{i}] must be an object")
        cid = case.get("id")
        if not isinstance(cid, str) or not cid:
            raise ValueError(f"case[{i}].id must be a non-empty string")
        if cid in ids:
            raise ValueError(f"duplicate case id: {cid}")
        ids.add(cid)
        for key in ("claim", "decision"):
            if not isinstance(case.get(key), str) or not case[key]:
                raise ValueError(f"{cid}.{key} must be a non-empty string")
        sources = case.get("sources")
        if not isinstance(sources, list) or len(sources) != 2:
            raise ValueError(f"{cid}.sources must contain exactly two reports")
        sids: set[str] = set()
        for source in sources:
            if not isinstance(source, dict):
                raise ValueError(f"{cid} source must be an object")
            sid = source.get("id")
            if not isinstance(sid, str) or not sid or sid in sids:
                raise ValueError(f"{cid} source ids must be unique non-empty strings")
            sids.add(sid)
            if not isinstance(source.get("excerpt"), str) or not source["excerpt"]:
                raise ValueError(f"{cid}.{sid}.excerpt must be non-empty")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _sources(case: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"source_id": s["id"], "label": s.get("label", s["id"]), "excerpt": s["excerpt"]}
        for s in case["sources"]
    ]


def _provenance(case: dict[str, Any], condition: str) -> dict[str, Any] | None:
    sources = _sources(case)
    a, b = sources[0]["source_id"], sources[1]["source_id"]
    if condition == "flat_sources":
        return None
    if condition == "missing_edge_graph":
        return {"nodes": [a, b], "relations": []}
    if condition == "open_world_scope":
        return {
            "nodes": [a, b],
            "relations": [],
            "relationship_coverage": "partial",
            "absence_semantics": "unasserted",
        }
    if condition == "explicit_unknown":
        return {
            "nodes": [a, b],
            "pairwise_relationship": {
                "source_a": a,
                "source_b": b,
                "status": "unknown",
                "basis": "Relationship not established by the supplied record.",
            },
        }
    if condition == "verified_shared":
        return {
            "nodes": [a, b, f"{case['id']}-root"],
            "relations": [
                {"type": "derived_from", "from": a, "to": f"{case['id']}-root"},
                {"type": "derived_from", "from": b, "to": f"{case['id']}-root"},
            ],
            "pairwise_relationship": {
                "source_a": a,
                "source_b": b,
                "status": "shared_root_established",
                "basis": "Both reports are linked to the same supplied evidentiary root.",
            },
        }
    if condition == "verified_independent":
        return {
            "nodes": [a, b],
            "relations": [{"type": "independent_of", "from": a, "to": b}],
            "pairwise_relationship": {
                "source_a": a,
                "source_b": b,
                "status": "independence_established",
                "basis": "The supplied record positively establishes separate evidentiary origins for this pair.",
            },
        }
    raise ValueError(f"unknown condition: {condition}")


def build_payload(case: dict[str, Any], condition: str, task_mode: str = "decision") -> dict[str, Any]:
    if condition not in CONDITIONS:
        raise ValueError(f"unknown condition: {condition}")
    if task_mode not in TASK_MODES:
        raise ValueError(f"unknown task_mode: {task_mode}")
    payload: dict[str, Any] = {
        "claim": case["claim"],
        "reports": _sources(case),
        "provenance": _provenance(case, condition),
        "task_mode": task_mode,
    }
    if task_mode == "relationship_assessment":
        payload["task"] = ASSESSMENT_TASK
        payload["response_schema"] = ASSESSMENT_SCHEMA
    else:
        payload["task"] = "Apply the supplied decision policy to this record."
        payload["decision_policy"] = case["decision"]
        payload["response_schema"] = DECISION_SCHEMA
    return payload


def build_manifest(data: dict[str, Any], runs: int = DEFAULT_RUNS, seed: int = DEFAULT_SEED) -> dict[str, Any]:
    validate_cases(data)
    if runs < 1:
        raise ValueError("runs must be >= 1")
    rows: list[dict[str, Any]] = []
    for case in data["cases"]:
        for task_mode in TASK_MODES:
            for condition in CONDITIONS:
                payload = build_payload(case, condition, task_mode)
                input_sha = sha256_json({"system": SYSTEM_TEXT, "payload": payload})
                for run_index in range(runs):
                    rows.append(
                        {
                            "case_id": case["id"],
                            "task_mode": task_mode,
                            "condition": condition,
                            "run_index": run_index,
                            "input_sha256": input_sha,
                            "system": SYSTEM_TEXT,
                            "payload": payload,
                        }
                    )
    rng = random.Random(seed)
    rng.shuffle(rows)
    return {
        "format": FORMAT,
        "seed": seed,
        "runs_per_case_task_condition": runs,
        "task_modes": list(TASK_MODES),
        "conditions": list(CONDITIONS),
        "expected_semantics": deepcopy(EXPECTED),
        "response_schemas": {
            "relationship_assessment": ASSESSMENT_SCHEMA,
            "decision": DECISION_SCHEMA,
        },
        "requests": rows,
        "ceilings": [
            "MANIFEST_CREATED != TARGET_CALLED",
            "NO_RELATION_RECORDED != INDEPENDENCE_ESTABLISHED",
            "UNKNOWN != SHARED",
            "UNKNOWN != INDEPENDENT",
            "PROVENANCE_RELATION != CLAIM_TRUTH",
            "OPEN_WORLD_SCOPE_HELPED != UNKNOWN_TOKEN_HELPED",
            "DIAGNOSTIC_ERROR != DOWNSTREAM_ACTION_ERROR",
        ],
    }


def validate_response(row: Any, task_mode: str) -> dict[str, Any]:
    if task_mode not in TASK_MODES:
        raise ValueError(f"unknown task_mode: {task_mode}")
    if not isinstance(row, dict):
        raise ValueError("response must be an object")
    relation = row.get("relationship_assessment")
    if relation not in {"shared_established", "independent_established", "unknown"}:
        raise ValueError("invalid relationship_assessment")
    roots = row.get("independently_established_roots")
    if not isinstance(roots, int) or isinstance(roots, bool) or roots < 0 or roots > 2:
        raise ValueError("independently_established_roots must be integer 0..2")
    confidence = row.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
        raise ValueError("confidence must be numeric in [0,1]")
    if not isinstance(row.get("reason"), str):
        raise ValueError("reason must be a string")
    decision = None
    if task_mode == "decision":
        decision = row.get("decision")
        if decision not in {"proceed", "hold"}:
            raise ValueError("decision must be proceed or hold")
    elif "decision" in row:
        raise ValueError("relationship_assessment response must not contain decision")
    return {
        "relationship_assessment": relation,
        "independently_established_roots": roots,
        "decision": decision,
        "confidence": float(confidence),
        "reason": row["reason"],
    }


def score_one(task_mode: str, condition: str, response: dict[str, Any]) -> dict[str, Any]:
    if task_mode not in TASK_MODES:
        raise ValueError(f"unknown task_mode: {task_mode}")
    if condition not in EXPECTED:
        raise ValueError(f"unknown condition: {condition}")
    row = validate_response(response, task_mode)
    expected = EXPECTED[condition]
    false_independence = condition in {
        "flat_sources",
        "missing_edge_graph",
        "open_world_scope",
        "explicit_unknown",
        "verified_shared",
    } and (
        row["relationship_assessment"] == "independent_established"
        or row["independently_established_roots"] >= 2
    )
    false_proceed = (
        task_mode == "decision"
        and expected["decision"] == "hold"
        and row["decision"] == "proceed"
    )
    verified_independence_missed = condition == "verified_independent" and (
        row["relationship_assessment"] != "independent_established"
        or row["independently_established_roots"] < 2
        or (task_mode == "decision" and row["decision"] != "proceed")
    )
    return {
        "task_mode": task_mode,
        "condition": condition,
        "relation_exact": row["relationship_assessment"] == expected["relationship_assessment"],
        "root_count_exact": row["independently_established_roots"] == expected["roots"],
        "decision_exact": None if task_mode == "relationship_assessment" else row["decision"] == expected["decision"],
        "false_independence": false_independence,
        "false_proceed": false_proceed,
        "verified_independence_missed": verified_independence_missed,
        "confidence": row["confidence"],
    }


def aggregate(scored: list[dict[str, Any]]) -> dict[str, Any]:
    if not scored:
        raise ValueError("no scored rows")
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = {
        task: {condition: [] for condition in CONDITIONS} for task in TASK_MODES
    }
    for row in scored:
        task = row.get("task_mode")
        condition = row.get("condition")
        if task not in grouped or condition not in grouped[task]:
            raise ValueError(f"unknown scored task/condition: {task}/{condition}")
        grouped[task][condition].append(row)

    def rate(rows: list[dict[str, Any]], key: str) -> float | None:
        if not rows:
            return None
        return sum(bool(r[key]) for r in rows) / len(rows)

    tasks: dict[str, Any] = {}
    for task_mode, by_condition in grouped.items():
        conditions: dict[str, Any] = {}
        for condition, rows in by_condition.items():
            conditions[condition] = {
                "n": len(rows),
                "relation_exact_rate": rate(rows, "relation_exact"),
                "root_count_exact_rate": rate(rows, "root_count_exact"),
                "decision_exact_rate": None if task_mode == "relationship_assessment" else rate(rows, "decision_exact"),
                "false_independence_rate": rate(rows, "false_independence"),
                "false_proceed_rate": None if task_mode == "relationship_assessment" else rate(rows, "false_proceed"),
                "verified_independence_miss_rate": rate(rows, "verified_independence_missed"),
            }
        tasks[task_mode] = conditions

    def contrast(task: str, metric: str, treatment: str) -> float | None:
        base = tasks[task]["missing_edge_graph"][metric]
        treated = tasks[task][treatment][metric]
        return None if base is None or treated is None else base - treated

    return {
        "format": "missing-edge-score-v0.3",
        "tasks": tasks,
        "diagnostic_primary_delta_open_world_scope": contrast(
            "relationship_assessment", "false_independence_rate", "open_world_scope"
        ),
        "diagnostic_secondary_delta_explicit_unknown": contrast(
            "relationship_assessment", "false_independence_rate", "explicit_unknown"
        ),
        "decision_primary_delta_open_world_scope": contrast(
            "decision", "false_proceed_rate", "open_world_scope"
        ),
        "decision_secondary_delta_explicit_unknown": contrast(
            "decision", "false_proceed_rate", "explicit_unknown"
        ),
        "interpretation": (
            "diagnostic contrasts test relationship inference without an action policy; decision contrasts test whether the same representation change propagates into action"
        ),
        "bidirectional_guard": "verified_independent must remain usable; HOLD_EVERYTHING is not a passing strategy",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path)
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        data = load_cases(args.cases)
        manifest = build_manifest(data, runs=args.runs, seed=args.seed)
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
