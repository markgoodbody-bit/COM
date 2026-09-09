"""The tamper suite for conduct_sweep. Offline; makes no network request.

A checker that reports "clean" is worthless unless it can be shown to REFUSE
when it cannot see. This suite breaks the matchers in the three specific ways
they have actually been broken, and requires the control to refuse a verdict
each time.

    TESTED_THAT_IT_REFUSES != TESTED_THAT_IT_REFUSES_ONLY_WHAT_IT_SHOULD

Two of these three were found by running this suite against the FIRST version
of the control, which passed them. That version asked only "does each matcher
fire at all" and called the third-party matcher from module scope rather than
from the list actually in use. So:

  - a matcher that ignored @import and url() passed, because the src= case
    alone satisfied the combined control -- and a web font hiding in a
    stylesheet is precisely the case that would then be missed;
  - a matcher that counted <a href> as a load passed, because the link/load
    check was testing a function nobody had swapped.

    A_CONTROL_THAT_FIRES_ONCE != A_CONTROL_THAT_TESTS_EACH_MECHANISM
    I_CHECKED_A_FUNCTION != I_CHECKED_THE_ONE_IN_USE
"""

import re
import sys
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "conduct_sweep", Path(__file__).with_name("conduct_sweep.py"))
cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)

BASE = list(cs.MATCHERS)


def with_third(fn):
    m = list(BASE)
    m[3] = ("third-party load", fn)
    return m


def only_src(doc, _hd):
    """Ignores @import and url(): a font in CSS becomes invisible."""
    found = set(re.findall(r'\ssrc="https?://([^/"]+)', doc))
    return sorted(d for d in found if cs.OWN not in d)


def links_as_loads(doc, _hd):
    """Counts <a href> as a load. This is an error I actually published."""
    found = set(re.findall(r'href="https?://([^/"]+)', doc))
    return sorted(d for d in found if cs.OWN not in d)


def script_at_line_start(doc, _hd):
    """Anchored to line start, so a mid-line <script> is missed. Same shape as
    the grep that made me tell FRAMEWORK a watcher never calls exit."""
    return re.findall(r"^<script", doc, re.M)


CASES = [
    ("third-party matcher ignoring @import and url()", with_third(only_src), False),
    ("third-party matcher counting <a href> as a load", with_third(links_as_loads), False),
    ("script matcher anchored to line start",
     [("script tag", script_at_line_start)] + BASE[1:], False),
    ("unmodified matchers", BASE, True),
]


def main():
    print(__doc__.strip().splitlines()[0])
    print()
    failures = 0
    for label, matchers, expected in CASES:
        ok, _rows, link_not_load, mech = cs.check_control(matchers)
        missed = [m for m, found in mech if not found]
        status = "allowed" if ok else "REFUSED"
        mark = "ok" if ok == expected else "GUARD BROKEN"
        if ok != expected:
            failures += 1
        print("  %-50s %-8s %s" % (label, status, mark))
        if missed:
            print("       mechanisms missed: %s" % ", ".join(missed))
        if not link_not_load:
            print("       a plain link was counted as a load")
    print()
    if failures:
        print("%d case(s) did not behave as required." % failures)
        return 1
    print("Every tamper is refused; the unmodified checker still returns a verdict.")
    print("The control tests each third-party mechanism separately, and tests")
    print("the matcher actually in the list rather than one in module scope.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
