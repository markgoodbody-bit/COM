#!/usr/bin/env python3
"""Bounded station-lift metadata consistency checker.

Checks existence/currentness contradictions only. It does not certify step-free
route availability or advise whether a passenger can travel.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "cases.json"

NO_LIFTS_PATTERNS = [re.compile(r"\bthere are no lifts\b", re.I)]
HAS_LIFTS_PATTERNS = [
    re.compile(r"\bthere are lifts\b", re.I),
    re.compile(r"\blifts? (?:have|has) (?:now )?been installed\b", re.I),
    re.compile(r"\blift access available\b", re.I),
    re.compile(r"\bnew (?:passenger )?lifts?\b", re.I),
    re.compile(r"\blift \d+\b", re.I),
]
OUT_PATTERNS = [
    re.compile(r"\blifts? (?:are|is) out of order\b", re.I),
    re.compile(r"\bstatus:\s*out of service\b", re.I),
]
IN_PATTERNS = [
    re.compile(r"\bstatus:\s*in service\b", re.I),
    re.compile(r"\blift is currently available\b", re.I),
]


@dataclass(frozen=True)
class Audit:
    crs: str
    name: str
    result: str
    summary_state: str
    corroborating_existence: bool
    operational: str
    note: str


def strip_markup(raw: str) -> str:
    raw = re.sub(r"<script\b[^>]*>.*?</script>", " ", raw, flags=re.I | re.S)
    raw = re.sub(r"<style\b[^>]*>.*?</style>", " ", raw, flags=re.I | re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    return re.sub(r"\s+", " ", raw).strip()


def fetch_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "bounded-accessibility-currentness-check/0.1"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return strip_markup(response.read().decode("utf-8", errors="replace"))


def summary_state(text: str) -> str:
    if any(p.search(text) for p in NO_LIFTS_PATTERNS):
        return "NO_LIFTS"
    if any(p.search(text) for p in HAS_LIFTS_PATTERNS):
        return "LIFTS_EXIST"
    return "UNKNOWN"


def existence_signal(text: str) -> bool:
    return any(p.search(text) for p in HAS_LIFTS_PATTERNS) or bool(
        re.search(r"\bthe lifts? (?:are|is) out of order\b", text, re.I)
    )


def operational_state(text: Optional[str]) -> str:
    if not text:
        return "NOT_CHECKED"
    if any(p.search(text) for p in OUT_PATTERNS):
        return "OUT_OF_SERVICE"
    if any(p.search(text) for p in IN_PATTERNS):
        return "IN_SERVICE"
    return "UNKNOWN"


def classify(name: str, crs: str, summary_text: str, other_texts: list[str], op_text: Optional[str]) -> Audit:
    ss = summary_state(summary_text)
    exists = any(existence_signal(t) for t in other_texts)
    op = operational_state(op_text)

    if ss == "NO_LIFTS" and exists:
        result = "CONTRADICTION"
        note = "Public summary says no lifts exist while another current owner surface indicates lifts exist."
    elif ss == "LIFTS_EXIST" and exists:
        result = "CONSISTENT_EXISTS"
        note = "Summary and at least one other owner surface agree that lifts exist."
    else:
        result = "NO_EXISTENCE_COMPARISON"
        note = "Checked public text does not provide both sides of an existence comparison."

    return Audit(crs, name, result, ss, exists, op, note)


def load_cases() -> dict:
    return json.loads(CASES.read_text(encoding="utf-8"))


def frozen_audits(data: dict) -> list[Audit]:
    out = []
    for station in data["stations"]:
        others = [s["observed"] for s in station["corroborating_surfaces"] if s.get("observed")]
        out.append(
            classify(
                station["name"],
                station["crs"],
                station["summary"]["observed"],
                others,
                station.get("operational", {}).get("observed"),
            )
        )
    return out


def live_audits(data: dict) -> list[Audit]:
    out = []
    for station in data["stations"]:
        try:
            summary = fetch_text(station["summary"]["url"])
            others = []
            for source in station["corroborating_surfaces"]:
                try:
                    others.append(fetch_text(source["url"]))
                except Exception as exc:
                    others.append(f"FETCH_FAILED {exc}")
            op_text = " ".join([summary] + others)
            out.append(classify(station["name"], station["crs"], summary, others, op_text))
        except Exception as exc:
            out.append(
                Audit(
                    station["crs"],
                    station["name"],
                    "FETCH_UNKNOWN",
                    "UNKNOWN",
                    False,
                    "UNKNOWN",
                    f"Summary fetch failed: {exc}",
                )
            )
    return out


def print_table(audits: list[Audit]) -> None:
    print("CRS\tSTATION\tRESULT\tSUMMARY\tOTHER_EXISTS\tOPERATIONAL")
    for audit in audits:
        print(
            f"{audit.crs}\t{audit.name}\t{audit.result}\t{audit.summary_state}\t"
            f"{str(audit.corroborating_existence).lower()}\t{audit.operational}"
        )
        print(f"  {audit.note}")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--frozen", action="store_true")
    mode.add_argument("--live", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    data = load_cases()
    audits = frozen_audits(data) if args.frozen else live_audits(data)

    if args.json:
        print(json.dumps([asdict(a) for a in audits], indent=2))
    else:
        print_table(audits)

    if args.frozen:
        expected = {s["crs"]: s["expected"] for s in data["stations"]}
        wrong = [a for a in audits if expected[a.crs] != a.result]
        if wrong:
            for audit in wrong:
                print(
                    f"EXPECTED_MISMATCH {audit.crs}: expected {expected[audit.crs]}, got {audit.result}",
                    file=sys.stderr,
                )
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
