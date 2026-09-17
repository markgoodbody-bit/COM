#!/usr/bin/env python3
"""No Free QALY v0: tiny executable stress-test for decision-improvement metrics.

This is not a universal decision-quality score. It deliberately demonstrates
where plausible existing metric families disagree, become undefined, or depend
on an explicit value/risk contract.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def load_cases(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _expected_policy_value(case: dict[str, Any], policy: dict[str, Any], utility: dict[str, Any]) -> float:
    total = 0.0
    for state, p_state in case["states"].items():
        for action, p_action in policy[state].items():
            total += p_state * p_action * utility[state][action]
    return total


def _accuracy(case: dict[str, Any], policy: dict[str, Any]) -> float:
    correct = case.get("correct_action")
    if correct is None:
        raise ValueError("accuracy undefined: no objective correct_action contract")
    return sum(case["states"][s] * policy[s][a] for s, a in correct.items())


def objective_case_metrics(case: dict[str, Any]) -> dict[str, float]:
    b_acc = _accuracy(case, case["baseline"])
    i_acc = _accuracy(case, case["intervention"])
    b_u = _expected_policy_value(case, case["baseline"], case["utility"])
    i_u = _expected_policy_value(case, case["intervention"], case["utility"])
    return {
        "baseline_accuracy": b_acc,
        "intervention_accuracy": i_acc,
        "accuracy_gain": i_acc - b_acc,
        "baseline_expected_utility": b_u,
        "intervention_expected_utility": i_u,
        "expected_utility_gain": i_u - b_u,
    }


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


def preference_case_metrics(case: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"accuracy": "UNDEFINED_NO_OBJECTIVE_CORRECT_ACTION", "stakeholders": {}}
    for stakeholder, utility in case["stakeholder_utilities"].items():
        baseline = _expected_policy_value(case, case["baseline"], utility)
        interventions = {
            name: _expected_policy_value(case, policy, utility)
            for name, policy in case["interventions"].items()
        }
        gains = {name: value - baseline for name, value in interventions.items()}
        ranking = sorted(gains, key=lambda name: (-gains[name], name))
        out["stakeholders"][stakeholder] = {
            "baseline_expected_utility": baseline,
            "intervention_gains": gains,
            "ranking": ranking,
        }
    return out


def _rank(rows: dict[str, dict[str, float]], metric: str) -> list[str]:
    return sorted(rows, key=lambda k: (-rows[k][metric], k))


def build_report(cases: dict[str, Any]) -> dict[str, Any]:
    objective = {case["id"]: objective_case_metrics(case) for case in cases["objective_cases"]}
    monetary = {case["id"]: monetary_case_metrics(case) for case in cases["monetary_cases"]}
    preference = preference_case_metrics(cases["preference_case"])

    objective_rankings = {
        "accuracy_gain": _rank(objective, "accuracy_gain"),
        "expected_utility_gain": _rank(objective, "expected_utility_gain"),
    }
    monetary_rankings = {
        "expected_utility_increase": _rank(monetary, "expected_utility_increase"),
        "certainty_equivalent_gain": _rank(monetary, "certainty_equivalent_gain"),
    }

    stakeholder_rankings = {
        s: row["ranking"] for s, row in preference["stakeholders"].items()
    }

    return {
        "status": "SYNTHETIC_STRESS_TEST_NOT_UNIVERSAL_METRIC",
        "objective_cases": objective,
        "objective_rankings": objective_rankings,
        "objective_rank_reversal": objective_rankings["accuracy_gain"] != objective_rankings["expected_utility_gain"],
        "monetary_cases": monetary,
        "monetary_rankings": monetary_rankings,
        "monetary_rank_reversal": monetary_rankings["expected_utility_increase"] != monetary_rankings["certainty_equivalent_gain"],
        "preference_sensitive_case": preference,
        "stakeholder_rank_reversal": len({tuple(v) for v in stakeholder_rankings.values()}) > 1,
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
            "ONE_NUMBER != COMPARABILITY",
            "METRIC_RANKING != VALUE_NEUTRALITY",
            "SYNTHETIC_COUNTEREXAMPLE != EMPIRICAL_PREVALENCE",
            "PROCESS_QUALITY != OUTCOME_LUCK",
            "UNDEFINED_METRIC != ZERO_IMPROVEMENT",
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
