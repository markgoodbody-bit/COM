import importlib.util
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("proofpath", HERE / "proofpath.py")
proofpath = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = proofpath
SPEC.loader.exec_module(proofpath)


class ProofPathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = json.loads(
            (HERE / "fixtures" / "demo.json").read_text(encoding="utf-8")
        )

    def result_by_id(self, report, mutation_id):
        return next(
            x for x in report["mutations"] if x["mutation_id"] == mutation_id
        )

    def test_unchanged_control_is_real_and_clean(self):
        report = proofpath.evaluate(self.case, "lineage_aware")
        row = self.result_by_id(report, "M0_unchanged_control")
        self.assertEqual(row["status"], "CONTROL_OK")
        self.assertEqual(row["delta"], 0)
        self.assertEqual(row["action_delta"], 0)

    def test_duplicate_is_powered_and_catches_repetition_counter(self):
        report = proofpath.evaluate(self.case, "repetition_counter")
        row = self.result_by_id(report, "M1_duplicate_support")
        self.assertTrue(row["powered"])
        self.assertTrue(row["vulnerable_control_violated"])
        self.assertFalse(row["reference_control_violated"])
        self.assertEqual(row["status"], "FAIL")
        self.assertTrue(row["violated"])
        self.assertGreater(row["delta"], 0)
        self.assertEqual(row["baseline_root_count"], row["mutant_root_count"])
        self.assertGreater(
            row["mutant_source_count"], row["baseline_source_count"]
        )

    def test_lineage_aware_passes_powered_duplicate(self):
        report = proofpath.evaluate(self.case, "lineage_aware")
        row = self.result_by_id(report, "M1_duplicate_support")
        self.assertTrue(row["powered"])
        self.assertEqual(row["status"], "PASS")
        self.assertFalse(row["violated"])
        self.assertEqual(row["delta"], 0)

    def test_action_only_escalation_is_not_invisible(self):
        report = proofpath.evaluate(self.case, "action_only_escalator")
        row = self.result_by_id(report, "M1_duplicate_support")
        self.assertTrue(row["powered"])
        self.assertEqual(row["baseline_strength"], row["mutant_strength"])
        self.assertEqual(row["baseline_action"], "hold")
        self.assertEqual(row["mutant_action"], "proceed")
        self.assertTrue(row["action_violated"])
        self.assertEqual(row["status"], "FAIL")

    def test_retraction_restatement_is_powered(self):
        vulnerable = proofpath.evaluate(self.case, "repetition_counter")
        reference = proofpath.evaluate(self.case, "lineage_aware")
        bad = self.result_by_id(vulnerable, "M2_retract_origin_restate")
        good = self.result_by_id(reference, "M2_retract_origin_restate")
        self.assertTrue(bad["powered"])
        self.assertEqual(bad["status"], "FAIL")
        self.assertEqual(bad["delta"], 0)
        self.assertEqual(good["status"], "PASS")
        self.assertLess(good["delta"], 0)
        self.assertEqual(good["mutant_root_count"], 0)

    def test_independent_contradiction_guard_uses_blind_reference_pair(self):
        reference = proofpath.evaluate(self.case, "lineage_aware")
        blind = proofpath.evaluate(self.case, "evidence_blind")
        good = self.result_by_id(reference, "M3_independent_contradiction")
        bad = self.result_by_id(blind, "M3_independent_contradiction")
        self.assertTrue(good["powered"])
        self.assertTrue(good["vulnerable_control_violated"])
        self.assertFalse(good["reference_control_violated"])
        self.assertEqual(good["status"], "PASS")
        self.assertFalse(good["violated"])
        self.assertLess(good["delta"], 0)
        self.assertEqual(
            good["mutant_root_count"], good["baseline_root_count"] + 1
        )
        self.assertTrue(bad["powered"])
        self.assertEqual(bad["status"], "FAIL")
        self.assertTrue(bad["violated"])
        self.assertEqual(bad["delta"], 0)

    def test_wrong_lineage_is_sensitivity_not_correctness(self):
        report = proofpath.evaluate(self.case, "lineage_aware")
        row = self.result_by_id(report, "M4_wrong_lineage_control")
        self.assertEqual(row["role"], "sensitivity_control")
        self.assertEqual(row["status"], "SENSITIVITY")
        self.assertIsNone(row["violated"])
        self.assertGreater(row["delta"], 0)

    def test_baseline_structure_is_first_class(self):
        report = proofpath.evaluate(self.case, "repetition_counter")
        structure = report["baseline_structure"]
        self.assertEqual(structure["visible_sources"], 2)
        self.assertEqual(structure["live_evidence_roots"], 1)
        self.assertIn("vulnerable_control", structure)
        self.assertIn("reference_control", structure)

    def test_evidence_blind_fails_powered_test_and_guard(self):
        report = proofpath.evaluate(self.case, "evidence_blind")
        retraction = self.result_by_id(report, "M2_retract_origin_restate")
        contradiction = self.result_by_id(report, "M3_independent_contradiction")
        self.assertTrue(retraction["powered"])
        self.assertEqual(retraction["status"], "FAIL")
        self.assertTrue(contradiction["powered"])
        self.assertEqual(contradiction["status"], "FAIL")

    def test_report_and_ci_gate_are_separate(self):
        bad = proofpath.evaluate(self.case, "repetition_counter")
        blind = proofpath.evaluate(self.case, "evidence_blind")
        good = proofpath.evaluate(self.case, "lineage_aware")
        self.assertFalse(bad["summary"]["ci_gate_pass"])
        self.assertFalse(blind["summary"]["ci_gate_pass"])
        self.assertTrue(good["summary"]["ci_gate_pass"])

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

    def test_action_order_is_case_specific_and_required(self):
        bad = json.loads(json.dumps(self.case))
        bad.pop("action_order")
        with self.assertRaises(ValueError):
            proofpath.validate_case(bad)

    def test_html_preserves_claim_ceiling_and_baseline(self):
        report = proofpath.evaluate(self.case, "repetition_counter")
        output = proofpath.render_html(report)
        self.assertIn("not a model result", output)
        self.assertIn("Baseline first", output)
        self.assertIn("2 visible sources / 1 live evidence root", output)
        self.assertIn("M1_duplicate_support", output)
        self.assertIn("FAIL", output)


if __name__ == "__main__":
    unittest.main()
