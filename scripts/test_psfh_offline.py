#!/usr/bin/env python3
"""Offline package source and extracted-file acceptance; no browser/network."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from scripts import package_psfh_offline as pack


class OfflineRouting(unittest.TestCase):
    def setUp(self):
        self.inventory = {"index.html", "style.css", "read/me-v0.8.html", "art/hero.jpg", "works/index.html"}

    def test_home_book_assets_and_directories_are_relative(self):
        self.assertEqual(pack.offline_url("/read/me-v0.8.html", "index.html", self.inventory)[0], "read/me-v0.8.html")
        self.assertEqual(pack.offline_url("/style.css", "read/me-v0.8.html", self.inventory)[0], "../style.css")
        self.assertEqual(pack.offline_url("/", "read/me-v0.8.html", self.inventory)[0], "../index.html")
        self.assertEqual(pack.offline_url("/works/", "index.html", self.inventory)[0], "works/index.html")
        self.assertEqual(pack.offline_url("#book", "read/me-v0.8.html", self.inventory)[0], "#book")

    def test_missing_asset_fails_but_optional_page_discloses_online_route(self):
        with self.assertRaisesRegex(ValueError, "Missing local asset"):
            pack.offline_url("/art/absent.jpg", "index.html", self.inventory, required=True)
        external, missing = pack.offline_url("/not-in-source/", "index.html", self.inventory)
        self.assertEqual(external, pack.DOMAIN + "/not-in-source/")
        self.assertEqual(missing, "/not-in-source/")

    def test_srcset_css_and_escaped_markup(self):
        html = '<img src="/art/hero.jpg" srcSet="/art/hero.jpg 720w, /art/hero.jpg 1440w">'
        revised, deferred = pack.transform_html(html, "index.html", self.inventory)
        self.assertIn('src="art/hero.jpg"', revised)
        self.assertIn('srcSet="art/hero.jpg 720w, art/hero.jpg 1440w"', revised)
        self.assertFalse(deferred)
        self.assertEqual(pack.transform_css("a{background:url('/art/hero.jpg')}", "style.css", self.inventory),
                         "a{background:url('art/hero.jpg')}")
        with self.assertRaisesRegex(ValueError, "Path traversal"):
            pack.offline_url("/../../secrets", "index.html", self.inventory)

    def test_index_disables_only_the_optional_journey_enhancement(self):
        markup = '<script defer src="/journey.js"></script><a href="/read/me-v0.8.html">Book</a>'
        revised, _ = pack.transform_html(markup, "index.html", self.inventory)
        self.assertNotIn("journey.js", revised)
        self.assertIn('href="read/me-v0.8.html"', revised)


class ExactCandidateBundle(unittest.TestCase):
    def test_actual_bundle_if_already_built(self):
        if not pack.TARGET.is_file():
            self.skipTest("offline bundle generated in CI packaging step")
        with zipfile.ZipFile(pack.TARGET) as bundle:
            self.assertIsNone(bundle.testzip())
            contents = set(bundle.namelist())
            self.assertIn("OPEN_THIS_FIRST.html", contents)
            self.assertIn("site/index.html", contents)
            self.assertIn("site/read/me-v0.8.html", contents)
            self.assertIn("site/resources/mechanical-ethics/MECHANICAL_ETHICS.pdf", contents)
            for figure in pack.FIGURES:
                self.assertIn("site/resources/mechanical-ethics/figures/" + figure, contents)
            manifest = json.loads(bundle.read("MANIFEST_SHA256.json"))
            self.assertEqual(manifest["status"], "DRAFT_OFFLINE_PREVIEW_NOT_PUBLISHED")
            self.assertEqual(
                hashlib.sha256(bundle.read("site/resources/mechanical-ethics/MECHANICAL_ETHICS.md")).hexdigest(),
                pack.RELEASE_SHA)
            for path, expected in manifest["files"].items():
                self.assertEqual(hashlib.sha256(bundle.read(path)).hexdigest(), expected, path)
            home = bundle.read("site/index.html").decode("utf-8")
            book = bundle.read("site/read/me-v0.8.html").decode("utf-8")
            self.assertLess(home.index('class="art-hero"'), home.index('class="human-first-door"'))
            self.assertLess(home.index('class="human-first-door"'), home.index('id="step-story"'))
            self.assertIn('href="read/me-v0.8.html"', home)
            self.assertIn("Released", book)
            self.assertIn("../resources/mechanical-ethics/figures/", book)
            self.assertNotIn('src="/resources/mechanical-ethics/figures/', book)
            self.assertIn('href="site/index.html"', bundle.read("OPEN_THIS_FIRST.html").decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
