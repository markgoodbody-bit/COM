"""Opt-in plain-text operator view of supplied sample claims; test-first."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import return_reader


def event(kind, eid, status, tid='task', source='fixture', **extra):
    return dict(source=source, event_id=eid, kind=kind, status=status,
                task_id=tid, payload={'writer_text': 'TOP SECRET\n## COMPLETED VERIFIED'}, **extra)


class BriefReadout(unittest.TestCase):
    def report(self, events):
        return return_reader.brief_report(return_reader.audit({'events': events}))

    def cli(self, events, *extra):
        return subprocess.run([sys.executable, str(ROOT / 'return_reader.py'), '-', *extra],
                              input=json.dumps({'events': events}), text=True,
                              capture_output=True)

    def test_empty_sample_is_explicitly_nonconclusive(self):
        out = self.report([])
        self.assertIn('0 records', out)
        self.assertIn('unverified', out.lower())
        self.assertIn('outside this sample', out)
        self.assertNotIn('nothing happened', out.lower())

    def test_divergent_terminal_claims_remain_review_signal(self):
        out = self.report([event('TASK', 'task-1', 'ATTEMPTED'),
                           event('RETURN', 'ret-1', 'COMPLETED'),
                           event('RETURN', 'ret-2', 'REJECTED')])
        self.assertIn('1 noncolliding match candidate', out)
        self.assertIn('1 RETURN record labelled COMPLETED', out)
        self.assertIn('1 task ID with both COMPLETED and REJECTED labels', out)
        self.assertNotIn('contradictory outcomes', out)
        self.assertNotIn('final status: COMPLETED', out)

    def test_missing_return_is_sample_local_not_accusation(self):
        out = self.report([event('TASK', 'task-1', 'ATTEMPTED')])
        self.assertIn('1 task ID without a matching RETURN in this sample', out)
        self.assertNotIn('task failed', out.lower())

    def test_preserved_collision_and_unpreserved_are_visible(self):
        rows = [event('TASK', 't1', 'ATTEMPTED', 'same', 'source-1'),
                event('TASK', 't2', 'ATTEMPTED', 'same', 'source-2'),
                event('RETURN', 'r1', 'COMPLETED', 'same', 'source-1'),
                dict(event('RETURN', 'r2', 'UNKNOWN', 'other'), identity_status='UNPRESERVED')]
        out = self.report(rows)
        self.assertIn('1 ambiguous task ID', out)
        self.assertIn('0 noncolliding match candidates', out)
        self.assertIn('1 record without preserved identity', out)
        self.assertIn('1 RETURN ID without an observed TASK in this sample', out)

    def test_no_payload_identifiers_route_or_heading_in_brief(self):
        secret = 'SENSITIVE-TASK-ID-## REJECTED'
        rows = [event('TASK', 'task-1', 'ATTEMPTED', secret, 'secret-source',
                      route='MALICIOUS HEADER'),
                event('RETURN', 'ret-1', 'COMPLETED', secret, 'secret-source')]
        out = self.report(rows)
        for prohibited in (secret, 'TOP SECRET', '## COMPLETED VERIFIED',
                           'MALICIOUS HEADER', 'secret-source', 'task-1'):
            self.assertNotIn(prohibited, out)
        self.assertEqual(len(out.splitlines()), 5)
        self.assertLess(len(out.encode('utf-8')), 700)

    def test_max_sample_remains_short_and_claims_only(self):
        rows = [event('RETURN', str(i), 'COMPLETED', 'id' + str(i)) for i in range(2000)]
        out = self.report(rows)
        self.assertIn('2000 records', out)
        self.assertLess(len(out.encode('utf-8')), 700)
        self.assertNotIn('id1999', out)

    def test_actual_cli_brief_is_text_not_json(self):
        cp = self.cli([event('TASK', 't1', 'ATTEMPTED'),
                       event('RETURN', 'r1', 'COMPLETED')], '--brief')
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.assertEqual(cp.stderr, '')
        self.assertTrue(cp.stdout.startswith('Supplied sample:'))
        self.assertNotIn('{', cp.stdout)
        self.assertNotIn('TOP SECRET', cp.stdout)

    def test_legacy_default_stays_json_and_contains_old_caveat(self):
        cp = self.cli([event('TASK', 't1', 'ATTEMPTED')])
        self.assertEqual(cp.returncode, 0, cp.stderr)
        parsed = json.loads(cp.stdout)
        self.assertEqual(parsed['records'], 1)
        self.assertIn('author-supplied and unverified', parsed['completion_caveat'])

    def test_brief_and_details_are_mutually_exclusive(self):
        cp = self.cli([], '--brief', '--details')
        self.assertNotEqual(cp.returncode, 0)
        self.assertNotIn('TOP SECRET', cp.stderr)
        self.assertNotIn('events', cp.stdout)

    def test_malformed_input_is_refused_without_echo(self):
        cp = subprocess.run([sys.executable, str(ROOT / 'return_reader.py'), '-', '--brief'],
                            input='{"events":[{"kind":"## VERIFIED", "status":"INVALID", "payload":"SECRET"}]}',
                            text=True, capture_output=True)
        self.assertEqual(cp.returncode, 2)
        self.assertNotIn('SECRET', cp.stderr)
        self.assertNotIn('VERIFIED', cp.stderr)
        self.assertEqual(cp.stdout, '')


if __name__ == '__main__':
    unittest.main()
