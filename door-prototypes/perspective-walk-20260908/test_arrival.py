"""Small-entry regression checks, not reader-effectiveness evidence."""
from __future__ import annotations
import copy
import hashlib
import json
import re
import unittest
from urllib.parse import urljoin, urlsplit
import build


class ArrivalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, _ = build.generate()
        cls.lib, _ = build.load(build.HERE)
        cls.entry = json.loads(cls.files['explore/start.json'])
        cls.catalogue = json.loads(cls.files['explore/questions.json'])

    def test_small_entry_budget(self):
        for name, limit in [('start.json', 2048), ('questions.json', 8192), ('questions.txt', 4096)]:
            self.assertLessEqual(len(self.files['explore/' + name]), limit)

    def test_entry_preserves_orientation_and_value_status(self):
        for key in ('purpose', 'orientation', 'boundary', 'value_choice'):
            self.assertEqual(self.lib[key], self.entry[key])
        self.assertIn('not an agent or callable tool', self.entry['reading'])
        self.assertIn('no claim of current public reachability', self.entry['scope'])

    def test_all_questions_are_source_exact(self):
        self.assertEqual([(n['id'], n['question']) for n in self.lib['nodes']],
                         [(n['id'], n['question']) for n in self.catalogue['nodes']])

    def test_all_edges_are_source_exact(self):
        for source, actual in zip(self.lib['nodes'], self.catalogue['nodes']):
            self.assertEqual(source['next'],
                             [{k: e[k] for k in ('relation', 'target')} for e in actual['next']])
            for edge in actual['next']:
                self.assertIn('explore/' + edge['path'], self.files)
                self.assertEqual(edge['target'], json.loads(self.files['explore/' + edge['path']])['id'])

    def test_sizes_are_bytes_of_exact_targets(self):
        for row in self.catalogue['nodes']:
            for kind, path in row['routes'].items():
                self.assertEqual(len(self.files['explore/' + path]), row['bytes'][kind])
                if kind == 'json':
                    self.assertEqual(row['id'], json.loads(self.files['explore/' + path])['id'])

    def test_text_menu_keeps_questions_paths_and_sizes(self):
        text = self.files['explore/questions.txt'].decode('utf-8')
        for row in self.catalogue['nodes']:
            expected = '- [' + row['question'] + '](' + row['routes']['text'] + ') — ' + str(row['bytes']['text']) + ' bytes'
            self.assertIn(expected, text)
        self.assertIn('not tokens or a usage charge', text)

    def test_relative_routes_work_on_site_and_pinned_raw_tree(self):
        paths = list(self.entry['routes'].values()) + list(self.catalogue['routes'].values())
        for row in self.catalogue['nodes']:
            paths.extend(row['routes'].values())
            paths.extend(e['path'] for e in row['next'])
        for root in ('https://pleasestartfromhere.com/explore/',
                     'https://raw.githubusercontent.com/owner/repo/' + 'a' * 40 + '/explore/'):
            for path in paths:
                u = urlsplit(path)
                self.assertFalse(u.scheme or u.netloc or u.query or u.fragment)
                self.assertFalse(path.startswith('/') or '..' in path.split('/'))
                resolved = urljoin(root + 'start.json', path)
                self.assertEqual(resolved, root + path)
                self.assertIn('explore/' + path, self.files)

    def test_discovery_is_present_in_both_entry_views_and_llms(self):
        for name in ('index.md', 'index.txt', 'index.html', 'llms.txt'):
            data = self.files['explore/' + name].decode()
            self.assertIn('start.json', data)
            self.assertIn('questions.txt', data)

    def test_new_resources_have_manifest_hashes(self):
        rows = {r['path']: r for r in json.loads(self.files['explore/map.json'])['resources']}
        for name in ('start.json', 'questions.json', 'questions.txt'):
            self.assertEqual(hashlib.sha256(self.files['explore/' + name]).hexdigest(), rows[name]['sha256'])

    def test_oversize_entry_fails_without_truncation(self):
        mutated = copy.deepcopy(self.lib)
        mutated['purpose'] = 'x' * 9000
        with self.assertRaisesRegex(ValueError, 'byte budget exceeded'):
            build.arrival(mutated, self.files)

    def test_oversize_questions_fail_without_truncation(self):
        mutated = copy.deepcopy(self.lib)
        mutated['nodes'][0]['question'] = 'x' * 12000
        with self.assertRaisesRegex(ValueError, 'byte budget exceeded'):
            build.arrival(mutated, self.files)

    def test_relative_links_do_not_claim_remote_reachability(self):
        self.assertIn('Relative paths', self.entry['base'])
        self.assertIn('Source snapshot', self.entry['scope'])
        self.assertNotIn('https://pleasestartfromhere.com', self.files['explore/start.json'].decode())
        self.assertNotIn('http://', self.files['explore/questions.txt'].decode())


if __name__ == '__main__':
    unittest.main(verbosity=2)
