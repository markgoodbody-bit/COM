"""Bounded text-extraction check; not a provider emulator or browser test.

Run after npm run build. Tests body text plus the deliberately quieter start.json
anchor destination in the concrete-first opening. Not an attribute-free reader model.
"""
from html.parser import HTMLParser
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
URLS = tuple('https://pleasestartfromhere.com/explore/' + route for route in
             ('start.json', 'example/entry.md', 'challenge.md'))
HISTORY_URL = 'https://pleasestartfromhere.com/changes.html'
WORKS_ROUTE = '/works/'
WORKS_URL = 'https://pleasestartfromhere.com/works/'


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
        assert parser.links.count(WORKS_ROUTE) == 1, (relative, WORKS_ROUTE, parser.links.count(WORKS_ROUTE))
        assert 'Works' in text, relative

    guide = (ROOT / 'out/llms.txt').read_text(encoding='utf-8')
    for url in URLS:
        assert '](' + url + ')' in guide, url
    assert '](https://pleasestartfromhere.com/changes.md)' in guide
    assert '](' + WORKS_URL + ')' in guide
    assert 'not a ranking or representative canon' in guide

    arrival = json.loads((ROOT / 'out/explore/start.json').read_text(encoding='utf-8'))
    assert arrival['routes']['human_works'] == WORKS_ROUTE
    assert 'not a ranking or representative canon' in arrival['reading']

    for relative in (
        'out/works/index.html',
        'out/works/harriet-powers/index.html',
        'out/works/johannes-vermeer/index.html',
        'out/works/anna-atkins/index.html',
        'out/works/shen-zhou/index.html',
        'out/works/edmonia-lewis/index.html'):
        assert (ROOT / relative).is_file(), relative

    print('Core destinations retained; Works appears once as an optional homepage route, is bounded in machine orientation, and six no-JS Works HTML routes exist. No provider-access, usefulness or curation-quality claim.')
