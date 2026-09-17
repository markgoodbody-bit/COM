import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("atrs_reader_lens", ROOT / "reader_lens.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


def row(title="Example tool", url="https://www.gov.uk/algorithmic-transparency-records/example"):
    return {
        "title": title,
        "url": url,
        "source_sha256": "a" * 64,
        "fetched_at_utc": "2026-09-17T12:00:00+00:00",
        "heading_profile": "current_named_family",
        "fields": {
            "appeals_review": {
                "section_present": True,
                "syntactic_contact_token_present": True,
                "matches": [{
                    "text": "A person may request review using https://example.gov.uk/review.",
                    "contact_tokens": {
                        "hrefs": [],
                        "urls_in_text": ["https://example.gov.uk/review"],
                        "emails": ["review@example.gov.uk"],
                        "phones": ["020 7946 0958"],
                    },
                }],
            },
            "human_review": {"matches": [{"text": "An officer reviews low-confidence outputs."}]},
            "senior_responsible_owner": {"matches": [{"text": "Director Example."}]},
        },
    }


class ReaderLensTests(unittest.TestCase):
    def test_card_preserves_source_text_and_original_source_link(self):
        page = mod.card(row(), [])
        self.assertIn("A person may request review", page)
        self.assertIn("Open original GOV.UK record", page)
        self.assertIn("Do not infer route effectiveness", page)

    def test_http_and_email_tokens_are_actionable_but_phone_is_not(self):
        page = mod.card(row(), [])
        self.assertIn('href="https://example.gov.uk/review"', page)
        self.assertIn('href="mailto:review@example.gov.uk"', page)
        self.assertNotIn('href="tel:', page)
        self.assertIn("Detected number; verify context in the source text", page)

    def test_relative_or_unsafe_href_is_not_made_actionable(self):
        r = row()
        r["fields"]["appeals_review"]["matches"][0]["contact_tokens"] = {
            "hrefs": ["/relative-route", "javascript:alert(1)"],
            "urls_in_text": [], "emails": [], "phones": [],
        }
        page = mod.card(r, [])
        self.assertIn("/relative-route", page)
        self.assertNotIn('href="/relative-route"', page)
        self.assertNotIn('href="javascript:', page)

    def test_card_does_not_call_contact_token_an_appeal_right(self):
        page = mod.card(row(), [])
        self.assertNotIn("appeal right established", page.lower())
        self.assertIn("Presence does not establish relevance, a legal right, or route effectiveness", page)

    def test_missing_appeals_field_is_bounded_to_disclosure(self):
        r = row()
        r["fields"]["appeals_review"] = {
            "section_present": False,
            "syntactic_contact_token_present": False,
            "matches": [],
        }
        page = mod.card(r, [])
        self.assertIn("No parser-recognised Appeals and review field was observed", page)
        self.assertIn("not about whether a route or practice exists elsewhere", page)

    def test_html_escapes_published_text(self):
        r = row(title="<script>alert(1)</script>")
        r["fields"]["appeals_review"]["matches"][0]["text"] = "<b>published</b>"
        page = mod.card(r, [])
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("&lt;b&gt;published&lt;/b&gt;", page)

    def test_semantic_annotations_are_explicitly_exploratory(self):
        page = mod.card(row(), ["PUBLIC_INITIATION"])
        self.assertIn("Concrete initiation described", page)
        self.assertIn("Exploratory annotations — post-pilot; not validated", page)
        self.assertIn("Exploratory annotation; not validated classification", page)

    def test_annotation_search_is_separate_from_source_search(self):
        page = mod.card(row(), ["PUBLIC_INITIATION"])
        self.assertIn('data-source-search=', page)
        self.assertIn('data-annotation-search=', page)
        # The machine label must not contaminate the source-search attribute.
        source_attr = page.split('data-source-search="', 1)[1].split('"', 1)[0]
        self.assertNotIn("public_initiation", source_attr)
        self.assertIn("public_initiation", page.lower())

    def test_exploratory_annotations_are_hidden_and_opt_in(self):
        report = {"records": [row()]}
        page = mod.build_html(report, {row()["url"]: ["PUBLIC_INITIATION"]})
        self.assertIn(".annotations { display: none", page)
        self.assertIn(".show-annotations .annotations { display: block", page)
        self.assertIn('id="annotations" type="checkbox"', page)
        self.assertIn("off by default", page)
        self.assertIn("annotations.checked && needle", page)

    def test_build_html_has_accessible_search_status_reset_and_advanced_filters(self):
        report = {"records": [row()]}
        page = mod.build_html(report, {})
        self.assertIn('label for="q"', page)
        self.assertIn('role="status" aria-live="polite"', page)
        self.assertIn('id="reset"', page)
        self.assertIn('id="reset-empty"', page)
        self.assertIn("Advanced evidence filters", page)
        self.assertIn("Published Appeals and review field", page)
        self.assertIn("Published link/contact-like token in that field", page)
        self.assertIn("not legal advice", page)

    def test_cards_are_compact_with_evidence_details(self):
        page = mod.card(row(), [])
        self.assertIn('<details class="record-details">', page)
        self.assertIn("Evidence details", page)
        self.assertIn("Frozen 2026-09-17", page)
        # Hash remains available but does not lead the summary.
        self.assertIn("Source SHA-256", page)

    def test_semantic_map_rejects_unbound_annotations(self):
        report = {"records": [row()]}
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "semantic.json"
            path.write_text(json.dumps({"records": []}), encoding="utf-8")
            with self.assertRaises(ValueError):
                mod.semantic_map(report, path)


if __name__ == "__main__":
    unittest.main()
