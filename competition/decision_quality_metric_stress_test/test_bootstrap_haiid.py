import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("bootstrap_haiid", HERE / "bootstrap_haiid.py")
boot = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = boot
SPEC.loader.exec_module(boot)


class BootstrapSanityTests(unittest.TestCase):
    def test_frozen_bootstrap_contract(self):
        self.assertEqual(boot.DEFAULT_REPLICATES, 2000)
        self.assertEqual(boot.DEFAULT_SEED, 20260917)
        self.assertEqual(boot.ALPHA, 0.05)
        self.assertEqual(
            boot.probe.QUALITY_DIRECTIONS,
            {
                "final_accuracy": "higher",
                "team_gain": "higher",
                "correct_confidence": "higher",
                "beneficial_correction_rate": "higher",
                "harmful_override_rate": "lower",
            },
        )

    def test_oriented_lower_is_better(self):
        self.assertEqual(boot.oriented("final_accuracy", 0.8), 0.8)
        self.assertEqual(boot.oriented("harmful_override_rate", 0.2), -0.2)
        self.assertIsNone(boot.oriented("harmful_override_rate", None))

    def test_quantile_linear_interpolation(self):
        xs = [0.0, 1.0, 2.0, 3.0, 4.0]
        self.assertEqual(boot.quantile(xs, 0.0), 0.0)
        self.assertEqual(boot.quantile(xs, 0.5), 2.0)
        self.assertEqual(boot.quantile(xs, 1.0), 4.0)
        self.assertAlmostEqual(boot.quantile([0.0, 10.0], 0.25), 2.5)

    def test_cluster_aggregation_preserves_eligible_denominators(self):
        rows = [
            # p1: beneficial correction
            {
                "task_name": "art", "advice_source": "ai", "perceived_accuracy": "80",
                "participant_id": "p1", "response_1": "-0.4", "response_2": "0.6", "advice": "0.8",
            },
            # p1: harmful override
            {
                "task_name": "art", "advice_source": "ai", "perceived_accuracy": "80",
                "participant_id": "p1", "response_1": "0.5", "response_2": "-0.3", "advice": "-0.9",
            },
            # p2: stays correct with correct advice
            {
                "task_name": "art", "advice_source": "ai", "perceived_accuracy": "80",
                "participant_id": "p2", "response_1": "0.4", "response_2": "0.5", "advice": "0.8",
            },
        ]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "tiny.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            clusters, meta = boot.load_clusters(path)
        cs = clusters["art"]["ai@80"]
        self.assertEqual(len(cs), 2)
        combined = boot.combine(cs)
        self.assertEqual(combined["n"], 3)
        self.assertEqual(combined["beneficial_eligible"], 1)
        self.assertEqual(combined["beneficial_corrected"], 1)
        self.assertEqual(combined["harmful_eligible"], 1)
        self.assertEqual(combined["harmful_overridden"], 1)
        metrics = boot.metrics_from_cluster(combined)
        self.assertAlmostEqual(metrics["beneficial_correction_rate"], 1.0)
        self.assertAlmostEqual(metrics["harmful_override_rate"], 1.0)
        self.assertEqual(meta["missing_participant_rows"], 0)

    def test_missing_participant_is_not_silently_trial_bootstrapped(self):
        row = {
            "task_name": "art", "advice_source": "human", "perceived_accuracy": "80",
            "participant_id": "", "response_1": "0.5", "response_2": "0.6", "advice": "0.8",
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "tiny.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(row))
                writer.writeheader()
                writer.writerow(row)
            clusters, meta = boot.load_clusters(path)
        self.assertEqual(meta["used_rows"], 0)
        self.assertEqual(meta["missing_participant_rows"], 1)
        self.assertEqual(clusters, {})


if __name__ == "__main__":
    unittest.main()
