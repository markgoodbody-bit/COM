import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("evidence_lineage", ROOT / "evidence_lineage.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class EvidenceLineageTests(unittest.TestCase):
    def load_fixture(self, name):
        return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))

    def test_derivative_repetition_exposes_shared_ancestry(self):
        bundle = self.load_fixture("derivative_repeat.json")
        self.assertEqual(mod.validate(bundle), [])
        report = mod.build_report(bundle)
        pairs = {
            (x["source_a"], x["source_b"]): (x["state"], set(x["shared_ancestry"]))
            for x in report["claims"][0]["source_pair_lineage"]
        }
        self.assertEqual(pairs[("s1", "s2")][0], "shared")
        self.assertIn("s1", pairs[("s1", "s2")][1])
        self.assertIn("s1", pairs[("s1", "s3")][1])
        self.assertIn("s1", pairs[("s2", "s3")][1])

    def test_unknown_lineage_does_not_become_independence(self):
        bundle = self.load_fixture("unknown_lineage.json")
        self.assertEqual(mod.validate(bundle), [])
        report = mod.build_report(bundle)
        pair = report["claims"][0]["source_pair_lineage"][0]
        self.assertEqual(pair["state"], "unknown")
        self.assertEqual(pair["shared_ancestry"], [])

    def test_declared_independence_is_not_proven_independence(self):
        bundle = self.load_fixture("adversarial_independence.json")
        report = mod.build_report(bundle)
        pairs = {
            (x["source_a"], x["source_b"]): x["state"]
            for x in report["claims"][0]["source_pair_lineage"]
        }
        self.assertEqual(pairs[("s1", "s4")], "declared_independent")
        self.assertIn("DECLARED_INDEPENDENT != PROVEN_INDEPENDENT", report["ceilings"])

    def test_claim_scoped_derivation_does_not_leak_to_other_claim(self):
        bundle = self.load_fixture("derivative_repeat.json")
        bundle["claims"].append({
            "id": "c2",
            "text": "A separate observation by s2 and s3.",
            "evidence_state": "source_stated",
            "source_ids": ["s2", "s3"],
        })
        self.assertEqual(mod.validate(bundle), [])
        report = mod.build_report(bundle)
        c2 = next(c for c in report["claims"] if c["id"] == "c2")
        pair = c2["source_pair_lineage"][0]
        self.assertNotEqual(pair["state"], "shared")

    def test_unresolved_is_preserved(self):
        bundle = self.load_fixture("partial_lineage.json")
        report = mod.build_report(bundle)
        states = {c["id"]: c["evidence_state"] for c in report["claims"]}
        self.assertEqual(states["c1"], "unresolved")
        self.assertEqual(states["c2"], "source_stated")

    def test_observed_without_source_fails(self):
        bundle = self.load_fixture("unknown_lineage.json")
        bundle["claims"][0]["evidence_state"] = "observed"
        bundle["claims"][0]["source_ids"] = []
        errors = mod.validate(bundle)
        self.assertTrue(any("requires at least one source" in e for e in errors))

    def test_missing_source_reference_fails(self):
        bundle = self.load_fixture("derivative_repeat.json")
        bundle["claims"][0]["source_ids"].append("missing")
        errors = mod.validate(bundle)
        self.assertTrue(any("unknown source_id" in e for e in errors))

    def test_duplicate_source_id_fails(self):
        bundle = self.load_fixture("derivative_repeat.json")
        bundle["sources"].append(dict(bundle["sources"][0]))
        errors = mod.validate(bundle)
        self.assertTrue(any("duplicate source id" in e for e in errors))

    def test_duplicate_relation_fails(self):
        bundle = self.load_fixture("derivative_repeat.json")
        bundle["relations"].append(dict(bundle["relations"][0]))
        errors = mod.validate(bundle)
        self.assertTrue(any("duplicate relation" in e for e in errors))

    def test_contradictory_independence_and_ancestry_fails(self):
        bundle = self.load_fixture("derivative_repeat.json")
        bundle["relations"].append({"type": "independent_of", "from": "s2", "to": "s1", "claim_id": "c1"})
        errors = mod.validate(bundle)
        self.assertTrue(any("contradictory ancestry/independence" in e for e in errors))

    def test_claim_scoped_ancestry_cycle_is_detected(self):
        bundle = self.load_fixture("derivative_repeat.json")
        bundle["relations"].append({"type": "derived_from", "from": "s1", "to": "s3", "claim_id": "c1"})
        _, cycles = mod.ancestry_map(bundle, "c1")
        self.assertTrue(cycles)

    def test_markdown_labels_input_and_unchecked_locator(self):
        bundle = self.load_fixture("adversarial_independence.json")
        report = mod.build_report(bundle)
        text = mod.render_markdown(report)
        self.assertIn("Input note (not independently checked)", text)
        self.assertIn("Supplied locator (not checked)", text)
        self.assertIn("MISSING_LINEAGE != INDEPENDENCE", text)
        self.assertIn("UNKNOWN != ABSENT", text)


if __name__ == "__main__":
    unittest.main()
