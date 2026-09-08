"""Offline behavioral tests using explicitly synthetic resource bodies.

These do not establish acquisition, content safety of every format, deployed
copies, or live reader access. Real-byte verification is a separate build run.
"""
from __future__ import annotations
import copy
import json
import tempfile
import unittest
from pathlib import Path
import build_resources as br

SVG = b'<svg xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrow"/></defs><path style="marker-end:url(#arrow)"/></svg>'


def fixture():
    projects, urls = [], {}
    for ident, repo in br.PROJECTS.items():
        commit = ('1' if ident == 'trace' else '2') * 40
        if ident == 'trace':
            bodies = {'README.md': b'# Source notices\n\n[Spine](TRACE-SPINE.md)\n[Full](TRACE.md)\n',
                      'TRACE-SPINE.md': b'# Spine\n\n[Full](TRACE.md#part)\n',
                      'TRACE.md': b'# Full\n\n[Neighbour](https://github.com/ailev/FPF)\n'}
        else:
            bodies = {'README.md': b'# Source notices\n\n[Book](MECHANICAL_ETHICS.md)\n[Figures](figures/)\n',
                      'MECHANICAL_ETHICS.md': b'# Book\n\n![Illustration](figures/figure-1.svg)\n',
                      'MECHANICAL_ETHICS.pdf': b'%PDF-1.7\nSYNTHETIC FIXTURE, NOT A REAL PDF\n%%EOF\n'}
            for i in range(1, 5):
                bodies[f'figures/figure-{i}.svg'] = SVG
                bodies[f'figures/figure-{i}.png'] = b'\x89PNG\r\n\x1a\nSYNTHETIC FIXTURE'
        specs = []
        for name, data in bodies.items():
            specs.append({'path': name, 'bytes': len(data), 'git_blob_sha1': br.blob(data),
                          'media_type': br.TYPES[Path(name).suffix],
                          'sha256_declared_by_source_readme': br.digest(data)})
            urls[f'https://raw.githubusercontent.com/{repo}/{commit}/{name}'] = data
        projects.append({'id': ident, 'repository': repo, 'commit': commit,
                         'status_at_source': 'TEST FIXTURE / NOT REAL CONTENT',
                         'baseline_distinction': 'Not a baseline', 'notice_path': 'README.md',
                         'current_prefix': f'/resources/{ident}/',
                         'snapshot_prefix': f'/resources/snapshots/{ident}/{commit}/',
                         'files': specs})
    total = sum(len(data) for data in urls.values())
    inv = {'format': 'psfh-resource-copy-input/0.1', 'prepared': '2026-09-08',
           'projects': projects, 'byte_totals': {'source_files': total,
           'source_file_count': len(urls), 'current_plus_one_snapshot': total * 2}}
    return inv, urls


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inv, self.urls = fixture()
        self.path = self.root / 'RESOURCE_COPIES.json'
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        self.path.write_bytes(br.encode(self.inv))

    def run_build(self):
        return br.generate(self.path, lambda url, size: self.urls[url])

    def test_all_originals_aliases_and_snapshots_are_exact(self):
        files, report = self.run_build()
        self.assertEqual(report['original_files'], 14)
        for p in self.inv['projects']:
            for s in p['files']:
                source = f'https://raw.githubusercontent.com/{p["repository"]}/{p["commit"]}/{s["path"]}'
                for prefix in (p['current_prefix'], p['snapshot_prefix']):
                    self.assertEqual(files[prefix.lstrip('/') + s['path']], self.urls[source])
        self.assertEqual(len(files), 33)  # 28 copies, 2 required folder indexes, 3 catalogue forms.

    def test_catalogue_matches_actual_hashes_and_local_paths(self):
        files, _ = self.run_build()
        cat = json.loads(files['resources/index.json'])
        self.assertEqual(cat['status'], 'VERIFIED BUILD OUTPUT / NOT A LIVE DELIVERY RECEIPT')
        for project in cat['projects']:
            for item in project['files']:
                path = item['current_url'].removeprefix(br.ORIGIN).lstrip('/')
                self.assertEqual(item['sha256'], br.digest(files[path]))
                self.assertIn(item['current_url'].encode(), files['resources/index.md'])
                self.assertIn(item['snapshot_url'].encode(), files['resources/index.html'])

    def test_directory_reference_gets_a_local_index_at_both_editions(self):
        files, _ = self.run_build()
        p = self.inv['projects'][1]
        for prefix in (p['current_prefix'], p['snapshot_prefix']):
            index = files[prefix.lstrip('/') + 'figures/index.html']
            self.assertIn(b'figure-1.svg', index)
            self.assertNotIn(b'<script', index)
            self.assertNotIn(b'noindex', index)

    def test_wrong_blob_is_refused_before_output(self):
        url = next(iter(self.urls))
        original = self.urls[url]
        self.urls[url] = b'!' + original[1:]
        with self.assertRaisesRegex(ValueError, 'Git blob'):
            self.run_build()
        self.assertEqual(list(self.root.iterdir()), [self.path])

    def test_missing_source_is_not_an_empty_resource(self):
        self.urls.pop(next(iter(self.urls)))
        with self.assertRaises(KeyError):
            self.run_build()

    def test_incorrect_declared_sha_is_refused(self):
        self.inv['projects'][0]['files'][0]['sha256_declared_by_source_readme'] = '0' * 64
        self.save()
        with self.assertRaisesRegex(ValueError, 'declared SHA-256'):
            self.run_build()

    def test_duplicate_json_keys_are_refused(self):
        self.path.write_text('{"format":1,"format":2}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON'):
            self.run_build()

    def test_unsafe_paths_prefixes_repos_and_nonimmutable_sources_are_refused(self):
        for path in ('../secret.md', '/secret.md', 'x\\y.md', 'x%2fy.md', 'x\".md', 'x<script>.md'):
            inv = copy.deepcopy(self.inv)
            inv['projects'][0]['files'][0]['path'] = path
            with self.assertRaises(ValueError):
                br.validate_inventory(inv)
        for field, value in [('commit', 'main'), ('repository', 'untrusted/repo'),
                             ('snapshot_prefix', '/resources/shared/')]:
            inv = copy.deepcopy(self.inv)
            inv['projects'][0][field] = value
            with self.assertRaises(ValueError):
                br.validate_inventory(inv)

    def test_missing_notice_and_wrong_totals_are_refused(self):
        for mutate in (lambda inv: inv['projects'][0].update(notice_path='other.md'),
                       lambda inv: inv['byte_totals'].update(source_files=1)):
            inv = copy.deepcopy(self.inv)
            mutate(inv)
            with self.assertRaises(ValueError):
                br.validate_inventory(inv)

    def test_svg_keeps_local_markers_but_refuses_active_external_and_dangling(self):
        br.check_svg(SVG)
        for data in (SVG.replace(b'<path', b'<script/><path'),
                     SVG.replace(b'<path', b'<path onload="alert(1)"'),
                     SVG.replace(b'url(#arrow)', b'url(https://example.com/a)'),
                     SVG.replace(b'url(#arrow)', b'url(#missing)'),
                     b'<!DOCTYPE svg>' + SVG):
            with self.assertRaises(ValueError):
                br.check_svg(data)

    def test_lfs_pointer_is_refused_even_when_hash_matches(self):
        data = b'version https://git-lfs.github.com/spec/v1\n'
        spec = {'path': 'test.pdf', 'bytes': len(data), 'git_blob_sha1': br.blob(data)}
        with self.assertRaisesRegex(ValueError, 'LFS'):
            br.verify_body(spec, data)

    def test_known_pdf_action_marker_is_refused(self):
        data = b'%PDF-1.7\n/JavaScript ()\n%%EOF\n'
        spec = {'path': 'test.pdf', 'bytes': len(data), 'git_blob_sha1': br.blob(data)}
        with self.assertRaisesRegex(ValueError, 'PDF action'):
            br.verify_body(spec, data)

    def test_missing_relative_dependency_is_not_declared_complete(self):
        with self.assertRaisesRegex(ValueError, 'Missing relative'):
            br.dependency_report({}, {'README.md': b'[Missing](not-here.md)\n'})
        with self.assertRaisesRegex(ValueError, 'Out-of-library'):
            br.dependency_report({}, {'README.md': b'[Outside](../other.md)\n'})

    def test_fenced_example_paths_are_not_actual_dependencies(self):
        result = br.dependency_report({}, {'README.md': b'# Test\n\n```md\n[Example](absent.md)\n```\n\n[Outside](https://example.com)\n'})
        self.assertEqual(result['relative_file_or_directory_links_checked'], 0)
        self.assertEqual(result['still_external_destinations'], ['https://example.com'])

    def test_generator_is_deterministic(self):
        files1, report1 = self.run_build()
        files2, report2 = self.run_build()
        self.assertEqual(files1, files2)
        self.assertEqual(report1, report2)

    def test_write_is_staging_only_and_preserves_existing_output(self):
        files, _ = self.run_build()
        output = self.root / 'output'
        br.write_new(output, files)
        self.assertEqual({p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob('*') if p.is_file()}, files)
        with self.assertRaisesRegex(ValueError, 'overwrite'):
            br.write_new(output, files)
        with self.assertRaisesRegex(ValueError, 'Unsafe generated'):
            br.write_new(self.root / 'bad', {'../outside': b'x'})
        self.assertFalse((self.root / 'outside').exists())

    def test_redirects_and_credential_bearing_sources_are_not_admitted(self):
        with self.assertRaisesRegex(ValueError, 'redirect refused'):
            br.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://other.com')
        with self.assertRaisesRegex(ValueError, 'Unexpected source host'):
            br.public_fetch('https://user:secret@raw.githubusercontent.com/test', 10)


if __name__ == '__main__':
    unittest.main()
