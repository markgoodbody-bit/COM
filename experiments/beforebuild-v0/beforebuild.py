#!/usr/bin/env python3
"""BeforeBuild v0.3: deterministic pre-build owner-trial decision core.

The core does not discover owners, browse the web, decide novelty, or verify
source truth. It consumes:
- typed world evidence;
- explicit hard cases;
- candidate owner relevance;
- machine/recorded trial results;
- separately reviewed semantic/functional losses;
- an optional bounded probe.

Review losses are separated from trial failures so a fresh execution can change
when the world or owner changes without erasing durable semantic review.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

VERDICTS = {"USE_OWNER", "INTEROPERATE", "SHRINK", "BUILD_PROBE", "STOP"}
HARD_RESULTS = {"PASS", "FAIL", "NOT_TESTED"}
RELEVANCE = {"exact", "near", "adjacent"}
WORLD_EVIDENCE_KINDS = {
    "reproduced_failure",
    "owner_source_contradiction",
    "current_user_need",
    "synthetic_only",
    "conceptual_only",
}
QUALIFYING_WORLD_EVIDENCE = {
    "reproduced_failure",
    "owner_source_contradiction",
    "current_user_need",
}
RELEVANT_CANDIDATES = {"exact", "near"}
RECEIPT_FORMAT = "beforebuild-owner-receipts-v0.1"


def load_cases(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != "beforebuild-calibration-v0.3":
        raise ValueError("unexpected calibration format")
    if not isinstance(data.get("cases"), list) or not data["cases"]:
        raise ValueError("cases must be a non-empty list")
    return data


def load_receipts(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != RECEIPT_FORMAT:
        raise ValueError("unexpected owner receipt format")
    if not isinstance(data.get("receipts"), list) or not data["receipts"]:
        raise ValueError("receipts must be a non-empty list")
    return data


def validate_case(case: dict[str, Any]) -> None:
    required = {"id", "proposal", "world_evidence", "hard_cases", "candidates", "smallest_probe"}
    if set(case) != required:
        raise ValueError(f"{case.get('id')}: case keys must be exactly {sorted(required)}")

    world = case["world_evidence"]
    if not isinstance(world, list) or not world:
        raise ValueError(f"{case['id']}: at least one world_evidence row required")
    evidence_ids = []
    for row in world:
        if row.get("kind") not in WORLD_EVIDENCE_KINDS:
            raise ValueError(f"{case['id']}: invalid world evidence kind")
        if not isinstance(row.get("evidence_ref"), str) or not row["evidence_ref"].strip():
            raise ValueError(f"{case['id']}: world evidence requires evidence_ref")
        evidence_ids.append(row.get("id"))
    if any(not isinstance(x, str) or not x for x in evidence_ids) or len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError(f"{case['id']}: world evidence ids must be unique non-empty strings")

    hard_cases = case["hard_cases"]
    if not hard_cases:
        raise ValueError(f"{case['id']}: at least one hard case required")
    ids = [row.get("id") for row in hard_cases]
    if any(not isinstance(x, str) or not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError(f"{case['id']}: hard-case ids must be unique non-empty strings")

    for candidate in case["candidates"]:
        if candidate.get("relevance") not in RELEVANCE:
            raise ValueError(f"{case['id']}: invalid candidate relevance")
        losses = candidate.get("review_losses")
        if not isinstance(losses, list):
            raise ValueError(f"{case['id']}: review_losses must be list")
        for loss in losses:
            if not isinstance(loss.get("consequential_failure_observed"), bool):
                raise ValueError(f"{case['id']}: review loss consequential flag must be bool")

        trial = candidate.get("trial") or {}
        if not isinstance(trial.get("executed"), bool):
            raise ValueError(f"{case['id']}: candidate trial.executed must be bool")
        results = trial.get("hard_case_results")
        if not isinstance(results, dict):
            raise ValueError(f"{case['id']}: hard_case_results must be object")
        unknown = set(results) - set(ids)
        if unknown:
            raise ValueError(f"{case['id']}: trial references unknown hard cases {sorted(unknown)}")
        if any(value not in HARD_RESULTS for value in results.values()):
            raise ValueError(f"{case['id']}: invalid hard-case result")
        if not isinstance(trial.get("semantic_cheating_observed"), bool):
            raise ValueError(f"{case['id']}: semantic_cheating_observed must be bool")
        if "receipt_source" in trial and (
            not isinstance(trial["receipt_source"], str) or not trial["receipt_source"].strip()
        ):
            raise ValueError(f"{case['id']}: receipt_source must be non-empty string")

    probe = case["smallest_probe"]
    if probe is not None:
        if not isinstance(probe.get("bounded"), bool):
            raise ValueError(f"{case['id']}: smallest_probe.bounded must be bool")
        if not isinstance(probe.get("kill_condition"), str) or not probe["kill_condition"].strip():
            raise ValueError(f"{case['id']}: smallest_probe.kill_condition required")


def apply_receipts(data: dict[str, Any], receipt_sets: list[dict[str, Any]]) -> dict[str, Any]:
    """Overlay owner-execution receipts without altering review judgments."""
    out = copy.deepcopy(data)
    cases = {case["id"]: case for case in out["cases"]}

    for receipt_set in receipt_sets:
        if receipt_set.get("format") != RECEIPT_FORMAT:
            raise ValueError("unexpected owner receipt format")
        for receipt in receipt_set.get("receipts", []):
            case_id = receipt.get("case_id")
            candidate_id = receipt.get("candidate_id")
            if case_id not in cases:
                raise ValueError(f"receipt references unknown case {case_id!r}")
            case = cases[case_id]
            candidates = {candidate["id"]: candidate for candidate in case["candidates"]}
            if candidate_id not in candidates:
                raise ValueError(f"receipt references unknown candidate {candidate_id!r} in {case_id}")

            hard_ids = {row["id"] for row in case["hard_cases"]}
            results = receipt.get("hard_case_results")
            if not isinstance(results, dict):
                raise ValueError("receipt hard_case_results must be object")
            if set(results) - hard_ids:
                raise ValueError("receipt references unknown hard case")
            if any(value not in HARD_RESULTS for value in results.values()):
                raise ValueError("receipt contains invalid hard-case result")
            if not isinstance(receipt.get("executed"), bool):
                raise ValueError("receipt executed must be bool")
            source = receipt.get("source")
            if not isinstance(source, str) or not source.strip():
                raise ValueError("receipt source required")

            trial = candidates[candidate_id]["trial"]
            trial["executed"] = receipt["executed"]
            trial["hard_case_results"] = results
            trial["receipt_source"] = source

    return out


def derive_world_need(case: dict[str, Any]) -> dict[str, Any]:
    qualifying = [row for row in case["world_evidence"] if row["kind"] in QUALIFYING_WORLD_EVIDENCE]
    return {
        "observed": bool(qualifying),
        "qualifying_evidence_ids": [row["id"] for row in qualifying],
        "all_evidence_kinds": [row["kind"] for row in case["world_evidence"]],
    }


def candidate_coverage(case: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    hard_ids = [row["id"] for row in case["hard_cases"]]
    trial = candidate["trial"]
    results = trial["hard_case_results"]

    passed = [hid for hid in hard_ids if results.get(hid) == "PASS"]
    failed = [hid for hid in hard_ids if results.get(hid) == "FAIL"]
    not_tested = [hid for hid in hard_ids if results.get(hid, "NOT_TESTED") == "NOT_TESTED"]
    losses = candidate["review_losses"]
    consequential = [loss["id"] for loss in losses if loss["consequential_failure_observed"]]

    return {
        "candidate_id": candidate["id"],
        "relevance": candidate["relevance"],
        "executed": trial["executed"],
        "receipt_source": trial.get("receipt_source"),
        "pass": passed,
        "fail": failed,
        "not_tested": not_tested,
        "all_hard_cases_pass": (
            trial["executed"]
            and len(passed) == len(hard_ids)
            and not failed
            and not not_tested
            and not trial["semantic_cheating_observed"]
        ),
        "review_loss_ids": [loss["id"] for loss in losses],
        "consequential_review_loss_ids": consequential,
        "semantic_cheating_observed": trial["semantic_cheating_observed"],
    }


def decide(case: dict[str, Any]) -> dict[str, Any]:
    validate_case(case)
    world = derive_world_need(case)
    coverage = [candidate_coverage(case, c) for c in case["candidates"]]

    if not world["observed"]:
        return {
            "case_id": case["id"],
            "verdict": "STOP",
            "reason": "No qualifying current-world need evidence is present. Synthetic/conceptual structure alone cannot earn custom work.",
            "world_need": world,
            "candidate_coverage": coverage,
        }

    relevant = [row for row in coverage if row["relevance"] in RELEVANT_CANDIDATES]

    full = [row for row in relevant if row["all_hard_cases_pass"]]
    if full:
        clean = [row for row in full if not row["review_loss_ids"]]
        if clean:
            return {
                "case_id": case["id"],
                "verdict": "USE_OWNER",
                "reason": f"Relevant candidate {clean[0]['candidate_id']} passes every declared hard case with no review loss recorded.",
                "world_need": world,
                "candidate_coverage": coverage,
            }

        nonconsequential = [
            row for row in full
            if row["review_loss_ids"] and not row["consequential_review_loss_ids"]
        ]
        if nonconsequential:
            return {
                "case_id": case["id"],
                "verdict": "INTEROPERATE",
                "reason": f"Relevant candidate {nonconsequential[0]['candidate_id']} passes every hard case. Review loss is visible, but no consequential use failure from that loss is observed.",
                "world_need": world,
                "candidate_coverage": coverage,
            }

        return {
            "case_id": case["id"],
            "verdict": "SHRINK",
            "reason": "A relevant candidate passes the current hard cases but a consequential review loss is also observed. The hard-case contract is incomplete; add the lost consequence before choosing custom work.",
            "world_need": world,
            "candidate_coverage": coverage,
        }

    untested_relevant = [row for row in relevant if not row["executed"]]
    if untested_relevant:
        return {
            "case_id": case["id"],
            "verdict": "SHRINK",
            "reason": f"Relevant candidate {untested_relevant[0]['candidate_id']} has not been executed against the hard cases. Test it before custom work.",
            "world_need": world,
            "candidate_coverage": coverage,
        }

    partial_relevant = [
        row for row in relevant
        if row["executed"] and row["not_tested"] and not row["fail"]
    ]
    if partial_relevant:
        return {
            "case_id": case["id"],
            "verdict": "SHRINK",
            "reason": f"Relevant candidate {partial_relevant[0]['candidate_id']} was executed but material hard cases remain NOT_TESTED. Improve the trial before custom work.",
            "world_need": world,
            "candidate_coverage": coverage,
        }

    failed_relevant = [row for row in relevant if row["executed"] and row["fail"]]
    probe = case["smallest_probe"]
    if failed_relevant and probe is not None and probe["bounded"] and probe["kill_condition"].strip():
        failed_ids = sorted({hid for row in failed_relevant for hid in row["fail"]})
        return {
            "case_id": case["id"],
            "verdict": "BUILD_PROBE",
            "reason": "Qualifying current-world evidence exists, relevant owner/candidate trials leave hard cases uncovered "
                      f"({', '.join(failed_ids)}), and a bounded falsifiable probe exists.",
            "world_need": world,
            "candidate_coverage": coverage,
            "smallest_probe": probe,
        }

    return {
        "case_id": case["id"],
        "verdict": "STOP",
        "reason": "A current need may exist, but the evidence contract has not earned custom work: no relevant executed candidate leaves declared hard cases uncovered with a bounded falsifiable probe.",
        "world_need": world,
        "candidate_coverage": coverage,
    }


def evaluate_all(data: dict[str, Any]) -> dict[str, Any]:
    rows = [decide(case) for case in data["cases"]]
    return {
        "format": "beforebuild-report-v0.3",
        "claim_ceiling": "historical calibration only; typed evidence is not source verification; not prospective validation or novelty evidence",
        "results": rows,
        "summary": {verdict: sum(row["verdict"] == verdict for row in rows) for verdict in sorted(VERDICTS)},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path)
    parser.add_argument("--receipt", action="append", type=Path, default=[])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    data = load_cases(args.cases)
    if args.receipt:
        data = apply_receipts(data, [load_receipts(path) for path in args.receipt])

    report = evaluate_all(data)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
