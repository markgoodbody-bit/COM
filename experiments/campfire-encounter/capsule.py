"""Inspect a bounded export as untrusted data. Never write it into the store."""
import json

MAX_BYTES = 4_000_000
FIELDS = {'id', 'encounter', 'claimed_producer', 'body', 'relation',
          'target', 'carry', 'observed_route', 'acceptance_handle'}
RELATIONS = {'statement', 'response', 'dispute', 'correction', 'decline'}


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key')
        result[key] = value
    return result


def inspect_capsule(raw):
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
        raise ValueError('Expected bounded UTF-8 bytes')
    try:
        packet = json.loads(raw.decode('utf-8'), object_pairs_hook=_object,
                            parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))
    except (UnicodeError, RecursionError, json.JSONDecodeError) as error:
        raise ValueError('Malformed capsule') from error
    if not isinstance(packet, dict) or set(packet) != {'format', 'authority', 'identity_verified', 'entries'}:
        raise ValueError('Unsupported envelope')
    if (packet['format'] != 'campfire-synthetic-v3' or packet['authority'] != 'NONE'
            or packet['identity_verified'] is not False):
        raise ValueError('Unsupported format or authority/identity assertion')
    entries = packet['entries']
    if not isinstance(entries, list) or len(entries) > 100:
        raise ValueError('Entry bound exceeded')
    seen = set()
    encounter = None
    claims = []
    for row in entries:
        if not isinstance(row, dict) or set(row) != FIELDS:
            raise ValueError('Unsupported entry shape')
        for key in FIELDS - {'target', 'carry'}:
            limit = 8192 if key == 'body' else 128
            if not isinstance(row[key], str) or not row[key] or len(row[key].encode('utf-8')) > limit:
                raise ValueError('Invalid entry text')
        if row['id'] in seen or row['relation'] not in RELATIONS:
            raise ValueError('Duplicate entry or invalid relation')
        if type(row['carry']) is not int or row['carry'] != 1:
            raise ValueError('Export includes entry without declared carry permission')
        if encounter is None:
            encounter = row['encounter']
        if row['encounter'] != encounter:
            raise ValueError('Mixed encounters')
        if row['relation'] == 'statement':
            if row['target'] is not None:
                raise ValueError('Statement must not have a target')
        elif not isinstance(row['target'], str) or row['target'] not in seen:
            raise ValueError('Target absent or not earlier in this capsule')
        seen.add(row['id'])
        # Preserve what the source claims, but never turn it into local facts.
        claims.append({'source_entry': row, 'verification': 'UNVERIFIED_IMPORT'})
    return {'kind': 'untrusted-capsule-inspection', 'authority': 'NONE',
            'completeness': 'NOT_ESTABLISHED', 'identity_verified': False,
            'permission_verified': False, 'claims': claims}
