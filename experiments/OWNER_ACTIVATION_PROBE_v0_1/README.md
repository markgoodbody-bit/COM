# OWNER ACTIVATION PROBE v0.1

Status: **DRAFT / LOCAL FIELD TEST / NOT CANON / NOT TRACE OR ME CHANGE / NO EFFICACY CLAIM**
Date: 2026-09-04 Europe/London

## Question

Current project evidence has repeatedly reached the same narrow remainder:

> strong domain owners already contain the substantive method; the unresolved question is whether a tiny prompt helps a competent non-specialist reach the relevant owner analysis sooner or more reliably.

This probe tests that remainder directly.

It does **not** test semantic novelty, framework superiority, moral truth, professional competence, or whether TRACE/ME should expand.

```text
OWNER_METHOD_EXISTS != OWNER_METHOD_ACTIVATED_IN_TIME
PROMPT_CHANGES_WORDING != PROMPT_CHANGES_ACTION
FASTER != BETTER_IF_IT_OVERFIRES
ONE SMALL TEST != EFFICACY
```

## Cases

### A — corrected social-care source

A council adult-social-care case note contains a material factual error. A practitioner reviewed it before it entered the record, but the error survived. A later needs assessment relied on the note. The factual error is now established and the official record can be corrected. The note was also sent to one external agency.

Neutral question:

> What is the smallest useful next action now, and what evidence would change your answer?

Treatment prompt:

> After correcting a material source, check whether any still-consequential assessment, plan, risk judgement or action relied on the bad source. If so, route only that act to its existing accountable owner for reconsideration.

This is the surviving small join under COM PR #100. It creates no new duty and does not prescribe the owner's decision.

### B — shared energy fallback under Hormuz disruption

During a severe disruption in the Strait of Hormuz, a planning team says regional oil exports remain resilient because alternative pipelines can bypass the strait. Current owner analysis says normal Strait flows are much larger than available bypass capacity; sustainable throughput can be below nameplate; rerouting logistics can constrain use; and regional LNG has no comparable bypass route.

Neutral question:

> What is the smallest useful next action now, and what evidence would change your answer?

Treatment prompt:

> Before relying on the backup, ask who else needs it in the same bad world, what shared bottleneck limits it, whether it can actually be delivered in time, and who allocates it if demand exceeds supply.

This is the unresolved activation-only remainder under COM PR #101. Energy-security owners already contain the substantive mechanics.

## Design

Use the local `probe.html` file. It has no network calls, telemetry, external assets or persistent browser storage.

Each participant receives both cases in a crossed order:

- one case `PLAIN`;
- one case `PROMPT`;
- assignment is randomized locally;
- response time begins only when the participant starts a case;
- results export as a local JSON file after both first answers are submitted.

Do not identify participants by real name. Use a disposable participant code if needed.

The participant should not be told the desired answer or shown the scoring rubric before answering.

## Scoring after collection

Score from the answer alone, blinded to arm where practical.

### Case A owner-critical observations

1. correct the established factual error / propagate correction to the external recipient as required by the relevant owner process;
2. identify the later assessment as a still-consequential dependent act;
3. route that assessment to its existing accountable owner for recorded reconsideration rather than automatically reversing it;
4. distinguish `no material reliance found` from `reliance cannot be established from available records` when evidence is incomplete.

### Case B owner-critical observations

1. do not equate nameplate bypass capacity with sustainable/exportable supply;
2. test joint availability / simultaneous claimants under the same disruption;
3. test conversion, logistics and delivery before treating the fallback as usable;
4. surface the allocation/authority question if joint demand exceeds deliverable capacity;
5. distinguish oil bypass from LNG where the physical route differs.

## Primary comparison

For each case compare:

1. consequential next action / owner / hold / reopen condition;
2. owner-critical observation count;
3. material false activation or invented authority;
4. elapsed seconds to first submitted answer;
5. response length as a crude burden indicator.

Do not score project vocabulary use.

## Allowed dispositions

```text
NO_MATERIAL_DIFFERENCE
POSSIBLE_ACTIVATION_DELTA
PROMPT_OVERFIRE
PLAIN_ALREADY_SUFFICIENT
INCONCLUSIVE
MALFORMED_CASE
```

`POSSIBLE_ACTIVATION_DELTA` requires an action-relevant owner-critical observation to appear in the prompted arm that is absent or materially later in the comparable plain arm. Mere extra detail does not count.

## First-run ceiling

A small first batch is a smoke test only. Do not infer population efficacy, professional usefulness, or TRACE/ME validation from it.

If plain answers already reach the owner-critical action with equal or lower burden, preserve the null and close/shrink the relevant activation claim.

If the prompt causes unnecessary tracing, confident invention, delay, or authority creep, count that as adverse evidence.

If a signal appears, the next step is a better real-user test with the relevant owner/professional population—not more project-internal model review.

## Boundaries

- no provider spend is required;
- no Square actuation;
- no credentials;
- no server or database;
- no participant PII should be collected;
- no TRACE/ME/Campfire/source mutation follows from a result;
- PR #100 and #101 remain separate objects and are not merged by this experiment;
- owner methods remain authoritative for domain decisions.

## Current source anchors

- COM PR #100 — social-care correction consequence check.
- COM PR #101 — shared correction-capacity stress route.
- NHS England record-amendment guidance — consider who viewed/reied on inaccurate health/care information when correcting records.
- IEA 2026 Strait of Hormuz factsheet — normal flows, bypass-capacity limits, sustainable/logistical constraints and LNG route limits.

Use current owner sources when scoring a real run. If a material owner fact changes, freeze a new case version rather than silently changing the answer key.
