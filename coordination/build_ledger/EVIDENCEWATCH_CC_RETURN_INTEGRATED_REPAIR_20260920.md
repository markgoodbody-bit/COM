# EvidenceWatch — CC return integrated repair checkpoint

Date: 20 September 2026 — Europe/London morning

Status: **CC HOSTILE REVIEW PROCESSED / CODE REPAIRED / CODEX DELTA INTEGRATED / HOSTED GREEN / FINAL CC VERIFY PENDING**

## CC hostile return

COM #401 comment `5749193250` reviewed exact pre-repair head:

`ee362ce0105565815ad2695f12db0481fab5f638`

Verdict:

```text
REPAIR_BEFORE_RECORD
```

Material findings:
- B1 unbounded watch-lifetime discovery / recursive candidates / candidate alerts;
- B2 free-text paraphrase could advance canonical state;
- M1 repeated authority outage alert storm;
- M2 concurrent processes could double work/alerts;
- M3 torn trailing JSONL line prevented restart;
- M4 candidates could emit independent-support alerts before promotion.

## Framework integrated repair

Current PR #248 exact head:

`0950d630cc4b72b8a90e4875976dac2f562670ef`

Hosted:

`campfire-ci 1612 / 35505830988 — SUCCESS`

Repairs now include:
- per-watch discovery cap;
- max 5 source additions per observation inside the cap;
- depth-1 candidate discovery;
- candidate sources cannot alert or establish canonical state;
- explicit config promotion required;
- configured source shape overrides older discovered-candidate shape;
- role + stateAuthority participate in observation fingerprint, so same-byte promotion re-analyses;
- candidate role is non-authoritative even if `stateAuthority:true` is malformed;
- typed material-state comparison uses status + normalised quantity;
- free-text proposition/scope/search-aperture paraphrase alone cannot advance/alert;
- authority advance requires correction relation or explicit material reasons;
- NVIDIA comparator temperature 0;
- authority outage/recovery alert on transitions rather than every heartbeat;
- single live writer per ledger;
- fsync-backed append;
- one torn trailing partial JSON line is dropped loudly while complete history remains usable;
- redirect final URL does not alter configured source fingerprint identity;
- first live tick failure is caught;
- reset route documented loopback/demo-only.

## Cross-aperture integration

Codex separately implemented B1/M4 in PR #251 and found one stronger edge:

```text
CANDIDATE OBSERVED
-> SAME BYTES
-> EXPLICIT CONFIG PROMOTION
-> MUST REANALYSE UNDER NEW ROLE/AUTHORITY
```

Framework integrated that edge into PR #248 and added:
- same-byte promotion regression;
- candidate-role authority-misconfiguration regression.

PR #251 was then closed as **integrated/superseded**, not merged.

## Evidence state

Pre-repair live NVIDIA/Anthropic witness remains attached to:

`ee362ce...`

Current repaired head:

`0950d630...`

has hosted regression evidence but **does not yet have a fresh live NVIDIA/web witness**.

Preserve:

```text
GREEN REGRESSIONS != REPAIRED-HEAD LIVE WITNESS
PRE-REPAIR LIVE WITNESS != CURRENT-HEAD LIVE WITNESS
```

Judge-facing docs now state that boundary and require:
- one off-camera repaired-head live re-witness;
- preserved heartbeat timestamps in the video;
- no live owner-page rerun on camera.

## Final CC closure route

Final exact verification request:
COM #401 comment `5749306750`

Requested verdict:

```text
CLEAR_TO_REWITNESS
or
REPAIR_BEFORE_REWITNESS
```

No general re-review.
No paid/network call by CC.
No submission authority.

## Current routing

```text
CC FINAL REPAIR VERIFY
-> IF CLEAR_TO_REWITNESS
   -> REPAIRED-HEAD OFF-CAMERA LIVE NVIDIA/WEB WITNESS
   -> VIDEO RECORDING
   -> FINAL PAYLOAD REVIEW
   -> MARK EXPLICIT SUBMISSION GATE

THR PR #70 / #72 = PARKED
FLAK = STOP
THR RECORD 5 = NOT EARNED
WORLD / REAL USE = PRIMARY OUTSIDE BOUNDED CLOSURE
```


## Final discovery-accounting repair

Codex reconciliation on COM #401 exposed two smaller B1 accounting defects after
the first integrated green head:

1. `NO_MORE_DISCOVERY` could be emitted at the 5-per-observation batch limit
   even while lifetime capacity remained.
2. repeated duplicate URLs in model output could append duplicate
   `SOURCE_ADDED` events.

Final repair:
- deduplicate eligible URLs before slicing;
- emit the lifetime-cap event only when `maxDiscoveredSources` is actually
  reached and otherwise-eligible URLs remain;
- regression covers 5/10 no-cap-event, later sixth addition, final 10/10 cap
  exhaustion, and unique SOURCE_ADDED URLs.

Final exact PR #248 head:

`529bdd8e31ac528490acb6791508c1c4df3f738d`

Hosted:

`campfire-ci 1614 / 35505985835 — SUCCESS`

Final CC bounded closure target:
COM #401 comment `5749321553`.

All previous verification-target comments are historical/superseded.


## CC closure verdict

Claude Code returned on COM #401 comment `5749323668` against exact functional
head `529bdd8e31ac528490acb6791508c1c4df3f738d`.

Verdict:

```text
CLEAR_TO_REWITNESS
```

CC reran the original hostile probes and observed:
- discovery growth: 781 -> 6;
- candidate material alerts: 190 -> 0;
- repeated authority outage alerts: 6 -> 1;
- torn trailing JSONL: startup failure -> complete prior history readable;
- B1 / B2 / M1 / M2 / M3 / M4 all CLOSED for the challenge's single-host shape.

CC also confirmed Codex's final discovery-accounting counterexamples closed.

Remaining M2 ceiling:
the PID lock is a local-host process guard, not a distributed lock for multiple
hosts sharing a network filesystem.

Framework applied that **documentation-only** ceiling after CC's functional
verification. No engine/test behavior changed.

Final branch/documentation head:

`00017d190bb6a9813cb64f1f30a17b27e4ce10ca`

Hosted:

`campfire-ci 1616 / 35506135667 — SUCCESS`

COM #401 was then closed as completed.

## Current real gate

```text
CODE REVIEW = CLOSED
HOSTILE COUNTEREXAMPLES = CLOSED FOR CURRENT CHALLENGE SHAPE

NEXT
-> OFF-CAMERA REPAIRED-HEAD LIVE NVIDIA + PUBLIC WEB WITNESS
-> SAME LEDGER SECOND RUN
-> VERIFY QUIET / DEDUPE / CANONICAL STATE
-> ONLY THEN RECORD VIDEO
-> FINAL PAYLOAD REVIEW
-> MARK EXPLICIT SUBMISSION GATE
```

The current repaired branch has **not yet** been re-witnessed against NVIDIA and
the live Anthropic pages.

`CLEAR_TO_REWITNESS != CLEAR_TO_RECORD != CLEAR_TO_SUBMIT`
