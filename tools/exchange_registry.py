#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

SCHEMA_VERSION = "exchange-artifact-registry-v0.2"


def now_dt() -> datetime:
    return datetime.now(timezone.utc)


def utc_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def now_utc() -> str:
    return utc_text(now_dt())


def parse_utc(value: str, label: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{label} must be a non-empty ISO-8601 timestamp with timezone")
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit(f"{label} is not valid ISO-8601: {value!r}") from exc
    if parsed.tzinfo is None:
        raise SystemExit(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def canonical_utc(value: str, label: str) -> str:
    return utc_text(parse_utc(value, label))


def empty_registry():
    return {
        "schema": SCHEMA_VERSION,
        "generation": 0,
        "updated_at": now_utc(),
        "reconciliations": [],
        "artifacts": {},
    }


def load_registry(path: Path):
    if not path.exists():
        return empty_registry()
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA_VERSION:
        raise SystemExit(f"unsupported registry schema: {data.get('schema')!r}")
    if not isinstance(data.get("artifacts"), dict):
        raise SystemExit("invalid registry: artifacts must be an object")
    if not isinstance(data.get("generation", 0), int):
        raise SystemExit("invalid registry: generation must be an integer")
    if not isinstance(data.get("reconciliations", []), list):
        raise SystemExit("invalid registry: reconciliations must be an array")
    data.setdefault("generation", 0)
    data.setdefault("reconciliations", [])
    return data


@contextmanager
def registry_lock(path: Path) -> Iterator[None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(path.suffix + ".lock")
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(
            f"registry is write-locked: {lock_path} "
            "(remove only after establishing no writer is active)"
        )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(
                json.dumps({"pid": os.getpid(), "created_at": now_utc()}) + "\n"
            )
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def save_registry(path: Path, data):
    data["generation"] = int(data.get("generation", 0)) + 1
    data["updated_at"] = now_utc()
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temp, path)


def sha256_file(path: Path):
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            total += len(chunk)
            digest.update(chunk)
    return digest.hexdigest(), total


def req(data, artifact_id):
    try:
        return data["artifacts"][artifact_id]
    except KeyError:
        raise SystemExit(f"unknown artifact: {artifact_id}")


def latest_rec(data):
    reconciliations = data.get("reconciliations", [])
    return reconciliations[-1] if reconciliations else None


def cmd_register(args):
    path = Path(args.registry)
    with registry_lock(path):
        data = load_registry(path)
        if args.id in data["artifacts"]:
            raise SystemExit(
                f"artifact already exists: {args.id}; "
                "corrections require a new artifact identity plus supersession"
            )

        expected_hash, expected_bytes = args.sha256, args.bytes
        identity_source = "DECLARED"
        if args.file:
            measured_hash, measured_bytes = sha256_file(Path(args.file))
            if expected_hash and expected_hash.lower() != measured_hash:
                raise SystemExit("provided --sha256 disagrees with measured --file")
            if expected_bytes is not None and expected_bytes != measured_bytes:
                raise SystemExit("provided --bytes disagrees with measured --file")
            expected_hash, expected_bytes, identity_source = (
                measured_hash,
                measured_bytes,
                "MEASURED",
            )
        elif expected_hash is None or expected_bytes is None:
            raise SystemExit(
                "declared artifact identity requires both --sha256 and --bytes; "
                "use --file to measure instead"
            )

        observed_at = (
            canonical_utc(args.observed_at, "artifact --observed-at")
            if args.observed_at
            else now_utc()
        )
        record = {
            "artifact_id": args.id,
            "locator": args.locator,
            "sha256": expected_hash.lower(),
            "bytes": expected_bytes,
            "identity_source": identity_source,
            "publication_commit": args.commit,
            "created_by": args.created_by,
            "observed_at": observed_at,
            "supersedes": [],
            "superseded_by": [],
            "verification_witnesses": [],
            "review_target_hashes": sorted(
                set(value.lower() for value in (args.review_target_hash or []))
            ),
        }
        data["artifacts"][args.id] = record
        save_registry(path, data)
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


def reachable(data, start, target):
    seen = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current == target:
            return True
        if current in seen:
            continue
        seen.add(current)
        record = data["artifacts"].get(current)
        if record:
            stack.extend(record.get("superseded_by", []))
    return False


def fork_ancestors(data, artifact_id):
    forks = set()
    seen = set()
    stack = [artifact_id]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        record = data["artifacts"].get(current)
        if not record:
            continue
        if len(record.get("superseded_by", [])) > 1:
            forks.add(current)
        stack.extend(record.get("supersedes", []))
    return sorted(forks)


def cmd_supersede(args):
    path = Path(args.registry)
    with registry_lock(path):
        data = load_registry(path)
        old = req(data, args.old)
        new = req(data, args.new)
        if args.old == args.new:
            raise SystemExit("an artifact cannot supersede itself")
        if reachable(data, args.new, args.old):
            raise SystemExit("supersession would create a cycle")
        if args.new not in old["superseded_by"]:
            old["superseded_by"].append(args.new)
            old["superseded_by"].sort()
        if args.old not in new["supersedes"]:
            new["supersedes"].append(args.old)
            new["supersedes"].sort()
        save_registry(path, data)
    print(json.dumps({"old": old, "new": new}, indent=2, sort_keys=True))
    return 0


def cmd_reconcile(args):
    path = Path(args.registry)
    observed_at = (
        canonical_utc(args.observed_at, "reconcile --observed-at")
        if args.observed_at
        else now_utc()
    )
    valid_until = canonical_utc(args.valid_until, "reconcile --valid-until")
    if parse_utc(valid_until, "reconcile --valid-until") <= parse_utc(
        observed_at, "reconcile --observed-at"
    ):
        raise SystemExit(
            "reconcile --valid-until must be later than the reconciliation observation"
        )
    witness = {
        "observed_at": observed_at,
        "valid_until": valid_until,
        "reconciled_against": args.against,
        "coverage": args.coverage,
        "method": args.method,
        "observer": args.observer,
        "evidence_ref": args.evidence_ref,
    }
    with registry_lock(path):
        data = load_registry(path)
        data.setdefault("reconciliations", []).append(witness)
        save_registry(path, data)
    print(json.dumps(witness, indent=2, sort_keys=True))
    return 0


def reconciliation_state(reconciliation, artifact):
    if reconciliation is None:
        return "ABSENT", "no registry reconciliation witness"

    evidence_ref = reconciliation.get("evidence_ref")
    valid_until = reconciliation.get("valid_until")
    observed_at = reconciliation.get("observed_at")
    if not evidence_ref:
        return "INVALID", "latest reconciliation has no evidence_ref"
    if not valid_until:
        return "INVALID", "latest reconciliation has no declared validity bound"
    if not observed_at:
        return "INVALID", "latest reconciliation has no observation time"

    try:
        rec_time = parse_utc(observed_at, "stored reconciliation observed_at")
        expiry = parse_utc(valid_until, "stored reconciliation valid_until")
        artifact_time = parse_utc(
            artifact.get("observed_at"), "stored artifact observed_at"
        )
    except SystemExit as exc:
        return "INVALID", str(exc)

    if expiry <= rec_time:
        return "INVALID", "reconciliation validity bound is not after its observation"
    if rec_time < artifact_time:
        return (
            "PREDATES_ARTIFACT",
            "latest reconciliation predates this artifact and cannot vouch for it",
        )
    if now_dt() > expiry:
        return "EXPIRED", f"latest reconciliation expired at {utc_text(expiry)}"
    return (
        "BOUNDED_DECLARATION",
        f"latest reconciliation is a declared basis bounded until {utc_text(expiry)}",
    )


def rt_summary(record):
    witnesses = [
        witness
        for witness in record.get("verification_witnesses", [])
        if witness.get("witness_kind") == "ROUND_TRIP_COPY"
    ]
    if not witnesses:
        return {
            "latest_result": "UNKNOWN",
            "latest_observed_at": None,
            "validity": "NO_WITNESS",
        }
    latest = witnesses[-1]
    return {
        "latest_result": "TRUE" if latest.get("match") else "FALSE",
        "latest_observed_at": latest.get("observed_at"),
        "validity": "OBSERVED_AT_TIME_ONLY",
        "witness_count": len(witnesses),
    }


def cmd_resolve(args):
    data = load_registry(Path(args.registry))
    record = req(data, args.id)
    successors = record.get("superseded_by", [])
    forks = fork_ancestors(data, args.id)
    reconciliation = latest_rec(data)
    rec_state, rec_detail = reconciliation_state(reconciliation, record)

    if len(successors) > 1:
        status = "FORKED"
    elif successors:
        status = "SUPERSEDED"
    elif forks:
        status = "CONTESTED_FORK"
    else:
        status = "CURRENT_IN_REGISTRY"

    if args.historical:
        allowed, reason, return_code = True, "explicit historical review", 0
    elif status == "FORKED":
        allowed, reason, return_code = (
            False,
            "lineage forks at this artifact; choose an explicit successor/lineage",
            3,
        )
    elif status == "CONTESTED_FORK":
        allowed, reason, return_code = (
            False,
            "artifact is a current descendant of a contested fork; "
            "ordinary current-target review requires explicit lineage adjudication",
            3,
        )
    elif status == "SUPERSEDED":
        allowed, reason, return_code = (
            False,
            "known-superseded object; name the successor or pass --historical",
            3,
        )
    elif args.allow_unreconciled and rec_state == "ABSENT":
        # ABSENT means no reconciliation basis exists. The other states mean the
        # registry DID detect a basis and found it defective or stale, which is
        # a different act to accept and must be named separately. A flag about
        # absence must not clear a detected fault.
        allowed, reason, return_code = (
            True,
            "current in bounded registry; absent reconciliation explicitly "
            "allowed (reconciliation_state=ABSENT)",
            0,
        )
    elif args.allow_unreconciled:
        allowed, reason, return_code = (
            False,
            f"--allow-unreconciled applies only to reconciliation_state=ABSENT; "
            f"this registry detected {rec_state}, which is a defective or stale "
            f"basis rather than a missing one and remains a refusal",
            5,
        )
    elif rec_state == "BOUNDED_DECLARATION" and args.accept_declared_reconciliation:
        allowed, reason, return_code = (
            True,
            "current in bounded registry; caller explicitly accepted a declared, "
            "time-bounded reconciliation basis (adequacy not mechanically verified)",
            0,
        )
    elif rec_state == "BOUNDED_DECLARATION":
        allowed, reason, return_code = (
            False,
            "a time-bounded reconciliation basis is recorded but remains a "
            "declaration; pass --accept-declared-reconciliation only if the "
            "using aperture explicitly accepts that boundary",
            5,
        )
    else:
        allowed, reason, return_code = (
            False,
            f"registry reconciliation is not usable for current-target review: "
            f"{rec_state}: {rec_detail}",
            5,
        )

    output = {
        "registry_generation": data.get("generation", 0),
        "registry_updated_at": data.get("updated_at"),
        "last_reconciliation": reconciliation,
        "reconciliation_state": rec_state,
        "reconciliation_detail": rec_detail,
        "artifact": record,
        "status": status,
        "successors": successors,
        "fork_ancestors": forks,
        "round_trip": rt_summary(record),
        "review_allowed": allowed,
        "reason": reason,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return return_code


def cmd_verify(args):
    path = Path(args.registry)

    def observe(data):
        record = req(data, args.id)
        measured_hash, measured_bytes = sha256_file(Path(args.file))
        expected_hash, expected_bytes = record.get("sha256"), record.get("bytes")
        match = (
            expected_hash is not None
            and expected_hash.lower() == measured_hash
            and expected_bytes is not None
            and expected_bytes == measured_bytes
        )
        return record, {
            "artifact_id": args.id,
            "method": "local-file-sha256+bytes",
            "source": str(Path(args.file)),
            "measured_sha256": measured_hash,
            "measured_bytes": measured_bytes,
            "expected_sha256": expected_hash,
            "expected_bytes": expected_bytes,
            "match": match,
            "observed_at": now_utc(),
        }

    if args.record_witness:
        if args.witness_kind == "ROUND_TRIP_COPY" and not args.source_ref:
            raise SystemExit("--source-ref is required for ROUND_TRIP_COPY witnesses")
        with registry_lock(path):
            data = load_registry(path)
            record, observation = observe(data)
            observation["witness_kind"] = args.witness_kind
            observation["source_ref"] = args.source_ref
            record.setdefault("verification_witnesses", []).append(observation)
            save_registry(path, data)
    else:
        data = load_registry(path)
        _, observation = observe(data)
        observation["witness_kind"] = args.witness_kind
        observation["source_ref"] = args.source_ref

    print(json.dumps(observation, indent=2, sort_keys=True))
    return 0 if observation["match"] else 4


def cmd_list(args):
    data = load_registry(Path(args.registry))
    reconciliation = latest_rec(data)
    current = []
    for record in data["artifacts"].values():
        if record.get("superseded_by"):
            continue
        forks = fork_ancestors(data, record["artifact_id"])
        rec_state, rec_detail = reconciliation_state(reconciliation, record)
        current.append(
            {
                "artifact": record,
                "lineage_status": "CONTESTED_FORK" if forks else "UNFORKED_IN_REGISTRY",
                "fork_ancestors": forks,
                "reconciliation_state": rec_state,
                "reconciliation_detail": rec_detail,
                "round_trip": rt_summary(record),
            }
        )
    current.sort(key=lambda row: row["artifact"]["artifact_id"])
    print(
        json.dumps(
            {
                "registry_generation": data.get("generation", 0),
                "registry_updated_at": data.get("updated_at"),
                "last_reconciliation": reconciliation,
                "current": current,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def parser():
    root = argparse.ArgumentParser()
    root.add_argument("--registry", default="exchange/artifacts.json")
    commands = root.add_subparsers(dest="command", required=True)

    command = commands.add_parser("register")
    command.add_argument("--id", required=True)
    command.add_argument("--locator")
    command.add_argument("--file")
    command.add_argument("--sha256")
    command.add_argument("--bytes", type=int)
    command.add_argument("--commit")
    command.add_argument("--created-by")
    command.add_argument("--observed-at")
    command.add_argument("--review-target-hash", action="append")
    command.set_defaults(func=cmd_register)

    command = commands.add_parser("supersede")
    command.add_argument("--old", required=True)
    command.add_argument("--new", required=True)
    command.set_defaults(func=cmd_supersede)

    command = commands.add_parser("reconcile")
    command.add_argument("--against", required=True)
    command.add_argument("--coverage", required=True)
    command.add_argument("--method", required=True)
    command.add_argument("--observer", required=True)
    command.add_argument("--evidence-ref", required=True)
    command.add_argument("--valid-until", required=True)
    command.add_argument("--observed-at")
    command.set_defaults(func=cmd_reconcile)

    command = commands.add_parser("resolve")
    command.add_argument("--id", required=True)
    command.add_argument("--historical", action="store_true")
    command.add_argument("--allow-unreconciled", action="store_true")
    command.add_argument("--accept-declared-reconciliation", action="store_true")
    command.set_defaults(func=cmd_resolve)

    command = commands.add_parser("verify-file")
    command.add_argument("--id", required=True)
    command.add_argument("--file", required=True)
    command.add_argument("--record-witness", action="store_true")
    command.add_argument(
        "--witness-kind",
        choices=["LOCAL_COPY", "ROUND_TRIP_COPY"],
        default="LOCAL_COPY",
    )
    command.add_argument("--source-ref")
    command.set_defaults(func=cmd_verify)

    command = commands.add_parser("list-current")
    command.set_defaults(func=cmd_list)

    return root


def main():
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
