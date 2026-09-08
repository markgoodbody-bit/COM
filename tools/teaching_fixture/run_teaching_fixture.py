"""Both-directions runner for teaching_fixture.

Direction 1  the honest reference surface over all ten LIVE nodes -> nothing fires.
Direction 2  one tamper per check -> that check fires, and ONLY that check.

The second direction is the one that matters. A suite that merely asserts
"something failed" cannot distinguish a guard from an accident; today a tamper
of mine passed a checker while the gate it deleted was still named in the error
message on the next line. So every tamper here declares the check it targets and
the run FAILS if the fired set is not exactly {that check}.

    REFUSED != REFUSED_FOR_THE_REASON_UNDER_TEST
"""
import copy
import json
import os
import sys

import teaching_fixture as TF

HERE = os.path.dirname(os.path.abspath(__file__))


def load_live_nodes():
    with open(os.path.join(HERE, "explore_nodes_all.json"), encoding="utf-8") as fh:
        return json.load(fh)


# Synthetic nodes: the live corpus has NO absence, so C5/C8/C9 cannot be
# exercised by it. These construct the absence the real data does not contain.
SYNTH_ONE_SUPPORTED = {
    "id": "synth_one", "title": "One", "short": "Only one route is genuinely supported.",
    "detail": "Only one route is genuinely supported.", "challenge": "A real challenge.",
    "next": [{"relation": "the one real relation", "target": "aperture", "path": "aperture.json"}],
}
SYNTH_NONE_SUPPORTED = {
    "id": "synth_none", "title": "None", "short": "No specialised route is supported here.",
    "detail": "No specialised route is supported here.",
}


def tamper_c1(s, n):
    s["routes"][0]["label"] = "for beginners: start here"
    return s


def tamper_c1_varies(s, n):
    return s  # handled specially: twin differs


def tamper_c2(s, n):
    s["routes"][0]["mandatory"] = True
    return s


def tamper_c3(s, n):
    s["routes"] = [r for r in s["routes"] if r["kind"] != "index"]
    s["index_reachable"] = False
    return s


def tamper_c4(s, n):
    s["shown"][0]["text"] = "A tidied-up paraphrase that reads better than the source."
    return s


def tamper_c5(s, n):
    s["routes"].insert(0, {"label": "example", "kind": "example", "target": "example",
                           "claimed_support_field": "example",
                           "relevance_basis": "source_field", "mandatory": False})
    return s


def tamper_c6(s, n):
    s["shown"] = [sh for sh in s["shown"] if sh["from_field"] != "challenge"]
    s["routes"] = [r for r in s["routes"] if r.get("claimed_support_field") != "challenge"]
    return s


def tamper_c7(s, n):
    s["routes"][0]["label"] = "unlock the deeper reading"
    return s


def tamper_c8(s, n):
    # A cross-node route to a node that EXISTS and is fully populated, but which
    # this node's source does not name in `next`. C5 cannot see this: no field
    # is absent. Only a relevance signal catches it.
    s["routes"].insert(0, {"label": "related", "kind": "related", "target": "power.json",
                           "to_node": "power", "claimed_support_field": None,
                           "relevance_basis": "source_next", "mandatory": False})
    return s


def tamper_c9(s, n):
    s["routes"].insert(0, {"label": "deeper", "kind": "deeper", "target": "deeper",
                           "claimed_support_field": None,
                           "relevance_basis": None, "mandatory": False})
    return s


def tamper_c10(s, n):
    s["routes"][0]["relevance_basis"] = "index_match"
    return s


# (target check, node, tamper fn, note)
TAMPERS = [
    ("C1_NO_DIAGNOSIS", "live", tamper_c1, "a route label that tells the reader what they are"),
    ("C1_NO_DIAGNOSIS", "live", tamper_c1_varies, "surface varies with the reader hint"),
    ("C2_NO_MANDATORY_REPRESENTATION", "live", tamper_c2, "one representation made mandatory"),
    ("C3_INDEX_AND_LEAVE_PERSIST", "live", tamper_c3, "the full index removed"),
    ("C4_NO_DRIFT_FROM_SOURCE", "live", tamper_c4, "a nicer paraphrase replaces the source"),
    ("C5_ABSENCE_IS_SILENT_NOT_A_HOLE", "synth_one", tamper_c5,
     "a route offered for a field the source does not carry"),
    ("C6_CHALLENGE_PRESERVED", "live", tamper_c6, "the challenge quietly dropped"),
    ("C7_NO_DEPTH_REWARD", "live", tamper_c7, "depth framed as a reward"),
    ("C8_ONE_SUPPORTED_ROUTE_BEATS_TWO", "synth_one", tamper_c8,
     "a cross-node route the source does not name (every field present)"),
    ("C9_NO_ROUTE_IS_AN_HONEST_ANSWER", "synth_none", tamper_c9,
     "a specialised route manufactured where source supports none"),
    ("C10_INDEX_MATCH_IS_NOT_RELEVANCE", "live", tamper_c10,
     "relevance claimed from a term match"),
]


def main():
    nodes = load_live_nodes()
    live_ids = sorted(nodes)
    probe = nodes[live_ids[0]]

    print("SOURCE: %d live Explore nodes" % len(nodes))
    absent = [(i, f) for i, n in nodes.items()
              for f in ("challenge", "perspective", "question") if not n.get(f)]
    print("        fields absent anywhere in the live corpus: %d" % len(absent))
    print("        -> C5/C8/C9 cannot be exercised by real data; they run on synthetic nodes\n")

    fails = 0

    print("DIRECTION 1 -- the honest reference surface over every live node")
    for nid in live_ids:
        n = nodes[nid]
        s = TF.reference_surface(n)
        twin = TF.reference_surface(n, reader_hint="an expert in a hurry")
        fired = TF.evaluate(s, n, twin)
        ok = not fired
        if not ok:
            fails += 1
        print("  %-12s %s%s" % (nid, "clean" if ok else "FIRED " + ",".join(sorted(fired)),
                                "" if ok else "  <-- a HONEST surface must not trip anything"))

    print("\nDIRECTION 2 -- one tamper per check; each must fire ITS OWN check and no other")
    for target, which, fn, note in TAMPERS:
        if which == "live":
            node = probe
        elif which == "synth_one":
            node = SYNTH_ONE_SUPPORTED
        else:
            node = SYNTH_NONE_SUPPORTED

        base = TF.reference_surface(node)
        s = fn(copy.deepcopy(base), node)
        if fn is tamper_c1_varies:
            twin = copy.deepcopy(base)
            twin["routes"] = list(reversed(twin["routes"]))
        else:
            twin = copy.deepcopy(s)

        fired = set(TF.evaluate(s, node, twin))
        exact = fired == {target}
        if not exact:
            fails += 1
        tag = "ok" if exact else ("FIRED %s" % (",".join(sorted(fired)) or "NOTHING"))
        print("  %-34s %-58s %s" % (target, note[:58], tag))
        if not exact:
            print("        ^ expected exactly {%s}; a tamper that fires the wrong check "
                  "proves nothing" % target)

    print("\n%s" % ("ALL DIRECTIONS CORRECT" if not fails else "%d PROBLEM(S)" % fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
