#!/usr/bin/env python3
"""ATRS answerability coverage audit.

Enumerates current UK Algorithmic Transparency Recording Standard records from
the official GOV.UK Search API, fetches the public record pages, and extracts a
small set of answerability-relevant sections.

This deliberately reports observable disclosure properties, not a transparency
or ethics score. GOV.UK public-sector information is reused under the Open
Government Licence v3.0. No code from third-party ATRS harvesters is copied.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

SEARCH_URL = "https://www.gov.uk/api/search.json"
BASE_URL = "https://www.gov.uk"
USER_AGENT = "framework-atrs-answerability-audit/0.1 (public research)"

FIELD_PATTERNS = {
    "human_review": (r"\bhuman (?:decisions and )?review\b", r"\bhuman decisions and review\b"),
    "appeals_review": (r"\bappeals? and review\b",),
    "model_performance": (r"\bmodel performance\b", r"\bperformance metrics?\b"),
    "risks": (r"\brisks?\b",),
    "impact_assessment": (r"\bimpact assessment\b",),
    "maintenance": (r"\bmaintenance\b",),
    "senior_responsible_owner": (r"\bsenior responsible owner\b",),
}

NONE_PATTERNS = (
    r"\bnot applicable\b",
    r"\bn/?a\b",
    r"\bnone\b",
    r"\bno human review\b",
    r"\bno (?:specific )?(?:appeal|complaint|review)\b",
)

PUBLIC_ROUTE_PATTERNS = (
    r"mailto:",
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    r"\bcontact(?: us)?\b",
    r"\bcomplaints? (?:procedure|process|route|page|team)\b",
    r"\breview request\b",
    r"\bappeal(?:s| process| procedure| route)?\b",
    r"\bqueries? (?:line|team|email)\b",
    r"https?://",
)


@dataclass
class Section:
    heading: str
    text: str
    html_fragment: str


class SectionParser(HTMLParser):
    """Extract h2/h3 sections while preserving links as visible href markers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_heading = False
        self.heading_tag: str | None = None
        self.heading_parts: list[str] = []
        self.current_heading: str | None = None
        self.current_text: list[str] = []
        self.current_html: list[str] = []
        self.sections: list[Section] = []
        self.capture = False

    def _flush(self) -> None:
        if self.current_heading is None:
            return
        text = re.sub(r"\s+", " ", " ".join(self.current_text)).strip()
        fragment = " ".join(self.current_html)
        self.sections.append(Section(self.current_heading, text, fragment))
        self.current_text = []
        self.current_html = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"h2", "h3"}:
            self._flush()
            self.in_heading = True
            self.heading_tag = tag
            self.heading_parts = []
            self.capture = False
            return
        if self.current_heading is not None:
            self.capture = True
            if tag == "a":
                href = dict(attrs).get("href")
                if href:
                    self.current_html.append(f'href="{html.escape(href)}"')

    def handle_endtag(self, tag: str) -> None:
        if self.in_heading and tag == self.heading_tag:
            self.current_heading = re.sub(r"\s+", " ", " ".join(self.heading_parts)).strip()
            self.in_heading = False
            self.heading_tag = None
            self.capture = True

    def handle_data(self, data: str) -> None:
        s = data.strip()
        if not s:
            return
        if self.in_heading:
            self.heading_parts.append(s)
        elif self.current_heading is not None and self.capture:
            self.current_text.append(s)
            self.current_html.append(html.escape(s))

    def close(self) -> None:
        super().close()
        self._flush()


def request_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)


def request_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def enumerate_records() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    start = 0
    while True:
        params = {
            "filter_content_store_document_type": "algorithmic_transparency_record",
            "count": 100,
            "start": start,
            "fields": ["title", "link", "description", "public_timestamp", "organisations"],
        }
        payload = request_json(SEARCH_URL + "?" + urllib.parse.urlencode(params, doseq=True))
        for item in payload.get("results", []):
            rows.append({
                "title": item.get("title"),
                "url": BASE_URL + item["link"],
                "description": item.get("description"),
                "published": item.get("public_timestamp"),
                "organisations": [o.get("title") for o in item.get("organisations", []) if o.get("title")],
            })
        start += 100
        if start >= int(payload.get("total", 0)):
            break
        time.sleep(0.2)
    return rows


def parse_sections(page_html: str) -> list[Section]:
    parser = SectionParser()
    parser.feed(page_html)
    parser.close()
    return parser.sections


def find_section(sections: list[Section], patterns: tuple[str, ...]) -> Section | None:
    for section in sections:
        h = section.heading.lower()
        if any(re.search(p, h, flags=re.I) for p in patterns):
            return section
    return None


def classify_section(section: Section | None) -> dict[str, Any]:
    if section is None:
        return {
            "section_present": False,
            "heading": None,
            "characters": 0,
            "states_none_or_not_applicable": False,
            "public_route_locator": False,
        }
    combined = f"{section.text} {section.html_fragment}"
    return {
        "section_present": True,
        "heading": section.heading,
        "characters": len(section.text),
        "states_none_or_not_applicable": any(re.search(p, section.text, flags=re.I) for p in NONE_PATTERNS),
        "public_route_locator": any(re.search(p, combined, flags=re.I) for p in PUBLIC_ROUTE_PATTERNS),
    }


def audit_record(record: dict[str, Any], page_html: str) -> dict[str, Any]:
    sections = parse_sections(page_html)
    fields = {
        name: classify_section(find_section(sections, patterns))
        for name, patterns in FIELD_PATTERNS.items()
    }
    return {**record, "fields": fields, "section_count": len(sections)}


def summarise(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"records": len(rows), "fields": {}}
    for name in FIELD_PATTERNS:
        values = [r["fields"][name] for r in rows]
        summary["fields"][name] = {
            "section_present": sum(v["section_present"] for v in values),
            "states_none_or_not_applicable": sum(v["states_none_or_not_applicable"] for v in values),
            "public_route_locator": sum(v["public_route_locator"] for v in values),
        }
    return summary


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["title", "url", "published", "section_count"]
    for field in FIELD_PATTERNS:
        fieldnames += [f"{field}_present", f"{field}_none_or_na", f"{field}_route_locator"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            flat: dict[str, Any] = {k: row.get(k) for k in ["title", "url", "published", "section_count"]}
            for field in FIELD_PATTERNS:
                v = row["fields"][field]
                flat[f"{field}_present"] = v["section_present"]
                flat[f"{field}_none_or_na"] = v["states_none_or_not_applicable"]
                flat[f"{field}_route_locator"] = v["public_route_locator"]
            writer.writerow(flat)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--csv-out", type=Path)
    parser.add_argument("--delay", type=float, default=0.15)
    args = parser.parse_args()

    records = enumerate_records()
    if args.limit is not None:
        records = records[: args.limit]

    audited: list[dict[str, Any]] = []
    for idx, record in enumerate(records):
        audited.append(audit_record(record, request_text(record["url"])))
        if idx + 1 < len(records):
            time.sleep(args.delay)

    report = {
        "status": "OBSERVED_PUBLIC_DISCLOSURE_COVERAGE_NOT_QUALITY_SCORE",
        "source": "GOV.UK Algorithmic Transparency Recording Standard records",
        "source_licence": "Open Government Licence v3.0",
        "records": audited,
        "summary": summarise(audited),
        "ceilings": [
            "SECTION_PRESENT != PRACTICALLY_EFFECTIVE_REMEDY",
            "ROUTE_LOCATOR_PRESENT != ROUTE_WORKS",
            "DISCLOSURE_ABSENT != PRACTICE_ABSENT",
            "ATRS_RECORD != COMPLETE_SYSTEM_REALITY",
            "PUBLIC_RECORD_AUDIT != POLICY_VERDICT",
        ],
    }
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        print(json.dumps(report["summary"], indent=2))
    if args.csv_out:
        write_csv(args.csv_out, audited)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
