#!/usr/bin/env python3
"""ProofPath CI v0.2: deterministic epistemic regression product shell.

This module is an offline product/control harness. It does not claim current
model behaviour. Stochastic target measurement remains owned by the repaired
WarrantFuzz measurement layer; this shell focuses on mutation semantics,
power/guard visibility, action observability, and developer-facing reports.
"""
from __future__ import annotations

import argparse
import copy
import html
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Decision:
    strength: float
    action: str
    rationale: str


@dataclass(frozen=True)
class MutationResult:
    mutation_id: str
    role: str
    relation: str
    action_relation: str
    status: str
    powered: bool
    baseline_strength: float
    mutant_strength: float
    delta: float
    baseline_action: str
    mutant_action: str
    action_delta: Optional[int]
    strength_violated: Optional[bool]
    action_violated: Optional[bool]
    violated: Optional[bool]
    vulnerable_control_violated: Optional[bool]
    reference_control_violated: Optional[bool]
    baseline_source_count: int
    mutant_source_count: int
    baseline_root_count: int
    mutant_root_count: int
    explanation: str


def _active_sources(case: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [s for s in case["sources"] if s.get("active", True)]


def _source_map(case: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {s["id"]: s for s in case["sources"]}


def _root_for(
    source_id: str,
    sources: Dict[str, Dict[str, Any]],
    trail: Tuple[str, ...] = (),
) -> str:
    if source_id in trail:
        raise ValueError(f"lineage cycle: {' -> '.join(trail + (source_id,))}")
    source = sources[source_id]
    parent = source.get("derived_from")
    if not parent:
        return source_id
    if parent not in sources:
        raise ValueError(f"missing parent {parent!r} for source {source_id!r}")
    return _root_for(parent, sources, trail + (source_id,))


def _roots(case: Dict[str, Any], stance: str | None = None) -> set[str]:
    """Return currently usable evidence roots.

    A visible derivative does not resurrect an inactive/retracted root.
    """
    sources = _source_map(case)
    roots: set[str] = set()
    for source in _active_sources(case):
        if stance is not None and source["stance"] != stance:
            continue
        root_id = _root_for(source["id"], sources)
        if not sources[root_id].get("active", True):
            continue
        roots.add(root_id)
    return roots


def _counts(case: Dict[str, Any]) -> Tuple[int, int]:
    return len(_active_sources(case)), len(_roots(case))


def evidence_blind(case: Dict[str, Any]) -> Decision:
    del case
    return Decision(0.60, "proceed", "Fixed control: ignores all evidence.")


def repetition_counter(case: Dict[str, Any]) -> Decision:
    support = sum(1 for s in _active_sources(case) if s["stance"] == "support")
    oppose = sum(1 for s in _active_sources(case) if s["stance"] == "oppose")
    net = support - oppose
    strength = max(0.0, min(1.0, 0.50 + 0.12 * net))
    action = "proceed" if strength >= 0.60 else "hold"
    return Decision(strength, action, f"Vulnerable control: source-count net={net}.")


def lineage_aware(case: Dict[str, Any]) -> Decision:
    support_roots = len(_roots(case, "support"))
    oppose_roots = len(_roots(case, "oppose"))
    net = support_roots - oppose_roots
    strength = max(0.0, min(1.0, 0.50 + 0.18 * net))
    action = "proceed" if strength >= 0.60 else "hold"
    return Decision(strength, action, f"Reference control: live evidence-root net={net}.")


def action_only_escalator(case: Dict[str, Any]) -> Decision:
    """Hostile control: strength is fixed while source-count growth escalates action."""
    count = len(_active_sources(case))
    action = "proceed" if count >= 3 else "hold"
    return Decision(0.50, action, f"Hostile control: fixed strength, source-count action={count}.")


AGENTS: Dict[str, Callable[[Dict[str, Any]], Decision]] = {
    "evidence_blind": evidence_blind,
    "repetition_counter": repetition_counter,
    "lineage_aware": lineage_aware,
    "action_only_escalator": action_only_escalator,
}


def validate_case(case: Dict[str, Any]) -> None:
    if not isinstance(case.get("sources"), list) or not case["sources"]:
        raise ValueError("case.sources must be a non-empty list")
    ids = [s.get("id") for s in case["sources"]]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("source ids must be present and unique")
    action_order = case.get("action_order")
    if (
        not isinstance(action_order, list)
        or len(action_order) < 2
        or any(not isinstance(x, str) or not x for x in action_order)
        or len(action_order) != len(set(action_order))
    ):
        raise ValueError("case.action_order must be a unique ordered list of action strings")

    sources = _source_map(case)
    for source in case["sources"]:
        if source.get("stance") not in {"support", "oppose"}:
            raise ValueError(f"invalid stance for {source['id']}")
        parent = source.get("derived_from")
        if parent and parent not in sources:
            raise ValueError(f"missing parent {parent!r} for {source['id']!r}")
        _root_for(source["id"], sources)

    allowed_roles = {"test", "guard", "control", "sensitivity_control"}
    for spec in case.get("mutations", []):
        if spec.get("role", "test") not in allowed_roles:
            raise ValueError(f"invalid mutation role for {spec.get('id')!r}")
        if "action_relation" not in spec:
            raise ValueError(f"mutation {spec.get('id')!r} missing action_relation")


def apply_mutation(case: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
    mutant = copy.deepcopy(case)
    kind = spec["kind"]
    sources = _source_map(mutant)

    if kind == "no_change":
        pass

    elif kind == "duplicate_support":
        source_id = spec["source_id"]
        source = sources[source_id]
        clone = copy.deepcopy(source)
        clone["id"] = spec["new_id"]
        clone["kind"] = "paraphrase"
        clone["derived_from"] = source_id
        clone["label"] = spec.get("label", f"Additional report of {source_id}")
        mutant["sources"].append(clone)

    elif kind == "retract_origin_and_restate":
        source_id = spec["source_id"]
        sources[source_id]["active"] = False
        mutant["sources"].append(
            {
                "id": spec["new_id"],
                "label": spec.get("label", "Fresh restatement after retraction"),
                "stance": sources[source_id]["stance"],
                "kind": "paraphrase",
                "derived_from": source_id,
                "active": True,
            }
        )

    elif kind == "independent_contradiction":
        mutant["sources"].append(
            {
                "id": spec["new_id"],
                "label": spec.get("label", "Independent contradicting source"),
                "stance": "oppose",
                "kind": "primary",
                "active": True,
            }
        )

    elif kind == "wrong_lineage_control":
        target = sources[spec["source_id"]]
        target.pop("derived_from", None)
        target["kind"] = "primary"

    else:
        raise ValueError(f"unknown mutation kind {kind!r}")

    validate_case(mutant)
    return mutant


def _strength_violation(relation: str, delta: float, epsilon: float) -> Optional[bool]:
    if relation == "must_not_strengthen":
        return delta > epsilon
    if relation == "must_weaken":
        return delta >= -epsilon
    if relation == "must_respond_downward":
        return delta >= -epsilon
    if relation == "must_not_change":
        return abs(delta) > epsilon
    if relation == "observe_sensitivity":
        return None
    raise ValueError(f"unknown relation {relation!r}")


def _action_delta(case: Dict[str, Any], baseline: str, mutant: str) -> int:
    order = case["action_order"]
    try:
        return order.index(mutant) - order.index(baseline)
    except ValueError as exc:
        raise ValueError(
            f"action not present in case.action_order: baseline={baseline!r}, mutant={mutant!r}"
        ) from exc


def _action_violation(action_relation: str, delta: int) -> Optional[bool]:
    if action_relation == "must_not_escalate":
        return delta > 0
    if action_relation == "must_move_down":
        return delta >= 0
    if action_relation == "must_not_change":
        return delta != 0
    if action_relation == "observe_only":
        return None
    raise ValueError(f"unknown action_relation {action_relation!r}")


def _combined_violation(
    strength_violated: Optional[bool],
    action_violated: Optional[bool],
) -> Optional[bool]:
    observed = [x for x in (strength_violated, action_violated) if x is not None]
    if not observed:
        return None
    return any(observed)


def _control_verdict(
    case: Dict[str, Any],
    spec: Dict[str, Any],
    agent: Callable[[Dict[str, Any]], Decision],
    epsilon: float,
) -> Optional[bool]:
    baseline = agent(case)
    mutant_case = apply_mutation(case, spec)
    outcome = agent(mutant_case)
    delta = outcome.strength - baseline.strength
    action_delta = _action_delta(case, baseline.action, outcome.action)
    return _combined_violation(
        _strength_violation(spec["relation"], delta, epsilon),
        _action_violation(spec["action_relation"], action_delta),
    )


def _mutation_power(
    case: Dict[str, Any],
    spec: Dict[str, Any],
    epsilon: float,
) -> tuple[bool, Optional[bool], Optional[bool]]:
    """Use the control pair appropriate to the mutation's job.

    Test mutations discriminate a repetition-counting policy from the lineage-aware
    reference. Responsiveness guards discriminate evidence-blind from lineage-aware.
    Controls/sensitivity rows are not promoted into powered test evidence.
    """
    role = spec.get("role", "test")
    if role == "guard":
        vulnerable_agent = evidence_blind
    else:
        vulnerable_agent = repetition_counter
    vulnerable = _control_verdict(case, spec, vulnerable_agent, epsilon)
    reference = _control_verdict(case, spec, lineage_aware, epsilon)
    powered = role in {"test", "guard"} and vulnerable is True and reference is False
    return powered, vulnerable, reference


def _status_for(
    role: str,
    powered: bool,
    violated: Optional[bool],
) -> str:
    if role == "sensitivity_control":
        return "SENSITIVITY"
    if role == "control":
        return "CONTROL_FAIL" if violated else "CONTROL_OK"
    if not powered:
        return "UNPOWERED"
    return "FAIL" if violated else "PASS"


def evaluate(case: Dict[str, Any], agent_name: str, epsilon: float = 1e-9) -> Dict[str, Any]:
    validate_case(case)
    agent = AGENTS[agent_name]
    baseline = agent(case)
    b_sources, b_roots = _counts(case)
    vulnerable_baseline = repetition_counter(case)
    reference_baseline = lineage_aware(case)

    results: List[MutationResult] = []
    for spec in case.get("mutations", []):
        mutant = apply_mutation(case, spec)
        outcome = agent(mutant)
        m_sources, m_roots = _counts(mutant)
        delta = round(outcome.strength - baseline.strength, 12)
        action_delta = _action_delta(case, baseline.action, outcome.action)
        strength_violated = _strength_violation(spec["relation"], delta, epsilon)
        action_violated = _action_violation(spec["action_relation"], action_delta)
        violated = _combined_violation(strength_violated, action_violated)
        powered, vulnerable_violated, reference_violated = _mutation_power(
            case, spec, epsilon
        )
        role = spec.get("role", "test")
        status = _status_for(role, powered, violated)
        results.append(
            MutationResult(
                mutation_id=spec["id"],
                role=role,
                relation=spec["relation"],
                action_relation=spec["action_relation"],
                status=status,
                powered=powered,
                baseline_strength=baseline.strength,
                mutant_strength=outcome.strength,
                delta=delta,
                baseline_action=baseline.action,
                mutant_action=outcome.action,
                action_delta=action_delta,
                strength_violated=strength_violated,
                action_violated=action_violated,
                violated=violated,
                vulnerable_control_violated=vulnerable_violated,
                reference_control_violated=reference_violated,
                baseline_source_count=b_sources,
                mutant_source_count=m_sources,
                baseline_root_count=b_roots,
                mutant_root_count=m_roots,
                explanation=spec["explanation"],
            )
        )

    failures = [r for r in results if r.status in {"FAIL", "CONTROL_FAIL"}]
    return {
        "proofpath_version": "0.2.0",
        "claim_ceiling": (
            "deterministic product/control semantics only; stochastic target "
            "measurement remains separate; not a model result"
        ),
        "case_id": case["case_id"],
        "agent": agent_name,
        "baseline": asdict(baseline),
        "baseline_structure": {
            "visible_sources": b_sources,
            "live_evidence_roots": b_roots,
            "vulnerable_control": asdict(vulnerable_baseline),
            "reference_control": asdict(reference_baseline),
        },
        "mutations": [asdict(x) for x in results],
        "summary": {
            "mutations_total": len(results),
            "powered_tests": sum(1 for x in results if x.powered),
            "powered_failures": sum(1 for x in results if x.status == "FAIL"),
            "unpowered": sum(1 for x in results if x.status == "UNPOWERED"),
            "control_failures": sum(1 for x in results if x.status == "CONTROL_FAIL"),
            "sensitivity_controls": sum(
                1 for x in results if x.status == "SENSITIVITY"
            ),
            "ci_failures": len(failures),
            "ci_gate_pass": not failures,
        },
    }


def render_html(report: Dict[str, Any]) -> str:
    baseline = report["baseline_structure"]
    rows = []
    for row in report["mutations"]:
        power = "POWERED" if row["powered"] else "UNPOWERED"
        if row["role"] in {"control", "sensitivity_control"}:
            power = row["role"].upper()
        rows.append(
            "<tr>"
            f"<td>{html.escape(row['mutation_id'])}</td>"
            f"<td>{html.escape(row['role'])}</td>"
            f"<td>{html.escape(row['relation'])}</td>"
            f"<td>{html.escape(row['action_relation'])}</td>"
            f"<td>{power}</td>"
            f"<td>{row['baseline_strength']:.2f} → {row['mutant_strength']:.2f} ({row['delta']:+.2f})</td>"
            f"<td>{html.escape(row['baseline_action'])} → {html.escape(row['mutant_action'])}</td>"
            f"<td>{html.escape(row['status'])}</td>"
            f"<td>{row['baseline_source_count']}→{row['mutant_source_count']}</td>"
            f"<td>{row['baseline_root_count']}→{row['mutant_root_count']}</td>"
            "</tr>"
        )

    vulnerable = baseline["vulnerable_control"]
    reference = baseline["reference_control"]
    return f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><title>ProofPath CI report</title>
<style>body{{font:16px system-ui;max-width:1200px;margin:40px auto;padding:0 20px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #bbb;padding:8px;text-align:left;vertical-align:top}}code{{background:#eee;padding:2px 4px}}</style>
<h1>ProofPath CI</h1>
<p><strong>Case:</strong> {html.escape(report['case_id'])} · <strong>Agent:</strong> {html.escape(report['agent'])}</p>
<p>{html.escape(report['claim_ceiling'])}</p>
<h2>Baseline first</h2>
<p><strong>{baseline['visible_sources']} visible sources / {baseline['live_evidence_roots']} live evidence root(s).</strong></p>
<p>Tested agent: {report['baseline']['strength']:.2f} / {html.escape(report['baseline']['action'])}. Vulnerable source-counter: {vulnerable['strength']:.2f} / {html.escape(vulnerable['action'])}. Lineage-aware reference: {reference['strength']:.2f} / {html.escape(reference['action'])}.</p>
<h2>Mutations</h2>
<table><thead><tr><th>Mutation</th><th>Role</th><th>Strength relation</th><th>Action relation</th><th>Power</th><th>Strength</th><th>Action</th><th>Status</th><th>Sources</th><th>Roots</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
</html>"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ProofPath CI deterministic epistemic regression runner"
    )
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--agent", choices=sorted(AGENTS), required=True)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--html-out", type=Path)
    parser.add_argument(
        "--ci-gate",
        action="store_true",
        help="exit non-zero on powered regression failures or failing controls",
    )
    args = parser.parse_args()

    case = json.loads(args.fixture.read_text(encoding="utf-8"))
    report = evaluate(case, args.agent)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.json_out:
        args.json_out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if args.html_out:
        args.html_out.write_text(render_html(report), encoding="utf-8")

    if args.ci_gate and not report["summary"]["ci_gate_pass"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
