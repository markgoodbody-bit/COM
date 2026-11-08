"""Regression: summary reports cannot link author drafts by deterministic content hash."""
import contextlib
import io
import re
import tempfile
import unittest
from pathlib import Path

import compare
import html_report


class SummaryPrivacyTests(unittest.TestCase):
    def setUp(self):
        self.before = b'{"private": "PERSONAL-WRITER-ONE", "claims": [{"text": "A"}, {"text": "B"}]}'
        self.after = b'{"private": "PERSONAL-WRITER-TWO", "claims": [{"text": "B"}, {"text": "A"}]}'
        self.diffs = compare.changes(compare.parse_json(self.before), compare.parse_json(self.after), True)
        self.h1, self.h2 = compare.sha256(self.before), compare.sha256(self.after)

    def _assert_private_summary(self, page):
        for secret in (self.h1, self.h2, 'PERSONAL-WRITER-ONE', 'PERSONAL-WRITER-TWO', '/private'):
            self.assertNotIn(secret, page)
        self.assertNotRegex(page, re.compile(r'[A-Fa-f0-9]{64}'))
        self.assertIn('CHANGED', page)
        self.assertIn('REORDERED', page)
        self.assertIn('fingerprint', page.lower())
        self.assertIn('counts', page.lower())

    def test_text_summary_omits_content_fingerprints_and_writer_data(self):
        page = compare.render(self.diffs, self.h1, self.h2, summary=True)
        self._assert_private_summary(page)

    def test_html_summary_omits_content_fingerprints_and_writer_data(self):
        page = html_report.render_html(self.diffs, self.h1, self.h2, summary=True)
        self._assert_private_summary(page)

    def test_text_full_retains_fingerprints_and_exact_fields(self):
        page = compare.render(self.diffs, self.h1, self.h2)
        self.assertIn(self.h1, page)
        self.assertIn(self.h2, page)
        self.assertIn('PERSONAL-WRITER-TWO', page)

    def test_html_full_retains_fingerprints_and_exact_fields(self):
        page = html_report.render_html(self.diffs, self.h1, self.h2)
        self.assertIn(self.h1, page)
        self.assertIn(self.h2, page)
        self.assertIn('PERSONAL-WRITER-TWO', page)

    def test_cli_summary_both_outputs_never_emits_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d)/'old.json', Path(d)/'new.json'
            a.write_bytes(self.before); b.write_bytes(self.after)
            for entry in (compare.main, html_report.main):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    rc = entry([str(a), str(b), '--summary', '--exact-row-moves'])
                self.assertEqual(rc, 0)
                self._assert_private_summary(out.getvalue())

    def test_atomic_output_retains_previous_on_invalid_input(self):
        with tempfile.TemporaryDirectory() as d:
            a, b, dest = (Path(d)/p for p in ('old.json','new.json','summary.txt'))
            a.write_bytes(self.before); b.write_bytes(b'{"x":1e999}')
            dest.write_text('ORIGINAL', encoding='utf-8')
            for entry in (compare.main, html_report.main):
                with contextlib.redirect_stderr(io.StringIO()):
                    rc = entry([str(a), str(b), '--summary', '-o', str(dest)])
                self.assertEqual(rc, 2)
                self.assertEqual(dest.read_text(encoding='utf-8'), 'ORIGINAL')

    def test_no_difference_summary_remains_honest(self):
        same = compare.changes(compare.parse_json(self.before), compare.parse_json(self.before))
        for fn in (compare.render, html_report.render_html):
            page = fn(same, self.h1, self.h1, summary=True)
            self.assertNotIn(self.h1, page)
            self.assertIn('CHANGED', page)
            if fn is compare.render:
                self.assertIn('not a claim that the world remained unchanged', page)
            else:
                self.assertIn('It does not verify events', page)


if __name__ == '__main__':
    unittest.main()
