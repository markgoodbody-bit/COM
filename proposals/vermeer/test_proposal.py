import json
import shutil
import tempfile
import unittest
from pathlib import Path

import build


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "vermeer"
        shutil.copytree(build.ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__"))

    def mutate_record(self, key, value):
        path = self.root / "artwork.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record[key] = value
        path.write_text(json.dumps(record), encoding="utf-8")

    def replace(self, name, old, new):
        path = self.root / name
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def test_candidate_valid(self):
        self.assertEqual(len(build.validate(self.root)), 5)

    def test_reject_master_claim(self):
        self.mutate_record("master_status", "VERIFIED")
        with self.assertRaisesRegex(ValueError, "master_status"):
            build.validate(self.root)

    def test_reject_source_category_erasure(self):
        self.mutate_record("source_category", "MUSEUM_ORIGINAL")
        with self.assertRaisesRegex(ValueError, "source_category"):
            build.validate(self.root)

    def test_reject_history_rewrite(self):
        self.replace("acquisition.json", "NOT BUILT", "BUILT")
        with self.assertRaisesRegex(ValueError, "history"):
            build.validate(self.root)

    def test_reject_changed_image_bytes(self):
        path = self.root / "assets/staedel-1149-thumb-xl.jpg"
        path.write_bytes(path.read_bytes() + b"x")
        with self.assertRaisesRegex(ValueError, "Image bytes"):
            build.validate(self.root)

    def test_reject_unbuilt_shelf_link(self):
        self.replace("index.html", "</footer>", '<a href="../">Works</a></footer>')
        with self.assertRaisesRegex(ValueError, "local route"):
            build.validate(self.root)

    def test_reject_active_content(self):
        self.replace("index.html", "</body>", "<script>alert(1)</script></body>")
        with self.assertRaisesRegex(ValueError, "Active content"):
            build.validate(self.root)

    def test_reject_caption_drift(self):
        self.replace("index.html", "Inventory 1149.", "Inventory 1148.")
        with self.assertRaisesRegex(ValueError, "wording drift"):
            build.validate(self.root)

    def test_reject_missing_bound(self):
        self.replace("work.css", "max-width: 640px", "max-width: 1440px")
        with self.assertRaisesRegex(ValueError, "bound"):
            build.validate(self.root)

    def test_reject_project_reading_change(self):
        self.mutate_record("project_response", "Vermeer proves PSFH")
        with self.assertRaisesRegex(ValueError, "project_response"):
            build.validate(self.root)


if __name__ == "__main__":
    unittest.main()
