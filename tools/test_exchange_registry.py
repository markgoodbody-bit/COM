from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT = Path(__file__).with_name("exchange_registry.py")


def utc_after(*, days=0, minutes=0):
    return (
        datetime.now(timezone.utc) + timedelta(days=days, minutes=minutes)
    ).isoformat().replace("+00:00", "Z")


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

    def add(self, artifact_id, file, observed_at=None):
        args = ["register", "--id", artifact_id, "--file", str(file)]
        if observed_at:
            args += ["--observed-at", observed_at]
        result = self.cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr)

    def reconcile(self, *, observed_at=None, valid_until=None):
        args = [
            "reconcile",
            "--against", "git:branch@abc",
            "--coverage", "full published candidate set",
            "--method", "adapter-head-walk",
            "--observer", "TEST",
            "--evidence-ref", "git:branch@abc#walk-receipt",
            "--valid-until", valid_until or utc_after(minutes=10),
        ]
        if observed_at:
            args += ["--observed-at", observed_at]
        result = self.cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_measured_and_declared_identity_are_distinct(self):
        self.add("A", self.a)
        digest = hashlib.sha256(b"beta").hexdigest()
        result = self.cli(
            "register", "--id", "B", "--sha256", digest, "--bytes", "4"
        )
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
        data = json.loads(result.stdout)
        self.assertFalse(data["review_allowed"])
        self.assertEqual(data["reconciliation_state"], "ABSENT")

    def test_reconcile_requires_evidence_reference(self):
        result = self.cli(
            "reconcile",
            "--against", "git:branch@abc",
            "--coverage", "full published candidate set",
            "--method", "adapter-head-walk",
            "--observer", "TEST",
            "--valid-until", utc_after(minutes=10),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence-ref", result.stderr)

    def test_reconcile_validity_bound_must_follow_observation(self):
        result = self.cli(
            "reconcile",
            "--against", "git:branch@abc",
            "--coverage", "full published candidate set",
            "--method", "adapter-head-walk",
            "--observer", "TEST",
            "--evidence-ref", "receipt:1",
            "--observed-at", "2026-01-02T00:00:00Z",
            "--valid-until", "2026-01-01T00:00:00Z",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("later than", result.stderr)

    def test_reconciled_current_carries_basis_but_does_not_self_verify(self):
        self.add("A", self.a)
        self.reconcile()
        result = self.cli("resolve", "--id", "A")
        self.assertEqual(result.returncode, 5)
        data = json.loads(result.stdout)
        self.assertFalse(data["review_allowed"])
        self.assertEqual(data["last_reconciliation"]["observer"], "TEST")
        self.assertEqual(data["reconciliation_state"], "BOUNDED_DECLARATION")
        self.assertIn("declared basis", data["reconciliation_detail"])

    def test_explicit_acceptance_of_declared_reconciliation_is_visible(self):
        self.add("A", self.a)
        self.reconcile()
        result = self.cli(
            "resolve", "--id", "A", "--accept-declared-reconciliation"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["review_allowed"])
        self.assertEqual(data["reconciliation_state"], "BOUNDED_DECLARATION")
        self.assertIn("explicitly accepted", data["reason"])
        self.assertIn("not mechanically verified", data["reason"])

    def test_expired_reconciliation_refuses(self):
        self.add("A", self.a, observed_at="2020-01-01T00:00:00Z")
        self.reconcile(
            observed_at="2020-01-02T00:00:00Z",
            valid_until="2020-01-03T00:00:00Z",
        )
        result = self.cli("resolve", "--id", "A")
        self.assertEqual(result.returncode, 5)
        data = json.loads(result.stdout)
        self.assertFalse(data["review_allowed"])
        self.assertEqual(data["reconciliation_state"], "EXPIRED")

    def test_reconciliation_predating_artifact_refuses(self):
        self.add("A", self.a, observed_at="2025-01-02T00:00:00Z")
        self.reconcile(
            observed_at="2025-01-01T00:00:00Z",
            valid_until="2099-01-01T00:00:00Z",
        )
        result = self.cli("resolve", "--id", "A")
        self.assertEqual(result.returncode, 5)
        data = json.loads(result.stdout)
        self.assertFalse(data["review_allowed"])
        self.assertEqual(data["reconciliation_state"], "PREDATES_ARTIFACT")

    def test_round_trip_is_timed_witness_not_standing_bool(self):
        self.add("A", self.a)
        result = self.cli(
            "verify-file", "--id", "A", "--file", str(self.a),
            "--record-witness", "--witness-kind", "ROUND_TRIP_COPY",
            "--source-ref", "github:raw/A",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.reconcile()
        resolved = json.loads(
            self.cli(
                "resolve", "--id", "A", "--accept-declared-reconciliation"
            ).stdout
        )
        self.assertEqual(resolved["round_trip"]["latest_result"], "TRUE")
        self.assertEqual(
            resolved["round_trip"]["validity"], "OBSERVED_AT_TIME_ONLY"
        )
        record = json.loads(
            self.registry.read_text(encoding="utf-8")
        )["artifacts"]["A"]
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
        result = self.cli(
            "verify-file", "--id", "A", "--file", str(self.a), "--record-witness"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.reconcile()
        resolved = json.loads(
            self.cli(
                "resolve", "--id", "A", "--accept-declared-reconciliation"
            ).stdout
        )
        self.assertEqual(resolved["round_trip"]["latest_result"], "UNKNOWN")

    def test_superseded_review_refuses(self):
        self.add("A", self.a)
        self.add("B", self.b)
        self.assertEqual(
            self.cli("supersede", "--old", "A", "--new", "B").returncode, 0
        )
        self.reconcile()
        result = self.cli("resolve", "--id", "A")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["status"], "SUPERSEDED")

    def test_fork_is_explicit_and_descendants_are_contested_and_refused(self):
        self.add("P", self.a)
        self.add("B", self.b)
        digest = hashlib.sha256(b"beta").hexdigest()
        self.assertEqual(
            self.cli(
                "register", "--id", "C", "--sha256", digest, "--bytes", "4"
            ).returncode,
            0,
        )
        self.cli("supersede", "--old", "P", "--new", "B")
        self.cli("supersede", "--old", "P", "--new", "C")
        self.reconcile()

        ancestor = self.cli("resolve", "--id", "P")
        self.assertEqual(ancestor.returncode, 3)
        self.assertEqual(json.loads(ancestor.stdout)["status"], "FORKED")

        descendant = self.cli("resolve", "--id", "B")
        self.assertEqual(descendant.returncode, 3)
        descendant_data = json.loads(descendant.stdout)
        self.assertFalse(descendant_data["review_allowed"])
        self.assertEqual(descendant_data["status"], "CONTESTED_FORK")
        self.assertEqual(descendant_data["fork_ancestors"], ["P"])

        listed = json.loads(self.cli("list-current").stdout)
        rows = {
            row["artifact"]["artifact_id"]: row for row in listed["current"]
        }
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
        self.assertNotEqual(
            self.cli(
                "register", "--id", "A", "--file", str(self.b)
            ).returncode,
            0,
        )

    def test_declared_identity_must_match_measured_file(self):
        result = self.cli(
            "register",
            "--id", "A",
            "--file", str(self.a),
            "--sha256", "0" * 64,
        )
        self.assertNotEqual(result.returncode, 0)

    def test_existing_writer_lock_refuses_mutation(self):
        lock = self.registry.with_suffix(".json.lock")
        lock.write_text("occupied\n", encoding="utf-8")
        result = self.cli("register", "--id", "A", "--file", str(self.a))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("write-locked", result.stderr)


if __name__ == "__main__":
    unittest.main()
