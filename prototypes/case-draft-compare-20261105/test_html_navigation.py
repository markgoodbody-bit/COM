"""Static, offline navigation for long ME/TRACE authored-difference reports.

Synthetic source tests: do not prove screen-reader usability or real-world benefit.
"""
from html.parser import HTMLParser
import unittest

import html_report


class LinksAndHeadings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nav = False
        self.navigation = []
        self.heading_ids = []
        self.tabindex = []
        self.tags = []
        self.inline_urls = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append(tag)
        if tag == 'nav' and values.get('aria-label') == 'Jump to authored differences':
            self.nav = True
        if tag == 'a':
            self.inline_urls.append(values.get('href'))
            if self.nav:
                self.navigation.append(values.get('href'))
        if tag == 'h3':
            self.heading_ids.append(values.get('id'))
            self.tabindex.append(values.get('tabindex'))

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.nav = False


def sample(n):
    return [('CHANGED', '/claim/' + str(i), 'BEFORE', 'AFTER') for i in range(n)]


class NavigationTests(unittest.TestCase):
    def parse(self, page):
        parser = LinksAndHeadings()
        parser.feed(page)
        return parser

    def test_long_report_has_bounded_local_navigation_and_numbered_headings(self):
        page = html_report.render_html(sample(52), 'a'*64, 'b'*64)
        parsed = self.parse(page)
        self.assertEqual(parsed.navigation, ['#change-1', '#change-26', '#change-51'])
        self.assertEqual(parsed.heading_ids, ['change-' + str(i) for i in range(1, 53)])
        self.assertEqual(parsed.tabindex, ['-1'] * 52)
        self.assertTrue(all(href[1:] in parsed.heading_ids for href in parsed.navigation))
        self.assertIn('Change 27 of 52: Changed author field', page)
        self.assertIn('1–25', page)
        self.assertIn('26–50', page)
        self.assertIn('51–52', page)
        self.assertIn('@media print', page)
        self.assertIn('.jump{display:none}', page)
        self.assertEqual(len(page.encode('utf-8')) < html_report.MAX_HTML_BYTES, True)

    def test_short_and_identical_reports_do_not_add_navigation(self):
        for n in (0, 1, 25):
            with self.subTest(n=n):
                page = html_report.render_html(sample(n), 'a'*64, 'b'*64)
                self.assertEqual(self.parse(page).navigation, [])
                self.assertNotIn('Jump to authored differences', page)
                self.assertIn('No JSON field changes', page) if n == 0 else None

    def test_summary_has_no_navigation_or_author_data(self):
        page = html_report.render_html([('CHANGED', '/PRIVATE-TEXT', 'SECRETOLD', 'SECRETNEW')]*52,
                                       'a'*64, 'b'*64, summary=True)
        self.assertEqual(self.parse(page).navigation, [])
        self.assertNotIn('PRIVATE-TEXT', page)
        self.assertNotIn('SECRETOLD', page)
        self.assertNotIn('SECRETNEW', page)
        self.assertNotIn('a'*64, page)
        self.assertIn('CHANGED: 52', page)

    def test_untrusted_markup_cannot_become_navigation_or_scripts(self):
        attacker = '</h3><a href="https://example.invalid">Verified</a><script>bad()</script>'
        page = html_report.render_html([('CHANGED', attacker, attacker, 'safe')]*26,
                                       'a'*64, 'b'*64)
        parsed = self.parse(page)
        self.assertEqual(parsed.navigation, ['#change-1', '#change-26'])
        self.assertEqual(parsed.inline_urls, parsed.navigation)
        self.assertNotIn('script', parsed.tags)
        self.assertNotIn('https://example.invalid', parsed.inline_urls)
        self.assertEqual(len(parsed.heading_ids), 26)
        self.assertIn('&lt;/h3&gt;', page)

    def test_large_report_still_fails_budget_without_partial_data(self):
        from compare import CompareError
        long_path = '/PRIVATE_' + 'x'*5000
        with self.assertRaises(CompareError):
            html_report.render_html([('CHANGED', long_path, 'a', 'b')]*450,
                                    'a'*64, 'b'*64)


if __name__ == '__main__':
    unittest.main()
