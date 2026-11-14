"""Regression tests for ambiguous string-only task/return correlation."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from return_reader import audit, parse_input


def task(source='sender', event_id='a', task_id='shared', **kwargs):
    return dict(source=source, event_id=event_id, kind='TASK', status='ATTEMPTED',
                task_id=task_id, payload={'p': 1}, **kwargs)


def ret(task_id='shared', **kwargs):
    return dict(source='receiver', event_id='r', kind='RETURN', status='COMPLETED',
                task_id=task_id, payload={'answer': 'sensitive'}, **kwargs)


class TaskCorrelationTests(unittest.TestCase):
    def test_same_task_id_from_two_sources_does_not_signal_unambiguous_match(self):
        r = audit({'events': [task(), task(source='other'), ret()]}, details=True)
        self.assertEqual(r['tasks_without_return_in_sample'], 0)  # historical string match
        self.assertEqual(r['task_ids_with_ambiguous_correlation_in_sample'], 1)
        self.assertEqual(r['task_ids_with_noncolliding_task_and_return_candidate_in_sample'], 0)
        self.assertEqual(r['return_records_with_ambiguous_task_id_in_sample'], 1)
        self.assertEqual(r['ambiguous_task_ids_in_sample'], ['shared'])
        self.assertEqual(r['ambiguous_task_id_reasons']['shared'], ['multiple_preserved_task_events'])

    def test_different_event_identity_same_source_also_ambiguous(self):
        r = audit({'events': [task(), task(event_id='b'), ret()]})
        self.assertEqual(r['task_ids_with_ambiguous_correlation_in_sample'], 1)

    def test_retry_same_preserved_identity_is_not_second_task(self):
        first = task()
        second = {**first, 'route': 'retry', 'status': 'ACCEPTED'}
        r = audit({'events': [first, second, ret()]})
        self.assertEqual(r['same_identity_redeliveries'], 1)
        self.assertEqual(r['task_ids_with_ambiguous_correlation_in_sample'], 0)
        self.assertEqual(r['task_ids_with_noncolliding_task_and_return_candidate_in_sample'], 1)

    def test_conflicting_task_semantics_cannot_be_silently_matched(self):
        altered = {**task(), 'payload': {'p': 2}}
        r = audit({'events': [task(), altered, ret()]})
        self.assertEqual(r['identity_conflicts'], 1)
        self.assertEqual(r['task_ids_with_ambiguous_correlation_in_sample'], 1)
        self.assertEqual(r['task_ids_with_noncolliding_task_and_return_candidate_in_sample'], 0)

    def test_missing_or_unpreserved_task_identity_is_ambiguous(self):
        r = audit({'events': [task(identity_status='UNPRESERVED'), ret()]})
        self.assertEqual(r['task_ids_with_ambiguous_correlation_in_sample'], 1)
        r2 = audit({'events': [task(source=None), ret()]})
        self.assertEqual(r2['task_ids_with_ambiguous_correlation_in_sample'], 1)

    def test_unknown_literal_is_not_an_id_or_a_matched_return(self):
        r = audit({'events': [task(task_id='UNKNOWN'), ret(task_id='UNKNOWN')]})
        self.assertEqual(r['tasks_with_id_in_sample'], 0)
        self.assertEqual(r['uncorrelated_returns'], 1)
        self.assertEqual(r['task_records_without_usable_id_in_sample'], 1)
        self.assertEqual(r['task_ids_with_noncolliding_task_and_return_candidate_in_sample'], 0)

    def test_orphan_return_is_bounded_nonobservation_not_fabricated_task(self):
        r = audit({'events': [ret(task_id='other')]}, details=True)
        self.assertEqual(r['return_ids_without_observed_task_in_sample'], 1)
        self.assertEqual(r['return_ids_without_observed_task'], ['other'])
        self.assertEqual(r['tasks_with_id_in_sample'], 0)
        self.assertEqual(r['tasks_without_return_in_sample'], 0)

    def test_absence_of_return_distinct_from_ambiguous_return(self):
        r = audit({'events': [task()]})
        self.assertEqual(r['tasks_without_return_in_sample'], 1)
        self.assertEqual(r['task_ids_with_ambiguous_correlation_in_sample'], 0)
        self.assertEqual(r['task_ids_with_noncolliding_task_and_return_candidate_in_sample'], 0)

    def test_counts_only_output_hides_identifiers_and_authored_text(self):
        r = audit({'events': [task(task_id='secret-task'), task(source='other', task_id='secret-task'), ret(task_id='secret-task')]})
        serialized = json.dumps(r)
        self.assertNotIn('secret-task', serialized)
        self.assertNotIn('sensitive', serialized)
        self.assertIn('sample', r['return_correlation_caveat'])

    def test_cli_stdin_bounded_and_no_echo(self):
        sample = json.dumps({'events': [task(), task(source='other'), ret()]})
        cp = subprocess.run([sys.executable, str(ROOT / 'return_reader.py'), '-'],
                            input=sample, capture_output=True, text=True)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        obj = json.loads(cp.stdout)
        self.assertEqual(obj['task_ids_with_ambiguous_correlation_in_sample'], 1)
        self.assertNotIn('sensitive', cp.stdout)


if __name__ == '__main__':
    unittest.main()
