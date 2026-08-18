#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("exchange_registry.py")


class ExchangeRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.registry = self.root / "artifacts.json"
        self.a = self.root / "a.txt"
        self.b = self.root / "b.txt"
        self.a.write_text("alpha", encoding="utf-8")
        self.b.write_text("beta", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--registry",
                str(self.registry),
                *args,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def register(self, artifact_id: str, file: Path) -> None:
        result = self.run_cli(
            "register", "--id", artifact_id, "--file", str(file), "--locator", file.name
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_measured_register_and_round_trip(self) -> None:
        self.register("A", self.a)
        result = self.run_cli(
            "verify-file", "--id", "A", "--file", str(self.a), "--update-round-trip"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        observation = json.loads(result.stdout)
        self.assertTrue(observation["match"])
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        record = registry["artifacts"]["A"]
        self.assertEqual(record["round_trip_verified"], "TRUE")
        self.assertEqual(len(record["round_trip_witnesses"]), 1)
        self.assertTrue(record["round_trip_witnesses"][0]["match"])

    def test_round_trip_failure_preserves_prior_witness(self) -> None:
        self.register("A", self.a)
        good = self.run_cli(
            "verify-file", "--id", "A", "--file", str(self.a), "--update-round-trip"
        )
        self.assertEqual(good.returncode, 0, good.stderr)
        bad = self.run_cli(
            "verify-file", "--id", "A", "--file", str(self.b), "--update-round-trip"
        )
        self.assertEqual(bad.returncode, 4)
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        record = registry["artifacts"]["A"]
        self.assertEqual(record["round_trip_verified"], "FALSE")
        self.assertEqual(len(record["round_trip_witnesses"]), 2)
        self.assertTrue(record["round_trip_witnesses"][0]["match"])
        self.assertFalse(record["round_trip_witnesses"][1]["match"])

    def test_wrong_round_trip_refuses(self) -> None:
        self.register("A", self.a)
        result = self.run_cli("verify-file", "--id", "A", "--file", str(self.b))
        self.assertEqual(result.returncode, 4)
        observation = json.loads(result.stdout)
        self.assertFalse(observation["match"])

    def test_duplicate_identity_refuses_instead_of_overwriting_history(self) -> None:
        self.register("A", self.a)
        duplicate = self.run_cli("register", "--id", "A", "--file", str(self.b))
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn("new artifact identity plus supersession", duplicate.stderr)
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        self.assertEqual(registry["artifacts"]["A"]["bytes"], 5)

    def test_superseded_review_refuses_by_default(self) -> None:
        self.register("A", self.a)
        self.register("B", self.b)
        result = self.run_cli("supersede", "--old", "A", "--new", "B")
        self.assertEqual(result.returncode, 0, result.stderr)

        result = self.run_cli("resolve", "--id", "A")
        self.assertEqual(result.returncode, 3)
        state = json.loads(result.stdout)
        self.assertEqual(state["status"], "SUPERSEDED")
        self.assertFalse(state["review_allowed"])
        self.assertEqual(state["successors"], ["B"])

        historical = self.run_cli("resolve", "--id", "A", "--historical")
        self.assertEqual(historical.returncode, 0, historical.stderr)
        self.assertTrue(json.loads(historical.stdout)["review_allowed"])

    def test_supersession_cycle_refuses(self) -> None:
        self.register("A", self.a)
        self.register("B", self.b)
        self.assertEqual(
            self.run_cli("supersede", "--old", "A", "--new", "B").returncode, 0
        )
        cycle = self.run_cli("supersede", "--old", "B", "--new", "A")
        self.assertNotEqual(cycle.returncode, 0)
        self.assertIn("cycle", cycle.stderr)

    def test_declared_identity_must_match_measured_file(self) -> None:
        result = self.run_cli(
            "register",
            "--id",
            "A",
            "--file",
            str(self.a),
            "--sha256",
            "0" * 64,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("disagrees", result.stderr)

    def test_existing_writer_lock_refuses_mutation(self) -> None:
        lock = self.registry.with_suffix(self.registry.suffix + ".lock")
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_text("occupied\n", encoding="utf-8")
        result = self.run_cli("register", "--id", "A", "--file", str(self.a))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("write-locked", result.stderr)
        self.assertFalse(self.registry.exists())


if __name__ == "__main__":
    unittest.main()
