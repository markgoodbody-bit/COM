"""Explicit, offline-after-acquisition reader copies. Never publishes or rewrites inputs.

Acquire: python scripts/import-resources.py --acquire NEW_EMPTY_DIRECTORY
Assemble: python scripts/import-resources.py --assemble ACQUIRED --output NEW_EMPTY_DIRECTORY
Uses gh for explicit acquisition; Python stdlib plus pypdf for PDF inspection.
"""
import argparse
import base64
import hashlib
import html
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
INPUT_SHA = '9fdd16b8f9871e06bae72650ed42a7f69fcd0c83cd5dfd6ed3467023b9d34cb5'
BASE = 'https://pleasestartfromhere.com'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def safe_path(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9._/-]+', value):
        raise ValueError('Unsafe resource path')
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in ('', '.', '..') for part in value.split('/')):
        raise ValueError('Unsafe resource path')
    return value


def source_input():
    raw = (HERE / 'RESOURCE_COPIES.json').read_bytes()
    if sha(raw) != INPUT_SHA:
        raise ValueError('Import inventory changed: review before changing its pin')
    return json.loads(raw)


def write_new(root, files):
    if root.exists() and (root.is_symlink() or not root.is_dir() or any(root.iterdir())):
        raise ValueError('Refusing nonempty output')
    for path in files:
        safe_path(path)
    root.mkdir(parents=True, exist_ok=True)
    for path, raw in files.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)


def api(route):
    return json.loads(subprocess.check_output(['gh', 'api', route], timeout=45))


def check_body(file, raw):
    if len(raw) != file['bytes'] or git_blob(raw) != file['git_blob_sha1']:
        raise ValueError('Git identity/size mismatch: ' + file['path'])
    declared = file.get('sha256_declared_by_source_readme')
    if declared and sha(raw) != declared:
        raise ValueError('Declared SHA256 mismatch: ' + file['path'])
    if raw.startswith(b'version https://git-lfs.github.com/spec/'):
        raise ValueError('Git LFS pointer, not body')


def inspect_format(file, raw):
    suffix = PurePosixPath(file['path']).suffix
    if suffix == '.png':
        if not raw.startswith(b'\x89PNG\r\n\x1a\n') or raw[12:16] != b'IHDR':
            raise ValueError('Invalid PNG header')
    elif suffix == '.svg':
        text = raw.decode('utf-8')
        if re.search(r'<!DOCTYPE|<!ENTITY|<\?xml-stylesheet|@|\\', text, re.I):
            raise ValueError('SVG external/indirect content refused')
        root = ET.fromstring(text)
        if root.tag != '{http://www.w3.org/2000/svg}svg':
            raise ValueError('Expected SVG root')
        raw_ids = [e.attrib['id'] for e in root.iter() if 'id' in e.attrib]
        ids = set(raw_ids)
        if len(ids) != len(raw_ids):
            raise ValueError('Duplicate SVG ID')
        for reference in re.findall(r'url\s*\(([^)]+)\)', text, re.I):
            if not re.fullmatch(r'#[A-Za-z][\w-]*', reference) or reference[1:] not in ids:
                raise ValueError('Nonlocal/unresolved SVG reference')
        allowed = {'svg', 'g', 'defs', 'marker', 'path', 'rect', 'line', 'polyline',
                   'polygon', 'circle', 'ellipse', 'text', 'tspan', 'title', 'desc', 'style'}
        # Local marker URLs are permitted only after XML parsing and exact fragment validation.
        for element in root.iter():
            if not element.tag.startswith('{http://www.w3.org/2000/svg}'):
                raise ValueError('Foreign SVG namespace')
            if element.tag.split('}')[-1] not in allowed:
                raise ValueError('Unexpected SVG element: ' + element.tag)
            for attr, value in element.attrib.items():
                name = attr.split('}')[-1].lower()
                if name.startswith('on') or name in ('href', 'src', 'base') or re.search(r'javascript:|https?:|data:', value, re.I):
                    raise ValueError('Active/external SVG attribute')
            css = '\n'.join(element.attrib.values()) + '\n' + (element.text or '')
            if re.search(r'expression\s*\(|javascript\s*:|behavior\s*:', css, re.I):
                raise ValueError('Active SVG style')
    elif suffix == '.pdf':
        if not raw.startswith(b'%PDF-') or b'%%EOF' not in raw[-1024:]:
            raise ValueError('Invalid PDF header/trailer')
        from pypdf import PdfReader
        from pypdf.generic import IndirectObject, DictionaryObject, ArrayObject
        reader = PdfReader(io.BytesIO(raw), strict=True)
        if reader.is_encrypted or not reader.pages:
            raise ValueError('Unreadable/encrypted PDF')
        seen = set()
        def inspect(obj):
            if isinstance(obj, IndirectObject):
                key = (obj.idnum, obj.generation)
                if key in seen:
                    return
                seen.add(key)
                obj = obj.get_object()
            if isinstance(obj, DictionaryObject):
                if set(obj) & {'/JS', '/JavaScript', '/Launch', '/EmbeddedFiles', '/RichMedia', '/XFA', '/OpenAction', '/AA'}:
                    raise ValueError('Active/embedded PDF content refused')
                if '/S' in obj and str(obj['/S']) not in ('/URI', '/GoTo'):
                    raise ValueError('Unexpected PDF action')
                if '/URI' in obj and not str(obj['/URI']).startswith(('https://', 'http://')):
                    raise ValueError('Unexpected PDF URI')
                for child in obj.values():
                    inspect(child)
            elif isinstance(obj, ArrayObject):
                for child in obj:
                    inspect(child)
        inspect(reader.trailer)
        return {'pages': len(reader.pages), 'check': 'Parsed reachable PDF objects; no authoring or visual review'}
    elif suffix == '.md':
        if '\x00' in raw.decode('utf-8'):
            raise ValueError('NUL in Markdown')
    else:
        raise ValueError('Unexpected file format')
    return {'check': 'Format and bounded active-content check'}


def acquire(root):
    spec, files, observations = source_input(), {}, []
    for project in spec['projects']:
        repo, commit = project['repository'], project['commit']
        head = api('repos/' + repo + '/commits/main')['sha']
        selected = api('repos/' + repo + '/git/commits/' + commit)
        if selected['sha'] != commit:
            raise ValueError('Source commit mismatch')
        tree = api('repos/' + repo + '/git/trees/' + selected['tree']['sha'] + '?recursive=1')
        if tree.get('truncated') or tree['sha'] != selected['tree']['sha']:
            raise ValueError('Incomplete source tree')
        nodes = {row['path']: row for row in tree['tree']}
        observations.append({'repository': repo, 'observed_main': head, 'selected_commit': commit,
                             'head_matches_pin': head == commit})
        for file in project['files']:
            path = safe_path(file['path'])
            row = nodes.get(path)
            if not row or row['type'] != 'blob' or row['mode'] != '100644' or row['sha'] != file['git_blob_sha1'] or row['size'] != file['bytes']:
                raise ValueError('Source tree identity mismatch: ' + path)
            blob = api('repos/' + repo + '/git/blobs/' + row['sha'])
            if blob['encoding'] != 'base64' or blob['sha'] != row['sha']:
                raise ValueError('Unexpected Git body response')
            raw = base64.b64decode(blob['content'])
            check_body(file, raw)
            files[project['id'] + '/' + path] = raw
    files['acquisition.json'] = (json.dumps(observations, indent=2) + '\n').encode()
    write_new(root, files)
    print(json.dumps({'acquired': len(files) - 1, 'observations': observations}, indent=2))


def dependencies(project, bodies):
    """Inventory inline/reference Markdown and HTML href/src destinations; don't rewrite."""
    result = []
    for file in project['files']:
        path = file['path']
        if not path.endswith('.md'):
            continue
        text = bodies[path].decode()
        # Code examples are not navigational dependencies.
        text = re.sub(r'^```[^\n]*\n.*?^```[^\n]*$', '', text, flags=re.M | re.S)
        urls = re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text)
        urls += re.findall(r'^\s*\[[^\]]+\]:\s*<?([^\s>]+)', text, re.M)
        urls += re.findall(r'(?:href|src)=["\']([^"\']+)', text, re.I)
        for url in sorted(set(urls)):
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                result.append({'from': path, 'url': url, 'kind': 'external source/history/participation/reference'})
                continue
            target = str(PurePosixPath(path).parent / unquote(parts.path)) if parts.path else path
            safe_path(target)
            is_directory = parts.path.endswith('/') and any(p.startswith(target + '/') for p in bodies)
            if target not in bodies and not is_directory:
                raise ValueError('Missing local dependency: ' + path + ' -> ' + url)
            result.append({'from': path, 'url': url, 'kind': 'local', 'target': target + '/index.html' if is_directory else target,
                           'fragment': parts.fragment or None,
                           'fragment_limit': 'Raw Markdown fragment behavior depends on the reader; no HTML conversion claimed.'})
    return result


def assemble(root, output, previous=None):
    spec, files, projects = source_input(), {}, []
    for project in spec['projects']:
        bodies, rows = {}, []
        for file in project['files']:
            source = root / project['id'] / safe_path(file['path'])
            if source.is_symlink():
                raise ValueError('Source symlink refused')
            raw = source.read_bytes()
            check_body(file, raw)
            inspection = inspect_format(file, raw)
            bodies[file['path']] = raw
            current = project['current_prefix'] + file['path']
            snapshot = project['snapshot_prefix'] + file['path']
            for url in (current, snapshot):
                key = safe_path(url.removeprefix('/resources/'))
                if key in files:
                    raise ValueError('Duplicate output')
                files[key] = raw
            rows.append(dict(file, sha256=sha(raw), current=current, snapshot=snapshot,
                             source_url='https://github.com/' + project['repository'] + '/blob/' + project['commit'] + '/' + file['path'],
                             inspection=inspection))
        # The preserved ME README links to figures/. Supply an index at both prefixes.
        directories = sorted({str(PurePosixPath(p).parent) for p in bodies if '/' in p})
        for directory in directories:
            links = ''.join('<li><a href="' + html.escape(PurePosixPath(p).name) + '">' + html.escape(PurePosixPath(p).name) + '</a></li>' for p in bodies if str(PurePosixPath(p).parent) == directory)
            page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mechanical Ethics diagrams</title><link rel="stylesheet" href="/style.css"></head><body><main><h1>Mechanical Ethics diagrams</h1><p>Explanatory carriers, not evidence. <a href="../README.md">Edition and original notices</a>.</p><ul>' + links + '</ul><p><a href="/resources/">Reading catalogue</a></p></main></body></html>\n').encode()
            for prefix in (project['current_prefix'], project['snapshot_prefix']):
                files[safe_path((prefix + directory + '/index.html').removeprefix('/resources/'))] = page
        projects.append({k: project[k] for k in ('id', 'repository', 'commit', 'status_at_source', 'baseline_distinction', 'notice_path')} |
                        {'files': rows, 'dependencies': dependencies(project, bodies)})
    inventory = {'format': 'psfh-resource-copies/0.1', 'input_sha256': INPUT_SHA,
                 'input_source': 'https://github.com/markgoodbody-bit/COM/blob/10c23eb1b971d1c14306637837de6d05d0dbec2f/door-prototypes/perspective-walk-20260908/RESOURCE_COPIES.json',
                 'boundary': 'Pinned project-controlled reading copies, not a whole ecosystem mirror, release, validation or new reuse/training licence. Current aliases name these selected editions, not continuously checked heads. Snapshot bytes must not be overwritten.',
                 'projects': projects}
    title = 'Read TRACE and Mechanical Ethics'
    intro = 'The documents are here on this site. You can read the Markdown or download the existing ME PDF. These are working editions, not validated releases. Their original notices are included unchanged.'
    limit = 'GitHub remains the place for source history, criticism and discussion. FPF and other third-party references remain elsewhere. This is not a self-contained copy of every linked source, and it does not grant new copying, adaptation or training rights.'
    text = '# ' + title + '\n\n' + intro + '\n\n' + limit + '\n'
    body = '<h1>' + title + '</h1><p>' + intro + '</p>'
    body += '<p>Optional HTML source-text views: <a href="/read/trace-spine.html">TRACE compact spine</a> · <a href="/read/me-book.html">ME book</a> · <a href="/read/start.html">Start</a> · <a href="/read/orientation.html">Orientation</a>. Complete source text, not a new formatted edition.</p>'
    text += '\nOptional HTML source-text views: [TRACE compact spine](' + BASE + '/read/trace-spine.html) · [ME book](' + BASE + '/read/me-book.html) · [Start](' + BASE + '/read/start.html) · [Orientation](' + BASE + '/read/orientation.html). Complete source text, not a new formatted edition.\n'
    for project in projects:
        name = 'TRACE' if project['id'] == 'trace' else 'Mechanical Ethics'
        body += '<section><h2>' + name + '</h2><p>' + html.escape(project['status_at_source']) + '. ' + html.escape(project['baseline_distinction']) + '.</p><ul>'
        text += '\n## ' + name + '\n\n' + project['status_at_source'] + '. ' + project['baseline_distinction'] + '.\n\n'
        for file in project['files']:
            label = file['path']
            body += '<li><a href="' + file['current'] + '">' + html.escape(label) + '</a> (' + str(file['bytes']) + ' bytes) · <a href="' + file['snapshot'] + '">fixed edition</a></li>'
            text += '- [' + label + '](' + BASE + file['current'] + ') · [fixed edition](' + BASE + file['snapshot'] + ') · ' + str(file['bytes']) + ' bytes\n'
        repo = 'https://github.com/' + project['repository'] + '/tree/' + project['commit']
        body += '</ul><p>Source edition: <a href="' + repo + '">' + project['commit'] + '</a>.</p></section>'
        text += '\n[Source edition ' + project['commit'] + '](' + repo + ').\n'
    body += '<p>' + limit + '</p><p><a href="inventory.json">File hashes, source identities and remaining external links</a> · <a href="index.md">Markdown catalogue</a> · <a href="/">Return or stop</a></p>'
    text += '\n[Hashes, identities and remaining external links](' + BASE + '/resources/inventory.json) · [Return or stop](' + BASE + '/).\n'
    files['index.md'] = text.encode()
    files['index.html'] = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + title + ' | Please Start From Here</title><link rel="stylesheet" href="/style.css"><link rel="alternate" type="text/markdown" href="index.md"><link rel="describedby" href="inventory.json"></head><body><header class="masthead"><a href="/">Please Start From Here</a></header><main>' + body + '</main></body></html>\n').encode()
    if previous and previous.exists():
        old = json.loads((previous / 'inventory.json').read_bytes())
        for entry in old['snapshot_files']:
            path = safe_path(entry['path'])
            if not path.startswith('snapshots/'):
                raise ValueError('Invalid prior snapshot path')
            source = previous / path
            if source.is_symlink():
                raise ValueError('Snapshot symlink refused')
            raw = source.read_bytes()
            if sha(raw) != entry['sha256'] or len(raw) != entry['bytes']:
                raise ValueError('Prior snapshot changed')
            if path in files and files[path] != raw:
                raise ValueError('Refusing snapshot replacement')
            files[path] = raw
    raw_paths = {url.removeprefix('/resources/') for p in projects for f in p['files'] for url in (f['current'], f['snapshot'])}
    describe = lambda p, b: {'path': p, 'bytes': len(b), 'sha256': sha(b)}
    inventory['generated_files'] = [describe(p, b) for p, b in files.items() if p not in raw_paths and not p.startswith('snapshots/')]
    inventory['snapshot_files'] = [describe(p, b) for p, b in files.items() if p.startswith('snapshots/')]
    files['inventory.json'] = (json.dumps(inventory, ensure_ascii=False, indent=2) + '\n').encode()
    write_new(output, files)
    print(json.dumps({'files': len(files), 'bytes': sum(map(len, files.values())),
                      'inventory_sha256': sha(files['inventory.json'])}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--acquire', type=Path)
    mode.add_argument('--assemble', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--previous', type=Path, default=HERE.parent / 'public/resources', help='Retain and verify previously published snapshots')
    args = parser.parse_args()
    if args.acquire:
        acquire(args.acquire)
    else:
        if not args.output:
            parser.error('--assemble requires --output')
        assemble(args.assemble, args.output, args.previous)
