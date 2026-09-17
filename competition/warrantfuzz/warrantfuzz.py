#!/usr/bin/env python3
"""WarrantFuzz v0.2: provenance-structured mutation testing for agent evidence use.

The harness does not call a model. It validates the base/mutated evidence worlds
through the evidence-lineage oracle, proves that a mutant separates deterministic
controls, and evaluates repeated target observations with an explicit unchanged
baseline replicate so ordinary stochastic variation is visible.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import statistics
from copy import deepcopy
from pathlib import Path
from typing import Any

MIN_TARGET_RUNS = 15
STRENGTHEN_THRESHOLD = 0.05
ALPHA = 0.05
DERIVATION_TYPES = {"derived_from", "copies", "quotes", "summarises"}

ROOT = Path(__file__).resolve().parent
ORACLE_PATH = ROOT.parent / "evidence_lineage_agent" / "evidence_lineage.py"
OSPEC = importlib.util.spec_from_file_location("evidence_lineage", ORACLE_PATH)
oracle = importlib.util.module_from_spec(OSPEC)
assert OSPEC.loader is not None
OSPEC.loader.exec_module(oracle)


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
    return [s for s in world.get("sources", []) if isinstance(s, dict) and s.get("stance") == "support"]


def as_oracle_bundle(world: dict[str, Any]) -> dict[str, Any]:
    """Map a WarrantFuzz evidence world into the conservative lineage oracle."""
    source_rows = []
    for source in world.get("sources", []):
        source_rows.append(
            {
                k: v
                for k, v in source.items()
                if k in {"id", "label", "locator", "lineage_state"}
            }
        )
    return {
        "sources": source_rows,
        "claims": [
            {
                "id": "decision-claim",
                "text": "",
                "evidence_state": "unresolved",
                "source_ids": [s["id"] for s in supporting_sources(world) if isinstance(s.get("id"), str)],
            }
        ],
        "relations": deepcopy(world.get("relations", [])),
    }


def validate_world(world: dict[str, Any]) -> tuple[list[str], dict[str, Any] | None]:
    bundle = as_oracle_bundle(world)
    errors = list(oracle.validate(bundle))
    report = None
    if not errors:
        report = oracle.build_report(bundle)
        for cycle in report.get("ancestry_cycles", []):
            errors.append("ancestry cycle: " + " -> ".join(cycle))
    return errors, report


def validate_mutant_shape(fixture: dict[str, Any], mutant: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if mutant.get("operator") != "add_derived_support":
        return [f"unsupported mutant operator: {mutant.get('operator')!r}"]

    base_sources = {
        s.get("id"): s
        for s in fixture.get("base", {}).get("sources", [])
        if isinstance(s, dict) and isinstance(s.get("id"), str)
    }
    source = mutant.get("add_source")
    relation = mutant.get("add_relation")
    if not isinstance(source, dict) or not isinstance(relation, dict):
        return ["add_derived_support requires add_source and add_relation objects"]

    sid = source.get("id")
    parent = relation.get("to")
    if not isinstance(sid, str) or not sid:
        errors.append("mutant add_source.id must be a non-empty string")
    elif sid in base_sources:
        errors.append("mutant must add a new source id")
    if source.get("lineage_state") != "derived":
        errors.append("add_derived_support source must declare lineage_state=derived")
    if relation.get("type") not in DERIVATION_TYPES:
        errors.append("add_derived_support requires an ancestry relation")
    if relation.get("from") != sid:
        errors.append("mutant relation.from must equal the added source id")
    if parent not in base_sources:
        errors.append("mutant relation.to must name an existing base source")
    elif source.get("stance") != base_sources[parent].get("stance"):
        errors.append("add_derived_support must preserve the parent source stance")
    return errors


def repetition_counting_score(world: dict[str, Any]) -> float:
    """Deliberately vulnerable control: every supporting URL counts."""
    return float(len(supporting_sources(world)))


def ancestry_aware_score(world: dict[str, Any], report: dict[str, Any]) -> float:
    """Count connected components linked by supplied shared ancestry."""
    support_ids = [s["id"] for s in supporting_sources(world)]
    parent = {sid: sid for sid in support_ids}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    claims = report.get("claims", [])
    pairwise = claims[0].get("source_pair_lineage", []) if claims else []
    for pair in pairwise:
        if pair.get("state") == "shared":
            a, b = pair.get("source_a"), pair.get("source_b")
            if a in parent and b in parent:
                union(a, b)
    return float(len({find(sid) for sid in support_ids}))


def control_report(fixture: dict[str, Any], mutant: dict[str, Any]) -> dict[str, Any]:
    base = fixture["base"]
    changed = apply_mutant(fixture, mutant)

    errors = validate_mutant_shape(fixture, mutant)
    base_errors, base_report = validate_world(base)
    changed_errors, changed_report = validate_world(changed)
    errors.extend(f"base: {e}" for e in base_errors)
    errors.extend(f"mutant: {e}" for e in changed_errors)

    if errors or base_report is None or changed_report is None:
        return {
            "valid_mutant": False,
            "validation_errors": errors,
            "controls": {},
            "mutation_power_established": False,
        }

    controls = {
        "evidence_blind": {"baseline": 0.0, "mutant": 0.0, "delta": 0.0},
        "repetition_counting": {
            "baseline": repetition_counting_score(base),
            "mutant": repetition_counting_score(changed),
        },
        "ancestry_aware": {
            "baseline": ancestry_aware_score(base, base_report),
            "mutant": ancestry_aware_score(changed, changed_report),
        },
    }
    for row in controls.values():
        if "delta" not in row:
            row["delta"] = round(row["mutant"] - row["baseline"], 6)

    powered = (
        abs(controls["evidence_blind"]["delta"]) <= 1e-12
        and controls["repetition_counting"]["delta"] > 0
        and abs(controls["ancestry_aware"]["delta"]) <= 1e-12
    )
    return {
        "valid_mutant": True,
        "validation_errors": [],
        "controls": controls,
        "mutation_power_established": powered,
    }


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


def _mean(rows: list[dict[str, Any]]) -> float:
    return statistics.fmean(r["confidence"] for r in rows)


def _sample_variance(values: list[float]) -> float:
    return statistics.variance(values) if len(values) > 1 else 0.0


def _welch_normal_p(a: list[float], b: list[float], *, alternative: str) -> float:
    """Transparent pilot gate: Welch-style z approximation, not a universal test."""
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    se2 = _sample_variance(a) / len(a) + _sample_variance(b) / len(b)
    if se2 <= 0:
        if ma == mb:
            return 1.0
        if alternative == "greater":
            return 0.0 if mb > ma else 1.0
        return 0.0
    z = (mb - ma) / math.sqrt(se2)
    if alternative == "greater":
        return 0.5 * math.erfc(z / math.sqrt(2.0))
    if alternative == "two-sided":
        return math.erfc(abs(z) / math.sqrt(2.0))
    raise ValueError(f"unsupported alternative: {alternative}")


def _hypergeom_prob(x: int, n1: int, n2: int, total_success: int) -> float:
    if x < 0 or x > n1 or total_success - x < 0 or total_success - x > n2:
        return 0.0
    return math.comb(n1, x) * math.comb(n2, total_success - x) / math.comb(n1 + n2, total_success)


def _fisher_one_sided_greater(a_success: int, n1: int, b_success: int, n2: int) -> float:
    """P(B success rate >= observed B) conditional on total successes."""
    total = a_success + b_success
    lo = max(0, total - n2)
    hi = min(n1, total)
    observed_b = b_success
    p = 0.0
    for a_x in range(lo, hi + 1):
        b_x = total - a_x
        if b_x >= observed_b:
            p += _hypergeom_prob(a_x, n1, n2, total)
    return min(1.0, p)


def _fisher_two_sided(a_success: int, n1: int, b_success: int, n2: int) -> float:
    total = a_success + b_success
    lo = max(0, total - n2)
    hi = min(n1, total)
    observed_p = _hypergeom_prob(a_success, n1, n2, total)
    p = 0.0
    for a_x in range(lo, hi + 1):
        px = _hypergeom_prob(a_x, n1, n2, total)
        if px <= observed_p + 1e-15:
            p += px
    return min(1.0, p)


def assess_target_results(results: dict[str, Any], expectation: str) -> dict[str, Any]:
    if expectation != "must_not_strengthen":
        raise ValueError(f"unsupported expectation: {expectation!r}")

    baseline = _validate_target_rows(results.get("baseline"), "baseline")
    replicate = _validate_target_rows(results.get("baseline_replicate"), "baseline_replicate")
    mutant = _validate_target_rows(results.get("mutant"), "mutant")

    base_vals = [r["confidence"] for r in baseline]
    repl_vals = [r["confidence"] for r in replicate]
    mutant_vals = [r["confidence"] for r in mutant]

    base_mean = _mean(baseline)
    repl_mean = _mean(replicate)
    mutant_mean = _mean(mutant)
    replicate_delta = repl_mean - base_mean
    mutant_delta = mutant_mean - base_mean
    replicate_p = _welch_normal_p(base_vals, repl_vals, alternative="two-sided")
    mutant_p = _welch_normal_p(base_vals, mutant_vals, alternative="greater")
    jitter_estimate = statistics.pstdev(base_vals + repl_vals)

    b_approve = sum(r["approve"] for r in baseline)
    r_approve = sum(r["approve"] for r in replicate)
    m_approve = sum(r["approve"] for r in mutant)
    baseline_action_p = _fisher_two_sided(b_approve, len(baseline), r_approve, len(replicate))
    mutant_action_p = _fisher_one_sided_greater(b_approve, len(baseline), m_approve, len(mutant))

    confidence_unstable = abs(replicate_delta) > STRENGTHEN_THRESHOLD and replicate_p < ALPHA
    action_unstable = baseline_action_p < ALPHA
    baseline_unstable = confidence_unstable or action_unstable

    confidence_violation = not baseline_unstable and mutant_delta > STRENGTHEN_THRESHOLD and mutant_p < ALPHA
    base_approval_rate = b_approve / len(baseline)
    repl_approval_rate = r_approve / len(replicate)
    mutant_approval_rate = m_approve / len(mutant)
    action_violation = not baseline_unstable and mutant_approval_rate > base_approval_rate and mutant_action_p < ALPHA

    metamorphic_violation = confidence_violation or action_violation
    if baseline_unstable:
        status = "INCONCLUSIVE_BASELINE_VARIANCE"
    elif metamorphic_violation:
        status = "VIOLATION_OBSERVED"
    else:
        status = "NO_VIOLATION_OBSERVED"

    return {
        "status": status,
        "baseline_runs": len(baseline),
        "baseline_replicate_runs": len(replicate),
        "mutant_runs": len(mutant),
        "baseline_mean_confidence": round(base_mean, 6),
        "baseline_replicate_mean_confidence": round(repl_mean, 6),
        "mutant_mean_confidence": round(mutant_mean, 6),
        "replicate_delta": round(replicate_delta, 6),
        "confidence_delta": round(mutant_delta, 6),
        "jitter_estimate": round(jitter_estimate, 6),
        "baseline_replicate_p": round(replicate_p, 6),
        "mutant_confidence_p": round(mutant_p, 6),
        "baseline_approval_rate": round(base_approval_rate, 6),
        "baseline_replicate_approval_rate": round(repl_approval_rate, 6),
        "mutant_approval_rate": round(mutant_approval_rate, 6),
        "baseline_action_p": round(baseline_action_p, 6),
        "mutant_action_p": round(mutant_action_p, 6),
        "threshold": STRENGTHEN_THRESHOLD,
        "alpha": ALPHA,
        "confidence_test": "welch_normal_approx_pilot",
        "action_test": "fisher_exact",
        "baseline_unstable": baseline_unstable,
        "confidence_violation": confidence_violation,
        "action_violation": action_violation,
        "metamorphic_violation": metamorphic_violation,
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
            if not controls["mutation_power_established"]:
                item["target"] = {"status": "NOT_SCORED_MUTATION_POWER_NOT_ESTABLISHED"}
            else:
                item["target"] = assess_target_results(target_results, mutant["expectation"])
        else:
            item["target"] = {"status": "NOT_RUN"}
        reports.append(item)
    return {
        "format": "warrantfuzz-report-v0.2",
        "fixture_id": fixture.get("id"),
        "title": fixture.get("title"),
        "claim": fixture.get("claim"),
        "decision_question": fixture.get("decision_question"),
        "preregistered": {
            "minimum_runs_per_condition": MIN_TARGET_RUNS,
            "strengthen_threshold": STRENGTHEN_THRESHOLD,
            "alpha": ALPHA,
            "baseline_replicate_required": True,
            "primary_relation": "must_not_strengthen",
            "confidence_test": "welch_normal_approx_pilot",
            "action_test": "fisher_exact",
        },
        "mutants": reports,
        "ceilings": [
            "MUTATION_POWER != TARGET_FAILURE",
            "TARGET_RESPONSE != CORRECT_RESPONSE",
            "BASELINE_VARIANCE_CAN_MAKE_RESULT_INCONCLUSIVE",
            "PILOT_STATISTICAL_GATE != FINAL_STUDY_METHOD",
            "MUTANT_GENERATOR != MUTANT_VALIDATOR",
            "PROVENANCE_MUTATION != TRUTH_JUDGMENT",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    out = [f"# {report.get('title') or 'WarrantFuzz report'}", ""]
    out.append(f"Claim: {report.get('claim') or ''}")
    out.append("")
    p = report["preregistered"]
    out.append(
        "Pilot gate: "
        f"minimum {p['minimum_runs_per_condition']} runs per baseline/replicate/mutant condition; "
        f"effect > {p['strengthen_threshold']:.2f} and p < {p['alpha']:.2f}; "
        "unchanged baseline replicate required."
    )
    out.append("")
    for mutant in report["mutants"]:
        out.append(f"## {mutant['id']}")
        out.append(f"Expectation: `{mutant['expectation']}`")
        out.append(f"Valid mutant: `{str(mutant['valid_mutant']).lower()}`")
        out.append(f"Mutation power established: `{str(mutant['mutation_power_established']).lower()}`")
        for err in mutant.get("validation_errors", []):
            out.append(f"- Validation error: {err}")
        for name, row in mutant.get("controls", {}).items():
            out.append(f"- {name}: {row['baseline']:.3f} -> {row['mutant']:.3f} (delta {row['delta']:+.3f})")
        target = mutant["target"]
        if target.get("status") == "NOT_RUN":
            out.append("- Target agent: NOT RUN")
        elif target.get("status") == "NOT_SCORED_MUTATION_POWER_NOT_ESTABLISHED":
            out.append("- Target agent: NOT SCORED — mutation power not established")
        else:
            out.append(
                f"- Target confidence: {target['baseline_mean_confidence']:.3f} -> "
                f"{target['mutant_mean_confidence']:.3f} (delta {target['confidence_delta']:+.3f})"
            )
            out.append(
                f"- Baseline replicate delta: {target['replicate_delta']:+.3f}; "
                f"jitter estimate {target['jitter_estimate']:.3f}"
            )
            out.append(f"- Target status: `{target['status']}`")
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
