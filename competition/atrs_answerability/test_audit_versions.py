import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("atrs_audit_versions", ROOT / "audit.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


def audit(body: str):
    return mod.audit_page(
        "https://www.gov.uk/algorithmic-transparency-records/legacy-example",
        body.encode("utf-8"),
        fetched_at_utc="2026-09-17T00:00:00+00:00",
    )


LEGACY = """
<html><body><main><h1>Legacy Tool</h1>
<h3>3.3 Human decisions</h3><p>A human makes the final decision.</p>
<h3>3.5 Appeals and review</h3><p>Existing appeal process applies.</p>
<h3>5.1 Impact assessment name</h3><p>DPIA</p>
<h3>5.2 Impact assessment description</h3><p>Assessment description.</p>
<h3>5.3 Impact assessment date</h3><p>2024-01-01</p>
<h3>5.4 Impact assessment link</h3><p>https://example.gov.uk/dpia</p>
<h3>5.5 Risk name</h3><p>False positive</p>
<h3>5.6 Risk description</h3><p>Description</p>
<h3>5.7 Risk mitigation</h3><p>Human check</p>
<h3>6.1 Maintenance</h3><p>Annual review</p>
<h3>1.4 Senior responsible owner</h3><p>Director</p>
</main></body></html>
"""

MIXED = """
<html><body><main><h1>Transition Tool</h1>
<h3>3.3 - Human decisions and review</h3><p>Officer review.</p>
<h3>3.5 - Appeals and review</h3><p>Existing process.</p>
<h3>5.1 - Impact assessment name</h3><p>DPIA</p>
<h3>5.5 - Risk name</h3><p>Risk</p>
</main></body></html>
"""

CURRENT = """
<html><body><main><h1>Current Tool</h1>
<h3>3.4 - Human decisions and review</h3><p>Officer review.</p>
<h3>3.6 - Appeals and review</h3><p>Complaint route.</p>
<h3>4.2.7 - Model performance</h3><p>Accuracy 90%.</p>
<h3>5.1 - Impact assessment</h3><p>DPIA complete.</p>
<h3>5.2 - Risks and mitigations</h3><p>Risk and mitigation.</p>
<h3>6.1 - Maintenance</h3><p>Annual.</p>
<h3>1.4 - Senior responsible owner</h3><p>Director.</p>
</main></body></html>
"""


class HeadingFamilyTests(unittest.TestCase):
    def test_legacy_2024_family_is_detected(self):
        self.assertEqual(audit(LEGACY)["heading_profile"], "legacy_2024_family")

    def test_mixed_transition_family_is_detected(self):
        self.assertEqual(audit(MIXED)["heading_profile"], "mixed_known_families")

    def test_legacy_human_decisions_is_human_review_disclosure(self):
        field = audit(LEGACY)["fields"]["human_review"]
        self.assertTrue(field["section_present"])
        self.assertEqual(field["matches"][0]["heading"], "3.3 Human decisions")

    def test_legacy_impact_subfields_are_preserved(self):
        field = audit(LEGACY)["fields"]["impact_assessment"]
        self.assertEqual(field["match_count"], 4)
        self.assertEqual([x["heading"] for x in field["matches"]], [
            "5.1 Impact assessment name",
            "5.2 Impact assessment description",
            "5.3 Impact assessment date",
            "5.4 Impact assessment link",
        ])

    def test_legacy_risk_subfields_are_preserved(self):
        self.assertEqual(audit(LEGACY)["fields"]["risks"]["match_count"], 3)

    def test_model_performance_absence_is_contextualised_for_legacy_family(self):
        field = audit(LEGACY)["fields"]["model_performance"]
        self.assertFalse(field["section_present"])
        self.assertEqual(field["heading_family_context"], "not_present_in_known_legacy_or_transition_family")

    def test_model_performance_absence_is_contextualised_for_transition_family(self):
        field = audit(MIXED)["fields"]["model_performance"]
        self.assertFalse(field["section_present"])
        self.assertEqual(field["heading_family_context"], "not_present_in_known_legacy_or_transition_family")

    def test_current_family_does_not_infer_requirement(self):
        row = audit(CURRENT)
        self.assertEqual(row["heading_profile"], "current_named_family")
        self.assertEqual(row["fields"]["model_performance"]["heading_family_context"], "no_template_requirement_inferred")

    def test_summary_separates_observed_absence_from_known_family_context(self):
        legacy = audit(LEGACY)
        mixed = audit(MIXED)
        current = audit(CURRENT)
        summary = mod.summarise([legacy, mixed, current])
        self.assertEqual(summary["fields"]["human_review"]["section_present"], 3)
        self.assertEqual(summary["fields"]["risks"]["section_present"], 3)
        self.assertEqual(summary["fields"]["impact_assessment"]["section_present"], 3)
        self.assertEqual(summary["fields"]["model_performance"]["section_not_observed"], 2)
        self.assertEqual(summary["fields"]["model_performance"]["known_family_without_field"], 2)


if __name__ == "__main__":
    unittest.main()
