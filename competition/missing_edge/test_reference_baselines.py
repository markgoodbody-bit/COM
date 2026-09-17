import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

MSPEC = importlib.util.spec_from_file_location("missing_edge", ROOT / "missing_edge.py")
me = importlib.util.module_from_spec(MSPEC)
assert MSPEC.loader is not None
MSPEC.loader.exec_module(me)

BSPEC = importlib.util.spec_from_file_location("reference_baselines", ROOT / "reference_baselines.py")
baselines = importlib.util.module_from_spec(BSPEC)
assert BSPEC.loader is not None
BSPEC.loader.exec_module(baselines)


class ReferenceBaselineTests(unittest.TestCase):
    def case(self):
        data = json.loads((ROOT / "fixtures" / "synthetic_cases.json").read_text(encoding="utf-8"))
        return data["cases"][0]

    def score_solver(self, solver, task_mode, condition):
        payload = me.build_payload(self.case(), condition, task_mode)
        return me.score_one(task_mode, condition, solver(payload))

    def test_open_world_solver_passes_every_condition_in_both_arms(self):
        for task_mode in me.TASK_MODES:
            for condition in me.CONDITIONS:
                with self.subTest(task_mode=task_mode, condition=condition):
                    row = self.score_solver(baselines.open_world_solver, task_mode, condition)
                    self.assertTrue(row["relation_exact"])
                    self.assertTrue(row["root_count_exact"])
                    self.assertFalse(row["false_independence"])
                    self.assertFalse(row["verified_independence_missed"])
                    if task_mode == "decision":
                        self.assertTrue(row["decision_exact"])
                        self.assertFalse(row["false_proceed"])

    def test_closed_world_solver_fails_missing_edge_but_not_positive_controls(self):
        for task_mode in me.TASK_MODES:
            missing = self.score_solver(baselines.closed_world_solver, task_mode, "missing_edge_graph")
            self.assertTrue(missing["false_independence"])
            if task_mode == "decision":
                self.assertTrue(missing["false_proceed"])

            shared = self.score_solver(baselines.closed_world_solver, task_mode, "verified_shared")
            independent = self.score_solver(baselines.closed_world_solver, task_mode, "verified_independent")
            self.assertTrue(shared["relation_exact"])
            self.assertTrue(independent["relation_exact"])
            self.assertFalse(independent["verified_independence_missed"])

    def test_closed_world_solver_respects_explicit_unknown_but_not_scope_only(self):
        for task_mode in me.TASK_MODES:
            explicit = self.score_solver(baselines.closed_world_solver, task_mode, "explicit_unknown")
            scoped = self.score_solver(baselines.closed_world_solver, task_mode, "open_world_scope")
            self.assertFalse(explicit["false_independence"])
            self.assertTrue(scoped["false_independence"])


if __name__ == "__main__":
    unittest.main()
