"""Offline structure and preservation tests, not evidence of reader benefit."""
import copy
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import build_trial as b

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.tags=[]; self.text=[]
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        for key,value in attrs:
            if key in ('href','src'): self.links.append(value)
    def handle_data(self, value): self.text.append(value)

class TrialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=b.HERE.parent/'library.json'
        cls.lib=b.load_library(cls.path)
        cls.files,cls.report=b.generate(cls.path)
        cls.f=next(x for x in cls.lib['nodes'] if x['id']=='futures')
    def test_small_start_and_determinism(self):
        self.assertLess(len(self.files['start.json']),1400)
        self.assertEqual(b.generate(self.path),(self.files,self.report))
        self.assertEqual(len(self.files),24)
    def test_all_card_links_resolve_without_homepage(self):
        for ident in b.IDS:
            obj=json.loads(self.files[ident+'.json'])
            self.assertIn('Optional reference',obj['boundary'])
            self.assertIn('NO READER RESULT',obj['status'])
            self.assertEqual(obj['basis'],'basis.json')
            self.assertTrue(any(e['move']=='bundle' for e in obj['routes']))
            for e in obj['routes']:
                b.safe_link(e['href'])
                if not urlsplit(e['href']).scheme: self.assertIn(e['href'],self.files)
    def test_html_routes_and_safe_tags(self):
        for name,data in self.files.items():
            if name.endswith('.html'):
                page=Page();page.feed(data.decode())
                self.assertFalse({'script','form','iframe','img','object'} & set(page.tags))
                for href in page.links:
                    if not urlsplit(href).scheme: self.assertIn(href,self.files)
    def test_same_fields_and_navigation_in_all_three_forms(self):
        for ident in b.IDS:
            obj=json.loads(self.files[ident+'.json'])
            md=self.files[ident+'.md'].decode()
            page=Page();page.feed(self.files[ident+'.html'].decode()); text=' '.join(page.text)
            for heading,body in obj['sections']:
                self.assertIn(body,md);self.assertIn(body,text)
            for e in obj['routes']:
                self.assertIn(e['label'],md);self.assertIn(e['label'],text)
    def test_source_wording_preserved(self):
        mapping={'futures':('short','challenge','question'),'detail':('short','detail','challenge'),
                 'perspective':('short','perspective','challenge'),'challenge':('challenge',)}
        for ident,fields in mapping.items():
            values=[v for k,v in json.loads(self.files[ident+'.json'])['sections']]
            for field in fields:self.assertIn(self.f[field],values)
    def test_small_account_keeps_counterexample(self):
        obj=json.loads(self.files['futures.json'])
        self.assertIn(self.f['challenge'],[v for k,v in obj['sections']])
        self.assertIn('predation',self.files['futures.json'].decode())
    def test_challenge_is_not_claimed_independent(self):
        self.assertIn('not independent criticism',self.files['challenge.json'].decode())
        self.assertIn('not testimony',self.files['perspective.json'].decode())
        self.assertIn('GitHub account',self.files['challenge.json'].decode())
    def test_packet_reuses_exact_records(self):
        packet=json.loads(self.files['packet.json'])
        self.assertEqual(packet['cards'],[json.loads(self.files[k+'.json']) for k in b.IDS])
        for card in packet['cards']:
            for _,body in card['sections']:
                self.assertIn(body,self.files['packet.md'].decode())
    def test_no_source_mutation(self):
        original=copy.deepcopy(self.lib);b.cards(self.lib);self.assertEqual(original,self.lib)
        self.assertEqual(b.sha(self.path.read_bytes()),b.LIBRARY_SHA256)
    def test_changed_source_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'library.json';p.write_bytes(self.path.read_bytes()+b' ')
            with self.assertRaises(ValueError):b.generate(p)
    def test_bad_links_refused(self):
        for href in ('../secret','/secret','data:text/plain,hello','https://user:pass@example.com','//evil.test/x','missing.json'):
            with self.subTest(href=href):
                with self.assertRaises(ValueError):b.safe_link(href)
    def test_html_escapes_text(self):
        obj=b.cards(self.lib)['start'];obj['sections']=[('H','<script>alert(1)</script>')]
        page=Page();page.feed(b.render(obj,'.html').decode())
        self.assertNotIn('script',page.tags);self.assertIn('<script>alert(1)</script>',' '.join(page.text))
    def test_overwrite_refused_and_fresh_output_exact(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'site';b.write_new(p,self.files)
            self.assertEqual({q.name:q.read_bytes() for q in p.iterdir()},self.files)
            with self.assertRaises(ValueError):b.write_new(p,self.files)
    def test_duplicate_json_keys_refused(self):
        with self.assertRaises(ValueError):json.loads('{"x":1,"x":2}',object_pairs_hook=b.unique)

if __name__=='__main__':unittest.main(verbosity=2)
