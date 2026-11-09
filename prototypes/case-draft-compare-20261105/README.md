# Case-draft comparison (offline, optional)

A writer may revise a Mechanical Ethics/TRACE-inspired case card and later need to know **which authored fields changed** before sending a new version. This independent Python 3.10+ standard-library tool compares two **local JSON drafts** and prints an exact, position-based structural comparison. It is not a new TRACE grammar, an incident detector, a source validator, a version-control replacement, or proof of changed events. Prefer a specialist system or normal document diff if that is more suitable.

Run `python3 compare.py old.json revised.json` for field-level values, or add `--summary` to show **only change counts**, omitting author paths, values **and SHA-256 content fingerprints**. A digest of a private draft can link reports or permit guesses about known small documents. Counts remain potentially sensitive, so a summary is not anonymisation. Add `--exact-row-moves` to recognize **pure permutations** of the complete `claims`, `parties` and `possibilities` row sets, when the exact full JSON values and duplicate counts of all rows are unchanged. Each such set is reported as one `REORDERED` event instead of many positional field changes. If any row has genuinely changed, that set retains the old positional comparison. This optional mode does not claim row identities, permission, evidence quality or changes in real events. Add `--output comparison.txt` to write the report atomically; failure preserves any existing output file. There are no accounts, network requests, API/model calls, downloads, installations or file edits besides that explicitly requested report. Beware that a full report contains **private author text**; do not share it without checking. Hashes identify file bytes, not custody or trusted authorship.

The comparer accepts up to 128 KiB of strict UTF-8 JSON **objects** per input, rejects duplicate keys, non-finite constants, lone surrogates, excessive nesting and more than 1,024 field changes. It **does not validate the case-card schema**. To check that a draft is renderable, run the existing optional `prototypes/trace-case-card-20261028/case_card.py` validator separately on its own isolated branch. No dependence on that module or a private specialist archive is introduced here.

Changes are described by JSON Pointer paths with RFC 6901 escaping, including `/claims/0/evidence` or `/correction/window`. By default arrays are compared **by position, not participant identity**; opt-in exact row-set recognition does not infer identities. Moving rows may otherwise appear as removal and changes; removals do not prove retraction, and updated `observed`, `executed`, `open` or `closed` strings remain unverified author labels. ABSENT differs from JSON `null` or an explicit `unknown`. The tool quotes all untrusted text in ASCII-escaped JSON to prevent terminal-control and forged plain-text heading presentation. It does not rewrite or evaluate any author field.

Run `python3 -m unittest -v test_compare test_exact_reorder` for the combined source-only regression suite. The added `test_exact_reorder` checks pure permutations, duplicate rows, edited-row fallback, opt-in default compatibility, hostile-looking values and CLI refusal. Its fixtures are synthetic. Local Python 3.13.5 passed 17/17 cases covering line/heading spoofing, unknown/absence, author evidence-label changes, list moves, bounds, malformed JSON, and CLI atomic failure behaviour. Browser experience, real reader value, author authentication, semantic equivalence, case-schema validity, actual witness independence and any consequences in the world are **NOT VERIFIED**.

Provenance: source-only Class A independent engineering return, 5 Nov 2026; initial COM main `46e240c55c07541ec57a98172ae1bff09a021a40`, compact COMHEADS blob `e436ebad7ef27a71c4b4dc915be905e8ef5ae4c7`, charter COM #887. Distinct from Build's case-import and Workshop integration, Codex's private native work, Claude Code's STOP-window work, the earlier YAC public-delta comparator and Passage brief. Optional noncanonical experiment; no main merge, publishing, provider, YAC, VM, rights or licence changes.


## Optional static HTML reader (7 November 2026)

For a side-by-side, printable offline HTML report, run:

    python3 html_report.py old.json revised.json --output comparison.html

Open the resulting local HTML file. Add --summary to suppress authored paths, values and file-byte fingerprints (counts can still reveal information), or --exact-row-moves to retain the opt-in pure-row-reorder distinction. This is an additive reader of the same compare.py parser/diff: it does not change the original plain-text CLI or its bounds. --output is atomic and refuses either input path as its destination. Without it, HTML is printed to stdout (do not redirect over a source file).

The HTML has no JavaScript, linked scripts/styles, uploads, network assets or telemetry. Authored JSON paths and values are rendered as escaped, quoted text; the displayed before/after values can contain private participant text. A hash fingerprints bytes, not authorship. A submitted label (observed, executed, open, etc.) remains unverified. REORDERED does not identify a person or event. Missing fields remain distinct from JSON null and explicit unknown. Use the separate original case-card validator for schema checks: this HTML view is not a schema validator, human impact study, nor truth/permission/correction detector.

Run python3 -m unittest -v test_html_report (10 synthetic Python standard-library checks). Tests cover escaping of forged headings/markup, summary privacy, exact reordered rows, absent/null/unknown, failed atomic write, inherited exponent-overflow refusal and inert HTML construction. A historical optional case-card intake fixture, blob f4167eb330897a5712c185f300225250ed6d70df, was separately checked with one author evidence-label edit and exact party order inversion: one CHANGED and one REORDERED; no world-state inference. No real browser or assistive-technology acceptance is claimed. Existing comparator source remains unchanged on this branch; parent includes Build's prior numeric-overflow correction at a7a40601aa41383e30fcc30b2028554ea5ba14e3.

This is a source-only optional reader prototype, not a canonical adoption, release or deployment.

## Windows entry and portable kit (9 November 2026)

See [START HERE.txt](START%20HERE.txt). With an existing Python 3.10+, double-click
`Review drafts.cmd`, drag the older JSON file into its prompt and press Enter,
then do the same for the newer file. A new `draft-review-*` folder beside the
newer draft contains `comparison.html`. Each run gets a separate folder; neither
input nor an earlier report is replaced. The program opens no browser and sends
no data. `Review counts only.cmd` omits authored report values, paths and content
fingerprints; counts remain potentially sensitive.

The small `review_drafts.py` entry reuses the existing parser and HTML renderer.
It is also usable with explicit command-line paths. Parsing/rendering completes
before an output folder is created; an empty newly created folder is removed if
writing fails. Same-file selections and cancelled prompts produce no report.

Build a new offline folder plus ZIP with `python make_portable.py NEW_FOLDER`.
The package uses an explicit file allowlist and includes fictional inputs, a
generated example report and a file manifest. Existing destinations are refused.
Run `python -m unittest discover -p 'test_*.py' -v` for the full source suite.
The new tests cover the actual Windows console entry with redirected input;
mouse drag gestures, browser rendering and independent reader benefit remain
unobserved. No new case schema or ethical evaluator is introduced.

## Numeric preservation guard (9 November 2026)

The reader refuses a decimal number if parsing it as a Python float and rendering
that float would change its decimal value. Otherwise, distinct inputs such as
`1e-4000` and `0.0`, or two long decimal fractions, could silently compare equal.
Ordinary round-trippable decimals and exact large integers remain supported;
insignificant numeric formatting is still not a byte-level edit. This is a
restricted numeric reader, not arbitrary-precision JSON comparison. For values
outside that range, use a decimal-aware specialist diff rather than changing the
authored value to get past the guard.

Both text and HTML CLIs, including summary mode, fail with a value-free error
before replacing an existing report. Run `python -m unittest -v
test_numeric_precision` for the seven additional regression methods. These tests
use synthetic inputs and establish no case-schema or real-world claim validity.


## Summary-linkability correction (8 November 2026)

The original text and HTML `--summary` modes suppressed field text but still displayed deterministic SHA-256 hashes of the complete private drafts. Those hashes can act as linkable identifiers and, for guessable inputs, may support offline content guesses. Both optional reports now omit file hashes **only** in summary mode. Full reports retain hashes so readers can compare exactly which input bytes they used. Summary counts remain share-sensitive and do not anonymise participant or case metadata. The parser, bounded comparison, atomic writer and nonfinite-number rejection are unchanged.

Test-first local source evidence: against exact `590458845979129b2c2099b712ea12ee034b73c3`, `python3 -m unittest -v test_private_summary` initially failed 4 of 7 tests because hashes remained in summaries. After the change 7/7 synthetic Python checks pass, including both real CLI entry points, regular detailed output, no-delta honesty and atomic refusal. No browser/screen-reader/human study, canonical integration or release is claimed. Run `python3 -m unittest -v test_private_summary` to repeat.

## Static HTML report size guard (optional, 9 November 2026)

`python3 html_report.py old.json revised.json` limits its resulting HTML to **2 MiB of UTF-8**. Even a valid small JSON input can expand into a much larger HTML report when many changes repeat a long shared JSON Pointer path. This guard fails closed rather than silently cutting off authored differences. An over-budget `--output` leaves any earlier report unchanged, and the error does not print input paths or values. Use `--summary` for small counts-only HTML (counts are still potentially sensitive), or a specialist diff when complete detail is necessary. The text comparator retains its prior behaviour; this is not schema validation or proof of real-world events.

Run `python3 -m unittest -v test_html_budget` for the four additional synthetic regressions, including the over-budget path, retained output, summary and ordinary escaped detail. Local `file://` browser rendering and actual reader benefit remain unverified.
