#!/usr/bin/env python3
"""Synthetic positive and negative tests for read-only release rehearsal."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from scripts import psfh_release_rehearsal as r

class ReleaseRehearsalTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.site = Path(self.tmp.name) / "out"
        self.site.mkdir()
        self.data = {
            "index.html": '<div class="art-hero"></div><div class="human-first-door"></div>'
                          '<a href="/explore/challenge-local.html">NOT SUBMITTED</a>'
                          '<article id="step-story"></article>',
            "read/me-v0.8.html": "<h1>Chapter</h1>" * 17 + "<h2>Section</h2>" * 38,
            "explore/yac/index.html": '<a href="https://yetanotherclearing.com/">Read</a>',
            "explore/yac/thr/index.html": "<h1>Human Record</h1>",
            "explore/challenge.html": "<a href='challenge-local.html'>Local</a>",
            "explore/challenge-local.html": "NOT SUBMITTED and connect-src 'none'; form-action 'none'",
            "resources/mechanical-ethics/MECHANICAL_ETHICS.md": "release",
            "resources/mechanical-ethics/MECHANICAL_ETHICS.pdf": "%PDF synthetic only",
        }
        for name, value in self.data.items():
            file = self.site / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(value, encoding="utf-8")
        self.target = {"commit": r.EXPECTED_PAGES_COMMIT, "tree": r.EXPECTED_PAGES_TREE,
                       "files": [{"path": "index.html", "sha": "0"*40},
                                 {"path": ".nojekyll", "sha": "1"*40}]}
        self.original_release = r.RELEASED_ME_SHA256
        r.RELEASED_ME_SHA256 = hashlib.sha256(b"release").hexdigest()
        self.addCleanup(setattr, r, "RELEASED_ME_SHA256", self.original_release)

    def run_rehearsal(self, **args):
        return r.inspect(self.site, self.target, public_ref=args.get("public_ref",r.EXPECTED_PAGES_COMMIT),
                         source_tree=args.get("source_tree",r.EXPECTED_SOURCE_TREE))

    def test_real_diff_categories_and_public_custody_stop(self):
        result = self.run_rehearsal()
        self.assertIn("index.html", result["modified"])
        self.assertIn(".nojekyll", result["deleted_if_naive_replace"])
        self.assertIn(".nojekyll", result["must_preserve_public_files"])
        self.assertIn("read/me-v0.8.html", result["added"])
        self.assertEqual(result["operator_gate"], "STOP_NO_RELEASE_APPROVAL")

    def test_stale_public_head_fails(self):
        with self.assertRaisesRegex(ValueError, "PUBLIC_TARGET_MOVED"):
            self.run_rehearsal(public_ref="f"*40)

    def test_wrong_source_tree_fails(self):
        with self.assertRaisesRegex(ValueError, "source tree differs"):
            self.run_rehearsal(source_tree="e"*40)

    def test_incomplete_or_corrupted_release_fails(self):
        (self.site / "resources/mechanical-ethics/MECHANICAL_ETHICS.md").write_text("changed")
        with self.assertRaisesRegex(ValueError, "Released ME"):
            self.run_rehearsal()

    def test_local_not_submitted_is_required(self):
        (self.site / "explore/challenge-local.html").write_text("SENT")
        with self.assertRaisesRegex(ValueError, "mistaken for submission"):
            self.run_rehearsal()

    def test_art_first_order_is_required(self):
        (self.site / "index.html").write_text(
            '<div class="human-first-door"></div><div class="art-hero"></div><article id="step-story"></article>')
        with self.assertRaisesRegex(ValueError, "Painting-first"):
            self.run_rehearsal()

    def test_missing_reader_aborts(self):
        (self.site / "read/me-v0.8.html").unlink()
        with self.assertRaisesRegex(ValueError, "Missing first-visit files"):
            self.run_rehearsal()

    def test_bad_target_snapshot_aborts(self):
        self.target["files"].append({"path": "index.html", "sha": "1"*40})
        with self.assertRaisesRegex(ValueError, "inventory malformed"):
            self.run_rehearsal()

    def test_pin_mismatch_aborts(self):
        self.target["tree"] = "3"*40
        with self.assertRaisesRegex(ValueError, "does not match"):
            self.run_rehearsal()

if __name__ == "__main__":
    unittest.main()
