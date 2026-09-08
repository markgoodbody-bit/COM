"""Packet-relative navigation regressions; no remote or reader-benefit claims."""
from __future__ import annotations
import copy
import json
import re
import unittest
from urllib.parse import urljoin, urlsplit
import build


def references(examples):
    for obj in examples.values():
        for key in ('case', 'shared_case'):
            if key in obj:
                yield obj[key]
        for edge in obj['next']:
            if 'path' in edge:
                yield edge['path']


def restore_source_paths(examples):
    original = copy.deepcopy(examples)
    for obj in original.values():
        for key in ('case', 'shared_case'):
            if key in obj:
                obj[key] = obj[key].removeprefix('example/')
        for edge in obj['next']:
            if 'path' in edge:
                edge['path'] = edge['path'].removeprefix('example/')
    return original


class PacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, _ = build.generate()
        _, cls.source_examples = build.load(build.HERE)
        cls.packet = json.loads(cls.files['explore/packet.json'])

    def test_embedded_references_resolve_from_actual_packet_location(self):
        for base in ('https://pleasestartfromhere.com/explore/',
                     'https://raw.githubusercontent.com/owner/repo/' + 'a' * 40 + '/explore/',
                     'file:///offline/explore/'):
            for link in references(self.packet['examples']):
                with self.subTest(base=base, link=link):
                    self.assertFalse(urlsplit(link).scheme or link.startswith('/'))
                    self.assertEqual(urljoin(base + 'packet.json', link), base + link)
                    self.assertIn('explore/' + link, self.files)
                    self.assertEqual(link, 'example/' + link.rsplit('/', 1)[-1])

    def test_markdown_and_json_carry_the_same_rebased_examples(self):
        text = self.files['explore/packet.md'].decode('utf-8')
        block = re.search(r'```json\n(.*?)\n```', text, re.S)
        self.assertIsNotNone(block)
        self.assertEqual(json.loads(block.group(1)), self.packet['examples'])
        self.assertIn(build.PACKET_REFERENCE_NOTE, text)
        self.assertEqual(build.PACKET_REFERENCE_NOTE, self.packet['example_reference_note'])

    def test_only_reference_paths_change_in_embedded_source(self):
        self.assertEqual(self.source_examples, restore_source_paths(self.packet['examples']))
        self.assertEqual(list(references(self.source_examples)),
                         [s.removeprefix('example/') for s in references(self.packet['examples'])])

    def test_packaging_does_not_mutate_source_objects(self):
        source = copy.deepcopy(self.source_examples)
        before = copy.deepcopy(source)
        rendered = build.packet_examples(source)
        self.assertEqual(source, before)
        self.assertEqual(rendered, self.packet['examples'])
        rendered['case']['facts'][0]['text'] = 'changed by caller'
        self.assertEqual(source, before)

    def test_unknown_example_reference_is_refused(self):
        for field in ('case', 'shared_case', 'next'):
            mutated = copy.deepcopy(self.source_examples)
            if field == 'case':
                mutated['route']['case'] = '../unreviewed.json'
            elif field == 'shared_case':
                mutated['entry']['shared_case'] = 'https://unreviewed.example/data.json'
            else:
                mutated['entry']['next'][0]['path'] = 'absent.json'
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, 'Unknown packet example reference'):
                    build.packet_examples(mutated)

    def test_no_new_fetch_is_required_to_read_shared_facts(self):
        self.assertEqual(self.source_examples['case']['facts'], self.packet['examples']['case']['facts'])
        self.assertEqual(self.source_examples['case']['unknowns'], self.packet['examples']['case']['unknowns'])
        self.assertIn('No fetch is required', self.packet['example_reference_note'])
        self.assertIn('source', self.packet['example_reference_note'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
