"""Local HTML destinations and anchors after the ordinary build; no network reads."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent / 'out'
ORIGIN = 'https://pleasestartfromhere.com/'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links = set(), []
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a' and 'name' in attrs:
            self.ids.add(attrs['name'])
        for name in ('href', 'src'):
            if attrs.get(name):
                self.links.append(attrs[name])
        if attrs.get('srcset'):
            self.links.extend(part.strip().split()[0] for part in attrs['srcset'].split(','))


def check():
    pages = {path.relative_to(ROOT).as_posix(): Page(path.read_text(encoding='utf-8'))
             for path in ROOT.rglob('*.html')}
    problems, checked, anchors = [], 0, 0
    for route, page in pages.items():
        for link in page.links:
            target = urlparse(urljoin(ORIGIN + route, link))
            if target.netloc != 'pleasestartfromhere.com' or target.scheme not in ('http', 'https'):
                continue
            relative = unquote(target.path).lstrip('/')
            file = (ROOT / relative).resolve()
            if not file.is_relative_to(ROOT.resolve()):
                problems.append([route, link, 'outside build']); continue
            if file.is_dir():
                file /= 'index.html'
            checked += 1
            if not file.is_file():
                problems.append([route, link, 'missing file']); continue
            key = file.relative_to(ROOT).as_posix()
            if target.fragment and key in pages:
                anchors += 1
                if unquote(target.fragment) not in pages[key].ids:
                    problems.append([route, link, 'missing HTML anchor'])
    result = dict(html_pages=len(pages), local_references=checked, html_anchors=anchors, problems=problems)
    print(json.dumps(result, indent=2))
    if problems:
        raise SystemExit(1)


if __name__ == '__main__':
    check()
