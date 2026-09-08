"""Content/delivery preservation, not proof of the historical claims."""
import re
import tempfile
import unittest
from pathlib import Path
import build
from test_build import HTMLLinks


class HistoryTests(unittest.TestCase):
    def test_complete_prose_links_and_stable_ids(self):
        files = build.generate_history()
        self.assertEqual(set(files), {'changes.md', 'changes.html'})
        raw = files['changes.md']
        self.assertEqual(raw, (build.HERE / 'CHANGES.md').read_bytes())
        self.assertEqual(build.digest(raw), build.HISTORY_SHA256)
        page = files['changes.html'].decode()
        parser = HTMLLinks()
        parser.feed(page)
        plain = ''.join(parser.text)
        for block in raw.decode().strip().split('\n\n'):
            expected = re.sub(r'^#{1,3} ', '', block).replace('**', '')
            expected = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'\1', expected)
            self.assertIn(expected, plain)
        for url in re.findall(r'\]\((https://[^)]+)\)', raw.decode()):
            self.assertIn(url, parser.links)
        self.assertEqual(re.findall(r'<h3 id="([^"]+)"', page),
                         ['d007', 'd006', 'd005', 'd004', 'd003', 'd002', 'd001', 'p001', 'p002', 'r001'])
        self.assertEqual(parser.tags.count('h1'), 1)
        self.assertEqual(parser.robots, [])
        self.assertFalse(set(parser.tags) & {'script', 'iframe', 'form', 'object'})
        self.assertIn('/' + build.HISTORY_COMMIT + '/', page)

    def test_missing_changed_duplicate_and_overwrite_refusals(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(FileNotFoundError):
                build.generate_history(root)
            (root / 'CHANGES.md').write_bytes(b'# Replacement\n')
            with self.assertRaisesRegex(ValueError, 'History changed'):
                build.generate_history(root)
            with self.assertRaisesRegex(ValueError, 'refusing to overwrite'):
                build.write_new(root, build.generate_history())
        with self.assertRaisesRegex(ValueError, 'Duplicate history'):
            build.prose_page(b'# Title\n\n### D001 one\n\n### D001 two\n',
                             'https://example.com/', 'changes.md', 'Return', True)


if __name__ == '__main__':
    unittest.main()
