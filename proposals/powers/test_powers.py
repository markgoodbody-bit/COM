import json
import shutil
import tempfile
import unittest
from pathlib import Path

from build import ROOT, FILES, validate


class PowersTests(unittest.TestCase):
    def test_frozen_candidate(self):
        self.assertEqual(len(validate()), 8)

    def rejection(self, filename, change):
        with tempfile.TemporaryDirectory(prefix="powers-contract-") as directory:
            root = Path(directory)
            for name in FILES:
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, root / name)
            file = root / filename
            file.write_bytes(change(file.read_bytes()))
            with self.assertRaises(ValueError):
                validate(root)

    def test_parent_byte_change(self):
        self.rejection(FILES[5], lambda b: b + b"x")

    def test_viewing_copy_byte_change(self):
        self.rejection(FILES[6], lambda b: b + b"x")

    def test_master_claim_rejected(self):
        self.rejection("artwork.json", lambda b: b.replace(b'"UNKNOWN"', b'"MASTER"'))

    def test_false_acquisition_time_rights_rejected(self):
        self.rejection("artwork.json", lambda b: b.replace(b"not Codex acquisition-time", b"Codex acquisition-time"))

    def test_acquisition_receipt_rewrite_rejected(self):
        self.rejection("acquisition.json", lambda b: b + b"\n")

    def test_detached_derivative_rejected(self):
        def detach(data):
            obj = json.loads(data)
            obj["variants"][0]["parent_sha256"] = "0" * 64
            return json.dumps(obj).encode()
        self.rejection("responsive.json", detach)

    def test_wrong_fallback_rejected(self):
        self.rejection("index.html", lambda b: b.replace(b'src="../../art/bible-quilt-1440.jpg"', b'src="../../art/bible-quilt-delivered.jpg"'))

    def test_script_rejected(self):
        self.rejection("index.html", lambda b: b.replace(b"</body>", b"<script></script></body>"))

    def test_creator_agency_drift_rejected(self):
        self.rejection("index.html", lambda b: b.replace(b"Powers insisted", b"Powers explained"))

    def test_panel_subject_omission_rejected(self):
        self.rejection("index.html", lambda b: b.replace(b"<li>The Holy Family</li>", b""))

    def test_credit_line_omission_rejected(self):
        self.rejection("index.html", lambda b: b.replace(b"Gift of Mr. and Mrs. H. M. Heckman. ", b""))


if __name__ == "__main__":
    unittest.main()
