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

A council adult-social-care case note contains a material factual error. A practitioner reviewed it before it entered the record, but the error survived. A later needs assessment was completed after the note entered the case record. The factual error is now established and the official record can be corrected. The note was also sent to one external agency.

Neutral question:

> What is the smallest useful next action now, and what evidence would change your answer?

Treatment prompt:

> After correcting a material source, check whether any still-consequential assessment, plan, risk judgement or action relied on the bad source. If so, route only that act to its existing accountable owner for reconsideration.

This is the surviving small join under COM PR #100. It creates no new duty and does not prescribe the owner's decision.

### B — shared energy fallback under Hormuz disruption

During a severe disruption in the Strait of Hormuz, a planning team says regional hydrocarbon exports remain resilient because Saudi and UAE pipelines can bypass the strait. Its briefing cites headline oil-pipeline capacities and treats them as sufficient evidence that the regional fallback is adequate.

Neutral question:

> What is the smallest useful next action now, and what evidence would change your answer?

Treatment prompt:

> Before relying on the backup, ask who else needs it in the same bad world, what shared bottleneck limits it, whether it can actually be delivered in time, and who allocates it if demand exceeds supply.

This is the unresolved activation-only remainder under COM PR #101. Energy-security owners already contain the substantive mechanics.

The plain case deliberately does **not** list the owner-critical gaps below. Earlier wording named reliance uncertainty in Case A and enumerated utilisation/logistics/concurrency/LNG gaps in Case B; that was rejected before use because it pre-activated the control arm.

## Current owner basis for the case design

Recheck before a real run.

- NHS England's current record-amendment guidance says inaccurate information may need to remain visible because professionals may have read or relied on it; information-governance staff should consider who viewed it and possibly relied on it in care/treatment decisions.
- The IEA Strait of Hormuz factsheet says about 20 mb/d of oil transited the strait in 2025 versus an estimated 3.5–5.5 mb/d of available crude bypass capacity; it warns that rerouting logistics/supply chains have not been robustly tested and that Gulf LNG has no equivalent route to market.

Owner links:
- https://transform.england.nhs.uk/information-governance/guidance/amending-patient-and-service-user-records/
- https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz

## Design

Use the local `probe.html` file. It has no network calls, telemetry, external assets or persistent browser storage.

Each participant is randomized once to a **session arm**:

- `PLAIN`: both cases are shown without the activation prompts; or
- `PROMPT`: each case is shown with its small case-specific activation prompt.

Case order is randomized independently.

This between-participant arm is deliberate. An earlier crossed design gave each person one prompted and one plain case; that was rejected before use because a prompt seen first could teach/prime the later `PLAIN` response and contaminate the control.

Before each case, title, facts, treatment and question remain hidden. The participant's `Reveal and start this case` click both starts the timer and reveals the case. The PROMPT arm's extra reading time therefore remains part of the treatment burden rather than occurring before the clock.

Elapsed time is only a proxy for time to first submitted answer. It includes reading and typing; it is not a direct timestamp of when an owner-critical insight occurred.

Results export as a local JSON file after both first answers are submitted.

The runner does not request a participant name or code and does not export wall-clock timestamps. A random session ID is sufficient to keep the two responses paired. Participants should still avoid putting identifying information into free-text answers.

The participant should not be told the desired answer or shown the scoring rubric before answering.

Compare `PLAIN` versus `PROMPT` **within the same case across participants**. Randomized case order can be inspected as a possible order/fatigue effect; do not silently pool it away if it matters.

For the first smoke test, collect at least four completed participants in each session arm before inspecting answer quality: minimum 8 participants, yielding at least four PLAIN and four PROMPT first attempts for each case. This is only a tiny feasibility batch, not a powered statistical design.

## Scoring after collection

Score from the answer alone, blinded to arm where practical.

### Case A owner-critical observations

1. correct/annotate the established factual error through the existing record owner and address the external copy through the relevant owner process;
2. ask whether the later assessment materially relied on the inaccurate fact rather than assuming either reliance or independence;
3. if material reliance is found, route that assessment to its existing accountable owner for recorded reconsideration rather than automatically reversing it;
4. distinguish `no material reliance found` from `reliance cannot be established from available records` when evidence is incomplete.

### Case B owner-critical observations

1. do not equate headline/nameplate bypass capacity with currently available sustainable/exportable supply;
2. ask for current utilisation, sustainable flow and conversion/export/logistics evidence before relying on the fallback;
3. test joint availability / simultaneous claimants under the same disruption;
4. surface the allocation/authority question if joint demand exceeds deliverable capacity;
5. keep physically non-substitutable flows such as LNG separate rather than laundering them into generic `energy capacity`.

## Primary comparison

For each case separately compare `PLAIN` versus `PROMPT` on:

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

`POSSIBLE_ACTIVATION_DELTA` requires an action-relevant owner-critical observation to appear more reliably or materially earlier in the prompted arm **for the same case**. Mere extra detail does not count.

## First-run ceiling

A small first batch is a smoke test only. Do not infer population efficacy, professional usefulness, or TRACE/ME validation from it.

Because the treatment prompts intentionally name case-specific owner-critical checks, a positive result can establish only changed first-answer behaviour on these cases. It cannot by itself establish transfer to a novel case or general framework efficacy.

If plain answers already reach the owner-critical action with equal or lower burden, preserve the null and close/shrink the relevant activation claim.

If the prompt causes unnecessary tracing, confident invention, delay, or authority creep, count that as adverse evidence.

If a signal appears, the next step is a better transfer/real-user test with the relevant owner/professional population—not more project-internal model review.

## Boundaries

- no provider spend is required;
- no Square actuation;
- no credentials;
- no server or database;
- do not collect participant names or identifiers;
- no TRACE/ME/Campfire/source mutation follows from a result;
- PR #100 and #101 remain separate objects and are not merged by this experiment;
- owner methods remain authoritative for domain decisions.

If a material owner fact changes, freeze a new case version rather than silently changing the answer key.
