#!/usr/bin/env python3
"""Structural checks for the unpublished Door visual candidate.

These checks do not establish reader benefit, visual quality or accessibility conformance.
They only make a few meaning-bearing survival properties explicit while presentation changes.
"""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "style.css").read_text(encoding="utf-8")


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.hrefs = []
        self.ids = []
        self.alternates = []
        self.scripts = 0
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "script":
            self.scripts += 1
        if tag == "h1":
            self.h1 += 1
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"])
        if tag == "link" and values.get("rel") == "alternate":
            self.alternates.append((values.get("type"), values.get("href")))

    def handle_data(self, data):
        value = " ".join(data.split())
        if value:
            self.text.append(value)


scan = Scan()
scan.feed(HTML)
text = " ".join(scan.text)

assert scan.scripts == 0, "visual candidate must not depend on JavaScript"
assert scan.h1 == 1, "root should keep one primary heading"

movements = ["situation", "possibility", "challenge", "source", "curiosity"]
positions = [scan.ids.index(item) for item in movements]
assert positions == sorted(positions), "first movements changed order"

assert ("text/plain", "https://pleasestartfromhere.com/llms.txt") in scan.alternates
assert ("application/json", "https://pleasestartfromhere.com/explore/start.json") in scan.alternates

all_routes = (
    "https://pleasestartfromhere.com/",
    "https://pleasestartfromhere.com/explore/",
    "https://pleasestartfromhere.com/explore/nodes/futures.html",
    "https://pleasestartfromhere.com/discussion/",
    "https://pleasestartfromhere.com/explore/start.json",
    "https://pleasestartfromhere.com/read/start.html",
    "https://pleasestartfromhere.com/resources/trace/README.md",
    "https://pleasestartfromhere.com/resources/mechanical-ethics/README.md",
)
for url in all_routes:
    assert url in scan.hrefs, f"missing route: {url}"

# These routes are deliberately exposed as literal addresses in the root text.
# Resource links may instead use human labels such as "Introduction and edition status".
literal_routes = (
    "https://pleasestartfromhere.com/",
    "https://pleasestartfromhere.com/explore/",
    "https://pleasestartfromhere.com/explore/nodes/futures.html",
    "https://pleasestartfromhere.com/discussion/",
    "https://pleasestartfromhere.com/explore/start.json",
    "https://pleasestartfromhere.com/read/start.html",
)
for url in literal_routes:
    assert url in text, f"literal route is no longer visible in stripped text: {url}"

for phrase in (
    "How can we make a better future?",
    "Start from whatever brought you here.",
    "You can hand this address to an AI.",
    "No special prompt is required.",
    "An AI answer is another perspective, not authority.",
    "This on-site discussion is read-only; it does not receive replies yet.",
    "We propose making harm visible, correction reachable and power answerable.",
    "You may disagree, use another method, or leave.",
    "Reading implies no adoption, obligation or consent.",
    "Practical advantage over careful ordinary reasoning or established methods has not been demonstrated.",
    "Neither is an independent assessment.",
    "repository status and licence notices remain authoritative for their own material.",
    "Visual candidate based on Preview 0.8 · not the public edition.",
):
    assert phrase in text, f"meaning-bearing phrase lost: {phrase}"

lower_css = CSS.lower()
assert "@import" not in lower_css, "no external CSS import"
assert "url(" not in lower_css, "candidate decoration should not fetch assets"
assert "animation:" not in lower_css and "@keyframes" not in lower_css, "no motion dependency"
assert ":focus-visible" in CSS
assert "prefers-color-scheme: dark" in CSS
assert "@media (max-width: 52rem)" in CSS
assert "@media print" in CSS

print("VISUAL_CANDIDATE_STRUCTURAL_PASS")
print("No reader-benefit or accessibility-conformance claim follows from this check.")
