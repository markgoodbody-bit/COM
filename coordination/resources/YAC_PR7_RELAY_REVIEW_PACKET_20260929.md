# YAC PR #7 — Relay supplementary provenance review packet — 29 September 2026

Status: **SUPPLEMENTARY CODE REVIEW / NOT FRESH-READER TEST / NOT VALIDATION**

Target repository: `markgoodbody-bit/yet-another-clearing`  
Target PR: #7  
Exact repaired head: `5d71d64d61bdde83d493d45a9af31dd4898efd22`

## Why this review exists

An earlier capture implementation checked worktree cleanliness and HEAD before capture, while runtime imports happened earlier and `orientation.json` was read live. A concurrent edit/checkout could therefore make the emitted `source_commit` disagree with the bytes actually served/captured.

The repaired implementation attempts to remove that ordinary mutable-worktree race by:
- resolving the target commit once;
- reading fixed required files from that commit tree as Git blobs;
- verifying each blob;
- materializing those bytes into a disposable directory;
- running an isolated Python child against only that materialized source;
- hashing the returned arrival bytes;
- emitting a source-blob manifest;
- keeping `OFFLINE_ARRIVAL_SNAPSHOT` and `live_address: null`.

Local and hosted Windows/Linux tests have passed. Codex exact-head self-review found no blocker. This packet asks for a **supplementary independent model review** of the repair only.

## Review question

Return exactly one leading disposition:

`NO BLOCKER`  
or  
`BLOCKER`

Then give concrete evidence.

Attack only these questions:

1. Can any ordinary live-worktree edit/checkout still influence the captured arrival bytes after the target commit is resolved?
2. Can the Git commit/tree/blob materialization mis-bind `source_commit` to served bytes through path parsing, object lookup, symlinks, modes, or another ordinary repository-state edge case?
3. Can the isolated child import/read code or `orientation.json` from outside the materialized source in a way that invalidates the commit-binding claim?
4. Does the regression actually reproduce the class of race that was repaired, or does it only test a weaker case?
5. Are the emitted Git blob IDs, SHA-256 values, UTF-8 bytes, and `source_commit` mutually consistent enough for the narrow claim being made?
6. Does this repair introduce a capability/secret leak or silently change the arrival semantics?

## Explicit non-goals / ceilings

Do **not** review product naming, constitution, moderation, storage choice, fresh-reader wording, or whether YAC should exist.

Do **not** claim:
- malicious-host or same-user-process isolation;
- successful live one-address discovery;
- successful model participation;
- fresh-reader usability;
- security validation.

Trusted local Git/Python/OS remain stated assumptions.

A reviewer that sees this packet is **not eligible to serve as the later fresh baseline reader**.

`REVIEWER AGREEMENT != VALIDATION`  
`COMMIT-BOUND CAPTURE != HOST-COMPROMISE RESISTANCE`

## File: tools/capture_arrival.py

```python
"""Capture local arrival evidence only; no model dispatch or retained database."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ('prototype/server.py', 'prototype/store.py', 'prototype/capsule.py',
         'prototype/disclosure.py', 'orientation.json', 'tools/capture_worker.py')


def capture(repo=ROOT, revision='HEAD'):
    repo = Path(repo)
    def git(*args, data=None):
        return subprocess.check_output(['git', *args], cwd=repo, input=data, stderr=subprocess.PIPE)
    commit = git('rev-parse', '--verify', '--end-of-options', revision + '^{commit}').decode().strip()
    manifest = {}
    with tempfile.TemporaryDirectory(prefix='yac-arrival-source-') as folder:
        root = Path(folder)
        for name in FILES:
            record = git('ls-tree', '-z', commit, '--', name).rstrip(b'\0')
            metadata, path = record.split(b'\t', 1)
            mode, kind, oid = metadata.decode().split()
            if path.decode() != name or mode not in ('100644', '100755') or kind != 'blob':
                raise ValueError('Required source is not a regular commit blob')
            raw = git('cat-file', 'blob', oid)
            if git('hash-object', '--stdin', data=raw).decode().strip() != oid:
                raise ValueError('Source blob verification failed')
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
            if destination.read_bytes() != raw:
                raise ValueError('Materialization verification failed')
            manifest[name] = {'git_blob': oid, 'sha256': hashlib.sha256(raw).hexdigest()}
        raw_result = subprocess.check_output(
            [sys.executable, '-I', '-B', str(root / 'tools/capture_worker.py'), commit],
            cwd=root, timeout=30, stderr=subprocess.PIPE)
        result = json.loads(raw_result.decode('utf-8'))
        if result['source_commit'] != commit or result['live_address'] is not None:
            raise ValueError('Capture identity mismatch')
        result['source_blobs'] = manifest
        return result


if __name__ == '__main__':
    sys.stdout.buffer.write((json.dumps(capture(), ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

```

## File: tools/capture_worker.py

```python
"""Internal worker executed from verified commit material, not the worktree."""
import hashlib
import http.client
import json
from pathlib import Path
import sys
import tempfile
import threading

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'prototype'))
from server import App, make_server


def run(commit):
    surfaces = []
    with tempfile.TemporaryDirectory(prefix='yac-arrival-room-') as folder:
        app = App(folder)
        server = make_server(app)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for path in ('/llms.txt', '/orientation.json', '/api/disclosure'):
                conn = http.client.HTTPConnection('127.0.0.1', server.server_port, timeout=5)
                try:
                    conn.request('GET', path)
                    response = conn.getresponse()
                    raw = response.read()
                    if response.status != 200 or app.token.encode() in raw:
                        raise ValueError('Arrival capture rejected; response omitted')
                    surfaces.append({'path': path, 'sha256': hashlib.sha256(raw).hexdigest(),
                                     'text': raw.decode('utf-8')})
                finally:
                    conn.close()
        finally:
            server.shutdown()
            thread.join()
            server.server_close()
            app.dispose()
    return {'source_commit': commit, 'kind': 'OFFLINE_ARRIVAL_SNAPSHOT',
            'live_address': None, 'entry_path': '/llms.txt', 'surfaces': surfaces}


if __name__ == '__main__':
    sys.stdout.buffer.write(json.dumps(run(sys.argv[1]), ensure_ascii=False).encode('utf-8'))

```

## File: prototype/test_capture.py

```python
"""Capture regression in a disposable Git repository; no project mutation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from capture_arrival import capture, FILES


class CaptureTests(unittest.TestCase):
    def test_committed_runtime_and_unicode_survive_worktree_edits(self):
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=repo, stderr=subprocess.PIPE)
            git('init')
            for name in FILES:
                dest = repo / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes((ROOT / name).read_bytes())
            orientation = repo / 'orientation.json'
            data = json.loads(orientation.read_text(encoding='utf-8'))
            data['description'] = 'A clearing: café, 木, £.'
            orientation.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            git('add', '.')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'Fixture')
            commit = git('rev-parse', 'HEAD').decode().strip()
            orientation.write_text('{}', encoding='utf-8')
            for name in ('prototype/server.py', 'tools/capture_worker.py'):
                (repo / name).write_text('raise RuntimeError("live source used")', encoding='utf-8')
            result = capture(repo, commit)
            self.assertEqual(result['source_commit'], commit)
            self.assertIsNone(result['live_address'])
            self.assertEqual(set(result['source_blobs']), set(FILES))
            for surface in result['surfaces']:
                self.assertEqual(hashlib.sha256(surface['text'].encode('utf-8')).hexdigest(), surface['sha256'])
            self.assertIn('café, 木, £', result['surfaces'][0]['text'])
            with self.assertRaises(subprocess.CalledProcessError):
                capture(repo, 'not-a-commit')


if __name__ == '__main__':
    unittest.main()

```
