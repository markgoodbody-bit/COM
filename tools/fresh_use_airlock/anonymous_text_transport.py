#!/usr/bin/env python3
"""Render and verify one fresh-use cell as a deterministic UTF-8 message.

This is a local transport adapter.  It does not dispatch a message, interpret
cell contents, score an answer, or read the evaluator-only arm map.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath


LAUNCH_SENTENCE = (
    "Read only the packet below. Do not browse or use outside information. "
    "Answer in English. Complete the requested task within the stated answer budget.\n"
).encode("utf-8")
TRANSPORT_START = b"<<<FRESH_USE_ANONYMOUS_TEXT_TRANSPORT_V1>>>\n"
MEMBER_START = b"<<<FRESH_USE_MEMBER_V1>>>\n"
MEMBER_END = b"\n<<<END_FRESH_USE_MEMBER_V1>>>\n"
TRANSPORT_END = b"<<<END_FRESH_USE_ANONYMOUS_TEXT_TRANSPORT_V1>>>\n"
DIGEST_LABEL = b"message_sha256: "
DELIMITER_PREFIXES = (b"<<<FRESH_USE_", b"<<<END_FRESH_USE_")
HASH_RE = re.compile(rb"[0-9a-f]{64}")

REQUIRED_FIRST = ("START_HERE.md", "RUN_INSTRUCTION.md", "CASE_TASK.md")
OPTIONAL_AID = "REASONING_AID.md"
MANIFEST_NAME = "CELL_MANIFEST.json"
MAX_MEMBERS = 64
MAX_NAME_UTF8_BYTES = 512
MAX_MEMBER_BYTES = 8 * 1024 * 1024
MAX_TOTAL_MEMBER_BYTES = 32 * 1024 * 1024
# Framing overhead is small; this separately bounds an input message before parsing.
MAX_MESSAGE_BYTES = MAX_TOTAL_MEMBER_BYTES + 128 * 1024


class TransportError(RuntimeError):
    """A fail-closed transport validation error."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_member_order(names: set[str]) -> list[str]:
    """Return the only accepted outward member order for a neutral cell."""
    required = set(REQUIRED_FIRST) | {MANIFEST_NAME}
    missing = required - names
    if missing:
        raise TransportError(f"missing required cell member(s): {', '.join(sorted(missing))}")

    allowed_fixed = required | {OPTIONAL_AID}
    sources = []
    for name in names - allowed_fixed:
        if not name.startswith("SOURCES/") or name.count("/") != 1:
            raise TransportError(f"unexpected cell member: {name}")
        sources.append(name)

    order = list(REQUIRED_FIRST)
    if OPTIONAL_AID in names:
        order.append(OPTIONAL_AID)
    order.extend(sorted(sources))
    order.append(MANIFEST_NAME)
    if set(order) != names:
        raise TransportError("cell member set is not canonical")
    return order


def _validate_name(name: str) -> None:
    posix = PurePosixPath(name)
    if (
        not name
        or len(name.encode("utf-8")) > MAX_NAME_UTF8_BYTES
        or any(ord(character) < 32 or ord(character) == 127 for character in name)
        or "\\" in name
        or "\x00" in name
        or posix.is_absolute()
        or name != posix.as_posix()
        or any(part in {"", ".", ".."} for part in name.split("/"))
    ):
        raise TransportError(f"unsafe ZIP member name: {name!r}")


def _validate_member_bytes(name: str, data: bytes) -> None:
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise TransportError(f"non-UTF-8 cell member: {name}") from exc
    if any(prefix in data for prefix in DELIMITER_PREFIXES):
        raise TransportError(f"transport delimiter collision in cell member: {name}")


def _validate_manifest(members: dict[str, bytes]) -> None:
    try:
        manifest = json.loads(members[MANIFEST_NAME].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TransportError("CELL_MANIFEST.json is not valid UTF-8 JSON") from exc
    if not isinstance(manifest, dict) or not isinstance(manifest.get("members"), dict):
        raise TransportError("CELL_MANIFEST.json lacks a members object")

    declared = manifest["members"]
    expected_names = set(members) - {"START_HERE.md", MANIFEST_NAME}
    if set(declared) != expected_names:
        raise TransportError("CELL_MANIFEST.json does not exactly cover sealed members")
    for name in sorted(expected_names):
        record = declared[name]
        if not isinstance(record, dict):
            raise TransportError(f"invalid manifest record for member: {name}")
        data = members[name]
        if record.get("size_bytes") != len(data) or record.get("sha256") != sha256_bytes(data):
            raise TransportError(f"CELL_MANIFEST.json mismatch for member: {name}")


def read_cell(cell_path: Path) -> dict[str, bytes]:
    """Read a bounded sealed cell, rejecting ambiguous or unsafe members."""
    members: dict[str, bytes] = {}
    total = 0
    with zipfile.ZipFile(cell_path, "r") as archive:
        infos = archive.infolist()
        if not infos or len(infos) > MAX_MEMBERS:
            raise TransportError(f"cell must contain 1..{MAX_MEMBERS} members")
        if len({info.filename for info in infos}) != len(infos):
            raise TransportError("duplicate ZIP member name")

        for info in infos:
            name = info.filename
            _validate_name(name)
            unix_mode = info.external_attr >> 16
            if info.is_dir() or (unix_mode and not stat.S_ISREG(unix_mode)):
                raise TransportError(f"non-regular ZIP member: {name}")
            if info.file_size > MAX_MEMBER_BYTES:
                raise TransportError(f"cell member exceeds byte limit: {name}")
            total += info.file_size
            if total > MAX_TOTAL_MEMBER_BYTES:
                raise TransportError("cell members exceed total byte limit")
            with archive.open(info, "r") as handle:
                data = handle.read(MAX_MEMBER_BYTES + 1)
            if len(data) != info.file_size or len(data) > MAX_MEMBER_BYTES:
                raise TransportError(f"ZIP size mismatch for member: {name}")
            _validate_member_bytes(name, data)
            members[name] = data

    canonical_member_order(set(members))
    _validate_manifest(members)
    return members


def render_members(members: dict[str, bytes]) -> bytes:
    """Render already validated member bytes in canonical transport framing."""
    order = canonical_member_order(set(members))
    if not order or len(order) > MAX_MEMBERS:
        raise TransportError(f"cell must contain 1..{MAX_MEMBERS} members")
    total = 0
    for name in order:
        _validate_name(name)
        data = members[name]
        if len(data) > MAX_MEMBER_BYTES:
            raise TransportError(f"cell member exceeds byte limit: {name}")
        total += len(data)
        if total > MAX_TOTAL_MEMBER_BYTES:
            raise TransportError("cell members exceed total byte limit")
        _validate_member_bytes(name, data)
    _validate_manifest(members)

    pieces = [LAUNCH_SENTENCE, TRANSPORT_START, f"member_count: {len(order)}\n".encode("ascii")]
    for name in order:
        data = members[name]
        encoded_name = json.dumps(name, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        pieces.extend(
            [
                MEMBER_START,
                b"name: " + encoded_name + b"\n",
                f"byte_length: {len(data)}\n".encode("ascii"),
                b"sha256: " + sha256_bytes(data).encode("ascii") + b"\n",
                b"content:\n",
                data,
                MEMBER_END,
            ]
        )
    pieces.append(TRANSPORT_END)
    hashed_message = b"".join(pieces)
    if len(hashed_message) + len(DIGEST_LABEL) + 65 > MAX_MESSAGE_BYTES:
        raise TransportError("transport message exceeds byte limit")
    return hashed_message + DIGEST_LABEL + sha256_bytes(hashed_message).encode("ascii") + b"\n"


def render_cell(cell_path: Path) -> bytes:
    return render_members(read_cell(cell_path))


class _Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def exact(self, expected: bytes, label: str) -> None:
        end = self.offset + len(expected)
        if self.data[self.offset:end] != expected:
            raise TransportError(f"invalid {label} at byte offset {self.offset}")
        self.offset = end

    def line(self, label: str) -> bytes:
        end = self.data.find(b"\n", self.offset)
        if end < 0:
            raise TransportError(f"unterminated {label}")
        value = self.data[self.offset:end]
        self.offset = end + 1
        return value

    def bytes(self, length: int, label: str) -> bytes:
        end = self.offset + length
        if length < 0 or end > len(self.data):
            raise TransportError(f"truncated {label}")
        value = self.data[self.offset:end]
        self.offset = end
        return value


def _decimal(value: bytes, label: str, maximum: int) -> int:
    if not value or not value.isdigit() or (len(value) > 1 and value.startswith(b"0")):
        raise TransportError(f"invalid {label}")
    number = int(value)
    if number > maximum:
        raise TransportError(f"{label} exceeds limit")
    return number


def parse_message(message: bytes) -> tuple[dict[str, bytes], str]:
    """Verify framing, all embedded member hashes, and the complete prefix hash."""
    if len(message) > MAX_MESSAGE_BYTES:
        raise TransportError("transport message exceeds byte limit")
    try:
        message.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise TransportError("transport message is not UTF-8") from exc
    if not message.endswith(b"\n"):
        raise TransportError("transport message must end with LF")

    digest_start = message.rfind(b"\n", 0, len(message) - 1) + 1
    digest_line = message[digest_start:-1]
    if not digest_line.startswith(DIGEST_LABEL):
        raise TransportError("transport message lacks final message_sha256")
    expected_message_hash = digest_line[len(DIGEST_LABEL) :]
    if not HASH_RE.fullmatch(expected_message_hash):
        raise TransportError("invalid message_sha256")
    hashed_message = message[:digest_start]
    actual_message_hash = sha256_bytes(hashed_message).encode("ascii")
    if actual_message_hash != expected_message_hash:
        raise TransportError("whole transport message hash mismatch")

    reader = _Reader(hashed_message)
    reader.exact(LAUNCH_SENTENCE, "launch sentence")
    reader.exact(TRANSPORT_START, "transport start delimiter")
    count_line = reader.line("member count")
    if not count_line.startswith(b"member_count: "):
        raise TransportError("transport lacks member_count")
    count = _decimal(count_line[len(b"member_count: ") :], "member_count", MAX_MEMBERS)

    members: dict[str, bytes] = {}
    order: list[str] = []
    total = 0
    for _ in range(count):
        reader.exact(MEMBER_START, "member start delimiter")
        name_line = reader.line("member name")
        if not name_line.startswith(b"name: "):
            raise TransportError("transport member lacks name")
        encoded_name = name_line[len(b"name: ") :]
        try:
            name = json.loads(encoded_name.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TransportError("invalid encoded member name") from exc
        if not isinstance(name, str):
            raise TransportError("member name must be a JSON string")
        canonical_name = json.dumps(name, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if encoded_name != canonical_name:
            raise TransportError("member name is not canonically encoded")
        _validate_name(name)
        if name in members:
            raise TransportError(f"duplicate transport member: {name}")

        length_line = reader.line("member byte length")
        if not length_line.startswith(b"byte_length: "):
            raise TransportError(f"transport member lacks byte_length: {name}")
        length = _decimal(
            length_line[len(b"byte_length: ") :], "member byte_length", MAX_MEMBER_BYTES
        )
        total += length
        if total > MAX_TOTAL_MEMBER_BYTES:
            raise TransportError("transport members exceed total byte limit")

        hash_line = reader.line("member SHA-256")
        if not hash_line.startswith(b"sha256: "):
            raise TransportError(f"transport member lacks sha256: {name}")
        expected_hash = hash_line[len(b"sha256: ") :]
        if not HASH_RE.fullmatch(expected_hash):
            raise TransportError(f"invalid member sha256: {name}")
        reader.exact(b"content:\n", "member content marker")
        data = reader.bytes(length, f"member content: {name}")
        reader.exact(MEMBER_END, "member end delimiter")
        _validate_member_bytes(name, data)
        if sha256_bytes(data).encode("ascii") != expected_hash:
            raise TransportError(f"member hash mismatch: {name}")
        members[name] = data
        order.append(name)

    reader.exact(TRANSPORT_END, "transport end delimiter")
    if reader.offset != len(hashed_message):
        raise TransportError("unexpected bytes after transport end delimiter")
    if order != canonical_member_order(set(members)):
        raise TransportError("transport members are not in canonical order")
    _validate_manifest(members)
    return members, expected_message_hash.decode("ascii")


def verify_against_cell(message: bytes, cell_path: Path) -> tuple[int, str]:
    reconstructed, message_hash = parse_message(message)
    originals = read_cell(cell_path)
    if set(reconstructed) != set(originals):
        raise TransportError("transport/original cell member sets differ")
    for name in canonical_member_order(set(originals)):
        if reconstructed[name] != originals[name]:
            raise TransportError(f"reconstructed/original member bytes differ: {name}")
    return len(reconstructed), message_hash


def _write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise TransportError(f"refusing to overwrite output: {path}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    render = sub.add_parser("render", help="render one sealed cell ZIP as one UTF-8 message")
    render.add_argument("--cell", required=True, type=Path)
    render.add_argument("--output", required=True, type=Path)
    verify = sub.add_parser("verify", help="verify a message against its original cell ZIP")
    verify.add_argument("--message", required=True, type=Path)
    verify.add_argument("--cell", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "render":
            message = render_cell(args.cell)
            _write_new(args.output, message)
            print(f"rendered {len(message)} UTF-8 bytes to {args.output}")
        else:
            message = args.message.read_bytes()
            count, message_hash = verify_against_cell(message, args.cell)
            print(f"verified {count} exact members; message_sha256={message_hash}")
    except (TransportError, OSError, RuntimeError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
