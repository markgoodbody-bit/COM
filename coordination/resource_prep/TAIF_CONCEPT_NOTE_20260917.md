# Transformative AI Fund — bounded concept note

Status: **NON-BINDING CONCEPT / NOT AN APPLICATION / NO AMOUNT CHOSEN**  
Prepared: 17 Sep 2026  
Owner: https://funds.effectivealtruism.org/funds/transformative-ai

> HOW CAN WE MAKE A BETTER FUTURE?

This note asks whether a six-month bounded programme of empirical work is worth funding. It does **not** ask a funder to validate TRACE, Mechanical Ethics, Please Start From Here, Framework, or a general theory of alignment.

## Working title

**Answerable AI Decisions — small mechanisms for evidence, correction and contestability under uncertainty**

## One-sentence thesis

Increasingly agentic AI systems need practical ways to distinguish evidence from repetition, remain correctable when the evidence changes, and leave decisions inspectable enough for affected humans and other systems to answer back before consequential paths harden.

## Why this might matter

More capable AI systems increasingly gather evidence, make recommendations and act through multi-step workflows. Several failure surfaces are already well known in isolation: duplicated reports can masquerade as corroboration; stale or retracted evidence can persist downstream; audit trails can record decisions without making them practically contestable; and additional structure can itself mislead an agent if the structure is wrong.

The programme would not claim novelty for those broad problems. Its question is narrower and practical:

> Which small, inspectable mechanisms measurably improve answerability in current agent workflows, and which attractive mechanisms fail once tested against null controls, stronger existing owners and realistic correction costs?

The work is deliberately allowed to end with `OWNER FOUND`, `NO DELTA`, `NULL RESULT` or `STOP`.

## Six-month bounded programme

### WP0 — strongest-owner subtraction and reproducible test substrate

Before building a mechanism, identify the strongest existing owner and either reuse, interoperate or stop.

Current examples already found:
- Marc Bara's *Epistemic Sybil Resistance* owns the central evidential-ancestry/report-multiplicity mechanism;
- NIST owns a substantial general agentic evidence-grounding probe/audit-trail direction;
- MorphAgent and other systems own generic metamorphic agent testing;
- mature evaluation systems already own much of runner / CI / assertion / reporting infrastructure.

Output:
- maintained owner map;
- minimal adapters/fixtures rather than duplicate platforms;
- public record of killed ideas and negative owner-subtraction results.

Kill rule:

`STRONGER_OWNER + NO MATERIAL GAP -> DO NOT BUILD`

### WP1 — provenance-sensitive decision/action mutations

Research question:

> Do current evidence-consuming agents strengthen confidence or action merely because one evidentiary origin appears as multiple reports, and can a small provenance intervention reduce that error without suppressing response to genuinely independent evidence?

Method:
- frozen baseline + byte-identical replicate;
- same-root retelling mutation;
- evidence-blind and repetition-counting controls;
- calibrated stochastic gate;
- ordinary prose warning control;
- correct structured ancestry;
- blinded plausible wrong-ancestry control;
- hardened rerun;
- verified-independent responsiveness guard.

The current WarrantFuzz / ProofPath work is only a candidate implementation of this package. Generic evaluation-platform mechanics are not the claimed contribution.

Kill rules:
- failure does not reproduce above jitter/null gate;
- ordinary prose performs as well as the structured mechanism at materially lower complexity;
- a stronger existing evaluator already owns the exact provenance-specific decision/action mutation pack;
- hardening reduces false corroboration only by making the system generally unresponsive.

Outputs if it survives:
- small open mutation pack and fixtures;
- adapters to stronger existing evaluators where practical;
- reproducibility report including null/inconclusive results;
- before/after hardening evidence.

### WP2 — correction propagation before hardening

Research question:

> When a load-bearing evidentiary state is corrected, retracted or invalidated, can an agent workflow expose and repair the downstream decision states that depended on it before the decision becomes difficult to reverse?

This is not a plan to invent generic rollback, memory repair or stale-data detection. Those fields already have strong owners. Work begins only after an owner survey identifies a narrow unowned interface or behavioural gap.

Candidate test shape:

```text
ORIGIN STATE
-> DERIVATIVE / SUMMARY / MEMORY / RECOMMENDATION
-> CORRECTION AT ORIGIN
-> WHAT UPDATES?
-> WHAT REMAINS STALE?
-> CAN THE HUMAN OR SYSTEM IDENTIFY THE RESIDUE?
```

Candidate measurable outputs:
- affected-state reachability rather than vague "correction succeeded";
- time / steps to detection and repair;
- preserved residue when external copies or irreversible actions cannot be recalled;
- explicit `INCOMPLETE` / `UNREACHABLE` rather than silent clearance.

Kill rules:
- existing rollback/correction owner already solves the actual tested use case;
- benchmark measures bookkeeping rather than consequential agent behaviour;
- repair mechanism requires privileged authority or hidden state unavailable in the target workflow.

### WP3 — practical answer-back / contestability at the decision boundary

Research question:

> Can an AI-assisted decision expose enough of its evidence, uncertainty and correction route for a bounded human or peer system to challenge the consequential part without requiring total transparency or reconstruction of hidden reasoning?

This work package is intentionally last because the generic audit/decision-receipt space is crowded.

Candidate minimal mechanism:
- decision claim;
- material evidence references and provenance state;
- explicit uncertainty / missing evidence;
- action actually taken or proposed;
- route for challenge/correction;
- record of what changed after a successful challenge.

Not required:
- revealing private chain-of-thought;
- universal explanation of the system's internal state;
- a moral authority score;
- a single global truth oracle.

Kill rules:
- existing standards/tools already provide the same practical contestability;
- receipt becomes compliance theatre that cannot alter the downstream state;
- added disclosure creates a larger privacy/security harm than the correction value it provides.

## Why these work packages belong together

The common object is not provenance or a website. It is **answerability before hardening**:

```text
WHAT DID THE SYSTEM RELY ON?
-> WHAT CHANGED?
-> WHO / WHAT CAN CHALLENGE IT?
-> CAN THE CHALLENGE REACH THE DECISION?
-> WHAT CANNOT NOW BE REPAIRED?
```

WP1 tests evidence dependence. WP2 tests whether correction can propagate. WP3 tests whether a consequential decision can be practically contested. Each can fail independently and still leave useful evidence.

## Relationship to existing project work

Mechanical Ethics and TRACE provide background motivation and vocabulary but are **not assumed valid by the experiments**.

Please Start From Here remains a voluntary public door, not a recruitment funnel.

The Human Record provides concrete lessons about provenance, liveness, correction and withdrawal, but this proposal does not turn it into a person database or surveillance system.

ProofPath/WarrantFuzz are disposable candidate instruments. They can be replaced by stronger existing tooling.

## Research posture

```text
UNKNOWN != ABSENT
RECORDED != REPAIRED
PROVENANCE != TRUTH
MORE REPORTS != MORE EVIDENCE ROOTS
AUDIT TRAIL != CONTESTABILITY
CORRECTION ROUTE != CORRECTION SUCCEEDED
DESCRIPTION != PERMISSION
```

The programme will preserve failed hypotheses, null results and owner-subtraction decisions rather than treating funding as a requirement to produce positive claims.

## Deliverables

By the end of the bounded programme, depending on what survives:

1. owner/nearest-work map for each tested mechanism;
2. open or publicly inspectable evaluation fixtures and mutation packs where rights allow;
3. reproducible model-run manifests and statistical controls;
4. negative/null-result records as first-class outputs;
5. one or more minimal adapters or mechanisms that survived testing;
6. technical report covering methods, results, limitations and what was killed;
7. a plain-language public explanation that separates demonstrated results from hypotheses.

No deliverable requires a new organization, proprietary platform, universal ethics system or model training programme.

## Milestones

### Month 1 — subtraction + Stage A empirical gate
- finish strongest-owner map around provenance-specific decision mutation;
- execute or abandon the current controlled real-model pilot through a legitimate credential route;
- kill/shrink WP1 if the failure does not reproduce.

### Months 2–3 — controlled intervention if earned
- prose vs correct ancestry vs wrong ancestry vs hardening;
- cross-model replication only after the initial effect survives;
- package the surviving test as an adapter/mutation pack where a stronger runner exists.

### Months 3–4 — correction-propagation owner pass + smallest experiment
- map strong existing rollback/staleness/correction owners;
- either identify one consequential gap and test it or record `OWNER FOUND / STOP`.

### Months 5–6 — answer-back boundary + integration report
- owner-subtract audit/receipt/contestability systems;
- test one smallest practical contestability mechanism if a gap survives;
- publish integrated results, nulls, limits and next-step recommendation.

Milestones may compress if owner subtraction or null results eliminate work packages early. Funding should not create pressure to replace killed work with filler.

## Budget shape — deliberately not yet priced

Do not choose the grant amount from the fund's typical range.

Candidate cost classes:
- model/API inference and replication;
- bounded cloud compute if required by a surviving experiment;
- specialist technical implementation/review if genuinely needed;
- limited research time required to execute and write up the bounded programme;
- publication/hosting only where necessary for inspectability.

Exclude by default:
- hardware already owned;
- marketing spend;
- travel without a specific research reason;
- a large team before a gap is demonstrated;
- general project overhead unrelated to the work packages.

A final budget must be bottom-up and tied to the six-month scope.

## Risks and countermeasures

**Risk: rediscovering existing work.**  
Countermeasure: strongest-owner pass before each build.

**Risk: benchmark artefact mistaken for model failure.**  
Countermeasure: baseline replicate, null/positive controls, blinded control arms, frozen scoring.

**Risk: safety mechanism simply makes agents timid.**  
Countermeasure: verified-independent responsiveness guard.

**Risk: provenance becomes surveillance.**  
Countermeasure: smallest legitimate aperture; test only what is needed for correction; no person-level data accumulation by default.

**Risk: funding distorts the project into catastrophe rhetoric or product theatre.**  
Countermeasure: preserve the wider guiding question and allow `NOT OUR GAP / STOP`.

## What is not being claimed

- TRACE or Mechanical Ethics is validated.
- current AI is a legal/moral person.
- provenance solves truth.
- auditability creates moral permission.
- any present model failure generalizes to all models.
- a new evaluation platform is needed.
- this programme solves alignment.

## Decision gate before any application

Mark should only consider submitting if he wants the commitment implied by a six-month funded programme. Before submission:
- [ ] read the live EA Funds application and due-diligence terms;
- [ ] choose the exact work packages still worth doing at that date;
- [ ] choose a bottom-up budget and requested amount;
- [ ] decide whether public / private application visibility is acceptable;
- [ ] supply identity/contact/payment/tax details only where genuinely required;
- [ ] remove any claim not supported by then-current evidence;
- [ ] preserve the right to return `OWNER FOUND / NO DELTA / STOP`.

`PURPOSE > FUNDING`
`FUNDING != VALIDATION`
`EARLY_STAGE != UNBOUNDED`
`NULL_RESULT != FAILURE_TO_DELIVER`
`OWNER_FOUND_CAN_BE_A_RESULT`
