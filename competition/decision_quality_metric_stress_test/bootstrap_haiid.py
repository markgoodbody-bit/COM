#!/usr/bin/env python3
"""Participant-cluster bootstrap for the HAIID feasibility probe.

This is a second, predeclared feasibility gate for PR #361. It uses the exact
five quality metrics frozen before the first HAIID result and resamples whole
participants within task × intervention condition. It does not pool tasks for
inference and does not add a composite decision-quality score.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("probe_haiid_bootstrap", HERE / "probe_haiid.py")
probe = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = probe
SPEC.loader.exec_module(probe)

DEFAULT_REPLICATES = 2000
DEFAULT_SEED = 20260917
ALPHA = 0.05


def init_cluster() -> dict[str, float | int]:
    return {
        "n": 0,
        "initial_correct": 0,
        "final_correct": 0,
        "correct_confidence_sum": 0.0,
        "correct_confidence_n": 0,
        "beneficial_eligible": 0,
        "beneficial_corrected": 0,
        "harmful_eligible": 0,
        "harmful_overridden": 0,
    }


def add_cluster_row(cluster: dict[str, float | int], row: dict[str, str]) -> None:
    r1 = probe.fnum(row.get("response_1", ""))
    r2 = probe.fnum(row.get("response_2", ""))
    advice = probe.fnum(row.get("advice", ""))
    if r1 is None or r2 is None or advice is None:
        return
    cluster["n"] += 1
    cluster["initial_correct"] += int(r1 > 0)
    cluster["final_correct"] += int(r2 > 0)
    cluster["correct_confidence_sum"] += r2
    cluster["correct_confidence_n"] += 1
    if r1 < 0 and advice > 0:
        cluster["beneficial_eligible"] += 1
        cluster["beneficial_corrected"] += int(r2 > 0)
    if r1 > 0 and advice < 0:
        cluster["harmful_eligible"] += 1
        cluster["harmful_overridden"] += int(r2 < 0)


def combine(clusters: list[dict[str, float | int]], indices: list[int] | None = None) -> dict[str, float | int]:
    out = init_cluster()
    selected = clusters if indices is None else [clusters[i] for i in indices]
    for c in selected:
        for key in out:
            out[key] += c[key]
    return out


def metrics_from_cluster(c: dict[str, float | int]) -> dict[str, float | None]:
    n = int(c["n"])
    if n <= 0:
        return {metric: None for metric in probe.QUALITY_DIRECTIONS}
    initial_accuracy = float(c["initial_correct"]) / n
    final_accuracy = float(c["final_correct"]) / n
    cc_n = int(c["correct_confidence_n"])
    be = int(c["beneficial_eligible"])
    he = int(c["harmful_eligible"])
    return {
        "final_accuracy": final_accuracy,
        "team_gain": final_accuracy - initial_accuracy,
        "correct_confidence": float(c["correct_confidence_sum"]) / cc_n if cc_n else None,
        "beneficial_correction_rate": float(c["beneficial_corrected"]) / be if be else None,
        "harmful_override_rate": float(c["harmful_overridden"]) / he if he else None,
    }


def oriented(metric: str, value: float | None) -> float | None:
    if value is None:
        return None
    return value if probe.QUALITY_DIRECTIONS[metric] == "higher" else -value


def quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("quantile requires values")
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return xs[lo]
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def load_clusters(path: Path) -> tuple[dict[str, dict[str, list[dict[str, float | int]]]], dict[str, Any]]:
    # task -> condition -> participant -> cluster
    tmp: dict[str, dict[str, dict[str, dict[str, float | int]]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    raw_rows = 0
    used_rows = 0
    missing_participant = 0
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            raw_rows += 1
            task = (row.get("task_name") or "").strip().lower()
            condition = probe.condition_key(row)
            participant = (row.get("participant_id") or "").strip()
            if not task or condition is None:
                continue
            if not participant:
                missing_participant += 1
                continue
            if any(probe.fnum(row.get(key, "")) is None for key in ("response_1", "response_2", "advice")):
                continue
            used_rows += 1
            cluster = tmp[task][condition].setdefault(participant, init_cluster())
            add_cluster_row(cluster, row)

    clusters: dict[str, dict[str, list[dict[str, float | int]]]] = {}
    participant_counts = {}
    for task, conditions in tmp.items():
        clusters[task] = {}
        participant_counts[task] = {}
        for condition, participants in conditions.items():
            clusters[task][condition] = list(participants.values())
            participant_counts[task][condition] = len(participants)
    meta = {
        "raw_rows": raw_rows,
        "used_rows": used_rows,
        "missing_participant_rows": missing_participant,
        "participant_counts": participant_counts,
    }
    return clusters, meta


def analyze(path: Path, replicates: int, seed: int) -> dict[str, Any]:
    if replicates < 100:
        raise ValueError("replicates must be >= 100")
    clusters, meta = load_clusters(path)
    rng = random.Random(seed)

    out: dict[str, Any] = {
        "probe": "HAIID participant-cluster bootstrap",
        "claim_ceiling": "uncertainty gate for feasibility result; not a sprint result or causal estimate",
        "upstream_repo": probe.UPSTREAM_REPO,
        "upstream_commit": probe.UPSTREAM_COMMIT,
        "upstream_license": probe.UPSTREAM_LICENSE,
        "bootstrap_replicates": replicates,
        "bootstrap_seed": seed,
        "alpha": ALPHA,
        **meta,
        "tasks": {},
    }

    for task in sorted(clusters):
        conditions = clusters[task]
        observed = {
            condition: metrics_from_cluster(combine(rows))
            for condition, rows in conditions.items()
        }
        eligible = {
            condition: {
                "participants": len(rows),
                "rows": int(combine(rows)["n"]),
                "beneficial_eligible": int(combine(rows)["beneficial_eligible"]),
                "harmful_eligible": int(combine(rows)["harmful_eligible"]),
            }
            for condition, rows in conditions.items()
        }

        # Freeze the bootstrap draw for each condition and replicate once, then
        # reuse it for every metric so metric comparisons see the same resample.
        replicate_metrics: list[dict[str, dict[str, float | None]]] = []
        for _ in range(replicates):
            rep: dict[str, dict[str, float | None]] = {}
            for condition, rows in conditions.items():
                idx = [rng.randrange(len(rows)) for _ in range(len(rows))]
                rep[condition] = metrics_from_cluster(combine(rows, idx))
            replicate_metrics.append(rep)

        metric_results = {}
        for metric in probe.QUALITY_DIRECTIONS:
            observed_rank = probe.rank_conditions(
                observed, metric, probe.QUALITY_DIRECTIONS[metric]
            )
            top_counts = {condition: 0 for condition in conditions}
            valid_top = 0
            for rep in replicate_metrics:
                rank = probe.rank_conditions(rep, metric, probe.QUALITY_DIRECTIONS[metric])
                if rank:
                    top_counts[rank[0][0]] += 1
                    valid_top += 1

            pairs = {}
            condition_names = sorted(conditions)
            for i, a in enumerate(condition_names):
                for b in condition_names[i + 1 :]:
                    oa = oriented(metric, observed[a].get(metric))
                    ob = oriented(metric, observed[b].get(metric))
                    if oa is None or ob is None:
                        continue
                    diffs = []
                    for rep in replicate_metrics:
                        ra = oriented(metric, rep[a].get(metric))
                        rb = oriented(metric, rep[b].get(metric))
                        if ra is None or rb is None:
                            continue
                        diffs.append(ra - rb)
                    if not diffs:
                        continue
                    lo = quantile(diffs, ALPHA / 2)
                    hi = quantile(diffs, 1 - ALPHA / 2)
                    observed_diff = oa - ob
                    if lo > 0:
                        verdict = f"{a}_BETTER"
                    elif hi < 0:
                        verdict = f"{b}_BETTER"
                    else:
                        verdict = "UNRESOLVED"
                    pairs[f"{a}__vs__{b}"] = {
                        "observed_oriented_difference": observed_diff,
                        "bootstrap_95_interval": [lo, hi],
                        "valid_replicates": len(diffs),
                        "p_a_better": sum(d > 0 for d in diffs) / len(diffs),
                        "p_b_better": sum(d < 0 for d in diffs) / len(diffs),
                        "verdict": verdict,
                    }

            metric_results[metric] = {
                "observed_ranking": [
                    {"condition": condition, "value": value}
                    for condition, value in observed_rank
                ],
                "top_probability": {
                    condition: (count / valid_top if valid_top else None)
                    for condition, count in top_counts.items()
                },
                "pairwise": pairs,
            }

        # Stable metric disagreement means at least two metrics support opposite
        # directions for the same condition pair. Keep this mechanical and report
        # the pair/metrics; do not synthesize them into a new score.
        stable_conflicts = []
        condition_names = sorted(conditions)
        for i, a in enumerate(condition_names):
            for b in condition_names[i + 1 :]:
                a_better = []
                b_better = []
                unresolved = []
                key = f"{a}__vs__{b}"
                for metric, data in metric_results.items():
                    row = data["pairwise"].get(key)
                    if row is None:
                        continue
                    if row["verdict"] == f"{a}_BETTER":
                        a_better.append(metric)
                    elif row["verdict"] == f"{b}_BETTER":
                        b_better.append(metric)
                    else:
                        unresolved.append(metric)
                if a_better and b_better:
                    stable_conflicts.append(
                        {
                            "pair": key,
                            f"{a}_better_metrics": a_better,
                            f"{b}_better_metrics": b_better,
                            "unresolved_metrics": unresolved,
                        }
                    )

        out["tasks"][task] = {
            "observed": observed,
            "eligible_counts": eligible,
            "metrics": metric_results,
            "stable_metric_conflicts": stable_conflicts,
        }

    return out


def print_summary(result: dict[str, Any]) -> None:
    print(
        f"rows={result['used_rows']}/{result['raw_rows']} "
        f"bootstrap={result['bootstrap_replicates']} seed={result['bootstrap_seed']}"
    )
    for task, data in result["tasks"].items():
        print(f"\n[{task}] stable_conflicts={len(data['stable_metric_conflicts'])}")
        for condition, counts in data["eligible_counts"].items():
            print(
                f"  {condition}: participants={counts['participants']} rows={counts['rows']} "
                f"beneficial_eligible={counts['beneficial_eligible']} "
                f"harmful_eligible={counts['harmful_eligible']}"
            )
        for conflict in data["stable_metric_conflicts"]:
            print("  CONFLICT " + json.dumps(conflict, sort_keys=True))
        print("  top probabilities:")
        for metric, metric_data in data["metrics"].items():
            probs = ", ".join(
                f"{c}={p:.3f}" for c, p in sorted(metric_data["top_probability"].items())
                if isinstance(p, (int, float))
            )
            print(f"    {metric}: {probs}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("/tmp/haiid_dataset.csv"))
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--replicates", type=int, default=DEFAULT_REPLICATES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    if args.download or not args.data.exists():
        probe.download(args.data)
    result = analyze(args.data, args.replicates, args.seed)
    print_summary(result)
    if args.json_out:
        args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
