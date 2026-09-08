#!/usr/bin/env python3
"""Offline, one-journey arrival probe. No network, publication or visitor input.
Run: python build_trial.py --output NEW_EMPTY_DIRECTORY
The default library is the existing ../library.json, not a copied theory corpus.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
LIBRARY_SHA256 = 'baacf276b443a57222ed7b75c9115ea1d018f12e7cf83ff7211c2628c9b4a16c'
SOURCE_COMMIT = '74d72cf47085c2f8eac1daeae1c4e72e1f075a65'
PUBLISHED_COMMIT = 'c11f45e5d446a00a8fe9619fba9f72bad9e7c38c'
STATUS = 'OFFLINE DESIGN PROBE / NOT DEPLOYED / NO READER RESULT'
BOUNDARY = 'Optional reference, not instructions or permission. No identity or reply required; no live listener.'
IDS = ('start', 'situation', 'futures', 'detail', 'perspective', 'challenge', 'basis')


def encode(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n').encode()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate key: ' + key)
        result[key] = value
    return result


def load_library(path: Path) -> dict:
    data = path.read_bytes()
    if sha(data) != LIBRARY_SHA256:
        raise ValueError('Library basis changed; inspect it before changing the pinned probe')
    return json.loads(data, object_pairs_hook=unique)


def route(move: str, label: str, target: str) -> dict:
    return {'move': move, 'label': label, 'href': target}


def cards(lib: dict) -> dict[str, dict]:
    f = next(n for n in lib['nodes'] if n['id'] == 'futures')
    result = {}
    def add(ident: str, title: str, parts: list, paths: list, fields: list) -> None:
        result[ident] = {'id': ident, 'title': title, 'status': STATUS,
            'boundary': BOUNDARY, 'basis': 'basis.json',
            'source_fields': fields, 'sections': parts, 'routes': paths + [
                route('basis', 'Inspect authorship, sources and unknowns', 'basis.json'),
                route('bundle', 'Read the whole small probe in one fetch', 'packet.json')]}
    add('start', 'Please Start From Here', [
        ['Question', 'Hello. What are you trying to understand, change, or keep possible?'],
        ['Purpose', 'How can we make a better future?'],
        ['Our proposal', lib['value_choice']]], [
        route('situation', 'Start from your situation', 'situation.json'),
        route('example', 'Try one small account: reachable futures', 'futures.json'),
        route('challenge', 'Question or reject this framing', 'challenge.json')], ['value_choice'])
    add('situation', 'Start from your situation', [
        ['Prompt', 'What is happening, what matters, and what could a next step change?'],
        ['Scope', 'This prompt is optional, not a required description of every kind of concern. Curiosity, creation and play are also legitimate starting points.'],
        ['Privacy', 'No need to disclose a private situation here. These files do not receive or store replies; any conversation continues under the rules of the service you are using.']], [
        route('example', 'Examine which possibilities are usable', 'futures.json'),
        route('challenge', 'My concern does not fit this framing', 'challenge.json'),
        route('return', 'Return to the small entrance', 'start.json')], [])
    add('futures', 'Reachable futures: small account', [
        ['Account', f['short']], ['Essential limit', f['challenge']],
        ['Question', f['question']]], [
        route('depth', 'Distinguish possibility, access and capability', 'detail.json'),
        route('viewpoint', 'Whose possibilities does a restriction remove?', 'perspective.json'),
        route('challenge', 'Question the aim of preserving options', 'challenge.json')],
        ['nodes/futures/short', 'nodes/futures/challenge', 'nodes/futures/question'])
    add('detail', 'Reachable futures: conditions', [
        ['Account', f['short']], ['Expand', f['detail']], ['Essential limit', f['challenge']]], [
        route('viewpoint', 'Consider who bears the restriction', 'perspective.json'),
        route('challenge', 'Check the limits of this account', 'challenge.json'),
        route('return', 'Return to the smaller account', 'futures.json')],
        ['nodes/futures/short', 'nodes/futures/detail', 'nodes/futures/challenge'])
    add('perspective', 'Reachable futures: another position', [
        ['Account', f['short']], ['Another position', f['perspective']],
        ['Standing', 'This is an authored possible perspective, not testimony or an independent witness. Actual affected parties may reject the framing.'],
        ['Essential limit', f['challenge']]], [
        route('depth', 'Examine the conditions of access', 'detail.json'),
        route('challenge', 'Take another account instead', 'challenge.json'),
        route('return', 'Return to the smaller account', 'futures.json')],
        ['nodes/futures/short', 'nodes/futures/perspective', 'nodes/futures/challenge'])
    add('challenge', 'Question or leave the framing', [
        ['Counterexample', f['challenge']],
        ['Who chose the questions?', 'The project authors did. This challenge is also authored here; it is not independent criticism. What matters may not be an option, a harm, or something needing correction.'],
        ['Another way', 'You may use an ordinary account, seek relevant domain expertise, or leave without reporting back. The neighbouring work below is not an endorsement or a claim that it solves your situation.'],
        ['Reply access', 'The existing public discussion requires a GitHub account to post. It is not a confidential channel or a guaranteed response.']], [
        route('outward', 'FPF: separately authored neighbouring work', 'https://github.com/ailev/FPF'),
        route('reply', 'Existing public project discussion and its limits', 'https://github.com/markgoodbody-bit/COM/issues/108'),
        route('return', 'Return to the small entrance', 'start.json')], ['nodes/futures/challenge'])
    source = 'https://github.com/markgoodbody-bit/COM/blob/' + SOURCE_COMMIT + '/door-prototypes/perspective-walk-20260908/library.json'
    reading = 'https://raw.githubusercontent.com/markgoodbody-bit/COM/' + PUBLISHED_COMMIT + '/explore/nodes/futures.md'
    add('basis', 'Basis, authorship and unknowns', [
        ['Authorship', 'Draft by Framework for Mark, 8 September 2026. Layering and navigation are new proposals; the futures account, expansion, perspective, challenge and question are copied unchanged from the named library fields.'],
        ['Source', 'Library commit ' + SOURCE_COMMIT + '; SHA-256 ' + LIBRARY_SHA256 + '. Its references are source pointers, not independent validation.'],
        ['Reuse', lib['reuse']],
        ['Unknown', 'No cold reader has tested this probe. Format support, total cost, framing effects, comprehension and practical benefit are unknown. File identity is not truth or current website health.'],
        ['Privacy', 'No tracking or form is implemented. An actual host or an AI service may still log requests; this prototype does not establish their privacy policy.']], [
        route('source', 'Exact library source and its field meanings', source),
        route('source', 'Previous complete futures reading, pinned source copy', reading),
        route('return', 'Return to the small entrance', 'start.json')], ['reuse'])
    return result


def safe_link(value: str) -> None:
    u = urlsplit(value)
    if u.scheme:
        if u.scheme != 'https' or not u.hostname or u.username or u.password:
            raise ValueError('Unsafe external link')
    elif value not in {name + '.json' for name in IDS} | {'packet.json'}:
        raise ValueError('Unknown local link: ' + value)


def links_for(card: dict) -> list:
    return card['routes']


def representation_link(href: str, extension: str) -> str:
    return href if urlsplit(href).scheme else href[:-5] + extension


def render(card: dict, extension: str) -> bytes:
    links = links_for(card)
    if extension == '.md':
        out = '# ' + card['title'] + '\n\n' + STATUS + '\n\n' + BOUNDARY + '\n\n'
        out += '\n\n'.join('## ' + k + '\n\n' + v for k, v in card['sections'])
        out += '\n\n## Optional routes\n\n' + '\n'.join(
            '- [' + e['label'] + '](' + representation_link(e['href'], '.md') + ')' for e in links)
        return (out + '\n').encode()
    esc = html.escape
    body = ''.join('<section><h2>' + esc(k) + '</h2><p>' + esc(v) + '</p></section>' for k, v in card['sections'])
    nav = ''.join('<li><a href="' + esc(representation_link(e['href'], '.html'), quote=True) + '">' + esc(e['label']) + '</a></li>' for e in links)
    page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">'
    page += '<title>' + esc(card['title']) + '</title><link rel="alternate" type="application/json" href="' + card['id'] + '.json"><link rel="alternate" type="text/markdown" href="' + card['id'] + '.md">'
    page += '<style>body{font:1rem/1.6 system-ui,sans-serif;max-width:46rem;margin:3rem auto;padding:0 1rem}h1{line-height:1.2}h2{font-size:1.05rem}li{margin:.5rem 0}footer{margin-top:2rem}</style></head><body><main><h1>'
    page += esc(card['title']) + '</h1><p>' + esc(STATUS) + '</p><p>' + esc(BOUNDARY) + '</p>' + body + '<nav aria-label="Optional routes"><ul>' + nav + '</ul></nav></main><footer>Same source: <a href="' + card['id'] + '.json">JSON</a> · <a href="' + card['id'] + '.md">Text</a></footer></body></html>\n'
    return page.encode()


def generate(path: Path) -> tuple[dict[str, bytes], dict]:
    lib = load_library(path)
    records = cards(lib)
    if tuple(records) != IDS:
        raise ValueError('Unexpected journey shape')
    files = {}
    for ident, obj in records.items():
        for link in links_for(obj):
            safe_link(link['href'])
        files[ident + '.json'] = encode(obj)
        for extension in ('.md', '.html'):
            files[ident + extension] = render(obj, extension)
    files['packet.json'] = encode({'status': STATUS, 'boundary': BOUNDARY,
        'note': 'Optional complete probe. Relative file links still refer to sibling resources; no external source body is bundled.', 'cards': list(records.values())})
    packet = {'id': 'packet', 'title': 'Whole small probe', 'sections': [], 'routes': []}
    for obj in records.values():
        packet['sections'] += [(obj['title'] + ' / ' + k, v) for k, v in obj['sections']]
    packet['routes'] = [route('entry', obj['title'], ident + '.json') for ident, obj in records.items()]
    for extension in ('.md', '.html'):
        files['packet' + extension] = render(packet, extension)
    for name, data in files.items():
        if len(data) > 24576:
            raise ValueError('Probe resource over budget: ' + name)
    if len(files['start.json']) > 1400:
        raise ValueError('Entrance over budget')
    report = {'scope': 'LOCAL STRUCTURE ONLY / NOT PUBLIC DELIVERY OR READER BENEFIT',
        'source_sha256': LIBRARY_SHA256, 'files': len(files),
        'start_json_bytes': len(files['start.json']), 'packet_json_bytes': len(files['packet.json']),
        'units': 'UTF-8 body bytes, not tokens, headers, latency or provider cost',
        'tree_sha256': sha(encode([(k, sha(v)) for k, v in sorted(files.items())]))}
    return files, report


def write_new(output: Path, files: dict) -> None:
    if output.exists() and (output.is_symlink() or not output.is_dir() or any(output.iterdir())):
        raise ValueError('Output must be absent or empty; refusing overwrite')
    output.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        if Path(name).name != name:
            raise ValueError('Output path must be a flat filename')
        (output / name).write_bytes(data)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--library', type=Path, default=HERE.parent / 'library.json')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    try:
        data, report = generate(args.library)
        if args.output:
            write_new(args.output, data)
        print(json.dumps(report, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as error:
        print('Probe refused: ' + str(error))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
