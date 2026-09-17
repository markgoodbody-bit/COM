#!/usr/bin/env python3
"""Deterministic evidence-lineage validator and renderer.

This is intentionally not an extractor or truth scorer. It validates an explicit
claim/source graph and makes ancestry and shared derivation inspectable.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ANCESTRY_RELATIONS = {"derived_from", "quotes", "summarises", "copies"}
EVIDENCE_STATES = {"observed", "source_stated", "inferred", "unresolved"}
RELATION_TYPES = ANCESTRY_RELATIONS | {"independent_of", "disputes", "corrects"}


def load_bundle(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    return data


def validate(bundle: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sources = bundle.get("sources", [])
    claims = bundle.get("claims", [])
    relations = bundle.get("relations", [])

    if not isinstance(sources, list) or not isinstance(claims, list) or not isinstance(relations, list):
        return ["sources, claims and relations must be arrays"]

    source_ids: set[str] = set()
    for i, src in enumerate(sources):
        if not isinstance(src, dict):
            errors.append(f"sources[{i}] must be an object")
            continue
        sid = src.get("id")
        if not isinstance(sid, str) or not sid:
            errors.append(f"sources[{i}].id must be a non-empty string")
        elif sid in source_ids:
            errors.append(f"duplicate source id: {sid}")
        else:
            source_ids.add(sid)

    claim_ids: set[str] = set()
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{i}] must be an object")
            continue
        cid = claim.get("id")
        state = claim.get("evidence_state")
        if not isinstance(cid, str) or not cid:
            errors.append(f"claims[{i}].id must be a non-empty string")
        elif cid in claim_ids:
            errors.append(f"duplicate claim id: {cid}")
        else:
            claim_ids.add(cid)
        if state not in EVIDENCE_STATES:
            errors.append(f"claim {cid or i}: invalid evidence_state {state!r}")
        for sid in claim.get("source_ids", []):
            if sid not in source_ids:
                errors.append(f"claim {cid or i}: unknown source_id {sid!r}")

    for i, rel in enumerate(relations):
        if not isinstance(rel, dict):
            errors.append(f"relations[{i}] must be an object")
            continue
        rtype = rel.get("type")
        src = rel.get("from")
        dst = rel.get("to")
        if rtype not in RELATION_TYPES:
            errors.append(f"relations[{i}]: invalid type {rtype!r}")
        if src not in source_ids:
            errors.append(f"relations[{i}]: unknown from source {src!r}")
        if dst not in source_ids:
            errors.append(f"relations[{i}]: unknown to source {dst!r}")
        if src == dst:
            errors.append(f"relations[{i}]: self relation is not allowed")

    return errors


def ancestry_map(bundle: dict[str, Any]) -> tuple[dict[str, set[str]], list[list[str]]]:
    parents: dict[str, set[str]] = defaultdict(set)
    source_ids = [s["id"] for s in bundle.get("sources", []) if isinstance(s, dict) and "id" in s]
    for rel in bundle.get("relations", []):
        if rel.get("type") in ANCESTRY_RELATIONS:
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


def build_report(bundle: dict[str, Any]) -> dict[str, Any]:
    ancestry, cycles = ancestry_map(bundle)
    source_by_id = {s["id"]: s for s in bundle.get("sources", [])}

    claim_reports = []
    for claim in bundle.get("claims", []):
        sids = claim.get("source_ids", [])
        roots: dict[str, set[str]] = {}
        for sid in sids:
            roots[sid] = {sid} | ancestry.get(sid, set())

        overlaps = []
        for i, a in enumerate(sids):
            for b in sids[i + 1 :]:
                shared = sorted(roots[a] & roots[b])
                if shared:
                    overlaps.append({"source_a": a, "source_b": b, "shared_ancestry": shared})

        claim_reports.append(
            {
                "id": claim["id"],
                "text": claim.get("text", ""),
                "evidence_state": claim["evidence_state"],
                "source_ids": sids,
                "shared_ancestry": overlaps,
                "notes": claim.get("notes", []),
            }
        )

    return {
        "format": "evidence-lineage-report-v0",
        "input_title": bundle.get("title"),
        "sources": [
            {
                "id": sid,
                "label": source_by_id[sid].get("label", sid),
                "locator": source_by_id[sid].get("locator"),
                "ancestors": sorted(ancestry.get(sid, set())),
            }
            for sid in source_by_id
        ],
        "claims": claim_reports,
        "relations": bundle.get("relations", []),
        "ancestry_cycles": cycles,
        "ceilings": [
            "REPETITION != CORROBORATION",
            "SHARED_ANCESTRY != INDEPENDENT_SOURCE",
            "UNKNOWN != ABSENT",
            "EVIDENCE_STATE != TRUTH_SCORE",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    out = [f"# {report.get('input_title') or 'Evidence lineage report'}", "", "## Claims", ""]
    for claim in report["claims"]:
        out.append(f"### {claim['id']}")
        out.append(claim["text"] or "*(no claim text supplied)*")
        out.append("")
        out.append(f"- Evidence state: `{claim['evidence_state']}`")
        out.append(f"- Sources: {', '.join(claim['source_ids']) if claim['source_ids'] else 'none'}")
        if claim["shared_ancestry"]:
            out.append("- Shared ancestry detected:")
            for item in claim["shared_ancestry"]:
                out.append(
                    f"  - `{item['source_a']}` + `{item['source_b']}` share: "
                    + ", ".join(f"`{x}`" for x in item["shared_ancestry"])
                )
        else:
            out.append("- Shared ancestry detected: none from supplied relations")
        for note in claim.get("notes", []):
            out.append(f"- Note: {note}")
        out.append("")

    out.extend(["## Sources", ""])
    for src in report["sources"]:
        out.append(f"- `{src['id']}` — {src['label']}")
        if src.get("locator"):
            out.append(f"  - Locator: {src['locator']}")
        out.append(
            "  - Ancestors: " + (", ".join(f"`{x}`" for x in src["ancestors"]) if src["ancestors"] else "none")
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
