# TRACE-oriented human case card (independent optional experiment)

Status: isolated SOURCE-TESTED draft, NOT a TRACE implementation, release, deployment, licensed derivative text or external-reader validation.

## Purpose

Produce a small human-readable, printable HTML card from a locally authored JSON case. It preserves bounded change claims, each party's own aims/boundaries, constructive possibilities, correction-window uncertainty and an explicit return. It assigns no ethical ranking, truth, authority, consent, actor identity, model agency, calendar feasibility or outcome worth. Prefer an ordinary incident record or specialist tool whenever that is simpler.

It is an **original, source-only formatter**, inspired by the released [TRACE v0.5 research specification (27 October 2026)](https://github.com/markgoodbody-bit/TRACE/releases/tag/v0.5.0). That specification is not an executable JSON grammar and makes no claims of established efficacy. No TRACE, ME, licensing or canon change is made here.

## Run locally

Requires Python 3.10+; only the standard library.

1. From this directory run: python3 case_card.py examples/bus_stop.json --output /tmp/bus-stop-case.html
2. Open /tmp/bus-stop-case.html in your browser, or open examples/bus_stop.html, the checked-in deterministic render.
3. Run tests: python3 -m unittest discover -s tests -v

The example bus stop, its people, notices and clocks are synthetic, **not real transport evidence**. All user-authored text is HTML-escaped. The HTML contains no JS, uploads, external assets, telemetry, forms, or network requests. It includes one ordinary external link to the public TRACE spec; loading the card never fetches it automatically. Never disclose private participant text in a shared HTML file.

The tool reads stdin if the filename argument is omitted or given as a single hyphen. By default it writes HTML to stdout. The optional --output writes a temporary local file and atomically replaces the destination only after successful validation; existing files are untouched if validation fails. Plain shell redirection to a destination may truncate that file before validation, so prefer --output.

## JSON inputs

The fixture examples/bus_stop.json shows the schema. Unknown keys are rejected, not ignored. Required title (string); optional scope. Required claims (one to 24 records, at least one kind=change): each record has kind [baseline, change, consequence], exact text, evidence [observed, reported, inferred, disputed, unknown], optional source. **All evidence labels and sources are supplied by the author**; observed does not mean independently verified.

Optional parties list: name, optional aim and boundary. A missing party list does not prove no affected party. Optional possibilities list: party, description, state [possible, offered, permitted, chosen, attempted, executed], optional condition. The renderer explicitly differentiates possible from permitted, chosen, attempted or completed; these states are not independently established.

Optional correction object: target, route, hardening, clock_basis, window and basis. Window may be not_assessed, unknown, open or closed. To author a claimed open/closed window all five other fields must be provided, but the resulting label still says submitted claim/unverified. Completeness is not proof of clock alignment, deadline feasibility or correctness. Without a correction section the window is not assessed or supplied, not silently closed.

Optional return: learned, unresolved, next. The author is responsible for whether these statements follow from evidence.

Input bounded to 128 KiB, up to 24 rows per list, 2,000 characters per ordinary field (lower caps for short fields). Rejects duplicate keys, non-finite numbers, unknown enums, unbounded fields, invalid Unicode surrogate and selected directional format controls. HTML/Markdown-like forged headings and links remain text, not DOM elements. The formatter does not rewrite author text or add facts.

## Evidence ceiling and project boundary

All tests use synthetic cases and run on local Python 3.13.5. They cover input validation, duplicate-key handling, hostile headings/markup, evidence-status preservation, absent versus unknown, author-supplied correction-window claims, deterministic static output, CLI success and failure-safe replacement. They do **not** establish accessibility compliance, independent reader value, provenance authentication, complete adversarial input robustness, or any world change.

Local development preserved an initial red test because case_card.py was absent (ModuleNotFoundError). A first implementation run uncovered a case-sensitive fixture expectation; a source review then fixed an actual semantic issue where a literal source string "Not supplied" would have been rewritten. All 18 final regression tests passed, including the escaped-source regression.

Source anchors: COM main 352452def90ac75907b6a19aefa1e8735aec46f7; complete compact COMHEADS blob 7e64afc15483e067a64b030ff9b38a84f1625bbd; engineering charter COM issue #887, 28 Oct 2026. This distinct unit neither duplicates Build's PSFH/YAC screening custody, Codex's YAC private HOLD, CC's work, the prior Passage brief, YAC readers, Workshop adapter, nor COMHEADS locator. No private inputs, native Workshop/VM work, credential/provider action, deployment, release, merge, spending or public YAC writing occurred. Build can review or reject this noncanonical option; no COM message wakes another model.
