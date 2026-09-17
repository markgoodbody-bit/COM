import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("no_free_qaly", ROOT / "benchmark.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class NoFreeQalyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
        cls.report = mod.build_report(cls.cases)

    def test_accuracy_and_expected_utility_reverse_cross_case_ranking(self):
        self.assertTrue(self.report["objective_rank_reversal"])
        self.assertEqual(
            self.report["objective_rankings"]["accuracy_gain"],
            ["low_stakes_classification", "high_stakes_triage"],
        )
        self.assertEqual(
            self.report["objective_rankings"]["expected_utility_gain"],
            ["high_stakes_triage", "low_stakes_classification"],
        )

    def test_eui_and_certainty_equivalent_gain_reverse_cross_problem_ranking(self):
        self.assertTrue(self.report["monetary_rank_reversal"])
        self.assertEqual(
            self.report["monetary_rankings"]["expected_utility_increase"],
            ["money_problem_a", "money_problem_b"],
        )
        self.assertEqual(
            self.report["monetary_rankings"]["certainty_equivalent_gain"],
            ["money_problem_b", "money_problem_a"],
        )

    def test_preference_sensitive_case_has_no_objective_accuracy(self):
        p = self.report["preference_sensitive_case"]
        self.assertEqual(p["accuracy"], "UNDEFINED_NO_OBJECTIVE_CORRECT_ACTION")

    def test_stakeholder_values_reverse_intervention_ranking(self):
        self.assertTrue(self.report["stakeholder_rank_reversal"])
        p = self.report["preference_sensitive_case"]["stakeholders"]
        self.assertEqual(p["benefit_priority"]["ranking"][0], "push_aggressive")
        self.assertEqual(p["burden_priority"]["ranking"][0], "push_conservative")

    def test_contract_does_not_output_universal_score(self):
        self.assertNotIn("decision_quality_score", self.report)
        self.assertIn("counterfactual_baseline", self.report["minimum_measurement_contract"])
        self.assertIn("outcome_or_value_function_and_whose_values", self.report["minimum_measurement_contract"])


if __name__ == "__main__":
    unittest.main()
