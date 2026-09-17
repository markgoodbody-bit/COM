#!/usr/bin/env python3
"""Version-aware ATRS public-disclosure parser.

This module parses the published GOV.UK ATRS record, preserving exact source
identity and known heading-family differences. It reports observable disclosure
only; it does not infer compliance, legal rights, remedy effectiveness, or
undisclosed practice.
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
USER_AGENT = "framework-atrs-answerability-audit/0.6 (public research)"
PREFIX = r"^(?:\d+(?:\.\d+)*\s*[-.]?\s*)?"

FIELD_PATTERNS = {
    "human_review": (
        PREFIX + r"human review$",
        PREFIX + r"human decisions and review$",
        PREFIX + r"human decisions?$",  # 2024 family
    ),
    "appeals_review": (PREFIX + r"appeals? and review$",),
    "model_performance": (PREFIX + r"model performance$",),
    "risks": (
        PREFIX + r"risks?$",
        PREFIX + r"risks and mitigations$",
        PREFIX + r"risk (?:name|description|mitigation)$",  # 2024 family
    ),
    "impact_assessment": (
        PREFIX + r"impact assessment$",
        PREFIX + r"impact assessments$",
        PREFIX + r"impact assessment (?:name|description|date|link)$",  # 2024 family
    ),
    "maintenance": (PREFIX + r"maintenance$",),
    "senior_responsible_owner": (PREFIX + r"senior responsible owner$",),
}

LEGACY_2024_MARKERS = (
    PREFIX + r"human decisions?$",
    PREFIX + r"impact assessment name$",
    PREFIX + r"risk name$",
)
CURRENT_MARKERS = (
    PREFIX + r"human review$",
    PREFIX + r"human decisions and review$",
    PREFIX + r"risks and mitigations$",
    PREFIX + r"impact assessments?$",
    PREFIX + r"model performance$",
)

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
        self.sections.append(Section(
            self.current_level,
            self.current_heading,
            re.sub(r"\s+", " ", " ".join(self.current_text)).strip(),
            list(dict.fromkeys(self.current_hrefs)),
        ))
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


def heading_profile(sections: list[Section]) -> str:
    headings = [normalize_heading(s.heading) for s in sections if not normalize_heading(s.heading).startswith("tier ")]
    legacy = any(any(re.fullmatch(p, h, re.I) for p in LEGACY_2024_MARKERS) for h in headings)
    current = any(any(re.fullmatch(p, h, re.I) for p in CURRENT_MARKERS) for h in headings)
    if legacy and current:
        return "mixed_known_families"
    if legacy:
        return "legacy_2024_family"
    if current:
        return "current_named_family"
    return "unclassified_heading_family"


def field_family_context(profile: str, field_name: str) -> str:
    if profile == "legacy_2024_family" and field_name == "model_performance":
        return "not_present_in_known_legacy_2024_family"
    return "no_template_requirement_inferred"


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
    value = html.unescape(TAG_RE.sub(" ", match.group(1)))
    return re.sub(r"\s+", " ", value).strip() or fallback


def contact_tokens(section: Section) -> dict[str, Any]:
    urls = list(dict.fromkeys(URL_RE.findall(section.text)))
    emails = list(dict.fromkeys(EMAIL_RE.findall(section.text)))
    phones = list(dict.fromkeys(PHONE_RE.findall(section.text)))
    return {
        "hrefs": section.hrefs,
        "urls_in_text": urls,
        "emails": emails,
        "phones": phones,
        "syntactic_contact_token_present": bool(section.hrefs or urls or emails or phones),
    }


def section_observation(section: Section) -> dict[str, Any]:
    return {
        "level": section.level,
        "heading": section.heading,
        "text": section.text,
        "characters": len(section.text),
        "contains_none_or_na_phrase": any(re.search(p, section.text, re.I) for p in NONE_PHRASE_PATTERNS),
        "contact_tokens": contact_tokens(section),
    }


def classify_matches(matches: list[Section], *, profile: str, field_name: str) -> dict[str, Any]:
    obs = [section_observation(s) for s in matches]
    return {
        "section_present": bool(matches),
        "match_count": len(matches),
        "heading_family_context": field_family_context(profile, field_name),
        "contains_none_or_na_phrase": any(o["contains_none_or_na_phrase"] for o in obs),
        "syntactic_contact_token_present": any(o["contact_tokens"]["syntactic_contact_token_present"] for o in obs),
        "matches": obs,
    }


def audit_page(url: str, page_bytes: bytes, *, fetched_at_utc: str | None = None) -> dict[str, Any]:
    page_html = decode_page(page_bytes)
    sections = parse_sections(page_html)
    profile = heading_profile(sections)
    fields = {
        name: classify_matches(find_sections(sections, patterns), profile=profile, field_name=name)
        for name, patterns in FIELD_PATTERNS.items()
    }
    return {
        "title": page_title(page_html, url.rsplit("/", 1)[-1]),
        "url": url,
        "source_sha256": hashlib.sha256(page_bytes).hexdigest(),
        "fetched_at_utc": fetched_at_utc or datetime.now(timezone.utc).isoformat(),
        "source_bytes": len(page_bytes),
        "heading_profile": profile,
        "section_count": len(sections),
        "fields": fields,
    }


def summarise(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "records": len(rows),
        "heading_profiles": dict(sorted(__import__('collections').Counter(r.get("heading_profile", "unknown") for r in rows).items())),
        "fields": {},
    }
    for name in FIELD_PATTERNS:
        vals = [r["fields"][name] for r in rows]
        legacy_not_in_family = sum(v.get("heading_family_context") == "not_present_in_known_legacy_2024_family" for v in vals)
        summary["fields"][name] = {
            "section_present": sum(bool(v["section_present"]) for v in vals),
            "section_not_observed": sum(not bool(v["section_present"]) for v in vals),
            "known_family_without_field": legacy_not_in_family,
            "records_with_multiple_matches": sum(v["match_count"] > 1 for v in vals),
            "contains_none_or_na_phrase": sum(bool(v["contains_none_or_na_phrase"]) for v in vals),
            "syntactic_contact_token_present": sum(bool(v["syntactic_contact_token_present"]) for v in vals),
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
    if membership["declared_count"] != len(membership["urls"]):
        raise RuntimeError("finder declared/enumerated membership mismatch")
    return membership["urls"]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = ["title", "url", "source_sha256", "fetched_at_utc", "heading_profile", "section_count"]
    for field in FIELD_PATTERNS:
        names += [f"{field}_present", f"{field}_match_count", f"{field}_family_context", f"{field}_none_phrase", f"{field}_contact_token"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names)
        writer.writeheader()
        for row in rows:
            flat = {k: row.get(k) for k in names if k in row}
            for field in FIELD_PATTERNS:
                value = row["fields"][field]
                flat[f"{field}_present"] = value["section_present"]
                flat[f"{field}_match_count"] = value["match_count"]
                flat[f"{field}_family_context"] = value["heading_family_context"]
                flat[f"{field}_none_phrase"] = value["contains_none_or_na_phrase"]
                flat[f"{field}_contact_token"] = value["syntactic_contact_token_present"]
            writer.writerow(flat)


def build_report(rows: list[dict[str, Any]], *, status: str = "OBSERVED_PUBLIC_DISCLOSURE_SYNTAX_NOT_QUALITY_SCORE") -> dict[str, Any]:
    return {
        "status": status,
        "membership_authority": "current public GOV.UK ATRS finder",
        "source": "GOV.UK Algorithmic Transparency Recording Standard records",
        "source_licence": "Open Government Licence v3.0",
        "records": rows,
        "summary": summarise(rows),
        "ceilings": [
            "SECTION_PRESENT != PRACTICALLY_EFFECTIVE_REMEDY",
            "SYNTACTIC_CONTACT_TOKEN_PRESENT != RELEVANT_APPEAL_ROUTE",
            "CONTAINS_NONE_OR_NA_PHRASE != FIELD_IS_INAPPLICABLE",
            "HEADING_FAMILY != COMPLIANCE_STATUS",
            "FIELD_NOT_OBSERVED != REQUIRED_FIELD_OMITTED",
            "DISCLOSURE_ABSENT != PRACTICE_ABSENT",
            "ATRS_RECORD != COMPLETE_SYSTEM_REALITY",
            "PUBLIC_RECORD_AUDIT != POLICY_VERDICT",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--csv-out", type=Path)
    parser.add_argument("--html-dir", type=Path)
    args = parser.parse_args()
    urls = finder_urls()
    if args.limit is not None:
        urls = urls[:args.limit]
    if args.html_dir:
        args.html_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for url in urls:
        fetched_at = datetime.now(timezone.utc).isoformat()
        page_bytes = request_bytes(url)
        row = audit_page(url, page_bytes, fetched_at_utc=fetched_at)
        if args.html_dir:
            name = f"{row['source_sha256']}.html"
            (args.html_dir / name).write_bytes(page_bytes)
            row["source_snapshot"] = name
        rows.append(row)
    report = build_report(rows)
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
