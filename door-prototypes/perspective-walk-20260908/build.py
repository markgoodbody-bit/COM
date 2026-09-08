#!/usr/bin/env python3
"""Build an additive /explore/ surface. Standard library only; no network or publishing.

Run: python build.py --output /path/to/EMPTY-staging-directory
The output root is only staging. Copy its explore/ child through the maintained
website build, never this source directory or the whole COM branch.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
BASE = 'https://pleasestartfromhere.com/explore/'
EXAMPLES = ('entry', 'case', 'route', 'affected', 'challenge')
STATUS = 'WORKING EXPERIMENT / NOT CANON / NO EFFICACY RESULT'


def encode(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')


def unique_pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)
    if not isinstance(value, dict):
        raise ValueError(f'Expected object: {path.name}')
    return value


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def external_url(value: str) -> None:
    u = urlsplit(value)
    if u.scheme != 'https' or not u.hostname or u.username or u.password:
        raise ValueError('External references must be public HTTPS URLs without credentials')


def load(source: Path) -> tuple[dict, dict]:
    library = read_json(source / 'library.json')
    if library.get('format') != 'psfh-reading-library/0.2':
        raise ValueError('Unsupported library format')
    nodes = library['nodes']
    ids = [n['id'] for n in nodes]
    if len(set(ids)) != len(ids) or not 1 <= len(ids) <= 32:
        raise ValueError('Node IDs must be unique; this bounded build allows 1–32 nodes')
    fields = ('id', 'title', 'short', 'detail', 'perspective', 'challenge', 'question', 'kind')
    for n in nodes:
        if not re.fullmatch(r'[a-z][a-z0-9-]*', n['id']):
            raise ValueError('Unsafe node ID')
        if any(not isinstance(n.get(k), str) or not n[k].strip() for k in fields):
            raise ValueError(f'Missing reading field: {n["id"]}')
        if len(encode(n)) > 3000:
            raise ValueError(f'Node too large: {n["id"]}')
        if not n['sources'] or any(s not in library['sources'] for s in n['sources']):
            raise ValueError('Unknown or missing source reference')
        for edge in n['next']:
            if edge['target'] not in ids or not edge['relation'].strip():
                raise ValueError('Unresolved or unlabelled graph edge')
    for src in library['sources'].values():
        external_url(src['url'])
        external_url(src['raw_url'])
        if not re.fullmatch(r'[0-9a-f]{40}', src['commit']):
            raise ValueError('Source commit must be explicit')
        if any('/' + src['commit'] + '/' not in src[k] for k in ('url', 'raw_url')):
            raise ValueError('Source URL does not bind its stated commit')
    for item in library['neighbours']:
        external_url(item['url'])
    external_url(library['challenge_route']['url'])
    examples = {name: read_json(source / f'{name}.json') for name in EXAMPLES}
    expected = [
        {'id': 'F1', 'text': 'An appeal route formally exists.'},
        {'id': 'F2', 'text': 'The decision being appealed takes effect before the appeal can be heard.'},
    ]
    if examples['case']['facts'] != expected:
        raise ValueError('The reviewed shared case changed; review it before regenerating')
    for name, example in examples.items():
        if example['id'] != name:
            raise ValueError('Example identity mismatch')
        if name in ('route', 'affected', 'challenge') and example['supported_by'] != ['F1', 'F2']:
            raise ValueError('A lens lost its shared-fact references')
        for link in example['next']:
            if 'path' in link and link['path'] not in [x + '.json' for x in EXAMPLES]:
                raise ValueError('Unresolved example link')
            if 'url' in link:
                external_url(link['url'])
    return library, examples


def document(title: str, parts: list[tuple[str, str]], links: list[tuple[str, str]]) -> str:
    text = '# ' + title + '\n\n' + '\n\n'.join('## ' + k + '\n\n' + v for k, v in parts)
    if links:
        text += '\n\n## Routes\n\n' + '\n'.join(f'- [{label}]({url})' for label, url in links)
    return text + '\n'


def html_document(title: str, parts: list[tuple[str, str]], links: list[tuple[str, str]], alternate: str, describedby: str) -> str:
    esc = html.escape
    sections = ''.join(f'<section><h2>{esc(k)}</h2><p>{esc(v).replace(chr(10), "<br>")}</p></section>' for k, v in parts)
    nav = ''.join(f'<li><a href="{esc(url, quote=True)}">{esc(label)}</a></li>' for label, url in links)
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex,nofollow">'
            f'<title>{esc(title)} · Please Start From Here</title>'
            f'<link rel="alternate" type="text/markdown" href="{esc(alternate, quote=True)}">'
            f'<link rel="describedby" href="{esc(describedby, quote=True)}">'
            '<style>html{color-scheme:light dark}body{font:1rem/1.6 system-ui,sans-serif;'
            'max-width:48rem;margin:3rem auto;padding:0 1.2rem}h1{line-height:1.15}'
            'h2{font-size:1.05rem;margin-top:1.8rem}p{white-space:normal}li{margin:.45rem 0}'
            'footer{border-top:1px solid;padding-top:1rem;margin-top:2rem;font-size:.85rem}</style>'
            f'</head><body><main><h1>{esc(title)}</h1>{sections}<nav aria-label="Optional routes"><ul>{nav}</ul></nav>'
            f'</main><footer>{esc(STATUS)}. Same source as the machine representations. '
            'No sign-in, personal disclosure or report-back is needed.</footer></body></html>\n')


def generate(source: Path = HERE) -> tuple[dict[str, bytes], dict]:
    lib, examples = load(source)
    files: dict[str, bytes] = {}
    def put(path: str, value: str | bytes) -> None:
        if path.startswith('/') or '..' in Path(path).parts or 'explore/' + path in files:
            raise ValueError('Unsafe or duplicate output path')
        files['explore/' + path] = value if isinstance(value, bytes) else value.encode('utf-8')
    title = lib['title'] + ' — explore'
    overview = [('Purpose', lib['purpose']), ('A small beginning', lib['orientation']),
                ('Choice', lib['reading']), ('Boundary', lib['boundary']),
                ('Our value choice', lib['value_choice'])]
    entry_links = [(n['title'], 'nodes/' + n['id'] + '.md') for n in lib['nodes']]
    entry_links += [('One case, several viewpoints', 'example/entry.md'),
                    ('Source identities and limits', 'sources.md'), ('Criticism and reply access', 'challenge.md'),
                    ('Machine map with resource sizes', 'map.json'), ('Optional complete local packet', 'packet.md')]
    put('index.md', document(title, overview, entry_links))
    put('index.txt', files['explore/index.md'])
    put('index.html', html_document(title, overview,
        [(label, url[:-3] + '.html' if url.endswith('.md') and url != 'packet.md' else url) for label, url in entry_links], 'index.md', 'llms.txt'))
    node_index = []
    for n in lib['nodes']:
        ident = n['id']
        node_obj = dict(n, status=STATUS, boundary=lib['boundary'])
        node_obj['next'] = [dict(e, path=e['target'] + '.json') for e in n['next']]
        node_obj['routes'] = {'map': '../map.json', 'sources': '../sources.json', 'challenge_access': '../challenge.md', 'example': '../example/entry.json'}
        node_obj['source_pointers'] = {k: lib['sources'][k] for k in n['sources']}
        put('nodes/' + ident + '.json', encode(node_obj))
        parts = [('Small account', n['short']), ('Expand', n['detail']), ('Another position', n['perspective']),
                 ('Challenge', n['challenge']), ('Open question', n['question']), ('Status', n['kind'] + '. ' + lib['boundary'])]
        links = [(e['relation'].replace('_', ' '), e['target'] + '.md') for e in n['next']]
        links += [(lib['sources'][s]['label'], lib['sources'][s]['url']) for s in n['sources']]
        links += [('Source terms and snapshots', '../sources.md'), ('Same facts, different views', '../example/entry.md'), ('Return or stop', '../index.md')]
        put('nodes/' + ident + '.md', document(n['title'], parts, links))
        put('nodes/' + ident + '.html', html_document(n['title'], parts,
            [(a, b[:-3] + '.html' if b.endswith('.md') and not b.startswith('https:') else b) for a, b in links], ident + '.md', '../llms.txt'))
        node_index.append({'id':ident, 'title':n['title'], 'short':n['short'], 'json':'nodes/' + ident + '.json', 'text':'nodes/' + ident + '.md'})
    for name, obj in examples.items():
        derived = copy.deepcopy(obj)
        derived['status'] = 'WORKING ILLUSTRATION / NOT FIELD EVIDENCE / NO RECEIVER RESULT'
        derived['rendering_note'] = 'Generated from PR114 source. Shared F1/F2 facts unchanged; presentation status updated for optional serving.'
        put('example/' + name + '.json', encode(derived))
        parts = [(k.replace('_', ' ').capitalize(), v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, indent=2))
                 for k, v in derived.items() if k not in ('next', 'id', 'format')]
        links = [(e['relation'].replace('_', ' '), e['path'].replace('.json','.md')) for e in obj['next'] if 'path' in e]
        links += [(e['relation'],e['url']) for e in obj['next'] if 'url' in e]
        links += [('Reading-space entry or stop', '../index.md')]
        put('example/' + name + '.md', document('Appeal example — ' + name, parts, links))
        put('example/' + name + '.html', html_document('Appeal example — ' + name, parts,
            [(a, b[:-3] + '.html' if b.endswith('.md') and not b.startswith('https:') else b) for a, b in links], name + '.md', '../llms.txt'))
    sources = {'status':STATUS,'relation':lib['source_relation'],'sources':lib['sources'],'neighbours':lib['neighbours'],'reuse':lib['reuse']}
    put('sources.json', encode(sources))
    src_parts = [('Relation to these sources', lib['source_relation']), ('Reuse', lib['reuse']), ('Boundary', lib['provenance'])]
    src_links = [(s['label'],s['url']) for s in lib['sources'].values()] + [(s['label'] + ' — raw text',s['raw_url']) for s in lib['sources'].values()]
    src_links += [(n['label'],n['url']) for n in lib['neighbours']] + [('Return', 'index.md')]
    put('sources.md', document('Sources and neighbouring work', src_parts, src_links))
    put('sources.html', html_document('Sources and neighbouring work', src_parts, src_links[:-1] + [('Return','index.html')], 'sources.md','llms.txt'))
    cparts = [('Challenge the content', 'These accounts can omit people, infer too much or steer the reader. A different account may serve better. A challenge need not be expressed in this project\'s vocabulary.'),
              ('Actual reply route', lib['challenge_route']['access']), ('Limits', 'A public issue link is not evidence of timely reply or practical remedy. This static site does not host a conversation, accept submissions, store visitor identity or run agent tools.')]
    clinks = [('Project discussion',lib['challenge_route']['url']),('Sources and alternatives','sources.md'),('Return or stop','index.md')]
    put('challenge.md', document('Challenge or leave', cparts, clinks))
    put('challenge.html', html_document('Challenge or leave', cparts, [(a,b.replace('.md','.html') if not b.startswith('https:') else b) for a,b in clinks], 'challenge.md','llms.txt'))
    packet = dict(lib, status=STATUS, examples=examples,
                  packet_boundary='Optional full local carrier. No external TRACE/ME text is bundled; source pointers only. Do not fetch the full packet unless it is useful.')
    put('packet.json', encode(packet))
    packet_text = document(title + ' — optional full packet', overview, [])
    for n in lib['nodes']:
        packet_text += '\n' + document(n['title'], [('Small account',n['short']),('Expand',n['detail']),('Another position',n['perspective']),('Challenge',n['challenge']),('Open question',n['question']),('Kind',n['kind'])], [])
    packet_text += '\n# Shared example data\n\n```json\n' + json.dumps(examples,ensure_ascii=False,indent=2) + '\n```\n'
    packet_text += '\n' + document('Sources, limits and reply access',src_parts + [('Reply access',lib['challenge_route']['access'])],src_links)
    put('packet.md',packet_text)
    llms = '# Please Start From Here — experimental reading space\n\n> ' + lib['purpose'] + '\n\n' + lib['boundary'] + '\n\nThis is a bounded static extension, not a required course or agent service. The full packet is optional.\n\n## Entry\n\n- [Small beginning](' + BASE + 'index.md): orientation without a required identity\n- [Machine map](' + BASE + 'map.json): individual resources and byte sizes\n\n## Patterns\n\n'
    llms += '\n'.join(f'- [{n["title"]}]({BASE}nodes/{n["id"]}.md): {n["short"]}' for n in lib['nodes'])
    llms += '\n\n## Other routes\n\n- [Shared example](' + BASE + 'example/entry.md): the same facts through different views\n- [Sources](' + BASE + 'sources.md): snapshots, neighbouring work and limits\n- [Challenge](' + BASE + 'challenge.md): actual reply access and its limits\n\n## Optional\n\n- [Whole local packet](' + BASE + 'packet.md): ' + str(len(files['explore/packet.md'])) + ' UTF-8 bytes; not required; no external corpus\n'
    put('llms.txt',llms)
    manifest = {'format':'psfh-resource-map/0.2','status':STATUS,'intended_base_if_published':BASE,
                'boundary':lib['boundary'],'traversal':'Optional, bounded reading. Links can cycle; no fetch or report-back is required. A reader can stop when its question is answered.',
                'source_sha256':digest((source/'library.json').read_bytes()),'nodes':node_index,
                'resources':[{'path':p.removeprefix('explore/'),'bytes':len(b),'sha256':digest(b)} for p,b in sorted(files.items())],
                'integrity_limit':'Hashes describe this authored build, not independent truth, safety, current deployment or custody. map.json excludes itself to avoid a self-hash claim.',
                'release_claim':'No live deployment or receiver result is asserted by this file.'}
    put('map.json', encode(manifest))
    report = {'format':'psfh-local-build-receipt/0.2','scope':'LOCAL BUILD ONLY; no remote fetch, deployment or efficacy test',
              'nodes':len(lib['nodes']),'example_nodes':len(examples),'generated_files':len(files),
              'total_bytes':sum(map(len,files.values())), 'source_sha256':manifest['source_sha256'],
              'output_tree_sha256':digest(encode([(p,digest(b)) for p,b in sorted(files.items())]))}
    return files, report


def write_new(output: Path, files: dict[str, bytes]) -> None:
    if output.exists() and (output.is_symlink() or not output.is_dir() or any(output.iterdir())):
        raise ValueError('Output must be absent or empty: refusing to overwrite a site or other files')
    output.mkdir(parents=True, exist_ok=True)
    for path, data in sorted(files.items()):
        target = output / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='New or empty staging directory; no publishing')
    parser.add_argument('--check',action='store_true',help='Validate and build in memory only')
    args = parser.parse_args()
    try:
        files,report = generate()
        if args.output:
            write_new(args.output, files)
        elif not args.check:
            parser.error('Use --output PATH or --check')
        print(json.dumps(report,indent=2))
        return 0
    except (OSError,ValueError,KeyError,TypeError) as error:
        print('Build refused: ' + str(error),file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
