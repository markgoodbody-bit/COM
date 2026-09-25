# EvidenceWatch — selectable synthetic research demo

Date: 25 September 2026

Status: **MERGED / POST-MERGE CI PASS / SYNTHETIC RESEARCH FIXTURE / NOT LIVE SCHOLARLY EVIDENCE**

EvidenceWatch code state:
- PR #10: `Add selectable synthetic research demo fixture`
- merge SHA / private main at merge: `b4c8f2bbbca1ae6ad1a5caa16a95cc76ce1b1f1f`
- post-merge workflow: `36182946076 / SUCCESS`

What changed:
- deterministic demo fixtures are selectable through `EVIDENCEWATCH_SEQUENCE`;
- existing Anthropic cybersecurity fixture remains the default;
- new `examples/research-correction-sequence.json` is explicitly synthetic;
- UI can render fixture-specific metric label and fixture disclosure;
- `scripts/start-research-demo.ps1` launches the synthetic research fixture locally;
- browser regression pins baseline 1.8 -> derivative repetition/no alert -> publisher correction 1.2 + dependent living-evidence-brief review.

Hosted branch validation:
- successful run `36182819624`;
- **47 tests / 47 pass / 0 fail**;
- PowerShell helper parse step completed.

Failure history preserved:
- first run `36182562713` failed all three server tests after the server emitted its URL and exited;
- cause: server/CLI imported the new fixture loader but still used the old hard-coded sequence line; server then referenced undefined `sequencePath` in the startup log and crashed;
- Framework identified the stale line, corrected both server and CLI to actually call `loadFixtureSequence`, and reran the suite;
- no failed branch state was merged.

Preserve:
```text
FAILED CI != PRODUCT FAILURE HIDDEN
SYNTHETIC RESEARCH FIXTURE != LIVE SCHOLARLY SOURCE
SELECTABLE DEMO != RESEARCHER VALIDATION
DEFAULT FIXTURE PRESERVED != NVIDIA SUBMISSION CHANGED
47 TESTS PASS != SEMANTIC RELIABILITY PROVEN
```

The already-submitted NVIDIA artifact remains bound to its earlier frozen head and video receipt. This later demo work does not rewrite that submission.
