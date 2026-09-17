import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("atrs_exploratory", ROOT / "exploratory_semantic_census.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)

EXPECTED_COUNTS = {
    "AMBIGUOUS": 4,
    "DATA_RIGHTS": 2,
    "EXPLANATION_ONLY": 2,
    "HELP_FEEDBACK": 40,
    "INTERNAL_REVIEW": 28,
    "IN_CHANNEL_HANDOFF": 9,
    "NO_SEPARATE": 67,
    "PROCESS_REFERENCE": 42,
    "PUBLIC_INITIATION": 33,
    "REFUSAL_OR_OPT_OUT": 2,
    "SELF_CORRECTION": 7,
}


class ExploratoryCodingStructureTests(unittest.TestCase):
    def test_label_schema_is_exact(self):
        self.assertEqual(set(mod.LABELS), set(EXPECTED_COUNTS))

    def test_all_151_indices_are_covered(self):
        covered = set()
        for label, indices in mod.LABEL_INDICES.items():
            self.assertEqual(len(indices), len(set(indices)), label)
            self.assertTrue(all(0 <= i < mod.EXPECTED_APPEALS for i in indices))
            covered.update(indices)
        self.assertEqual(covered, set(range(mod.EXPECTED_APPEALS)))

    def test_label_counts_are_frozen(self):
        actual = {label: len(indices) for label, indices in mod.LABEL_INDICES.items()}
        self.assertEqual(actual, EXPECTED_COUNTS)

    def test_status_and_ceilings_preserve_exploratory_boundary(self):
        self.assertIn("EXPLORATORY", " ".join(mod.CEILINGS))
        self.assertIn("FRAMEWORK_LABEL != VALIDATED_CLASSIFICATION", mod.CEILINGS)
        self.assertIn("LABELS_MAY_CO_OCCUR", mod.CEILINGS)


if __name__ == "__main__":
    unittest.main()
