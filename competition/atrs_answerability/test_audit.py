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

SAMPLE = """
<html><body>
<h2>Tier 2 - Decision-making Processes</h2>
<p>Context only.</p>
<h3>3.2 - Human review</h3>
<p>If confidence is low, an officer checks the result before any decision.</p>
<h3>3.5 - Appeals and review</h3>
<p>Users can submit a review request at <a href="https://example.gov.uk/review">the public review page</a>.</p>
<h2>Tier 2 - Technical Specification and Data</h2>
<h3>4.2.7 - Model performance</h3>
<p>Precision and recall are monitored quarterly.</p>
<h2>Tier 2 - Risks, Mitigations and Impact Assessments</h2>
<p>This category heading is not itself a risk disclosure.</p>
<h3>5.1 - Impact assessments</h3>
<p>A DPIA was completed.</p>
<h3>5.2 - Risks and mitigations</h3>
<p>Known risk: false positives; mitigation: manual check.</p>
</body></html>
"""

SAMPLE_NONE = """
<html><body>
<h3>3.2 - Human review</h3><p>No human review as no decision making capability.</p>
<h3>3.5 - Appeals and review</h3><p>Not applicable.</p>
</body></html>
"""

SAMPLE_CONTACT_WORD_ONLY = """
<html><body>
<h3>3.5 - Appeals and review</h3>
<p>The Contact Centre team reviews routing and may transfer a user to an advisor or email channel.</p>
</body></html>
"""

SAMPLE_PHONE = """
<html><body>
<h3>3.5 - Appeals and review</h3>
<p>Users can call 0800 011 3797 for help.</p>
</body></html>
"""


class ATRSAuditTests(unittest.TestCase):
    def test_sections_extract_by_heading(self):
        sections = mod.parse_sections(SAMPLE)
        human = mod.find_section(sections, mod.FIELD_PATTERNS["human_review"])
        appeals = mod.find_section(sections, mod.FIELD_PATTERNS["appeals_review"])
        self.assertIsNotNone(human)
        self.assertIsNotNone(appeals)
        self.assertIn("officer checks", human.text)

    def test_category_heading_is_not_mistaken_for_risk_field(self):
        row = mod.audit_record({"title": "x", "url": "u"}, SAMPLE)
        risk = row["fields"]["risks"]
        self.assertEqual(risk["heading"], "5.2 - Risks and mitigations")
        self.assertGreater(risk["characters"], 0)

    def test_plural_impact_assessments_is_recognised(self):
        row = mod.audit_record({"title": "x", "url": "u"}, SAMPLE)
        impact = row["fields"]["impact_assessment"]
        self.assertTrue(impact["section_present"])
        self.assertEqual(impact["heading"], "5.1 - Impact assessments")

    def test_appeal_href_is_public_route_locator(self):
        row = mod.audit_record({"title": "x", "url": "u"}, SAMPLE)
        self.assertTrue(row["fields"]["appeals_review"]["public_route_locator"])

    def test_phone_is_public_route_locator(self):
        row = mod.audit_record({"title": "x", "url": "u"}, SAMPLE_PHONE)
        self.assertTrue(row["fields"]["appeals_review"]["public_route_locator"])

    def test_generic_contact_word_is_not_public_route_locator(self):
        row = mod.audit_record({"title": "x", "url": "u"}, SAMPLE_CONTACT_WORD_ONLY)
        self.assertFalse(row["fields"]["appeals_review"]["public_route_locator"])

    def test_route_locator_is_only_interpreted_for_appeals_field(self):
        row = mod.audit_record({"title": "x", "url": "u"}, SAMPLE)
        self.assertFalse(row["fields"]["human_review"]["public_route_locator"])
        self.assertFalse(row["fields"]["risks"]["public_route_locator"])

    def test_explicit_none_is_preserved(self):
        row = mod.audit_record({"title": "x", "url": "u"}, SAMPLE_NONE)
        self.assertTrue(row["fields"]["human_review"]["states_none_or_not_applicable"])
        self.assertTrue(row["fields"]["appeals_review"]["states_none_or_not_applicable"])

    def test_missing_field_is_not_inferred_absent_in_reality(self):
        row = mod.audit_record({"title": "x", "url": "u"}, "<html><body><h2>Tier 1</h2><p>Hello</p></body></html>")
        self.assertFalse(row["fields"]["appeals_review"]["section_present"])

    def test_summary_counts_observations_only(self):
        rows = [
            mod.audit_record({"title": "a", "url": "a"}, SAMPLE),
            mod.audit_record({"title": "b", "url": "b"}, SAMPLE_NONE),
        ]
        summary = mod.summarise(rows)
        self.assertEqual(summary["records"], 2)
        self.assertEqual(summary["fields"]["appeals_review"]["section_present"], 2)
        self.assertEqual(summary["fields"]["appeals_review"]["states_none_or_not_applicable"], 1)
        self.assertEqual(summary["fields"]["appeals_review"]["public_route_locator"], 1)
        self.assertNotIn("public_route_locator", summary["fields"]["risks"])


if __name__ == "__main__":
    unittest.main()
