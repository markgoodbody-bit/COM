#!/usr/bin/env python3
"""Build a static reader lens for frozen ATRS audit evidence.

The lens does not score a department, infer legal rights, or decide whether a
review route is effective. It reorganises already-published ATRS evidence around
a practical retrieval question: what does this record actually say about what
someone can do next?

The default surface is source evidence only. Optional exploratory annotations
are evidence-bound, hidden by default, and cannot affect search unless the
reader explicitly enables them.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

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
    "A published contact or link is not proof that a legal right exists or that a route is effective.",
    "A missing route or field is not proof that no route or practice exists elsewhere.",
    "Exploratory labels, when enabled, are post-pilot annotations rather than validated classifications.",
]

EMAIL_ONLY_RE = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.I)


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def field_text(row: dict[str, Any], field_name: str) -> str:
    field = row.get("fields", {}).get(field_name, {})
    matches = field.get("matches", [])
    return "\n\n".join(
        str(m.get("text", "")).strip()
        for m in matches
        if str(m.get("text", "")).strip()
    )


def frozen_date(row: dict[str, Any]) -> str:
    value = str(row.get("fetched_at_utc") or "")
    return value[:10] if len(value) >= 10 else "frozen September 2026 evidence"


def safe_href(token: str) -> str | None:
    """Return an actionable destination only for explicit safe schemes.

    Relative hrefs and phone-like strings remain visible evidence but are not
    converted into actions by this reader.
    """
    token = token.strip()
    if EMAIL_ONLY_RE.fullmatch(token):
        return f"mailto:{token}"
    parsed = urlparse(token)
    if parsed.scheme.lower() in {"http", "https"} and parsed.netloc:
        return token
    if parsed.scheme.lower() == "mailto" and parsed.path:
        return token
    return None


def observed_tokens(row: dict[str, Any]) -> list[dict[str, str]]:
    field = row.get("fields", {}).get("appeals_review", {})
    out: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for match in field.get("matches", []):
        tokens = match.get("contact_tokens", {})
        for kind, key in (
            ("published link", "hrefs"),
            ("URL in published text", "urls_in_text"),
            ("email in published text", "emails"),
            ("phone-like text", "phones"),
        ):
            for raw in tokens.get(key, []) or []:
                value = str(raw).strip()
                identity = (kind, value)
                if not value or identity in seen:
                    continue
                seen.add(identity)
                out.append({"kind": kind, "value": value})
    return out


def token_html(token: dict[str, str]) -> str:
    value = token["value"]
    kind = token["kind"]
    href = safe_href(value) if kind != "phone-like text" else None
    if href:
        rendered = (
            f'<a href="{esc(href)}" target="_blank" rel="noopener noreferrer">'
            f'{esc(value)}</a>'
        )
    else:
        rendered = f"<code>{esc(value)}</code>"
    caution = (
        ' <span class="token-note">Detected number; verify context in the source text.</span>'
        if kind == "phone-like text"
        else ""
    )
    return f"<li><span class=\"token-kind\">{esc(kind)}:</span> {rendered}{caution}</li>"


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
    appeals_text = field_text(row, "appeals_review")
    human = field_text(row, "human_review")
    owner = field_text(row, "senior_responsible_owner")
    tokens = observed_tokens(row)
    field_present = bool(appeals.get("section_present"))
    contact_present = bool(appeals.get("syntactic_contact_token_present"))

    annotation_html = ""
    if labels:
        tags = "".join(
            f'<span class="tag" title="Exploratory annotation; not validated classification">'
            f'{esc(LABEL_TITLES.get(label, label))}</span>'
            for label in labels
        )
        annotation_html = (
            '<div class="annotations">'
            '<p class="annotation-label">Exploratory annotations — post-pilot; not validated</p>'
            f'<div class="tags">{tags}</div>'
            '</div>'
        )

    token_block = (
        '<ul class="token-list">' + "".join(token_html(t) for t in tokens) + "</ul>"
        if tokens
        else (
            '<p class="muted">No URL, email, phone-like token, or link destination was '
            'observed in the published Appeals and review field. This does not mean no route exists.</p>'
        )
    )
    appeals_block = (
        f'<p class="source-text">{esc(appeals_text)}</p>'
        if appeals_text
        else (
            '<p class="muted">No parser-recognised Appeals and review field was observed '
            'in this frozen record. This is a statement about the published page, not about '
            'whether a route or practice exists elsewhere.</p>'
        )
    )
    human_block = (
        f'<p class="source-text">{esc(human)}</p>'
        if human
        else '<p class="muted">No recognised human-review disclosure was observed on this frozen page.</p>'
    )
    owner_block = (
        f'<p class="source-text">{esc(owner)}</p>'
        if owner
        else '<p class="muted">No recognised senior-responsible-owner disclosure was observed.</p>'
    )

    source_search = " ".join(
        [str(row.get("title", "")), appeals_text, human, owner]
        + [t["value"] for t in tokens]
    ).lower()
    annotation_search = " ".join(
        [label for label in labels] + [LABEL_TITLES.get(label, label) for label in labels]
    ).lower()
    attrs = {
        "data-source-search": source_search,
        "data-annotation-search": annotation_search,
        "data-appeals": "yes" if field_present else "no",
        "data-contact": "yes" if contact_present else "no",
    }
    attr_text = " ".join(f'{k}="{esc(v)}"' for k, v in attrs.items())
    source_url = str(row.get("url", ""))

    return f'''<article class="card" {attr_text}>
      <details class="record-details">
        <summary>
          <span class="summary-title">{esc(row.get("title", "Untitled record"))}</span>
          <span class="summary-meta">Frozen {esc(frozen_date(row))} · Appeals field: {"observed" if field_present else "not observed"}</span>
        </summary>
        <div class="record-body">
          <p class="source-row"><a class="source-link" href="{esc(source_url)}" target="_blank" rel="noopener noreferrer">Open original GOV.UK record</a></p>
          <p class="annotation-match hidden" aria-hidden="true">This result matched an optional exploratory annotation.</p>
          {annotation_html}
          <section>
            <h3>Published Appeals and review passage</h3>
            {appeals_block}
          </section>
          <section>
            <h3>Published links and contact-like text in that passage</h3>
            <p class="field-note">Shown as published evidence. Presence does not establish relevance, a legal right, or route effectiveness.</p>
            {token_block}
          </section>
          <details>
            <summary>Human review disclosed in the record</summary>
            {human_block}
          </details>
          <details>
            <summary>Senior responsible owner disclosed in the record</summary>
            {owner_block}
          </details>
          <details class="evidence-details">
            <summary>Evidence details</summary>
            <dl>
              <dt>Frozen source date</dt><dd>{esc(frozen_date(row))}</dd>
              <dt>Source SHA-256</dt><dd><code>{esc(row.get("source_sha256", "unknown"))}</code></dd>
              <dt>Heading family</dt><dd>{esc(row.get("heading_profile", "not recorded"))}</dd>
            </dl>
          </details>
          <aside class="ceiling">Do not infer route effectiveness, legal entitlement, completeness, or internal practice from this card.</aside>
        </div>
      </details>
    </article>'''


def build_html(report: dict[str, Any], semantic: dict[str, list[str]]) -> str:
    rows = report.get("records", [])
    cards = "\n".join(card(row, semantic.get(str(row.get("url", "")), [])) for row in rows)
    ceilings = "".join(f"<li>{esc(item)}</li>" for item in CEILINGS)
    annotated = sum(1 for row in rows if semantic.get(str(row.get("url", ""))))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ATRS Reader Lens</title>
<style>
:root {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #161616; background: #f5f5f5; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; }}
a {{ overflow-wrap: anywhere; }}
main {{ max-width: 980px; margin: 0 auto; padding: 1.5rem 1rem 5rem; }}
.hero {{ background: #fff; border: 1px solid #ddd; padding: 1.3rem; margin-bottom: 1rem; }}
.hero h1 {{ margin-top: 0; }}
.controls {{ background: #fff; border: 1px solid #ddd; padding: 1rem; margin-bottom: 1rem; }}
.search-row {{ display: grid; grid-template-columns: 1fr auto; gap: .6rem; align-items: end; }}
.field {{ display: grid; gap: .3rem; }}
.field label, .control-label {{ font-size: .88rem; font-weight: 650; }}
input, select, button {{ font: inherit; }}
input[type=search], select {{ width: 100%; padding: .65rem; border: 1px solid #888; background: #fff; }}
button {{ padding: .65rem .9rem; border: 1px solid #666; background: #fff; cursor: pointer; }}
.advanced {{ margin-top: .75rem; }}
.advanced-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: .75rem; padding-top: .75rem; }}
.annotation-toggle {{ display: flex; align-items: center; gap: .45rem; margin-top: .75rem; }}
.results-status {{ margin: .65rem 0 0; color: #555; }}
.no-results {{ padding: 1rem; background: #fff; border: 1px solid #ddd; }}
.card {{ background: #fff; border: 1px solid #d5d5d5; margin: .65rem 0; }}
.record-details > summary {{ cursor: pointer; list-style-position: outside; padding: 1rem 1.1rem; }}
.record-details[open] > summary {{ border-bottom: 1px solid #ddd; }}
.summary-title {{ display: block; font-weight: 700; line-height: 1.25; }}
.summary-meta {{ display: block; margin-top: .25rem; color: #666; font-size: .85rem; }}
.record-body {{ padding: 0 1.1rem 1.1rem; }}
.source-row {{ margin: .85rem 0; }}
h2, h3 {{ line-height: 1.25; }} h3 {{ margin: 1.1rem 0 .35rem; font-size: 1rem; }}
.source-text {{ white-space: pre-wrap; line-height: 1.55; border-left: 3px solid #999; padding-left: .8rem; }}
.muted, .field-note {{ color: #666; }} .field-note {{ font-size: .88rem; }}
.annotations {{ display: none; margin: .8rem 0; padding: .65rem .75rem; border: 1px dashed #999; background: #fafafa; }}
.show-annotations .annotations {{ display: block; }}
.annotation-label {{ margin: 0 0 .45rem; font-size: .8rem; font-weight: 650; }}
.annotation-match {{ margin: .5rem 0; padding: .45rem .6rem; background: #fff8db; font-size: .85rem; }}
.annotation-match.visible {{ display: block; }}
.tags {{ display: flex; flex-wrap: wrap; gap: .4rem; }}
.tag {{ border: 1px solid #999; border-radius: 999px; padding: .2rem .55rem; font-size: .78rem; }}
.token-list {{ padding-left: 1.25rem; }} .token-kind {{ font-weight: 650; }} .token-note {{ color: #666; font-size: .8rem; }}
.evidence-details {{ margin-top: .8rem; }}
dl {{ display: grid; grid-template-columns: max-content 1fr; gap: .35rem .8rem; }} dt {{ font-weight: 650; }} dd {{ margin: 0; min-width: 0; overflow-wrap: anywhere; }}
.ceiling {{ margin-top: 1rem; padding: .75rem; background: #f3f3f3; font-size: .85rem; }}
.hidden {{ display: none !important; }} code {{ overflow-wrap: anywhere; }}
@media (max-width: 650px) {{ .search-row, .advanced-grid {{ grid-template-columns: 1fr; }} .search-row button {{ width: 100%; }} dl {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<main>
<section class="hero">
<h1>ATRS Reader Lens</h1>
<p><strong>ATRS</strong> is the UK Algorithmic Transparency Recording Standard: public records describing algorithmic tools used by public bodies.</p>
<p><strong>Reader question:</strong> what does a published record actually say about review, challenge, correction, complaint, clarification or help?</p>
<p>This lens reorganises frozen public evidence. It is not legal advice, a transparency score, a compliance finding, or a claim about undisclosed practice.</p>
<p><strong>{len(rows)}</strong> frozen records. Optional evidence-bound exploratory annotations exist for <strong>{annotated}</strong> records and are off by default.</p>
<ul>{ceilings}</ul>
</section>

<section class="controls" aria-labelledby="find-heading">
<h2 id="find-heading">Find a record</h2>
<div class="search-row">
  <div class="field">
    <label for="q">Search tool, organisation or published text</label>
    <input id="q" type="search" autocomplete="off">
  </div>
  <button id="reset" type="button">Reset</button>
</div>
<details class="advanced">
  <summary>Advanced evidence filters</summary>
  <div class="advanced-grid">
    <div class="field">
      <label for="appeals">Published Appeals and review field</label>
      <select id="appeals"><option value="">Any</option><option value="yes">Observed on frozen page</option><option value="no">Not observed on frozen page</option></select>
    </div>
    <div class="field">
      <label for="contact">Published link/contact-like token in that field</label>
      <select id="contact"><option value="">Any</option><option value="yes">Observed</option><option value="no">Not observed</option></select>
    </div>
  </div>
  <label class="annotation-toggle"><input id="annotations" type="checkbox"> Include exploratory annotations in search and show them on cards</label>
</details>
<p id="count" class="results-status" role="status" aria-live="polite"></p>
<p id="no-results" class="no-results hidden">No records match these filters. <button id="reset-empty" type="button">Clear filters</button></p>
</section>
<section id="cards">{cards}</section>
</main>
<script>
const q = document.getElementById('q');
const appeals = document.getElementById('appeals');
const contact = document.getElementById('contact');
const annotations = document.getElementById('annotations');
const reset = document.getElementById('reset');
const resetEmpty = document.getElementById('reset-empty');
const cards = [...document.querySelectorAll('.card')];
const count = document.getElementById('count');
const noResults = document.getElementById('no-results');

function apply() {{
  const needle = q.value.trim().toLowerCase();
  let shown = 0;
  for (const card of cards) {{
    const sourceMatch = !needle || card.dataset.sourceSearch.includes(needle);
    const annotationMatch = annotations.checked && needle && card.dataset.annotationSearch.includes(needle);
    const textMatch = sourceMatch || annotationMatch;
    const ok = textMatch &&
      (!appeals.value || card.dataset.appeals === appeals.value) &&
      (!contact.value || card.dataset.contact === contact.value);
    card.classList.toggle('hidden', !ok);
    const explanation = card.querySelector('.annotation-match');
    if (explanation) {{
      const visible = Boolean(ok && annotationMatch && !sourceMatch);
      explanation.classList.toggle('visible', visible);
      explanation.setAttribute('aria-hidden', visible ? 'false' : 'true');
    }}
    if (ok) shown++;
  }}
  document.body.classList.toggle('show-annotations', annotations.checked);
  count.textContent = `${{shown}} of ${{cards.length}} records shown.`;
  noResults.classList.toggle('hidden', shown !== 0);
}}

function clearAll() {{
  q.value = '';
  appeals.value = '';
  contact.value = '';
  annotations.checked = false;
  apply();
  q.focus();
}}

for (const el of [q, appeals, contact, annotations]) el.addEventListener('input', apply);
reset.addEventListener('click', clearAll);
resetEmpty.addEventListener('click', clearAll);
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
