import importlib.util
import json
import tempfile
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
        overlaps = report["claims"][0]["shared_ancestry"]
        pairs = {(x["source_a"], x["source_b"]): set(x["shared_ancestry"]) for x in overlaps}
        self.assertIn("s1", pairs[("s1", "s2")])
        self.assertIn("s1", pairs[("s1", "s3")])
        self.assertIn("s1", pairs[("s2", "s3")])

    def test_unresolved_is_preserved(self):
        bundle = self.load_fixture("partial_lineage.json")
        report = mod.build_report(bundle)
        states = {c["id"]: c["evidence_state"] for c in report["claims"]}
        self.assertEqual(states["c1"], "unresolved")
        self.assertEqual(states["c2"], "source_stated")

    def test_independent_relation_does_not_create_ancestry(self):
        bundle = self.load_fixture("adversarial_independence.json")
        report = mod.build_report(bundle)
        source = {s["id"]: s for s in report["sources"]}
        self.assertEqual(source["s4"]["ancestors"], [])
        overlaps = report["claims"][0]["shared_ancestry"]
        pairs = {(x["source_a"], x["source_b"]) for x in overlaps}
        self.assertIn(("s2", "s3"), pairs)
        self.assertNotIn(("s1", "s4"), pairs)

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

    def test_ancestry_cycle_is_detected(self):
        bundle = self.load_fixture("derivative_repeat.json")
        bundle["relations"].append({"type": "derived_from", "from": "s1", "to": "s3"})
        _, cycles = mod.ancestry_map(bundle)
        self.assertTrue(cycles)

    def test_markdown_keeps_ceiling(self):
        bundle = self.load_fixture("adversarial_independence.json")
        report = mod.build_report(bundle)
        text = mod.render_markdown(report)
        self.assertIn("REPETITION != CORROBORATION", text)
        self.assertIn("UNKNOWN != ABSENT", text)


if __name__ == "__main__":
    unittest.main()
