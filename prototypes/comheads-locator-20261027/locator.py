#!/usr/bin/env python3
"""Offline byte-pinned locator for a dated Markdown continuity file.

No interpretation of status, commands, authorisation, or freshness is performed.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MAX_SOURCE_BYTES = 1_048_576
HEADING = re.compile(r'^ {0,3}##[ \t]+(.+?)\s*$')
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')


class LocatorError(ValueError):
    pass


def load_source(path: Path, *, max_bytes: int = MAX_SOURCE_BYTES) -> bytes:
    if max_bytes < 0:
        raise LocatorError('max_bytes must be nonnegative')
    with path.open('rb') as stream:
        raw = stream.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise LocatorError('input exceeds local byte limit')
    return raw


def _physical_lines(raw: bytes) -> list[bytes]:
    # Only the actual LF byte is a Markdown physical line break here. Keep
    # original LF/CRLF bytes so the pinned section is exactly recoverable.
    parts = raw.split(b'\n')
    lines = [part + b'\n' for part in parts[:-1]]
    if parts[-1]:
        lines.append(parts[-1])
    return lines


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _make_section(lines: list[bytes], ordinal: int, title: str, start: int, end: int) -> dict:
    payload = b''.join(lines[start - 1:end]) if start else b''
    return {
        'ordinal': ordinal,
        'title': title,
        'first_line': start,
        'last_line': end,
        'byte_length': len(payload),
        'sha256': _sha(payload),
    }


def build_index(raw: bytes) -> dict:
    try:
        raw.decode('utf-8', errors='strict')
    except UnicodeDecodeError as exc:
        raise LocatorError('source is not valid UTF-8') from exc
    lines = _physical_lines(raw)
    headings = []
    fence_char = None
    fence_len = 0
    for number, line in enumerate(lines, start=1):
        text = line.decode('utf-8').rstrip('\r\n')
        fence = FENCE.match(text)
        if fence_char is not None:
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_len and not fence.group(2).strip():
                fence_char = None
                fence_len = 0
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
            continue
        heading = HEADING.match(text)
        if heading:
            headings.append((number, heading.group(1)))

    sections = []
    if not headings:
        sections.append(_make_section(lines, 0, 'SOURCE PREAMBLE', 1 if lines else 0, len(lines)))
    else:
        if headings[0][0] > 1:
            sections.append(_make_section(lines, 0, 'SOURCE PREAMBLE', 1, headings[0][0] - 1))
        for ordinal, (start, title) in enumerate(headings, start=1):
            end = headings[ordinal][0] - 1 if ordinal < len(headings) else len(lines)
            sections.append(_make_section(lines, ordinal, title, start, end))

    return {
        'source_sha256': _sha(raw),
        'source_bytes': len(raw),
        'source_line_count': len(lines),
        'section_count': len(sections),
        'sections': sections,
        '_lines': lines,
    }


def show_section(index: dict, ordinal: int) -> str:
    for section in index['sections']:
        if section['ordinal'] == ordinal:
            start, end = section['first_line'], section['last_line']
            return b''.join(index['_lines'][start - 1:end]).decode('utf-8') if start else ''
    raise LocatorError(f'section ordinal {ordinal} absent from this exact source')


def search_index(index: dict, term: str, *, max_results: int = 40, max_lines: int = 8) -> dict:
    if not term.strip():
        raise LocatorError('search term must be nonblank')
    if not (1 <= max_results <= 100 and 1 <= max_lines <= 20):
        raise LocatorError('result or line limit outside supported range')
    folded = term.casefold()
    hits = []
    for section in index['sections']:
        start, end = section['first_line'], section['last_line']
        match_lines = [n for n in range(start, end + 1)
                       if folded in index['_lines'][n - 1].decode('utf-8').casefold()]
        if match_lines:
            hits.append({
                'ordinal': section['ordinal'],
                'title': section['title'],
                'first_line': start,
                'last_line': end,
                'sha256': section['sha256'],
                'total_matching_lines': len(match_lines),
                'match_lines': match_lines[:max_lines],
                'additional_matching_lines': max(0, len(match_lines) - max_lines),
            })
    return {
        'source_sha256': index['source_sha256'],
        'query': term,
        'match_mode': 'literal Unicode casefold, whole physical lines; no semantic or temporal ranking',
        'total_matching_sections': len(hits),
        'returned_sections': min(len(hits), max_results),
        'truncated': len(hits) > max_results,
        'matches': hits[:max_results],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Local exact-source COMHEADS locator; JSON output only')
    parser.add_argument('source', type=Path, help='explicit local UTF-8 Markdown file (no fetch)')
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--find', metavar='TEXT', help='literal case-insensitive source-line search')
    selection.add_argument('--show', type=int, metavar='ORDINAL', help='emit exact chosen section text')
    parser.add_argument('--max-results', type=int, default=40)
    args = parser.parse_args(argv)
    try:
        index = build_index(load_source(args.source))
        if args.find is not None:
            report = search_index(index, args.find, max_results=args.max_results)
        elif args.show is not None:
            report = {
                'source_sha256': index['source_sha256'],
                'ordinal': args.show,
                'source_excerpt_only': True,
                'source_text': show_section(index, args.show),
            }
        else:
            report = {k: v for k, v in index.items() if k != '_lines'}
            report['disclaimer'] = ('Source-order index, not a current-state projection. '
                                    'Earlier/later and contradictory entries remain unadjudicated.')
        print(json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True))
        return 0
    except (OSError, LocatorError) as exc:
        print(f'LOCATOR_ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
