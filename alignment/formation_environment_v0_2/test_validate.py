"""Deterministic stdlib-only checks for Formation Environment v0.2 candidate."""
import copy
import unittest
from pathlib import Path

from validate import read, schema_contract, validate

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE / "examples"
SCHEMA = HERE / "episode.schema.json"


class CandidateChecks(unittest.TestCase):
    def load(self, name):
        return read(EXAMPLES / name)

    def test_all_constructed_examples_are_structurally_valid(self):
        for path in sorted(EXAMPLES.glob("*.json")):
            with self.subTest(path=path.name):
                self.assertEqual(validate(read(path)), [], path.name)

    def test_unknown_clock_cannot_smuggle_time(self):
        record = self.load("06-clock-unknown.json")
        record["clocks"]["routing"]["bound"]["time_value"] = "10 minutes"
        self.assertTrue(any("unknown must not invent" in e for e in validate(record)))

    def test_non_unknown_bound_needs_evidence(self):
        record = self.load("02-wrong-premise.json")
        record["clocks"]["correction"]["bound"]["basis_evidence"] = []
        self.assertTrue(any("non-unknown bound needs referenced basis evidence" in e for e in validate(record)))

    def test_definite_window_needs_evidence(self):
        record = self.load("05-route-exists-window-closed.json")
        record["clocks"]["window"]["basis_evidence"] = []
        self.assertTrue(any("definite assessment needs referenced evidence" in e for e in validate(record)))

    def test_unknown_window_may_remain_evidence_incomplete(self):
        record = self.load("06-clock-unknown.json")
        record["clocks"]["window"]["assessment_as_of"] = {
            "kind":"unknown", "time_value":"", "event":"", "basis":"Currentness unavailable.",
            "notes":"Unknown window may retain an unknown as-of anchor.", "basis_evidence":[]
        }
        self.assertEqual(record["clocks"]["window"]["assessment"], "unknown")
        self.assertEqual(record["clocks"]["window"]["basis_evidence"], [])
        self.assertEqual(record["clocks"]["window"]["assessment_as_of"]["kind"], "unknown")
        self.assertEqual(validate(record), [])

    def test_definite_window_needs_non_unknown_as_of_anchor(self):
        record = self.load("02-wrong-premise.json")
        record["clocks"]["window"]["assessment_as_of"] = {
            "kind":"unknown", "time_value":"", "event":"", "basis":"Currentness unavailable.",
            "notes":"Unknown is not a definite as-of anchor.", "basis_evidence":[]
        }
        self.assertTrue(any("needs a non-unknown assessment_as_of anchor" in e for e in validate(record)))

    def test_window_evidence_reference_must_exist(self):
        record = self.load("02-wrong-premise.json")
        record["clocks"]["window"]["basis_evidence"] = ["does-not-exist"]
        self.assertTrue(any("missing evidence" in e for e in validate(record)))

    def test_definite_window_cannot_rest_only_on_unknown_evidence(self):
        record = self.load("02-wrong-premise.json")
        record["evidence"][0]["kind"] = "unknown"
        record["evidence"][3]["kind"] = "unknown"
        self.assertTrue(any("cannot rest only on evidence marked unknown" in e for e in validate(record)))

    def test_occurred_hardening_requires_closed_window_for_same_remedy(self):
        record = self.load("05-route-exists-window-closed.json")
        for assessment in ("open", "unknown"):
            with self.subTest(assessment=assessment):
                changed = copy.deepcopy(record)
                changed["clocks"]["window"]["assessment"] = assessment
                self.assertTrue(any("occurred hardening requires a closed window" in e for e in validate(changed)))
        self.assertEqual(validate(record), [])

    def test_open_window_may_coexist_with_unusable_route(self):
        record = self.load("09-window-open-route-unusable.json")
        self.assertEqual(record["clocks"]["window"]["assessment"], "open")
        self.assertEqual(record["clocks"]["routing"]["usability"]["assessment"], "unusable")
        self.assertEqual(validate(record), [])

    def test_act_scope_still_requires_recorded_grant(self):
        record = self.load("03-delay-also-burdens.json")
        record["action"]["scope"] = "indefinite retention"
        self.assertTrue(any("ACT scope not in recorded grant" in e for e in validate(record)))

    def test_standing_self_resolution_is_a_documented_ceiling_not_a_guard(self):
        record = self.load("08-standing-self-resolved.json")
        standing = next(x for x in record["uncertainties"] if x["id"] == "u1")
        self.assertEqual(standing["status"], "resolved")
        self.assertEqual(standing["owner"], "the participant")
        self.assertEqual(standing["resolution_evidence"], ["e2"])
        self.assertEqual(validate(record), [])

    def test_evidence_history_cannot_be_rewritten(self):
        previous = self.load("02-wrong-premise.json")
        current = copy.deepcopy(previous)
        current["evidence"][0]["claim"] = "rewritten"
        self.assertTrue(any("earlier evidence rewritten" in e for e in validate(current, previous)))

    def test_wider_grant_ignores_whitespace_as_basis_change(self):
        previous = self.load("04-success-not-authority.json")
        current = copy.deepcopy(previous)
        current["authority"]["granted_scopes"].append("production account settings")
        current["authority"]["basis"] += " "
        errors = validate(current, previous)
        self.assertTrue(any("whitespace or prior success" in e for e in errors))
        self.assertTrue(any("newly represented non-unknown evidence" in e for e in errors))

    def test_wider_grant_cannot_use_only_unknown_new_evidence(self):
        previous = self.load("04-success-not-authority.json")
        current = copy.deepcopy(previous)
        current["evidence"].append({"id":"e9","kind":"unknown","claim":"A claimed new basis.","source":"constructed unknown evidence"})
        current["authority"]["basis"] = "Materially changed basis is represented."
        current["authority"]["basis_evidence"] = ["e9"]
        current["authority"]["granted_scopes"].append("production account settings")
        self.assertTrue(any("newly represented non-unknown evidence" in e for e in validate(current, previous)))

    def test_wider_grant_can_record_new_traceability_without_becoming_authority_proof(self):
        previous = self.load("04-success-not-authority.json")
        current = copy.deepcopy(previous)
        current["evidence"].append({"id":"e4","kind":"scenario","claim":"A new scoped grant is represented.","source":"constructed new grant"})
        current["authority"]["basis"] = "New scoped production grant is represented; validator checks traceability only."
        current["authority"]["basis_evidence"] = ["e4"]
        current["authority"]["granted_scopes"].append("production account settings")
        self.assertEqual(validate(current, previous), [])

    def test_repaired_residue_requires_evidence(self):
        record = self.load("03-delay-also-burdens.json")
        record["residue"][0]["status"] = "repaired"
        self.assertTrue(any("repaired residue requires referenced evidence" in e for e in validate(record)))

    def test_repaired_residue_cannot_use_only_unknown_evidence(self):
        record = self.load("03-delay-also-burdens.json")
        record["evidence"].append({"id":"e9","kind":"unknown","claim":"Repair may have happened.","source":"constructed unknown evidence"})
        record["residue"][0]["status"] = "repaired"
        record["residue"][0]["repair_evidence"] = ["e9"]
        self.assertTrue(any("cannot rest only on evidence marked unknown" in e for e in validate(record)))

    def test_schema_contract_rejects_unknown_assertion_keyword(self):
        schema = read(SCHEMA)
        schema["properties"]["situation"]["pattern"] = ".+"
        self.assertTrue(any("unsupported schema keyword" in e for e in schema_contract(schema, schema)))

    def test_schema_contract_rejects_ref_assertion_siblings(self):
        schema = read(SCHEMA)
        schema["properties"]["authority"]["minLength"] = 1
        self.assertTrue(any("siblings beside $ref" in e for e in schema_contract(schema, schema)))

    def test_schema_contract_rejects_external_and_unresolved_refs(self):
        for ref in ("https://example.com/schema.json", "#/$defs/does-not-exist", "#/$defs/evidence/extra"):
            schema = read(SCHEMA)
            schema["properties"]["authority"]["$ref"] = ref
            errors = schema_contract(schema, schema)
            self.assertTrue(any("references are supported" in e or "unresolved local reference" in e for e in errors), ref)


if __name__ == "__main__":
    unittest.main()
