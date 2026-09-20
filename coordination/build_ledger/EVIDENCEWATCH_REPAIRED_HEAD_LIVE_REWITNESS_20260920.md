# EvidenceWatch — repaired-head live re-witness

Date: 20 September 2026 — Europe/London

Status: **REPAIRED-HEAD LIVE NVIDIA + PUBLIC WEB WITNESS PASS_WITH_CEILING**

## Exact local source

Mark ran from:

`framework/nvidia-claw-evidencewatch-20260919`

and verified:

`git rev-parse HEAD = 00017d190bb6a9813cb64f1f30a17b27e4ce10ca`

The branch had been fast-forwarded from `ee362ce...` to the final repaired
documentation head.

NVIDIA key handling:
- key already existed in Mark's PowerShell session;
- it was not pasted to chat or GitHub;
- run used `nvidia/nemotron-3-super-120b-a12b`.

## Clean first run

Mark set:

`EVIDENCEWATCH_RESET=1`

Then ran the bounded live heartbeat.

Observed:

```text
anthropic-july-2026
-> BASELINE_ESTABLISHED
-> relation baseline
-> quantity 3
-> discovered one candidate:
   https://www.anthropic.com/transparency

anthropic-september-2026
-> MATERIAL_DELTA
-> relation correction
-> quantity 4

canonical quantity -> 4
alerts total -> 1
new alert kind -> correction
dependent briefing -> flagged for review
EVIDENCEWATCH_LIVE_ONCE_OK
```

No source error.

The current canonical state after the correction was:
- proposition: Anthropic has publicly identified four real-world cybersecurity evaluation incidents;
- quantity: 4;
- scope: real-world cybersecurity evaluation incidents;
- search aperture: Anthropic cybersecurity evaluation incidents.

Model-supplied `status` was `contradicted`; see semantic ceiling below.

## Same-ledger second run

Mark removed `EVIDENCEWATCH_RESET` and ran the same bounded live heartbeat again.

Observed:

```text
anthropic-july-2026
-> DUPLICATE_OBSERVATION

anthropic-september-2026
-> DUPLICATE_OBSERVATION

discovered-b9e7915be186
-> NO_MATERIAL_DELTA
-> relation independent
-> quantity null
-> addedSources []

canonical quantity -> 4
observations -> 3
alerts total -> 1
newAlerts -> []
EVIDENCEWATCH_LIVE_ONCE_OK
```

This is important:
- both configured owner sources deduplicated;
- no repeated material alert occurred;
- the discovered candidate was fetched/analyzed on the next run;
- candidate quarantine held: it produced NO_MATERIAL_DELTA, no alert, no
  canonical advance, no recursive discovery.

## Re-witness result

```text
REAL PUBLIC OWNER FETCH = PASS
REAL NVIDIA NEMOTRON CALL = PASS
BASELINE 3 = PASS
OWNER CORRECTION 3 -> 4 = PASS
DEPENDENT REVIEW ROUTING = PASS
SAME-LEDGER CONFIGURED-SOURCE DEDUPE = PASS
NO DUPLICATE ALERT = PASS
DISCOVERED CANDIDATE QUARANTINE = PASS
REPAIRED-HEAD LIVE-ONCE COMPLETION = PASS
```

Therefore:

`REPAIRED_HEAD_LIVE_REWITNESS = PASS_WITH_CEILING`

## Semantic ceiling

The model returned:

```text
proposition = "... four ... incidents"
status = "contradicted"
quantity = 4
relation = correction
```

That `status` label is semantically awkward because the returned proposition
itself states the four-incident source claim. The browser demo does not display
`currentState.status`; it displays quantity, scope, engine result status,
summary and alert before/after values.

The repaired engine also no longer advances canonical authority on free-text /
typed-state difference alone; authority advance requires explicit correction or
material reasons. So this label did not manufacture the witnessed correction or
a duplicate second-run alert.

Preserve:

```text
LIVE BEHAVIOUR PASS != EVERY MODEL FIELD SEMANTICALLY IDEAL
MODEL STATUS LABEL != ENGINE OUTCOME STATUS
CORRECTION RELATION + QUANTITY CHANGE = WITNESSED
STATUS "contradicted" = SEMANTIC ANOMALY TO DISPOSE BEFORE FINAL SUBMISSION
```

## Next

Before final recording/submission:
1. decide whether to tighten analyzer status semantics or document/remove that
   field from competition-facing claims;
2. if functional analyzer code changes, re-run the bounded two-pass witness;
3. if no functional change, preserve this as a nonblocking ceiling;
4. record video only against an exact green/witnessed head;
5. final payload review;
6. Mark explicit submission gate.

No submission occurred.
No public export occurred.
No credential was exposed.
