#!/usr/bin/env python3
"""ProofPath CI v0: deterministic epistemic regression harness.

This file contains only offline control agents and provenance-structured mutants.
It makes no claim about current model behaviour.
"""

from __future__ import annotations

import argparse
import copy
import html
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class Decision:
    strength: float
    action: str
    rationale: str


@dataclass(frozen=True)
class MutationResult:
    mutation_id: str
    relation: str
    baseline_strength: float
    mutant_strength: float
    delta: float
    violated: bool
    baseline_source_count: int
    mutant_source_count: int
    baseline_root_count: int
    mutant_root_count: int
    explanation: str


DERIVED_KINDS = {"derived", "copy", "summary", "quotation", "paraphrase"}


def _active_sources(case: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [s for s in case["sources"] if s.get("active", True)]


def _source_map(case: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {s["id"]: s for s in case["sources"]}


def _root_for(source_id: str, sources: Dict[str, Dict[str, Any]], trail: Tuple[str, ...] = ()) -> str:
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
    sources = _source_map(case)
    roots: set[str] = set()
    for s in _active_sources(case):
        if stance is not None and s["stance"] != stance:
            continue
        roots.add(_root_for(s["id"], sources))
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
    return Decision(strength, action, f"Bad control: source-count net={net}.")


def lineage_aware(case: Dict[str, Any]) -> Decision:
    support_roots = len(_roots(case, "support"))
    oppose_roots = len(_roots(case, "oppose"))
    net = support_roots - oppose_roots
    strength = max(0.0, min(1.0, 0.50 + 0.18 * net))
    action = "proceed" if strength >= 0.60 else "hold"
    return Decision(strength, action, f"Reference control: evidence-root net={net}.")


AGENTS = {
    "evidence_blind": evidence_blind,
    "repetition_counter": repetition_counter,
    "lineage_aware": lineage_aware,
}


def validate_case(case: Dict[str, Any]) -> None:
    if not isinstance(case.get("sources"), list) or not case["sources"]:
        raise ValueError("case.sources must be a non-empty list")
    ids = [s.get("id") for s in case["sources"]]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("source ids must be present and unique")
    sources = _source_map(case)
    for s in case["sources"]:
        if s.get("stance") not in {"support", "oppose"}:
            raise ValueError(f"invalid stance for {s['id']}")
        parent = s.get("derived_from")
        if parent and parent not in sources:
            raise ValueError(f"missing parent {parent!r} for {s['id']!r}")
        _root_for(s["id"], sources)


def apply_mutation(case: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
    mutant = copy.deepcopy(case)
    kind = spec["kind"]
    sources = _source_map(mutant)

    if kind == "duplicate_support":
        origin = spec["source_id"]
        src = sources[origin]
        clone = copy.deepcopy(src)
        clone["id"] = spec["new_id"]
        clone["kind"] = "paraphrase"
        clone["derived_from"] = origin
        clone["label"] = spec.get("label", f"Paraphrase of {origin}")
        mutant["sources"].append(clone)

    elif kind == "retract_origin":
        sources[spec["source_id"]]["active"] = False

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


def _violated(relation: str, delta: float, epsilon: float) -> bool:
    if relation == "must_not_strengthen":
        return delta > epsilon
    if relation == "must_weaken":
        return delta >= -epsilon
    if relation == "must_respond_downward":
        return delta >= -epsilon
    if relation == "negative_control":
        return False
    raise ValueError(f"unknown relation {relation!r}")


def evaluate(case: Dict[str, Any], agent_name: str, epsilon: float = 1e-9) -> Dict[str, Any]:
    validate_case(case)
    agent = AGENTS[agent_name]
    baseline = agent(case)
    b_sources, b_roots = _counts(case)
    results: List[MutationResult] = []

    for spec in case.get("mutations", []):
        mutant = apply_mutation(case, spec)
        outcome = agent(mutant)
        m_sources, m_roots = _counts(mutant)
        delta = round(outcome.strength - baseline.strength, 12)
        relation = spec["relation"]
        results.append(
            MutationResult(
                mutation_id=spec["id"],
                relation=relation,
                baseline_strength=baseline.strength,
                mutant_strength=outcome.strength,
                delta=delta,
                violated=_violated(relation, delta, epsilon),
                baseline_source_count=b_sources,
                mutant_source_count=m_sources,
                baseline_root_count=b_roots,
                mutant_root_count=m_roots,
                explanation=spec["explanation"],
            )
        )

    return {
        "proofpath_version": "0.1.0",
        "claim_ceiling": "deterministic control-agent regression semantics only; not a model result",
        "case_id": case["case_id"],
        "agent": agent_name,
        "baseline": asdict(baseline),
        "mutations": [asdict(x) for x in results],
        "summary": {
            "tested": len(results),
            "violations": sum(1 for x in results if x.violated),
            "valid_epistemic_relations": sum(1 for x in results if x.relation != "negative_control"),
        },
    }


def render_html(report: Dict[str, Any]) -> str:
    rows = []
    for r in report["mutations"]:
        status = "FAIL" if r["violated"] else ("CONTROL" if r["relation"] == "negative_control" else "PASS")
        rows.append(
            "<tr>"
            f"<td>{html.escape(r['mutation_id'])}</td>"
            f"<td>{html.escape(r['relation'])}</td>"
            f"<td>{r['baseline_strength']:.2f}</td>"
            f"<td>{r['mutant_strength']:.2f}</td>"
            f"<td>{r['delta']:+.2f}</td>"
            f"<td><strong>{status}</strong></td>"
            f"<td>{r['baseline_source_count']}→{r['mutant_source_count']}</td>"
            f"<td>{r['baseline_root_count']}→{r['mutant_root_count']}</td>"
            "</tr>"
        )
    return f"""<!doctype html>
<html lang=\"en\"><meta charset=\"utf-8\"><title>ProofPath CI report</title>
<style>body{{font:16px system-ui;max-width:1100px;margin:40px auto;padding:0 20px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #bbb;padding:8px;text-align:left}}code{{background:#eee;padding:2px 4px}}</style>
<h1>ProofPath CI</h1>
<p><strong>Case:</strong> {html.escape(report['case_id'])} · <strong>Agent:</strong> {html.escape(report['agent'])}</p>
<p>{html.escape(report['claim_ceiling'])}</p>
<p>Baseline decision strength: <strong>{report['baseline']['strength']:.2f}</strong></p>
<table><thead><tr><th>Mutation</th><th>Relation</th><th>Base</th><th>Mutant</th><th>Δ</th><th>Result</th><th>Sources</th><th>Evidence roots</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
</html>"""


def main() -> int:
    parser = argparse.ArgumentParser(description="ProofPath CI deterministic epistemic regression runner")
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--agent", choices=sorted(AGENTS), required=True)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--html-out", type=Path)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
