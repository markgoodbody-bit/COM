#!/usr/bin/env python3
"""Deterministic evidence-lineage validator and renderer.

This is intentionally not an extractor, independence prover, or truth scorer. It
validates an explicit claim/source graph and makes supplied ancestry inspectable
without converting missing lineage evidence into independence.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ANCESTRY_RELATIONS = {"derived_from", "quotes", "summarises", "copies"}
EVIDENCE_STATES = {"observed", "source_stated", "inferred", "unresolved"}
LINEAGE_STATES = {"primary", "derived", "unknown"}
RELATION_TYPES = ANCESTRY_RELATIONS | {"independent_of", "disputes", "corrects"}


def load_bundle(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    return data


def _relation_key(rel: dict[str, Any]) -> tuple[Any, ...]:
    return (rel.get("type"), rel.get("from"), rel.get("to"), rel.get("claim_id"))


def validate(bundle: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sources = bundle.get("sources", [])
    claims = bundle.get("claims", [])
    relations = bundle.get("relations", [])

    if not isinstance(sources, list) or not isinstance(claims, list) or not isinstance(relations, list):
        return ["sources, claims and relations must be arrays"]

    source_ids: set[str] = set()
    source_states: dict[str, str] = {}
    for i, src in enumerate(sources):
        if not isinstance(src, dict):
            errors.append(f"sources[{i}] must be an object")
            continue
        sid = src.get("id")
        if not isinstance(sid, str) or not sid:
            errors.append(f"sources[{i}].id must be a non-empty string")
            continue
        if sid in source_ids:
            errors.append(f"duplicate source id: {sid}")
            continue
        source_ids.add(sid)
        lineage_state = src.get("lineage_state", "unknown")
        if lineage_state not in LINEAGE_STATES:
            errors.append(f"source {sid}: invalid lineage_state {lineage_state!r}")
        else:
            source_states[sid] = lineage_state

    claim_ids: set[str] = set()
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{i}] must be an object")
            continue
        cid = claim.get("id")
        state = claim.get("evidence_state")
        if not isinstance(cid, str) or not cid:
            errors.append(f"claims[{i}].id must be a non-empty string")
            cid = f"#{i}"
        elif cid in claim_ids:
            errors.append(f"duplicate claim id: {cid}")
        else:
            claim_ids.add(cid)
        if state not in EVIDENCE_STATES:
            errors.append(f"claim {cid}: invalid evidence_state {state!r}")
        source_refs = claim.get("source_ids", [])
        if not isinstance(source_refs, list):
            errors.append(f"claim {cid}: source_ids must be an array")
            source_refs = []
        for sid in source_refs:
            if sid not in source_ids:
                errors.append(f"claim {cid}: unknown source_id {sid!r}")
        if state in {"observed", "source_stated"} and not source_refs:
            errors.append(f"claim {cid}: {state} requires at least one source")

    seen_relations: set[tuple[Any, ...]] = set()
    ancestry_pairs: set[tuple[str, str, Any]] = set()
    independent_pairs: set[tuple[str, str, Any]] = set()
    for i, rel in enumerate(relations):
        if not isinstance(rel, dict):
            errors.append(f"relations[{i}] must be an object")
            continue
        rtype = rel.get("type")
        src = rel.get("from")
        dst = rel.get("to")
        claim_id = rel.get("claim_id")
        key = _relation_key(rel)
        if key in seen_relations:
            errors.append(f"relations[{i}]: duplicate relation {key!r}")
        seen_relations.add(key)
        if rtype not in RELATION_TYPES:
            errors.append(f"relations[{i}]: invalid type {rtype!r}")
        if src not in source_ids:
            errors.append(f"relations[{i}]: unknown from source {src!r}")
        if dst not in source_ids:
            errors.append(f"relations[{i}]: unknown to source {dst!r}")
        if src == dst:
            errors.append(f"relations[{i}]: self relation is not allowed")
        if claim_id is not None and claim_id not in claim_ids:
            errors.append(f"relations[{i}]: unknown claim_id {claim_id!r}")
        if isinstance(src, str) and isinstance(dst, str):
            pair = tuple(sorted((src, dst))) + (claim_id,)
            if rtype in ANCESTRY_RELATIONS:
                ancestry_pairs.add(pair)
            if rtype == "independent_of":
                independent_pairs.add(pair)

    for pair in ancestry_pairs & independent_pairs:
        errors.append(f"contradictory ancestry/independence relations for {pair!r}")

    return errors


def ancestry_map(bundle: dict[str, Any], claim_id: str | None = None) -> tuple[dict[str, set[str]], list[list[str]]]:
    parents: dict[str, set[str]] = defaultdict(set)
    source_ids = [s["id"] for s in bundle.get("sources", []) if isinstance(s, dict) and "id" in s]
    for rel in bundle.get("relations", []):
        if rel.get("type") not in ANCESTRY_RELATIONS:
            continue
        scope = rel.get("claim_id")
        if scope is not None and scope != claim_id:
            continue
        parents[rel["from"]].add(rel["to"])

    memo: dict[str, set[str]] = {}
    cycles: list[list[str]] = []

    def walk(node: str, stack: list[str]) -> set[str]:
        if node in memo:
            return memo[node]
        if node in stack:
            start = stack.index(node)
            cycles.append(stack[start:] + [node])
            return set()
        ancestors: set[str] = set()
        for parent in parents.get(node, set()):
            ancestors.add(parent)
            ancestors.update(walk(parent, stack + [node]))
        memo[node] = ancestors
        return ancestors

    for sid in source_ids:
        walk(sid, [])
    return memo, cycles


def _declared_independent(bundle: dict[str, Any], a: str, b: str, claim_id: str) -> bool:
    for rel in bundle.get("relations", []):
        if rel.get("type") != "independent_of":
            continue
        if rel.get("claim_id") not in {None, claim_id}:
            continue
        if {rel.get("from"), rel.get("to")} == {a, b}:
            return True
    return False


def _pair_state(bundle: dict[str, Any], claim_id: str, a: str, b: str, ancestry: dict[str, set[str]], source_by_id: dict[str, Any]) -> dict[str, Any]:
    roots_a = {a} | ancestry.get(a, set())
    roots_b = {b} | ancestry.get(b, set())
    shared = sorted(roots_a & roots_b)
    if shared:
        return {"source_a": a, "source_b": b, "state": "shared", "shared_ancestry": shared}

    declared = _declared_independent(bundle, a, b, claim_id)
    a_state = source_by_id[a].get("lineage_state", "unknown")
    b_state = source_by_id[b].get("lineage_state", "unknown")
    if declared:
        state = "declared_independent"
    elif a_state == "primary" and b_state == "primary":
        state = "none_on_supplied_graph"
    else:
        state = "unknown"
    return {"source_a": a, "source_b": b, "state": state, "shared_ancestry": []}


def build_report(bundle: dict[str, Any]) -> dict[str, Any]:
    global_ancestry, global_cycles = ancestry_map(bundle, None)
    source_by_id = {s["id"]: s for s in bundle.get("sources", [])}

    claim_reports = []
    all_cycles = list(global_cycles)
    for claim in bundle.get("claims", []):
        cid = claim["id"]
        claim_ancestry, claim_cycles = ancestry_map(bundle, cid)
        all_cycles.extend(claim_cycles)
        sids = claim.get("source_ids", [])
        pairwise = []
        for i, a in enumerate(sids):
            for b in sids[i + 1 :]:
                pairwise.append(_pair_state(bundle, cid, a, b, claim_ancestry, source_by_id))
        shared = [p for p in pairwise if p["state"] == "shared"]
        claim_reports.append(
            {
                "id": cid,
                "text": claim.get("text", ""),
                "evidence_state": claim["evidence_state"],
                "source_ids": sids,
                "source_pair_lineage": pairwise,
                "shared_ancestry": shared,
                "input_notes": claim.get("notes", []),
            }
        )

    # Deduplicate cycles while preserving order.
    cycles: list[list[str]] = []
    seen_cycles: set[tuple[str, ...]] = set()
    for cycle in all_cycles:
        key = tuple(cycle)
        if key not in seen_cycles:
            seen_cycles.add(key)
            cycles.append(cycle)

    return {
        "format": "evidence-lineage-report-v0.2",
        "input_title": bundle.get("title"),
        "sources": [
            {
                "id": sid,
                "label": source_by_id[sid].get("label", sid),
                "locator": source_by_id[sid].get("locator"),
                "locator_status": "supplied_unverified" if source_by_id[sid].get("locator") else "absent",
                "lineage_state": source_by_id[sid].get("lineage_state", "unknown"),
                "global_ancestors": sorted(global_ancestry.get(sid, set())),
            }
            for sid in source_by_id
        ],
        "claims": claim_reports,
        "relations": bundle.get("relations", []),
        "ancestry_cycles": cycles,
        "ceilings": [
            "REPETITION != CORROBORATION",
            "MISSING_LINEAGE != INDEPENDENCE",
            "DECLARED_INDEPENDENT != PROVEN_INDEPENDENT",
            "UNKNOWN != ABSENT",
            "EVIDENCE_STATE != TRUTH_SCORE",
            "SUPPLIED_LOCATOR != CHECKED_LOCATOR",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    out = [f"# {report.get('input_title') or 'Evidence lineage report'}", "", "## Claims", ""]
    for claim in report["claims"]:
        out.append(f"### {claim['id']}")
        out.append(claim["text"] or "*(no claim text supplied)*")
        out.append("")
        out.append(f"- Evidence state (input): `{claim['evidence_state']}`")
        out.append(f"- Sources: {', '.join(claim['source_ids']) if claim['source_ids'] else 'none'}")
        if claim["source_pair_lineage"]:
            out.append("- Pairwise lineage on supplied graph:")
            for item in claim["source_pair_lineage"]:
                detail = ""
                if item["shared_ancestry"]:
                    detail = " via " + ", ".join(f"`{x}`" for x in item["shared_ancestry"])
                out.append(f"  - `{item['source_a']}` + `{item['source_b']}`: `{item['state']}`{detail}")
        else:
            out.append("- Pairwise lineage: not applicable")
        for note in claim.get("input_notes", []):
            out.append(f"- Input note (not independently checked): {note}")
        out.append("")

    out.extend(["## Sources", ""])
    for src in report["sources"]:
        out.append(f"- `{src['id']}` — {src['label']}")
        out.append(f"  - Lineage state (input/default): `{src['lineage_state']}`")
        if src.get("locator"):
            out.append(f"  - Supplied locator (not checked): {src['locator']}")
        out.append(
            "  - Global ancestors on supplied graph: "
            + (", ".join(f"`{x}`" for x in src["global_ancestors"]) if src["global_ancestors"] else "none")
        )

    if report["ancestry_cycles"]:
        out.extend(["", "## Invalid ancestry cycles", ""])
        for cycle in report["ancestry_cycles"]:
            out.append("- " + " -> ".join(cycle))

    out.extend(["", "## Ceilings", ""])
    out.extend(f"- `{c}`" for c in report["ceilings"])
    out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", dest="json_out", type=Path)
    parser.add_argument("--markdown", dest="md_out", type=Path)
    args = parser.parse_args()

    try:
        bundle = load_bundle(args.input)
        errors = validate(bundle)
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 2
        report = build_report(bundle)
        if report["ancestry_cycles"]:
            for cycle in report["ancestry_cycles"]:
                print("ERROR: ancestry cycle: " + " -> ".join(cycle))
            return 3
        if args.json_out:
            args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.md_out:
            args.md_out.write_text(render_markdown(report), encoding="utf-8")
        if not args.json_out and not args.md_out:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
