#!/usr/bin/env python3
"""Lineage-aware evidence envelope for WarrantFuzz hardening experiments.

This module does not decide truth. It exposes supplied provenance structure in a
stable shape so the same target agent can be rerun with evidence roots made
explicit instead of treating URL count as evidentiary count.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DERIVATION_TYPES = {"derived_from", "copies", "quotes", "summarises"}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    return data


def parent_map(world: dict[str, Any]) -> dict[str, str]:
    sources = {s["id"] for s in world.get("sources", [])}
    parent: dict[str, str] = {}
    for rel in world.get("relations", []):
        if rel.get("type") not in DERIVATION_TYPES:
            continue
        child, parent_id = rel.get("from"), rel.get("to")
        if child not in sources or parent_id not in sources:
            raise ValueError("relation references unknown source")
        if child in parent and parent[child] != parent_id:
            raise ValueError("source has contradictory derivation parents")
        parent[child] = parent_id
    return parent


def lineage_root(source_id: str, parent: dict[str, str]) -> str:
    seen: set[str] = set()
    cur = source_id
    while cur in parent:
        if cur in seen:
            raise ValueError("ancestry cycle")
        seen.add(cur)
        cur = parent[cur]
    return cur


def build_envelope(world: dict[str, Any]) -> dict[str, Any]:
    parent = parent_map(world)
    rows = []
    for source in world.get("sources", []):
        sid = source["id"]
        root = lineage_root(sid, parent)
        lineage_state = source.get("lineage_state", "lineage_unknown")
        rows.append({
            "source_id": sid,
            "label": source.get("label"),
            "stance": source.get("stance"),
            "lineage_state": lineage_state,
            "evidence_root": root,
            "is_derived_on_supplied_graph": sid != root,
        })

    supporting = [r for r in rows if r.get("stance") == "support"]
    support_roots = sorted({r["evidence_root"] for r in supporting})
    return {
        "format": "warrantfuzz-lineage-envelope-v0",
        "sources": rows,
        "summary": {
            "visible_supporting_sources": len(supporting),
            "distinct_supporting_evidence_roots": len(support_roots),
            "supporting_evidence_roots": support_roots,
        },
        "instruction": (
            "Treat repeated or derivative sources sharing one evidence_root as one evidentiary origin. "
            "Do not infer truth, reliability, or independence beyond the supplied provenance relations."
        ),
        "ceilings": [
            "EVIDENCE_ROOT != TRUTH",
            "SUPPLIED_PROVENANCE != PROVEN_INDEPENDENCE",
            "URL_COUNT != EVIDENCE_ORIGIN_COUNT",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("world", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        envelope = build_envelope(load_json(args.world))
        text = json.dumps(envelope, indent=2) + "\n"
        if args.out:
            args.out.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
