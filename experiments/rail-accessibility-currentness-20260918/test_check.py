import copy
import unittest

import check


class RailAccessibilityCurrentnessTests(unittest.TestCase):
    def test_frozen_contract(self):
        data = check.load_cases()
        audits = {a.crs: a for a in check.frozen_audits(data)}
        self.assertEqual(audits["HIR"].result, "CONTRADICTION")
        self.assertEqual(audits["IRL"].result, "CONTRADICTION")
        self.assertEqual(audits["DSY"].result, "CONTRADICTION")
        self.assertEqual(audits["BIW"].result, "CONSISTENT_EXISTS")
        self.assertEqual(audits["AGV"].result, "CONSISTENT_EXISTS")
        self.assertEqual(audits["LLE"].result, "CONSISTENT_EXISTS")

    def test_outage_is_existence_evidence_not_operational_claim(self):
        audit = check.classify(
            "Example",
            "XXX",
            "There are no lifts",
            ["The lifts are out of order between platform 1 and the subway"],
        )
        self.assertEqual(audit.result, "CONTRADICTION")
        self.assertTrue(audit.corroborating_existence)
        self.assertFalse(hasattr(audit, "operational"))

    def test_step_free_alone_does_not_invent_lift(self):
        audit = check.classify(
            "Example",
            "XXX",
            "Step-free category A: there is step-free access to all platforms",
            ["There is step-free access by a ramp"],
        )
        self.assertEqual(audit.result, "NO_EXISTENCE_COMPARISON")
        self.assertFalse(audit.corroborating_existence)

    def test_installed_lifts_survive_missing_status(self):
        audit = check.classify(
            "Example",
            "XXX",
            "There are no lifts",
            ["Lifts have been installed with access to an overbridge. No lift information available."],
        )
        self.assertEqual(audit.result, "CONTRADICTION")

    def test_negated_positive_phrases_do_not_invent_lift(self):
        for text in (
            "There is no lift access available.",
            "No lifts have been installed at this station.",
            "Access is provided without a lift 1 connection.",
        ):
            with self.subTest(text=text):
                self.assertFalse(check.existence_signal(text))

    def test_partial_fetch_without_positive_evidence_is_unknown(self):
        audit = check.classify(
            "Example",
            "XXX",
            "There are no lifts",
            [],
            corroborating_fetch_complete=False,
        )
        self.assertEqual(audit.result, "FETCH_UNKNOWN")

    def test_control_can_flip_when_summary_regresses(self):
        data = check.load_cases()
        mutant = copy.deepcopy(data)
        station = next(s for s in mutant["stations"] if s["crs"] == "BIW")
        station["summary"]["observed"] = "There are no lifts"
        audits = {a.crs: a for a in check.frozen_audits(mutant)}
        self.assertEqual(audits["BIW"].result, "CONTRADICTION")


if __name__ == "__main__":
    unittest.main()
