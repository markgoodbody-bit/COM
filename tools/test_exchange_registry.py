from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("exchange_registry.py")


class ExchangeRegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.registry = self.root / "registry.json"
        self.a = self.root / "a.txt"
        self.b = self.root / "b.txt"
        self.a.write_text("alpha", encoding="utf-8")
        self.b.write_text("beta", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--registry", str(self.registry), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def add(self, artifact_id, file):
        result = self.cli("register", "--id", artifact_id, "--file", str(file))
        self.assertEqual(result.returncode, 0, result.stderr)

    def reconcile(self):
        result = self.cli(
            "reconcile",
            "--against", "git:branch@abc",
            "--coverage", "full published candidate set",
            "--method", "adapter-head-walk",
            "--observer", "TEST",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_measured_and_declared_identity_are_distinct(self):
        self.add("A", self.a)
        digest = hashlib.sha256(b"beta").hexdigest()
        result = self.cli("register", "--id", "B", "--sha256", digest, "--bytes", "4")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(self.registry.read_text(encoding="utf-8"))
        self.assertEqual(data["artifacts"]["A"]["identity_source"], "MEASURED")
        self.assertEqual(data["artifacts"]["B"]["identity_source"], "DECLARED")

    def test_declared_identity_requires_hash_and_bytes(self):
        result = self.cli("register", "--id", "A", "--sha256", "0" * 64)
        self.assertNotEqual(result.returncode, 0)

    def test_unreconciled_current_refuses_by_default(self):
        self.add("A", self.a)
        result = self.cli("resolve", "--id", "A")
        self.assertEqual(result.returncode, 5)
        self.assertFalse(json.loads(result.stdout)["review_allowed"])

    def test_reconciled_current_carries_basis(self):
        self.add("A", self.a)
        self.reconcile()
        result = self.cli("resolve", "--id", "A")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["review_allowed"])
        self.assertEqual(data["last_reconciliation"]["observer"], "TEST")

    def test_round_trip_is_timed_witness_not_standing_bool(self):
        self.add("A", self.a)
        result = self.cli(
            "verify-file", "--id", "A", "--file", str(self.a),
            "--record-witness", "--witness-kind", "ROUND_TRIP_COPY",
            "--source-ref", "github:raw/A",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.reconcile()
        resolved = json.loads(self.cli("resolve", "--id", "A").stdout)
        self.assertEqual(resolved["round_trip"]["latest_result"], "TRUE")
        self.assertEqual(resolved["round_trip"]["validity"], "OBSERVED_AT_TIME_ONLY")
        record = json.loads(self.registry.read_text(encoding="utf-8"))["artifacts"]["A"]
        self.assertNotIn("round_trip_verified", record)

    def test_round_trip_requires_source_reference(self):
        self.add("A", self.a)
        result = self.cli(
            "verify-file", "--id", "A", "--file", str(self.a),
            "--record-witness", "--witness-kind", "ROUND_TRIP_COPY",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source-ref", result.stderr)

    def test_local_copy_witness_does_not_become_round_trip(self):
        self.add("A", self.a)
        result = self.cli("verify-file", "--id", "A", "--file", str(self.a), "--record-witness")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.reconcile()
        resolved = json.loads(self.cli("resolve", "--id", "A").stdout)
        self.assertEqual(resolved["round_trip"]["latest_result"], "UNKNOWN")

    def test_superseded_review_refuses(self):
        self.add("A", self.a)
        self.add("B", self.b)
        self.assertEqual(self.cli("supersede", "--old", "A", "--new", "B").returncode, 0)
        self.reconcile()
        result = self.cli("resolve", "--id", "A")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["status"], "SUPERSEDED")

    def test_fork_is_explicit_and_descendants_are_contested(self):
        self.add("P", self.a)
        self.add("B", self.b)
        digest = hashlib.sha256(b"beta").hexdigest()
        self.assertEqual(self.cli("register", "--id", "C", "--sha256", digest, "--bytes", "4").returncode, 0)
        self.cli("supersede", "--old", "P", "--new", "B")
        self.cli("supersede", "--old", "P", "--new", "C")
        self.reconcile()
        result = self.cli("resolve", "--id", "P")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["status"], "FORKED")
        listed = json.loads(self.cli("list-current").stdout)
        rows = {row["artifact"]["artifact_id"]: row for row in listed["current"]}
        self.assertEqual(rows["B"]["lineage_status"], "CONTESTED_FORK")
        self.assertEqual(rows["C"]["fork_ancestors"], ["P"])

    def test_supersession_cycle_refuses(self):
        self.add("A", self.a)
        self.add("B", self.b)
        self.cli("supersede", "--old", "A", "--new", "B")
        result = self.cli("supersede", "--old", "B", "--new", "A")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cycle", result.stderr)

    def test_duplicate_identity_refuses(self):
        self.add("A", self.a)
        self.assertNotEqual(self.cli("register", "--id", "A", "--file", str(self.b)).returncode, 0)

    def test_declared_identity_must_match_measured_file(self):
        result = self.cli("register", "--id", "A", "--file", str(self.a), "--sha256", "0" * 64)
        self.assertNotEqual(result.returncode, 0)

    def test_existing_writer_lock_refuses_mutation(self):
        lock = self.registry.with_suffix(".json.lock")
        lock.write_text("occupied\n", encoding="utf-8")
        result = self.cli("register", "--id", "A", "--file", str(self.a))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("write-locked", result.stderr)


if __name__ == "__main__":
    unittest.main()
