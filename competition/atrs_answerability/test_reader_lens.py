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
        "fields": {
            "appeals_review": {
                "section_present": True,
                "syntactic_contact_token_present": True,
                "matches": [{
                    "text": "A person may request review using https://example.gov.uk/review.",
                    "contact_tokens": {
                        "hrefs": [],
                        "urls_in_text": ["https://example.gov.uk/review"],
                        "emails": [],
                        "phones": [],
                    },
                }],
            },
            "human_review": {"matches": [{"text": "An officer reviews low-confidence outputs."}]},
            "senior_responsible_owner": {"matches": [{"text": "Director Example."}]},
        },
    }


class ReaderLensTests(unittest.TestCase):
    def test_card_preserves_source_text_and_link(self):
        page = mod.card(row(), [])
        self.assertIn("A person may request review", page)
        self.assertIn("https://example.gov.uk/review", page)
        self.assertIn("Open GOV.UK source", page)
        self.assertIn("Do not infer route effectiveness", page)

    def test_card_does_not_call_contact_token_an_appeal_right(self):
        page = mod.card(row(), [])
        self.assertNotIn("appeal right established", page.lower())
        self.assertIn("Published contact / link tokens", page)

    def test_missing_appeals_field_is_bounded_to_disclosure(self):
        r = row()
        r["fields"]["appeals_review"] = {
            "section_present": False,
            "syntactic_contact_token_present": False,
            "matches": [],
        }
        page = mod.card(r, [])
        self.assertIn("No parser-recognised Appeals and review field was observed", page)
        self.assertIn("does not mean no route exists", page)

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

    def test_exploratory_annotations_are_hidden_by_default(self):
        report = {"records": [row()]}
        page = mod.build_html(report, {row()["url"]: ["PUBLIC_INITIATION"]})
        self.assertIn(".annotations { display: none", page)
        self.assertIn(".show-annotations .annotations { display: block", page)
        self.assertIn('id="annotations" type="checkbox"', page)
        self.assertIn("hidden by default", page)

    def test_build_html_has_search_filters_and_claim_ceilings(self):
        report = {"records": [row()]}
        page = mod.build_html(report, {})
        self.assertIn("ATRS Reader Lens", page)
        self.assertIn("Search tool, organisation or disclosed text", page)
        self.assertIn("Appeals field: any", page)
        self.assertIn("Contact token: any", page)
        self.assertIn("not a transparency score", page)
        self.assertIn("data-search=", page)

    def test_semantic_map_rejects_unbound_annotations(self):
        report = {"records": [row()]}
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "semantic.json"
            path.write_text(json.dumps({"records": []}), encoding="utf-8")
            with self.assertRaises(ValueError):
                mod.semantic_map(report, path)


if __name__ == "__main__":
    unittest.main()
