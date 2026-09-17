import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("probe_haiid", HERE / "probe_haiid.py")
probe = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(probe)


class HAIIDProbeSanityTests(unittest.TestCase):
    def test_condition_key_accepts_only_released_treatments(self):
        expected = {
            (source, pa): f"{source}@{pa}"
            for source in ("human", "ai")
            for pa in (65, 80, 95)
        }
        for (source, pa), label in expected.items():
            self.assertEqual(
                probe.condition_key({"advice_source": source, "perceived_accuracy": str(pa)}),
                label,
            )
        for row in (
            {"advice_source": "other", "perceived_accuracy": "80"},
            {"advice_source": "ai", "perceived_accuracy": "70"},
            {"advice_source": "human", "perceived_accuracy": ""},
        ):
            self.assertIsNone(probe.condition_key(row))

    def test_lower_is_better_ranking_is_direction_aware(self):
        metrics = {
            "A": {"harmful_override_rate": 0.10, "final_accuracy": 0.80},
            "B": {"harmful_override_rate": 0.30, "final_accuracy": 0.90},
            "C": {"harmful_override_rate": 0.20, "final_accuracy": 0.70},
        }
        harm = probe.rank_conditions(metrics, "harmful_override_rate", "lower")
        acc = probe.rank_conditions(metrics, "final_accuracy", "higher")
        self.assertEqual([x[0] for x in harm], ["A", "C", "B"])
        self.assertEqual([x[0] for x in acc], ["B", "A", "C"])
        disagreement = probe.pairwise_disagreement(harm, acc)
        self.assertEqual(disagreement["comparable_pairs"], 3)
        self.assertEqual(disagreement["discordant_pairs"], 2)

    def test_feasibility_metrics_are_predeclared(self):
        self.assertEqual(
            probe.QUALITY_DIRECTIONS,
            {
                "final_accuracy": "higher",
                "team_gain": "higher",
                "correct_confidence": "higher",
                "beneficial_correction_rate": "higher",
                "harmful_override_rate": "lower",
            },
        )

    def test_tiny_dataset_keeps_quality_metrics_separate(self):
        rows = [
            {
                "task_name": "art",
                "advice_source": "ai",
                "perceived_accuracy": "80",
                "response_1": "-0.4",
                "response_2": "0.7",
                "advice": "0.9",
            },
            {
                "task_name": "art",
                "advice_source": "ai",
                "perceived_accuracy": "80",
                "response_1": "0.6",
                "response_2": "-0.2",
                "advice": "-0.8",
            },
            {
                "task_name": "art",
                "advice_source": "human",
                "perceived_accuracy": "80",
                "response_1": "0.6",
                "response_2": "0.7",
                "advice": "0.8",
            },
        ]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "tiny.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            result = probe.analyze(path)
        ai = result["scopes"]["art"]["conditions"]["ai@80"]
        self.assertEqual(ai["n"], 2)
        self.assertAlmostEqual(ai["final_accuracy"], 0.5)
        self.assertAlmostEqual(ai["team_gain"], 0.0)
        self.assertAlmostEqual(ai["beneficial_correction_rate"], 1.0)
        self.assertAlmostEqual(ai["harmful_override_rate"], 1.0)
        self.assertNotIn("appropriate_reliance", ai)
        self.assertNotIn("decision_quality_score", ai)


if __name__ == "__main__":
    unittest.main()
