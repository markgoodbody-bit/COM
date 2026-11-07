"""Synthetic offline HTML reader regression for optional case-draft comparison."""
import contextlib
import io
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

import compare
import html_report


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []
        self.attrs = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.attrs.extend(attrs)

    def handle_data(self, data):
        self.text.append(data)


def report(old, new, summary=False, exact=False):
    a = json.dumps(old, ensure_ascii=False).encode('utf-8')
    b = json.dumps(new, ensure_ascii=False).encode('utf-8')
    result = compare.changes(compare.parse_json(a), compare.parse_json(b), exact)
    return html_report.render_html(result, compare.sha256(a), compare.sha256(b), summary=summary)


class HtmlReportTests(unittest.TestCase):
    def test_changed_author_text_remains_literal_without_markup(self):
        bad = '</pre><script>alert(1)</script>\nBEFORE_SHA256: false'
        page = report({'title':'Before'}, {'title':bad})
        p = DocumentParser(); p.feed(page)
        self.assertNotIn('script', p.tags)
        self.assertNotIn('iframe', p.tags)
        self.assertNotIn('img', p.tags)
        self.assertIn('&lt;/pre&gt;', page)
        self.assertNotIn('<script>', page)
        self.assertIn('BEFORE_SHA256', ''.join(p.text))
        self.assertEqual(p.tags.count('h1'), 1)
        self.assertEqual(p.tags.count('h2'), 1)
        self.assertEqual(p.tags.count('h3'), 1)

    def test_key_heading_spoof_cannot_add_sections(self):
        page = report({}, {'</h2><h1>VERIFIED</h1>': 'x'})
        p = DocumentParser(); p.feed(page)
        self.assertEqual(p.tags.count('h1'), 1)
        self.assertNotIn('<h1>VERIFIED', page)
        self.assertIn('&lt;~1h2&gt;', page)  # RFC 6901 escapes slash within the path

    def test_add_remove_null_and_unknown_remain_distinct(self):
        a = {'correction': {'window': 'unknown', 'basis': None}}
        b = {'correction': {'window': None, 'target': 'unknown'}}
        page = report(a,b)
        p = DocumentParser(); p.feed(page)
        text = ' '.join(p.text)
        self.assertIn('Added author field', text)
        self.assertIn('Removed author field', text)
        self.assertIn('Changed author field', text)
        self.assertIn('null', text)
        self.assertIn('<ABSENT>', text)
        self.assertIn('"unknown"', text)

    def test_summary_omits_all_author_paths_and_values(self):
        page = report({'secret/path': 'PRIVATETEXT'}, {'secret/path': 'PRIVATEOTHER'}, summary=True)
        self.assertNotIn('PRIVATETEXT', page)
        self.assertNotIn('PRIVATEOTHER', page)
        self.assertNotIn('secret/path', page)
        self.assertIn('Summary only', page)
        self.assertIn('CHANGED', page)

    def test_no_change_not_asserted_as_world_unchanged(self):
        page = report({'title': 'unchanged'}, {'title':'unchanged'})
        self.assertIn('No JSON field changes', page)
        self.assertIn('not evidence that real events remained unchanged', page)

    def test_exact_reorder_is_labeled_not_identity(self):
        rows = [{'kind': 'change', 'text': 'A'}, {'kind': 'change', 'text': 'B'}]
        a={'claims':rows}; b={'claims':list(reversed(rows))}
        page=report(a,b,exact=True)
        self.assertIn('Reordered exact row set', page)
        self.assertIn('No row identity is inferred', page)
        self.assertIn('REORDERED', page)
        self.assertIn('/claims', page)

    def test_printable_offline_document_and_no_resources(self):
        page=report({}, {'title':'A'})
        p=DocumentParser(); p.feed(page)
        self.assertTrue(page.startswith('<!doctype html>'))
        self.assertIn('lang="en"', page)
        self.assertIn('@media print', page)
        self.assertNotIn('<script', page)
        self.assertNotIn('<link', page)
        self.assertNotIn('<img', page)
        self.assertNotIn('http://', page)
        self.assertNotIn('https://', page)
        self.assertEqual(len([tag for tag,val in p.attrs if tag in ('href','src')]),0)

    def test_cli_atomic_fails_without_overwriting(self):
        with tempfile.TemporaryDirectory() as d:
            old=Path(d)/'old.json'; new=Path(d)/'new.json'; out=Path(d)/'view.html'
            old.write_text('{"claims": []}',encoding='utf-8')
            new.write_text('{"claims": [NaN]}', encoding='utf-8')
            out.write_text('KEEP', encoding='utf-8')
            with contextlib.redirect_stderr(io.StringIO()):
                rc=html_report.main([str(old),str(new),'--output',str(out)])
            self.assertEqual(rc,2)
            self.assertEqual(out.read_text(), 'KEEP')

    def test_cli_success_and_source_guard(self):
        with tempfile.TemporaryDirectory() as d:
            old=Path(d)/'old.json'; new=Path(d)/'new.json'; out=Path(d)/'view.html'
            old.write_text('{"title":"old"}',encoding='utf-8')
            new.write_text('{"title":"new"}',encoding='utf-8')
            self.assertEqual(html_report.main([str(old),str(new),'--output',str(out)]),0)
            self.assertIn('Changed author field',out.read_text(encoding='utf-8'))
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(html_report.main([str(old),str(new),'--output',str(old)]),2)
            self.assertEqual(old.read_text(encoding='utf-8'),'{"title":"old"}')

    def test_rejects_numeric_overflow_inherited_from_comparator(self):
        with tempfile.TemporaryDirectory() as d:
            old=Path(d)/'old.json'; new=Path(d)/'new.json'
            old.write_text('{"x": 1e999}',encoding='utf-8')
            new.write_text('{"x": 2e999}',encoding='utf-8')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(html_report.main([str(old),str(new)]),2)


if __name__ == '__main__':
    unittest.main()
