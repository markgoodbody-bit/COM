import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("atrs_membership", ROOT / "membership.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)

PAGE = '''
<html><body>
<h3>152 records</h3>
<a href="/algorithmic-transparency-records/tool-a">Tool A</a>
<a href='/algorithmic-transparency-records/tool-b'>Tool B</a>
<a href="/algorithmic-transparency-records/tool-a">Tool A duplicate link</a>
<a href="/algorithmic-transparency-records/email-signup">Get emails</a>
<a href="?page=2" rel="next">Next page: 2 of 4</a>
</body></html>
'''
LAST = '''
<html><body><h2>152 records</h2>
<a href="/algorithmic-transparency-records/tool-c">Tool C</a>
<a href="/algorithmic-transparency-records/email-signup">Subscribe</a>
</body></html>
'''

class MembershipTests(unittest.TestCase):
    def test_parse_finder_page_deduplicates_and_excludes_utility_links(self):
        urls, count, next_page = mod.parse_finder_page(PAGE)
        self.assertEqual(urls, [
            "https://www.gov.uk/algorithmic-transparency-records/tool-a",
            "https://www.gov.uk/algorithmic-transparency-records/tool-b",
        ])
        self.assertEqual(count, 152)
        self.assertEqual(next_page, 2)

    def test_last_page_has_no_next(self):
        urls, count, next_page = mod.parse_finder_page(LAST)
        self.assertEqual(urls, ["https://www.gov.uk/algorithmic-transparency-records/tool-c"])
        self.assertEqual(count, 152)
        self.assertIsNone(next_page)

if __name__ == "__main__":
    unittest.main()
