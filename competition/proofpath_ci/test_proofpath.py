import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("proofpath", HERE / "proofpath.py")
proofpath = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(proofpath)


class ProofPathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = json.loads((HERE / "fixtures" / "demo.json").read_text(encoding="utf-8"))

    def result_by_id(self, report, mutation_id):
        return next(x for x in report["mutations"] if x["mutation_id"] == mutation_id)

    def test_repetition_counter_is_caught_by_duplicate(self):
        report = proofpath.evaluate(self.case, "repetition_counter")
        row = self.result_by_id(report, "M1_duplicate_support")
        self.assertTrue(row["violated"])
        self.assertGreater(row["delta"], 0)
        self.assertEqual(row["baseline_root_count"], row["mutant_root_count"])
        self.assertGreater(row["mutant_source_count"], row["baseline_source_count"])

    def test_lineage_aware_does_not_strengthen_on_duplicate(self):
        report = proofpath.evaluate(self.case, "lineage_aware")
        row = self.result_by_id(report, "M1_duplicate_support")
        self.assertFalse(row["violated"])
        self.assertEqual(row["delta"], 0)

    def test_lineage_aware_responds_to_independent_contradiction(self):
        report = proofpath.evaluate(self.case, "lineage_aware")
        row = self.result_by_id(report, "M3_independent_contradiction")
        self.assertFalse(row["violated"])
        self.assertLess(row["delta"], 0)
        self.assertEqual(row["mutant_root_count"], row["baseline_root_count"] + 1)

    def test_evidence_blind_fails_responsiveness_relations(self):
        report = proofpath.evaluate(self.case, "evidence_blind")
        self.assertTrue(self.result_by_id(report, "M2_retract_origin")["violated"])
        self.assertTrue(self.result_by_id(report, "M3_independent_contradiction")["violated"])

    def test_retraction_weakens_lineage_aware(self):
        report = proofpath.evaluate(self.case, "lineage_aware")
        row = self.result_by_id(report, "M2_retract_origin")
        self.assertFalse(row["violated"])
        self.assertLess(row["delta"], 0)

    def test_wrong_lineage_is_marked_control_not_pass_evidence(self):
        report = proofpath.evaluate(self.case, "lineage_aware")
        row = self.result_by_id(report, "M4_wrong_lineage_control")
        self.assertEqual(row["relation"], "negative_control")
        self.assertFalse(row["violated"])

    def test_cycle_fails_closed(self):
        bad = json.loads(json.dumps(self.case))
        bad["sources"][0]["derived_from"] = "news_summary"
        with self.assertRaises(ValueError):
            proofpath.validate_case(bad)

    def test_missing_parent_fails_closed(self):
        bad = json.loads(json.dumps(self.case))
        bad["sources"][1]["derived_from"] = "missing"
        with self.assertRaises(ValueError):
            proofpath.validate_case(bad)

    def test_html_preserves_claim_ceiling(self):
        report = proofpath.evaluate(self.case, "repetition_counter")
        output = proofpath.render_html(report)
        self.assertIn("not a model result", output)
        self.assertIn("M1_duplicate_support", output)


if __name__ == "__main__":
    unittest.main()
