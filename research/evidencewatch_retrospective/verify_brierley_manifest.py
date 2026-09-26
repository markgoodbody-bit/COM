#!/usr/bin/env python3
"""Verify the current frozen Brierley challenge against both pinned owner files.

No network access. Usage:
  python research/evidencewatch_retrospective/verify_brierley_manifest.py \
    /path/to/abstract_scoring.csv \
    /path/to/all_pairs.tsv \
    research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v2.json
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

EXPECTED_SCHEMA = "evidencewatch-retrospective-major-change-challenge-v2"
EXPECTED_STATUS = "PRE_RUN_FROZEN_SELECTION_NO_EVIDENCEWATCH_OUTPUTS"
MISSING = {"", "NA", "N/A", "NULL"}


def day(value: str) -> int:
    return (datetime.strptime(value, "%d/%m/%Y") - datetime(1970, 1, 1)).days


def usable(value: str | None) -> bool:
    text = str(value or "").strip()
    return bool(text) and text.upper() not in MISSING and "\ufffd" not in text


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="cp1252") as handle:
        rows = list(csv.DictReader(handle))
    out = []
    for row_number, row in enumerate(rows, start=2):
        try:
            highest = int(float(row["Highest_change"]))
            posted_day = day(row["posted_date"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append(
            {
                "source_row": row_number,
                "preprint_doi": str(row["doi"] or "").strip(),
                "published_doi": str(row["published_doi.x"] or "").strip(),
                "posted_date": row["posted_date"],
                "posted_day": posted_day,
                "covid": row["covid_preprint"] == "TRUE",
                "highest_change": highest,
            }
        )
    return out


def load_reconstructable_pairs(path: Path) -> set[tuple[str, str]]:
    by_key: dict[tuple[str, str], list[dict]] = defaultdict(list)
    with path.open(newline="", encoding="cp1252", errors="replace") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            doi = str(row.get("doi") or "").strip()
            published_doi = str(row.get("published_doi") or "").strip()
            if not doi or not published_doi:
                continue
            by_key[(doi, published_doi)].append(row)

    reconstructable: set[tuple[str, str]] = set()
    for key, rows in by_key.items():
        for row in rows:
            if usable(row.get("abstract")) and usable(row.get("published_pubmed_abstract")):
                reconstructable.add(key)
                break
    return reconstructable


def expected_pairs(rows: list[dict], reconstructable: set[tuple[str, str]]) -> list[dict]:
    positives = sorted(
        (r for r in rows if r["highest_change"] >= 2),
        key=lambda r: (r["posted_day"], r["preprint_doi"]),
    )
    unreconstructable_positive = [
        r["preprint_doi"]
        for r in positives
        if (r["preprint_doi"], r["published_doi"]) not in reconstructable
    ]
    if unreconstructable_positive:
        raise AssertionError(
            "Owner-labelled major-change rows are not reconstructable: "
            + ", ".join(unreconstructable_positive)
        )

    controls = [
        r
        for r in rows
        if r["highest_change"] == 0
        and (r["preprint_doi"], r["published_doi"]) in reconstructable
    ]

    used: set[str] = set()
    result = []
    for positive in positives:
        candidates = [
            dict(control, delta_days=abs(control["posted_day"] - positive["posted_day"]))
            for control in controls
            if control["covid"] == positive["covid"]
            and control["preprint_doi"] not in used
        ]
        if not candidates:
            raise AssertionError(f"No eligible reconstructable control for {positive['preprint_doi']}")
        candidates.sort(key=lambda r: (r["delta_days"], r["preprint_doi"]))
        control = candidates[0]
        used.add(control["preprint_doi"])
        result.append(
            {
                "positive_doi": positive["preprint_doi"],
                "control_doi": control["preprint_doi"],
                "delta_days": control["delta_days"],
            }
        )
    return result


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    scoring_path = Path(sys.argv[1])
    all_pairs_path = Path(sys.argv[2])
    manifest_path = Path(sys.argv[3])

    rows = load_rows(scoring_path)
    reconstructable = load_reconstructable_pairs(all_pairs_path)
    expected = expected_pairs(rows, reconstructable)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    observed = [
        {
            "positive_doi": episode["positive"]["preprint_doi"],
            "control_doi": episode["control"]["preprint_doi"],
            "delta_days": episode["matched_posting_date_gap_days"],
        }
        for episode in manifest["episodes"]
    ]

    assert manifest["schema"] == EXPECTED_SCHEMA, manifest["schema"]
    assert manifest["status"] == EXPECTED_STATUS, manifest["status"]
    assert len(expected) == 22, len(expected)
    assert observed == expected
    assert manifest["selection"]["positives"] == 22
    assert manifest["selection"]["controls"] == 22
    assert manifest["selection"]["positive_covid"] == 15
    assert manifest["selection"]["positive_non_covid"] == 7
    assert manifest["selection"]["reconstructable_text_required"] is True
    assert manifest["selection"]["max_control_date_gap_days"] == max(
        pair["delta_days"] for pair in expected
    )
    sorted_gaps = sorted(pair["delta_days"] for pair in expected)
    assert manifest["selection"]["median_control_date_gap_days"] == sorted_gaps[len(sorted_gaps) // 2]

    print("PASS")
    print(f"positives={len(expected)} controls={len(observed)}")
    print(
        "max_gap_days="
        f"{manifest['selection']['max_control_date_gap_days']} "
        "median_gap_days="
        f"{manifest['selection']['median_control_date_gap_days']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
