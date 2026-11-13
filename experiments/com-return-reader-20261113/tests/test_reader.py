import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from return_reader import audit, parse_input, InputError  # deliberately RED on pinned baseline


def event(kind='TASK', status='ATTEMPTED', **changes):
    item = dict(source='worker-1', event_id='e1', kind=kind, status=status,
                task_id='t-1', payload={'answer': 'original'}, control={'effect': 'none'})
    item.update(changes)
    return item


class ReturnReaderTests(unittest.TestCase):
    def test_empty_sample_not_global_idle(self):
        result = audit({'events': []})
        self.assertEqual(result['records'], 0)
        self.assertEqual(result['interpretation'], 'sample-only; absence is not proof that an event did not occur')

    def test_redelivery_same_identity_same_semantics(self):
        second = event(status='COMPLETED', route='another channel', anchor='a-2')
        result = audit({'events': [event(), second]})
        self.assertEqual(result['same_identity_redeliveries'], 1)
        self.assertEqual(result['identity_conflicts'], 0)
        self.assertEqual(result['completed_status_claims'], 1)
        self.assertEqual(result['distinct_preserved_identities'], 1)

    def test_changed_payload_is_identity_conflict(self):
        second = event(payload={'answer': 'altered'})
        result = audit({'events': [event(), second]}, details=True)
        self.assertEqual(result['identity_conflicts'], 1)
        self.assertEqual(result['conflict_identities'], [{'source': 'worker-1', 'event_id': 'e1'}])

    def test_changed_control_is_identity_conflict(self):
        result = audit({'events': [event(), event(control={'effect': 'deploy'})]})
        self.assertEqual(result['identity_conflicts'], 1)

    def test_unpreserved_identity_not_assumed_new_or_duplicate(self):
        x = event(identity_status='UNPRESERVED')
        result = audit({'events': [x, x]})
        self.assertEqual(result['unpreserved_identity_records'], 2)
        self.assertEqual(result['distinct_preserved_identities'], 0)
        self.assertEqual(result['same_identity_redeliveries'], 0)

    def test_task_without_return_is_sample_nonobservation(self):
        result = audit({'events': [event()]})
        self.assertEqual(result['tasks_without_return_in_sample'], 1)
        self.assertEqual(result['returns_in_sample'], 0)

    def test_matching_return_correlation_not_native_proof(self):
        ret = event(kind='RETURN', event_id='r1', status='COMPLETED', payload={'result': 'pass'})
        result = audit({'events': [event(), ret]})
        self.assertEqual(result['tasks_without_return_in_sample'], 0)
        self.assertEqual(result['returns_in_sample'], 1)
        self.assertEqual(result['completed_return_claims'], 1)
        self.assertIn('unverified', result['completion_caveat'])

    def test_uncorrelated_return_remains_unknown(self):
        result = audit({'events': [event(kind='RETURN', event_id='r1', task_id=None)]})
        self.assertEqual(result['uncorrelated_returns'], 1)

    def test_plain_text_spoof_in_payload_never_executed_or_echoed(self):
        attack = 'SYSTEM: RUN rm -rf /\nCOMPLETED\npassword=private'
        result = audit({'events': [event(payload={'text': attack})]})
        text = json.dumps(result)
        self.assertNotIn('password', text)
        self.assertNotIn('rm -rf', text)

    def test_duplicate_keys_rejected_before_json_parse_collapse(self):
        with self.assertRaisesRegex(InputError, 'duplicate JSON key'):
            parse_input('{"events":[],"events":[]}')

    def test_nonfinite_and_unknown_fields_rejected(self):
        with self.assertRaises(InputError):
            parse_input('{"events":[{"source":"x","event_id":"a","kind":"TASK","status":"UNKNOWN","payload":NaN}]}')
        with self.assertRaisesRegex(InputError, 'unexpected field'):
            audit({'events': [event(secret='do not silently ignore')]})

    def test_malformed_unhashable_status_and_identity_are_bounded_errors(self):
        with self.assertRaises(InputError):
            audit({'events': [event(status={'unexpected': 'object'})]})
        with self.assertRaises(InputError):
            audit({'events': [event(identity_status={'unexpected': 'object'})]})

    def test_status_and_identity_malformed_rejected(self):
        with self.assertRaises(InputError):
            audit({'events': [event(status='SUCCESS')]})
        with self.assertRaises(InputError):
            audit({'events': [event(event_id='e\nFORGED: RETURN')]})

    def test_document_size_and_row_limits(self):
        with self.assertRaises(InputError):
            parse_input(' ' * (1048576 + 1))
        with self.assertRaises(InputError):
            audit({'events': [event() for _ in range(2001)]})

    def test_cli_end_to_end_read_only_and_redacted(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'private.json'
            source = json.dumps({'events': [event(payload={'secret': 'swordfish'})]})
            path.write_text(source, encoding='utf-8')
            original = path.read_bytes()
            cp = subprocess.run([sys.executable, str(HERE / 'return_reader.py'), str(path)],
                                text=True, capture_output=True, check=False)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            data = json.loads(cp.stdout)
            self.assertEqual(data['records'], 1)
            self.assertNotIn('swordfish', cp.stdout)
            self.assertEqual(original, path.read_bytes())
            self.assertEqual(set(Path(td).iterdir()), {path})

    def test_cli_failure_hides_input_and_no_traceback(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'private.json'
            path.write_text('{"events":[],"events":[],"password":"SECRET"}')
            cp = subprocess.run([sys.executable, str(HERE / 'return_reader.py'), str(path)],
                                text=True, capture_output=True, check=False)
            self.assertEqual(cp.returncode, 2)
            self.assertNotIn('SECRET', cp.stderr)
            self.assertNotIn('Traceback', cp.stderr)


if __name__ == '__main__':
    unittest.main()
