"""A bounded detailed HTML report must not expand a small private draft into megabytes."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import compare
import html_report


class BoundedHtmlTests(unittest.TestCase):
    def setUp(self):
        # The common parent key is represented once in each 128 KiB JSON input,
        # but a separate, escaped JSON Pointer repeats it for every difference.
        self.private_key = 'PRIVATE_PARENT_' + 'z' * 4300
        self.before = {self.private_key: {'field_' + str(i): 'old' for i in range(650)}}
        self.after = {self.private_key: {'field_' + str(i): 'new' for i in range(650)}}
        self.raw_old = json.dumps(self.before).encode('utf-8')
        self.raw_new = json.dumps(self.after).encode('utf-8')
        self.assertLess(len(self.raw_old), compare.MAX_BYTES)
        self.assertLess(len(self.raw_new), compare.MAX_BYTES)

    def test_detailed_document_fails_before_giant_output(self):
        diffs = compare.changes(compare.parse_json(self.raw_old), compare.parse_json(self.raw_new))
        self.assertEqual(len(diffs), 650)
        with self.assertRaisesRegex(compare.CompareError, '2 MiB') as error:
            html_report.render_html(diffs, 'a' * 64, 'b' * 64)
        self.assertNotIn('PRIVATE_PARENT_', str(error.exception))

    def test_summary_still_small_and_no_private_paths_or_hashes(self):
        diffs = compare.changes(compare.parse_json(self.raw_old), compare.parse_json(self.raw_new))
        page = html_report.render_html(diffs, 'a' * 64, 'b' * 64, summary=True)
        self.assertLess(len(page.encode('utf-8')), 8192)
        self.assertIn('CHANGED: 650', page)
        self.assertNotIn('PRIVATE_PARENT_', page)
        self.assertNotIn('a' * 64, page)

    def test_cli_refusal_keeps_previous_output_and_inputs(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            old, new, out = p/'old.json', p/'new.json', p/'report.html'
            old.write_bytes(self.raw_old)
            new.write_bytes(self.raw_new)
            out.write_text('KEEP THE PREVIOUS REPORT', encoding='utf-8')
            error = io.StringIO()
            with contextlib.redirect_stderr(error):
                self.assertEqual(html_report.main([str(old), str(new), '-o', str(out)]), 2)
            self.assertEqual(out.read_text(encoding='utf-8'), 'KEEP THE PREVIOUS REPORT')
            self.assertEqual(old.read_bytes(), self.raw_old)
            self.assertEqual(new.read_bytes(), self.raw_new)
            self.assertIn('2 MiB', error.getvalue())
            self.assertNotIn('PRIVATE_PARENT_', error.getvalue())
            self.assertNotIn('Traceback', error.getvalue())

    def test_normal_detail_unchanged_and_literal(self):
        old, new = {'title': 'Before'}, {'title': '</code><h1>FAKE</h1>'}
        diffs = compare.changes(old, new)
        page = html_report.render_html(diffs, 'c'*64, 'd'*64)
        self.assertIn('&lt;/code&gt;&lt;h1&gt;FAKE&lt;/h1&gt;', page)
        self.assertIn('BEFORE_SHA256: ' + 'c'*64, page)
        self.assertLess(len(page.encode('utf-8')), 2 * 1024 * 1024)


if __name__ == '__main__':
    unittest.main()
