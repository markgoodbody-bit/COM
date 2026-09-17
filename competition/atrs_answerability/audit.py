#!/usr/bin/env python3
"""ATRS answerability disclosure audit.

Audits the records currently visible in the official GOV.UK ATRS finder.
The audit preserves source hashes, fetch times, every matching field section,
section text/link destinations, and can retain the exact fetched HTML bytes.

It reports syntactic public-disclosure observables only. It does not score
transparency, compliance, remedy quality, or infer undisclosed practice.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import importlib.util
import json
import re
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
USER_AGENT = "framework-atrs-answerability-audit/0.5 (public research)"

FIELD_PATTERNS = {
    "human_review": (
        r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?human review$",
        r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?human decisions and review$",
    ),
    "appeals_review": (r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?appeals? and review$",),
    "model_performance": (r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?model performance$",),
    "risks": (
        r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?risks$",
        r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?risks and mitigations$",
    ),
    "impact_assessment": (
        r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?impact assessment$",
        r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?impact assessments$",
    ),
    "maintenance": (r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?maintenance$",),
    "senior_responsible_owner": (r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?senior responsible owner$",),
}

# Phrase occurrence only. These do not adjudicate the semantic scope of a
# negation or declare the whole field inapplicable.
NONE_PHRASE_PATTERNS = (
    r"\bnot applicable\b",
    r"\bn/?a\b",
    r"(?:^|[.!?]\s*)none(?:\s*[.!?]|\s*$)",
    r"\bno human review\b",
    r"\bno (?:specific |formal |separate |dedicated |direct )?(?:appeals?|complaints?|reviews?)(?:\s+(?:procedures?|process(?:es)?|routes?))?\b",
)

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+44\s?\d(?:[\s-]?\d){8,10}|0\d{2,4}(?:[\s-]?\d){6,10})(?!\d)")
URL_RE = re.compile(r"https?://[^\s<>'\"\])}]+", re.I)
TAG_RE = re.compile(r"<[^>]+>")
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)


@dataclass
class Section:
    level: str
    heading: str
    text: str
    hrefs: list[str]


class SectionParser(HTMLParser):
    """Extract h2/h3 sections, normally only from the page's <main> element."""

    def __init__(self, *, main_only: bool) -> None:
        super().__init__(convert_charrefs=True)
        self.main_only = main_only
        self.saw_main = False
        self.in_main = not main_only
        self.main_depth = 0
        self.in_heading = False
        self.heading_tag: str | None = None
        self.heading_parts: list[str] = []
        self.current_heading: str | None = None
        self.current_level: str | None = None
        self.current_text: list[str] = []
        self.current_hrefs: list[str] = []
        self.sections: list[Section] = []

    def _flush(self) -> None:
        if self.current_heading is None or self.current_level is None:
            return
        text = re.sub(r"\s+", " ", " ".join(self.current_text)).strip()
        self.sections.append(
            Section(
                level=self.current_level,
                heading=self.current_heading,
                text=text,
                hrefs=list(dict.fromkeys(self.current_hrefs)),
            )
        )
        self.current_heading = None
        self.current_level = None
        self.current_text = []
        self.current_hrefs = []
        self.in_heading = False
        self.heading_tag = None
        self.heading_parts = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "main":
            self.saw_main = True
            self.main_depth += 1
            self.in_main = True
            return
        if self.main_only and not self.in_main:
            return
        if tag in {"h2", "h3"}:
            self._flush()
            self.in_heading = True
            self.heading_tag = tag
            self.heading_parts = []
            return
        if self.current_heading is not None and tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.current_hrefs.append(html.unescape(href))

    def handle_endtag(self, tag: str) -> None:
        if tag == "main" and self.saw_main:
            self._flush()
            self.main_depth = max(0, self.main_depth - 1)
            self.in_main = self.main_depth > 0
            return
        if self.main_only and not self.in_main:
            return
        if self.in_heading and tag == self.heading_tag:
            self.current_heading = re.sub(r"\s+", " ", " ".join(self.heading_parts)).strip()
            self.current_level = tag
            self.in_heading = False
            self.heading_tag = None

    def handle_data(self, data: str) -> None:
        if self.main_only and not self.in_main:
            return
        value = data.strip()
        if not value:
            return
        if self.in_heading:
            self.heading_parts.append(value)
        elif self.current_heading is not None:
            self.current_text.append(value)

    def close(self) -> None:
        super().close()
        self._flush()


def request_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def decode_page(page_bytes: bytes) -> str:
    return page_bytes.decode("utf-8", errors="replace")


def parse_sections(page_html: str) -> list[Section]:
    parser = SectionParser(main_only=True)
    parser.feed(page_html)
    parser.close()
    if parser.saw_main:
        return parser.sections
    fallback = SectionParser(main_only=False)
    fallback.feed(page_html)
    fallback.close()
    return fallback.sections


def normalize_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def find_sections(sections: list[Section], patterns: tuple[str, ...]) -> list[Section]:
    matches: list[Section] = []
    ordered = [s for s in sections if s.level == "h3"] + [s for s in sections if s.level != "h3"]
    for section in ordered:
        heading = normalize_heading(section.heading)
        if heading.startswith("tier "):
            continue
        if any(re.fullmatch(pattern, heading, flags=re.I) for pattern in patterns):
            matches.append(section)
    return matches


def page_title(page_html: str, fallback: str) -> str:
    match = H1_RE.search(page_html)
    if not match:
        return fallback
    text = html.unescape(TAG_RE.sub(" ", match.group(1)))
    return re.sub(r"\s+", " ", text).strip() or fallback


def contact_tokens(section: Section) -> dict[str, Any]:
    urls_in_text = list(dict.fromkeys(URL_RE.findall(section.text)))
    emails = list(dict.fromkeys(EMAIL_RE.findall(section.text)))
    phones = list(dict.fromkeys(PHONE_RE.findall(section.text)))
    return {
        "hrefs": section.hrefs,
        "urls_in_text": urls_in_text,
        "emails": emails,
        "phones": phones,
        "syntactic_contact_token_present": bool(section.hrefs or urls_in_text or emails or phones),
    }


def section_observation(section: Section) -> dict[str, Any]:
    return {
        "level": section.level,
        "heading": section.heading,
        "text": section.text,
        "characters": len(section.text),
        "contains_none_or_na_phrase": any(
            re.search(pattern, section.text, flags=re.I) for pattern in NONE_PHRASE_PATTERNS
        ),
        "contact_tokens": contact_tokens(section),
    }


def classify_matches(matches: list[Section]) -> dict[str, Any]:
    observations = [section_observation(section) for section in matches]
    return {
        "section_present": bool(matches),
        "match_count": len(matches),
        "contains_none_or_na_phrase": any(o["contains_none_or_na_phrase"] for o in observations),
        "syntactic_contact_token_present": any(
            o["contact_tokens"]["syntactic_contact_token_present"] for o in observations
        ),
        "matches": observations,
    }


def audit_page(url: str, page_bytes: bytes, *, fetched_at_utc: str | None = None) -> dict[str, Any]:
    page_html = decode_page(page_bytes)
    sections = parse_sections(page_html)
    fields = {
        name: classify_matches(find_sections(sections, patterns))
        for name, patterns in FIELD_PATTERNS.items()
    }
    return {
        "title": page_title(page_html, url.rsplit("/", 1)[-1]),
        "url": url,
        "source_sha256": hashlib.sha256(page_bytes).hexdigest(),
        "fetched_at_utc": fetched_at_utc or datetime.now(timezone.utc).isoformat(),
        "source_bytes": len(page_bytes),
        "section_count": len(sections),
        "fields": fields,
    }


def summarise(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"records": len(rows), "fields": {}}
    for name in FIELD_PATTERNS:
        values = [row["fields"][name] for row in rows]
        summary["fields"][name] = {
            "section_present": sum(bool(value["section_present"]) for value in values),
            "records_with_multiple_matches": sum(value["match_count"] > 1 for value in values),
            "contains_none_or_na_phrase": sum(bool(value["contains_none_or_na_phrase"]) for value in values),
            "syntactic_contact_token_present": sum(
                bool(value["syntactic_contact_token_present"]) for value in values
            ),
        }
    return summary


def load_membership_module():
    path = ROOT / "membership.py"
    spec = importlib.util.spec_from_file_location("atrs_membership_for_audit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import membership.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def finder_urls() -> list[str]:
    membership = load_membership_module().enumerate_finder()
    declared = membership["declared_count"]
    urls = membership["urls"]
    if declared != len(urls):
        raise RuntimeError(f"finder membership mismatch: declared={declared} enumerated={len(urls)}")
    return urls


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["title", "url", "source_sha256", "fetched_at_utc", "section_count"]
    for field in FIELD_PATTERNS:
        fieldnames += [
            f"{field}_present",
            f"{field}_match_count",
            f"{field}_none_phrase",
            f"{field}_contact_token",
        ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            flat: dict[str, Any] = {key: row.get(key) for key in fieldnames if key in row}
            for field in FIELD_PATTERNS:
                value = row["fields"][field]
                flat[f"{field}_present"] = value["section_present"]
                flat[f"{field}_match_count"] = value["match_count"]
                flat[f"{field}_none_phrase"] = value["contains_none_or_na_phrase"]
                flat[f"{field}_contact_token"] = value["syntactic_contact_token_present"]
            writer.writerow(flat)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--csv-out", type=Path)
    parser.add_argument("--html-dir", type=Path, help="retain exact fetched HTML bytes by SHA-256 filename")
    args = parser.parse_args()

    urls = finder_urls()
    if args.limit is not None:
        urls = urls[: args.limit]

    if args.html_dir:
        args.html_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for url in urls:
        fetched_at = datetime.now(timezone.utc).isoformat()
        page_bytes = request_bytes(url)
        row = audit_page(url, page_bytes, fetched_at_utc=fetched_at)
        if args.html_dir:
            snapshot_name = f"{row['source_sha256']}.html"
            (args.html_dir / snapshot_name).write_bytes(page_bytes)
            row["source_snapshot"] = snapshot_name
        rows.append(row)

    report = {
        "status": "OBSERVED_PUBLIC_DISCLOSURE_SYNTAX_NOT_QUALITY_SCORE",
        "membership_authority": "current public GOV.UK ATRS finder",
        "source": "GOV.UK Algorithmic Transparency Recording Standard records",
        "source_licence": "Open Government Licence v3.0",
        "records": rows,
        "summary": summarise(rows),
        "ceilings": [
            "SECTION_PRESENT != PRACTICALLY_EFFECTIVE_REMEDY",
            "SYNTACTIC_CONTACT_TOKEN_PRESENT != RELEVANT_APPEAL_ROUTE",
            "CONTAINS_NONE_OR_NA_PHRASE != FIELD_IS_INAPPLICABLE",
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
        write_csv(args.csv_out, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
