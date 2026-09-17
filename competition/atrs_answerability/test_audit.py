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
<p>Users can submit a review request to the service team at <a href="mailto:review@example.gov.uk">review@example.gov.uk</a>.</p>
<h2>Tier 2 - Technical Specification and Data</h2>
<h3>4.5 - Model performance</h3>
<p>Precision and recall are monitored quarterly.</p>
<h2>Tier 2 - Risks, Mitigations and Impact Assessments</h2>
<h3>5.1 - Impact assessment</h3>
<p>A DPIA was completed.</p>
<h3>5.2 - Risks</h3>
<p>Known risk: false positives.</p>
</body></html>
"""

SAMPLE_NONE = """
<html><body>
<h3>3.2 - Human review</h3><p>No human review as no decision making capability.</p>
<h3>3.5 - Appeals and review</h3><p>Not applicable.</p>
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

    def test_appeal_route_locator_is_observable_not_quality_score(self):
        row = mod.audit_record({"title": "x", "url": "u"}, SAMPLE)
        a = row["fields"]["appeals_review"]
        self.assertTrue(a["section_present"])
        self.assertTrue(a["public_route_locator"])
        self.assertFalse(a["states_none_or_not_applicable"])

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
        s = mod.summarise(rows)
        self.assertEqual(s["records"], 2)
        self.assertEqual(s["fields"]["appeals_review"]["section_present"], 2)
        self.assertEqual(s["fields"]["appeals_review"]["states_none_or_not_applicable"], 1)
        self.assertEqual(s["fields"]["appeals_review"]["public_route_locator"], 1)


if __name__ == "__main__":
    unittest.main()
