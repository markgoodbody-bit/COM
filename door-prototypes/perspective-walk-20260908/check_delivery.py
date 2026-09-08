#!/usr/bin/env python3
"""One-shot HTTPS delivery check; never publish, change settings or fall back to HTTP.

Run against the complete maintained website output, not only the explore/ subtree:
    python check_delivery.py --expected PATH_TO_BUILT_SITE

Exit 0: selected HTTPS response bytes matched that local build.
Exit 1: a selected request failed or differed. Exit 2: invalid local input.
This checks selected delivery, not every file, provider-specific access, reputation,
reader understanding, source truth, or the independent provenance of local bytes.
No credentials, third-party scanner, scheduler or persistent process is used.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import posixpath
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ORIGIN = 'https://pleasestartfromhere.com/'
MAX_BYTES = 262144
MAX_PATHS = 24


def timestamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_url(url: str) -> None:
    u = urllib.parse.urlsplit(url)
    if (u.scheme != 'https' or u.hostname != 'pleasestartfromhere.com'
            or u.username is not None or u.password is not None
            or u.port not in (None, 443) or u.query or u.fragment):
        raise ValueError('Only the canonical HTTPS origin without credentials is allowed')


class SameOriginRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse insecure or cross-origin redirects before issuing their requests."""
    def __init__(self) -> None:
        super().__init__()
        self.chain: list[dict] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        newurl = urllib.parse.urljoin(req.full_url, newurl)
        check_url(newurl)
        if len(self.chain) >= 4:
            raise ValueError('Redirect limit exceeded')
        self.chain.append({'status': code, 'from': req.full_url, 'to': newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def local_path(base: str, reference: str) -> str:
    if (not isinstance(reference, str) or not reference
            or not re.fullmatch(r'[A-Za-z0-9_./-]+', reference)
            or reference.startswith('/') or '..' in reference.split('/')):
        raise ValueError('Expected a document-relative local reference')
    path = posixpath.normpath(posixpath.join(posixpath.dirname(base), reference))
    if not path.startswith('explore/'):
        raise ValueError('Reading reference left explore/')
    return path


def read_expected(root: Path, path: str) -> bytes:
    candidate = root / path
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError('Expected file is outside the build or is not a file: ' + path)
    with resolved.open('rb') as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('Expected file exceeds byte limit: ' + path)
    return data


def expected_routes(root: Path) -> dict[str, bytes]:
    """Freeze a bounded route from the local build before any network operation."""
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Expected input must be a complete built-site directory')
    start_path = 'explore/start.json'
    start = json.loads(read_expected(root, start_path))
    if start.get('format') != 'psfh-arrival/0.1' or not isinstance(start.get('routes'), dict):
        raise ValueError('Unsupported small-entrance document')
    refs = start['routes']
    if not refs or len(refs) > MAX_PATHS - 4:
        raise ValueError('Small-entrance route count outside this check scope')
    question_path = local_path(start_path, refs['questions'])
    questions = json.loads(read_expected(root, question_path))
    nodes = questions.get('nodes')
    if not isinstance(nodes, list):
        raise ValueError('Missing question catalogue')
    matches = [n for n in nodes if isinstance(n, dict) and n.get('id') == 'hardening']
    if len(matches) != 1:
        raise ValueError('Expected one hardening reading for this explicit sample route')
    leaf = local_path(question_path, matches[0]['routes']['text'])
    paths = {'index.html', 'llms.txt', start_path, leaf}
    paths.update(local_path(start_path, ref) for ref in refs.values())
    if len(paths) > MAX_PATHS:
        raise ValueError('Selected route count exceeds limit')
    return {p: read_expected(root, p) for p in sorted(paths)}


def fetch_https(url: str) -> tuple[int, str, bytes, str, list[dict]]:
    check_url(url)
    redirect = SameOriginRedirect()
    request = urllib.request.Request(url, headers={
        'User-Agent': 'PleaseStartFromHere-one-shot-delivery-check',
        'Cache-Control': 'no-cache', 'Accept-Encoding': 'identity'})
    # The default HTTPSHandler verifies the certificate and hostname. No custom
    # trust context, authentication handler or HTTP fallback is installed.
    with urllib.request.build_opener(redirect).open(request, timeout=8) as response:
        check_url(response.url)
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError('Response exceeds byte limit')
        return (response.status, response.url, body,
                response.headers.get('Content-Type', ''), redirect.chain)


def check_one(path: str, expected: bytes, fetcher=fetch_https) -> dict:
    # index.html is checked through the actual root entry, not only its file URL.
    url = ORIGIN if path == 'index.html' else ORIGIN + path
    row = {'path': path, 'requested': url, 'at': timestamp(),
           'expected_sha256': sha(expected), 'expected_bytes': len(expected), 'ok': False}
    try:
        status, final, body, mime, redirects = fetcher(url)
        check_url(final)
        row.update(status=status, final=final, bytes=len(body), sha256=sha(body),
                   content_type=mime, redirects=redirects)
        row['ok'] = status == 200 and body == expected and len(body) <= MAX_BYTES
        if not row['ok']:
            row['error'] = 'Unexpected response status or bytes'
    except (OSError, ValueError, urllib.error.URLError) as error:
        row['error'] = type(error).__name__ + ': ' + str(error)[:350]
    return row


def run(expected: dict[str, bytes], fetcher=fetch_https) -> tuple[dict, int]:
    if not expected or len(expected) > MAX_PATHS:
        raise ValueError('A nonempty bounded sample is required')
    started = timestamp()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda item: check_one(*item, fetcher=fetcher),
                             sorted(expected.items())))
    ok = all(row['ok'] for row in rows)
    report = {
        'started': started, 'finished': timestamp(),
        'state': 'SELECTED_HTTPS_BYTES_MATCHED' if ok else 'DELIVERY_NOT_CONFIRMED',
        'origin': ORIGIN, 'selected': len(rows), 'matched': sum(r['ok'] for r in rows),
        'limits': 'Selected paths against local build bytes. Not an all-site audit, '
                  'HTTP redirect/enforcement check, provider-access guarantee or reader-benefit test.',
        'results': rows}
    return report, 0 if ok else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report, code = run(expected_routes(args.expected))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        report, code = {'state': 'LOCAL_INPUT_INVALID',
                        'error': type(error).__name__ + ': ' + str(error)[:350]}, 2
    print(json.dumps(report, indent=2))
    return code


if __name__ == '__main__':
    sys.exit(main())
