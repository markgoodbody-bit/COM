#!/usr/bin/env python3
"""Build a static reader lens for frozen ATRS audit evidence.

The lens does not score a department, infer legal rights, or decide whether a
review route is effective. It reorganises already-published ATRS evidence into a
reader-facing view centred on one practical question: what does this record
actually say about what someone can do next?

Input:
- a frozen audit report produced by audit.py;
- optionally, evidence-bound exploratory semantic coding produced by
  exploratory_semantic_census.py.

Output:
- one self-contained HTML file with search/filter and source-linked cards.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

LABEL_TITLES = {
    "PUBLIC_INITIATION": "Concrete initiation described",
    "PROCESS_REFERENCE": "Review / complaint process referenced",
    "HELP_FEEDBACK": "Help or feedback route",
    "IN_CHANNEL_HANDOFF": "Human handoff inside the interaction",
    "INTERNAL_REVIEW": "Internal / professional review",
    "NO_SEPARATE": "No separate process / no relevant decision stated",
    "SELF_CORRECTION": "Self-correction / retry path",
    "DATA_RIGHTS": "Data-rights action",
    "REFUSAL_OR_OPT_OUT": "Refusal / opt-out described",
    "EXPLANATION_ONLY": "Explanation / audit trail without reversal",
    "PLANNED_NOT_OPERATING": "Process planned but not operating",
    "AMBIGUOUS": "Published wording remains ambiguous",
}

CEILINGS = [
    "This page reorganises public ATRS disclosure; it does not establish hidden or internal practice.",
    "A published contact route is not proof that a legal right exists or that the route is effective.",
    "A missing route or field is not proof that no route or practice exists elsewhere.",
    "Exploratory labels, when shown, are provisional annotations rather than validated classifications.",
]


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def text(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def field_text(row: dict[str, Any], field_name: str) -> str:
    field = row.get("fields", {}).get(field_name, {})
    matches = field.get("matches", [])
    return "\n\n".join(str(m.get("text", "")).strip() for m in matches if str(m.get("text", "")).strip())


def observed_tokens(row: dict[str, Any]) -> list[str]:
    field = row.get("fields", {}).get("appeals_review", {})
    out: list[str] = []
    for match in field.get("matches", []):
        tokens = match.get("contact_tokens", {})
        for key in ("hrefs", "urls_in_text", "emails", "phones"):
            for token in tokens.get(key, []) or []:
                token = str(token).strip()
                if token and token not in out:
                    out.append(token)
    return out


def semantic_map(report: dict[str, Any], semantic_path: Path | None) -> dict[str, list[str]]:
    if semantic_path is None:
        return {}
    semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
    expected_digest = semantic.get("evidence_sha256")
    if not expected_digest:
        raise ValueError("semantic coding has no evidence_sha256; refusing unbound annotation")
    module = load_module("atrs_reader_semantic", "exploratory_semantic_census.py")
    actual_digest = module.appeals_evidence_digest(report)
    if actual_digest != expected_digest:
        raise ValueError("semantic coding does not match audit evidence")
    return {str(r["url"]): list(r.get("labels", [])) for r in semantic.get("records", [])}


def card(row: dict[str, Any], labels: list[str]) -> str:
    appeals = row.get("fields", {}).get("appeals_review", {})
    human = field_text(row, "human_review")
    owner = field_text(row, "senior_responsible_owner")
    appeals_text = field_text(row, "appeals_review")
    tokens = observed_tokens(row)
    field_present = bool(appeals.get("section_present"))
    contact_present = bool(appeals.get("syntactic_contact_token_present"))

    annotation_html = ""
    if labels:
        tags = "".join(
            f'<span class="tag" title="Exploratory annotation; not validated classification">{text(LABEL_TITLES.get(label, label))}</span>'
            for label in labels
        )
        annotation_html = (
            '<div class="annotations">'
            '<p class="annotation-label">Exploratory annotations — post-pilot; not validated</p>'
            f'<div class="tags">{tags}</div>'
            '</div>'
        )

    token_html = (
        "<ul>" + "".join(f"<li><code>{text(token)}</code></li>" for token in tokens) + "</ul>"
        if tokens
        else '<p class="muted">No URL, email, phone-like token, or link destination was observed in the published Appeals and review field. This does not mean no route exists.</p>'
    )

    appeals_html = (
        f'<p class="source-text">{text(appeals_text)}</p>'
        if appeals_text
        else '<p class="muted">No parser-recognised Appeals and review field was observed in this frozen record.</p>'
    )
    human_html = f'<p class="source-text">{text(human)}</p>' if human else '<p class="muted">No parser-recognised human-review field was observed.</p>'
    owner_html = f'<p class="source-text">{text(owner)}</p>' if owner else '<p class="muted">No parser-recognised senior-responsible-owner field was observed.</p>'

    search_text = " ".join(
        [str(row.get("title", "")), appeals_text, human, owner, " ".join(labels)]
    ).lower()
    attrs = {
        "data-search": search_text,
        "data-appeals": "yes" if field_present else "no",
        "data-contact": "yes" if contact_present else "no",
    }
    attr_text = " ".join(f'{k}="{text(v)}"' for k, v in attrs.items())

    return f'''<article class="card" {attr_text}>
      <header>
        <div>
          <h2>{text(row.get("title", "Untitled record"))}</h2>
          <p class="meta">Frozen source SHA-256: <code>{text(row.get("source_sha256", "unknown"))}</code></p>
        </div>
        <a class="source-link" href="{text(row.get("url", ""))}" target="_blank" rel="noopener noreferrer">Open GOV.UK source</a>
      </header>
      {annotation_html}
      <section>
        <h3>What the record says about appeals and review</h3>
        {appeals_html}
      </section>
      <section>
        <h3>Published contact / link tokens in that field</h3>
        {token_html}
      </section>
      <details>
        <summary>Human review disclosed in the record</summary>
        {human_html}
      </details>
      <details>
        <summary>Senior responsible owner disclosed in the record</summary>
        {owner_html}
      </details>
      <aside class="ceiling">Do not infer route effectiveness, legal entitlement, completeness, or internal practice from this card.</aside>
    </article>'''


def build_html(report: dict[str, Any], semantic: dict[str, list[str]]) -> str:
    rows = report.get("records", [])
    cards = "\n".join(card(row, semantic.get(str(row.get("url", "")), [])) for row in rows)
    ceilings = "".join(f"<li>{text(item)}</li>" for item in CEILINGS)
    annotated = sum(1 for row in rows if semantic.get(str(row.get("url", ""))))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ATRS Reader Lens</title>
<style>
:root {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #161616; background: #f5f5f5; }}
body {{ margin: 0; }}
main {{ max-width: 1080px; margin: 0 auto; padding: 2rem 1rem 5rem; }}
.hero {{ background: #fff; border: 1px solid #ddd; padding: 1.5rem; margin-bottom: 1rem; }}
.controls {{ position: sticky; top: 0; z-index: 10; background: rgba(245,245,245,.96); padding: .75rem 0; display: grid; gap: .5rem; grid-template-columns: 2fr repeat(2, minmax(150px, 1fr)) minmax(210px, 1fr); align-items: center; }}
input, select {{ font: inherit; padding: .7rem; border: 1px solid #aaa; background: #fff; }}
.annotation-toggle {{ display: flex; align-items: center; gap: .5rem; padding: .55rem .65rem; background: #fff; border: 1px solid #aaa; font-size: .88rem; }}
.annotation-toggle input {{ margin: 0; }}
.card {{ background: #fff; border: 1px solid #d5d5d5; padding: 1.2rem; margin: 1rem 0; }}
.card header {{ display: flex; justify-content: space-between; gap: 1rem; align-items: flex-start; }}
h1, h2, h3 {{ line-height: 1.2; }} h2 {{ margin: 0; font-size: 1.2rem; }} h3 {{ margin-bottom: .35rem; font-size: 1rem; }}
.meta, .muted {{ color: #666; }} .meta {{ font-size: .85rem; word-break: break-all; }}
.source-link {{ white-space: nowrap; }} .source-text {{ white-space: pre-wrap; line-height: 1.55; border-left: 3px solid #bbb; padding-left: .8rem; }}
.annotations {{ display: none; margin: .8rem 0; padding: .65rem .75rem; border: 1px dashed #999; background: #fafafa; }}
.show-annotations .annotations {{ display: block; }}
.annotation-label {{ margin: 0 0 .45rem; font-size: .8rem; font-weight: 650; }}
.tags {{ display: flex; flex-wrap: wrap; gap: .4rem; }}
.tag {{ border: 1px solid #999; border-radius: 999px; padding: .2rem .55rem; font-size: .78rem; }}
.ceiling {{ margin-top: 1rem; padding: .75rem; background: #f3f3f3; font-size: .85rem; }}
.hidden {{ display: none; }} code {{ overflow-wrap: anywhere; }}
@media (max-width: 900px) {{ .controls {{ grid-template-columns: 1fr 1fr; position: static; }} }}
@media (max-width: 620px) {{ .controls {{ grid-template-columns: 1fr; }} .card header {{ display: block; }} .source-link {{ display: inline-block; margin-top: .5rem; }} }}
</style>
</head>
<body>
<main>
<section class="hero">
<h1>ATRS Reader Lens</h1>
<p><strong>Question:</strong> what does a published ATRS record actually say about what someone can do next?</p>
<p>This view reorganises the frozen public record. It is not a transparency score, legal-advice tool, compliance finding, or claim about undisclosed government practice.</p>
<p><strong>{len(rows)}</strong> frozen records. Optional evidence-bound exploratory annotations exist for <strong>{annotated}</strong> records but are hidden by default.</p>
<ul>{ceilings}</ul>
</section>
<section class="controls" aria-label="Reader filters">
<input id="q" type="search" placeholder="Search tool, organisation or disclosed text">
<select id="appeals"><option value="">Appeals field: any</option><option value="yes">Observed</option><option value="no">Not observed</option></select>
<select id="contact"><option value="">Contact token: any</option><option value="yes">Observed</option><option value="no">Not observed</option></select>
<label class="annotation-toggle"><input id="annotations" type="checkbox"> Show exploratory annotations</label>
</section>
<p id="count" class="meta"></p>
<section id="cards">{cards}</section>
</main>
<script>
const q = document.getElementById('q');
const appeals = document.getElementById('appeals');
const contact = document.getElementById('contact');
const annotations = document.getElementById('annotations');
const cards = [...document.querySelectorAll('.card')];
const count = document.getElementById('count');
function apply() {{
  const needle = q.value.trim().toLowerCase();
  let shown = 0;
  for (const card of cards) {{
    const ok = (!needle || card.dataset.search.includes(needle)) &&
      (!appeals.value || card.dataset.appeals === appeals.value) &&
      (!contact.value || card.dataset.contact === contact.value);
    card.classList.toggle('hidden', !ok);
    if (ok) shown++;
  }}
  document.body.classList.toggle('show-annotations', annotations.checked);
  count.textContent = `${{shown}} of ${{cards.length}} records shown`;
}}
for (const el of [q, appeals, contact, annotations]) el.addEventListener('input', apply);
apply();
</script>
</body>
</html>'''


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("report", type=Path)
    p.add_argument("--semantic", type=Path)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    semantic = semantic_map(report, args.semantic)
    output = build_html(report, semantic)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
