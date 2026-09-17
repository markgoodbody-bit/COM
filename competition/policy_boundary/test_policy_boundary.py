import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("policy_boundary", HERE / "policy_boundary.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class PolicyBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = mod.load_fixtures(HERE / "fixtures.json")

    def row(self, report, case_id):
        return next(r for r in report["cases"] if r["case_id"] == case_id)

    def test_preserving_reference_matches_all_frozen_cases(self):
        report = mod.evaluate_all(self.fixtures, "preserving")
        self.assertEqual(report["summary"]["state_matches"], report["summary"]["total"])
        self.assertEqual(report["summary"]["consequence_matches"], report["summary"]["total"])
        self.assertEqual(report["summary"]["unsafe_escalations"], 0)
        self.assertEqual(report["summary"]["missed_permissions"], 0)

    def test_lossy_compiler_creates_multiple_unsafe_consequences(self):
        report = mod.evaluate_all(self.fixtures, "lossy")
        self.assertGreater(report["summary"]["boundary_losses"], 0)
        self.assertGreater(report["summary"]["unsafe_escalations"], 0)

    def test_non_authority_allows_disclosure_but_not_bargain_or_commit(self):
        good = self.row(mod.evaluate_all(self.fixtures, "preserving"), "PB04_non_authority")
        self.assertTrue(good["actual_actions"]["clarify"])
        self.assertTrue(good["actual_actions"]["disclose_value"])
        self.assertFalse(good["actual_actions"]["bargain"])
        self.assertFalse(good["actual_actions"]["commit"])
        self.assertEqual(good["compiled"]["authority_state"], "not_authorized")

    def test_fixed_boundary_can_be_stated_without_becoming_tradeable(self):
        good = self.row(mod.evaluate_all(self.fixtures, "preserving"), "PB05_non_negotiable")
        self.assertTrue(good["actual_actions"]["clarify"])
        self.assertTrue(good["actual_actions"]["disclose_value"])
        self.assertFalse(good["actual_actions"]["bargain"])
        self.assertFalse(good["actual_actions"]["commit"])

    def test_ordinary_preference_is_positive_control_for_bargaining(self):
        good = self.row(mod.evaluate_all(self.fixtures, "preserving"), "PB08_ordinary_preference")
        self.assertTrue(good["actual_actions"]["bargain"])
        self.assertFalse(good["actual_actions"]["commit"])
        self.assertTrue(good["consequence_match"])

    def test_explicit_delegation_is_positive_control_for_commitment(self):
        good = self.row(mod.evaluate_all(self.fixtures, "preserving"), "PB09_delegated_commit")
        self.assertTrue(good["actual_actions"]["bargain"])
        self.assertTrue(good["actual_actions"]["commit"])

    def test_refusal_withheld_and_unresolved_have_different_consequences(self):
        report = mod.evaluate_all(self.fixtures, "preserving")
        unresolved = self.row(report, "PB01_unresolved")
        refused = self.row(report, "PB02_refused")
        withheld = self.row(report, "PB03_withheld")
        self.assertTrue(unresolved["actual_actions"]["clarify"])
        self.assertFalse(refused["actual_actions"]["clarify"])
        self.assertFalse(withheld["actual_actions"]["clarify"])
        self.assertEqual(
            {
                unresolved["compiled"]["value_state"],
                refused["compiled"]["value_state"],
                withheld["compiled"]["value_state"],
            },
            {"unresolved", "refused", "withheld"},
        )

    def test_revocation_blocks_old_authority_but_allows_reclarification(self):
        row = self.row(mod.evaluate_all(self.fixtures, "preserving"), "PB07_revoked")
        self.assertEqual(row["compiled"]["authority_state"], "revoked")
        self.assertTrue(row["actual_actions"]["clarify"])
        self.assertFalse(row["actual_actions"]["bargain"])
        self.assertFalse(row["actual_actions"]["commit"])

    def test_lossy_compiler_oversteps_refusal_and_withheld(self):
        report = mod.evaluate_all(self.fixtures, "lossy")
        for case_id in ("PB02_refused", "PB03_withheld"):
            row = self.row(report, case_id)
            self.assertIn("disclose_value", row["unsafe_escalations"])
            self.assertIn("bargain", row["unsafe_escalations"])
            self.assertIn("commit", row["unsafe_escalations"])

    def test_claim_ceiling_is_explicit(self):
        report = mod.evaluate_all(self.fixtures, "preserving")
        self.assertIn("not a model result", report["claim_ceiling"])


if __name__ == "__main__":
    unittest.main()
