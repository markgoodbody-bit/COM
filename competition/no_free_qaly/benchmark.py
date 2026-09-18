#!/usr/bin/env python3
"""No Free QALY: bounded teaching appendix for decision-improvement comparability.

This is not a universal decision-quality score and not a benchmark contribution.
The executable example illustrates an existing decision-analysis result: even
under one declared CARA utility family, different value-of-information measures
need not preserve one ordering across decision problems.

Identifier order is never treated as scientific preference. Ties are preserved.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations
from pathlib import Path
from typing import Any

DEFAULT_TOLERANCE = 1e-12


def load_cases(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cara_utility(x: float, risk_tolerance: float) -> float:
    return -math.exp(-x / risk_tolerance)


def distribution_expected_utility(dist: list[list[float]], risk_tolerance: float) -> float:
    return sum(float(p) * cara_utility(float(x), risk_tolerance) for p, x in dist)


def certainty_equivalent(dist: list[list[float]], risk_tolerance: float) -> float:
    eu = distribution_expected_utility(dist, risk_tolerance)
    return -risk_tolerance * math.log(-eu)


def monetary_case_metrics(case: dict[str, Any]) -> dict[str, float]:
    r = float(case["risk_tolerance"])
    b_eu = distribution_expected_utility(case["baseline"], r)
    i_eu = distribution_expected_utility(case["intervention"], r)
    b_ce = certainty_equivalent(case["baseline"], r)
    i_ce = certainty_equivalent(case["intervention"], r)
    return {
        "expected_utility_increase": i_eu - b_eu,
        "certainty_equivalent_gain": i_ce - b_ce,
    }


def _cmp(a: float, b: float, tolerance: float = DEFAULT_TOLERANCE) -> int:
    if a > b + tolerance:
        return 1
    if b > a + tolerance:
        return -1
    return 0


def pairwise_metric_relations(
    rows: dict[str, dict[str, float]],
    metric: str,
    tolerance: float = DEFAULT_TOLERANCE,
) -> dict[str, int]:
    out: dict[str, int] = {}
    for left, right in combinations(sorted(rows), 2):
        out[f"{left}::{right}"] = _cmp(rows[left][metric], rows[right][metric], tolerance)
    return out


def compare_metric_orderings(
    rows: dict[str, dict[str, float]],
    metric_a: str,
    metric_b: str,
    tolerance: float = DEFAULT_TOLERANCE,
) -> dict[str, Any]:
    a = pairwise_metric_relations(rows, metric_a, tolerance)
    b = pairwise_metric_relations(rows, metric_b, tolerance)
    strict_reversals = [pair for pair in a if a[pair] * b[pair] < 0]
    resolution_differences = [
        pair for pair in a if (a[pair] == 0) != (b[pair] == 0)
    ]
    return {
        "metric_a": metric_a,
        "metric_b": metric_b,
        "tolerance": tolerance,
        "metric_a_pairwise": a,
        "metric_b_pairwise": b,
        "strict_reversal_pairs": strict_reversals,
        "tie_vs_order_pairs": resolution_differences,
        "strict_rank_reversal": bool(strict_reversals),
        "same_pairwise_order": a == b,
    }


def display_ranking(
    rows: dict[str, dict[str, float]],
    metric: str,
    tolerance: float = DEFAULT_TOLERANCE,
) -> list[list[str]]:
    """Return rank groups. IDs inside a tie group are display order only."""
    ordered = sorted(rows, key=lambda k: (-rows[k][metric], k))
    groups: list[list[str]] = []
    for item in ordered:
        if not groups:
            groups.append([item])
            continue
        representative = groups[-1][0]
        if _cmp(rows[item][metric], rows[representative][metric], tolerance) == 0:
            groups[-1].append(item)
        else:
            groups.append([item])
    return groups


def build_report(cases: dict[str, Any]) -> dict[str, Any]:
    monetary = {case["id"]: monetary_case_metrics(case) for case in cases["monetary_cases"]}
    comparison = compare_metric_orderings(
        monetary,
        "expected_utility_increase",
        "certainty_equivalent_gain",
    )

    return {
        "status": "TEACHING_APPENDIX_OWNER_THEORY_NOT_BENCHMARK",
        "monetary_cases": monetary,
        "monetary_rank_groups": {
            "expected_utility_increase": display_ranking(monetary, "expected_utility_increase"),
            "certainty_equivalent_gain": display_ranking(monetary, "certainty_equivalent_gain"),
        },
        "monetary_order_comparison": comparison,
        "monetary_rank_reversal": comparison["strict_rank_reversal"],
        "minimum_measurement_contract": [
            "decision_owner_or_affected_scope",
            "alternatives",
            "counterfactual_baseline",
            "outcome_or_value_function_and_whose_values",
            "uncertainty_or_probability_model",
            "time_horizon",
            "utility_and_risk_assumptions",
            "process_metric_vs_outcome_metric",
            "distribution_or_aggregation_rule_across_people_or_cases",
            "correction_or_irreversibility_handling_when_material",
        ],
        "ceilings": [
            "OWNER_THEORY != OUR_NOVELTY",
            "TEACHING_APPENDIX != BENCHMARK_CONTRIBUTION",
            "TIE != STRICT_PREFERENCE",
            "IDENTIFIER_ORDER != SCIENTIFIC_ORDER",
            "REPORTING_CONTRACT != UNIVERSAL_SCORE",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = build_report(load_cases(args.cases))
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
