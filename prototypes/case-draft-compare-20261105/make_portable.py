#!/usr/bin/env python3
"""Build an offline review kit from an explicit source allowlist; no network or browser."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

import compare
import html_report

ROOT = Path(__file__).resolve().parent
PRODUCT_FILES = ('compare.py', 'html_report.py', 'review_drafts.py',
                 'Review drafts.cmd', 'Review counts only.cmd', 'START HERE.txt', 'README.md',
                 'examples/before.json', 'examples/after.json')


def build(destination):
    destination = Path(destination).resolve()
    archive = destination.with_suffix('.zip')
    if destination.exists() or archive.exists():
        raise ValueError('The kit folder or ZIP already exists; choose a new destination.')
    # Prepare the bounded fictional example before writing the new kit.
    a, b = (ROOT / 'examples/before.json').read_bytes(), (ROOT / 'examples/after.json').read_bytes()
    example = html_report.render_html(compare.changes(compare.parse_json(a), compare.parse_json(b)),
                                      compare.sha256(a), compare.sha256(b))
    destination.mkdir(parents=True, exist_ok=False)
    for name in PRODUCT_FILES:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    (destination / 'Example comparison.html').write_text(example, encoding='utf8')
    manifest = [{'path':p.relative_to(destination).as_posix(), 'bytes':p.stat().st_size,
                 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in sorted(destination.rglob('*')) if p.is_file()]
    (destination / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2), encoding='utf8')
    # Exclusive creation never replaces another ZIP. Source and input files remain untouched.
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as output:
        for p in sorted(destination.rglob('*')):
            if p.is_file():
                output.write(p, destination.name + '/' + p.relative_to(destination).as_posix())
    return {'folder':str(destination), 'zip':str(archive), 'files':len(manifest)+1,
            'zip_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make a portable offline draft-review kit')
    parser.add_argument('destination', help='new kit folder; matching ZIP is created beside it')
    args = parser.parse_args()
    print(json.dumps(build(args.destination), indent=2))
