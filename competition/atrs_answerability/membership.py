#!/usr/bin/env python3
"""Compare the public ATRS finder membership with GOV.UK generic Search API pages.

The public finder is the authority for the current visible register. The generic
Search API is useful for discovery but is checked rather than assumed equivalent.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

FINDER_URL = "https://www.gov.uk/algorithmic-transparency-records"
SEARCH_URL = "https://www.gov.uk/api/search.json"
BASE_URL = "https://www.gov.uk"
USER_AGENT = "framework-atrs-membership-audit/0.2 (public research)"

RECORD_HREF = re.compile(
    r'href=["\'](?P<path>/algorithmic-transparency-records/(?P<slug>[^"\'?#/]+))["\']',
    re.I,
)
NON_RECORD_SLUGS = {"email-signup"}
COUNT_PATTERNS = (
    re.compile(r'<h3[^>]*>\s*(\d+)\s+records\s*</h3>', re.I),
    re.compile(r'<h2[^>]*>\s*(\d+)\s+records\s*</h2>', re.I),
)
NEXT_PAGE = re.compile(r'href=["\']([^"\']*\bpage=(\d+)[^"\']*)["\'][^>]*>\s*(?:<[^>]+>\s*)*Next page', re.I)


def request_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def request_json(url: str) -> dict[str, Any]:
    return json.loads(request_text(url))


def parse_finder_page(page_html: str) -> tuple[list[str], int | None, int | None]:
    urls: list[str] = []
    seen: set[str] = set()
    for match in RECORD_HREF.finditer(page_html):
        slug = html.unescape(match.group("slug"))
        if slug in NON_RECORD_SLUGS:
            continue
        url = BASE_URL + html.unescape(match.group("path"))
        if url not in seen:
            seen.add(url)
            urls.append(url)
    count = None
    for pattern in COUNT_PATTERNS:
        match = pattern.search(page_html)
        if match:
            count = int(match.group(1))
            break
    next_page = None
    match = NEXT_PAGE.search(page_html)
    if match:
        next_page = int(match.group(2))
    return urls, count, next_page


def enumerate_finder() -> dict[str, Any]:
    all_urls: list[str] = []
    seen: set[str] = set()
    page = 1
    declared_count: int | None = None
    pages: list[dict[str, Any]] = []
    while True:
        url = FINDER_URL if page == 1 else f"{FINDER_URL}?page={page}"
        body = request_text(url)
        urls, count, next_page = parse_finder_page(body)
        if declared_count is None:
            declared_count = count
        elif count != declared_count:
            raise RuntimeError(f"finder count changed during pagination: {declared_count} -> {count}")
        pages.append({"page": page, "url": url, "record_urls": len(urls), "declared_count": count})
        for record_url in urls:
            if record_url not in seen:
                seen.add(record_url)
                all_urls.append(record_url)
        if next_page is None or next_page <= page:
            break
        page = next_page
        if page > 20:
            raise RuntimeError("refusing implausible finder pagination")
    return {"declared_count": declared_count, "urls": all_urls, "pages": pages}


def enumerate_search_api() -> list[str]:
    urls: list[str] = []
    start = 0
    while True:
        params = {
            "filter_content_store_document_type": "algorithmic_transparency_record",
            "count": 100,
            "start": start,
            "fields": ["link"],
        }
        payload = request_json(SEARCH_URL + "?" + urllib.parse.urlencode(params, doseq=True))
        for item in payload.get("results", []):
            link = item.get("link")
            if link:
                urls.append(BASE_URL + link)
        start += 100
        if start >= int(payload.get("total", 0)):
            break
    return list(dict.fromkeys(urls))


def compare_membership() -> dict[str, Any]:
    finder = enumerate_finder()
    search_urls = enumerate_search_api()
    finder_set = set(finder["urls"])
    search_set = set(search_urls)
    return {
        "authority": "live public ATRS finder membership",
        "finder_declared_count": finder["declared_count"],
        "finder_enumerated_count": len(finder_set),
        "search_api_count": len(search_set),
        "finder_pages": finder["pages"],
        "search_api_not_in_finder": sorted(search_set - finder_set),
        "finder_not_in_search_api": sorted(finder_set - search_set),
        "finder_urls": sorted(finder_set),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = compare_membership()
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "finder_urls"}, indent=2))
    if report["finder_declared_count"] != report["finder_enumerated_count"]:
        raise SystemExit("finder declared/enumerated membership mismatch")
    if report["search_api_not_in_finder"] or report["finder_not_in_search_api"]:
        raise SystemExit("finder/Search API membership mismatch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
