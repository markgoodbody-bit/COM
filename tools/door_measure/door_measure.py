#!/usr/bin/env python3
"""Measure a published static page, the same way twice.

Three questions this answers mechanically, so the next version of each is
settled by a re-run rather than by argument:

    moved   did a given sentence move between published versions?
    links   does every destination on the page actually resolve?
    open    how much of the opening tells a reader what the page ISN'T?

WHY THIS EXISTS. On 2026-09-08 I published, twice, that a sentence on the
project door had moved -- once as a regression, once as a repair, crediting
another aperture for closing it. FRAMEWORK objected that a raw-byte offset in
HTML and a rendered-character offset in stripped text cannot be compared. That
was right, and testing it was worse than the objection: measured with one
instrument across all twelve published versions, the sentence had not moved
since 11:29Z and did not exist at all before 10:06Z. Neither number looked
wrong on its own. The error lived entirely in the comparison.

    TWO_MEASUREMENTS != A_COMPARISON
    THE_NUMBER_IMPROVED != SOMETHING_WAS_REPAIRED

The figures from the first claim matched no published version, because the
instrument was not saved and could not be re-run. Hence this file.

Usage:
    python door_measure.py moved --repo OWNER/NAME --needle "harm visible"
    python door_measure.py links --url https://example.org/
    python door_measure.py open  --url https://example.org/ --window 1500
"""
import argparse
import base64
import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "door-measure"}


def rendered(raw_bytes):
    """Reader-visible text. Tags stripped only AFTER script/style removal, so
    stylesheet and script bodies never count as things a reader met."""
    text = raw_bytes.decode("utf-8", "replace")
    body = re.search(r"(?is)<body[^>]*>(.*)</body>", text)
    inner = body.group(1) if body else text
    inner = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", inner)
    flat = re.sub(r"(?s)<[^>]+>", " ", inner)
    return html.unescape(re.sub(r"\s+", " ", flat)).strip(), inner


def gh_json(path):
    r = subprocess.run(["gh", "api", path], capture_output=True,
                       encoding="utf-8", errors="replace")
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def cmd_moved(a):
    commits = gh_json("repos/%s/commits?sha=%s&per_page=%d"
                      % (a.repo, a.branch, a.limit)) or []
    if not commits:
        sys.exit("no commits from repos/%s (branch %s)" % (a.repo, a.branch))
    commits = list(reversed(commits))

    print("needle: %r    file: %s    %s@%s"
          % (a.needle, a.path, a.repo, a.branch))
    print("\n%-10s %-17s %8s %8s | %9s %6s | %9s %6s"
          % ("commit", "authored", "htmlB", "rendC",
             "byte_off", "%html", "char_off", "%text"))

    rows = []
    for c in commits:
        sha = c["sha"]
        blob = gh_json("repos/%s/contents/%s?ref=%s"
                       % (a.repo, urllib.parse.quote(a.path), sha))
        if not blob or "content" not in blob:
            print("%-10s %-17s  (no %s at this ref)" % (sha[:8], c["commit"]["author"]["date"][5:19], a.path))
            continue
        raw = base64.b64decode(blob["content"])
        vis, _ = rendered(raw)
        b = raw.find(a.needle.encode())
        ch = vis.find(a.needle)
        rows.append((sha[:8], b, ch))
        print("%-10s %-17s %8d %8d | %9s %5s%% | %9s %5s%%"
              % (sha[:8], c["commit"]["author"]["date"][5:19], len(raw), len(vis),
                 b if b >= 0 else "absent",
                 ("%.0f" % (100.0 * b / len(raw))) if b >= 0 else "-",
                 ch if ch >= 0 else "absent",
                 ("%.0f" % (100.0 * ch / len(vis))) if ch >= 0 else "-"))

    present = [r for r in rows if r[1] >= 0]
    print()
    if not present:
        print("VERDICT: the needle appears in no version. Nothing moved; it was never there.")
        return
    first = present[0]
    byte_vals = {r[1] for r in present}
    char_vals = {r[2] for r in present}
    if len(present) < len(rows):
        print("The needle is ABSENT before %s -- any claim about it drifting from an" % first[0])
        print("earlier position is about text that had not been written yet.")
    if len(byte_vals) == 1 and len(char_vals) == 1:
        print("VERDICT: it has NOT moved across the versions where it exists "
              "(byte %d, char %d)." % (first[1], first[2]))
    else:
        print("VERDICT: it moved. byte offsets seen: %s"
              % sorted(byte_vals))
    print("Read each column down. Never compare a byte offset to a char offset.")


def cmd_links(a):
    raw = urllib.request.urlopen(urllib.request.Request(a.url, headers=UA), timeout=25).read()
    _, inner = rendered(raw)
    hrefs = [html.unescape(m.group(1)) for m in
             re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\']', inner)]
    seen, order = set(), []
    for h in hrefs:
        if h.startswith("#"):
            continue
        u = urllib.parse.urljoin(a.url, h)
        if u not in seen:
            seen.add(u)
            order.append(u)
    print("%d unique destinations\n" % len(order))
    bad = []
    for u in order:
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25) as r:
                data = r.read()
                note = "" if r.geturl().rstrip("/") == u.rstrip("/") else "  -> " + r.geturl()
                print("  %-3d %-8d %s%s" % (r.status, len(data), u, note))
        except urllib.error.HTTPError as e:
            print("  %-3d %-8s %s   <-- FAILS" % (e.code, "", u))
            bad.append((e.code, u))
        except Exception as e:
            print("  %-3s %-8s %s   <-- %s" % ("ERR", "", u, type(e).__name__))
            bad.append((type(e).__name__, u))

    anchors = set(re.findall(r'(?is)<a\b[^>]*href\s*=\s*["\']#([^"\']+)["\']', inner))
    ids = set(re.findall(r'(?is)\bid\s*=\s*["\']([^"\']+)["\']', inner))
    missing = sorted(anchors - ids)
    print("\n%d of %d destinations fail" % (len(bad), len(order)))
    for code, u in bad:
        print("  %s  %s" % (code, u))
    # A #ref with no matching id returns 200 and goes nowhere; no status
    # check catches it.
    print("in-page anchors: %d; targets missing: %s" % (len(anchors), missing or "none"))
    sys.exit(1 if (bad or missing) else 0)


LIMIT_CUES = [r"\bnot\b", r"\bno\b", r"\bcannot\b", r"\bnever\b", r"\bwithout\b",
              r"\bnothing\b", r"\bnor\b", r"\bunverified\b", r"\blimits?\b"]


def cmd_open(a):
    raw = urllib.request.urlopen(urllib.request.Request(a.url, headers=UA), timeout=25).read()
    vis, inner = rendered(raw)
    sents = [(m.start(), m.group(0).strip())
             for m in re.finditer(r"[^.?!]*[.?!]+(?:\s|$)|[^.?!]+$", vis)
             if m.group(0).strip()]

    # The census is mechanical: every sentence in the window, none skipped.
    # The classification is a judgement, so every call is printed and can be
    # disputed one at a time. A proportion whose calls are hidden is not a
    # measurement.
    print("rendered %d chars; first %d analysed\n" % (len(vis), a.window))
    lim = sub = limc = subc = 0
    for off, s in sents:
        if off >= a.window:
            break
        is_lim = any(re.search(c, s, re.I) for c in LIMIT_CUES)
        print("%-6d %-9s %s" % (off, "LIMIT" if is_lim else "substance", s[:104]))
        if is_lim:
            lim += 1
            limc += len(s)
        else:
            sub += 1
            subc += len(s)
    tot = lim + sub
    if tot:
        print("\n%d sentences: %d limit / %d substance  (%.0f%% by sentence, %.0f%% by character)"
              % (tot, lim, sub, 100.0 * lim / tot, 100.0 * limc / (limc + subc)))
    print("\nThe classification is the caller's, not a result. Dispute individual calls.")

    heads = []
    for m in re.finditer(r"(?is)<h([1-6])[^>]*>(.*?)</h\1>", inner):
        label = html.unescape(re.sub(r"(?s)<[^>]+>", "", m.group(2))).strip()
        i = vis.find(label[:40])
        if i >= 0:
            heads.append((i, "h" + m.group(1), label[:58]))
    heads.sort()
    print("\nsignposts, and the runs between them:")
    prev = 0
    for i, lvl, label in heads:
        print("  %-4s @%-6d %6d chars since the previous break   %s" % (lvl, i, i - prev, label))
        prev = i
    print("  %-4s @%-6d %6d chars to the end" % ("end", len(vis), len(vis) - prev))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("moved", help="did a sentence move between published versions?")
    m.add_argument("--repo", required=True)
    m.add_argument("--branch", default="gh-pages")
    m.add_argument("--path", default="index.html")
    m.add_argument("--needle", required=True)
    m.add_argument("--limit", type=int, default=30)
    m.set_defaults(func=cmd_moved)

    l = sub.add_parser("links", help="does every destination resolve?")
    l.add_argument("--url", required=True)
    l.set_defaults(func=cmd_links)

    o = sub.add_parser("open", help="how much of the opening states a limit?")
    o.add_argument("--url", required=True)
    o.add_argument("--window", type=int, default=1500)
    o.set_defaults(func=cmd_open)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
