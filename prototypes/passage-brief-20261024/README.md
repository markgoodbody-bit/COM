# Passage brief — optional offline projection, 24 October 2026

Status: CLASS A, isolated and noncanonical. Not adopted, released, deployed, integrated with the Passage HTML interface, an evidence certificate or an ethical decision engine.

Purpose: offer a genuinely short, reversible presentation of existing writer-entered Passage v0 notes. The historical public Passage engine is visible at COM commit dad08b0845ad82ed35f3f26667ddf41131fc2d8a, original source files prototypes/passage-v0/index.html and START_HERE.txt, blobs 07d2cca75b351a3d130669e18e0fd61e6b16d657 and fff0ea01c5a5e45427d71a44e3160614dbc589a0. At this run's main head, that directory was absent. This isolated directory intentionally does not restore the original HTML or copy Codex's separately staged private CHANGE repair.

The formatter recognises exactly the public Passage v0 JSON schema and 16 named fields. It emits only nonempty writer notes and the minimal unverified/authority boundary; a possibility is writer-proposed, not judged worthwhile. Evidence labels including OBSERVED are explicitly writer-labelled, not independently confirmed. Each writer field is one reversible JSON-quoted physical line; CR/LF/NEL, Unicode paragraph separators and bidi controls cannot mint top-level headings. Whitespace-only fields are treated as unsupplied. No permission, specialist judgement, causality, open correction window or achieved outcome is inferred. Where better domain guidance exists, use it instead.

Use locally with Node 20+ from this directory:

    node --test brief.test.mjs
    node brief.mjs example.json

The tool reads exactly the nominated local file, writes text to stdout, and performs no network calls or automatic storage. Review output before sharing; saved files may contain private text. It is also a side-effect-free importable module exposing parseSaved, normalise and renderBrief.

Reference problem: Codex COM #873 comment 6350505294 measured a DIFFERENT 99-character note yielding 1,435 output characters in the historical verbose formatter. This separate synthetic 99-character three-field input produces 397 characters locally; it is not the same test input or a human usability evaluation. First local run: 13 of 14 passed; the failure was an incorrect synthetic fixture assertion (140 characters counted, 143 expected), not code. The fixture was replaced with an actual 99-character case and retested successfully.

Limits: local Node tests only. No original HTML integration, browser/keyboard/assistive-tech trial, native Workshop VM execution, hosted acceptance, reader comparison or evidence of better real decisions. Owner reconciliation with the separately staged Passage candidate is needed before adoption. No private Codex/CC material is copied or published here.
