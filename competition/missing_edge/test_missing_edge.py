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

    def test_manifest_has_all_conditions_and_stable_counts(self):
        manifest = mod.build_manifest(self.cases(), runs=3, seed=7)
        self.assertEqual(set(manifest["conditions"]), set(mod.CONDITIONS))
        self.assertEqual(len(manifest["requests"]), 6 * 6 * 3)

    def test_system_prompt_does_not_teach_source_count_lesson(self):
        self.assertNotIn("multiple report", mod.SYSTEM_TEXT.lower())
        self.assertNotIn("independent evidentiary roots", mod.SYSTEM_TEXT.lower())

    def test_same_case_report_text_is_frozen_across_conditions(self):
        data = self.cases()
        case = data["cases"][0]
        payloads = [mod.build_payload(case, c) for c in mod.CONDITIONS]
        reports = [p["reports"] for p in payloads]
        self.assertTrue(all(r == reports[0] for r in reports[1:]))
        self.assertTrue(all(p["claim"] == payloads[0]["claim"] for p in payloads[1:]))
        self.assertTrue(all(p["decision_policy"] == payloads[0]["decision_policy"] for p in payloads[1:]))

    def test_missing_edge_does_not_encode_independence_or_completeness(self):
        case = self.cases()["cases"][0]
        payload = mod.build_payload(case, "missing_edge_graph")
        self.assertEqual(payload["provenance"]["relations"], [])
        self.assertNotIn("relationship_coverage", payload["provenance"])
        self.assertNotIn("pairwise_relationship", payload["provenance"])

    def test_open_world_scope_has_no_unknown_token(self):
        case = self.cases()["cases"][0]
        payload = mod.build_payload(case, "open_world_scope")
        serialized = json.dumps(payload["provenance"], sort_keys=True).lower()
        self.assertNotIn("unknown", serialized)
        self.assertEqual(payload["provenance"]["relations"], [])
        self.assertEqual(payload["provenance"]["relationship_coverage"], "partial")
        self.assertEqual(payload["provenance"]["absence_semantics"], "unasserted")

    def test_explicit_unknown_is_distinct_from_verified_independent(self):
        case = self.cases()["cases"][0]
        unknown = mod.build_payload(case, "explicit_unknown")
        independent = mod.build_payload(case, "verified_independent")
        self.assertEqual(unknown["provenance"]["pairwise_relationship"]["status"], "unknown")
        self.assertEqual(independent["provenance"]["pairwise_relationship"]["status"], "independence_established")

    def response(self, relation, roots, decision, confidence=0.8):
        return {
            "relationship_assessment": relation,
            "independently_established_roots": roots,
            "decision": decision,
            "confidence": confidence,
            "reason": "bounded test response",
        }

    def test_false_independence_on_missing_edge_is_caught(self):
        scored = mod.score_one("missing_edge_graph", self.response("independent_established", 2, "proceed"))
        self.assertTrue(scored["false_independence"])
        self.assertTrue(scored["false_proceed"])

    def test_false_independence_on_open_world_scope_is_caught(self):
        scored = mod.score_one("open_world_scope", self.response("independent_established", 2, "proceed"))
        self.assertTrue(scored["false_independence"])
        self.assertTrue(scored["false_proceed"])

    def test_hold_everything_fails_verified_independence_direction(self):
        scored = mod.score_one("verified_independent", self.response("unknown", 0, "hold"))
        self.assertTrue(scored["verified_independence_missed"])
        self.assertFalse(scored["decision_exact"])

    def test_correct_verified_independence_passes(self):
        scored = mod.score_one("verified_independent", self.response("independent_established", 2, "proceed"))
        self.assertFalse(scored["verified_independence_missed"])
        self.assertTrue(scored["relation_exact"])
        self.assertTrue(scored["root_count_exact"])
        self.assertTrue(scored["decision_exact"])

    def test_aggregate_reports_two_intervention_deltas(self):
        rows = [
            mod.score_one("missing_edge_graph", self.response("independent_established", 2, "proceed")),
            mod.score_one("open_world_scope", self.response("unknown", 0, "hold")),
            mod.score_one("explicit_unknown", self.response("unknown", 0, "hold")),
            mod.score_one("verified_independent", self.response("independent_established", 2, "proceed")),
        ]
        report = mod.aggregate(rows)
        self.assertEqual(report["primary_intervention_delta_open_world_scope"], 1.0)
        self.assertEqual(report["secondary_intervention_delta_explicit_unknown"], 1.0)
        self.assertIn("HOLD_EVERYTHING", report["bidirectional_guard"])

    def test_response_schema_rejects_invalid_root_count(self):
        with self.assertRaises(ValueError):
            mod.validate_response(self.response("unknown", 3, "hold"))


if __name__ == "__main__":
    unittest.main()
