"""Independent source-bound accept/reject fixture for the PSFH teaching surface.

Assigned by FW-PSFH-GENTLE-TEACHING-PROTOTYPE-20260908-001 and resumed by
FW-PSFH-HUMAN-ART-LAYER-AND-TEACHING-REVIEW-20260909-001. Written BEFORE
reading CODEX's implementation or its tests, deliberately, so that what it
refuses is derived from the brief and the published source rather than from
the shape of the thing under test.

WHAT IT IS. Ten checks over a normalised "surface" -- one node as a reader
would meet it. It is not a site design and renders nothing. An implementation
binds through ONE adapter function (see ADAPTER SEAM); nothing else about the
implementation is assumed.

THE DISCIPLINE THAT COST ME MOST TODAY, INSTALLED HERE. Every tamper must fail
on ITS OWN check id, not merely exit non-zero. A guard that refuses for the
wrong reason is not a guard, and a suite that only asserts "something failed"
cannot tell the difference.

    REFUSED != REFUSED_FOR_THE_REASON_UNDER_TEST

WHAT THIS FIXTURE CANNOT DO, STATED UP FRONT. Measured against the live corpus
on 2026-09-08: all ten Explore nodes carry all fourteen fields. There is NO
absence anywhere in it. So the three checks that exist to keep absence honest
(C5, C8, C9) CANNOT be exercised by the real data -- a prototype could satisfy
them vacuously and nobody would learn anything. Those rows are driven by
synthetic nodes and are labelled SYNTHETIC-ONLY in the report.

    A_CHECK_IS_BLIND_EXACTLY_WHERE_ITS_CORPUS_IS_EMPTY

That is @cairnfield's rule, and it is the most important thing this file has to
say about the prototype it is going to judge.
"""
import json
import re

SPECIALISED = ("example", "source", "challenge", "deeper", "perspective", "question")


# ---------------------------------------------------------------- ADAPTER SEAM
# An implementation supplies build_surface(node, reader_hint) -> surface.
# The surface shape is the whole contract:
#
#   {"node_id": str,
#    "shown":  [{"text": str, "from_field": str}],
#    "routes": [{"label": str, "kind": str, "target": str,
#                "claimed_support_field": str or None,
#                "relevance_basis": str or None,   # "source_field" | "index_match" | ...
#                "mandatory": bool}],
#    "index_reachable": bool, "leave_reachable": bool}
#
# reader_hint is passed ONLY so C1 can prove the output ignores it.

def reference_surface(node, reader_hint=None):
    """An honest surface built from source. The known-good direction."""
    shown = [{"text": node["short"], "from_field": "short"}]
    if node.get("detail"):
        shown.append({"text": node["detail"], "from_field": "detail"})
    routes = []
    for field in ("challenge", "perspective", "question"):
        if node.get(field):
            routes.append({"label": field, "kind": field, "target": field,
                           "claimed_support_field": field,
                           "relevance_basis": "source_field", "mandatory": False})
    for rel in (node.get("next") or []):
        if isinstance(rel, dict) and rel.get("target"):
            routes.append({"label": rel.get("relation", "related"), "kind": "related",
                           "target": rel.get("path", ""), "to_node": rel["target"],
                           "claimed_support_field": None,
                           "relevance_basis": "source_next", "mandatory": False})
    routes.append({"label": "full index", "kind": "index", "target": "../map.json",
                   "claimed_support_field": None, "relevance_basis": None,
                   "mandatory": False})
    routes.append({"label": "leave", "kind": "leave", "target": "/",
                   "claimed_support_field": None, "relevance_basis": None,
                   "mandatory": False})
    return {"node_id": node["id"], "shown": shown, "routes": routes,
            "index_reachable": True, "leave_reachable": True}


# ------------------------------------------------------------------- THE CHECKS

DIAGNOSIS = re.compile(
    r"\b(if you (?:are|re)\b|for beginners?\b|beginners?\b|novices?\b|as an expert\b"
    r"|advanced readers?\b|people like you\b|your level\b|we think you\b|based on your\b"
    r"|since you\b|readers like you\b|suitable for you\b|recommended for you\b)", re.I)

DEPTH_REWARD = re.compile(
    r"\b(next level\b|level up\b|advance\b|progress\b|unlock\b|completion\b"
    r"|continue your journey\b|step \d+ of \d+|\d+\s*%\s*(?:done|complete)|streak\b"
    r"|go deeper to\b|you have read \d+)", re.I)

PLACEHOLDER = re.compile(
    r"^\s*(n/?a|none|not available|no example(?: available)?|nothing here|empty|—|-{1,3}"
    r"|coming soon|to be added|tbd)\s*$", re.I)


def c1_no_diagnosis(s, node, twin=None):
    v = []
    for r in s["routes"]:
        if DIAGNOSIS.search(r["label"]):
            v.append("route label classifies the reader: %r" % r["label"])
    for sh in s["shown"]:
        if DIAGNOSIS.search(sh["text"]):
            v.append("shown text classifies the reader: %r" % sh["text"][:60])
    if twin is not None and json.dumps(twin, sort_keys=True) != json.dumps(s, sort_keys=True):
        v.append("surface VARIES with the reader hint; it is a function of the reader, "
                 "not of the source")
    return v


def c2_no_mandatory_representation(s, node, twin=None):
    v = ["route %r is marked mandatory" % r["label"] for r in s["routes"] if r.get("mandatory")]
    if not any(sh["from_field"] in ("short", "detail") for sh in s["shown"]):
        v.append("the node cannot be read at all without entering a specialised representation")
    return v


def c3_index_and_leave_persist(s, node, twin=None):
    v = []
    kinds = set(r["kind"] for r in s["routes"])
    if not s.get("index_reachable") or "index" not in kinds:
        v.append("the full index is not reachable from this node")
    if not s.get("leave_reachable") or "leave" not in kinds:
        v.append("there is no leave path")
    return v


def c4_no_drift_from_source(s, node, twin=None):
    v = []
    for sh in s["shown"]:
        f = sh["from_field"]
        src = node.get(f)
        if not isinstance(src, str):
            v.append("shown text claims field %r which is not text in source" % f)
        elif sh["text"] not in src:
            v.append("shown text is NOT present in source field %r (drift)" % f)
    return v


def c5_absence_is_silent(s, node, twin=None):
    v = []
    for r in s["routes"]:
        f = r.get("claimed_support_field")
        if f and not node.get(f):
            v.append("route %r offered though source field %r is absent/empty" % (r["label"], f))
        if PLACEHOLDER.match(r["label"]):
            v.append("route %r renders absence as a visible hole" % r["label"])
    for sh in s["shown"]:
        if PLACEHOLDER.match(sh["text"]):
            v.append("shown text renders absence as a visible hole: %r" % sh["text"])
    return v


def c6_challenge_preserved(s, node, twin=None):
    if not node.get("challenge"):
        return []
    carried = (any(sh["from_field"] == "challenge" for sh in s["shown"])
               or any(r.get("claimed_support_field") == "challenge" for r in s["routes"]))
    if not carried:
        return ["source carries a challenge and the surface drops it"]
    return []


def c7_no_depth_reward(s, node, twin=None):
    v = []
    for r in s["routes"]:
        if DEPTH_REWARD.search(r["label"]):
            v.append("route %r rewards depth rather than the chosen movement" % r["label"])
    for sh in s["shown"]:
        if DEPTH_REWARD.search(sh["text"]):
            v.append("shown text rewards depth: %r" % sh["text"][:60])
    return v


def supported_fields(node):
    return [f for f in ("challenge", "perspective", "question", "example", "deeper")
            if node.get(f)]


def grounded_next_targets(node):
    """The node's own onward relations. This is the source's relevance signal."""
    return set(x.get("target") for x in (node.get("next") or []) if isinstance(x, dict))


def c8_one_supported_route_beats_two(s, node, twin=None):
    """One relevant route beats two noisy ones.

    First written against field PRESENCE, which made this check a strict special
    case of C5: under that model a noisy route necessarily claimed an absent
    field, so C8 could never fire alone and proved nothing C5 had not already
    proved. Presence is not relevance -- my own INDEX_MATCH != RELEVANCE_
    ESTABLISHED, pointed at my own fixture.

    The source carries a real relevance signal: each node lists its onward
    `next` relations. A cross-node route whose target the node does not name is
    noise EVEN THOUGH the target node exists and every field on it is present.
    That is the extension C5 cannot reach.
    """
    grounded = grounded_next_targets(node)
    cross = [r for r in s["routes"] if r.get("to_node")]
    if not cross:
        return []
    ungrounded = [r["to_node"] for r in cross if r["to_node"] not in grounded]
    if ungrounded and len(grounded) >= 1:
        return ["%d cross-node route(s) point where the source does not: %s "
                "(source names %s)" % (len(ungrounded), sorted(ungrounded), sorted(grounded))]
    return []


def c9_no_route_is_an_honest_answer(s, node, twin=None):
    if supported_fields(node):
        return []
    offered = [r["label"] for r in s["routes"] if r["kind"] in SPECIALISED]
    if offered:
        return ["source supports NO specialised route; %d were manufactured: %s"
                % (len(offered), offered)]
    return []


def c10_index_match_is_not_relevance(s, node, twin=None):
    v = []
    for r in s["routes"]:
        if r["kind"] not in SPECIALISED:
            continue
        basis = r.get("relevance_basis")
        if basis in ("index_match", "term_match", "keyword", "search_hit"):
            v.append("route %r claims relevance from a match, not from source: %r"
                     % (r["label"], basis))
        elif basis == "source_field" and not r.get("claimed_support_field"):
            v.append("route %r claims a source basis but names no field" % r["label"])
    return v


CHECKS = [
    ("C1_NO_DIAGNOSIS", c1_no_diagnosis, False),
    ("C2_NO_MANDATORY_REPRESENTATION", c2_no_mandatory_representation, False),
    ("C3_INDEX_AND_LEAVE_PERSIST", c3_index_and_leave_persist, False),
    ("C4_NO_DRIFT_FROM_SOURCE", c4_no_drift_from_source, False),
    ("C5_ABSENCE_IS_SILENT_NOT_A_HOLE", c5_absence_is_silent, True),
    ("C6_CHALLENGE_PRESERVED", c6_challenge_preserved, False),
    ("C7_NO_DEPTH_REWARD", c7_no_depth_reward, False),
    ("C8_ONE_SUPPORTED_ROUTE_BEATS_TWO", c8_one_supported_route_beats_two, True),
    ("C9_NO_ROUTE_IS_AN_HONEST_ANSWER", c9_no_route_is_an_honest_answer, True),
    ("C10_INDEX_MATCH_IS_NOT_RELEVANCE", c10_index_match_is_not_relevance, True),
]

SYNTHETIC_ONLY = set(cid for cid, _fn, synth in CHECKS if synth)


def evaluate(surface, node, twin=None):
    """Return {check_id: [violations]} for every check that fired."""
    fired = {}
    for cid, fn, _synth in CHECKS:
        v = fn(surface, node, twin)
        if v:
            fired[cid] = v
    return fired
