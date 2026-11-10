"""Standalone source tests of the optional report destination contract.

A minimal explicit dependency fixture isolates review_drafts' location handling;
this does NOT rerun the inherited parser or HTML renderer suites.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent


def load_entry():
    compare = types.ModuleType('compare')
    class CompareError(ValueError):
        pass
    compare.CompareError = CompareError
    compare._read = lambda path: Path(path).read_bytes()
    compare.parse_json = lambda raw: json.loads(raw)
    compare.changes = lambda a, b: [('CHANGED', '/value', a.get('value'), b.get('value'))] if a != b else []
    compare.sha256 = lambda raw: hashlib.sha256(raw).hexdigest()
    compare._atomic = lambda path, report: Path(path).write_text(report, encoding='utf8')
    html_report = types.ModuleType('html_report')
    html_report.render_html = lambda diff, a, b, summary: '<html>COUNTS ONLY</html>' if summary else '<html>PRIVATE_CONTENT</html>'
    with mock.patch.dict(sys.modules, {'compare': compare, 'html_report': html_report}):
        spec = importlib.util.spec_from_file_location('return_review_entry', HERE / 'review_drafts.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    return mod


class ReportLocationTests(unittest.TestCase):
    def setUp(self):
        self.entry = load_entry()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source_dir = self.root / 'writer drafts & spaces'
        self.source_dir.mkdir()
        self.private_dir = self.root / 'chosen private reports'
        self.private_dir.mkdir()
        self.before = self.source_dir / 'earlier.json'
        self.after = self.source_dir / 'revised.json'
        self.before.write_text('{"value":"earlier"}', encoding='utf8')
        self.after.write_text('{"value":"later"}', encoding='utf8')
        self.prior = (self.before.read_bytes(), self.after.read_bytes())

    def test_explicit_parent_sends_only_new_report_to_chosen_directory(self):
        target = self.entry.review_files(self.before, self.after, report_parent=self.private_dir)
        self.assertEqual(target.parent.parent, self.private_dir)
        self.assertEqual(target.name, 'comparison.html')
        self.assertIn('PRIVATE_CONTENT', target.read_text())
        self.assertEqual(list(self.source_dir.glob('draft-review-*')), [])
        self.assertEqual((self.before.read_bytes(), self.after.read_bytes()), self.prior)

    def test_default_is_backward_compatible_and_never_overwrites(self):
        a = self.entry.review_files(self.before, self.after)
        b = self.entry.review_files(self.before, self.after)
        self.assertEqual(a.parent.parent, self.source_dir)
        self.assertNotEqual(a, b)
        self.assertEqual(a.read_text(), b.read_text())
        self.assertEqual((self.before.read_bytes(), self.after.read_bytes()), self.prior)

    def test_explicit_parent_is_existing_folder_not_new_parent(self):
        missing = self.root / 'does not exist'
        with self.assertRaises(self.entry.compare.CompareError):
            self.entry.review_files(self.before, self.after, report_parent=missing)
        self.assertFalse(missing.exists())
        with self.assertRaises(self.entry.compare.CompareError):
            self.entry.review_files(self.before, self.after, report_parent=self.before)
        self.assertEqual(list(self.source_dir.glob('draft-review-*')), [])

    def test_failed_parsing_does_not_create_report_even_with_selected_parent(self):
        self.after.write_text('not json', encoding='utf8')
        with self.assertRaises(json.JSONDecodeError):
            self.entry.review_files(self.before, self.after, report_parent=self.private_dir)
        self.assertEqual(list(self.private_dir.iterdir()), [])

    def test_failed_write_cleans_new_folder_but_keeps_existing_reports(self):
        old = self.private_dir / 'keep.html'
        old.write_text('KEEP ME', encoding='utf8')
        with mock.patch.object(self.entry.compare, '_atomic', side_effect=OSError('fixture')):
            with self.assertRaises(OSError):
                self.entry.review_files(self.before, self.after, report_parent=self.private_dir)
        self.assertEqual(old.read_text(), 'KEEP ME')
        self.assertEqual(list(self.private_dir.glob('draft-review-*')), [])
        self.assertEqual((self.before.read_bytes(), self.after.read_bytes()), self.prior)

    def test_cli_selected_private_folder_and_summary(self):
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            code = self.entry.main([str(self.before), str(self.after), '--summary', '--report-parent', str(self.private_dir)])
        self.assertEqual(code, 0)
        reports = list(self.private_dir.glob('draft-review-*/comparison.html'))
        self.assertEqual(len(reports), 1)
        self.assertIn('COUNTS ONLY', reports[0].read_text())
        self.assertIn('selected folder', stdout.getvalue())
        self.assertEqual(list(self.source_dir.glob('draft-review-*')), [])

    def test_cli_unavailable_parent_refuses_without_exposing_writer_text(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = self.entry.main([str(self.before), str(self.after), '--report-parent', str(self.root / 'missing')])
        self.assertEqual(code, 2)
        self.assertIn('No report created', err.getvalue())
        self.assertNotIn('later', err.getvalue())
        self.assertEqual(list(self.source_dir.glob('draft-review-*')), [])


if __name__ == '__main__':
    unittest.main()
