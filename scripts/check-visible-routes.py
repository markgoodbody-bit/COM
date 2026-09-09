"""Bounded text-extraction check; not a provider emulator or browser test.

Run after npm run build. Tests body text plus the deliberately quieter start.json
anchor destination in the concrete-first opening. Not an attribute-free reader model.
"""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URLS = tuple('https://pleasestartfromhere.com/explore/' + route for route in
             ('start.json', 'example/entry.md', 'challenge.md'))
HISTORY_URL = 'https://pleasestartfromhere.com/changes.html'


class BodyText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_body = False
        self.hidden = 0
        self.parts = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
        if tag in ('script', 'style'):
            self.hidden += 1
        if self.in_body and not self.hidden and tag == 'a':
            self.links.append(dict(attrs).get('href'))

    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
        if tag in ('script', 'style'):
            self.hidden -= 1

    def handle_data(self, data):
        if self.in_body and not self.hidden:
            self.parts.append(data)


if __name__ == '__main__':
    for relative in ('out/index.html', 'downloads/Campfire-preview.html'):
        parser = BodyText()
        parser.feed((ROOT / relative).read_text(encoding='utf-8'))
        text = ' '.join(parser.parts)
        for url in (*URLS, HISTORY_URL):
            assert parser.links.count(url) == 1, (relative, url, parser.links.count(url))
            if url == URLS[0]:
                assert 'Compact text and machine routes:' in text, relative
                assert 'start.json' in text, relative
            else:
                assert text.count(url) == 1, (relative, url, text.count(url))
    guide = (ROOT / 'out/llms.txt').read_text(encoding='utf-8')
    for url in URLS:
        assert '](' + url + ')' in guide, url
    assert '](https://pleasestartfromhere.com/changes.md)' in guide
    print('Three reading destinations and history link retained; example/challenge/history URLs remain visible, start.json uses its compact label. Guide links are absolute. No attribute-free start.json, provider-access or usability claim.')
