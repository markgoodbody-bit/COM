# Offline fill-in companion to the independent human case card (30 October 2026)

**Status: noncanonical Class A source-only draft, not deployed and not a TRACE/ME implementation or release.** This is an additive, original authoring interface to the existing experimental `case_card.py` from [case-card source commit f862b506](https://github.com/markgoodbody-bit/COM/commit/f862b506c168a97c7f0ff0ab007a95e60caa2922). It is for someone who wants to describe a change and potential correction without hand-writing the Python renderer's JSON fields. The form does **not** evaluate ethical worth, authenticate sources, prove evidence, make a legal deadline assessment or validate actual correction reachability.

## Use

Keep `case_intake.html` and `case_intake.js` together. Open the HTML locally in a conventional browser. Fill in the title and at least one **change** claim with a manually chosen evidence label. Optional rows let the author describe independently held aims, boundaries, possible alternatives, and correction questions. Use **Check and download JSON** to save a local JSON document. Neither the web form nor its JS library uploads content, sends network requests, stores it persistently, or uses analytics. The HTML includes a click-only link to the public GitHub source; it is not automatically fetched.

To make a printable card, use the Python renderer already in this prototype directory:

`python3 case_card.py examples/library_form.json --output library-card.html`

Or replace `examples/library_form.json` with the newly downloaded `case-card-draft.json`. `case_card.py` is the separate original program, not built into the authoring form. Do not share the JSON or resulting HTML if they contain sensitive information. No autosave: **download a JSON file before leaving the tab**. You can reimport that saved file to edit it later. Browsers differ in their local-file and download policies, so a filesystem/browser-specific refusal may still occur.

All factual claims and evidence-status choices remain the writer's assertions. "Observed" is not authenticated; "executed" is not independently confirmed. The default correction window is *not assessed*, omitted when no correction detail exists. A user-claimed open/closed window requires all five basis fields, but this does not establish the reality of any deadline, permission or remedy. If ordinary incident reporting or a specialist tool is simpler, use that instead.

## Controls and compatibility boundary

- No dependencies for normal browser use. HTML uses a separate **local** script file and standard DOM input elements; user text is set through `.value` / `.textContent`, not raw HTML interpretation.
- The form creates the renderer's top-level `title`, optional `scope`, required `claims`, and optional `parties`, `possibilities`, `correction`, and `return`. It deliberately uses the renderer's existing enum terms and maximum single-field lengths, and preserves author-entered whitespace rather than trimming meaningful text. Empty optional fields and rows are omitted, but incomplete filled rows are refused rather than silently dropped.
- JSON import rejects unexpected keys, wrong types/enums, duplicate keys, selected bidirectional formatting controls, malformed Unicode, overlong fields, excessive rows/nesting and oversized input. The original Python renderer remains the authoritative parser when generating HTML.
- Export checks the **pretty-printed file** against the original renderer's 128 KiB input ceiling. This corrects an initially omitted export-size case discovered in local source review; the regression was added before final verification.
- `examples/library_form.json` is fiction. No actual library, passenger, policy, incident, person or correction clock is asserted.

## Tests and observed limits

From this directory: `node --test tests/test_intake.cjs` (Node 22 tested). **24/24 passed**. First test invocation before implementation was RED (`Cannot find module '../case_intake.js'`, 0/1 passed). First full implementation run was 23/23 pass. An additional export-size regression initially failed because its fixture was too small; the fixture was corrected to distinguish compact from pretty JSON, and final 24/24 pass. Do not treat a bad fixture as a source defect.

Optional smoke: `python3 tests/browser_smoke_local.py` with Playwright and Chromium installed in the test environment. The first attempt to open `file://` was blocked by this sandbox's browser administrator (`ERR_BLOCKED_BY_ADMINISTRATOR`), not a demonstrated script defect. The same actual HTML+JS source was then loaded into a headless Chromium document **in memory**; local download, reimport, rejected duplicate-key import, exact hostile-looking text preservation, zero HTTP requests and zero page exceptions all **passed**. This does **not** establish that arbitrary browsers permit opening local files, full WCAG accessibility, screen-reader usability, or that the Python renderer has executed this exported fixture in this runtime.

This new interface does not modify any original card generator, README, example or regression tests. The prior 28-Oct prototype is source-tested and noncanonical. No public YAC call, private source transfer, credential, VM, model provider, live contact, spending, release, merge or deployment. No claimed real-world improvement or external validation.

**Exact acquisition anchors:** COM main `352452def90ac75907b6a19aefa1e8735aec46f7`, compact COMHEADS blob `7e64afc15483e067a64b030ff9b38a84f1625bbd`, source-work charter COM #887, source card `f862b506c168a97c7f0ff0ab007a95e60caa2922`; current owner returns Build #877 c6514307397, Codex #873 c6514307111, CC #874 c6486694175. The active Build/Codex work is private YAC API packaging/runtime and CC's separate research slice, not this form.

## 31 October 2026 compatibility correction and direct renderer test

The first independent cross-language run used the **exact original Python renderer** at blob `fea476ee242f74b519e2675b9e159d41e04a0df9`, rather than a mocked schema. The supplied fictional library example rendered successfully. Additive `tests/test_renderer_contract.cjs` calls that actual sibling `case_card.py` through `python3` (or `PYTHON`) and checks output escaping, evidence provenance, unsupported inference about correction windows and deterministic invalid-input refusal. The test intentionally pins the original renderer byte identity; when the renderer changes, review its contract and deliberately update the pin rather than silently accepting a different executable.

Two previously undetected source defects were reproduced with red tests before correction: JavaScript considered an author field containing only U+0085 (NEXT LINE) nonempty, whereas Python `str.strip()` rejected it; and a blank-looking row bearing an unexpected key could be silently discarded before validation. Both now fail closed. Source test runner `node --test tests/test_intake.cjs tests/test_renderer_contract.cjs`; current focused results are 26/26 JavaScript intake plus 4/4 direct renderer cases. These are source tests using fictional data, not accessibility, browser-local-file, human-outcome or external-validation evidence.

The original 30 October browser smoke result remains limited: the in-memory Chromium test passed; opening a real `file://` page was blocked by that test environment's administrator. No claim is made that all browsers permit local files or downloads. No renderer or historic fixture was modified by this patch.
