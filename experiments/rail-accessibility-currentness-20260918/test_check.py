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

    def test_out_of_order_is_not_no_lift(self):
        audit = check.classify(
            "Example", "XXX", "There are lifts",
            ["The lifts are out of order between platform 1 and the subway"],
            "The lifts are out of order",
        )
        self.assertEqual(audit.result, "CONSISTENT_EXISTS")
        self.assertEqual(audit.operational, "OUT_OF_SERVICE")

    def test_no_lifts_plus_outage_is_contradiction(self):
        audit = check.classify(
            "Example", "XXX", "There are no lifts",
            ["The lifts are out of order between platform 1 and the subway"],
            "The lifts are out of order",
        )
        self.assertEqual(audit.result, "CONTRADICTION")
        self.assertEqual(audit.operational, "OUT_OF_SERVICE")

    def test_step_free_alone_does_not_invent_lift(self):
        audit = check.classify(
            "Example", "XXX",
            "Step-free category A: there is step-free access to all platforms",
            ["There is step-free access by a ramp"],
            None,
        )
        self.assertEqual(audit.result, "NO_EXISTENCE_COMPARISON")
        self.assertFalse(audit.corroborating_existence)

    def test_missing_lift_status_does_not_negate_installed_lifts(self):
        audit = check.classify(
            "Example", "XXX", "There are no lifts",
            ["Lifts have been installed with access to an overbridge"],
            "No lift information available",
        )
        self.assertEqual(audit.result, "CONTRADICTION")
        self.assertEqual(audit.operational, "UNKNOWN")

    def test_control_can_flip_when_summary_regresses(self):
        data = check.load_cases()
        mutant = copy.deepcopy(data)
        station = next(s for s in mutant["stations"] if s["crs"] == "BIW")
        station["summary"]["observed"] = "There are no lifts"
        audits = {a.crs: a for a in check.frozen_audits(mutant)}
        self.assertEqual(audits["BIW"].result, "CONTRADICTION")


if __name__ == "__main__":
    unittest.main()
