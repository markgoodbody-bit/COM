"""Run the bounded AI-route attack against the PUBLISHED surface.

Direction 1: a synthetic hostile document must trip every text check.
Direction 2: the published llms.txt and seed.txt, measured.
Then the mechanical checks that regexes cannot answer: context burden, ceiling
consistency across entrances, machine-tool compatibility, route parity.
"""
import json
import re
import sys

import ai_route_attack as A

ORIGIN = "https://pleasestartfromhere.com/"


def main():
    print("== DIRECTION 1: does each check fire on a deliberately hostile document? ==")
    fired = A.attack_text("hostile", A.HOSTILE)
    dead = []
    for cid, _fn in A.CHECKS_TEXT:
        hit = cid in fired
        if not hit:
            dead.append(cid)
        print("  %-32s %s" % (cid, "fires" if hit else "DEAD -- cannot fire, proves nothing"))
    if dead:
        print("\n  %d check(s) could not fire. A clean report from a dead check is not a "
              "clean page." % len(dead))
    print()

    print("== DIRECTION 2: the published AI surface ==")
    surfaces = {}
    for p in ("llms.txt", "seed.txt"):
        st, body, hdrs = A.fetch(ORIGIN + p)
        surfaces[p] = body.decode("utf-8", "replace") if st == 200 else ""
        f = A.attack_text(p, surfaces[p])
        print("  /%-10s %5s  %6d bytes  %s" % (p, st, len(body),
              "clean on all %d checks" % len(A.CHECKS_TEXT) if not f
              else "FIRED: " + ", ".join(sorted(f))))
        for cid, vs in sorted(f.items()):
            for v in vs[:3]:
                print("        %s: %s" % (cid, v))
    print()

    llms = surfaces["llms.txt"]
    seed = surfaces["seed.txt"]

    # ---- A7 context burden -------------------------------------------------
    print("== A7_CONTEXT_BURDEN: what an agent must ingest to orient ==")
    burden = []
    for p in ("llms.txt", "seed.txt", "manifest.json", "explore/start.json", "explore/map.json"):
        st, b, _ = A.fetch(ORIGIN + p)
        burden.append((p, st, len(b) if st == 200 else 0))
        print("  %-22s %5s %8s bytes  ~%s tokens" % (p, st, format(len(b), ","),
                                                     format(len(b) // 4, ",")))
    total = sum(x[2] for x in burden)
    print("  %-22s       %8s bytes  ~%s tokens  (all five)" %
          ("TOTAL", format(total, ","), format(total // 4, ",")))
    print("  minimum useful entry: seed.txt alone = %s bytes (~%s tokens)"
          % (format(burden[1][2], ","), format(burden[1][2] // 4, ",")))
    print()

    # ---- A8 ceilings: same at every entrance? ------------------------------
    print("== A8_STALE_DUPLICATED_CEILINGS: does every entrance carry the same limits? ==")
    # Patterns must catch the CLAIM, not one phrasing of it. The first version of
    # this grid reported that node records carry no ceilings at all; they carry
    # the most compact ceiling on the site ("A reader may stop, disagree or use a
    # better account" + "WORKING EXPERIMENT / NOT CANON / NO EFFICACY RESULT").
    # A ceiling stated in different words is still stated.
    #
    #     MY_PHRASING_IS_ABSENT != THE_CEILING_IS_ABSENT
    CEILINGS = {
        "no adoption / consent": r"(no adoption|not consent|is not adoption|"
                                 r"implies no adoption|obligation is assigned|"
                                 r"no obligation|encounter is not adoption)",
        "advantage unproven": r"(advantage[^.]{0,120}(unproven|not been demonstrated)|"
                              r"no efficacy|NO EFFICACY)",
        "does not override the reader's task": r"(override|overriding)",
        "stopping/disagreement legitimate": r"(stopping (are|is) legitimate|"
                                            r"disagreement[^.]{0,80}legitimate|"
                                            r"may stop, disagree|reader may stop|"
                                            r"right to stop|and leave)",
        "not canon / not a release": r"(not (a )?(validation|release|canon)|NOT CANON|"
                                     r"WORKING EXPERIMENT|not a TRACE or ME release)",
    }
    st, mb, _ = A.fetch(ORIGIN + "explore/map.json")
    mapj = mb.decode("utf-8", "replace") if st == 200 else ""
    st, nb, _ = A.fetch(ORIGIN + "explore/nodes/change.json")
    nodej = nb.decode("utf-8", "replace") if st == 200 else ""
    entrances = [("llms.txt", llms), ("seed.txt", seed),
                 ("explore/map.json", mapj), ("a node record", nodej)]
    print("  %-34s %s" % ("ceiling", "  ".join("%-16s" % e[0] for e in entrances)))
    gaps = []
    for name, pat in CEILINGS.items():
        cells = []
        for ename, text in entrances:
            ok = bool(re.search(pat, text, re.I | re.S))
            cells.append(ok)
            if not ok:
                gaps.append((name, ename))
        print("  %-34s %s" % (name, "  ".join("%-16s" % ("carried" if c else "-- ABSENT --")
                                              for c in cells)))
    print("\n  %d entrance/ceiling gaps: an agent arriving by one route meets limits another "
          "route states." % len(gaps))
    print()

    # ---- A9 machine-tool compatibility -------------------------------------
    print("== A9_MACHINE_TOOL_COMPATIBILITY ==")
    links = re.findall(r"\]\((https?://[^)]+|/[^)]+)\)", llms)
    absolute = [l for l in links if l.startswith("http")]
    relative = [l for l in links if l.startswith("/")]
    print("  links in llms.txt: %d absolute, %d relative" % (len(absolute), len(relative)))
    if absolute and relative:
        print("  MIXED addressing in one machine-read file. Relative links resolve only if the")
        print("  tool kept the base URL; a fetcher that passes the TEXT to a model loses it.")
        for r in relative:
            print("      relative: %s" % r)
    bad = []
    for l in links:
        u = l if l.startswith("http") else ORIGIN.rstrip("/") + l
        st, _b, _h = A.fetch(u)
        if st != 200:
            bad.append((l, st))
    print("  %d of %d links resolve 200; %d do not" % (len(links) - len(bad), len(links), len(bad)))
    for l, st in bad:
        print("      BROKEN %s -> %s" % (l, st))
    print()

    # ---- A11 route parity ---------------------------------------------------
    print("== A11_ROUTE_PARITY: can a model choose the human route or generic map? ==")
    human = re.search(r"\[Human reading\]|pleasestartfromhere\.com/\)", llms)
    genmap = re.search(r"manifest\.json|Machine map", llms)
    print("  human route offered from the AI surface : %s" % ("yes" if human else "NO"))
    print("  generic machine map offered             : %s" % ("yes" if genmap else "NO"))
    print("  either marked as lesser/penalised       : %s"
          % ("yes" if re.search(r"(instead of|rather than) the (AI|machine)", llms, re.I) else "no"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
