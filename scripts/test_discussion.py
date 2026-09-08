"""Checks editorial preservation and local destinations, not a reply service."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.text = []; self.links = []; self.ids = []; self.tags = []
    def handle_data(self, data): self.text.append(data)
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag); a = dict(attrs)
        if 'href' in a: self.links.append(a['href'])
        if 'id' in a: self.ids.append(a['id'])

class DiscussionTests(unittest.TestCase):
    def test_source_and_optional_local_links(self):
        raw = (ROOT / 'out/discussion/index.md').read_bytes()
        page_bytes = (ROOT / 'out/discussion/index.html').read_bytes()
        pins = json.loads((ROOT / 'out/manifest.json').read_bytes())['provenance']['discussion']
        self.assertEqual(hashlib.sha256(raw).hexdigest(), pins['markdown_sha256'])
        self.assertEqual(hashlib.sha256(page_bytes).hexdigest(), pins['html_sha256'])
        p = Page(); p.feed(page_bytes.decode()); plain = ''.join(p.text)
        for block in raw.decode().strip().split('\n\n'):
            expected = re.sub(r'^#{1,2} ', '', block)
            expected = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'\1', expected)
            self.assertIn(expected, plain)
        self.assertEqual(len(p.ids), 7); self.assertEqual(len(set(p.ids)), 7)
        self.assertFalse(set(p.tags) & {'script', 'form', 'iframe', 'input', 'object'})
        self.assertIn('It does not receive submissions.', plain)
        for link in p.links:
            url = urlsplit(urljoin('https://pleasestartfromhere.com/discussion/', link))
            if url.netloc != 'pleasestartfromhere.com': continue
            relative = unquote(url.path).lstrip('/')
            if url.path.endswith('/'): relative += 'index.html'
            target = ROOT / 'out' / relative
            self.assertTrue(target.is_file(), link)
            if url.fragment:
                q = Page(); q.feed(target.read_text(encoding='utf8'))
                self.assertIn(unquote(url.fragment), q.ids, link)

    def test_home_route_and_legacy_participation(self):
        p = Page(); p.feed((ROOT / 'out/index.html').read_text(encoding='utf8'))
        self.assertIn('https://pleasestartfromhere.com/discussion/', p.links)
        challenge = (ROOT / 'out/explore/challenge.html').read_text(encoding='utf8')
        self.assertIn('https://pleasestartfromhere.com/discussion/', challenge)
        self.assertIn('Legacy GitHub discussion and participation', challenge)
        self.assertIn('https://github.com/', challenge)

if __name__ == '__main__': unittest.main()
