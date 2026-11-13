#!/usr/bin/env python3
"""Offline read-only inspection of *supplied* COM-style event records.

No network, task dispatch, subprocess, command execution, filesystem writes,
receipt authentication or native Workshop integration. This is an optional
normalised-event sample reader, not a COM/Workshop protocol implementation.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_EVENTS = 2_000
STATUSES = frozenset({'ATTEMPTED', 'ACCEPTED', 'COMPLETED', 'REJECTED', 'UNKNOWN'})
IDENTITIES = frozenset({'PRESERVED', 'UNPRESERVED', 'UNKNOWN'})
FIELDS = frozenset({
    'source', 'event_id', 'identity_status', 'kind', 'status', 'task_id',
    'payload', 'payload_ref', 'control', 'parents', 'in_reply_to',
    'route', 'anchor',
})
SEMANTIC = ('kind', 'task_id', 'payload', 'payload_ref', 'control', 'parents', 'in_reply_to')


class InputError(ValueError):
    """A bounded, non-echoing error about the supplied local data."""


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError('duplicate JSON key')
        result[key] = value
    return result


def _nonfinite(_value):
    raise InputError('non-finite JSON value')


def parse_input(text):
    if not isinstance(text, str):
        raise InputError('expected UTF-8 text')
    try:
        if len(text.encode('utf-8')) > MAX_BYTES:
            raise InputError('input exceeds 1 MiB')
        data = json.loads(text, object_pairs_hook=_unique_keys, parse_constant=_nonfinite)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InputError('invalid UTF-8 or JSON') from exc
    return _validated(data)


def _identifier(value, optional=False):
    if optional and value is None:
        return None
    if not isinstance(value, str) or not (1 <= len(value) <= 120) or not value.isprintable():
        raise InputError('invalid event identifier')
    if any(0x202A <= ord(x) <= 0x202E or 0x2066 <= ord(x) <= 0x2069
           or ord(x) in (0x200E, 0x200F, 0x061C) for x in value):
        raise InputError('invalid directional character in identifier')
    return value


def _validated(data):
    if not isinstance(data, dict) or set(data) != {'events'}:
        raise InputError('expected an object with only the events array')
    events = data['events']
    if not isinstance(events, list) or len(events) > MAX_EVENTS:
        raise InputError('events must be an array of at most 2000 entries')
    for row in events:
        if not isinstance(row, dict):
            raise InputError('event must be an object')
        if set(row) - FIELDS:
            raise InputError('event contains unexpected field')
        if not all(k in row for k in ('kind', 'status')):
            raise InputError('event requires kind and status')
        _identifier(row['kind'])
        if not isinstance(row['status'], str) or row['status'] not in STATUSES:
            raise InputError('unsupported event status')
        if not isinstance(row.get('identity_status', 'PRESERVED'), str) or row.get('identity_status', 'PRESERVED') not in IDENTITIES:
            raise InputError('unsupported identity preservation status')
        for key in ('source', 'event_id', 'task_id', 'in_reply_to'):
            if key in row:
                _identifier(row[key], optional=key in ('source', 'event_id', 'task_id', 'in_reply_to'))
        if 'parents' in row and not isinstance(row['parents'], (list, str, type(None))):
            raise InputError('invalid parents field')
    return data


def _semantic_key(row):
    # Distinguish omitted from explicitly null. Status and route metadata are
    # observations about the same semantic event; payload/control are not.
    return json.dumps({key: row[key] for key in SEMANTIC if key in row},
                      sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False)


def audit(data, details=False):
    """Audit a bounded input SAMPLE, never infer global work or authority state."""
    _validated(data)
    rows = data['events']
    groups = defaultdict(list)
    unpreserved = 0
    task_ids = set()
    return_ids = set()
    uncorr = 0
    completed_returns = 0
    for row in rows:
        src = row.get('source')
        eid = row.get('event_id')
        if row.get('identity_status', 'PRESERVED') != 'PRESERVED' or not src or not eid or src == 'UNKNOWN' or eid == 'UNKNOWN':
            unpreserved += 1
        else:
            groups[(src, eid)].append(row)
        if row['kind'] == 'TASK' and row.get('task_id'):
            task_ids.add(row['task_id'])
        if row['kind'] == 'RETURN':
            if row.get('task_id'):
                return_ids.add(row['task_id'])
            else:
                uncorr += 1
            if row['status'] == 'COMPLETED':
                completed_returns += 1
    conflicts = sorted([{'source': source, 'event_id': ident}
                        for (source, ident), observations in groups.items()
                        if len({_semantic_key(row) for row in observations}) > 1],
                       key=lambda pair: (pair['source'], pair['event_id']))
    duplicate_count = sum(len(observations) - 1 for observations in groups.values()
                          if len({_semantic_key(row) for row in observations}) == 1)
    statuses = Counter(row['status'] for row in rows)
    result = {
        'interpretation': 'sample-only; absence is not proof that an event did not occur',
        'records': len(rows),
        'distinct_preserved_identities': len(groups),
        'unpreserved_identity_records': unpreserved,
        'same_identity_redeliveries': duplicate_count,
        'identity_conflicts': len(conflicts),
        'status_claim_counts': {key: statuses[key] for key in sorted(STATUSES)},
        'completed_status_claims': statuses['COMPLETED'],
        'tasks_with_id_in_sample': len(task_ids),
        'returns_in_sample': sum(row['kind'] == 'RETURN' for row in rows),
        'uncorrelated_returns': uncorr,
        'tasks_without_return_in_sample': len(task_ids - return_ids),
        'completed_return_claims': completed_returns,
        'completion_caveat': 'All statuses, identities and anchors are author-supplied and unverified; no native work, authority or completion is established.',
    }
    if details:
        result['conflict_identities'] = conflicts
        result['task_ids_without_return_in_sample'] = sorted(task_ids - return_ids)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description='Inspect supplied COM-style JSON events without executing anything')
    parser.add_argument('input', help='local UTF-8 JSON file, or - for stdin')
    parser.add_argument('--details', action='store_true', help='also print event/task identifiers (may be sensitive)')
    args = parser.parse_args(argv)
    try:
        if args.input == '-':
            raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        else:
            with Path(args.input).open('rb') as stream:
                raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise InputError('input exceeds 1 MiB')
        result = audit(parse_input(raw.decode('utf-8')), details=args.details)
        print(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2))
        return 0
    except (InputError, OSError, UnicodeError, TypeError, ValueError, OverflowError) as exc:
        # Do not echo malformed input, including purported commands, payload or raw paths.
        kind = str(exc) if isinstance(exc, InputError) else 'unreadable or invalid local input'
        print('return-reader: ' + kind, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
