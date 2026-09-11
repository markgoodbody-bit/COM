"""Offline representation checks, never an alignment verdict or execution gate."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate key: ' + key)
        result[key] = value
    return result


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs)


def shape(value, rule, root, location, errors):
    if '$ref' in rule:
        return shape(value, root['$defs'][rule['$ref'].split('/')[-1]], root, location, errors)
    kind = rule.get('type')
    valid = {'object': isinstance(value, dict), 'array': isinstance(value, list),
             'string': isinstance(value, str), 'boolean': type(value) is bool}
    if kind and not valid.get(kind, False):
        errors.append(location + ': expected ' + kind)
        return
    if 'enum' in rule and value not in rule['enum']:
        errors.append(location + ': invalid enum')
    if isinstance(value, str) and len(value.strip()) < rule.get('minLength', 0):
        errors.append(location + ': empty text')
    if isinstance(value, dict):
        for key in rule.get('required', []):
            if key not in value:
                errors.append(location + '.' + key + ': missing')
        for key, item in value.items():
            if key not in rule.get('properties', {}):
                if rule.get('additionalProperties') is False:
                    errors.append(location + '.' + key + ': unknown field')
            else:
                shape(item, rule['properties'][key], root, location + '.' + key, errors)
    if isinstance(value, list):
        if len(value) < rule.get('minItems', 0):
            errors.append(location + ': too few items')
        if rule.get('uniqueItems') and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            errors.append(location + ': duplicate items')
        for i, item in enumerate(value):
            shape(item, rule.get('items', {}), root, f'{location}[{i}]', errors)


def validate(record, previous=None):
    schema = read(HERE / 'episode.schema.json')
    errors = []
    shape(record, schema, schema, 'episode', errors)
    if errors:
        return errors
    groups = ('evidence', 'affected', 'uncertainties', 'challenges', 'residue')
    ids = {}
    for group in groups:
        values = [item['id'] for item in record[group]]
        if len(values) != len(set(values)):
            errors.append(group + ': duplicate ids')
        ids[group] = set(values)
    for uncertainty in record['uncertainties']:
        if uncertainty['status'] == 'resolved' and not uncertainty['resolution_evidence']:
            errors.append(uncertainty['id'] + ': resolution requires evidence')
        for ref in uncertainty['resolution_evidence']:
            if ref not in ids['evidence']:
                errors.append(uncertainty['id'] + ': missing evidence ' + ref)
    for challenge in record['challenges']:
        for ref in challenge['evidence']:
            if ref not in ids['evidence']:
                errors.append(challenge['id'] + ': missing evidence ' + ref)
        if challenge['status'] != 'open' and not challenge['disposition']:
            errors.append(challenge['id'] + ': disposition missing')
    for party in record['affected']:
        if party['voice'] != 'direct' and not party['representation_limit']:
            errors.append(party['id'] + ': absent/proxy voice needs explicit limit')
    action = record['action']
    if action['mode'] == 'ACT' and action['scope'] not in record['authority']['granted_scopes']:
        errors.append('ACT scope not in recorded grant (record check, not permission)')
    if record['state'] == 'closed' and not record['closure_receipt']:
        errors.append('closed episode requires receipt; residue still remains')
    if previous is not None:
        prior_errors = validate(previous)
        if prior_errors:
            return errors + ['previous: ' + e for e in prior_errors]
        if previous['episode_id'] != record['episode_id']:
            errors.append('previous episode id differs')
        for group in groups:
            missing = {item['id'] for item in previous[group]} - ids[group]
            if missing:
                errors.append(group + ': history removed: ' + ', '.join(sorted(missing)))
        evidence_now = {item['id']: item for item in record['evidence']}
        for item in previous['evidence']:
            if item['id'] in evidence_now and evidence_now[item['id']] != item:
                errors.append(item['id'] + ': earlier evidence rewritten; append a correction instead')
        if not set(previous['authority']['granted_scopes']).issuperset(record['authority']['granted_scopes']):
            if record['authority']['basis'] == previous['authority']['basis']:
                errors.append('wider recorded grant needs a changed authority basis, not prior success')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('episode', type=Path)
    parser.add_argument('--previous', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(read(args.episode), read(args.previous) if args.previous else None)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, 'INVALID REPRESENTATION: ' + str(exc) + '\n')
    if errors:
        parser.exit(1, '\n'.join(errors) + '\n')
    print('STRUCTURE VALID ONLY: not goodness, internalized values, factual truth, authority or alignment.')


if __name__ == '__main__':
    main()
