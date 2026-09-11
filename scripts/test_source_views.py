"""Static HTML-parser roundtrips, not provider emulation or browser QA."""
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import subprocess
import unittest
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = 'https://pleasestartfromhere.com'


class Reading(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.capture = False
        self.payload = []
        self.links = []
        self.tags = []
        self.ids = []
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        values = dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        if tag == 'code' and values.get('id') == 'source-text':
            self.capture = True
        if tag == 'a':
            self.links.append(values['href'])
    def handle_endtag(self, tag):
        if tag == 'code':
            self.capture = False
    def handle_data(self, data):
        if self.capture:
            self.payload.append(data)


def node(code):
    return subprocess.check_output(['node', '--input-type=module', '-e', code], cwd=ROOT).decode()


class SourceViewTests(unittest.TestCase):
    def test_four_complete_sources_and_actual_navigation(self):
        manifest = json.loads((ROOT / 'out/manifest.json').read_bytes())
        views = manifest['provenance']['html_source_text']
        self.assertEqual(len(views), 4)
        edition = subprocess.check_output(['node', '--input-type=module', '-e', "import {SITE_EDITION} from './scripts/site-edition.mjs';process.stdout.write(SITE_EDITION)"], cwd=ROOT).decode()
        self.assertEqual(manifest['site_edition'], edition)
        for view in views:
            raw = (ROOT / 'public' / view['source']).read_bytes()
            page = (ROOT / 'out' / view['output']).read_text(encoding='utf-8')
            parser = Reading()
            parser.feed(page)
            self.assertEqual(''.join(parser.payload).encode(), raw)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), view['sha256'])
            self.assertIn(view['sha256'], page)
            self.assertIn('Site Preview ' + edition, page)
            self.assertIn(ORIGIN + '/' + view['source'], parser.links)
            self.assertFalse(set(parser.tags) & {'script', 'iframe', 'form', 'object', 'embed'})
            self.assertEqual(parser.ids.count('source-text'), 1)
            notices = {
                'read/trace-spine.html': 'https://github.com/markgoodbody-bit/TRACE/blob/main/README.md#review-history-and-licence',
                'read/me-book.html': 'https://github.com/markgoodbody-bit/mechanical-ethics/blob/main/README.md#review-history-and-licence',
            }
            expected_notice = notices.get(view['output'])
            external = [href for href in parser.links if urlsplit(href).netloc == 'github.com']
            self.assertEqual(external, [expected_notice] if expected_notice else [])
            if expected_notice:
                self.assertLess(page.index(expected_notice), page.index('<code id="source-text">'))
            for href in parser.links:
                if href == expected_notice:
                    continue
                url = urlsplit(href)
                self.assertIn(url.scheme, ('', 'https'))
                self.assertIn(url.netloc, ('', 'pleasestartfromhere.com'))
                target = ROOT / 'out' / unquote(url.path).lstrip('/')
                if target.is_dir():
                    target /= 'index.html'
                self.assertTrue(target.is_file(), href)
                if url.fragment:
                    other = Reading()
                    other.feed(target.read_text(encoding='utf-8'))
                    self.assertIn(url.fragment, other.ids)

    def test_unicode_whitespace_markup_cr_and_bom_roundtrip(self):
        text = '\n\t café 雪 😀 &amp; </code><script>alert(1)</script>\r\n\r"\'\ufeff\n'
        code = "import {renderSource,digest} from './scripts/source-views.mjs'; const b=Buffer.from(" + json.dumps(text) + "); console.log(renderSource({source:'fixture.txt',title:'Fixture',edition:'test',sha256:digest(b)},b,[]));"
        page = node(code)
        parser = Reading()
        parser.feed(page)
        self.assertEqual(''.join(parser.payload), text)
        self.assertNotIn('script', parser.tags)

    def test_refuse_changed_invalid_utf8_and_nul(self):
        result = json.loads(node("import {renderSource,digest} from './scripts/source-views.mjs'; const cases=[Buffer.from([0]),Buffer.from([255]),Buffer.from('changed')]; console.log(JSON.stringify(cases.map(b=>{try{renderSource({source:'test',title:'test',edition:'test',sha256:digest(Buffer.from('original'))},b,[]);return false}catch{return true}})));"))
        self.assertEqual(result, [True, True, True])

    def test_paths_resolve_against_original_not_wrapper(self):
        result = json.loads(node("import {sourceReferences} from './scripts/source-views.mjs'; console.log(JSON.stringify(sourceReferences({source:'resources/mechanical-ethics/MECHANICAL_ETHICS.md'},'[diagram](figures/a.png)').map(([l,u])=>u.href)));"))
        self.assertEqual(result, [ORIGIN + '/resources/mechanical-ethics/figures/a.png'])


if __name__ == '__main__':
    unittest.main()
