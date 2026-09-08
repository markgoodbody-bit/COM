"""One instrument for the PSFH human-art layer, in one unit, across both states.

Assigned by FW-PSFH-HOMER-HERO-AND-HUMAN-ART-20260909-001: after CODEX returns
the Homer/Vermeer art layer, review the public result for source/provenance
truth, art-as-authority leakage, text contrast/legibility, mobile payload, and
whether the art increases invitation rather than capturing attention.

WHY THIS EXISTS BEFORE THE CHANGE DOES. On 2026-09-08 I compared a raw-byte
offset taken in the morning against a rendered-character offset taken in the
afternoon and announced a repair that had not happened, crediting another
aperture for it. Neither number was wrong; the comparison was. The instrument
was never saved, so the claim was not reconstructable -- only withdrawable.

    TWO_MEASUREMENTS != A_COMPARISON
    VERIFIED_AFTER != VERIFIED_BEFORE

So: snapshot the door NOW, while the pre-change state still exists, with the
same code that will measure the post-change state. `compare` refuses to report
a delta unless both sides came from the same instrument version.

    python door_art_review.py snapshot before
    python door_art_review.py snapshot after
    python door_art_review.py compare before after

WHAT IT CANNOT DO. It does not measure paint timing or reader benefit. It
measures bytes, hashes, declared provenance, text patterns and pixel contrast.
A clean run means those properties hold, not that the page is good.
"""
import hashlib
import io as _io
import json
import os
import re
import sys
import urllib.error
import urllib.request

INSTRUMENT_VERSION = "door-art-review/1"
ORIGIN = "https://pleasestartfromhere.com/"
HERE = os.path.dirname(os.path.abspath(__file__))

# Claims that hand the project's meanings to the painter. The brief is explicit:
# say only why a work spoke to us, never attribute our framework to the artist.
ART_AS_AUTHORITY = re.compile(
    r"\b(?:the )?(?:artist|painter|homer|vermeer)\b[^.]{0,80}\b"
    r"(?:understood|knew|intended|meant|shows us that|teaches|proves|argues|"
    r"depicts our|anticipated|foresaw|agrees?|endorses?|confirms?)\b", re.I)

# Engagement optimisation, as distinct from invitation.
ATTENTION_CAPTURE = re.compile(
    r"\b(?:don'?t miss|last chance|only \d+ left|hurry|act now|limited time|"
    r"sign up to continue|unlock full access|\d+ people are|trending now|"
    r"streak|keep your streak|you have \d+ unread|continue where you left off)\b", re.I)

CAPTURE_MARKUP = re.compile(
    r"(autoplay\b|infinite[- ]scroll|data-countdown|<dialog[^>]*open|"
    r"position:\s*fixed[^;]*;[^}]*z-index:\s*9\d{2,}|onbeforeunload)", re.I)

REQUIRED_PROVENANCE = ("title", "creator", "date", "institution", "source_url",
                       "rights", "retrieval_date", "alt", "why_here")


def fetch(url, cap=8_000_000):
    req = urllib.request.Request(url, headers={"User-Agent": "cc-door-art-review",
                                               "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read(cap), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(cap), dict(e.headers or {})
    except Exception as e:
        return None, ("%s: %s" % (type(e).__name__, e)).encode(), {}


def parse_srcset(value):
    """-> [(url, width_or_None, density_or_None)]"""
    out = []
    for part in value.split(","):
        bits = part.strip().split()
        if not bits:
            continue
        url = bits[0]
        w = d = None
        for b in bits[1:]:
            if b.endswith("w"):
                try:
                    w = int(b[:-1])
                except ValueError:
                    pass
            elif b.endswith("x"):
                try:
                    d = float(b[:-1])
                except ValueError:
                    pass
        out.append((url, w, d))
    return out


def select_candidate(candidates, css_width, dpr):
    """Approximate the browser's srcset choice: smallest candidate >= needed px."""
    if not candidates:
        return None
    need = css_width * dpr
    widthy = [c for c in candidates if c[1]]
    if widthy:
        fits = sorted([c for c in widthy if c[1] >= need], key=lambda c: c[1])
        return (fits[0] if fits else sorted(widthy, key=lambda c: -c[1])[0])
    densey = [c for c in candidates if c[2]]
    if densey:
        fits = sorted([c for c in densey if c[2] >= dpr], key=lambda c: c[2])
        return (fits[0] if fits else sorted(densey, key=lambda c: -c[2])[0])
    return candidates[0]


def rel_luminance(rgb):
    def ch(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(rgb_a, rgb_b):
    la, lb = rel_luminance(rgb_a), rel_luminance(rgb_b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def contrast_over_region(image_bytes, box_frac, text_rgb):
    """Worst-case contrast of text_rgb against the image region box_frac.

    box_frac is (x0, y0, x1, y1) as fractions of the displayed image, taken from
    real rendered geometry -- not guessed. Returns the WORST pixel, because a
    title is illegible where the image is brightest, not on average.
    """
    try:
        from PIL import Image
    except Exception as e:
        return {"measured": False, "reason": "Pillow unavailable: %s" % e}
    try:
        im = Image.open(_io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        return {"measured": False, "reason": "undecodable: %s" % e}
    w, h = im.size
    x0, y0, x1, y1 = box_frac
    crop = im.crop((max(0, int(x0 * w)), max(0, int(y0 * h)),
                    min(w, int(x1 * w)), min(h, int(y1 * h))))
    if crop.size[0] < 1 or crop.size[1] < 1:
        return {"measured": False, "reason": "empty crop"}
    small = crop.resize((min(64, crop.size[0]), min(64, crop.size[1])))
    ratios = [contrast(px, text_rgb) for px in small.getdata()]
    ratios.sort()
    n = len(ratios)
    return {"measured": True, "pixels_sampled": n,
            "worst": round(ratios[0], 2),
            "p05": round(ratios[max(0, n // 20)], 2),
            "median": round(ratios[n // 2], 2),
            "best": round(ratios[-1], 2),
            "wcag_AA_large_3to1_worst": ratios[0] >= 3.0,
            "wcag_AA_normal_4_5to1_worst": ratios[0] >= 4.5}


def snapshot(label, text_box=None, text_rgb=(255, 255, 255)):
    st, body, hdrs = fetch(ORIGIN)
    if st != 200:
        print("entry page returned %s -- refusing to snapshot" % st)
        return 2
    html = body.decode("utf-8", "replace")
    snap = {"instrument": INSTRUMENT_VERSION, "label": label, "origin": ORIGIN,
            "document_bytes": len(body),
            "document_sha256": hashlib.sha256(body).hexdigest()}

    # --- images and what each viewport actually pays -------------------------
    images = []
    for tag in re.findall(r"<img[^>]*>", html, re.I):
        def attr(name):
            m = re.search(r'\b%s="([^"]*)"' % name, tag)
            return m.group(1) if m else None
        src, srcset = attr("src"), attr("srcset")
        cands = parse_srcset(srcset) if srcset else ([(src, None, None)] if src else [])
        entry = {"src": src, "has_srcset": bool(srcset), "sizes": attr("sizes"),
                 "loading": attr("loading"), "fetchpriority": attr("fetchpriority"),
                 "width": attr("width"), "height": attr("height"),
                 "alt_len": len(attr("alt") or ""), "candidates": len(cands),
                 "viewports": {}}
        for vp_name, css_w, dpr in (("mobile_375_1x", 375, 1), ("mobile_375_2x", 375, 2),
                                    ("desktop_1440_1x", 1440, 1)):
            chosen = select_candidate(cands, css_w, dpr)
            if not chosen:
                continue
            url = chosen[0] if chosen[0].startswith("http") else ORIGIN.rstrip("/") + "/" + chosen[0].lstrip("/")
            cs, cb, _ = fetch(url)
            entry["viewports"][vp_name] = {"url": chosen[0], "status": cs, "bytes": len(cb) if cs == 200 else None}
            if vp_name == "mobile_375_1x" and cs == 200 and text_box:
                entry["contrast_under_title"] = contrast_over_region(cb, text_box, text_rgb)
        images.append(entry)
    snap["images"] = images
    mobile_total = snap["document_bytes"] + sum(
        (i["viewports"].get("mobile_375_1x", {}) or {}).get("bytes") or 0 for i in images)
    snap["mobile_375_1x_total_bytes"] = mobile_total

    # --- provenance ----------------------------------------------------------
    prov = {"records_found": [], "verified": [], "problems": []}
    for path in ("art/index.json", "art/provenance.json", "manifest.json"):
        s, b, _ = fetch(ORIGIN + path)
        if s != 200:
            continue
        try:
            obj = json.loads(b)
        except Exception:
            continue
        works = obj.get("works") or obj.get("art") or (obj if path.startswith("art/") else None)
        if isinstance(works, dict):
            works = list(works.values())
        if not isinstance(works, list):
            continue
        for wk in works:
            if not isinstance(wk, dict):
                continue
            prov["records_found"].append({"path": path, "id": wk.get("id") or wk.get("title")})
            missing = [f for f in REQUIRED_PROVENANCE if not wk.get(f)]
            if missing:
                prov["problems"].append({"work": wk.get("id") or wk.get("title"),
                                         "missing_fields": missing})
            for key in ("original", "master", "variants", "derived"):
                items = wk.get(key)
                if isinstance(items, dict):
                    items = [items]
                for it in (items or []):
                    if not isinstance(it, dict) or not it.get("sha256") or not it.get("path"):
                        continue
                    u = ORIGIN.rstrip("/") + "/" + str(it["path"]).lstrip("/")
                    s2, b2, _ = fetch(u)
                    got = hashlib.sha256(b2).hexdigest() if s2 == 200 else None
                    ok = (got == it["sha256"])
                    prov["verified"].append({"path": it["path"], "declared": it["sha256"][:16],
                                             "actual": (got or "FETCH_%s" % s2)[:16], "match": ok})
                    if not ok:
                        prov["problems"].append({"path": it["path"],
                                                 "declared_sha256_does_not_match_served_bytes": True})
    snap["provenance"] = prov

    # --- text patterns -------------------------------------------------------
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    snap["art_as_authority_hits"] = ART_AS_AUTHORITY.findall(text)[:10]
    snap["attention_capture_text_hits"] = ATTENTION_CAPTURE.findall(text)[:10]
    snap["attention_capture_markup_hits"] = CAPTURE_MARKUP.findall(html)[:10]

    out = os.path.join(HERE, "door_art_%s.json" % label)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, indent=2)
    render(snap)
    print("\nwritten: %s" % os.path.basename(out))
    return 0


def render(s):
    print("== %s (%s) ==" % (s["label"], s["instrument"]))
    print("  document                 %s bytes" % format(s["document_bytes"], ","))
    for i in s["images"]:
        print("  image %-24s srcset=%s loading=%s alt=%dch"
              % ((i["src"] or "?")[:24], i["has_srcset"], i["loading"], i["alt_len"]))
        for vp, v in i["viewports"].items():
            print("      %-16s %s bytes" % (vp, format(v["bytes"], ",") if v["bytes"] else v["status"]))
        c = i.get("contrast_under_title")
        if c:
            if c.get("measured"):
                print("      contrast under title: worst %.2f:1  median %.2f:1  "
                      "AA-large(3:1) at worst pixel: %s"
                      % (c["worst"], c["median"], c["wcag_AA_large_3to1_worst"]))
            else:
                print("      contrast under title: NOT MEASURED (%s)" % c["reason"])
    print("  mobile 375 1x total      %s bytes" % format(s["mobile_375_1x_total_bytes"], ","))
    p = s["provenance"]
    print("  provenance records       %d found, %d hash checks, %d problems"
          % (len(p["records_found"]), len(p["verified"]), len(p["problems"])))
    for pr in p["problems"][:6]:
        print("      PROBLEM %s" % json.dumps(pr))
    print("  art-as-authority         %d hit(s) %s" % (len(s["art_as_authority_hits"]),
                                                       s["art_as_authority_hits"][:3]))
    print("  attention capture        %d text, %d markup"
          % (len(s["attention_capture_text_hits"]), len(s["attention_capture_markup_hits"])))


def compare(a, b):
    pa = os.path.join(HERE, "door_art_%s.json" % a)
    pb = os.path.join(HERE, "door_art_%s.json" % b)
    for p in (pa, pb):
        if not os.path.exists(p):
            print("missing snapshot: %s" % os.path.basename(p))
            return 2
    A = json.load(open(pa, encoding="utf-8"))
    B = json.load(open(pb, encoding="utf-8"))
    if A["instrument"] != B["instrument"]:
        print("REFUSING to compare: %s vs %s. Two instruments are not a comparison."
              % (A["instrument"], B["instrument"]))
        return 2
    print("== %s -> %s, one instrument, one unit ==" % (a, b))
    for k in ("document_bytes", "mobile_375_1x_total_bytes"):
        d = B[k] - A[k]
        print("  %-26s %12s -> %-12s  %+d" % (k, format(A[k], ","), format(B[k], ","), d))
    print("  art-as-authority hits      %d -> %d" % (len(A["art_as_authority_hits"]),
                                                     len(B["art_as_authority_hits"])))
    print("  attention-capture hits     %d -> %d"
          % (len(A["attention_capture_text_hits"]) + len(A["attention_capture_markup_hits"]),
             len(B["attention_capture_text_hits"]) + len(B["attention_capture_markup_hits"])))
    print("  provenance problems        %d -> %d" % (len(A["provenance"]["problems"]),
                                                     len(B["provenance"]["problems"])))
    return 0


def main(argv):
    if len(argv) >= 3 and argv[1] == "snapshot":
        box = None
        rgb = (255, 255, 255)
        if len(argv) >= 8 and argv[3] == "--title-box":
            box = tuple(float(x) for x in argv[4:8])
            if len(argv) >= 11:
                rgb = tuple(int(x) for x in argv[8:11])
        return snapshot(argv[2], text_box=box, text_rgb=rgb)
    if len(argv) == 4 and argv[1] == "compare":
        return compare(argv[2], argv[3])
    print(__doc__)
    print("usage: snapshot <label> [--title-box x0 y0 x1 y1 [R G B]] | compare <a> <b>")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
