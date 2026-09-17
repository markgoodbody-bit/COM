import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("lineage_envelope", ROOT / "lineage_envelope.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class LineageEnvelopeTests(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / "fixtures" / "source_laundering.json").read_text(encoding="utf-8"))

    def test_base_has_one_visible_source_and_one_root(self):
        out = mod.build_envelope(self.fixture()["base"])
        self.assertEqual(out["summary"]["visible_supporting_sources"], 1)
        self.assertEqual(out["summary"]["distinct_supporting_evidence_roots"], 1)

    def test_mutant_has_two_urls_but_one_root(self):
        f = self.fixture()
        world = json.loads(json.dumps(f["base"]))
        m = f["mutants"][0]
        world["sources"].append(m["add_source"])
        world["relations"].append(m["add_relation"])
        out = mod.build_envelope(world)
        self.assertEqual(out["summary"]["visible_supporting_sources"], 2)
        self.assertEqual(out["summary"]["distinct_supporting_evidence_roots"], 1)
        derived = next(r for r in out["sources"] if r["source_id"] == "derivative-a")
        self.assertTrue(derived["is_derived_on_supplied_graph"])
        self.assertEqual(derived["evidence_root"], "origin-a")

    def test_unknown_relation_refuses(self):
        world = {"sources": [{"id": "a", "stance": "support"}], "relations": [{"type": "copies", "from": "b", "to": "a"}]}
        with self.assertRaises(ValueError):
            mod.build_envelope(world)

    def test_cycle_refuses(self):
        world = {
            "sources": [{"id": "a"}, {"id": "b"}],
            "relations": [
                {"type": "copies", "from": "a", "to": "b"},
                {"type": "copies", "from": "b", "to": "a"},
            ],
        }
        with self.assertRaises(ValueError):
            mod.build_envelope(world)


if __name__ == "__main__":
    unittest.main()
