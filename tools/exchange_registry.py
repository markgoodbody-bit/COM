#!/usr/bin/env python3
"""
Experimental Exchange artifact/supersession registry.

Stdlib-only. This tool records mechanical artifact identity and supersession.
It does not decide correctness, canon, authority, or semantic validity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

SCHEMA_VERSION = "exchange-artifact-registry-v0.1"
TRI = {"TRUE", "FALSE", "UNKNOWN"}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def empty_registry() -> dict[str, Any]:
    return {
        "schema": SCHEMA_VERSION,
        "generation": 0,
        "updated_at": now_utc(),
        "artifacts": {},
    }


def load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return empty_registry()
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA_VERSION:
        raise SystemExit(f"unsupported registry schema: {data.get('schema')!r}")
    if not isinstance(data.get("artifacts"), dict):
        raise SystemExit("invalid registry: artifacts must be an object")
    if not isinstance(data.get("generation", 0), int):
        raise SystemExit("invalid registry: generation must be an integer")
    data.setdefault("generation", 0)
    return data


@contextmanager
def registry_lock(path: Path) -> Iterator[None]:
    """Fail rather than silently race another local writer."""
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
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps({"pid": os.getpid(), "created_at": now_utc()}) + "\n")
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def save_registry(path: Path, data: dict[str, Any]) -> None:
    data["generation"] = int(data.get("generation", 0)) + 1
    data["updated_at"] = now_utc()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    total = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            total += len(chunk)
            h.update(chunk)
    return h.hexdigest(), total


def require_artifact(data: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    try:
        return data["artifacts"][artifact_id]
    except KeyError:
        raise SystemExit(f"unknown artifact: {artifact_id}")


def command_register(args: argparse.Namespace) -> int:
    reg_path = Path(args.registry)
    with registry_lock(reg_path):
        data = load_registry(reg_path)
        artifacts = data["artifacts"]
        if args.id in artifacts:
            raise SystemExit(
                f"artifact already exists: {args.id}; "
                "corrections require a new artifact identity plus supersession"
            )

        observed_hash = args.sha256
        observed_bytes = args.bytes
        if args.file:
            file_hash, file_bytes = sha256_file(Path(args.file))
            if observed_hash and observed_hash.lower() != file_hash:
                raise SystemExit("provided --sha256 disagrees with measured --file")
            if observed_bytes is not None and observed_bytes != file_bytes:
                raise SystemExit("provided --bytes disagrees with measured --file")
            observed_hash, observed_bytes = file_hash, file_bytes

        record = {
            "artifact_id": args.id,
            "locator": args.locator,
            "sha256": observed_hash.lower() if observed_hash else None,
            "bytes": observed_bytes,
            "publication_commit": args.commit,
            "created_by": args.created_by,
            "observed_at": args.observed_at or now_utc(),
            "supersedes": [],
            "superseded_by": [],
            "round_trip_verified": args.round_trip_verified,
            "round_trip_witnesses": [],
            "review_target_hashes": sorted(
                set(h.lower() for h in (args.review_target_hash or []))
            ),
        }
        artifacts[args.id] = record
        save_registry(reg_path, data)
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


def _reachable(data: dict[str, Any], start: str, target: str) -> bool:
    seen: set[str] = set()
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


def command_supersede(args: argparse.Namespace) -> int:
    reg_path = Path(args.registry)
    with registry_lock(reg_path):
        data = load_registry(reg_path)
        old = require_artifact(data, args.old)
        new = require_artifact(data, args.new)
        if args.old == args.new:
            raise SystemExit("an artifact cannot supersede itself")
        if _reachable(data, args.new, args.old):
            raise SystemExit("supersession would create a cycle")

        if args.new not in old["superseded_by"]:
            old["superseded_by"].append(args.new)
            old["superseded_by"].sort()
        if args.old not in new["supersedes"]:
            new["supersedes"].append(args.old)
            new["supersedes"].sort()

        save_registry(reg_path, data)
    print(json.dumps({"old": old, "new": new}, indent=2, sort_keys=True))
    return 0


def command_resolve(args: argparse.Namespace) -> int:
    data = load_registry(Path(args.registry))
    record = require_artifact(data, args.id)
    superseded = bool(record.get("superseded_by"))
    result = {
        "registry_generation": data.get("generation", 0),
        "registry_updated_at": data.get("updated_at"),
        "artifact": record,
        "status": "SUPERSEDED" if superseded else "CURRENT_IN_REGISTRY",
        "review_allowed": (not superseded) or args.historical,
    }
    if superseded:
        result["successors"] = record["superseded_by"]
        if not args.historical:
            result["reason"] = (
                "known-superseded object; name a successor or "
                "pass --historical explicitly"
            )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["review_allowed"] else 3


def command_verify_file(args: argparse.Namespace) -> int:
    reg_path = Path(args.registry)

    def observe(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        record = require_artifact(data, args.id)
        measured_hash, measured_bytes = sha256_file(Path(args.file))
        expected_hash = record.get("sha256")
        expected_bytes = record.get("bytes")
        hash_match = expected_hash is not None and expected_hash.lower() == measured_hash
        bytes_match = expected_bytes is not None and expected_bytes == measured_bytes
        match = hash_match and bytes_match
        observation = {
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
        return record, observation

    if args.update_round_trip:
        with registry_lock(reg_path):
            data = load_registry(reg_path)
            record, observation = observe(data)
            witnesses = record.setdefault("round_trip_witnesses", [])
            witnesses.append(observation)
            record["round_trip_verified"] = "TRUE" if observation["match"] else "FALSE"
            record["round_trip_observed_at"] = observation["observed_at"]
            save_registry(reg_path, data)
    else:
        data = load_registry(reg_path)
        _, observation = observe(data)

    print(json.dumps(observation, indent=2, sort_keys=True))
    return 0 if observation["match"] else 4


def command_list_current(args: argparse.Namespace) -> int:
    data = load_registry(Path(args.registry))
    current = [
        record
        for record in data["artifacts"].values()
        if not record.get("superseded_by")
    ]
    current.sort(key=lambda record: record["artifact_id"])
    print(
        json.dumps(
            {
                "registry_generation": data.get("generation", 0),
                "registry_updated_at": data.get("updated_at"),
                "current": current,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Mechanical artifact identity/supersession registry for Exchange."
    )
    p.add_argument("--registry", default="exchange/artifacts.json")
    sub = p.add_subparsers(dest="command", required=True)

    register = sub.add_parser("register", help="register an artifact identity")
    register.add_argument("--id", required=True)
    register.add_argument("--locator")
    register.add_argument("--file", help="measure sha256 and bytes from a local file")
    register.add_argument("--sha256")
    register.add_argument("--bytes", type=int)
    register.add_argument("--commit")
    register.add_argument("--created-by")
    register.add_argument("--observed-at")
    register.add_argument(
        "--round-trip-verified", choices=sorted(TRI), default="UNKNOWN"
    )
    register.add_argument("--review-target-hash", action="append")
    register.set_defaults(func=command_register)

    supersede = sub.add_parser("supersede", help="record old -> new supersession")
    supersede.add_argument("--old", required=True)
    supersede.add_argument("--new", required=True)
    supersede.set_defaults(func=command_supersede)

    resolve = sub.add_parser("resolve", help="resolve review status for an artifact")
    resolve.add_argument("--id", required=True)
    resolve.add_argument("--historical", action="store_true")
    resolve.set_defaults(func=command_resolve)

    verify = sub.add_parser(
        "verify-file", help="round-trip check a local copy against registry identity"
    )
    verify.add_argument("--id", required=True)
    verify.add_argument("--file", required=True)
    verify.add_argument("--update-round-trip", action="store_true")
    verify.set_defaults(func=command_verify_file)

    current = sub.add_parser(
        "list-current", help="list artifacts without known successors"
    )
    current.set_defaults(func=command_list_current)
    return p


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
