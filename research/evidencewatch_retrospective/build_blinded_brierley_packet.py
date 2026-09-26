#!/usr/bin/env python3
"""Build a blinded execution packet for the frozen Brierley challenge.

Offline only.

Usage:
  python research/evidencewatch_retrospective/build_blinded_brierley_packet.py \
    /path/to/all_pairs.tsv \
    research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v1.json \
    /tmp/evidencewatch_brierley_packet.json \
    /tmp/evidencewatch_brierley_key.json
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

BLIND_SALT = "evidencewatch-brierley-blind-v1"
EXPECTED_CASES = 44


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean_text(value: str) -> str:
    return " ".join(str(value or "").split())


def load_all_pairs(path: Path) -> dict[str, dict]:
    with path.open(newline="", encoding="cp1252") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows: dict[str, dict] = {}
        for row in reader:
            doi = str(row.get("doi") or "").strip()
            if not doi:
                continue
            if doi in rows:
                raise AssertionError(f"Duplicate preprint DOI in all_pairs.tsv: {doi}")
            rows[doi] = row
    return rows


def selected_cases(manifest: dict) -> list[dict]:
    out = []
    seen = set()
    for episode in manifest["episodes"]:
        for role in ("positive", "control"):
            record = episode[role]
            doi = record["preprint_doi"]
            if doi in seen:
                raise AssertionError(f"Duplicate selected preprint DOI: {doi}")
            seen.add(doi)
            out.append(
                {
                    "pair_id": episode["pair_id"],
                    "role": role,
                    "owner_label": record["owner_label"],
                    "source_row": record["source_row"],
                    "preprint_doi": doi,
                    "published_doi": record["published_doi"],
                }
            )
    if len(out) != EXPECTED_CASES:
        raise AssertionError(f"Expected {EXPECTED_CASES} selected cases, got {len(out)}")
    return out


def blind_rank(doi: str) -> str:
    return sha256_hex(f"{BLIND_SALT}\n{doi}".encode("utf-8"))


def build(manifest: dict, all_pairs: dict[str, dict]) -> tuple[dict, dict]:
    selected = selected_cases(manifest)
    selected.sort(key=lambda item: (blind_rank(item["preprint_doi"]), item["preprint_doi"]))

    packet_cases = []
    key_cases = []

    for index, selected_case in enumerate(selected, start=1):
        doi = selected_case["preprint_doi"]
        row = all_pairs.get(doi)
        if row is None:
            raise AssertionError(f"Selected DOI missing from all_pairs.tsv: {doi}")

        row_published_doi = str(row.get("published_doi") or "").strip()
        if row_published_doi != selected_case["published_doi"]:
            raise AssertionError(
                f"Published DOI mismatch for {doi}: "
                f"manifest={selected_case['published_doi']} source={row_published_doi}"
            )

        preprint = clean_text(row.get("abstract"))
        published = clean_text(row.get("published_pubmed_abstract"))
        if not preprint:
            raise AssertionError(f"Missing preprint abstract for {doi}")
        if not published:
            raise AssertionError(f"Missing published abstract for {doi}")

        case_id = f"case-{index:03d}"
        packet_cases.append(
            {
                "case_id": case_id,
                "preprint_abstract": preprint,
                "published_abstract": published,
            }
        )
        key_cases.append(
            {
                "case_id": case_id,
                "blind_rank_sha256": blind_rank(doi),
                **selected_case,
            }
        )

    packet = {
        "schema": "evidencewatch-brierley-blinded-packet-v1",
        "status": "BLINDED_INPUT_NO_OWNER_LABELS",
        "source": {
            "repository": manifest["source"]["repository"],
            "repository_commit": manifest["source"]["repository_commit"],
            "all_pairs_path": manifest["source"]["all_pairs_path"],
            "all_pairs_git_blob": manifest["source"]["all_pairs_git_blob"],
        },
        "case_count": len(packet_cases),
        "cases": packet_cases,
    }

    key = {
        "schema": "evidencewatch-brierley-blinded-key-v1",
        "status": "KEEP_SEPARATE_FROM_ANALYSIS_PATH_UNTIL_UNBLINDING",
        "blind_salt": BLIND_SALT,
        "manifest_schema": manifest["schema"],
        "manifest_status": manifest["status"],
        "case_count": len(key_cases),
        "cases": key_cases,
    }
    return packet, key


def write_json(path: Path, value: object) -> str:
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    path.write_text(rendered, encoding="utf-8")
    return sha256_hex(rendered.encode("utf-8"))


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    all_pairs_path = Path(sys.argv[1])
    manifest_path = Path(sys.argv[2])
    packet_path = Path(sys.argv[3])
    key_path = Path(sys.argv[4])

    if packet_path.resolve() == key_path.resolve():
        raise AssertionError("Packet and key outputs must be different files")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["status"] != "PRE_RUN_FROZEN_SELECTION_NO_EVIDENCEWATCH_OUTPUTS":
        raise AssertionError(f"Unexpected manifest status: {manifest['status']}")

    all_pairs = load_all_pairs(all_pairs_path)
    packet, key = build(manifest, all_pairs)

    # The analysis packet must not contain labels, source roles, DOI identifiers,
    # source rows, or the blind salt.
    packet_serialized = json.dumps(packet, ensure_ascii=False)
    forbidden = [
        "ABSTRACT_MAJOR_CHANGE",
        "ABSTRACT_NO_CHANGE",
        '"role"',
        '"preprint_doi"',
        '"published_doi"',
        '"source_row"',
        BLIND_SALT,
    ]
    for token in forbidden:
        if token in packet_serialized:
            raise AssertionError(f"Blinding leak in packet: {token}")

    packet_sha = write_json(packet_path, packet)
    key_sha = write_json(key_path, key)

    print("PASS")
    print(f"cases={packet['case_count']}")
    print(f"packet_sha256={packet_sha}")
    print(f"key_sha256={key_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
