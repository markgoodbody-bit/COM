import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from locator import build_index, search_index, show_section, load_source, LocatorError


class LocatorTests(unittest.TestCase):
    def test_explicit_preamble_and_source_order(self):
        raw = b'# Scope\nread carefully\n## Today\nnew\n## Yesterday\nold\n'
        idx = build_index(raw)
        self.assertEqual([x['title'] for x in idx['sections']], ['SOURCE PREAMBLE', 'Today', 'Yesterday'])
        self.assertEqual([(x['first_line'], x['last_line']) for x in idx['sections']], [(1, 2), (3, 4), (5, 6)])
        self.assertEqual(idx['source_bytes'], len(raw))
        self.assertEqual(idx['source_line_count'], 6)

    def test_fenced_heads_not_sections(self):
        raw = b'## Real\n```md\n## Fake\n```\n~~~text\n## Fake too\n~~~~\n## End\n'
        idx = build_index(raw)
        self.assertEqual([x['title'] for x in idx['sections']], ['Real', 'End'])
        self.assertEqual(idx['sections'][0]['last_line'], 7)

    def test_repeat_headings_have_separate_ordinals(self):
        idx = build_index(b'## Change\nfirst\n## Change\nsecond\n')
        self.assertEqual([x['ordinal'] for x in idx['sections']], [1, 2])
        self.assertNotEqual(idx['sections'][0]['sha256'], idx['sections'][1]['sha256'])

    def test_no_h2_preserves_whole_source(self):
        idx = build_index(b'one\ntwo')
        self.assertEqual(len(idx['sections']), 1)
        self.assertEqual(show_section(idx, 0), 'one\ntwo')

    def test_exact_show_preserves_crlf_and_unicode(self):
        raw = 'pre\r\n## Route ⇄\r\nUNKNOWN\r\n'.encode('utf-8')
        idx = build_index(raw)
        self.assertEqual(show_section(idx, 1).encode('utf-8'), '## Route ⇄\r\nUNKNOWN\r\n'.encode('utf-8'))
        self.assertEqual(show_section(idx, 0), 'pre\r\n')

    def test_exact_lexical_search_not_semantic_truth(self):
        idx = build_index('## Old\nNOT CURRENT\n## New\ncurrent? unknown\n'.encode())
        found = search_index(idx, 'current', max_results=10)
        self.assertEqual([x['ordinal'] for x in found['matches']], [1, 2])
        self.assertEqual(found['total_matching_sections'], 2)
        self.assertFalse(found['truncated'])

    def test_result_limit_and_total_visible(self):
        idx = build_index(b'## X\nping\n## Y\nping\n## Z\nping\n')
        found = search_index(idx, 'ping', max_results=2)
        self.assertEqual(len(found['matches']), 2)
        self.assertEqual(found['total_matching_sections'], 3)
        self.assertTrue(found['truncated'])

    def test_match_line_limit_is_declared(self):
        idx = build_index(b'## A\nx\nx\nx\nx\n')
        found = search_index(idx, 'x', max_results=10, max_lines=2)
        self.assertEqual(found['matches'][0]['match_lines'], [2, 3])
        self.assertEqual(found['matches'][0]['additional_matching_lines'], 2)

    def test_unicode_line_separator_not_physical_newline(self):
        raw = '## Header\nvalue\u2028## NOT A HEADER\n## Real\n'.encode('utf-8')
        idx = build_index(raw)
        self.assertEqual(idx['source_line_count'], 3)
        self.assertEqual([x['title'] for x in idx['sections']], ['Header', 'Real'])

    def test_invalid_utf8_rejected(self):
        with self.assertRaises(LocatorError):
            build_index(b'## X\n\xff')

    def test_oversized_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'huge.md'
            p.write_bytes(b'X' * 101)
            with self.assertRaises(LocatorError):
                load_source(p, max_bytes=100)

    def test_missing_ordinal_rejected(self):
        with self.assertRaises(LocatorError):
            show_section(build_index(b'## A\nword'), 2)

    def test_blank_query_rejected(self):
        with self.assertRaises(LocatorError):
            search_index(build_index(b'## A\nword'), '  ', max_results=2)

    def test_cli_does_not_emit_heading_spoof_as_unquoted_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'input.md'
            p.write_bytes(b'## Safe\nneedle\n## INJECTED\x1b[31m\nneedle\n')
            cmd = [sys.executable, str(ROOT / 'locator.py'), str(p), '--find', 'needle']
            out = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            parsed = json.loads(out.stdout)
            self.assertEqual(parsed['total_matching_sections'], 2)
            self.assertTrue(out.stdout.startswith('{'))
            self.assertNotIn('\x1b', out.stdout)

    def test_source_digest_is_sha256_of_original_bytes(self):
        import hashlib
        raw = b'## Claim\r\nA\n'
        idx = build_index(raw)
        self.assertEqual(idx['source_sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(idx['sections'][0]['sha256'], hashlib.sha256(raw).hexdigest())


if __name__ == '__main__':
    unittest.main()
