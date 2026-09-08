#!/usr/bin/env python3
"""Build pinned first-party resource copies. No publication or site-setting writes.

The output dictionary can be merged by the maintained site build. Acquire and
verify all selected bodies before writing an empty staging directory. Original
Markdown, images and PDF bytes are never rewritten. See the report for limits.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from typing import Callable
from urllib.parse import unquote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

HERE = Path(__file__).resolve().parent
ORIGIN = 'https://pleasestartfromhere.com'
PROJECTS = {'trace': 'markgoodbody-bit/TRACE',
            'mechanical-ethics': 'markgoodbody-bit/mechanical-ethics'}
TYPES = {'.md': 'text/markdown; charset=utf-8', '.pdf': 'application/pdf',
         '.png': 'image/png', '.svg': 'image/svg+xml'}
Fetch = Callable[[str, int], bytes]


def encode(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def unique(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def clean_path(value: str) -> bool:
    return (isinstance(value, str) and bool(value) and not value.startswith('/')
            and re.fullmatch(r'[A-Za-z0-9_./-]+', value) is not None
            and all(part not in ('', '.', '..') for part in value.split('/')))


def validate_inventory(inv: dict) -> None:
    if inv.get('format') != 'psfh-resource-copy-input/0.1':
        raise ValueError('Unsupported inventory format')
    seen, destinations, total, count = set(), set(), 0, 0
    for project in inv['projects']:
        ident, commit = project['id'], project['commit']
        if ident in seen or PROJECTS.get(ident) != project['repository']:
            raise ValueError('Unknown or repeated project')
        seen.add(ident)
        if not isinstance(commit, str) or not re.fullmatch(r'[0-9a-f]{40}', commit):
            raise ValueError('A full immutable commit is required')
        expected = ('/resources/' + ident + '/',
                    '/resources/snapshots/' + ident + '/' + commit + '/')
        if (project['current_prefix'], project['snapshot_prefix']) != expected:
            raise ValueError('Unexpected destination prefix')
        names = set()
        for spec in project['files']:
            name, size = spec['path'], spec['bytes']
            if not clean_path(name) or name.casefold() in names:
                raise ValueError('Unsafe or duplicate input path')
            names.add(name.casefold())
            if type(size) is not int or not 0 < size <= 4_000_000:
                raise ValueError('Invalid input size')
            if TYPES.get(PurePosixPath(name).suffix) != spec['media_type']:
                raise ValueError('Unsupported or mismatched media type')
            if not re.fullmatch(r'[0-9a-f]{40}', spec['git_blob_sha1']):
                raise ValueError('Missing Git blob identity')
            claimed = spec.get('sha256_declared_by_source_readme')
            if claimed is not None and not re.fullmatch(r'[0-9a-f]{64}', claimed):
                raise ValueError('Invalid declared SHA-256')
            total += size
            count += 1
            for prefix in expected:
                path = (prefix + name).lstrip('/')
                if path.casefold() in destinations:
                    raise ValueError('Overlapping output paths')
                destinations.add(path.casefold())
        if project['notice_path'] != 'README.md' or 'readme.md' not in names:
            raise ValueError('Source notices must accompany every project')
    if seen != set(PROJECTS):
        raise ValueError('Both selected projects are required')
    totals = inv['byte_totals']
    if (count != totals['source_file_count'] or total != totals['source_files']
            or total * 2 != totals['current_plus_one_snapshot']):
        raise ValueError('Inventory total mismatch')


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Source redirect refused: ' + str(code))


def public_fetch(url: str, size: int) -> bytes:
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.netloc != 'raw.githubusercontent.com':
        raise ValueError('Unexpected source host')
    req = Request(url, headers={'User-Agent': 'PSFH-pinned-resource-build/0.1',
                                'Accept-Encoding': 'identity'})
    # Default certificate verification, no credentials, no proxy around a block.
    with build_opener(NoRedirect()).open(req, timeout=20) as response:
        if response.status != 200 or response.geturl() != url:
            raise ValueError('Source did not return a direct 200 response')
        return response.read(size + 1)


def check_svg(data: bytes) -> None:
    text = data.decode('utf-8')
    if re.search(r'<!DOCTYPE|<!ENTITY|<\?xml-stylesheet', text, re.I):
        raise ValueError('SVG declaration or external stylesheet refused')
    root = ET.fromstring(text)
    allowed = {'svg', 'title', 'desc', 'defs', 'marker', 'path', 'style', 'rect',
               'text', 'tspan', 'g', 'line', 'polyline', 'polygon', 'circle', 'ellipse'}
    if root.tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError('Expected an SVG root')
    ids, refs = set(), []
    for node in root.iter():
        if not node.tag.startswith('{http://www.w3.org/2000/svg}'):
            raise ValueError('Foreign SVG namespace')
        if node.tag.split('}')[-1] not in allowed:
            raise ValueError('Unreviewed SVG element')
        if 'id' in node.attrib:
            if node.attrib['id'] in ids:
                raise ValueError('Duplicate SVG id')
            ids.add(node.attrib['id'])
        for key, value in node.attrib.items():
            local = key.split('}')[-1].lower()
            if local.startswith('on') or local in {'href', 'src', 'base'}:
                raise ValueError('Active or external SVG attribute')
        css = '\n'.join(node.attrib.values()) + '\n' + (node.text or '')
        if re.search(r'@import|expression\s*\(|javascript\s*:|behavior\s*:', css, re.I):
            raise ValueError('Active SVG style')
        for value in re.findall(r'url\s*\(([^)]*)\)', css, re.I):
            value = value.strip().strip('\"\'')
            if not re.fullmatch(r'#[A-Za-z_][\w.-]*', value):
                raise ValueError('External SVG style reference')
            refs.append(value[1:])
    if any(ref not in ids for ref in refs):
        raise ValueError('Missing local SVG reference')


def verify_body(spec: dict, data: bytes) -> None:
    if not isinstance(data, bytes) or len(data) != spec['bytes']:
        raise ValueError('Wrong resource size: ' + spec['path'])
    if blob(data) != spec['git_blob_sha1']:
        raise ValueError('Wrong Git blob: ' + spec['path'])
    claimed = spec.get('sha256_declared_by_source_readme')
    if claimed is not None and digest(data) != claimed:
        raise ValueError('Wrong declared SHA-256: ' + spec['path'])
    if data.startswith(b'version https://git-lfs.github.com/spec/'):
        raise ValueError('Git LFS pointer is not a resource body')
    suffix = PurePosixPath(spec['path']).suffix
    if suffix == '.md':
        if '\x00' in data.decode('utf-8'):
            raise ValueError('NUL in Markdown')
    elif suffix == '.svg':
        check_svg(data)
    elif suffix == '.png' and not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Invalid PNG signature')
    elif suffix == '.pdf':
        if not data.startswith(b'%PDF-') or b'%%EOF' not in data[-2048:]:
            raise ValueError('Invalid PDF signature/ending')
        # This is an explicit-token guard, not a full PDF-parser security audit.
        if re.search(rb'/(?:JavaScript|JS|Launch|OpenAction|AA|EmbeddedFile)\b', data):
            raise ValueError('PDF action/embedded-file marker requires separate review')


def markdown_references(data: bytes) -> list[str]:
    text = data.decode('utf-8')
    # Scan prose references, not example URLs inside fenced code blocks.
    text = re.sub(r'^([`~]{3,})[^\n]*\n.*?^\1\s*$', '', text,
                  flags=re.M | re.S)
    return re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)', text)


def dependency_report(project: dict, bodies: dict[str, bytes]) -> dict:
    outward, directories = set(), set()
    relative_count = 0
    for name, data in bodies.items():
        if not name.endswith('.md'):
            continue
        for href in markdown_references(data):
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                outward.add(href)
                continue
            if not parsed.path:
                continue  # Fragment semantics are not claimed by this scanner.
            path = unquote(parsed.path)
            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), path))
            if path.startswith('/') or target.startswith('../') or target == '..':
                raise ValueError('Out-of-library reference: ' + name + ' -> ' + href)
            relative_count += 1
            if target in bodies:
                continue
            prefix = target.rstrip('/') + '/'
            if any(item.startswith(prefix) for item in bodies):
                directories.add(target.rstrip('/'))
                continue
            raise ValueError('Missing relative dependency: ' + name + ' -> ' + href)
    return {'relative_file_or_directory_links_checked': relative_count,
            'directory_indexes_required': sorted(directories),
            'still_external_destinations': sorted(outward),
            'scope': 'Inline prose Markdown references; not arbitrary Markdown, code examples, PDF links or fragment conformance.'}


def html_page(title: str, body: str) -> bytes:
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + html.escape(title) + '</title></head><body><main><h1>'
            + html.escape(title) + '</h1>' + body + '</main></body></html>\n').encode('utf-8')


def generate(inventory_path: Path, fetch: Fetch = public_fetch) -> tuple[dict[str, bytes], dict]:
    inventory_bytes = inventory_path.read_bytes()
    inv = json.loads(inventory_bytes, object_pairs_hook=unique)
    validate_inventory(inv)
    acquired, projects = {}, []
    for project in inv['projects']:
        bodies = {}
        for spec in project['files']:
            source = ('https://raw.githubusercontent.com/' + project['repository']
                      + '/' + project['commit'] + '/' + spec['path'])
            data = fetch(source, spec['bytes'])
            verify_body(spec, data)
            bodies[spec['path']] = data
        deps = dependency_report(project, bodies)
        acquired[project['id']] = bodies
        record = {key: project[key] for key in ('id', 'repository', 'commit',
                  'status_at_source', 'baseline_distinction', 'notice_path')}
        record['dependency_check'] = deps
        record['files'] = []
        for spec in project['files']:
            name, data = spec['path'], bodies[spec['path']]
            record['files'].append({'path': name, 'bytes': len(data), 'sha256': digest(data),
                'git_blob_sha1': blob(data), 'media_type_declared': spec['media_type'],
                'current_url': ORIGIN + project['current_prefix'] + name,
                'snapshot_url': ORIGIN + project['snapshot_prefix'] + name,
                'original_url': 'https://github.com/' + project['repository'] + '/blob/'
                                + project['commit'] + '/' + name})
        projects.append(record)
    # No writes, partial output or alias advance before every source verifies.
    files = {}
    for project, record in zip(inv['projects'], projects):
        for prefix in (project['current_prefix'], project['snapshot_prefix']):
            for name, data in acquired[project['id']].items():
                files[prefix.lstrip('/') + name] = data
            for directory in record['dependency_check']['directory_indexes_required']:
                children = sorted(n for n in acquired[project['id']] if n.startswith(directory + '/'))
                body = '<p>Copied explanatory resources, not evidence. Source edition: ' + html.escape(project['commit']) + '.</p><ul>'
                for name in children:
                    relative = posixpath.relpath(name, directory)
                    body += '<li><a href="' + html.escape(relative, quote=True) + '">' + html.escape(relative) + '</a></li>'
                body += '</ul><p><a href="' + prefix + 'README.md">Source status and notices</a></p>'
                files[prefix.lstrip('/') + directory + '/index.html'] = html_page('Figures — Mechanical Ethics', body)
    notice = ('Complete first-party reading copies. Choose a file; no full-library retrieval is required. '
              'Current addresses can change with deliberate releases; source-commit snapshot addresses retain the selected bytes. '
              'The original notices and candidate/baseline status remain. No new reuse or training licence is granted. '
              'History, discussion and third-party references can still lead outside this domain.')
    catalogue = {'format': 'psfh-resource-catalogue/0.1', 'prepared': inv['prepared'],
                 'status': 'VERIFIED BUILD OUTPUT / NOT A LIVE DELIVERY RECEIPT',
                 'inventory_sha256': digest(inventory_bytes), 'reading': notice,
                 'checks_scope': 'Source identity, signatures, restricted SVG policy and bounded inline-link closure; not a comprehensive document security audit or reader-benefit test.',
                 'projects': projects}
    files['resources/index.json'] = encode(catalogue)
    md = '# Reading resources\n\n' + notice + '\n\n'
    body = '<p>' + html.escape(notice) + '</p>'
    for project in projects:
        md += '## ' + project['id'] + '\n\n' + project['status_at_source'] + '\n\n'
        md += project['baseline_distinction'] + '\n\nSource revision: ' + project['commit'] + '\n\n'
        body += '<section><h2>' + html.escape(project['id']) + '</h2><p>' + html.escape(project['status_at_source']) + '</p><p>' + html.escape(project['baseline_distinction']) + '</p><p>Source revision: ' + project['commit'] + '</p><ul>'
        for item in project['files']:
            md += '- [' + item['path'] + '](' + item['current_url'] + ') — ' + str(item['bytes']) + ' bytes; [fixed edition](' + item['snapshot_url'] + '); [original](' + item['original_url'] + ').\n'
            body += '<li><a href="' + item['current_url'] + '">' + html.escape(item['path']) + '</a> — ' + str(item['bytes']) + ' bytes; <a href="' + item['snapshot_url'] + '">fixed edition</a>; <a href="' + item['original_url'] + '">original source</a></li>'
        md += '\n'
        body += '</ul></section>'
    md += '[File hashes and dependency scope](index.json) · [What changed and why](/changes.md) · [Return to the Door](/)\n'
    body += '<p><a href="index.md">Plain text</a> · <a href="index.json">File hashes and dependency scope</a> · <a href="/changes.html">What changed and why</a> · <a href="/">Return to the Door</a></p>'
    files['resources/index.md'], files['resources/index.html'] = md.encode('utf-8'), html_page('Reading resources', body)
    report = {'scope': 'Verified source/build only, not public delivery', 'original_files': inv['byte_totals']['source_file_count'],
              'original_bytes': inv['byte_totals']['source_files'], 'output_files': len(files),
              'output_bytes': sum(map(len, files.values())),
              'tree_sha256': digest(encode([(p, digest(b)) for p, b in sorted(files.items())])),
              'projects': [{key: p[key] for key in ('id', 'commit', 'dependency_check')} for p in projects]}
    return files, report


def write_new(directory: Path, files: dict[str, bytes]) -> None:
    if directory.is_symlink() or (directory.exists() and (not directory.is_dir() or any(directory.iterdir()))):
        raise ValueError('Refusing to overwrite an existing output')
    if any(not clean_path(name) for name in files):
        raise ValueError('Unsafe generated output path')
    directory.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, default=HERE / 'RESOURCE_COPIES.json')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.output.exists() and (not args.output.is_dir() or any(args.output.iterdir())):
            raise ValueError('Use an empty staging directory')
        files, report = generate(args.inventory)
        write_new(args.output, files)
        print(json.dumps(report, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as error:
        print('Resource build refused: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
