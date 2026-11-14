import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("atrs_audit", ROOT / "audit.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


def audit(body: str):
    return mod.audit_page(
        "https://www.gov.uk/algorithmic-transparency-records/example",
        body.encode("utf-8"),
        fetched_at_utc="2026-09-17T00:00:00+00:00",
    )


SAMPLE = """
<html><body><main><h1>Example Tool</h1>
<h2>Tier 2 - Decision-making Processes</h2><p>Context only.</p>
<h3>3.2 - Human review</h3><p>If confidence is low, an officer checks the result.</p>
<h3>3.5 - Appeals and review</h3><p>Users can submit a review at <a href="https://example.gov.uk/review">the review page</a>.</p>
<h2>Tier 2 - Technical Specification and Data</h2>
<h3>4.2.7 - Model performance</h3><p>Precision and recall are monitored quarterly.</p>
<h2>Tier 2 - Risks, Mitigations and Impact Assessments</h2>
<h3>5.1 - Impact assessments</h3><p>A DPIA was completed.</p>
<h3>5.2 - Risks and mitigations</h3><p>Known risk: false positives.</p>
</main><footer><a href="https://example.org/privacy">Privacy</a></footer></body></html>
"""


class ATRSAuditTests(unittest.TestCase):
    def test_exact_field_heading_does_not_match_tier_heading(self):
        row = audit(SAMPLE)
        risk = row["fields"]["risks"]
        self.assertEqual(risk["match_count"], 1)
        self.assertEqual(risk["matches"][0]["heading"], "5.2 - Risks and mitigations")

    def test_plural_impact_assessments_is_recognised(self):
        row = audit(SAMPLE)
        self.assertEqual(row["fields"]["impact_assessment"]["match_count"], 1)

    def test_source_evidence_is_preserved(self):
        row = audit(SAMPLE)
        self.assertEqual(row["title"], "Example Tool")
        self.assertEqual(len(row["source_sha256"]), 64)
        self.assertEqual(row["fetched_at_utc"], "2026-09-17T00:00:00+00:00")
        appeal = row["fields"]["appeals_review"]["matches"][0]
        self.assertIn("Users can submit", appeal["text"])
        self.assertEqual(appeal["contact_tokens"]["hrefs"], ["https://example.gov.uk/review"])

    def test_unrelated_href_is_only_a_syntactic_token_not_a_route_claim(self):
        body = '''<html><main><h3>3.5 - Appeals and review</h3><p>No appeals are available. Read <a href="https://example.org/privacy">our privacy policy</a>.</p></main></html>'''
        row = audit(body)
        field = row["fields"]["appeals_review"]
        self.assertTrue(field["syntactic_contact_token_present"])
        self.assertNotIn("public_route_locator", field)
        self.assertTrue(field["contains_none_or_na_phrase"])

    def test_plain_text_url_is_preserved_as_syntactic_token(self):
        body = '''<html><main><h3>3.5 - Appeals and review</h3><p>Request review at https://example.gov.uk/appeal</p></main></html>'''
        row = audit(body)
        token = row["fields"]["appeals_review"]["matches"][0]["contact_tokens"]
        self.assertEqual(token["urls_in_text"], ["https://example.gov.uk/appeal"])
        self.assertTrue(token["syntactic_contact_token_present"])

    def test_repeated_sections_are_all_preserved(self):
        body = '''
        <html><main><h3>4.2.7 - Model performance</h3><p>None.</p>
        <h3>4.2.7 - Model performance</h3><p>Model B accuracy is 95 percent.</p></main></html>'''
        row = audit(body)
        field = row["fields"]["model_performance"]
        self.assertEqual(field["match_count"], 2)
        self.assertEqual([x["text"] for x in field["matches"]], ["None.", "Model B accuracy is 95 percent."])
        self.assertTrue(field["contains_none_or_na_phrase"])

    def test_none_phrase_is_not_promoted_to_field_semantics(self):
        body = '''<html><main><h3>3.5 - Appeals and review</h3><p>The old process is not applicable. Request review at <a href="/appeal">current route</a>.</p></main></html>'''
        row = audit(body)
        field = row["fields"]["appeals_review"]
        self.assertTrue(field["contains_none_or_na_phrase"])
        self.assertNotIn("states_none_or_not_applicable", field)
        self.assertTrue(field["syntactic_contact_token_present"])

    def test_na_phrase_is_detected_with_following_text(self):
        body = '''<html><main><h3>3.5 - Appeals and review</h3><p>N/A no decisions.</p></main></html>'''
        row = audit(body)
        self.assertTrue(row["fields"]["appeals_review"]["contains_none_or_na_phrase"])

    def test_no_formal_appeals_process_phrase_is_detected(self):
        body = '''<html><main><h3>3.5 - Appeals and review</h3><p>There is no formal appeals process, as the tool does not make decisions.</p></main></html>'''
        row = audit(body)
        self.assertTrue(row["fields"]["appeals_review"]["contains_none_or_na_phrase"])

    def test_footer_content_does_not_bleed_into_last_main_section(self):
        body = '''<html><body><main><h3>3.5 - Appeals and review</h3><p>None.</p></main><footer><a href="https://example.org/privacy">Privacy</a></footer></body></html>'''
        row = audit(body)
        appeal = row["fields"]["appeals_review"]["matches"][0]
        self.assertEqual(appeal["text"], "None.")
        self.assertEqual(appeal["contact_tokens"]["hrefs"], [])
        self.assertFalse(row["fields"]["appeals_review"]["syntactic_contact_token_present"])

    def test_nested_h4_content_remains_inside_parent_field(self):
        body = '''<html><main><h3>4.2.7 - Model performance</h3><h4>Model A</h4><p>Accuracy 91%.</p><h4>Model B</h4><p>Accuracy 93%.</p></main></html>'''
        row = audit(body)
        perf = row["fields"]["model_performance"]
        self.assertEqual(perf["match_count"], 1)
        self.assertIn("Model A", perf["matches"][0]["text"])
        self.assertIn("Accuracy 93%", perf["matches"][0]["text"])

    def test_legacy_no_main_fixture_uses_explicit_fallback(self):
        row = audit('<html><h3>3.5 - Appeals and review</h3><p>None.</p></html>')
        self.assertTrue(row["fields"]["appeals_review"]["section_present"])

    def test_missing_disclosure_is_only_missing_disclosure(self):
        row = audit("<html><main><h2>Tier 1</h2><p>Hello</p></main></html>")
        self.assertFalse(row["fields"]["appeals_review"]["section_present"])
        self.assertEqual(row["fields"]["appeals_review"]["match_count"], 0)

    def test_summary_counts_multiple_matches_separately(self):
        repeated = audit('''<html><main><h3>4.2.7 - Model performance</h3><p>None.</p><h3>4.2.7 - Model performance</h3><p>Accuracy 95%.</p></main></html>''')
        ordinary = audit(SAMPLE)
        summary = mod.summarise([repeated, ordinary])
        self.assertEqual(summary["records"], 2)
        self.assertEqual(summary["fields"]["model_performance"]["records_with_multiple_matches"], 1)


if __name__ == "__main__":
    unittest.main()
