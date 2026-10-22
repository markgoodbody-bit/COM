#!/usr/bin/env python3
"""Finite inside/outside observation. No network, shell, credentials, or model calls.

A claimed surface is a LABEL supplied by the operator, not a machine attestation.
Run under a separately reviewed, bounded execution grant only.
"""
import argparse
import datetime
import hashlib
import json
import os
import platform
import re
import secrets
import sys
from pathlib import Path

SCHEMA = "me-workshop-boundary-probe.v1"
SURFACES = ("assistant_sandbox", "ubuntu_guest", "windows_host", "other")
CHALLENGE = re.compile(r"[A-Za-z0-9:_-]{8,96}\Z")


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def capture(surface, challenge, output=None):
    if surface not in SURFACES:
        raise ValueError("unsupported declared surface")
    if not CHALLENGE.fullmatch(challenge):
        raise ValueError("challenge must contain 8–96 safe ASCII characters")
    if output is not None:
        path = Path(output)
        if not path.is_absolute():
            raise ValueError("output must be an absolute, preapproved scratch-file path")
        if path.parent.is_symlink() or not path.parent.is_dir():
            raise ValueError("scratch parent must be a present, non-symlink directory")
        if path.exists() or path.is_symlink():
            raise FileExistsError("receipt exists: refusing overwrite")
    else:
        path = None

    receipt = {
        "schema": SCHEMA,
        "declared_surface": surface,
        "surface_attested": False,
        "challenge": challenge,
        "run_id_not_authority": secrets.token_hex(12),
        "observer_utc_not_trusted_clock": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(timespec="milliseconds"),
        "observations": {
            "python_executed": True,
            "python_version": ".".join(str(n) for n in sys.version_info[:3]),
            "os_family": platform.system(),
            "effective_uid": os.geteuid() if hasattr(os, "geteuid") else None,
            "scratch_write": "NOT_TESTED" if path is None else "ATTEMPTED",
            "scratch_same_process_readback": "NOT_TESTED" if path is None else "ATTEMPTED",
        },
        "not_observed": [
            "host_independent_confirmation",
            "vm_origin_attestation",
            "persistent_model_process",
            "network_egress",
            "external_side_effect",
            "durable_replay_or_stop_authority",
        ],
    }
    if path is not None:
        receipt["observations"]["scratch_write"] = "OBSERVED"
        receipt["observations"]["scratch_same_process_readback"] = "OBSERVED"
        raw = canonical_bytes(receipt)
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(str(path), flags, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
            f.flush()
        with path.open("rb") as f:
            if f.read() != raw:
                raise OSError("same-process scratch readback mismatch")
    else:
        raw = canonical_bytes(receipt)

    return receipt, hashlib.sha256(raw).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("capture",))
    parser.add_argument("--surface", required=True, choices=SURFACES)
    parser.add_argument("--challenge", required=True)
    parser.add_argument("--out", help="optional absolute, preapproved scratch receipt file; never overwritten")
    args = parser.parse_args(argv)
    try:
        receipt, digest = capture(args.surface, args.challenge, args.out)
    except (ValueError, FileExistsError, OSError) as error:
        print("BOUNDARY_PROBE_REFUSED: " + type(error).__name__, file=sys.stderr)
        return 2
    print(json.dumps({
        "schema": SCHEMA,
        "status": "LOCAL_PROCESS_FINISHED",
        "declared_surface": receipt["declared_surface"],
        "surface_attested": False,
        "challenge": receipt["challenge"],
        "run_id_not_authority": receipt["run_id_not_authority"],
        "receipt_sha256": digest,
        "receipt_persisted_in_preapproved_scratch": args.out is not None,
        "host_independent_confirmation": "NOT_PERFORMED",
        "network_or_model_work": "NOT_PERFORMED",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
