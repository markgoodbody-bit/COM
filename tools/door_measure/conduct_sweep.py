"""What the door does to a reader's browser, measured -- and what it cannot say.

Written 2026-09-09 after I proposed a front-page claim from a six-route sample,
had it refuted twice in twenty minutes, and was asked for the instrument rather
than the number.

    SAVE_THE_INSTRUMENT_BESIDE_THE_NUMBER

WHAT THIS MEASURES. For each URL given, whether the response contains a script
tag, a script-accessible storage call, a Set-Cookie header, or a load from a
third-party origin. Loads are separated from links: a <a href> to a museum
fetches nothing until a reader clicks it, and an earlier version of this check
conflated the two and nearly killed a true statement.

    A_LINK_IS_NOT_A_LOAD

WHAT THIS CANNOT SAY, and the report prints all four every run:

  1. It is a DISCOVERED surface, not closure. Routes come from llms.txt, the
     manifest, explore/map.json and page hrefs -- what the site advertises, not
     what is deployed. Orphans, aliases, redirects and error pages are outside
     it. CODEX, 2026-09-09: "a set discovered from maps and hrefs is the
     discovered surface, not demonstrated closure."
  2. It says NOTHING about host or CDN log retention. Response headers carry
     per-request identifiers (X-GitHub-Request-Id, X-Fastly-Request-ID); those
     demonstrate identifiers in responses, not whether or how long anything is
     kept. I wrote "a request ID is a record" and that was a step too far --
     enough to refute "your visit is not recorded", not enough to assert
     retention.
  3. "No script" is NOT "nothing is stored in the browser". Ordinary HTTP
     caching stores the response; this door serves Cache-Control: max-age=600.
     The honest scope is SCRIPT-ACCESSIBLE storage.
  4. It is a client-conduct measurement. It establishes nothing about whether
     the door is useful, correct, or good.

THE CONTROL. Every matcher is fired against a synthetic document that must trip
all of them. If any matcher fails to fire there, the sweep refuses a verdict
instead of reporting clean -- a matcher that cannot fail is decoration, and a
clean result from a broken matcher is how a false zero gets published.

    A_POSITIVE_CONTROL_MUST_BE_ABLE_TO_FAIL_THE_SAME_WAY
"""

import re
import sys
import json
import hashlib
import urllib.error
import urllib.parse
import urllib.request

ORIGIN = "https://pleasestartfromhere.com"
OWN = "pleasestartfromhere.com"

# Each matcher returns the offending items it finds. Names are the report's rows.
def m_script(doc, _hd):
    return re.findall(r"<script\b[^>]*>", doc, re.I)

def m_storage(doc, _hd):
    return re.findall(r"\b(?:localStorage|sessionStorage|indexedDB|openDatabase)\b", doc)

def m_cookie(_doc, hd):
    return [v for k, v in hd.items() if k.lower() == "set-cookie"]

def m_third_party_load(doc, _hd):
    found = set()
    found |= set(re.findall(r'\ssrc="https?://([^/"]+)', doc))
    found |= set(re.findall(r'<link[^>]+href="https?://([^/"]+)', doc))
    found |= set(re.findall(r'url\(\s*["\']?https?://([^/"\')]+)', doc))
    found |= set(re.findall(r'@import\s+(?:url\()?["\']?https?://([^/"\')]+)', doc))
    return sorted(d for d in found if OWN not in d)

MATCHERS = [
    ("script tag", m_script),
    ("script-accessible storage", m_storage),
    ("Set-Cookie", m_cookie),
    ("third-party load", m_third_party_load),
]

# Must trip EVERY matcher. If it does not, no verdict is reported.
CONTROL_DOC = (
    '<html><head>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=X">'
    '<style>@import url(https://cdn.example.net/a.css);'
    'body{background:url("https://img.example.org/b.png")}</style>'
    '<script src="https://cdn.example.com/x.js"></script>'
    '</head><body onload="localStorage.setItem(1,2)">'
    '<a href="https://www.metmuseum.org/link-only">a link, not a load</a>'
    '</body></html>'
)
CONTROL_HEADERS = {"Set-Cookie": "a=b; Path=/"}


# A third-party resource can arrive by four mechanisms and the control must
# exercise each SEPARATELY. Tampering found this: a matcher that ignored
# @import and url() still passed a single combined control, because the src=
# case alone satisfied it -- and a web font hiding in a stylesheet is exactly
# the case that would then be missed.
#
#     A_CONTROL_THAT_FIRES_ONCE != A_CONTROL_THAT_TESTS_EACH_MECHANISM
MECHANISMS = [
    ("script src", '<script src="https://cdn.example.com/x.js"></script>', "cdn.example.com"),
    ("link href", '<link rel="stylesheet" href="https://fonts.googleapis.com/c">', "fonts.googleapis.com"),
    ("css url()", '<style>body{background:url("https://img.example.org/b.png")}</style>', "img.example.org"),
    ("css @import", '<style>@import url(https://cdn.example.net/a.css);</style>', "cdn.example.net"),
]


def check_control(matchers=None):
    """-> (ok, rows, link_not_load, mech). Refuse a verdict unless the matchers
    ACTUALLY IN USE fire on every mechanism, and only on loads."""
    matchers = MATCHERS if matchers is None else matchers
    rows, ok = [], True
    for name, fn in matchers:
        hits = fn(CONTROL_DOC, CONTROL_HEADERS)
        rows.append((name, len(hits)))
        if not hits:
            ok = False
    # Take the third-party matcher FROM THE LIST, not from module scope. The
    # first version called m_third_party_load directly, so a swapped-in broken
    # matcher was never the thing being tested -- the check certified a
    # function nobody was using.
    third = dict(matchers).get("third-party load", m_third_party_load)
    mech = []
    for label, doc, host in MECHANISMS:
        found = host in third(doc, {})
        mech.append((label, found))
        if not found:
            ok = False
    # metmuseum.org appears only as an <a href> and must NOT count as a load.
    link_not_load = "www.metmuseum.org" not in third(CONTROL_DOC, CONTROL_HEADERS)
    return ok and link_not_load, rows, link_not_load, mech


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "psfh-conduct-sweep", "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, b"", dict(getattr(e, "headers", {}) or {})
    except Exception as e:                      # loud, never a silent skip
        return type(e).__name__, b"", {}


def discover():
    """Routes the site advertises. NOT closure over what is deployed."""
    routes = {"/", "/llms.txt", "/seed.txt", "/manifest.json",
              "/changes.html", "/explore/", "/style.css", "/robots.txt"}
    def text(p):
        st, b, _ = fetch(ORIGIN + p)
        return b.decode("utf-8", "replace") if st == 200 else ""
    routes |= set(re.findall(r"https://pleasestartfromhere\.com(/[^\s\)\]\"]*)", text("/llms.txt")))
    for p in ("/manifest.json", "/explore/map.json", "/explore/start.json"):
        routes |= set(re.findall(r'"(/[A-Za-z0-9_\-./]+)"', text(p)))
    # Absolute AND relative hrefs. The first version of this function matched
    # only absolute ones and found 30 routes where an earlier hand sweep had
    # found 48 -- the ten /explore/nodes/*.html pages and their .md twins are
    # linked relatively. Caught only by comparing against a number I already
    # had, which is the argument for saving instruments next to their results.
    for page in ("/", "/explore/", "/changes.html", "/resources/", "/discussion/"):
        doc = text(page)
        for href in re.findall(r'href="([^"#][^"]*)"', doc):
            if href.startswith(("http://", "https://", "mailto:", "//")):
                continue
            routes.add(urllib.parse.urljoin(page, href))
    return sorted(r for r in routes if r.startswith("/") and not r.startswith("//"))


def sweep(routes):
    findings, missing, checked = [], [], []
    for route in routes:
        st, body, hd = fetch(ORIGIN + route)
        if st != 200:
            missing.append((route, st))
            continue
        doc = body.decode("utf-8", "replace")
        checked.append((route, len(body), hashlib.sha256(body).hexdigest()[:12]))
        for name, fn in MATCHERS:
            hits = fn(doc, hd)
            if hits:
                findings.append((route, name, hits[:3]))
    return checked, missing, findings


def main():
    print(__doc__.strip().splitlines()[0])
    print()

    ok, rows, link_not_load, mech = check_control()
    print("CONTROL -- every matcher must fire on a document that trips them all:")
    for name, n in rows:
        print("   %-28s %s" % (name, "fires (%d)" % n if n else "DID NOT FIRE"))
    print("   and each third-party mechanism separately:")
    for label, found in mech:
        print("     %-26s %s" % (label, "detected" if found else "MISSED"))
    print("   %-28s %s" % ("link is not counted as load",
                           "correct" if link_not_load else "WRONG"))
    if not ok:
        print("\nCONTROL FAILED. No verdict reported: a matcher that cannot fire")
        print("cannot certify an absence. Fix the checker, not the report.")
        return 2
    print()

    routes = discover()
    checked, missing, findings = sweep(routes)
    print("SWEEP -- %d routes discovered, %d returned 200" % (len(routes), len(checked)))
    if missing:
        print("   not 200: %s" % ", ".join("%s(%s)" % m for m in missing))
    print()
    if findings:
        print("FINDINGS:")
        for route, name, hits in findings:
            print("   %-40s %-28s %s" % (route, name, hits))
    else:
        print("No matcher fired on any route checked.")
    print()
    print("SCOPE -- what this run does NOT establish:")
    print("   1. closure: %d routes are the DISCOVERED surface (llms.txt,"
          " manifest, map, hrefs)," % len(routes))
    print("      not every deployed resource, alias, redirect or error response")
    print("   2. nothing about host/CDN log retention; responses carry")
    print("      per-request identifiers, which are not a retention record")
    print("   3. 'no script' is not 'nothing stored': ordinary HTTP caching")
    print("      stores the response. Scope here is SCRIPT-ACCESSIBLE storage")
    print("   4. nothing about whether the door is useful, correct or good")
    print()
    print("Defensible sentence for this run:")
    print("   \"Across the %d discovered URLs checked in this sweep, the named" % len(checked))
    print("    matchers detected none of the targeted scripts, script-accessible")
    print("    storage calls, Set-Cookie responses or third-party embedded loads.")
    print("    Hosting log retention was not established.\"")
    if "--json" in sys.argv:
        print(json.dumps({"routes": routes, "checked": checked,
                          "missing": missing, "findings": findings}, indent=1))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
