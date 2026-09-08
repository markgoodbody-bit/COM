"""Preservation and routing checks; no reception, usability or benefit claim."""
import re
import tempfile
import unittest
from pathlib import Path
import build
from test_build import HTMLLinks

class DiscussionTests(unittest.TestCase):
    def test_complete_content_and_seven_stable_anchors(self):
        files = build.generate_discussion()
        raw = files['discussion/index.md']
        self.assertEqual(raw, (build.HERE / 'discussion/DISCUSSION.md').read_bytes())
        self.assertEqual(build.digest(raw), build.DISCUSSION_SHA256)
        page = files['discussion/index.html'].decode()
        parser = HTMLLinks()
        parser.feed(page)
        plain = ''.join(parser.text)
        for block in raw.decode().strip().split('\n\n'):
            expected = re.sub(r'^#{1,2} ', '', block)
            expected = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'\1', expected)
            self.assertIn(expected, plain)
        for link in re.findall(r'\]\((https://[^)]+)\)', raw.decode()):
            self.assertIn(link, parser.links)
        self.assertEqual(re.findall(r'<h2 id="([^"]+)"', page), list(build.DISCUSSION_HEADINGS.values()))
        self.assertEqual(parser.tags.count('h1'), 1)
        self.assertFalse(set(parser.tags) & {'script', 'form', 'iframe', 'object', 'input'})
        self.assertEqual(parser.robots, [])
        self.assertIn('href="/"', page)
        self.assertIn('href="/llms.txt"', page)
        self.assertIn('href="index.md"', page)
        self.assertIn('It does not receive submissions.', plain)

    def test_changed_missing_and_overwrite_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(FileNotFoundError):
                build.generate_discussion(root)
            (root / 'discussion').mkdir()
            (root / 'discussion/DISCUSSION.md').write_bytes(b'# Different\n')
            with self.assertRaisesRegex(ValueError, 'Discussion changed'):
                build.generate_discussion(root)
            with self.assertRaisesRegex(ValueError, 'refusing to overwrite'):
                build.write_new(root, build.generate_discussion())

    def test_route_keeps_legacy_participation(self):
        files, _ = build.generate()
        lib, _ = build.load(build.HERE)
        for name in ['explore/challenge.html', 'explore/challenge.md']:
            text = files[name].decode()
            self.assertIn('https://pleasestartfromhere.com/discussion/', text)
            self.assertIn(lib['challenge_route']['url'], text)
            self.assertIn('Legacy GitHub discussion and participation', text)

if __name__ == '__main__':
    unittest.main()
