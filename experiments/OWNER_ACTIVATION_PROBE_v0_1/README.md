# OWNER ACTIVATION PROBE v0.1

Status: **DRAFT / LOCAL FIELD TEST / NOT CANON / NOT TRACE OR ME CHANGE / NO EFFICACY CLAIM**
Date: 2026-09-04 Europe/London

## Question

Current project evidence has repeatedly reached the same narrow remainder:

> strong domain owners already contain the substantive method; the unresolved question is whether a tiny prompt helps a competent non-specialist reach the relevant owner analysis sooner or more reliably.

This probe is a **feasibility step toward testing that remainder**, not an efficacy test by itself.

It does **not** test semantic novelty, framework superiority, moral truth, professional competence, or whether TRACE/ME should expand.

```text
OWNER_METHOD_EXISTS != OWNER_METHOD_ACTIVATED_IN_TIME
PROMPT_CHANGES_WORDING != PROMPT_CHANGES_ACTION
FASTER != BETTER_IF_IT_OVERFIRES
FEASIBILITY_SIGNAL != EFFICACY
ONE_SMALL_TEST != GENERAL_TRANSFER
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

## Method owner check

This is not being claimed as a clinical RCT, but established pilot/feasibility-trial guidance is useful owner pressure on the design.

The CONSORT extension for randomised pilot/feasibility trials emphasises that pilot objectives should be about feasibility, participant identification/consent should be explicit, measurements should match those feasibility objectives, and progression logic should be specified before interpreting results. UK HRA guidance separately emphasises proportionate participant information and consent.

Method anchors:
- https://www.bmj.com/content/355/bmj.i5239
- https://www.hra.nhs.uk/planning-and-improving-research/best-practice/informing-participants-and-seeking-consent/

These sources do not establish that this informal project exercise is legally or institutionally a clinical trial. They are used here as stronger neighbouring methodology. If participants are recruited through an institution, professional workplace, patient/service-user setting, or other context with its own research-governance requirements, determine the applicable ethics/data-protection/review route **before recruitment**. This draft does not decide that question.

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

The participant-facing HTML deliberately uses the neutral title `Two-Case Decision Exercise`; it does not advertise `owner activation`, `A/B`, TRACE, ME, #100 or #101 before answers are complete.

The setup screen gives proportionate information before participation: what is collected, local-only storage/export behavior, no time limit, voluntary participation, stop/discard route, no requested identifying information, and the intended feasibility comparison. The Start button remains disabled until the participant affirmatively checks the consent box.

The runner does not request a participant name or code and does not export wall-clock timestamps. A random session ID is sufficient to keep the two responses paired. This is **data minimisation, not a guarantee of de-identification**: participants should avoid putting identifying information into free-text answers, and an operator should treat any accidentally identifying free text according to the applicable data-handling context.

The participant should not be told the desired answer or shown the scoring rubric before answering.

Compare `PLAIN` versus `PROMPT` **within the same case across participants**. Randomized case order can be inspected as a possible order/fatigue effect; do not silently pool it away if it matters.

## First feasibility batch

Primary objective: **test whether this experiment can be run cleanly enough to justify designing a better behavioural comparison**. The small batch is not sized to estimate a reliable treatment effect.

Continue collection until there are at least four completed sessions in **each** arm. Eight is only the minimum possible total; random assignment may require more. If arm counts must be checked during collection, inspect only the exported `assignment.arm` field and do not inspect or score response text before both arm minima are reached.

Feasibility observations include:
- consent/start interaction works without confusion;
- cases remain hidden until start;
- session completes both cases;
- first answers freeze correctly;
- export succeeds and contains only the intended fields;
- no identifying information is intentionally collected;
- no obvious treatment-induced authority creep or unusable verbosity appears;
- no obvious case defect makes one arm/case uninterpretable.

Do **not** turn four-per-arm answer counts into a population efficacy estimate. Any apparent behavioural difference is descriptive pilot evidence only and may inform whether/how a later comparison should be designed.

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

## Descriptive comparison

For each case separately describe `PLAIN` versus `PROMPT` on:

1. consequential next action / owner / hold / reopen condition;
2. owner-critical observation count;
3. material false activation or invented authority;
4. elapsed seconds to first submitted answer;
5. response length as a crude burden indicator.

Do not score project vocabulary use. Do not present this tiny batch as a statistical efficacy comparison.

## Allowed dispositions

```text
FEASIBILITY_FAIL
NO_OBVIOUS_BEHAVIOURAL_DELTA
DESCRIPTIVE_ACTIVATION_SIGNAL
PROMPT_OVERFIRE
PLAIN_ALREADY_SUFFICIENT_ON_THESE_CASES
INCONCLUSIVE
MALFORMED_CASE
```

`DESCRIPTIVE_ACTIVATION_SIGNAL` requires an action-relevant owner-critical observation to appear more often or materially earlier in the prompted arm **for the same case** without a compensating material overfire. It is a reason to consider a better transfer/real-user study, not a success claim.

## Pre-specified progression logic

- Native-browser failure or material participant-flow defect -> `FEASIBILITY_FAIL`; repair or stop before recruitment continues.
- Malformed/leaky case -> freeze the affected case version; do not rescue its data post hoc.
- Plain responses already reach the owner-critical action cleanly on these cases -> preserve `PLAIN_ALREADY_SUFFICIENT_ON_THESE_CASES`; do not enlarge the activation claim.
- Prompt causes material invented authority, unnecessary tracing, or harmful delay -> `PROMPT_OVERFIRE`; shrink/stop.
- No obvious difference -> preserve the null; a larger test is not automatically earned.
- Descriptive signal with acceptable burden -> at most earn design of a later **novel-case transfer / real-user** comparison with an explicit sample-size rationale and applicable governance review.

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
