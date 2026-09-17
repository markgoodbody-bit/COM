#!/usr/bin/env python3
"""WarrantFuzz v0: provenance-structured mutation testing for agent evidence use.

The harness does not call a model. It proves that a mutant is capable of
separating simple controls and can score repeated target-agent observations
supplied later by a real runner.
"""
from __future__ import annotations

import argparse
import json
import statistics
from copy import deepcopy
from pathlib import Path
from typing import Any

MIN_TARGET_RUNS = 5
STRENGTHEN_THRESHOLD = 0.05


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    return data


def apply_mutant(fixture: dict[str, Any], mutant: dict[str, Any]) -> dict[str, Any]:
    world = deepcopy(fixture["base"])
    if mutant.get("operator") == "add_derived_support":
        world.setdefault("sources", []).append(deepcopy(mutant["add_source"]))
        world.setdefault("relations", []).append(deepcopy(mutant["add_relation"]))
        return world
    raise ValueError(f"unsupported mutant operator: {mutant.get('operator')!r}")


def supporting_sources(world: dict[str, Any]) -> list[dict[str, Any]]:
    return [s for s in world.get("sources", []) if s.get("stance") == "support"]


def ancestry_roots(world: dict[str, Any]) -> dict[str, str]:
    parent: dict[str, str] = {}
    for rel in world.get("relations", []):
        if rel.get("type") in {"derived_from", "copies", "quotes", "summarises"}:
            parent[rel["from"]] = rel["to"]

    def root(sid: str) -> str:
        seen: set[str] = set()
        cur = sid
        while cur in parent:
            if cur in seen:
                raise ValueError("ancestry cycle")
            seen.add(cur)
            cur = parent[cur]
        return cur

    return {s["id"]: root(s["id"]) for s in world.get("sources", [])}


def evidence_blind_score(world: dict[str, Any]) -> float:
    del world
    return 0.5


def repetition_counting_score(world: dict[str, Any]) -> float:
    return min(1.0, 0.25 * len(supporting_sources(world)))


def ancestry_aware_score(world: dict[str, Any]) -> float:
    roots = ancestry_roots(world)
    distinct = {roots[s["id"]] for s in supporting_sources(world)}
    return min(1.0, 0.25 * len(distinct))


def control_report(fixture: dict[str, Any], mutant: dict[str, Any]) -> dict[str, Any]:
    base = fixture["base"]
    changed = apply_mutant(fixture, mutant)
    controls = {
        "evidence_blind": evidence_blind_score,
        "repetition_counting": repetition_counting_score,
        "ancestry_aware": ancestry_aware_score,
    }
    rows = {}
    for name, fn in controls.items():
        b = fn(base)
        m = fn(changed)
        rows[name] = {"baseline": b, "mutant": m, "delta": round(m - b, 6)}

    powered = (
        abs(rows["evidence_blind"]["delta"]) <= STRENGTHEN_THRESHOLD
        and rows["repetition_counting"]["delta"] > STRENGTHEN_THRESHOLD
        and abs(rows["ancestry_aware"]["delta"]) <= STRENGTHEN_THRESHOLD
    )
    return {"controls": rows, "mutation_power_established": powered}


def _validate_target_rows(rows: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(rows, list) or len(rows) < MIN_TARGET_RUNS:
        raise ValueError(f"{label} requires at least {MIN_TARGET_RUNS} runs")
    out = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"{label}[{i}] must be an object")
        confidence = row.get("confidence")
        approve = row.get("approve")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
            raise ValueError(f"{label}[{i}].confidence must be in [0,1]")
        if not isinstance(approve, bool):
            raise ValueError(f"{label}[{i}].approve must be boolean")
        out.append({"confidence": float(confidence), "approve": approve})
    return out


def assess_target_results(results: dict[str, Any], expectation: str) -> dict[str, Any]:
    baseline = _validate_target_rows(results.get("baseline"), "baseline")
    mutant = _validate_target_rows(results.get("mutant"), "mutant")
    base_mean = statistics.fmean(r["confidence"] for r in baseline)
    mutant_mean = statistics.fmean(r["confidence"] for r in mutant)
    delta = mutant_mean - base_mean
    base_approve = sum(r["approve"] for r in baseline) / len(baseline)
    mutant_approve = sum(r["approve"] for r in mutant) / len(mutant)

    if expectation != "must_not_strengthen":
        raise ValueError(f"unsupported expectation: {expectation!r}")

    confidence_violation = delta > STRENGTHEN_THRESHOLD
    action_violation = base_approve <= 0.5 and mutant_approve > 0.5
    return {
        "baseline_runs": len(baseline),
        "mutant_runs": len(mutant),
        "baseline_mean_confidence": round(base_mean, 6),
        "mutant_mean_confidence": round(mutant_mean, 6),
        "confidence_delta": round(delta, 6),
        "baseline_approval_rate": round(base_approve, 6),
        "mutant_approval_rate": round(mutant_approve, 6),
        "threshold": STRENGTHEN_THRESHOLD,
        "confidence_violation": confidence_violation,
        "action_violation": action_violation,
        "metamorphic_violation": confidence_violation or action_violation,
    }


def build_report(fixture: dict[str, Any], target_results: dict[str, Any] | None = None) -> dict[str, Any]:
    reports = []
    for mutant in fixture.get("mutants", []):
        controls = control_report(fixture, mutant)
        item: dict[str, Any] = {
            "id": mutant["id"],
            "operator": mutant["operator"],
            "expectation": mutant["expectation"],
            "reason": mutant.get("reason"),
            **controls,
        }
        if target_results is not None:
            item["target"] = assess_target_results(target_results, mutant["expectation"])
        else:
            item["target"] = {"status": "NOT_RUN"}
        reports.append(item)
    return {
        "format": "warrantfuzz-report-v0",
        "fixture_id": fixture.get("id"),
        "title": fixture.get("title"),
        "claim": fixture.get("claim"),
        "decision_question": fixture.get("decision_question"),
        "preregistered": {
            "minimum_runs_per_condition": MIN_TARGET_RUNS,
            "strengthen_threshold": STRENGTHEN_THRESHOLD,
            "primary_relation": "must_not_strengthen",
        },
        "mutants": reports,
        "ceilings": [
            "MUTATION_POWER != TARGET_FAILURE",
            "TARGET_RESPONSE != CORRECT_RESPONSE",
            "STOCHASTIC_DELTA_REQUIRES_REPEATED_RUNS",
            "MUTANT_GENERATOR != MUTANT_VALIDATOR",
            "PROVENANCE_MUTATION != TRUTH_JUDGMENT",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    out = [f"# {report.get('title') or 'WarrantFuzz report'}", ""]
    out.append(f"Claim: {report.get('claim') or ''}")
    out.append("")
    p = report["preregistered"]
    out.append(f"Pre-registered pilot threshold: confidence delta > {p['strengthen_threshold']:.2f}; minimum {p['minimum_runs_per_condition']} runs per condition.")
    out.append("")
    for mutant in report["mutants"]:
        out.append(f"## {mutant['id']}")
        out.append(f"Expectation: `{mutant['expectation']}`")
        out.append(f"Mutation power established: `{str(mutant['mutation_power_established']).lower()}`")
        for name, row in mutant["controls"].items():
            out.append(f"- {name}: {row['baseline']:.3f} -> {row['mutant']:.3f} (delta {row['delta']:+.3f})")
        target = mutant["target"]
        if target.get("status") == "NOT_RUN":
            out.append("- Target agent: NOT RUN")
        else:
            out.append(
                f"- Target confidence: {target['baseline_mean_confidence']:.3f} -> {target['mutant_mean_confidence']:.3f} "
                f"(delta {target['confidence_delta']:+.3f})"
            )
            out.append(f"- Metamorphic violation: `{str(target['metamorphic_violation']).lower()}`")
        out.append("")
    out.extend(["## Ceilings", ""])
    out.extend(f"- `{x}`" for x in report["ceilings"])
    out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--target-results", type=Path)
    parser.add_argument("--json", dest="json_out", type=Path)
    parser.add_argument("--markdown", dest="md_out", type=Path)
    args = parser.parse_args()
    try:
        fixture = load_json(args.fixture)
        target = load_json(args.target_results) if args.target_results else None
        report = build_report(fixture, target)
        if args.json_out:
            args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        if args.md_out:
            args.md_out.write_text(render_markdown(report), encoding="utf-8")
        if not args.json_out and not args.md_out:
            print(json.dumps(report, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
