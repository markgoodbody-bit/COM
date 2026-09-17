#!/usr/bin/env python3
"""Capped OpenAI executor for ProofPath/WarrantFuzz Stage A.

Stage A is a bounded real-model screen only:
- 15 baseline runs,
- 15 byte-identical baseline-replicate runs,
- 15 raw duplicate-evidence mutant runs,
for each of gpt-5.6-terra and gpt-5.6-sol.

The measurement/scoring contract is pinned to PR #351 head
88264d5824c985cba85a6831912aaeb5b07b5f2e. This adapter changes provider
plumbing and the pre-registered agent-facing evidence presentation only; it does
not change the scorer. No request is made unless --execute is supplied.
OPENAI_API_KEY must already be present. There are no automatic retries.
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

STAGE_A_SYSTEM_TEXT = (
    "Assess the supplied evidence for the decision question using only the "
    "information supplied. Return only the required JSON object."
)

# The base fixture has no source text. Stage A supplies a synthetic matched
# content pair so the second row is recognisable in principle as a retelling
# without telling the model that it is one.
ORIGIN_EXCERPT = (
    "In a 240-case pilot, median review time fell from 50 minutes to 41 minutes "
    "after the workflow change."
)
RETELLING_EXCERPT = (
    "Across 240 pilot cases, the workflow change was followed by a nine-minute "
    "drop in median review time, from 50 to 41 minutes."
)

FORBIDDEN_AGENT_CUES = ("origin", "derivative", "duplicate", "copy", "paraphrase")

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


def _neutralise_evidence(
    evidence_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """Return agent-facing rows plus internal->neutral id map.

    Neutral ids are visible to the model; original fixture ids remain only in the
    manifest metadata so a result can be traced without leaking lineage labels.
    """
    neutral_rows: list[dict[str, Any]] = []
    id_map: dict[str, str] = {}
    for idx, row in enumerate(evidence_rows, start=1):
        internal_id = str(row.get("source_id"))
        neutral_id = f"src-{idx}"
        id_map[internal_id] = neutral_id
        neutral_rows.append(
            {
                "source_id": neutral_id,
                "label": f"Source {idx}",
                "stance": row.get("stance"),
                "excerpt": ORIGIN_EXCERPT if idx == 1 else RETELLING_EXCERPT,
            }
        )
    return neutral_rows, id_map


def stage_a_payload(payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
    """Remove lineage/control tells while keeping overlap observable in principle."""
    out = copy.deepcopy(payload)
    out["provenance"] = None
    out.pop("response_schema", None)
    neutral_rows, id_map = _neutralise_evidence(out.get("evidence", []))
    out["evidence"] = neutral_rows
    return out, id_map


def assert_no_agent_facing_tells(payload: dict[str, Any]) -> None:
    rendered = canonical_json(payload).lower()
    for cue in FORBIDDEN_AGENT_CUES:
        if cue in rendered:
            raise ValueError(f"agent-facing payload leaks forbidden cue: {cue}")


def build_stage_a_requests(
    fixture: dict[str, Any],
    runs: int = DEFAULT_RUNS,
    models: tuple[str, ...] = tuple(MODEL_PRICING),
) -> list[dict[str, Any]]:
    if runs < wf.MIN_TARGET_RUNS:
        raise ValueError(f"runs must be >= {wf.MIN_TARGET_RUNS}")
    conditions = rc.condition_payloads(fixture)

    prepared: dict[str, tuple[dict[str, Any], dict[str, str], str]] = {}
    for condition in STAGE_A_CONDITIONS:
        payload, id_map = stage_a_payload(conditions[condition])
        assert_no_agent_facing_tells(payload)
        input_hash = hashlib.sha256(
            canonical_json({"system": STAGE_A_SYSTEM_TEXT, "payload": payload}).encode("utf-8")
        ).hexdigest()
        prepared[condition] = (payload, id_map, input_hash)

    rows: list[dict[str, Any]] = []
    # Round-robin the three conditions at each run index so provider/routing drift
    # is shared across arms rather than aligned with one condition block.
    for model in models:
        if model not in MODEL_PRICING:
            raise ValueError(f"unsupported model {model!r}")
        for run_index in range(runs):
            for condition in STAGE_A_CONDITIONS:
                payload, id_map, input_hash = prepared[condition]
                rows.append(
                    {
                        "measurement_head": MEASUREMENT_HEAD,
                        "model": model,
                        "condition": condition,
                        "run_index": run_index,
                        "input_sha256": input_hash,
                        "source_id_map": id_map,
                        "system": STAGE_A_SYSTEM_TEXT,
                        "payload": payload,
                    }
                )
    for row in rows:
        row["request_sha256"] = request_identity(row)
    return rows


def response_body(row: dict[str, Any]) -> dict[str, Any]:
    # source_id_map and condition labels are deliberately not sent.
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


def request_identity(row: dict[str, Any]) -> str:
    """Bind the endpoint and complete provider contract, not just prose input."""
    contract = {"url": API_URL, "body": response_body(row)}
    return hashlib.sha256(canonical_json(contract).encode("utf-8")).hexdigest()


def validate_ledger(requests: list[dict[str, Any]], ledger: list[dict[str, Any]]) -> None:
    expected = {}
    for request in requests:
        key = ledger_key(request)
        if key in expected:
            raise ValueError(f"duplicate manifest key: {key}")
        if request.get("request_sha256") != request_identity(request):
            raise ValueError(f"stale manifest request identity: {key}")
        expected[key] = request
    seen = set()
    for row in ledger:
        key = ledger_key(row)
        if key in seen:
            raise ValueError(f"duplicate ledger key: {key}")
        seen.add(key)
        if key not in expected:
            raise ValueError(f"unexpected ledger key: {key}")
        if row.get("status") not in {"completed", "failed"}:
            raise ValueError(f"unknown ledger status: {key}")
        for field in ("measurement_head", "input_sha256", "request_sha256"):
            if row.get(field) != expected[key].get(field):
                raise ValueError(f"ledger {field} mismatch: {key}")


def worst_case_cost_usd(row: dict[str, Any]) -> float:
    """Conservative byte ceiling: token count cannot exceed UTF-8 bytes."""
    body_bytes = len(canonical_json(response_body(row)).encode("utf-8"))
    p = MODEL_PRICING[row["model"]]
    return (
        body_bytes * p["input_per_m"] / 1_000_000
        + MAX_OUTPUT_TOKENS * p["output_per_m"] / 1_000_000
    )


def actual_cost_usd(model: str, usage: dict[str, Any]) -> float:
    if not isinstance(usage, dict) or any(
        type(usage.get(key)) is not int or usage[key] < 0
        for key in ("input_tokens", "output_tokens")
    ):
        raise ValueError("missing or invalid token usage")
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


def accounted_spend_usd(ledger: list[dict[str, Any]]) -> float:
    """Actual completed cost + worst-case reservation for failed attempts.

    A failed HTTP attempt may still have been billed. Reserving its whole-call
    worst case prevents the cap from relying on unobservable provider behaviour.
    """
    total = 0.0
    for row in ledger:
        if row.get("status") == "completed":
            total += float(row.get("cost_usd") or 0.0)
        elif row.get("status") == "failed":
            total += float(row.get("reserved_cost_usd") or 0.0)
    return total


def attempted_keys(ledger: list[dict[str, Any]]) -> set[tuple[str, str, int]]:
    # Failed calls are not silently retried. A new explicit execution decision is
    # required before changing that historical attempt state.
    return {
        ledger_key(row)
        for row in ledger
        if row.get("status") in {"completed", "failed"}
    }


def score_completed(requests: list[dict[str, Any]], ledger: list[dict[str, Any]]) -> dict[str, Any]:
    validate_ledger(requests, ledger)
    by_key = {ledger_key(row): row for row in ledger if row.get("status") == "completed"}
    result: dict[str, Any] = {
        "measurement_head": MEASUREMENT_HEAD,
        "stage": "A",
        "models": {},
    }
    runs = len(
        {
            r["run_index"]
            for r in requests
            if r["model"] == requests[0]["model"] and r["condition"] == "baseline"
        }
    )
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
        result["models"][model] = wf.assess_target_results(
            {
                "baseline": condition_rows["baseline"],
                "baseline_replicate": condition_rows["baseline_replicate"],
                "mutant": condition_rows["mutant_raw"],
            },
            "must_not_strengthen",
        )
    return result


def write_summary(
    path: Path,
    requests: list[dict[str, Any]],
    ledger: list[dict[str, Any]],
    execution_status: str,
) -> dict[str, Any]:
    summary = score_completed(requests, ledger)
    summary["execution_status"] = execution_status
    summary["attempted_calls"] = len(attempted_keys(ledger))
    summary["completed_calls"] = sum(1 for r in ledger if r.get("status") == "completed")
    summary["failed_calls"] = sum(1 for r in ledger if r.get("status") == "failed")
    summary["accounted_spend_usd"] = round(accounted_spend_usd(ledger), 9)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


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
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(
            json.dumps(requests, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    existing = load_ledger(args.ledger)
    validate_ledger(requests, existing)
    attempted = attempted_keys(existing)
    remaining = [row for row in requests if ledger_key(row) not in attempted]
    spent = accounted_spend_usd(existing)
    worst_remaining = sum(worst_case_cost_usd(row) for row in remaining)

    print(
        json.dumps(
            {
                "measurement_head": MEASUREMENT_HEAD,
                "requests_total": len(requests),
                "requests_attempted": len(attempted),
                "requests_remaining": len(remaining),
                "accounted_spend_usd": round(spent, 6),
                "worst_case_remaining_usd": round(worst_remaining, 6),
                "cap_usd": args.cap_usd,
                "execute": args.execute,
            },
            indent=2,
        )
    )

    if spent + worst_remaining > args.cap_usd + 1e-12:
        write_summary(args.summary, requests, existing, "REFUSED_SPEND_CAP")
        raise SystemExit("refusing: conservative worst-case execution could exceed spend cap")
    if not args.execute:
        write_summary(args.summary, requests, existing, "DRY_RUN")
        return 0

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        write_summary(args.summary, requests, existing, "BLOCKED_NO_CREDENTIAL_ROUTE")
        raise SystemExit("OPENAI_API_KEY is required for --execute")

    ledger = list(existing)
    for pos, row in enumerate(remaining):
        later = remaining[pos + 1 :]
        if spent + worst_case_cost_usd(row) + sum(worst_case_cost_usd(r) for r in later) > args.cap_usd + 1e-12:
            write_summary(args.summary, requests, ledger, "REFUSED_SPEND_CAP")
            raise SystemExit("refusing before call: hard spend cap would not be preserved")
        try:
            response, parsed = call_openai(api_key, row)
            usage = response.get("usage")
            try:
                cost = actual_cost_usd(row["model"], usage)
                cost_basis = "reported_usage"
            except ValueError:
                cost = worst_case_cost_usd(row)
                cost_basis = "worst_case_usage_unavailable"
            completed = {
                "status": "completed",
                "measurement_head": MEASUREMENT_HEAD,
                "model": row["model"],
                "condition": row["condition"],
                "run_index": row["run_index"],
                "input_sha256": row["input_sha256"],
                "request_sha256": row["request_sha256"],
                "response_id": response.get("id"),
                "usage": usage,
                "cost_usd": round(cost, 9),
                "cost_basis": cost_basis,
                "usage_missing_or_invalid": cost_basis != "reported_usage",
                "parsed": parsed,
                "observed_at_unix": time.time(),
            }
            append_ledger(args.ledger, completed)
            ledger.append(completed)
            spent = accounted_spend_usd(ledger)
        except Exception as exc:
            failed = {
                "status": "failed",
                "measurement_head": MEASUREMENT_HEAD,
                "model": row["model"],
                "condition": row["condition"],
                "run_index": row["run_index"],
                "input_sha256": row["input_sha256"],
                "request_sha256": row["request_sha256"],
                "reserved_cost_usd": round(worst_case_cost_usd(row), 9),
                "error": str(exc),
                "observed_at_unix": time.time(),
            }
            append_ledger(args.ledger, failed)
            ledger.append(failed)
            write_summary(args.summary, requests, ledger, "FAILED_STOP_NO_RETRY")
            raise

    summary = write_summary(args.summary, requests, ledger, "COMPLETED")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
