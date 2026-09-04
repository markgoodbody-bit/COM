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

The case does **not** establish whether or how much the later assessment relied on the inaccurate fact. That is deliberately left for the participant to notice or investigate.

Neutral question:

> What is the smallest useful next action now, and what evidence would change your answer?

Treatment prompt:

> After correcting a material source, check whether any still-consequential assessment, plan, risk judgement or action relied on the bad source. If so, route only that act to its existing accountable owner for reconsideration.

This is the surviving small join under COM PR #100. It creates no new duty and does not prescribe the owner's decision.

### B — shared energy fallback under Hormuz disruption

During a severe disruption in the Strait of Hormuz, a planning team says regional oil exports remain resilient because Saudi and UAE pipelines can bypass the strait. Its briefing cites headline pipeline capacities but does not reconcile those figures with current utilisation, sustainable operating flow, export/logistics constraints, simultaneous demand for the same routes, or what happens to Gulf LNG that has no equivalent bypass.

Neutral question:

> What is the smallest useful next action now, and what evidence would change your answer?

Treatment prompt:

> Before relying on the backup, ask who else needs it in the same bad world, what shared bottleneck limits it, whether it can actually be delivered in time, and who allocates it if demand exceeds supply.

This is the unresolved activation-only remainder under COM PR #101. Energy-security owners already contain the substantive mechanics.

## Current owner basis for the case design

Recheck before a real run.

- NHS England's current record-amendment guidance says inaccurate information may need to remain visible because professionals may have read or relied on it; information-governance staff should consider who viewed it and possibly relied on it in care/treatment decisions.
- The IEA Strait of Hormuz factsheet says about 20 mb/d of oil transited the strait in 2025 versus an estimated 3.5–5.5 mb/d of available crude bypass capacity; it warns that rerouting logistics/supply chains have not been robustly tested and that Gulf LNG has no equivalent route to market.

Owner links:
- https://transform.england.nhs.uk/information-governance/guidance/amending-patient-and-service-user-records/
- https://www.iea.org/about/oil-security-and-emergency-response/strait-of-hormuz

## Design

Use the local `probe.html` file. It has no network calls, telemetry, external assets or persistent browser storage.

Each participant receives both cases in a crossed order:

- one case `PLAIN`;
- one case `PROMPT`;
- assignment and case order are randomized locally;
- response time begins only when the participant starts a case;
- results export as a local JSON file after both first answers are submitted.

Do not identify participants by real name. Use a disposable participant code if needed.

The participant should not be told the desired answer or shown the scoring rubric before answering.

Important analysis boundary: because each participant sees different cases under different arms, **do not** treat one participant's prompted Case A versus plain Case B as a causal comparison. Compare `PLAIN` versus `PROMPT` **within the same case across participants**. The crossed design reduces participant-level burden and exposes order, but it does not make the two cases interchangeable.

For the first smoke test, collect without inspecting answer quality until each case has at least four first attempts in each arm. Randomization may require more than eight participants. This is only a stopping rule for a tiny feasibility batch, not a powered statistical design.

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

If a material owner fact changes, freeze a new case version rather than silently changing the answer key.
