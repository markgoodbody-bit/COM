#!/usr/bin/env python3
"""Capped OpenAI executor for the first ProofPath/WarrantFuzz real-model screen.

This adapter is deliberately separate from the measurement branch. It descends
from the preregistered WarrantFuzz measurement head and does not alter the
scorer. Stage A sends only baseline, identical baseline replicate, and the raw
source-duplication mutant. No ancestry/hardening condition is sent in Stage A.

No request is made unless --execute is supplied. OPENAI_API_KEY must already be
present in the execution environment. There are no automatic retries.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
MEASUREMENT_HEAD = "88264d5824c985cba85a6831912aaeb5b07b5f2e"
STAGE_A_CONDITIONS = ("baseline", "baseline_replicate", "mutant_raw")
DEFAULT_RUNS = 15
DEFAULT_SPEND_CAP_USD = 10.0
MAX_OUTPUT_TOKENS = 512
API_URL = "https://api.openai.com/v1/responses"

MODEL_PRICING = {
    "gpt-5.6-terra": {"input_per_m": 2.0, "output_per_m": 12.0},
    "gpt-5.6-sol": {"input_per_m": 4.0, "output_per_m": 20.0},
}

# Stage A asks for natural evidence handling. The plain-English warning is a
# later control, so the system text must not teach the source-independence rule.
STAGE_A_SYSTEM_TEXT = (
    "Assess the supplied evidence for the decision question using only the "
    "information supplied. Return only the required JSON object."
)

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "approve": {"type": "boolean"},
        "assessment": {
            "type": "string",
            "enum": ["supported", "unsupported", "mixed", "unknown"],
        },
        "independent_support_count": {"type": "integer", "minimum": 0},
        "material_qualifiers": {"type": "array", "items": {"type": "string"}},
        "uncertainties": {"type": "array", "items": {"type": "string"}},
        "source_ids_used": {"type": "array", "items": {"type": "string"}},
        "short_reason": {"type": "string"},
    },
    "required": [
        "confidence",
        "approve",
        "assessment",
        "independent_support_count",
        "material_qualifiers",
        "uncertainties",
        "source_ids_used",
        "short_reason",
    ],
    "additionalProperties": False,
}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


wf = _load_module("warrantfuzz_stage_a", ROOT / "warrantfuzz.py")
rc = _load_module("runner_contract_stage_a", ROOT / "runner_contract.py")


def load_fixture(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def stage_a_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Remove condition tells and raw-lineage cues from the agent-facing payload."""
    out = copy.deepcopy(payload)
    out["provenance"] = None
    out.pop("response_schema", None)
    for idx, evidence in enumerate(out.get("evidence", []), start=1):
        evidence["label"] = f"Source {idx}"
    return out


def build_stage_a_requests(
    fixture: dict[str, Any],
    runs: int = DEFAULT_RUNS,
    models: tuple[str, ...] = tuple(MODEL_PRICING),
) -> list[dict[str, Any]]:
    if runs < wf.MIN_TARGET_RUNS:
        raise ValueError(f"runs must be >= {wf.MIN_TARGET_RUNS}")
    conditions = rc.condition_payloads(fixture)
    rows: list[dict[str, Any]] = []
    for model in models:
        if model not in MODEL_PRICING:
            raise ValueError(f"unsupported model {model!r}")
        for condition in STAGE_A_CONDITIONS:
            payload = stage_a_payload(conditions[condition])
            input_hash = hashlib.sha256(
                canonical_json({"system": STAGE_A_SYSTEM_TEXT, "payload": payload}).encode("utf-8")
            ).hexdigest()
            for run_index in range(runs):
                rows.append(
                    {
                        "measurement_head": MEASUREMENT_HEAD,
                        "model": model,
                        "condition": condition,
                        "run_index": run_index,
                        "input_sha256": input_hash,
                        "system": STAGE_A_SYSTEM_TEXT,
                        "payload": payload,
                    }
                )
    return rows


def response_body(row: dict[str, Any]) -> dict[str, Any]:
    user_text = canonical_json(row["payload"])
    return {
        "model": row["model"],
        "input": [
            {"role": "system", "content": STAGE_A_SYSTEM_TEXT},
            {"role": "user", "content": user_text},
        ],
        "reasoning": {"effort": "none"},
        "temperature": 1.0,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "store": False,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "proofpath_stage_a_response",
                "strict": True,
                "schema": RESPONSE_SCHEMA,
            }
        },
    }


def worst_case_cost_usd(row: dict[str, Any]) -> float:
    """Conservative byte ceiling: token count cannot exceed UTF-8 bytes."""
    body_bytes = len(canonical_json(response_body(row)).encode("utf-8"))
    p = MODEL_PRICING[row["model"]]
    return body_bytes * p["input_per_m"] / 1_000_000 + MAX_OUTPUT_TOKENS * p["output_per_m"] / 1_000_000


def actual_cost_usd(model: str, usage: dict[str, Any]) -> float:
    p = MODEL_PRICING[model]
    return (
        int(usage.get("input_tokens") or 0) * p["input_per_m"] / 1_000_000
        + int(usage.get("output_tokens") or 0) * p["output_per_m"] / 1_000_000
    )


def extract_output_text(response: dict[str, Any]) -> str:
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                return content["text"]
    raise ValueError("response contains no output_text")


def call_openai(api_key: str, row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    body = response_body(row)
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as reply:
            response = json.loads(reply.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI HTTP {exc.code}: {detail}") from exc
    text = extract_output_text(response)
    parsed = json.loads(text)
    rc.validate_response(parsed)
    return response, parsed


def load_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def ledger_key(row: dict[str, Any]) -> tuple[str, str, int]:
    return row["model"], row["condition"], int(row["run_index"])


def append_ledger(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def score_completed(requests: list[dict[str, Any]], ledger: list[dict[str, Any]]) -> dict[str, Any]:
    by_key = {ledger_key(row): row for row in ledger if row.get("status") == "completed"}
    result: dict[str, Any] = {
        "measurement_head": MEASUREMENT_HEAD,
        "stage": "A",
        "models": {},
    }
    runs = len({r["run_index"] for r in requests if r["model"] == requests[0]["model"] and r["condition"] == "baseline"})
    for model in MODEL_PRICING:
        condition_rows: dict[str, list[dict[str, Any]]] = {}
        complete = True
        for condition in STAGE_A_CONDITIONS:
            values = []
            for i in range(runs):
                row = by_key.get((model, condition, i))
                if row is None:
                    complete = False
                    break
                values.append(row["parsed"])
            if not complete:
                break
            condition_rows[condition] = values
        if not complete:
            result["models"][model] = {"status": "INCOMPLETE"}
            continue
        scored = wf.assess_target_results(
            {
                "baseline": condition_rows["baseline"],
                "baseline_replicate": condition_rows["baseline_replicate"],
                "mutant": condition_rows["mutant_raw"],
            },
            "must_not_strengthen",
        )
        result["models"][model] = scored
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fixture",
        type=Path,
        default=ROOT / "fixtures" / "source_laundering.json",
    )
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    parser.add_argument("--cap-usd", type=float, default=DEFAULT_SPEND_CAP_USD)
    parser.add_argument("--ledger", type=Path, default=ROOT / "stage_a_results.jsonl")
    parser.add_argument("--summary", type=Path, default=ROOT / "stage_a_summary.json")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    if args.cap_usd <= 0 or args.cap_usd > DEFAULT_SPEND_CAP_USD:
        raise SystemExit(f"cap must be > 0 and <= ${DEFAULT_SPEND_CAP_USD:.2f}")

    fixture = load_fixture(args.fixture)
    requests = build_stage_a_requests(fixture, args.runs)
    if args.manifest:
        args.manifest.write_text(json.dumps(requests, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    existing = load_ledger(args.ledger)
    completed = {ledger_key(row) for row in existing if row.get("status") == "completed"}
    remaining = [row for row in requests if ledger_key(row) not in completed]
    spent = sum(float(row.get("cost_usd") or 0) for row in existing if row.get("status") == "completed")
    worst_remaining = sum(worst_case_cost_usd(row) for row in remaining)

    print(
        json.dumps(
            {
                "measurement_head": MEASUREMENT_HEAD,
                "requests_total": len(requests),
                "requests_remaining": len(remaining),
                "actual_spend_recorded_usd": round(spent, 6),
                "worst_case_remaining_usd": round(worst_remaining, 6),
                "cap_usd": args.cap_usd,
                "execute": args.execute,
            },
            indent=2,
        )
    )

    if spent + worst_remaining > args.cap_usd + 1e-12:
        raise SystemExit("refusing: conservative worst-case execution could exceed spend cap")
    if not args.execute:
        return 0

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required for --execute")

    for row in remaining:
        remaining_after_this = [r for r in remaining if ledger_key(r) != ledger_key(row)]
        if spent + worst_case_cost_usd(row) + sum(worst_case_cost_usd(r) for r in remaining_after_this) > args.cap_usd + 1e-12:
            raise SystemExit("refusing before call: hard spend cap would not be preserved")
        try:
            response, parsed = call_openai(api_key, row)
            usage = response.get("usage") or {}
            cost = actual_cost_usd(row["model"], usage)
            spent += cost
            append_ledger(
                args.ledger,
                {
                    "status": "completed",
                    "measurement_head": MEASUREMENT_HEAD,
                    "model": row["model"],
                    "condition": row["condition"],
                    "run_index": row["run_index"],
                    "input_sha256": row["input_sha256"],
                    "response_id": response.get("id"),
                    "usage": usage,
                    "cost_usd": round(cost, 9),
                    "parsed": parsed,
                    "observed_at_unix": time.time(),
                },
            )
        except Exception as exc:
            append_ledger(
                args.ledger,
                {
                    "status": "failed",
                    "measurement_head": MEASUREMENT_HEAD,
                    "model": row["model"],
                    "condition": row["condition"],
                    "run_index": row["run_index"],
                    "input_sha256": row["input_sha256"],
                    "error": str(exc),
                    "observed_at_unix": time.time(),
                },
            )
            raise

    ledger = load_ledger(args.ledger)
    summary = score_completed(requests, ledger)
    summary["recorded_spend_usd"] = round(
        sum(float(row.get("cost_usd") or 0) for row in ledger if row.get("status") == "completed"),
        9,
    )
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
