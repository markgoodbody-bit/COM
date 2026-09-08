"""Structural regression checks. Not a cold-reader or behavioural evaluation."""
from __future__ import annotations
import copy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
import build


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.tags = []
        self.text = []
    def handle_starttag(self,tag,attrs):
        self.tags.append(tag)
        for key,value in attrs:
            if key in ('href','src') and value:
                self.links.append(value)
    def handle_data(self,data):
        self.text.append(data)


def local_target(base: str, link: str) -> str | None:
    url = urlsplit(link)
    if url.scheme or url.netloc or not url.path:
        return None
    parts = list(PurePosixPath(base).parent.parts)
    for part in unquote(url.path).split('/'):
        if part == '..':
            if not parts:
                raise AssertionError('Path escapes output')
            parts.pop()
        elif part not in ('','.'): parts.append(part)
    return '/'.join(parts)


class ReadingBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files,cls.receipt = build.generate()
        cls.library,cls.examples = build.load(build.HERE)
    def mutate(self,fn):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for file in ('library.json',) + tuple(x+'.json' for x in build.EXAMPLES):
                shutil.copyfile(build.HERE/file,root/file)
            data=build.read_json(root/'library.json')
            fn(data)
            (root/'library.json').write_bytes(build.encode(data))
            with self.assertRaises(ValueError): build.generate(root)
    def test_deterministic(self):
        self.assertEqual((self.files,self.receipt),build.generate())
    def test_utf8_and_json(self):
        for path,data in self.files.items():
            self.assertTrue(data.decode('utf-8'))
            if path.endswith('.json'): json.loads(data,object_pairs_hook=build.unique_pairs)
    def test_only_additive_explore_namespace(self):
        self.assertTrue(all(p.startswith('explore/') and '..' not in PurePosixPath(p).parts for p in self.files))
        self.assertFalse(any(PurePosixPath(p).name in ('CNAME','robots.txt') for p in self.files))
    def test_no_executable_visitor_surface(self):
        for path,data in self.files.items():
            if path.endswith('.html'):
                parser=HTMLLinks(); parser.feed(data.decode())
                self.assertFalse(set(parser.tags)&{'script','form','iframe','object','embed'})
    def test_html_and_markdown_links(self):
        checked=0
        for path,data in self.files.items():
            text=data.decode()
            if path.endswith('.html'):
                parser=HTMLLinks(); parser.feed(text); links=parser.links
            elif path.endswith(('.md','.txt')):
                links=re.findall(r'\]\(([^)]+)\)',text)
            else: continue
            for link in links:
                target=local_target(path,link)
                if target:
                    self.assertTrue(target in self.files,(path,link)); checked+=1
                else: build.external_url(link)
        self.assertGreater(checked,100)
    def test_json_links(self):
        for path,data in self.files.items():
            if not path.endswith('.json') or path.endswith('packet.json'): continue
            obj=json.loads(data)
            links=[]
            for edge in obj.get('next',[]):
                if 'path' in edge: links.append(edge['path'])
            links.extend(obj.get('routes',{}).values())
            for key in ('case','shared_case'):
                if key in obj: links.append(obj[key])
            for link in links:
                self.assertTrue(local_target(path,link) in self.files,(path,link))
    def test_self_described_llms_links(self):
        text=self.files['explore/llms.txt'].decode()
        self.assertTrue(text.startswith('# '))
        self.assertIn('## Optional',text)
        for link in re.findall(r'\]\(([^)]+)\)',text):
            self.assertTrue(link.startswith(build.BASE))
            self.assertIn('explore/'+link[len(build.BASE):],self.files)
    def test_source_identity(self):
        for src in self.library['sources'].values():
            for key in ('url','raw_url'):
                self.assertIn('/'+src['commit']+'/',src[key])
    def test_exact_shared_facts(self):
        original=self.examples['case']['facts']
        self.assertEqual(original,json.loads(self.files['explore/example/case.json'])['facts'])
        for name in ('route','affected','challenge'):
            self.assertEqual(['F1','F2'],json.loads(self.files[f'explore/example/{name}.json'])['supported_by'])
    def test_representations_preserve_meaning_fields(self):
        for node in self.library['nodes']:
            stem='explore/nodes/'+node['id']
            machine=json.loads(self.files[stem+'.json'])
            text=self.files[stem+'.md'].decode()
            parser=HTMLLinks(); parser.feed(self.files[stem+'.html'].decode()); plain=''.join(parser.text)
            for key in ('short','detail','perspective','challenge','question','kind'):
                self.assertEqual(node[key],machine[key])
                self.assertIn(node[key],text)
                self.assertIn(node[key],plain)
    def test_alternate_representations(self):
        for path in self.files:
            if path.endswith('.html'):
                self.assertIn('rel="alternate"',self.files[path].decode())
                self.assertIn('rel="describedby"',self.files[path].decode())
    def test_individual_reading_size(self):
        for p,b in self.files.items():
            if '/nodes/' in p and p.endswith('.json'): self.assertLess(len(b),4500)
            if '/nodes/' in p and p.endswith('.md'): self.assertLess(len(b),3000)
        self.assertLess(len(self.files['explore/index.md']),3000)
    def test_manifest_sizes_and_hashes(self):
        m=json.loads(self.files['explore/map.json'])
        self.assertEqual(len(self.files)-1,len(m['resources']))
        for item in m['resources']:
            data=self.files['explore/'+item['path']]
            self.assertEqual(item['bytes'],len(data))
            self.assertEqual(item['sha256'],hashlib.sha256(data).hexdigest())
        self.assertFalse(any(r['path']=='map.json' for r in m['resources']))
    def test_packet_has_all_nodes_and_original_example(self):
        packet=json.loads(self.files['explore/packet.json'])
        self.assertEqual(self.library['nodes'],packet['nodes'])
        embedded = copy.deepcopy(packet['examples'])
        for obj in embedded.values():
            for key in ('case', 'shared_case'):
                if key in obj:
                    self.assertTrue(obj[key].startswith('example/'))
                    obj[key] = obj[key].removeprefix('example/')
            for edge in obj['next']:
                if 'path' in edge:
                    self.assertTrue(edge['path'].startswith('example/'))
                    edge['path'] = edge['path'].removeprefix('example/')
        self.assertEqual(self.examples, embedded)
    def test_output_refuses_existing_site(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); (root/'CNAME').write_text('existing.test\n')
            with self.assertRaises(ValueError): build.write_new(root,self.files)
            self.assertEqual((root/'CNAME').read_text(),'existing.test\n')
            self.assertEqual(len(list(root.iterdir())),1)
    def test_write_exact_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'stage'; build.write_new(root,self.files)
            found={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(self.files,found)
    def test_duplicate_ids_rejected(self):
        self.mutate(lambda d:d['nodes'].append(copy.deepcopy(d['nodes'][0])))
    def test_unknown_edge_rejected(self):
        self.mutate(lambda d:d['nodes'][0]['next'][0].update(target='absent'))
    def test_unsafe_node_path_rejected(self):
        self.mutate(lambda d:d['nodes'][0].update(id='../CNAME'))
    def test_missing_challenge_rejected(self):
        self.mutate(lambda d:d['nodes'][0].update(challenge=''))
    def test_false_source_pin_rejected(self):
        self.mutate(lambda d:d['sources']['trace'].update(commit='0'*40))
    def test_credential_url_rejected(self):
        with self.assertRaises(ValueError): build.external_url('https://secret:password@example.com/')
        with self.assertRaises(ValueError): build.external_url('javascript:alert(1)')
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError): json.loads('{"id":"a","id":"b"}',object_pairs_hook=build.unique_pairs)
    def test_html_content_is_escaped(self):
        rendered=build.html_document('<script>x</script>',[('Note','<img src=x onerror=alert(1)>')],[],'index.md','llms.txt')
        parser=HTMLLinks(); parser.feed(rendered)
        self.assertNotIn('script',parser.tags); self.assertNotIn('img',parser.tags)
        self.assertIn('&lt;script&gt;',rendered)

if __name__=='__main__':
    unittest.main(verbosity=2)
