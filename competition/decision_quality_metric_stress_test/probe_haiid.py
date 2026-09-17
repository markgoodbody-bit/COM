#!/usr/bin/env python3
"""Disposable pre-sprint feasibility probe for PR #361.

This is not the sprint artefact and not a new metric. It re-analyses the
MIT-licensed Human-AI Interactions Dataset (HAIID) using only measurements
supported directly by the released schema/helper code.

Upstream dataset commit is pinned. No model/API calls are made.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

UPSTREAM_COMMIT = "24881cc7586180a9c9742a7dd838aea97d008235"
DATA_URL = (
    "https://raw.githubusercontent.com/kailas-v/human-ai-interactions/"
    f"{UPSTREAM_COMMIT}/haiid_dataset.csv"
)
UPSTREAM_REPO = "https://github.com/kailas-v/human-ai-interactions"
UPSTREAM_LICENSE = "MIT"

# Metrics with an explicit quality direction. Activation / weight-of-advice are
# reported descriptively but are not labelled 'better' because more reliance or
# more movement is not intrinsically better.
QUALITY_DIRECTIONS = {
    "final_accuracy": "higher",
    "team_gain": "higher",
    "correct_confidence": "higher",
    "beneficial_correction_rate": "higher",
    "harmful_override_rate": "lower",
}


def fnum(value: str) -> float | None:
    try:
        if value is None or not str(value).strip():
            return None
        x = float(value)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def condition_key(row: dict[str, str]) -> str | None:
    source = (row.get("advice_source") or "").strip().lower()
    pa = fnum(row.get("perceived_accuracy", ""))
    if source not in {"human", "ai"} or pa is None:
        return None
    # Released schema says perceived_accuracy ∈ {65,80,95}. Refuse other values
    # rather than silently making new treatment groups.
    pa_i = int(round(pa))
    if pa_i not in {65, 80, 95} or abs(pa - pa_i) > 1e-9:
        return None
    return f"{source}@{pa_i}"


def download(path: Path) -> None:
    request = urllib.request.Request(
        DATA_URL,
        headers={"User-Agent": "COM-decision-quality-feasibility-probe/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        path.write_bytes(response.read())


def init_bucket() -> dict[str, Any]:
    return {
        "n": 0,
        "initial_correct": 0,
        "final_correct": 0,
        "correct_confidence_sum": 0.0,
        "correct_confidence_n": 0,
        "activated": 0,
        "woa": [],
        "beneficial_eligible": 0,
        "beneficial_corrected": 0,
        "harmful_eligible": 0,
        "harmful_overridden": 0,
    }


def add_row(bucket: dict[str, Any], row: dict[str, str]) -> None:
    r1 = fnum(row.get("response_1", ""))
    r2 = fnum(row.get("response_2", ""))
    advice = fnum(row.get("advice", ""))
    if r1 is None or r2 is None or advice is None:
        return

    bucket["n"] += 1
    bucket["initial_correct"] += int(r1 > 0)
    bucket["final_correct"] += int(r2 > 0)
    bucket["correct_confidence_sum"] += r2
    bucket["correct_confidence_n"] += 1
    bucket["activated"] += int(abs(r2 - r1) > 0.07)

    denom = advice - r1 + 1e-3  # released helper's convention
    if abs(denom) > 1e-12:
        w = (r2 - r1) / denom
        if math.isfinite(w):
            bucket["woa"].append(w)

    # Beneficial correction: participant initially wrong, advice correct.
    if r1 < 0 and advice > 0:
        bucket["beneficial_eligible"] += 1
        bucket["beneficial_corrected"] += int(r2 > 0)

    # Harmful override: participant initially correct, advice wrong.
    if r1 > 0 and advice < 0:
        bucket["harmful_eligible"] += 1
        bucket["harmful_overridden"] += int(r2 < 0)


def finalize(bucket: dict[str, Any]) -> dict[str, Any]:
    n = bucket["n"]
    if not n:
        return {"n": 0}
    initial_accuracy = bucket["initial_correct"] / n
    final_accuracy = bucket["final_correct"] / n
    be = bucket["beneficial_eligible"]
    he = bucket["harmful_eligible"]
    woa = bucket["woa"]
    return {
        "n": n,
        "initial_accuracy": initial_accuracy,
        "final_accuracy": final_accuracy,
        "team_gain": final_accuracy - initial_accuracy,
        "correct_confidence": bucket["correct_confidence_sum"] / bucket["correct_confidence_n"],
        "activation_rate": bucket["activated"] / n,
        "weight_of_advice_median": statistics.median(woa) if woa else None,
        "beneficial_eligible": be,
        "beneficial_correction_rate": bucket["beneficial_corrected"] / be if be else None,
        "harmful_eligible": he,
        "harmful_override_rate": bucket["harmful_overridden"] / he if he else None,
    }


def rank_conditions(metrics: dict[str, dict[str, Any]], metric: str, direction: str) -> list[tuple[str, float]]:
    rows = []
    for condition, values in metrics.items():
        value = values.get(metric)
        if isinstance(value, (int, float)) and math.isfinite(value):
            rows.append((condition, float(value)))
    rows.sort(key=lambda x: x[1], reverse=(direction == "higher"))
    return rows


def pairwise_disagreement(rank_a: list[tuple[str, float]], rank_b: list[tuple[str, float]]) -> dict[str, Any]:
    """Simple order-disagreement count; ties are excluded, not broken arbitrarily."""
    a = dict(rank_a)
    b = dict(rank_b)
    common = sorted(set(a) & set(b))
    comparable = 0
    discordant = 0
    for i, x in enumerate(common):
        for y in common[i + 1 :]:
            da = a[x] - a[y]
            db = b[x] - b[y]
            if abs(da) <= 1e-12 or abs(db) <= 1e-12:
                continue
            comparable += 1
            discordant += int((da > 0) != (db > 0))
    return {
        "comparable_pairs": comparable,
        "discordant_pairs": discordant,
        "discordance_rate": discordant / comparable if comparable else None,
    }


def analyze(path: Path) -> dict[str, Any]:
    # scope -> condition -> bucket. Scope 'ALL' is retained but interpreted
    # cautiously because task mixture is itself an aggregation choice.
    buckets: dict[str, dict[str, dict[str, Any]]] = defaultdict(lambda: defaultdict(init_bucket))
    raw_rows = 0
    used_rows = 0
    tasks = set()

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw_rows += 1
            task = (row.get("task_name") or "").strip().lower()
            condition = condition_key(row)
            if not task or condition is None:
                continue
            r1 = fnum(row.get("response_1", ""))
            r2 = fnum(row.get("response_2", ""))
            advice = fnum(row.get("advice", ""))
            if r1 is None or r2 is None or advice is None:
                continue
            used_rows += 1
            tasks.add(task)
            add_row(buckets[task][condition], row)
            add_row(buckets["ALL"][condition], row)

    result: dict[str, Any] = {
        "probe": "HAIID metric-ranking feasibility",
        "claim_ceiling": "descriptive public-data feasibility probe; not a sprint result",
        "upstream_repo": UPSTREAM_REPO,
        "upstream_commit": UPSTREAM_COMMIT,
        "upstream_license": UPSTREAM_LICENSE,
        "raw_rows": raw_rows,
        "used_rows": used_rows,
        "tasks": sorted(tasks),
        "quality_directions": QUALITY_DIRECTIONS,
        "scopes": {},
    }

    for scope in [*sorted(tasks), "ALL"]:
        metrics = {cond: finalize(bucket) for cond, bucket in sorted(buckets[scope].items())}
        rankings = {
            metric: rank_conditions(metrics, metric, direction)
            for metric, direction in QUALITY_DIRECTIONS.items()
        }
        top = {metric: (rows[0][0] if rows else None) for metric, rows in rankings.items()}
        pairwise = {}
        metric_names = list(QUALITY_DIRECTIONS)
        for i, a in enumerate(metric_names):
            for b in metric_names[i + 1 :]:
                pairwise[f"{a}__vs__{b}"] = pairwise_disagreement(rankings[a], rankings[b])
        result["scopes"][scope] = {
            "conditions": metrics,
            "rankings": {k: [{"condition": c, "value": v} for c, v in rows] for k, rows in rankings.items()},
            "top_condition": top,
            "top_condition_count": len({x for x in top.values() if x is not None}),
            "pairwise_order_disagreement": pairwise,
        }

    return result


def print_summary(result: dict[str, Any]) -> None:
    print(f"raw_rows={result['raw_rows']} used_rows={result['used_rows']} tasks={','.join(result['tasks'])}")
    for scope, data in result["scopes"].items():
        tops = data["top_condition"]
        print(f"\n[{scope}] distinct_top_conditions={data['top_condition_count']}")
        for metric in QUALITY_DIRECTIONS:
            ranking = data["rankings"][metric]
            short = " > ".join(f"{r['condition']}:{r['value']:.4f}" for r in ranking)
            print(f"  {metric}: {short}")
        disagreements = [
            (name, row["discordance_rate"])
            for name, row in data["pairwise_order_disagreement"].items()
            if isinstance(row.get("discordance_rate"), (int, float)) and row["discordance_rate"] > 0
        ]
        disagreements.sort(key=lambda x: x[1], reverse=True)
        print("  metric-pair discordance:")
        if not disagreements:
            print("    NONE OBSERVED")
        else:
            for name, rate in disagreements:
                print(f"    {name}: {rate:.3f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("/tmp/haiid_dataset.csv"))
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    if args.download or not args.data.exists():
        download(args.data)
    result = analyze(args.data)
    print_summary(result)
    if args.json_out:
        args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
