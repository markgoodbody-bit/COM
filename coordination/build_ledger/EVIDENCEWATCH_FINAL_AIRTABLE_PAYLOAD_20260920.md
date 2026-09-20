# EvidenceWatch — final Airtable payload draft

Date: 20 September 2026 — Europe/London

Status: **FORM COPY FINAL / VIDEO URL TBD / TERMS CHECKBOX + SUBMISSION HUMAN-GATED**

## Basis

Current standalone product source:

```text
repo: markgoodbody-bit/evidencewatch
visibility: PRIVATE
main: 79e4d5270844342b74fd4e0c1e2439ab17772dd6
hosted CI: 35508764265 / SUCCESS
runtime source snapshot with repaired-head live witness:
00017d190bb6a9813cb64f1f30a17b27e4ce10ca
```

Recording pack and final clinical UI are merged into standalone main. Current main includes:
- sanitised live-witness evidence;
- evidence-bound recording guide;
- deterministic demo launcher;
- PowerShell syntax parsing in CI;
- isolated demo-ledger/port launcher repair;
- clinical monitoring interface with visible Demo mode boundary.

The final UI pass did not change engine/analyzer/ledger/live-runner semantics.

## Identity / eligibility fields

Use the already-reviewed values in:

`coordination/build_ledger/NVIDIA_CLAW_AIRTABLE_FORM_MAPPED_20260919.md`

Do not duplicate identity/contact data into additional project artifacts.

Confirmed field dispositions:
- UK located: Yes;
- entrant: individual;
- Agent harness: Other;
- Industry: closest truthful technology/software/IT option;
- Terms: final human checkbox only after reviewing the final form state.

## Other harness

```text
Custom Node.js long-running agent using NVIDIA Build / Nemotron 3 Super
```

## Claw Agent Description — preferred

EvidenceWatch is a long-running agent for claims people have already relied on.
It fingerprints selected public sources, uses NVIDIA Nemotron to analyse bounded
source changes, preserves an append-only claim-level evidence state, separates
configured canonical authority from derivative/supporting sources, and routes
material corrections to downstream briefs or decisions that need another look.

In a real public-source witness it established an earlier owner-reported count of
3, detected a later owner correction to 4, produced one downstream-review alert,
then on a same-ledger second run deduplicated both configured owner sources with
no new alert. A discovered candidate was analysed but remained quarantined:
no canonical advance, no alert, no recursive discovery.

EvidenceWatch is not a truth oracle. Model analysis is kept separate from
configured source authority.

## Claw Agent Description — shorter fallback

EvidenceWatch monitors evidence behind claims that people have already relied on.
It uses NVIDIA Nemotron to analyse bounded source changes, preserves durable
claim-level state and correction history, and tells the user which dependent
brief or decision needs review. In a real public-source witness it tracked an
owner-reported count from 3 to a later correction of 4, raised one review alert,
then deduplicated unchanged configured sources on a same-ledger second run with
no new alert. Model analysis is not treated as truth or canonical authority.

## Challenge experience feedback — preferred

The challenge format was useful because it encouraged a genuinely long-running
agent rather than a one-shot wrapper, and NVIDIA Build made it straightforward
to test real hosted inference.

The biggest friction was documentation consistency. The supplied Official Rules
contained a UK/Spain wording conflict and a PST/BST/PDT deadline inconsistency,
while the registered London page was clearer. Future challenges would benefit
from one authoritative deadline/timezone and explicit guidance that a custom
long-running harness is acceptable alongside OpenClaw/NemoClaw examples.

The short demo requirement is a good constraint: it forced the project to make
the real user value visible rather than explaining architecture for its own sake.

## Challenge experience feedback — shorter fallback

Useful challenge format and a straightforward NVIDIA Build integration. The main
friction was inconsistent rules wording: UK vs Spain and PST vs the London
page's BST deadline. A single authoritative deadline/timezone and clearer
guidance for custom harnesses would help. The short demo requirement was useful
because it forced the product value to be shown quickly.

## Demo / project field

Preferred submission artifact:

```text
PUBLIC VIDEO URL = TBD
```

Use a 60–90 second public YouTube/Loom-style video after final credential/claim
review.

Do **not** provide the private GitHub repository as a judge-facing link unless
Mark separately authorises making an appropriate surface public.

Current private repository:

`https://github.com/markgoodbody-bit/evidencewatch`

is a build/audit surface, not currently a public submission URL.

## Demo claims allowed

The recording may truthfully show/say:

```text
DETERMINISTIC FIXTURE REPLAY
-> baseline 3
-> supplied derivative repetition stays quiet
-> later owner-reported count 4
-> dependent briefing flagged for review

EARLIER REAL LIVE WITNESS
-> public Anthropic owner pages
-> NVIDIA Nemotron inference
-> first run 3 -> 4 correction / one alert
-> same-ledger second run configured sources DUPLICATE_OBSERVATION
-> newAlerts []
-> discovered candidate NO_MATERIAL_DELTA / no alert / no recursion
```

The browser segment must be visibly labelled as a deterministic fixture replay,
not live retrieval or fresh model inference.

## Claims not allowed

Do not claim:
- production deployment;
- customers or user adoption;
- general classification accuracy;
- truth verification;
- independent verification of the fixture's derivative classification;
- that the underlying cybersecurity events changed when the reported count changed;
- superiority over most tools without comparative evaluation;
- novelty/firstness over page monitoring, provenance, retraction tracking,
  append-only logs or long-running agents;
- competition success before an award.

Preserve the known semantic ceiling:
the live model returned an internally awkward `status=contradicted` alongside
the four-incident proposition and correction relation. The browser does not show
that model field; the anomaly remains unresolved.

## Final human gates

```text
1. RECORD VIDEO
2. REVIEW FINISHED VIDEO
   - no credentials
   - no personal/private tabs
   - no unsupported claims
   - deterministic/live labels visible
3. UPLOAD VIDEO
4. INSERT PUBLIC VIDEO URL INTO FORM
5. REVIEW FINAL AIRTABLE VALUES + TERMS CHECKBOX
6. MARK EXPLICITLY AUTHORIZES SUBMISSION
7. SUBMIT
8. PRESERVE EXACT SUBMISSION RECEIPT
```

`PREPARED != SUBMITTED`
`VIDEO UPLOADED != FORM SUBMITTED`
`FORM FILLED != TERMS ACCEPTED`
`SUBMITTED != AWARDED`
