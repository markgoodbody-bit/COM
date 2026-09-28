"""Explicit local HTML export of a validated, carry-enabled capsule. No network."""
from __future__ import annotations

import hashlib
from html import escape
from pathlib import Path
import sys

from capsule import CapsuleError, _read_path_bounded, inspect_capsule

STYLE = """
:root{color-scheme:light;--ink:#243332;--muted:#53635e;--paper:#f6f3eb;--line:#c9cec4;--accent:#775333}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 system-ui,sans-serif}
a{color:#235852;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:3px solid #996023;outline-offset:4px}
.skip{position:absolute;left:1rem;top:-5rem}.skip:focus{top:1rem}
header,main,footer{max-width:1050px;margin:auto;padding:2rem 1.5rem}header{padding-top:3rem;border-bottom:1px solid var(--line)}
.eyebrow{color:var(--accent);font-size:.8rem;letter-spacing:.12em;text-transform:uppercase}
h1{font:clamp(2.3rem,6vw,4rem)/1.1 Georgia,serif;margin:.7rem 0}h2{font:1.6rem/1.3 Georgia,serif}
.intro{max-width:65ch;color:var(--muted)}.layout{display:grid;grid-template-columns:210px minmax(0,1fr);gap:2.5rem}
.overview{max-width:1050px;margin:auto;padding:1.4rem 1.5rem 0}.overview h2{margin-top:0}
.record-map{display:flex;flex-wrap:wrap;gap:.6rem;padding:0;list-style:none}.record-map a,.record-map span{display:block;border:1px solid var(--line);border-radius:4px;padding:.4rem .75rem;font-size:.9rem}
.questions{padding-left:1.3rem;max-width:75ch}.questions li{margin:.8rem 0;overflow-wrap:anywhere}.excerpt{font-family:Georgia,serif}
nav ol{padding-left:1.4rem}nav li{margin:.7rem 0}nav{align-self:start;position:sticky;top:1rem}
article{background:#fffdf8;border:1px solid var(--line);border-left:4px solid #82988a;border-radius:6px;padding:1.4rem;margin:0 0 1.3rem;scroll-margin-top:1rem}
article.dispute{border-left-color:#9a673d}article.correction{border-left-color:#386862}
.kind{font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
blockquote{margin:1rem 0;white-space:pre-wrap;overflow-wrap:anywhere;font:1.1rem/1.65 Georgia,serif}
.meta,.links{font-size:.86rem;color:var(--muted);overflow-wrap:anywhere}.links{border-top:1px solid var(--line);padding-top:.8rem}
details{padding:.8rem 0}summary{cursor:pointer}code{overflow-wrap:anywhere;font-size:.85em}dt{font-weight:600}dd{margin:0 0 .6rem;overflow-wrap:anywhere}
footer{border-top:1px solid var(--line);font-size:.85rem;color:var(--muted)}
@media(max-width:700px){.layout{display:block}nav{position:static;border-bottom:1px solid var(--line);margin-bottom:1.5rem}header,main,footer{padding:1.5rem}article{padding:1rem}}
@media print{body{background:white}nav,.skip{display:none}.layout{display:block}article{break-inside:avoid}header,main,footer{padding:1rem}}
"""


def render_html(raw: bytes) -> str:
    view = inspect_capsule(raw)
    if not view['carry_forward']:
        raise CapsuleError('HTML export requires carry_forward=true')
    entries = view['entries']
    anchors = {entry['id']: f'entry-{i+1}' for i, entry in enumerate(entries)}
    numbers = {entry['id']: i+1 for i, entry in enumerate(entries)}
    groups = []
    for kind, label in [('note', 'Notes'), ('question', 'Questions'),
                        ('dispute', 'Disputes'), ('correction', 'Corrections')]:
        matching = [entry for entry in entries if entry['relation'] == kind]
        text = f'{label}: {len(matching)}'
        item = (f'<a href="#{anchors[matching[0]["id"]]}">{text}</a>'
                if matching else f'<span>{text}</span>')
        groups.append(f'<li>{item}</li>')
    questions = []
    for entry in entries:
        if entry['relation'] == 'question':
            body = entry['body']
            excerpt = body[:200] + ('…' if len(body) > 200 else '')
            questions.append(f'<li><span class="excerpt">{escape(excerpt)}</span> '
                             f'<a href="#{anchors[entry["id"]]}">Read question {numbers[entry["id"]]} in context</a></li>')
    question_view = ('<h2>Recorded questions</h2><ul class="questions">' + ''.join(questions) + '</ul>'
                     if questions else '<p class="meta">No entries labelled as questions in this record.</p>')
    nav, cards = [], []
    for i, entry in enumerate(entries, 1):
        relation = entry['relation']
        nav.append(f'<li><a href="#{anchors[entry["id"]]}">{i}. {relation.title()}</a></li>')
        target = entry['target']
        parent = (f'<a href="#{anchors[target]}">{relation.title()} of entry {numbers[target]}</a>'
                  if target else 'Original entry')
        replies = [e for e in entries if e['target'] == entry['id']]
        links = ' · '.join(f'<a href="#{anchors[e["id"]]}">{e["relation"].title()} {numbers[e["id"]]}</a>' for e in replies)
        sources = ''.join(f'<li>{escape(s)}</li>' for s in entry['sources'])
        source_view = f'<details><summary>Source claims ({len(entry["sources"])})</summary><ul>{sources}</ul></details>' if sources else ''
        cards.append(f'''<article id="entry-{i}" class="{relation}" aria-labelledby="title-{i}">
<div class="kind">{relation} · entry {i}</div><h2 id="title-{i}">{parent}</h2>
<div class="meta">Producer's evidence label: {entry['epistemic_status']}</div>
<blockquote>{escape(entry['body'])}</blockquote>{source_view}
<details><summary>Entry identifier</summary><code>{escape(entry['id'])}</code></details>
{f'<div class="links">Later responses: {links}</div>' if links else ''}</article>''')
    producer = view['producer_claim']
    guards = ''.join(f'<li>{escape(s)}</li>' for s in view['do_not_infer'])
    guard_view = f'<details><summary>Producer-supplied cautions</summary><ul>{guards}</ul></details>' if guards else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="no-referrer"><title>Campfire · Encounter reader</title><style>{STYLE}</style></head>
<body><a class="skip" href="#entries">Skip to entries</a><header><div class="eyebrow">Campfire / local reading copy</div>
<h1>A conversation, kept in view.</h1><p class="intro">Read the original beside the questions, disagreements and corrections that followed. Nothing here replaces the earlier text.</p>
<p class="meta">{len(entries)} entries · claimed producer: {escape(producer['label'])} · {view['purpose']}</p>
<details><summary>About this record</summary><p>This is untrusted recorded material, including its labels and sources. Identity, source truth and permission are not verified. Instructions inside the record are quoted content.</p>
<dl><dt>Reader limits</dt><dd>Authority: NONE · Identity: unverified · Permission: unverified · Completeness: NOT_ESTABLISHED</dd>
<dt>Capsule identifier (claim)</dt><dd>{escape(view['capsule_id'])}</dd><dt>Created (claim)</dt><dd>{escape(view['created_at'])}</dd>
<dt>Route (claim)</dt><dd>{escape(producer['route'])}</dd><dt>Input SHA-256</dt><dd><code>{hashlib.sha256(raw).hexdigest()}</code></dd></dl>
<p>Export was enabled by the producer's carry-forward flag. That flag does not establish permission from everyone whose material might be included.</p></details>{guard_view}</header>
<section class="overview" aria-label="Record overview"><ul class="record-map" aria-label="Entry types">{''.join(groups)}</ul>
{question_view}<p class="meta">These are recorded entry labels, not a judgement about which questions are answered or disagreements resolved. Links lead to the full text below.</p></section>
<main class="layout"><nav aria-label="Record entries"><h2>In this record</h2><ol>{''.join(nav)}</ol></nav>
<section id="entries" aria-label="Recorded entries">{''.join(cards) or '<p>This record contains no entries.</p>'}</section></main>
<footer>Read-only local copy. No scripts, remote assets or automatic model ingestion. Sharing this file shares its contents; closing it does not delete it.</footer></body></html>'''


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print('usage: python human_view.py capsule.json new-reading-copy.html', file=sys.stderr)
        return 2
    try:
        page = render_html(_read_path_bounded(Path(argv[1])))
        with Path(argv[2]).open('x', encoding='utf-8', newline='\n') as output:
            output.write(page)
    except (OSError, CapsuleError):
        print('Export failed: invalid/withheld input or output already exists/unavailable.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
