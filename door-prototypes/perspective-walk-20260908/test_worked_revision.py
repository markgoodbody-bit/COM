"""Worked-example preservation, not validation of the account's conclusions."""
import re
import tempfile
import unittest
from pathlib import Path
import build
from test_build import HTMLLinks


class WorkedRevisionTests(unittest.TestCase):
    def test_exact_markdown_and_all_visible_prose_and_evidence_links(self):
        raw, rendered = build.worked_revision(build.HERE)
        self.assertEqual(raw, (build.HERE / 'WORKED_REVISION.md').read_bytes())
        self.assertEqual(build.digest(raw), build.WORKED_SHA256)
        parser = HTMLLinks()
        parser.feed(rendered)
        plain = ''.join(parser.text)
        for block in raw.decode().strip().split('\n\n'):
            expected = re.sub(r'^#{1,2} ', '', block)
            expected = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'\1', expected)
            self.assertIn(expected, plain)
        for url in re.findall(r'\]\((https://[^)]+)\)', raw.decode()):
            self.assertIn(url, parser.links)
        self.assertEqual(parser.tags.count('h1'), 1)
        self.assertEqual(parser.robots, [])
        self.assertFalse(set(parser.tags) & {'script', 'iframe', 'form', 'object'})
        self.assertIn('/' + build.WORKED_COMMIT + '/', rendered)

    def test_missing_or_changed_edition_is_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(FileNotFoundError):
                build.worked_revision(root)
            (root / 'WORKED_REVISION.md').write_bytes(b'# Replacement\n')
            with self.assertRaisesRegex(ValueError, 'Worked revision changed'):
                build.worked_revision(root)


if __name__ == '__main__':
    unittest.main()
