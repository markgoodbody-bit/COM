import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("missing_edge", ROOT / "missing_edge.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class MissingEdgeTests(unittest.TestCase):
    def cases(self):
        return json.loads((ROOT / "fixtures" / "synthetic_cases.json").read_text(encoding="utf-8"))

    def test_manifest_has_two_task_arms_all_conditions_and_stable_counts(self):
        manifest = mod.build_manifest(self.cases(), runs=3, seed=7)
        self.assertEqual(set(manifest["conditions"]), set(mod.CONDITIONS))
        self.assertEqual(set(manifest["task_modes"]), set(mod.TASK_MODES))
        self.assertEqual(len(manifest["requests"]), 6 * 2 * 6 * 3)

    def test_system_prompt_does_not_teach_source_count_lesson(self):
        lower = mod.SYSTEM_TEXT.lower()
        self.assertNotIn("multiple report", lower)
        self.assertNotIn("independent evidentiary roots", lower)
        self.assertNotIn("unknown", lower)

    def test_assessment_arm_has_no_decision_policy(self):
        case = self.cases()["cases"][0]
        payload = mod.build_payload(case, "missing_edge_graph", "relationship_assessment")
        self.assertNotIn("decision_policy", payload)
        self.assertNotIn("decision", payload["response_schema"])
        self.assertIn("what is established", payload["task"].lower())

    def test_decision_arm_keeps_case_policy(self):
        case = self.cases()["cases"][0]
        payload = mod.build_payload(case, "missing_edge_graph", "decision")
        self.assertEqual(payload["decision_policy"], case["decision"])
        self.assertIn("decision", payload["response_schema"])

    def test_same_case_reports_are_frozen_across_conditions_within_each_arm(self):
        case = self.cases()["cases"][0]
        for task_mode in mod.TASK_MODES:
            payloads = [mod.build_payload(case, c, task_mode) for c in mod.CONDITIONS]
            reports = [p["reports"] for p in payloads]
            self.assertTrue(all(r == reports[0] for r in reports[1:]))
            self.assertTrue(all(p["claim"] == payloads[0]["claim"] for p in payloads[1:]))

    def test_missing_edge_does_not_encode_independence_or_completeness(self):
        case = self.cases()["cases"][0]
        payload = mod.build_payload(case, "missing_edge_graph", "relationship_assessment")
        self.assertEqual(payload["provenance"]["relations"], [])
        self.assertNotIn("relationship_coverage", payload["provenance"])
        self.assertNotIn("pairwise_relationship", payload["provenance"])

    def test_open_world_scope_has_no_unknown_token(self):
        case = self.cases()["cases"][0]
        payload = mod.build_payload(case, "open_world_scope", "relationship_assessment")
        serialized = json.dumps(payload["provenance"], sort_keys=True).lower()
        self.assertNotIn("unknown", serialized)
        self.assertEqual(payload["provenance"]["relations"], [])
        self.assertEqual(payload["provenance"]["relationship_coverage"], "partial")
        self.assertEqual(payload["provenance"]["absence_semantics"], "unasserted")

    def test_explicit_unknown_is_distinct_from_verified_independent(self):
        case = self.cases()["cases"][0]
        unknown = mod.build_payload(case, "explicit_unknown", "relationship_assessment")
        independent = mod.build_payload(case, "verified_independent", "relationship_assessment")
        self.assertEqual(unknown["provenance"]["pairwise_relationship"]["status"], "unknown")
        self.assertEqual(independent["provenance"]["pairwise_relationship"]["status"], "independence_established")

    def assessment_response(self, relation, roots, confidence=0.8):
        return {
            "relationship_assessment": relation,
            "independently_established_roots": roots,
            "confidence": confidence,
            "reason": "bounded test response",
        }

    def decision_response(self, relation, roots, decision, confidence=0.8):
        return {**self.assessment_response(relation, roots, confidence), "decision": decision}

    def test_diagnostic_false_independence_on_missing_edge_is_caught(self):
        scored = mod.score_one(
            "relationship_assessment",
            "missing_edge_graph",
            self.assessment_response("independent_established", 2),
        )
        self.assertTrue(scored["false_independence"])
        self.assertFalse(scored["false_proceed"])
        self.assertIsNone(scored["decision_exact"])

    def test_decision_false_proceed_on_missing_edge_is_caught(self):
        scored = mod.score_one(
            "decision",
            "missing_edge_graph",
            self.decision_response("independent_established", 2, "proceed"),
        )
        self.assertTrue(scored["false_independence"])
        self.assertTrue(scored["false_proceed"])

    def test_hold_everything_fails_verified_independence_in_both_arms(self):
        diagnostic = mod.score_one(
            "relationship_assessment", "verified_independent", self.assessment_response("unknown", 0)
        )
        decision = mod.score_one(
            "decision", "verified_independent", self.decision_response("unknown", 0, "hold")
        )
        self.assertTrue(diagnostic["verified_independence_missed"])
        self.assertTrue(decision["verified_independence_missed"])
        self.assertFalse(decision["decision_exact"])

    def test_correct_verified_independence_passes_both_arms(self):
        diagnostic = mod.score_one(
            "relationship_assessment",
            "verified_independent",
            self.assessment_response("independent_established", 2),
        )
        decision = mod.score_one(
            "decision",
            "verified_independent",
            self.decision_response("independent_established", 2, "proceed"),
        )
        self.assertFalse(diagnostic["verified_independence_missed"])
        self.assertFalse(decision["verified_independence_missed"])
        self.assertTrue(decision["decision_exact"])

    def test_aggregate_separates_diagnostic_and_consequence_deltas(self):
        rows = [
            mod.score_one(
                "relationship_assessment", "missing_edge_graph", self.assessment_response("independent_established", 2)
            ),
            mod.score_one(
                "relationship_assessment", "open_world_scope", self.assessment_response("unknown", 0)
            ),
            mod.score_one(
                "relationship_assessment", "explicit_unknown", self.assessment_response("unknown", 0)
            ),
            mod.score_one(
                "decision", "missing_edge_graph", self.decision_response("independent_established", 2, "proceed")
            ),
            mod.score_one(
                "decision", "open_world_scope", self.decision_response("unknown", 0, "hold")
            ),
            mod.score_one(
                "decision", "explicit_unknown", self.decision_response("unknown", 0, "hold")
            ),
            mod.score_one(
                "decision", "verified_independent", self.decision_response("independent_established", 2, "proceed")
            ),
        ]
        report = mod.aggregate(rows)
        self.assertEqual(report["diagnostic_primary_delta_open_world_scope"], 1.0)
        self.assertEqual(report["diagnostic_secondary_delta_explicit_unknown"], 1.0)
        self.assertEqual(report["decision_primary_delta_open_world_scope"], 1.0)
        self.assertEqual(report["decision_secondary_delta_explicit_unknown"], 1.0)
        self.assertIn("HOLD_EVERYTHING", report["bidirectional_guard"])

    def test_response_schema_rejects_invalid_root_count(self):
        with self.assertRaises(ValueError):
            mod.validate_response(self.assessment_response("unknown", 3), "relationship_assessment")

    def test_assessment_response_refuses_decision_field(self):
        with self.assertRaises(ValueError):
            mod.validate_response(self.decision_response("unknown", 0, "hold"), "relationship_assessment")


if __name__ == "__main__":
    unittest.main()
