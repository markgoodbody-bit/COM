"""Does this surface carry any claim that could fail?

Installed because @echo-weaver found, from outside and unpaid, what eleven of my
own checks could not: the door carries no claim that can fail, so it cannot be
wrong, so it cannot be useful. Every check I had written asked *is this claiming
too much* -- authority theatre, false universality, obedience, conversion
pressure. A page claiming NOTHING passes all of them perfectly.

    A_CHECK_FOR_OVERCLAIMING_IS_BLIND_TO_UNFALSIFIABILITY
    NOTHING_TO_ATTACK != NOTHING_WRONG

I said in public I would rather add this than have it found again. This is that,
rather than another sentence about it.

    A_THEORY_OF_THE_FAILURE != A_GUARD_AGAINST_IT

WHAT IT DOES NOT DO. Falsifiability is not the only test of meaning, and FW is
right to hold that line: a value commitment and a conceptual distinction are
contestable without being empirical hypotheses. So this check never says a
sentence is bad. It says only: among everything here, is there at least one
claim about the SUBJECT that an outside observation could kill -- as distinct
from provenance about a painting, an edition or a hash.
"""
import re

# Provenance and bibliography: falsifiable, but about the artefact rather than
# the subject. The door has 13 of these and echo-weaver's point survives them.
PROVENANCE = re.compile(
    r"\b(Homer|Vermeer|Met\b|Metropolitan|museum|oil painting|canvas|accession|"
    r"public domain|open access|Preview \d|edition|sha-?256|commit|byte|bytes|"
    r"prepared \d|\b1[6-9]\d\d\b|licen[cs]e|copyright|printmaking|biography)", re.I)

# One example confirms it and nothing refutes it.
POSSIBILITY = re.compile(r"\b(can|could|may|might|sometimes|often|tends? to)\b", re.I)

# Definitional or normative rather than empirical.
CONCEPTUAL = re.compile(
    r"\b(is not|are not|does not mean|means that|by definition|is a |is the )\b", re.I)

# A commitment, not a prediction.
NORMATIVE = re.compile(
    r"\b(we propose|should|ought|must|we choose|value choice|we commit|belongs)\b", re.I)

# A ceiling: says what the material does NOT do, require or imply. Falsifiable in
# principle, but it asserts nothing a reader could use -- and it must be tested
# BEFORE the empirical pattern, or every disclaimer counts as a finding. The
# first version of this file credited the door with three "empirical" claims
# that were all ceilings: wrong in the FLATTERING direction, which is worse.
#
#     A_DISCLAIMER_IS_NOT_A_FINDING
CEILING = re.compile(
    r"\b(implies no|offers no|requires? no|does not (require|imply|override|"
    r"constitute|establish|receive)|do not (require|imply)|is not (permission|"
    r"authority|adoption|consent|validation)|no (adoption|obligation|consent|"
    r"authority|efficacy)|not neutral or complete|not a deduction|"
    r"does not by itself establish)\b", re.I)

# A statement about the artefact's own operation rather than about the subject.
OPERATIONAL = re.compile(
    r"\b(this (static )?site|this page|this file|read-only|receive replies|"
    r"no continuous freshness|links can change|posting may require)\b", re.I)

# A claim about the STATE OF EVIDENCE rather than about the world. Falsifiable --
# demonstrate the advantage and it dies -- but it asserts only that we have shown
# nothing, which is echo-weaver's complaint restated, not an answer to it.
EVIDENCE_STATE = re.compile(
    r"\b(has not been demonstrated|is unproven|no efficacy|has been measured|"
    r"not been measured|remains unproven)\b", re.I)

# Shapes that can be killed by observing the world AND assert something usable.
EMPIRICAL = re.compile(
    r"\b(in \d+ of \d+|\d+\s*%|reduces?|increases?|faster|slower|more likely|"
    r"less likely|outperforms?|no difference|surfaces?|causes?|predicts?|"
    r"we measured|we found|we observed|was demonstrated)\b", re.I)


def classify(sentence):
    """-> one of: provenance, question, possibility, normative, conceptual, empirical"""
    s = sentence.strip()
    if not s:
        return "empty"
    if s.endswith("?"):
        return "question"
    if PROVENANCE.search(s):
        return "provenance"
    if CEILING.search(s):
        return "ceiling"
    if OPERATIONAL.search(s):
        return "operational"
    if EVIDENCE_STATE.search(s):
        return "evidence_state"
    if POSSIBILITY.search(s):
        return "possibility"
    if NORMATIVE.search(s):
        return "normative"
    if EMPIRICAL.search(s):
        return "empirical"
    if CONCEPTUAL.search(s):
        return "conceptual"
    return "other"


def sentences(text):
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 25]


def a12_carries_a_claim_that_could_fail(text, ctx=None):
    """Fires when NOTHING here about the subject could be shown false."""
    counts = {}
    empirical = []
    for s in sentences(text):
        k = classify(s)
        counts[k] = counts.get(k, 0) + 1
        if k == "empirical":
            empirical.append(s)
    if empirical:
        return []
    return ["no claim about the subject can fail; %d sentences, breakdown %s"
            % (sum(counts.values()), sorted(counts.items()))]


def report(label, text):
    counts = {}
    empirical = []
    for s in sentences(text):
        k = classify(s)
        counts[k] = counts.get(k, 0) + 1
        if k == "empirical":
            empirical.append(s)
    total = sum(counts.values())
    print("  %-22s %3d sentences  %s" % (label, total,
          "  ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))))
    for s in empirical[:4]:
        print("        CAN FAIL: %s" % s[:104])
    if not empirical:
        print("        nothing here can fail")
    return len(empirical)


# --------------------------------------------------------- both directions
HAS_A_CLAIM = """
This project asks how to notice risk sooner. Working through these questions
surfaces irreversibility points that a generic risk prompt does not surface.
In a pilot of six published accounts, readers using the questions found 40% more
of the reference points than readers given a generic prompt. Practical advantage
over established methods has not been demonstrated beyond that pilot.
"""

HAS_NO_CLAIM = """
A description can stay still while the situation changes. An option is not usable
merely because it can be described. A description is not permission. We propose
making harm visible, correction reachable and power answerable. Reading implies no
adoption, obligation or consent. You may disagree, use another method, or leave.
What would show this reading was wrong?
"""

if __name__ == "__main__":
    import sys
    print(__doc__.strip().splitlines()[0])
    print()
    print("BOTH DIRECTIONS -- the check must fire on one and not the other\n")
    n_yes = report("surface WITH a claim", HAS_A_CLAIM)
    fired_yes = a12_carries_a_claim_that_could_fail(HAS_A_CLAIM)
    n_no = report("surface WITHOUT one", HAS_NO_CLAIM)
    fired_no = a12_carries_a_claim_that_could_fail(HAS_NO_CLAIM)
    print()
    ok = (not fired_yes) and bool(fired_no)
    print("  fires on the claimless surface : %s" % bool(fired_no))
    print("  silent on the surface with one : %s" % (not fired_yes))
    print()
    if not ok:
        print("THE CHECK DOES NOT DISCRIMINATE -- it proves nothing")
        sys.exit(1)
    print("discriminates. Now the published surface:\n")
    import urllib.request
    def get(u):
        r = urllib.request.Request(u, headers={"User-Agent": "cc-claim-check",
                                               "Cache-Control": "no-cache"})
        return urllib.request.urlopen(r, timeout=25).read().decode("utf-8", "replace")
    total_fail = 0
    for path in ("llms.txt", "seed.txt"):
        n = report("/" + path, get("https://pleasestartfromhere.com/" + path))
        total_fail += (n == 0)
    html = get("https://pleasestartfromhere.com/")
    html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    n = report("/ (root, stripped)", re.sub(r"<[^>]+>", " ", html))
    total_fail += (n == 0)
    print()
    print("  %d of 3 published surfaces carry no claim that can fail." % total_fail)
    print("  echo-weaver reached this from outside, unpaid, before any check of mine did.")
    sys.exit(0)
