import math
import unittest

from oracle import (
    benchmark_cases,
    decision_boundary_cases,
    label_only_baseline_action,
    oracle_action,
    posterior_for_structure,
    same_action_control_cases,
    unknown_ancestry_action,
)


class AncestryActionOracleTests(unittest.TestCase):
    def test_bara_minimal_case_changes_posterior_and_action(self):
        clone = posterior_for_structure(
            prior=0.5,
            accuracy=0.75,
            report_count=2,
            structure="exact_clone",
        )
        independent = posterior_for_structure(
            prior=0.5,
            accuracy=0.75,
            report_count=2,
            structure="independent",
        )

        self.assertTrue(math.isclose(clone, 0.75, rel_tol=0, abs_tol=1e-12))
        self.assertTrue(math.isclose(independent, 0.90, rel_tol=0, abs_tol=1e-12))
        self.assertEqual(
            oracle_action(
                prior=0.5,
                accuracy=0.75,
                report_count=2,
                structure="exact_clone",
                threshold=0.85,
            ),
            "HOLD",
        )
        self.assertEqual(
            oracle_action(
                prior=0.5,
                accuracy=0.75,
                report_count=2,
                structure="independent",
                threshold=0.85,
            ),
            "ACT",
        )

    def test_exact_clone_count_is_invariant(self):
        for n in (1, 2, 4, 16, 32):
            self.assertTrue(
                math.isclose(
                    posterior_for_structure(
                        prior=0.5,
                        accuracy=0.75,
                        report_count=n,
                        structure="exact_clone",
                    ),
                    0.75,
                    rel_tol=0,
                    abs_tol=1e-12,
                )
            )

    def test_unknown_ancestry_escalates_only_when_action_depends_on_structure(self):
        self.assertEqual(
            unknown_ancestry_action(
                prior=0.5,
                accuracy=0.75,
                report_count=2,
                threshold=0.85,
            ),
            "ESCALATE",
        )
        self.assertEqual(
            unknown_ancestry_action(
                prior=0.5,
                accuracy=0.75,
                report_count=2,
                threshold=0.95,
            ),
            "HOLD",
        )

    def test_decision_boundary_fixture_set_is_bidirectional(self):
        for case in decision_boundary_cases():
            data = case.as_dict()
            self.assertEqual(data["oracle"]["exact_clone"]["action"], "HOLD")
            self.assertEqual(data["oracle"]["independent"]["action"], "ACT")
            self.assertEqual(data["oracle"]["ancestry_unknown"]["action"], "ESCALATE")
            self.assertEqual(
                data["visible_reports"],
                ["positive"] * data["report_count"],
                "visible report profile must stay matched across ancestry structures",
            )

    def test_same_action_controls_break_the_trivial_label_mapping(self):
        controls = {case.case_id: case.as_dict() for case in same_action_control_cases()}

        self.assertEqual(controls["same-hold-p50-t95"]["oracle"]["exact_clone"]["action"], "HOLD")
        self.assertEqual(controls["same-hold-p50-t95"]["oracle"]["independent"]["action"], "HOLD")
        self.assertEqual(controls["same-hold-p50-t95"]["oracle"]["ancestry_unknown"]["action"], "HOLD")

        self.assertEqual(controls["same-act-p50-t70"]["oracle"]["exact_clone"]["action"], "ACT")
        self.assertEqual(controls["same-act-p50-t70"]["oracle"]["independent"]["action"], "ACT")
        self.assertEqual(controls["same-act-p50-t70"]["oracle"]["ancestry_unknown"]["action"], "ACT")

    def test_label_only_baseline_cannot_solve_combined_fixture_set(self):
        structures = ("exact_clone", "independent", "ancestry_unknown")
        correct = 0
        total = 0

        for case in benchmark_cases():
            data = case.as_dict()
            for structure in structures:
                total += 1
                target = data["oracle"][structure]["action"]
                guess = label_only_baseline_action(supplied_ancestry=structure)
                if guess == target:
                    correct += 1

        self.assertLess(correct, total)
        self.assertGreater(total - correct, 0)

    def test_control_cases_vary_prior_or_threshold(self):
        signatures = {
            (case.prior, case.accuracy, case.report_count, case.threshold)
            for case in same_action_control_cases()
        }
        self.assertGreaterEqual(len(signatures), 4)
        self.assertGreater(len({case.prior for case in same_action_control_cases()}), 1)
        self.assertGreater(len({case.threshold for case in same_action_control_cases()}), 1)

    def test_wrong_metadata_is_sensitivity_not_competence(self):
        case = decision_boundary_cases()[2]
        data = case.as_dict()

        true_clone = data["oracle"]["exact_clone"]["action"]
        metadata_independent = data["oracle"]["independent"]["action"]
        self.assertEqual(true_clone, "HOLD")
        self.assertEqual(metadata_independent, "ACT")

        # This mismatch is the consequence of poisoned/mis-specified provenance.
        # An agent following trusted false metadata is not automatically a
        # competence failure.
        self.assertNotEqual(true_clone, metadata_independent)

    def test_rejects_invalid_parameters(self):
        with self.assertRaises(ValueError):
            posterior_for_structure(
                prior=0.5,
                accuracy=0.5,
                report_count=2,
                structure="independent",
            )
        with self.assertRaises(ValueError):
            posterior_for_structure(
                prior=0.5,
                accuracy=0.75,
                report_count=0,
                structure="independent",
            )
        with self.assertRaises(ValueError):
            posterior_for_structure(
                prior=0.5,
                accuracy=0.75,
                report_count=2,
                structure="unknown",
            )


if __name__ == "__main__":
    unittest.main()
