#!/usr/bin/env python3
"""Optional source-only TRACE-inspired human case card (not TRACE canon).

Usage: python3 case_card.py case.json --output case.html
       python3 case_card.py - > case.html  # stdout, use care with shell redirection

Reads an author-supplied local JSON file; emits inert, escaped HTML. The author's
labels are not authenticated, and the tool makes no real-world classification.
"""

import argparse
import html
import json
import os
import sys
import tempfile
from pathlib import Path

MAX_BYTES = 131_072
MAX_FIELD = 2_000
MAX_ROWS = 24
EVIDENCE = {"observed", "reported", "inferred", "disputed", "unknown"}
STAGES = {"possible", "offered", "permitted", "chosen", "attempted", "executed"}
WINDOWS = {"unknown", "not_assessed", "open", "closed"}
KIND = {"baseline", "change", "consequence"}
FORBIDDEN_FORMAT = set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A)) | {0x200E, 0x200F, 0x061C}


class CaseError(ValueError):
    """Malformed input, without echoing private input values into errors."""


def _duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise CaseError("duplicate JSON key")
        obj[key] = value
    return obj


def _bad_constant(_value):
    raise CaseError("non-finite JSON values are unsupported")


def parse_case(raw):
    if not isinstance(raw, str):
        raise CaseError("input must be UTF-8 text")
    try:
        if len(raw.encode("utf-8")) > MAX_BYTES:
            raise CaseError("input exceeds 128 KiB limit")
        data = json.loads(raw, object_pairs_hook=_duplicate_keys, parse_constant=_bad_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise CaseError("invalid UTF-8/JSON input") from exc
    validate_case(data)
    return data


def _object(value, allowed, label):
    if not isinstance(value, dict):
        raise CaseError(label + " must be an object")
    extras = set(value) - set(allowed)
    if extras:
        raise CaseError(label + " has unexpected keys")
    if not all(isinstance(k, str) for k in value):
        raise CaseError(label + " keys must be strings")
    return value


def _string(obj, key, label, required=False, limit=MAX_FIELD):
    if key not in obj:
        if required:
            raise CaseError(label + "." + key + " is required")
        return None
    value = obj[key]
    if not isinstance(value, str) or not value.strip():
        raise CaseError(label + "." + key + " must be nonempty text")
    if len(value) > limit:
        raise CaseError(label + "." + key + " is too long")
    if any(ord(ch) in FORBIDDEN_FORMAT for ch in value):
        raise CaseError(label + "." + key + " contains a directional format control")
    if any(ord(ch) < 0x20 and ch not in "\n\t" for ch in value):
        raise CaseError(label + "." + key + " contains a control character")
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
        raise CaseError(label + "." + key + " has an invalid Unicode surrogate")
    return value


def _enum(obj, key, choices, label, required=True):
    value = _string(obj, key, label, required=required, limit=40)
    if value is not None and value not in choices:
        raise CaseError(label + "." + key + " has an unsupported value")
    return value


def _rows(data, key, allowed, required, fields, label):
    if key not in data:
        if required:
            raise CaseError(key + " is required")
        return []
    value = data[key]
    if not isinstance(value, list) or len(value) > MAX_ROWS or (required and not value):
        raise CaseError(key + " must be a bounded list")
    for row in value:
        _object(row, allowed, label)
        for field, is_required, limit in fields:
            _string(row, field, label, is_required, limit)
    return value


def validate_case(data):
    _object(data, {"title", "scope", "claims", "parties", "possibilities", "correction", "return"}, "case")
    _string(data, "title", "case", True, 180)
    _string(data, "scope", "case", False, 500)
    claims = _rows(data, "claims", {"kind", "text", "evidence", "source"}, True,
                   [("kind", True, 40), ("text", True, MAX_FIELD), ("evidence", True, 40), ("source", False, 500)], "claim")
    for claim in claims:
        _enum(claim, "kind", KIND, "claim")
        _enum(claim, "evidence", EVIDENCE, "claim")
    if not any(x["kind"] == "change" for x in claims):
        raise CaseError("a change claim is required; use evidence=unknown if unsettled")
    _rows(data, "parties", {"name", "aim", "boundary"}, False,
          [("name", True, 150), ("aim", False, 500), ("boundary", False, 500)], "party")
    routes = _rows(data, "possibilities", {"party", "description", "state", "condition"}, False,
                   [("party", True, 150), ("description", True, 1000), ("state", True, 40), ("condition", False, 500)], "possibility")
    for route in routes:
        _enum(route, "state", STAGES, "possibility")
    if "correction" in data:
        c = _object(data["correction"], {"target", "route", "hardening", "clock_basis", "window", "basis"}, "correction")
        for k in ("target", "route", "hardening", "clock_basis", "basis"):
            _string(c, k, "correction", False, 500)
        w = _enum(c, "window", WINDOWS, "correction", False)
        if w in {"open", "closed"} and not all(c.get(k) for k in ("target", "route", "hardening", "clock_basis", "basis")):
            raise CaseError("open/closed correction window requires target, route, hardening, clock_basis and basis")
    if "return" in data:
        r = _object(data["return"], {"learned", "unresolved", "next"}, "return")
        for k in ("learned", "unresolved", "next"):
            _string(r, k, "return", False, 1000)
    try:
        if len(json.dumps(data, ensure_ascii=False).encode("utf-8")) > MAX_BYTES:
            raise CaseError("case exceeds 128 KiB limit")
    except (UnicodeError, RecursionError) as exc:
        raise CaseError("input has invalid Unicode or nesting") from exc


def _h(value):
    return html.escape(value, quote=True)


def _show(value, missing="Not supplied"):
    return _h(value) if value is not None else '<span class="missing">' + missing + '</span>'


def _field(label, value, missing="Not supplied"):
    return '<div class="field"><b>' + label + ':</b> <span class="written">' + _show(value, missing) + '</span></div>'


def build_card(data):
    """Render deterministic, static HTML. All case data is displayed as untrusted text."""
    validate_case(data)
    claims = []
    for claim in data["claims"]:
        claims.append('<li><span class="chip">' + claim["kind"].title() + '</span> '
                      + '<span class="chip evidence">' + claim["evidence"] + ' · user label</span>'
                      + '<p class="written">' + _h(claim["text"]) + '</p>'
                      + _field("Source", claim.get("source"), "Source not supplied")
                      + '</li>')
    if "parties" in data and data["parties"]:
        parties = ''.join('<li><b class="written">' + _h(p["name"]) + '</b>' + _field('Aim', p.get('aim'))
                          + _field('Boundary', p.get('boundary')) + '</li>' for p in data['parties'])
    else:
        parties = '<p class="missing">No affected parties supplied; this does not establish absence.</p>'
    stages = {
        "possible": "Possible · not permission or execution",
        "offered": "Offered · not accepted or executed",
        "permitted": "Permitted · not chosen or executed",
        "chosen": "Chosen · not necessarily attempted",
        "attempted": "Attempted · not proven completed",
        "executed": "Executed · submitted claim, effects unverified",
    }
    if data.get('possibilities'):
        routes = ''.join('<li><b class="written">' + _h(p['party']) + '</b>'
                         + ' <span class="chip">' + stages[p['state']] + '</span>'
                         + '<p class="written">' + _h(p['description']) + '</p>'
                         + _field('Condition', p.get('condition')) + '</li>' for p in data['possibilities'])
    else:
        routes = '<p class="missing">No alternatives supplied; this does not establish that none exists.</p>'
    c = data.get('correction')
    if c is None:
        correction = '<p class="missing">Correction window not assessed or supplied.</p>'
    else:
        w = c.get('window', 'not_assessed')
        status = 'Window: ' + (w + ' (submitted claim; unverified)' if w in ('open', 'closed') else
                               'unknown (submitted claim)' if w == 'unknown' else 'not assessed (not supplied)')
        correction = '<p><b>' + status + '</b></p>' + ''.join(
            _field(title, c.get(key)) for key, title in
            [('target', 'Target'), ('route', 'Proposed route'), ('hardening', 'Hardening boundary'),
             ('clock_basis', 'Clock basis'), ('basis', 'Claim basis')])
        if w in ('open', 'closed'):
            correction += '<p class="caution">Clock/completion assumptions remain unverified. Use a specialist method for real deadlines.</p>'
    ret = data.get('return', {})
    returns = ''.join(_field(k, ret.get(field)) for k, field in
                      [('Learned', 'learned'), ('Unresolved', 'unresolved'), ('Next question / route', 'next')])
    return '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Case card — ''' + _h(data['title']) + '''</title>
<style>
:root{color-scheme:light;--ink:#202b37;--line:#d7e0e9;--quiet:#4c5a68;--tint:#f3f6f9}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:860px;margin:auto;padding:2rem 1.2rem 3rem}header{border-bottom:2px solid var(--ink);padding-bottom:1rem}
h1{font-size:clamp(1.5rem,3.5vw,2.1rem);line-height:1.2;overflow-wrap:anywhere}
h2{font-size:1.1rem;margin:0 0 .65rem}section{margin:1.3rem 0;padding:1.1rem 1.2rem;border:1px solid var(--line);border-radius:10px}
.subtitle,.caution{color:var(--quiet)}.caution{font-size:.92rem}.missing{font-style:italic;color:var(--quiet)}
ul{list-style:none;padding:0;margin:0}li{border-top:1px solid var(--line);padding:.8rem 0}li:first-child{border:0}
p{margin:.5rem 0}.chip{display:inline-block;font-size:.79rem;padding:.1rem .4rem;border-radius:4px;background:var(--tint);margin-right:.3rem}
.evidence{border:1px solid var(--line)}.field{margin:.25rem 0}.written{white-space:pre-wrap;overflow-wrap:anywhere;unicode-bidi:plaintext}
footer{font-size:.85rem;color:var(--quiet)}footer a{color:inherit}
@media print{main{max-width:none;padding:0}section{break-inside:avoid}body{font-size:11pt}a{color:var(--ink)}}
</style></head><body><main>
<header><div class="subtitle">Optional human case card · author-supplied claims</div><h1 class="written">''' + _h(data['title']) + '''</h1>
''' + _field('Scope', data.get('scope')) + '''
<p class="caution">Not independently verified. User labels are not proof of events, sources, independence, authorization, completion or outcomes.</p></header>
<section><h2>What changed, according to the supplied record?</h2><ul>''' + ''.join(claims) + '''</ul></section>
<section><h2>Who has aims or boundaries?</h2><ul>''' + parties + '''</ul></section>
<section><h2>What could become possible?</h2><ul>''' + routes + '''</ul></section>
<section><h2>What could still be corrected?</h2>''' + correction + '''</section>
<section><h2>Return: what remains to learn or do?</h2>''' + returns + '''</section>
<footer>Independent experimental worksheet, not a TRACE implementation, endorsement, fact-checker, risk score or scheduling proof. A blank field is not evidence of absence. If a normal incident record or specialist method is simpler, use it. Inspired by the <a href="https://github.com/markgoodbody-bit/TRACE/blob/v0.5.0/TRACE-v0.5.md" rel="noopener noreferrer">TRACE v0.5 research specification</a>; no general licence or canon change implied. HTML contains no scripts, external assets, network calls or telemetry.</footer>
</main></body></html>\n'''


def _read_bytes(source):
    if source == '-':
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
    else:
        with open(source, 'rb') as f:
            raw = f.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise CaseError('input exceeds 128 KiB limit')
    try:
        return raw.decode('utf-8')
    except UnicodeError as exc:
        raise CaseError('input must be UTF-8') from exc


def _write_atomic(dest, content):
    dest = Path(dest)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n', dir=str(dest.parent),
                                         prefix='.case-card-', suffix='.tmp', delete=False) as f:
            tmp = f.name
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, dest)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.unlink(tmp)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Render a local, self-contained, non-authoritative case card')
    parser.add_argument('input', nargs='?', default='-', help='JSON path or - for stdin')
    parser.add_argument('--output', '-o', help='HTML path (atomic replacement after validation; default stdout)')
    args = parser.parse_args(argv)
    try:
        if args.output and args.input != '-' and Path(args.output).resolve() == Path(args.input).resolve():
            raise CaseError('input and output paths must differ')
        rendered = build_card(parse_case(_read_bytes(args.input)))
        if args.output:
            _write_atomic(args.output, rendered)
        else:
            sys.stdout.write(rendered)
        return 0
    except (CaseError, OSError, UnicodeError) as exc:
        print('case-card: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
