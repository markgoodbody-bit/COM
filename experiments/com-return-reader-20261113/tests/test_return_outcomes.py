"""Test-first, source-only outcome-claim divergence; not native verification."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from return_reader import audit, parse_input


def event(kind, eid, status, tid='t', source='worker', **kw):
    return dict(source=source, event_id=eid, kind=kind, status=status,
                task_id=tid, payload={'private': 'SWORD-FISH'}, **kw)


class DivergentReturnClaims(unittest.TestCase):
    def test_completed_and_rejected_claims_are_visible_without_verdict(self):
        rows = [event('TASK', 'task', 'ATTEMPTED'),
                event('RETURN', 'r1', 'COMPLETED'),
                event('RETURN', 'r2', 'REJECTED')]
        result = audit({'events': rows}, details=True)
        self.assertEqual(result['completed_return_claims'], 1)
        self.assertEqual(result['return_task_ids_with_divergent_terminal_claims_in_sample'], 1)
        self.assertEqual(result['return_terminal_records_on_divergent_task_ids_in_sample'], 2)
        self.assertEqual(result['return_task_ids_with_divergent_terminal_claims'], ['t'])
        self.assertIn('not proof', result['outcome_divergence_caveat'])

    def test_status_change_of_one_preserved_identity_is_still_observed(self):
        rows = [event('RETURN', 'r1', 'COMPLETED'), event('RETURN', 'r1', 'REJECTED')]
        report = audit({'events': rows})
        self.assertEqual(report['identity_conflicts'], 0)  # status not in semantic key
        self.assertEqual(report['return_task_ids_with_divergent_terminal_claims_in_sample'], 1)

    def test_attempted_to_completed_is_not_terminal_divergence(self):
        rows = [event('RETURN', 'r1', 'ATTEMPTED'), event('RETURN', 'r1', 'COMPLETED')]
        self.assertEqual(audit({'events': rows})['return_task_ids_with_divergent_terminal_claims_in_sample'], 0)

    def test_unknown_or_absent_task_ids_are_not_correlated(self):
        rows = [event('RETURN', 'r1', 'COMPLETED', 'UNKNOWN'),
                event('RETURN', 'r2', 'REJECTED', 'UNKNOWN'),
                event('RETURN', 'r3', 'COMPLETED', None),
                event('RETURN', 'r4', 'REJECTED', None)]
        report = audit({'events': rows})
        self.assertEqual(report['return_task_ids_with_divergent_terminal_claims_in_sample'], 0)
        self.assertEqual(report['uncorrelated_returns'], 4)

    def test_task_status_does_not_contribute_to_return_divergence(self):
        rows = [event('TASK', 'task', 'REJECTED'), event('RETURN', 'r1', 'COMPLETED')]
        self.assertEqual(audit({'events': rows})['return_task_ids_with_divergent_terminal_claims_in_sample'], 0)

    def test_two_ids_only_one_divergent_and_deterministic_details(self):
        rows = [event('RETURN', 'r1', 'REJECTED', 'z'),
                event('RETURN', 'r2', 'COMPLETED', 'z'),
                event('RETURN', 'r3', 'COMPLETED', 'a'),
                event('RETURN', 'r4', 'COMPLETED', 'a')]
        result = audit({'events': rows}, details=True)
        self.assertEqual(result['return_task_ids_with_divergent_terminal_claims'], ['z'])
        self.assertEqual(result['return_terminal_records_on_divergent_task_ids_in_sample'], 2)
        self.assertEqual(result['same_identity_redeliveries'], 0)

    def test_repeated_terminal_record_is_counted_as_record_not_unique_event(self):
        x = event('RETURN', 'r1', 'COMPLETED')
        rows = [x, dict(x, route='retry'), event('RETURN', 'r2', 'REJECTED')]
        report = audit({'events': rows})
        self.assertEqual(report['same_identity_redeliveries'], 1)
        self.assertEqual(report['return_terminal_records_on_divergent_task_ids_in_sample'], 3)

    def test_default_counts_only_no_task_or_private_text(self):
        rows = [event('RETURN', 'r1', 'COMPLETED', 'sensitive-ID'),
                event('RETURN', 'r2', 'REJECTED', 'sensitive-ID')]
        out = json.dumps(audit({'events': rows}))
        self.assertNotIn('sensitive-ID', out)
        self.assertNotIn('SWORD-FISH', out)
        self.assertIn('divergent_terminal_claims_in_sample', out)

    def test_all_outcome_claims_remain_unverified_even_unique(self):
        rows = [event('RETURN', 'r1', 'COMPLETED', 't')]
        result = audit({'events': rows})
        self.assertEqual(result['return_task_ids_with_divergent_terminal_claims_in_sample'], 0)
        self.assertIn('unverified', result['completion_caveat'])

    def test_real_cli_stdin_and_unchanged_legacy_counts(self):
        rows = [event('TASK', 'task', 'ATTEMPTED'), event('RETURN', 'r1', 'COMPLETED'),
                event('RETURN', 'r2', 'REJECTED')]
        raw = json.dumps({'events': rows})
        cp = subprocess.run([sys.executable, str(ROOT / 'return_reader.py'), '-'],
                            input=raw, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        result = json.loads(cp.stdout)
        self.assertEqual(result['tasks_without_return_in_sample'], 0)
        self.assertEqual(result['task_ids_with_noncolliding_task_and_return_candidate_in_sample'], 1)
        self.assertEqual(result['return_task_ids_with_divergent_terminal_claims_in_sample'], 1)
        self.assertNotIn('SWORD-FISH', cp.stdout)


if __name__ == '__main__':
    unittest.main()
