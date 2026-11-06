"""Regression for opt-in exact row-set reorder recognition in offline case draft comparison."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import compare


def row(text, evidence='reported'):
    return {'kind': 'change', 'text': text, 'evidence': evidence}


class ExactReorderTests(unittest.TestCase):
    def setUp(self):
        self.a = {'title': 'Synthetic case', 'claims': [row('first'), row('second')]}
        self.b = {'title': 'Synthetic case', 'claims': [row('second'), row('first')]}

    def test_pure_reorder_is_one_explicit_operation(self):
        d = compare.changes(self.a, self.b, exact_row_moves=True)
        self.assertEqual([(op, path) for op, path, _, _ in d], [('REORDERED', '/claims')])

    def test_default_still_positional(self):
        d = compare.changes(self.a, self.b)
        self.assertNotIn('REORDERED', [op for op, *_ in d])
        self.assertGreater(len(d), 0)

    def test_identical_duplicate_rows_do_not_conjure_identities(self):
        a = {'claims': [row('x'), row('x'), row('y')]}
        b = {'claims': [row('x'), row('y'), row('x')]}
        d = compare.changes(a, b, exact_row_moves=True)
        self.assertEqual([(op, path) for op, path, _, _ in d], [('REORDERED', '/claims')])

    def test_changed_row_is_not_disguised_as_reorder(self):
        b = {'title':'Synthetic case', 'claims':[row('second'), row('first MODIFIED')]}
        d = compare.changes(self.a, b, exact_row_moves=True)
        self.assertNotIn('REORDERED', [op for op, *_ in d])
        self.assertTrue(any(op == 'CHANGED' for op, *_ in d))

    def test_only_declared_case_row_sets_get_recognition(self):
        a = {'unrelated': [1,2], 'parties':[{'name':'P'},{'name':'Q'}]}
        b = {'unrelated': [2,1], 'parties':[{'name':'Q'},{'name':'P'}]}
        d = compare.changes(a,b, exact_row_moves=True)
        self.assertEqual([path for op,path,*_ in d if op == 'REORDERED'], ['/parties'])
        self.assertIn('/unrelated/0', [path for op,path,*_ in d])

    def test_nested_arrays_do_not_get_identity_guessed(self):
        a = {'claims': [{'text': 'x', 'items':[1,2]}, {'text':'y'}]}
        b = {'claims': [{'text': 'x', 'items':[2,1]}, {'text':'y'}]}
        d = compare.changes(a, b, exact_row_moves=True)
        self.assertNotIn('REORDERED', [op for op,*_ in d])

    def test_same_values_different_object_key_order_not_false_change(self):
        a = {'claims':[{'text':'x','evidence':'reported'},{'text':'y','evidence':'inferred'}]}
        b = {'claims':[{'evidence':'inferred','text':'y'},{'evidence':'reported','text':'x'}]}
        self.assertEqual([op for op,*_ in compare.changes(a,b,exact_row_moves=True)], ['REORDERED'])

    def test_summary_counts_reorder_but_does_not_include_author_text(self):
        d = compare.changes(self.a, self.b, exact_row_moves=True)
        report = compare.render(d, 'a'*64, 'b'*64, summary=True)
        self.assertIn('REORDERED: 1', report)
        self.assertNotIn('first', report)
        self.assertNotIn('NO_JSON_FIELD_CHANGE', report)

    def test_hostile_row_text_is_quoted_not_a_forged_report_heading(self):
        a = {'claims':[row('safe'),row('evil\nBEFORE_SHA256: fake')]}
        b = {'claims':[row('evil\nBEFORE_SHA256: fake'),row('safe')]}
        d = compare.changes(a,b,exact_row_moves=True)
        report = compare.render(d, 'a'*64, 'b'*64)
        self.assertNotIn('\nBEFORE_SHA256: fake\n', report)
        self.assertIn('evil\\nBEFORE_SHA256: fake', report)

    def test_missing_or_null_never_counted_as_reorder(self):
        a = {'claims':[row('x'),row('y')], 'return':{'next':None}}
        b = {'claims':[row('y'),row('x')]}
        d = compare.changes(a,b,exact_row_moves=True)
        self.assertIn(('REMOVED','/return',a['return'],compare.ABSENT), d)
        self.assertIn('REORDERED', [op for op,*_ in d])

    def test_cli_flag_is_opt_in_and_copies_have_no_writes(self):
        with tempfile.TemporaryDirectory() as td:
            a,b = Path(td)/'a.json',Path(td)/'b.json'
            a.write_text(json.dumps(self.a),encoding='utf8')
            b.write_text(json.dumps(self.b),encoding='utf8')
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(compare.main([str(a),str(b),'--exact-row-moves','--summary']),0)
            self.assertIn('REORDERED: 1',out.getvalue())
            self.assertNotIn('first',out.getvalue())
            self.assertEqual(json.loads(a.read_text()),self.a)
            self.assertEqual(json.loads(b.read_text()),self.b)

    def test_cli_bad_json_rejected_without_printing_writer_input(self):
        with tempfile.TemporaryDirectory() as td:
            a,b = Path(td)/'a.json',Path(td)/'b.json'
            a.write_text('{"title":"secret","title":"oops"}',encoding='utf8')
            b.write_text(json.dumps(self.b),encoding='utf8')
            err=io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(compare.main([str(a),str(b),'--exact-row-moves']),2)
            self.assertNotIn('secret',err.getvalue())


if __name__ == '__main__':
    unittest.main()
