#!/usr/bin/env python3
"""Offline positional comparison of two author-held ME/TRACE case-card JSON drafts.

Not an event, truth, identity, author, or ethical-change detector. No network usage.
"""
import argparse
from collections import Counter
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile

MAX_BYTES = 131072
MAX_DEPTH = 32
MAX_CHANGES = 1024
EXACT_ROW_SETS = frozenset(('claims', 'parties', 'possibilities'))
ABSENT = object()


class CompareError(ValueError):
    """Invalid or unsafe comparison input; input contents are not echoed in errors."""


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CompareError('duplicate JSON key')
        result[key] = value
    return result


def _bad_constant(_value):
    raise CompareError('non-finite JSON value')


def _preserved_float(token):
    """Refuse decimal values that the existing float/report path would round away."""
    value = float(token)
    if not math.isfinite(value):
        raise CompareError('non-finite JSON value')
    try:
        preserved = Decimal(token) == Decimal(repr(value))
    except (InvalidOperation, ValueError, OverflowError):
        raise CompareError('JSON number exceeds supported decimal range') from None
    if not preserved:
        raise CompareError('JSON number loses decimal precision; use a decimal-aware diff')
    return value


def _check_tree(item, depth=0):
    if depth > MAX_DEPTH:
        raise CompareError('JSON nesting exceeds limit')
    if isinstance(item, dict):
        for key, val in item.items():
            _check_text(key)
            _check_tree(val, depth + 1)
    elif isinstance(item, list):
        for val in item:
            _check_tree(val, depth + 1)
    elif isinstance(item, str):
        _check_text(item)
    elif isinstance(item, float) and not math.isfinite(item):
        # JSON's numeric exponent can overflow Python's float without invoking
        # parse_constant; reject it before distinct authored values collapse.
        raise CompareError('non-finite JSON value')


def _check_text(text):
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in text):
        raise CompareError('invalid surrogate in text')


def parse_json(raw):
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
        raise CompareError('input must be at most 128 KiB of UTF-8 JSON')
    try:
        item = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique,
                          parse_constant=_bad_constant, parse_float=_preserved_float)
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        if isinstance(exc, CompareError):
            raise
        raise CompareError('invalid UTF-8 JSON') from exc
    if not isinstance(item, dict):
        raise CompareError('top-level case draft must be a JSON object')
    _check_tree(item)
    return item


def _pointer(parts):
    return '/' + '/'.join(str(p).replace('~', '~0').replace('/', '~1') for p in parts)


def changes(before, after, exact_row_moves=False):
    """Positional exact changes; optionally recognize whole-row-set permutations.

    Missing keys/rows remain ABSENT, distinct from explicit JSON null.
    No inference of authorship, event changes or claim correctness is made.
    Exact row moves require equal JSON-value multisets; edited rows still use positional diff.
    """
    found = []

    def walk(old, new, path):
        if old is ABSENT or new is ABSENT:
            found.append(('ADDED' if old is ABSENT else 'REMOVED', _pointer(path), old, new))
        elif type(old) is not type(new):
            found.append(('CHANGED', _pointer(path), old, new))
        elif isinstance(old, dict):
            for k in sorted(set(old) | set(new)):
                walk(old.get(k, ABSENT), new.get(k, ABSENT), path + [k])
        elif isinstance(old, list):
            if (exact_row_moves and len(path) == 1 and path[0] in EXACT_ROW_SETS
                    and old != new and len(old) == len(new)
                    and all(isinstance(row, dict) for row in old + new)
                    and Counter(_quote(row) for row in old) == Counter(_quote(row) for row in new)):
                # This is a change in sequence, not evidence that any row/entity changed.
                # Duplicate identical rows have no inferred individual identities.
                found.append(('REORDERED', _pointer(path), old, new))
            else:
                for i in range(max(len(old), len(new))):
                    walk(old[i] if i < len(old) else ABSENT,
                         new[i] if i < len(new) else ABSENT, path + [i])
        elif old != new:
            found.append(('CHANGED', _pointer(path), old, new))
        if len(found) > MAX_CHANGES:
            raise CompareError('difference count exceeds limit')

    walk(before, after, [])
    return found


def _quote(value):
    if value is ABSENT:
        return '<ABSENT>'
    # ASCII JSON string escaping keeps untrusted values/keys on one literal line.
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'))


def render(differences, before_hash, after_hash, summary=False):
    counts = Counter(op for op, _, _, _ in differences)
    lines = [
        'ME/TRACE CASE DRAFT — LOCAL STRUCTURAL COMPARISON',
    ]
    if summary:
        # A digest of a private draft enables equality matching (and guesses
        # about small/known drafts). Counts are not anonymous either.
        lines.append('CONTENT_FINGERPRINTS_OMITTED: summary counts can still disclose information.')
    else:
        lines.extend(('BEFORE_SHA256: ' + before_hash, 'AFTER_SHA256: ' + after_hash))
    lines.extend([
        'ADDED: ' + str(counts['ADDED']) + ' | REMOVED: ' + str(counts['REMOVED']) +
        ' | CHANGED: ' + str(counts['CHANGED']) + ' | REORDERED: ' + str(counts['REORDERED']),
        'Comparison of author JSON, not a claim about real events, witnesses, standing,',
        'permission, evidence quality, or whether any correction was reached.',
        'List items compare by position by default; changes may reflect reordering, not changed identity.',
        'Opt-in REORDERED identifies only an exact whole-row-set permutation.',
        'REORDERED does not identify individual rows, authors, affected people or events.',
        'Absent is not the same as null or an explicit unknown label.',
    ])
    if not differences:
        lines.append('NO_JSON_FIELD_CHANGE (not a claim that the world remained unchanged).')
    elif not summary:
        for op, path, old, new in differences:
            lines.append(op + ' ' + _quote(path))
            lines.append('  before: ' + _quote(old))
            lines.append('  after:  ' + _quote(new))
    else:
        lines.append('SUMMARY_ONLY: paths, author values and file fingerprints omitted; counts remain share-sensitive.')
    return '\n'.join(lines) + '\n'


def _read(path):
    with Path(path).open('rb') as f:
        raw = f.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise CompareError('input exceeds 128 KiB limit')
    return raw


def _atomic(path, text):
    dest = Path(path)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                dir=str(dest.parent), prefix='.case-compare-', suffix='.tmp', delete=False) as f:
            tmp = f.name
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, dest)
        tmp = None
    finally:
        if tmp is not None and os.path.exists(tmp):
            os.unlink(tmp)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Compare two saved local case JSON drafts, never event truth')
    parser.add_argument('before', help='older author-held JSON draft')
    parser.add_argument('after', help='newer author-held JSON draft')
    parser.add_argument('--summary', action='store_true', help='counts only; omit author paths, values and content fingerprints (counts may still reveal information)')
    parser.add_argument('--exact-row-moves', action='store_true',
                        help='report exact whole-row permutations in claims/parties/possibilities as REORDERED')
    parser.add_argument('--output', '-o', help='atomically write report only after successful comparison')
    args = parser.parse_args(argv)
    try:
        if args.output and Path(args.output).resolve() in {Path(args.before).resolve(), Path(args.after).resolve()}:
            raise CompareError('output must not overwrite either input')
        a, b = _read(args.before), _read(args.after)
        result = render(changes(parse_json(a), parse_json(b), args.exact_row_moves),
                        sha256(a), sha256(b), args.summary)
        if args.output:
            _atomic(args.output, result)
        else:
            sys.stdout.write(result)
        return 0
    except (CompareError, OSError, UnicodeError, RecursionError) as exc:
        print('case-compare: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
