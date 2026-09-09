"""Synthetic mutation checks. No browser, network, intake or real visitor data."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent


class RepresentationTests(unittest.TestCase):
    def check_fixture(self, mutate_rows=None, mutate_html=None):
        with tempfile.TemporaryDirectory(prefix="guestbook-check-") as directory:
            target = Path(directory)
            shutil.copy2(ROOT / "check_representation.py", target)
            rows = [json.loads(line) for line in (ROOT / "register.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
            html = (ROOT / "register.html").read_text(encoding="utf-8")
            if mutate_rows:
                mutate_rows(rows)
            if mutate_html:
                html = mutate_html(html)
            (target / "register.jsonl").write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows), encoding="utf-8")
            (target / "register.html").write_text(html, encoding="utf-8")
            return subprocess.run([sys.executable, str(target / "check_representation.py")], capture_output=True, text=True, timeout=10)

    def assert_rejected(self, **changes):
        result = self.check_fixture(**changes)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("FAIL:", result.stdout + result.stderr)

    def test_unchanged_fixture_passes(self):
        self.assertEqual(self.check_fixture().returncode, 0)

    def test_url_in_claimed_name_rejected(self):
        self.assert_rejected(mutate_rows=lambda rows: rows[1].update(claimed_name="https://example.invalid"))

    def test_bare_domain_in_claimed_name_rejected(self):
        self.assert_rejected(mutate_rows=lambda rows: rows[1].update(claimed_name="example.invalid"))

    def test_dangling_correction_rejected(self):
        self.assert_rejected(mutate_rows=lambda rows: rows[4].update(corrects_public_id="missing-original"))

    def test_self_correction_rejected(self):
        self.assert_rejected(mutate_rows=lambda rows: rows[4].update(corrects_public_id=rows[4]["public_id"]))

    def test_removal_cannot_hide_text_in_extra_field(self):
        self.assert_rejected(mutate_rows=lambda rows: rows[-1].update(removed_note="Synthetic removed private text"))

    def test_removed_id_cannot_still_name_exported_guest(self):
        self.assert_rejected(mutate_rows=lambda rows: rows[-1].update(removed_public_id=rows[1]["public_id"]))

    def test_non_synthetic_record_rejected(self):
        self.assert_rejected(mutate_rows=lambda rows: rows[1].update(fixture=False))

    def test_each_guest_article_needs_its_own_label(self):
        self.assert_rejected(mutate_html=lambda text: text.replace("Visitor-supplied untrusted data · project-development fixture", "Project-development fixture", 1))

    def test_active_link_rejected(self):
        self.assert_rejected(mutate_html=lambda text: text.replace("</footer>", '<a href="javascript:void(0)">synthetic</a></footer>'))

    def test_event_attribute_rejected(self):
        self.assert_rejected(mutate_html=lambda text: text.replace("<body>", '<body onload="void(0)">'))

    def test_bare_domain_in_guest_html_rejected(self):
        self.assert_rejected(mutate_html=lambda text: text.replace("I was here.", "example.invalid", 1))

    def test_missing_machine_trust_rejected(self):
        self.assert_rejected(mutate_rows=lambda rows: rows[1].pop("trust"))


if __name__ == "__main__":
    unittest.main()
