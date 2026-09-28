import json
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest

from capsule import CapsuleError
from human_view import main, render_html


class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags=[]
        self.links=[]
        self.ids=[]
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attrs=dict(attrs)
        if 'href' in attrs: self.links.append(attrs['href'])
        if 'id' in attrs: self.ids.append(attrs['id'])


class HumanViewTests(unittest.TestCase):
    def setUp(self):
        self.raw=(Path(__file__).parent/'examples/benign.json').read_bytes()
    def test_links_point_to_preserved_entries(self):
        page=render_html(self.raw)
        parsed=Structure(); parsed.feed(page)
        self.assertEqual(parsed.tags.count('article'),4)
        self.assertEqual(len(parsed.ids),len(set(parsed.ids)))
        self.assertTrue(all(h.startswith('#') and h[1:] in parsed.ids for h in parsed.links))
        self.assertIn('Dispute of entry 1',page)
        self.assertIn('Correction of entry 1',page)
    def test_html_payload_is_text_and_sources_are_not_links(self):
        data=json.loads(self.raw)
        data['entries'][0]['body']='<script>alert(1)</script><img src="https://example.com/pixel">'
        data['entries'][0]['sources']=['https://example.com/private?secret=example']
        page=render_html(json.dumps(data).encode())
        parsed=Structure(); parsed.feed(page)
        self.assertNotIn('script',parsed.tags)
        self.assertNotIn('img',parsed.tags)
        self.assertIn('&lt;script&gt;',page)
        self.assertTrue(all(h.startswith('#') for h in parsed.links))
    def test_withheld_and_duplicate_input_rejected(self):
        data=json.loads(self.raw); data['carry_forward']=False
        for raw in (json.dumps(data).encode(),b'{"format":1,"format":2}'):
            with self.assertRaises(CapsuleError): render_html(raw)
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'record.json'; source.write_bytes(self.raw)
            target=Path(folder)/'view.html'; target.write_text('keep')
            self.assertEqual(main(['viewer',str(source),str(target)]),1)
            self.assertEqual(target.read_text(),'keep')
    def test_empty_record(self):
        data=json.loads(self.raw); data['entries']=[]
        self.assertIn('This record contains no entries.',render_html(json.dumps(data).encode()))

    def test_overview_counts_labels_without_inventing_resolution(self):
        page=render_html(self.raw)
        for label in ('Notes: 1','Questions: 1','Disputes: 1','Corrections: 1'):
            self.assertIn(label,page)
        self.assertIn('Recorded questions',page)
        self.assertIn('Read question 2 in context',page)
        self.assertNotIn('Unresolved questions',page)
        self.assertIn('not a judgement',page)

    def test_question_excerpt_is_escaped_and_full_original_survives(self):
        data=json.loads(self.raw)
        body='<img src=x onerror=alert(1)>'+'x'*220+'END'
        data['entries'][1]['body']=body
        page=render_html(json.dumps(data).encode())
        parsed=Structure(); parsed.feed(page)
        self.assertNotIn('img',parsed.tags)
        self.assertIn('…',page)
        self.assertIn('x'*220+'END',page)
        self.assertTrue(all(h.startswith('#') and h[1:] in parsed.ids for h in parsed.links))


if __name__=='__main__': unittest.main()
