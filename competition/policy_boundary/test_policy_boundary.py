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
        self.assertEqual(report["summary"]["unauthorized_negotiability"], 0)

    def test_lossy_compiler_creates_unauthorized_negotiability(self):
        report = mod.evaluate_all(self.fixtures, "lossy")
        self.assertGreater(report["summary"]["boundary_losses"], 0)
        self.assertGreater(report["summary"]["unauthorized_negotiability"], 0)

    def test_non_authority_is_not_converted_to_negotiable_preference(self):
        report = mod.evaluate_all(self.fixtures, "lossy")
        row = self.row(report, "PB04_non_authority")
        self.assertTrue(row["unauthorized_negotiability"])
        good = self.row(mod.evaluate_all(self.fixtures, "preserving"), "PB04_non_authority")
        self.assertFalse(good["downstream_offer_allowed"])
        self.assertEqual(good["compiled"]["value_state"], "specified")
        self.assertEqual(good["compiled"]["authority_state"], "not_authorized")

    def test_ordinary_preference_remains_negotiable_positive_control(self):
        good = self.row(mod.evaluate_all(self.fixtures, "preserving"), "PB08_ordinary_preference")
        self.assertTrue(good["downstream_offer_allowed"])
        self.assertTrue(good["state_match"])

    def test_refusal_withheld_and_unresolved_are_distinct(self):
        report = mod.evaluate_all(self.fixtures, "preserving")
        states = {
            self.row(report, "PB01_unresolved")["compiled"]["value_state"],
            self.row(report, "PB02_refused")["compiled"]["value_state"],
            self.row(report, "PB03_withheld")["compiled"]["value_state"],
        }
        self.assertEqual(states, {"unresolved", "refused", "withheld"})

    def test_revocation_is_not_ordinary_preference_change(self):
        row = self.row(mod.evaluate_all(self.fixtures, "preserving"), "PB07_revoked")
        self.assertEqual(row["compiled"]["authority_state"], "revoked")
        self.assertFalse(row["downstream_offer_allowed"])

    def test_claim_ceiling_is_explicit(self):
        report = mod.evaluate_all(self.fixtures, "preserving")
        self.assertIn("not a model result", report["claim_ceiling"])


if __name__ == "__main__":
    unittest.main()
