# Door measurement instruments

Three questions about a published static page, answered mechanically so the
next version of each is settled by a re-run rather than by argument.

```bash
python door_measure.py moved --repo markgoodbody-bit/COM --needle "harm visible"
python door_measure.py links --url https://pleasestartfromhere.com/
python door_measure.py open  --url https://pleasestartfromhere.com/
```

| command | question | exit |
|---|---|---|
| `moved` | did a sentence move between published versions? | 0 |
| `links` | does every destination resolve, including in-page anchors? | 1 if any fail |
| `open`  | how much of the opening states a limit rather than a claim? | 0 |
| `notice` | does the reuse pointer resolve at the served work? | 1 if any lack it, 2 if unreachable |

## `notice` — does the reuse pointer resolve?

```bash
python door_measure.py notice --url https://pleasestartfromhere.com/ \
    --work /read/trace-spine.html --work /read/me-book.html
```

Exit `0` every work carries a notice · `1` some do not · `2` something was
unreachable, so no verdict is given.

The door's `robots.txt` says *"Consult each source's licence notices for reuse
permissions."* That is a promise a reader can try to keep, so this checks
whether it can be kept — **at the point of contact**, inside the served work,
not in a README beside it that the work does not link to.

    THE_NOTICE_IS_BESIDE_THE_WORK != THE_NOTICE_IS_WITH_THE_WORK

It reports presence and absence. **It states no terms and proposes none** — what
the terms are, and whether a missing notice matters, is the owner's to say and
not a tool's.

### The exit-2 case exists because of its own first run

An MSYS shell rewrote every leading-slash `--work` path into a Windows path, so
all four fetches raised `InvalidURL`. The command then printed **"0 of 4 served
works carry no notice"** and exited 0 — a total failure to reach anything,
rendered as a pass, in a tool written that hour to catch exactly this class.

    REACHED_NOTHING != FOUND_NOTHING_WRONG

## Why these exist

On 2026-09-08 I published, twice, that a sentence on the door had moved — once
as a regression, once as a repair, **crediting another aperture with closing a
defect**. FRAMEWORK objected that a raw-byte offset in HTML and a
rendered-character offset in stripped text cannot be compared.

That was right, and testing it was worse than the objection. Measured with one
instrument across every published version:

```text
3eaf0da2  10:06Z   byte 882    <- the sentence is INTRODUCED here
bc290b96  11:01Z   byte 1259   <- moved down once, by material inserted above
c11f45e5  11:29Z   byte 1212
ba181af0  13:49Z   byte 1212   <- unchanged since
```

It had not moved since 11:29, and **did not exist at all** before 10:06, so the
earlier "drift" claim was about text that had not been written. Its share of
the page improved only because the page grew *below* it.

    TWO_MEASUREMENTS != A_COMPARISON
    THE_NUMBER_IMPROVED != SOMETHING_WAS_REPAIRED

Neither number looked wrong alone; the error lived entirely in the comparison.
And the figures from the first claim matched no published version, because the
instrument was not saved and could not be re-run — so they could only be
withdrawn, not repaired.

## What they will not do for you

`open` prints a proportion, and **the classification behind it is a judgement,
not a result.** The census is mechanical — every sentence in the window, none
skipped — but which sentences count as stating a limit is the caller's call, so
every call is printed to be disputed one at a time. A proportion whose
individual calls are hidden is not a measurement.

`moved` reports offsets in two units side by side and refuses to combine them.
Read each column down. That is the whole point.

## Pin provenance repair (2026-09-09)

`python tools/door_measure/TEST_pin_provenance.py` runs offline regression cases.
`PIN_PROVENANCE_REVISION=edd3764bce4843643503271bcd4b91b591b6a53c`
selects the historical tool for a negative-control run (set this environment
variable using your shell's syntax). No website or GitHub requests are made by
these tests; the historical variant reads local Git objects.

Before: an invented declared hash/length could pass via a real emitted file's
LF-normalised match. An unreadable source blob was silently omitted but counted
as hashed. The source scan could therefore appear complete when it was not.

After: both exact and normalised matches require the declaration's SHA-256 and
integer byte count to match the committed emitted copy. Source scans count only
successfully read blobs and return no verdict if truncated or partly unreadable.
Empty blobs remain readable content. Normalised matches are not byte-exact
matches and do not establish how a file acquired its line endings.

Exit 0: all declared entries resolve under those checks. Exit 1: an invalid
declaration or unresolved source content. Exit 2: incomplete reads or a failed
control. These are reviewer-tool results, not museum provenance, route-mapping
verification, coverage of undeclared files, or validation of a new website head.
This repair changes no public page and does not close the larger provenance gap.

Verification: 21 offline synthetic tests pass. The two original counterexample
tests fail against `edd3764` and pass after the repair. The initial repair also
mis-targeted the raw-response condition; an empty-blob test caught it before
commit. JSON/raw request-mode tests now cover that boundary explicitly.

Set `PIN_PROVENANCE_LOCAL_HISTORY=1` to include a 22nd test using local Git blobs
from inventory `b078c3cf4aa251c4226985c2547d03e3d88b196a` and source
`dfe4b5fcfa279ef08a1d5aac5d3c3a1c59494175`. It reads 67 source blobs, checks all
36 declared emitted identities, finds 24 exact and six LF-normalised matches,
and leaves six HTML files unresolved (checker exit 1, expected by the test).
No claim transfers to a newer inventory or to museum custody. The first fixture
run used a directory-relative Git tree and found zero source blobs; using
`--full-tree` corrected the fixture, not the production checker or its result.
