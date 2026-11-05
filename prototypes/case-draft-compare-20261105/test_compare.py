import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import compare

ROOT = Path(__file__).resolve().parent


def sample():
    return {
        'title': 'Imaginary bus-stop case',
        'claims': [{'kind': 'change', 'text': 'Notice may have moved', 'evidence': 'reported'}],
        'parties': [{'name': 'Passenger', 'aim': 'Find the stop'}],
        'correction': {'window': 'unknown'},
    }


class DraftCompareTests(unittest.TestCase):
    def test_label_downgrade_shown_as_writer_change_not_verified_event(self):
        a, b = sample(), sample()
        b['claims'][0]['evidence'] = 'observed'
        changes = compare.changes(a, b)
        self.assertEqual(changes, [('CHANGED', '/claims/0/evidence', 'reported', 'observed')])
        out = compare.render(changes, '0'*64, '1'*64)
        self.assertIn('"reported"', out)
        self.assertIn('"observed"', out)
        self.assertIn('author JSON', out)
        self.assertNotIn('Verified observation', out)

    def test_absent_distinct_from_explicit_null(self):
        a, b = sample(), sample()
        a.pop('correction')
        b['correction'] = None
        changes = compare.changes(a, b)
        self.assertEqual(len(changes), 1)
        self.assertIs(changes[0][2], compare.ABSENT)
        self.assertIsNone(changes[0][3])
        out = compare.render(changes, '0'*64, '1'*64)
        self.assertIn('<ABSENT>', out)
        self.assertIn('null', out)

    def test_deleted_option_is_not_assumed_retracted(self):
        a, b = sample(), sample()
        a['possibilities'] = [{'state':'possible', 'description':'Try another route'}]
        b['possibilities'] = []
        diff = compare.changes(a, b)
        self.assertEqual(diff[0][0], 'REMOVED')
        self.assertIn('/possibilities/0', diff[0][1])
        self.assertIn('may reflect reordering', compare.render(diff, '0'*64, '1'*64))

    def test_no_change_does_not_claim_world_unchanged(self):
        self.assertEqual(compare.changes(sample(), sample()), [])
        txt = compare.render([], '0'*64, '0'*64)
        self.assertIn('NO_JSON_FIELD_CHANGE', txt)
        self.assertIn('not a claim', txt)

    def test_hostile_text_and_keys_cannot_forge_headings(self):
        a, b = sample(), sample()
        b['title'] = 'line1\nSTATUS: VERIFIED\x85\u2028\x1b[31m'
        b['bad\nAUTHORITY'] = 'claimed\r\nPASS'
        out = compare.render(compare.changes(a, b), '0'*64, '1'*64)
        self.assertNotIn('line1\nSTATUS', out)
        self.assertNotIn('\x1b', out)
        self.assertNotIn('\x85', out)
        self.assertNotIn('\u2028', out)
        self.assertNotIn('bad\nAUTHORITY', out)
        self.assertIn('\\nSTATUS', out)
        self.assertIn('\\u0085', out)
        self.assertIn('\\u2028', out)

    def test_nonidentical_types_not_coerced(self):
        a, b = sample(), sample()
        a['extra'] = False
        b['extra'] = 0
        self.assertEqual(compare.changes(a, b), [('CHANGED', '/extra', False, 0)])

    def test_lists_diff_by_position_not_identity(self):
        a, b = sample(), sample()
        a['parties'] = [{'name':'A'}, {'name':'B'}]
        b['parties'] = [{'name':'B'}, {'name':'A'}]
        diff = compare.changes(a,b)
        self.assertEqual([d[1] for d in diff], ['/parties/0/name','/parties/1/name'])

    def test_strict_json_disallows_duplicate_keys(self):
        with self.assertRaisesRegex(compare.CompareError, 'duplicate'):
            compare.parse_json(b'{"title":"A","title":"B"}')

    def test_strict_json_disallows_nan(self):
        with self.assertRaises(compare.CompareError):
            compare.parse_json(b'{"x":NaN}')

    def test_only_top_level_objects(self):
        with self.assertRaises(compare.CompareError):
            compare.parse_json(b'[1,2]')

    def test_oversize_and_depth_fail_bounded(self):
        with self.assertRaises(compare.CompareError):
            compare.parse_json(b' ' * (compare.MAX_BYTES+1))
        data = {'a': 1}
        for _ in range(compare.MAX_DEPTH+2):
            data = {'a': data}
        with self.assertRaises(compare.CompareError):
            compare.parse_json(json.dumps(data).encode())

    def test_summary_does_not_echo_values_or_paths(self):
        a, b = sample(), sample()
        b['title'] = 'PRIVATE-ZZ-1122'
        out = compare.render(compare.changes(a,b), '0'*64, '1'*64, summary=True)
        self.assertIn('CHANGED: 1',out)
        self.assertNotIn('PRIVATE-ZZ-1122',out)
        self.assertNotIn('/title',out)

    def test_exact_change_limit_is_accepted_and_next_is_rejected(self):
        a = {'items': [0] * compare.MAX_CHANGES}
        b = {'items': [1] * compare.MAX_CHANGES}
        self.assertEqual(len(compare.changes(a, b)), compare.MAX_CHANGES)
        a['z_last_equal'] = 5
        b['z_last_equal'] = 5
        self.assertEqual(len(compare.changes(a, b)), compare.MAX_CHANGES)
        b['one_more'] = 'x'
        with self.assertRaises(compare.CompareError):
            compare.changes(a, b)

    def test_invalid_utf8_and_surrogate_rejected(self):
        with self.assertRaises(compare.CompareError):
            compare.parse_json(b'{"a":"\xff"}')
        with self.assertRaises(compare.CompareError):
            compare.parse_json(b'{"a":"\\ud800"}')

    def test_structural_not_schema_validation(self):
        parsed = compare.parse_json(b'{"some_other_tool":true}')
        self.assertEqual(parsed, {'some_other_tool': True})

    def test_cli_real_files_atomic_output_and_byte_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            before, after, report = p/'before.json',p/'after.json',p/'report.txt'
            before.write_text(json.dumps(sample()),encoding='utf-8')
            edited = sample(); edited['claims'][0]['text'] = 'Writer corrected account'
            after.write_text(json.dumps(edited),encoding='utf-8')
            cp = subprocess.run([sys.executable,str(ROOT/'compare.py'),str(before),str(after),'--output',str(report)],capture_output=True,text=True)
            self.assertEqual(cp.returncode,0,cp.stderr)
            self.assertIn('Writer corrected account',report.read_text())
            self.assertIn(compare.sha256(before.read_bytes()),report.read_text())
            after.write_text('{"title":"x","title":"y"}',encoding='utf-8')
            cp = subprocess.run([sys.executable,str(ROOT/'compare.py'),str(before),str(after),'--output',str(report)],capture_output=True,text=True)
            self.assertEqual(cp.returncode,2)
            self.assertIn('Writer corrected account',report.read_text())
            self.assertNotIn('Traceback',cp.stderr)

    def test_cli_prohibits_output_overwriting_inputs(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'sample.json'
            p.write_text(json.dumps(sample()))
            cp=subprocess.run([sys.executable,str(ROOT/'compare.py'),str(p),str(p),'--output',str(p)],capture_output=True,text=True)
            self.assertEqual(cp.returncode,2)
            self.assertEqual(json.loads(p.read_text()),sample())


if __name__ == '__main__':
    unittest.main()
