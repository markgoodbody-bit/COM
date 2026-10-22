"""Offline checks for the finite inside/outside observation; not a VM test."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

import boundary_probe as probe


class BoundaryProbeTests(unittest.TestCase):
    def test_stdout_only_does_not_claim_disk_or_host_confirmation(self):
        data, sha = probe.capture("assistant_sandbox", "COM-IO-20261023-A")
        self.assertEqual(data["declared_surface"], "assistant_sandbox")
        self.assertFalse(data["surface_attested"])
        self.assertEqual(data["observations"]["scratch_write"], "NOT_TESTED")
        self.assertIn("vm_origin_attestation", data["not_observed"])
        self.assertEqual(sha, hashlib.sha256(probe.canonical_bytes(data)).hexdigest())

    def test_one_exclusive_private_local_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "receipt.json"
            data, sha = probe.capture("ubuntu_guest", "COM-IO-20261023-A", path)
            raw = path.read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), sha)
            self.assertEqual(json.loads(raw), data)
            self.assertEqual(data["observations"]["scratch_write"], "OBSERVED")
            self.assertFalse(data["surface_attested"])
            if os.name == "posix":
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                probe.capture("ubuntu_guest", "COM-IO-20261023-A", path)

    def test_invalid_or_unsanctioned_path_refused(self):
        with self.assertRaises(ValueError):
            probe.capture("other", "tiny")
        with self.assertRaises(ValueError):
            probe.capture("unknown", "COM-IO-20261023-A")
        with self.assertRaises(ValueError):
            probe.capture("assistant_sandbox", "COM-IO-20261023-A", "relative.json")

    def test_symlink_scratch_parent_refused(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            real = root / "real"
            real.mkdir()
            link = root / "link"
            try:
                link.symlink_to(real, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with self.assertRaises(ValueError):
                probe.capture("ubuntu_guest", "COM-IO-20261023-A", link / "receipt.json")


if __name__ == "__main__":
    unittest.main()
