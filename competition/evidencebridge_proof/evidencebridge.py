#!/usr/bin/env python3
"""EvidenceBridge v0: deterministic, source-bound evidence inspection."""
from __future__ import annotations

import argparse
import html
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ALLOWED_STATES = {"OBSERVED", "REPORTED", "INFERRED", "UNKNOWN"}
ALLOWED_RELATIONS = {
    "ASSERTS", "SUPPORTS", "CONTRADICTS", "QUESTIONS",
    "RESTATES", "NEARBY_NOT_SUPPORT", "LIMITS",
}


class EvidenceBridgeError(ValueError):
    pass


@dataclass(frozen=True)
class ClaimAnalysis:
    claim_id: str
    text: str
    verdict: str
    support_groups: tuple[str, ...]
    supports: tuple[str, ...]
    assertions: tuple[str, ...]
    dependent_restatements: tuple[str, ...]
    contradictions: tuple[str, ...]
    questions: tuple[str, ...]
    limits: tuple[str, ...]
    unknowns: tuple[str, ...]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceBridgeError(message)


def _index(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for item in items:
        ident = item.get("id")
        _require(isinstance(ident, str) and ident.strip(), f"{label}: missing id")
        _require(ident not in out, f"{label}: duplicate id {ident}")
        out[ident] = item
    return out


def validate_bundle(bundle: dict[str, Any]) -> None:
    _require(bundle.get("format") == "evidencebridge/0.1", "unsupported format")
    claims = _index(bundle.get("claims", []), "claim")
    sources = _index(bundle.get("sources", []), "source")
    propositions = _index(bundle.get("propositions", []), "proposition")
    _require(bool(claims), "at least one focal claim is required")
    _require(bool(sources), "at least one source is required")

    for sid, source in sources.items():
        group = source.get("independence_group")
        _require(isinstance(group, str) and group.strip(), f"source {sid}: independence_group required")
        parents = source.get("derived_from", [])
        _require(isinstance(parents, list), f"source {sid}: derived_from must be a list")
        for parent in parents:
            _require(parent in sources, f"source {sid}: unknown derived_from source {parent}")
            _require(parent != sid, f"source {sid}: cannot derive from itself")
            _require(
                sources[parent].get("independence_group") == group,
                f"source {sid}: derived source must share parent independence_group",
            )

    for pid, prop in propositions.items():
        _require(prop.get("source_id") in sources, f"proposition {pid}: unknown source {prop.get('source_id')}")
        _require(prop.get("claim_id") in claims, f"proposition {pid}: unknown claim {prop.get('claim_id')}")
        _require(prop.get("state") in ALLOWED_STATES, f"proposition {pid}: invalid state {prop.get('state')}")
        _require(prop.get("relation") in ALLOWED_RELATIONS, f"proposition {pid}: invalid relation {prop.get('relation')}")
        _require(isinstance(prop.get("text"), str) and prop["text"].strip(), f"proposition {pid}: text required")

    corrections = _index(bundle.get("corrections", []), "correction")
    for cid, correction in corrections.items():
        old = correction.get("supersedes_proposition_id")
        new = correction.get("replacement_proposition_id")
        sid = correction.get("source_id")
        _require(old in propositions, f"correction {cid}: missing superseded proposition {old}")
        _require(new in propositions, f"correction {cid}: missing replacement proposition {new}")
        if sid is not None:
            _require(sid in sources, f"correction {cid}: unknown source {sid}")


def analyze_claim(bundle: dict[str, Any], claim_id: str) -> ClaimAnalysis:
    validate_bundle(bundle)
    claims = _index(bundle["claims"], "claim")
    sources = _index(bundle["sources"], "source")
    propositions = _index(bundle.get("propositions", []), "proposition")
    _require(claim_id in claims, f"unknown claim {claim_id}")
    relevant = [p for p in propositions.values() if p["claim_id"] == claim_id]

    supports = [p for p in relevant if p["relation"] == "SUPPORTS"]
    assertions = [p for p in relevant if p["relation"] == "ASSERTS"]
    restatements = [p for p in relevant if p["relation"] == "RESTATES"]
    contradictions = [p for p in relevant if p["relation"] == "CONTRADICTS"]
    questions = [p for p in relevant if p["relation"] == "QUESTIONS"]
    limits = [p for p in relevant if p["relation"] in {"NEARBY_NOT_SUPPORT", "LIMITS"}]
    support_groups = sorted({sources[p["source_id"]]["independence_group"] for p in supports})

    reported_contradictions = [p for p in contradictions if p["state"] == "REPORTED"]
    direct_contradictions = [p for p in contradictions if p["state"] == "OBSERVED"]

    if support_groups and not contradictions:
        verdict = "SUPPORTED_WITHIN_CHECKED_SOURCES"
    elif support_groups and contradictions:
        verdict = "DISPUTED_WITHIN_CHECKED_SOURCES"
    elif direct_contradictions:
        verdict = "CONTRADICTED_WITHIN_CHECKED_SOURCES"
    elif reported_contradictions:
        verdict = "UNRESOLVED_WITH_REPORTED_CONTRADICTION"
    elif assertions or restatements:
        verdict = "ASSERTED_BUT_UNSUPPORTED_IN_CHECKED_SOURCES"
    else:
        verdict = "UNRESOLVED"

    unknowns = tuple(
        u["text"] for u in bundle.get("unknowns", [])
        if not u.get("claim_ids") or claim_id in u.get("claim_ids", [])
    )

    return ClaimAnalysis(
        claim_id=claim_id,
        text=claims[claim_id]["text"],
        verdict=verdict,
        support_groups=tuple(support_groups),
        supports=tuple(p["id"] for p in supports),
        assertions=tuple(p["id"] for p in assertions),
        dependent_restatements=tuple(p["id"] for p in restatements),
        contradictions=tuple(p["id"] for p in contradictions),
        questions=tuple(p["id"] for p in questions),
        limits=tuple(p["id"] for p in limits),
        unknowns=unknowns,
    )


def analyze_bundle(bundle: dict[str, Any]) -> list[ClaimAnalysis]:
    validate_bundle(bundle)
    return [analyze_claim(bundle, claim["id"]) for claim in bundle["claims"]]


def _prop_rows(bundle: dict[str, Any], claim_id: str) -> list[dict[str, Any]]:
    sources = _index(bundle["sources"], "source")
    rows: list[dict[str, Any]] = []
    for prop in bundle.get("propositions", []):
        if prop["claim_id"] != claim_id:
            continue
        source = sources[prop["source_id"]]
        rows.append({
            **prop,
            "source_label": source["label"],
            "source_url": source.get("url") or source.get("locator"),
            "independence_group": source["independence_group"],
            "derived_from": source.get("derived_from", []),
        })
    return rows


def render_text(bundle: dict[str, Any]) -> str:
    validate_bundle(bundle)
    lines = [
        f"EVIDENCEBRIDGE :: {bundle.get('title', bundle.get('case_id', 'case'))}",
        f"case={bundle.get('case_id')}",
        "",
    ]
    for analysis in analyze_bundle(bundle):
        lines += [
            f"CLAIM: {analysis.text}",
            f"VERDICT: {analysis.verdict}",
            f"INDEPENDENT_SUPPORT_GROUPS: {len(analysis.support_groups)}",
        ]
        for row in _prop_rows(bundle, analysis.claim_id):
            derived = f" derived_from={','.join(row['derived_from'])}" if row["derived_from"] else ""
            lines.append(
                f"  [{row['relation']}/{row['state']}] {row['source_label']} "
                f"(group={row['independence_group']}{derived})"
            )
            lines.append(f"    {row['text']}")
            if row.get("scope_note"):
                lines.append(f"    LIMIT: {row['scope_note']}")
        if analysis.unknowns:
            lines.append("  UNKNOWNS:")
            lines.extend(f"    - {item}" for item in analysis.unknowns)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_html(bundle: dict[str, Any]) -> str:
    validate_bundle(bundle)
    analyses = analyze_bundle(bundle)
    sources = _index(bundle["sources"], "source")
    sections: list[str] = []

    for analysis in analyses:
        rows: list[str] = []
        for row in _prop_rows(bundle, analysis.claim_id):
            url = row.get("source_url")
            label = html.escape(row["source_label"])
            source_display = f'<a href="{html.escape(url, quote=True)}">{label}</a>' if url else label
            derived = ""
            if row["derived_from"]:
                parent_labels = [sources[p]["label"] for p in row["derived_from"]]
                derived = '<p class="dependence"><strong>Depends on:</strong> ' + html.escape(", ".join(parent_labels)) + "</p>"
            scope = f'<p class="scope"><strong>Ceiling:</strong> {html.escape(row["scope_note"])}</p>' if row.get("scope_note") else ""
            rows.append(
                '<article class="evidence">'
                f'<div class="badges"><span>{html.escape(row["relation"])}</span>'
                f'<span>{html.escape(row["state"])}</span>'
                f'<span>group {html.escape(row["independence_group"])}</span></div>'
                f'<p>{html.escape(row["text"])}</p>'
                f'<p class="source"><strong>Source:</strong> {source_display}</p>'
                f'{derived}{scope}</article>'
            )
        unknown_html = "".join(f"<li>{html.escape(x)}</li>" for x in analysis.unknowns)
        sections.append(
            '<section class="claim">'
            '<p class="kicker">Focal claim</p>'
            f'<h2>{html.escape(analysis.text)}</h2>'
            f'<div class="verdict">{html.escape(analysis.verdict.replace("_", " "))}</div>'
            f'<p class="metric"><strong>Independent support groups:</strong> {len(analysis.support_groups)}</p>'
            '<details open><summary>Show me why</summary>'
            + ("".join(rows) if rows else "<p>No checked proposition bears directly on this claim.</p>")
            + "</details>"
            + (f"<h3>Still unknown</h3><ul>{unknown_html}</ul>" if unknown_html else "")
            + "</section>"
        )

    title = html.escape(bundle.get("title", "EvidenceBridge"))
    note = html.escape(bundle.get("case_note", ""))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — EvidenceBridge</title>
<style>
:root{{font-family:Inter,ui-sans-serif,system-ui,sans-serif}}body{{margin:0;background:#f5f3ee;color:#191816}}
main{{max-width:900px;margin:0 auto;padding:48px 20px 80px}}header{{border-bottom:1px solid #cfc8bd;padding-bottom:24px;margin-bottom:28px}}
h1{{font-size:clamp(2rem,6vw,4.6rem);line-height:.96;margin:.3rem 0 1rem;letter-spacing:-.04em}}h2{{font-size:1.55rem;line-height:1.2}}
.kicker{{text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;font-weight:800;color:#80552f}}
.claim{{background:white;border:1px solid #d8d1c6;border-radius:18px;padding:24px;margin:20px 0}}
.verdict{{display:inline-block;background:#1d1c19;color:white;border-radius:999px;padding:8px 12px;font-size:.78rem;font-weight:800}}
.metric{{color:#5b554d}}details{{margin-top:22px}}summary{{cursor:pointer;font-weight:800;margin-bottom:14px}}
.evidence{{border-left:3px solid #b27846;padding:10px 14px;margin:14px 0;background:#faf8f4}}
.badges{{display:flex;flex-wrap:wrap;gap:6px}}.badges span{{font-size:.68rem;letter-spacing:.06em;background:#e9e3da;padding:4px 7px;border-radius:999px}}
.source,.dependence,.scope{{font-size:.88rem;color:#5f594f}}.scope{{border-top:1px solid #e3ddd4;padding-top:8px}}a{{color:#70441f}}
footer{{color:#6a645b;font-size:.83rem;margin-top:28px}}
</style></head><body><main><header><p class="kicker">EvidenceBridge · deterministic proof</p>
<h1>{title}</h1><p>{note}</p>
<p><strong>No truth score.</strong> Repetition is not silently counted as corroboration; source reports remain attributed.</p>
</header>{''.join(sections)}
<footer>EvidenceBridge v0 · product proof, not a truth oracle or automated fact-checking authority.</footer>
</main></body></html>"""


def load_bundle(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--format", choices=("text", "json", "html"), default="text")
    args = parser.parse_args()
    bundle = load_bundle(args.bundle)
    validate_bundle(bundle)
    if args.format == "text":
        print(render_text(bundle), end="")
    elif args.format == "json":
        print(json.dumps([a.__dict__ for a in analyze_bundle(bundle)], indent=2))
    else:
        print(render_html(bundle))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
