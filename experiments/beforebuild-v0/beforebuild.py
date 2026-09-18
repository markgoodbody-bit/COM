#!/usr/bin/env python3
"""BeforeBuild v0: deterministic decision core for owner-trial evidence.

This module does not discover owners, browse the web, or decide novelty.
It consumes an explicit evidence contract and returns the smallest justified
pre-build disposition.

The point of v0 is falsification: can the same mechanical rules reproduce
historical USE/INTEROPERATE/STOP/BUILD decisions without an expected verdict
being present in the fixture?
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

VERDICTS = {"USE_OWNER", "INTEROPERATE", "SHRINK", "BUILD", "STOP"}
HARD_RESULTS = {"PASS", "FAIL", "NOT_TESTED"}


def load_cases(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != "beforebuild-calibration-v0.1":
        raise ValueError("unexpected calibration format")
    if not isinstance(data.get("cases"), list) or not data["cases"]:
        raise ValueError("cases must be a non-empty list")
    return data


def validate_case(case: dict[str, Any]) -> None:
    required = {
        "id", "proposal", "world_need", "hard_cases", "owners",
        "uncovered_requirement", "smallest_build",
    }
    if set(case) != required:
        raise ValueError(f"{case.get('id')}: case keys must be exactly {sorted(required)}")

    need = case["world_need"]
    if not isinstance(need.get("observed"), bool):
        raise ValueError(f"{case['id']}: world_need.observed must be bool")
    if not isinstance(need.get("description"), str) or not need["description"].strip():
        raise ValueError(f"{case['id']}: world_need.description required")
    if not isinstance(need.get("evidence"), list):
        raise ValueError(f"{case['id']}: world_need.evidence must be list")

    hard_cases = case["hard_cases"]
    if not hard_cases:
        raise ValueError(f"{case['id']}: at least one hard case required")
    ids = [row.get("id") for row in hard_cases]
    if any(not isinstance(x, str) or not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError(f"{case['id']}: hard-case ids must be unique non-empty strings")

    for owner in case["owners"]:
        if not isinstance(owner.get("exact_function_match"), bool):
            raise ValueError(f"{case['id']}: owner exact_function_match must be bool")
        trial = owner.get("trial") or {}
        if not isinstance(trial.get("executed"), bool):
            raise ValueError(f"{case['id']}: owner trial.executed must be bool")
        results = trial.get("hard_case_results")
        if not isinstance(results, dict):
            raise ValueError(f"{case['id']}: hard_case_results must be object")
        unknown = set(results) - set(ids)
        if unknown:
            raise ValueError(f"{case['id']}: owner results reference unknown hard cases {sorted(unknown)}")
        if any(value not in HARD_RESULTS for value in results.values()):
            raise ValueError(f"{case['id']}: invalid hard-case result")
        losses = trial.get("material_losses")
        if not isinstance(losses, list):
            raise ValueError(f"{case['id']}: material_losses must be list")
        for loss in losses:
            if not isinstance(loss.get("consequential_failure_observed"), bool):
                raise ValueError(f"{case['id']}: loss consequential flag must be bool")
        if not isinstance(trial.get("semantic_cheating_observed"), bool):
            raise ValueError(f"{case['id']}: semantic_cheating_observed must be bool")

    gap = case["uncovered_requirement"]
    if not isinstance(gap.get("observed"), bool) or not isinstance(gap.get("material"), bool):
        raise ValueError(f"{case['id']}: uncovered requirement flags must be bool")

    build = case["smallest_build"]
    if build is not None:
        if not isinstance(build.get("bounded"), bool):
            raise ValueError(f"{case['id']}: smallest_build.bounded must be bool")
        if not isinstance(build.get("kill_condition"), str) or not build["kill_condition"].strip():
            raise ValueError(f"{case['id']}: smallest_build.kill_condition required")


def owner_trial_coverage(case: dict[str, Any], owner: dict[str, Any]) -> dict[str, Any]:
    hard_ids = [row["id"] for row in case["hard_cases"]]
    trial = owner["trial"]
    results = trial["hard_case_results"]
    pass_ids = [hid for hid in hard_ids if results.get(hid) == "PASS"]
    fail_ids = [hid for hid in hard_ids if results.get(hid) == "FAIL"]
    not_tested_ids = [hid for hid in hard_ids if results.get(hid, "NOT_TESTED") == "NOT_TESTED"]
    losses = trial["material_losses"]
    consequential_losses = [
        loss["id"] for loss in losses if loss["consequential_failure_observed"]
    ]
    return {
        "owner_id": owner["id"],
        "executed": trial["executed"],
        "exact_function_match": owner["exact_function_match"],
        "pass": pass_ids,
        "fail": fail_ids,
        "not_tested": not_tested_ids,
        "all_hard_cases_pass": (
            trial["executed"]
            and len(pass_ids) == len(hard_ids)
            and not fail_ids
            and not not_tested_ids
            and not trial["semantic_cheating_observed"]
        ),
        "material_loss_ids": [loss["id"] for loss in losses],
        "consequential_loss_ids": consequential_losses,
        "semantic_cheating_observed": trial["semantic_cheating_observed"],
    }


def decide(case: dict[str, Any]) -> dict[str, Any]:
    validate_case(case)
    coverage = [owner_trial_coverage(case, owner) for owner in case["owners"]]

    if not case["world_need"]["observed"]:
        return {
            "case_id": case["id"],
            "verdict": "STOP",
            "reason": "No real current failure/need is observed; synthetic or conceptual structure cannot manufacture a product gap.",
            "owner_coverage": coverage,
        }

    full = [row for row in coverage if row["all_hard_cases_pass"]]
    if full:
        clean = [row for row in full if not row["material_loss_ids"]]
        if clean:
            return {
                "case_id": case["id"],
                "verdict": "USE_OWNER",
                "reason": f"Owner {clean[0]['owner_id']} passes every declared hard case with no material loss recorded.",
                "owner_coverage": coverage,
            }

        nonconsequential = [
            row for row in full
            if row["material_loss_ids"] and not row["consequential_loss_ids"]
        ]
        if nonconsequential:
            return {
                "case_id": case["id"],
                "verdict": "INTEROPERATE",
                "reason": (
                    f"Owner {nonconsequential[0]['owner_id']} passes every declared hard case. "
                    "Loss is visible, but no consequential failure from that loss is observed."
                ),
                "owner_coverage": coverage,
            }

        return {
            "case_id": case["id"],
            "verdict": "SHRINK",
            "reason": (
                "An owner passes the current hard cases but a consequential loss is also observed. "
                "The acceptance contract is incomplete; add the lost consequence as a hard case before choosing build."
            ),
            "owner_coverage": coverage,
        }

    exact_untested = [
        row for row in coverage
        if row["exact_function_match"] and not row["executed"]
    ]
    if exact_untested:
        return {
            "case_id": case["id"],
            "verdict": "SHRINK",
            "reason": (
                f"Candidate owner {exact_untested[0]['owner_id']} appears to match the function but has not been executed "
                "against the hard cases. Test the owner before rebuilding it."
            ),
            "owner_coverage": coverage,
        }

    gap = case["uncovered_requirement"]
    build = case["smallest_build"]
    if (
        gap["observed"]
        and gap["material"]
        and build is not None
        and build["bounded"]
        and build["kill_condition"].strip()
    ):
        return {
            "case_id": case["id"],
            "verdict": "BUILD",
            "reason": (
                "A real material requirement remains uncovered by the tested/identified owners, "
                "and a bounded build with an explicit kill condition exists."
            ),
            "owner_coverage": coverage,
            "smallest_build": build,
        }

    return {
        "case_id": case["id"],
        "verdict": "STOP",
        "reason": "No owner passed all hard cases, but no observed material uncovered requirement justifies a bounded build.",
        "owner_coverage": coverage,
    }


def evaluate_all(data: dict[str, Any]) -> dict[str, Any]:
    rows = [decide(case) for case in data["cases"]]
    return {
        "format": "beforebuild-report-v0.1",
        "claim_ceiling": "historical calibration only; not prospective validation or novelty evidence",
        "results": rows,
        "summary": {
            verdict: sum(row["verdict"] == verdict for row in rows)
            for verdict in sorted(VERDICTS)
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    report = evaluate_all(load_cases(args.cases))
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
