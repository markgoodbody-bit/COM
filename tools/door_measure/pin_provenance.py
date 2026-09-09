"""Resolve declared pins against the historical tree they claim to come from.

Written 2026-09-09 after I reviewed a five-work integration and found that its
test compared two inventories living in the SAME JSON record -- `files` against
`reviewed_files`. That comparison proves the file agrees with itself. It cannot
detect a record that was wrong when written, because both halves would be wrong
together.

    TWO_FIELDS_OF_ONE_FILE_AGREEING != VERIFIED_AGAINST_THE_SOURCE

CODEX accepted the limitation and documented it rather than papering over it,
and asked that it NOT be turned into a checker written to make the row green.
That is right, and this tool is deliberately a different thing:

  - it does NOT run in their build and changes no test assertion;
  - it does NOT declare the ceiling closed;
  - it is REVIEWER-side, so the independent check a reviewer does by hand can
    be repeated by the next reviewer instead of being taken on trust.

I closed the ceiling for one commit by comparing 16 image blobs by hand. That
closure was my read of one head, not a property of anything, and a later head
would inherit the assumption without the check. This makes the read repeatable.

    SAVE_THE_INSTRUMENT_BESIDE_THE_NUMBER

METHOD, and why it is content-first. Pins name routes in the built output
(art/bible-quilt-1440.jpg); the source lives at another path entirely
(proposals/powers/assets/bible-quilt-1440.jpg). Matching by filename is
guesswork that breaks on any rename. So this resolves by CONTENT: it hashes
every blob in the historical tree and asks whether a blob with the declared
sha256 exists there at all.

What that establishes, and what it does not:

    a blob with this exact content EXISTED in the named source tree     yes
    the route mapping from source path to output path is correct        NO
    the pinned bytes are what a museum supplied                         NO

The last two need separate evidence. A pin whose content is absent from the
source tree is a real finding; a pin whose content is present is necessary but
not sufficient, and the report says so on every run.
"""

import sys
import json
import base64
import hashlib
import subprocess


def gh(path, raw=False):
    args = ["gh", "api", path]
    if raw:
        args += ["-H", "Accept: application/vnd.github.raw"]
    r = subprocess.run(args, capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if raw else json.loads(r.stdout.decode("utf-8", "replace"))


def tree(repo, ref):
    j = gh("repos/%s/git/trees/%s?recursive=1" % (repo, ref))
    if j is None:
        return None, False
    blobs = {e["path"]: e["sha"] for e in j.get("tree", []) if e["type"] == "blob"}
    return blobs, bool(j.get("truncated"))


def blob_bytes(repo, sha):
    raw = gh("repos/%s/git/blobs/%s" % (repo, sha), raw=True)
    if raw is not None:
        return raw
    j = gh("repos/%s/git/blobs/%s" % (repo, sha))
    if j and j.get("encoding") == "base64" and j.get("content") is not None:
        return base64.b64decode(j["content"])
    return None


def index_by_content(repo, ref, prefixes):
    """-> (exact, normalised, successfully_hashed_count, incomplete).

    Two indexes, because a bare content match reports a false alarm on a real
    corpus. Measured on the first run: 12 of 36 pins did not resolve, and every
    one had an explanation -- SIX were the same text with CRLF line endings, and
    SIX had no source blob in that tree at all. A tool that prints those as
    "NOT FOUND" invites exactly the harsh-direction error I spent that day
    correcting.

    Two corrections from CODEX, both upheld, both recorded here rather than
    quietly fixed. FIRST: this docstring said five and seven while the reported
    result was six and six -- written from the first run and never updated when
    the classification changed, so the file disagreed with its own output.
    SECOND: the six with no source blob must NOT be called "built". This tool
    cannot distinguish a generated file from an absent one -- it says so in its
    own report -- so "generated" is inference, and "36 fully accounted for" was
    an overclaim on my part.

        MY_DOCSTRING_DISAGREED_WITH_MY_OUTPUT
        NO_SOURCE_BLOB != GENERATED

        UNRESOLVED != WRONG

    So the second index is keyed on LF-normalised content, and anything that
    resolves only there is reported as a line-ending shift, not a discrepancy.
    """
    blobs, truncated = tree(repo, ref)
    if blobs is None:
        return None, None, None, False
    wanted = {p: s for p, s in blobs.items()
              if any(p.startswith(pre) for pre in prefixes)}
    exact, normalised = {}, {}
    scanned = 0
    incomplete = truncated
    for path, sha in sorted(wanted.items()):
        data = blob_bytes(repo, sha)
        if data is None:
            print("  cannot read source blob %s @ %s" % (path, sha))
            incomplete = True
            continue
        scanned += 1
        exact.setdefault(hashlib.sha256(data).hexdigest(), []).append(path)
        lf = data.replace(b"\r\n", b"\n")
        normalised.setdefault(hashlib.sha256(lf).hexdigest(), []).append(path)
    return exact, normalised, scanned, incomplete


def emitted_bytes(repo, ref, route):
    """The built copy as committed, for the line-ending second pass."""
    j = gh("repos/%s/contents/public/%s?ref=%s" % (repo, route, ref))
    if not j:
        return None
    if j.get("encoding") == "base64" and j.get("content") is not None:
        return base64.b64decode(j["content"])
    return blob_bytes(repo, j["sha"])


def check(repo, pins_ref, pins_path, pins_key, source_ref, prefixes):
    rec = gh("repos/%s/contents/%s?ref=%s" % (repo, pins_path, pins_ref))
    if rec is None:
        print("  cannot read the pins record %s@%s" % (pins_path, pins_ref[:8]))
        return 2
    pins = json.loads(base64.b64decode(rec["content"]).decode("utf-8"))
    declared = pins.get(pins_key) or {}
    review = pins.get("source_review") or source_ref

    print("  pins record   %s @ %s" % (pins_path, pins_ref[:12]))
    print("  declares      %d entries under %r" % (len(declared), pins_key))
    print("  source_review %s" % review)
    print()

    exact, normalised, scanned, incomplete = index_by_content(repo, review, prefixes)
    if exact is None:
        print("  cannot read the source tree %s -- NO VERDICT" % review[:12])
        return 2
    print("  hashed %d blobs under %s in %s" % (scanned, ",".join(prefixes), review[:12]))
    if incomplete:
        print("  INCOMPLETE source scan: tree truncated or a blob could not be read.")
        print("  Missing content cannot be treated as absent. NO VERDICT.")
        return 2
    print()

    byte_exact, eol_shift, no_source = [], [], []
    invalid, unavailable = [], []
    for route, meta in sorted(declared.items()):
        meta = meta if isinstance(meta, dict) else {}
        want = meta.get("sha256")
        size = meta.get("bytes")
        if not isinstance(want, str) or not want or type(size) is not int or size < 0:
            invalid.append((route, "sha256 and non-negative integer bytes are required"))
            continue
        data = emitted_bytes(repo, pins_ref, route)
        if data is None:
            unavailable.append(route)
            continue
        # Check the declaration BEFORE either source-matching path. A valid
        # emitted file cannot rehabilitate a fabricated checksum or length.
        if hashlib.sha256(data).hexdigest() != want or len(data) != size:
            invalid.append((route, "declared sha256 or bytes differ from emitted copy"))
            continue
        if want in exact:
            byte_exact.append((route, exact[want][0]))
            continue
        lf = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
        if lf in normalised:
            eol_shift.append((route, normalised[lf][0],
                              data.count(b"\r\n")))
        else:
            no_source.append((route, want))

    print("  BYTE-EXACT in the source tree: %d of %d" % (len(byte_exact), len(declared)))
    for route, src in byte_exact[:3]:
        print("     %-34s <- %s" % (route, src))
    if len(byte_exact) > 3:
        print("     ... and %d more" % (len(byte_exact) - 3))
    if eol_shift:
        print()
        print("  SAME CONTENT, line endings differ: %d" % len(eol_shift))
        print("     (declared emitted bytes verified; identical after LF normalisation)")
        for route, src, n in eol_shift:
            print("     %-34s <- %-40s emitted CRLFs=%d" % (route, src, n))
    if no_source:
        print()
        print("  NO SOURCE BLOB: %d  -- generated by a build, or genuinely absent" % len(no_source))
        for route, want in no_source:
            print("     %-34s %s" % (route, want[:16] if isinstance(want, str) else ""))
        print("     Distinguishing 'built' from 'absent' needs the builder, not this tool.")
    if invalid:
        print()
        print("  INVALID DECLARED IDENTITY: %d" % len(invalid))
        for route, reason in invalid:
            print("     %s: %s" % (route, reason))
    if unavailable:
        print()
        print("  UNREADABLE EMITTED COPY: %d -- NO VERDICT" % len(unavailable))
        for route in unavailable:
            print("     %s" % route)

    # Index sanity check only. The regression suite exercises fabricated pins
    # through check(); absence from an index alone does not test that path.
    fake = hashlib.sha256(b"a blob that is not in any tree").hexdigest()
    control_ok = fake not in exact and fake not in normalised
    print()
    print("  control: a fabricated sha256 resolves in neither index -> %s"
          % ("correct" if control_ok else "BROKEN, everything 'resolves'"))
    if not control_ok:
        return 2

    print()
    print("  WHAT THIS ESTABLISHES")
    print("    each resolved declaration matches its committed emitted copy")
    print("    a byte-exact or LF-normalised source match was found in %s, as labelled" % review[:12])
    print("  WHAT IT DOES NOT")
    print("    - that the source-path -> output-route mapping is correct")
    print("    - that those bytes are what any museum or upstream actually supplied")
    print("    - anything about files added to the output but never declared")
    if unavailable:
        return 2
    return 1 if no_source or invalid else 0


def main():
    repo = "markgoodbody-bit/COM"
    pins_ref = sys.argv[1] if len(sys.argv) > 1 else "b078c3cf4aa251c4226985c2547d03e3d88b196a"
    print(__doc__.strip().splitlines()[0])
    print()
    return check(repo, pins_ref, "scripts/WORKS_COPIES.json", "files",
                 "dfe4b5fcfa279ef08a1d5aac5d3c3a1c59494175", ("proposals/",))


if __name__ == "__main__":
    sys.exit(main())
