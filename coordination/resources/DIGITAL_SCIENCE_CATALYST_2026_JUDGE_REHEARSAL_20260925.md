# Digital Science Catalyst 2026 — judge rehearsal

Date: 25 September 2026

Status: **INTERNAL REVIEW / NOT SUBMITTED / NOT A CLAIM OF SHORTLISTING**

Purpose: pressure-test the current 1,297-token EvidenceWatch application against Digital Science's seven published judging areas and recent Catalyst selection signals without adding product churn or inventing validation.

Current proposal:
`coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_SUBMISSION_PACKET.md`

Current EvidenceWatch:
`f08e35086a3a6b7c16de72f42f060d47b0ab1ae7`
(54/59 deterministic tests green in both Windows and Ubuntu CI; PR #12 pilot protocol, PR #13 offline scorer and PR #14 cross-platform test repair merged)

## External selection signals

### 2026 owner criteria

Digital Science says judges score:
- team;
- problem;
- solution;
- competitors;
- market;
- progress to date;
- fit with Digital Science.

The 2026 brief also asks applicants to:
- name the research decision and current decision-maker;
- identify the existing tool/workflow the agent must live inside;
- show the work genuinely needs multiple steps;
- demonstrate a refuse/flag/escalate case;
- name an outcome metric.

Owner source:
https://www.digital-science.com/about-us/investment/catalyst-grant/

### 2025 winners

Digital Science said:
- FigureTwo stood out because of the team's deeply relevant publishing/product background and an elegant solution;
- Pathfinder brought deep bibliometrics/science-mapping pedigree and a product aligned with Digital Science customers/products.

Source:
https://www.digital-science.com/press-releases/digital-science-awards-2025-catalyst-grants/

### 2024 research-integrity winners

PostPub and VIRUS were already rooted in research-integrity work and proposed concrete tools using wider scholarly-data/workflow surfaces.

Source:
https://www.digital-science.com/press-releases/digital-science-catalyst-grant-winners-research-integrity/

### Shortlisted but not awarded comparator — OpenRefine 2025

OpenRefine's public application shows a mature 17-year product, roughly 15,500 monthly downloads, established maintainers, fiscal sponsorship, community/user evidence and a full £25k delivery plan. It was shortlisted but its own funding page later records the award as not received.

Sources:
- https://forum.openrefine.org/t/funding-opportunity-2025-digital-science-catalyst-grant/2574
- https://openrefine.org/funding

Do not infer why it lost; no rejection rationale is public. The useful negative lesson is only:

```text
TRACTION + MATURE TEAM + DELIVERY CAPACITY != AUTOMATIC CATALYST WIN
THEME / DISTINCTIVE FIT / PRODUCT DIRECTION STILL MATTER
```

## EvidenceWatch judging pressure

### TEAM

Evidence:
- Mark Goodbody: 25+ years IT/telecoms/systems engineering;
- current work demonstrates state management, restart/recovery, audit trails, authority boundaries and operational failure handling;
- multiple AI systems used for implementation/adversarial review with human release/accountability gate.

Risk:
- no academic research appointment;
- no systematic-review domain expert currently on the team;
- no pilot partner.

Honest answer:
The relevant expertise is systems engineering, not academic-domain authority. The pilot is explicitly the mechanism for bringing research-workflow expertise into the product and for falsifying Mark's assumptions before they harden.

Do not:
- inflate systems engineering into research-methods expertise;
- imply AI collaborators are advisors with independent professional standing;
- invent a pilot partner.

### PROBLEM

Decision:
Does a living systematic review need reopening because evidence already relied upon materially changed?

Current-owner subtraction:
- formal retractions/corrections: Zotero/Crossmark/Cochrane;
- new-evidence surveillance: living-review practice;
- residual: material post-reliance changes outside those well-owned routes plus downstream routing.

Risk:
Frequency/materiality of the residual class is unmeasured in a current target workflow.

Public historical workflow evidence now exists:
- the University of Bern asymptomatic-COVID living review explicitly checked included preprints for later peer-reviewed publication and re-extracted data when content changed;
- one public Lombardi episode moved from a preprint reporting 41/138 asymptomatic positives to a final publication/review extraction of 17/139 after longer follow-up / changed symptom definition;
- the review repository explicitly records that the final publication succeeded a preprint already included, so it was not counted as independent new evidence;
- the fifth review uses the public extracted data in synthesis.

Receipt:
`coordination/build_ledger/EVIDENCEWATCH_PUBLIC_WORKFLOW_SPECIMEN_20260926.md`

Best answer:
The maintenance problem is real, but current practice already handled this public case. That cuts the claim down to burden/integration: can tooling make that repeated currentness + lineage + re-extraction routing cheaper without degrading judgement? Frequency and user-value remain pilot questions. Stop if the residual is too rare or existing practice performs as well.

### SOLUTION

EvidenceWatch genuinely runs a multi-step loop:
```text
configured question/source policy
-> scheduled fetch/fingerprint
-> change detection
-> bounded model extraction when needed
-> source-role / authority check
-> typed state comparison
-> downstream dependency routing
-> human review
```

Trust behavior already demonstrated:
- duplicate suppression;
- derivative disagreement without canonical overwrite;
- candidate quarantine;
- source loss preserves last known state;
- restart reconstruction;
- correction history.

Risk:
Current reference-manager connection is CSL-JSON file handoff, not embedded integration.

Best answer:
The grant is for testing the integration hypothesis, not funding a disguised finished product.

### COMPETITORS

Current application is strong here because it subtracts rather than hand-waves:
- Cochrane;
- Zotero/Crossmark;
- ReadCube/scite;
- Refract;
- AIEP P170;
- PostPub/VIRUS;
- Perma.cc.

Best answer to "why isn't this already solved?":
It may be. EvidenceWatch only survives if joining heterogeneous post-reliance state, explicit authority, materiality filtering, dependency routing and human review inside one existing workflow saves enough effort to matter. If a stronger owner already does this well, stop.

### MARKET

Current state:
- buyer hypothesis only: institutions/research teams maintaining updateable reviews;
- plausible initial users: university evidence-synthesis teams, health evidence/guideline units and similar organisations;
- pricing untested.

Risk:
This is one of the weakest judging dimensions.

Do not manufacture TAM figures.

Interview answer:
The first commercial question is not price; it is whether the workflow saves reviewer time at acceptable missed-change and false-alert rates. Pricing follows only if that survives.

### PROGRESS TO DATE

Strongest evidence:
- working Node.js prototype;
- 59 deterministic tests green on both Windows and Ubuntu CI;
- append-only/restart behavior;
- live one-watch/two-run model witness;
- deterministic research-shaped browser demo;
- CSL-JSON handoff;
- controlled restart/correction fixture;
- predeclared shadow-mode pilot protocol + deterministic offline scorer for the promised evaluation metrics;
- explicit unresolved model-status inconsistency retained rather than hidden.

Additional real-workflow evidence:
- one public historical living-review episode now demonstrates that preprint -> final-publication change, same-lineage handling and re-extraction are real maintenance work;
- the same owner source reports a seven-person core team becoming overwhelmed and later recruiting 20 experienced volunteers committing at least 3 hours/month across review tasks;
- that workload context is not an episode-specific time saving and does not validate EvidenceWatch.

Ceiling:
No research customers, willing pilot partner, current matched-burden measurement or user-efficiency result.

### FIT WITH DIGITAL SCIENCE

This is the strongest judging dimension.

Direct alignment:
- evidence synthesis / research integrity;
- multi-step agent;
- provenance/audit/governance native to architecture;
- explicit stay-quiet / flag / refuse behavior;
- proposed integration surface overlaps Digital Science's research-workflow ecosystem.

Why Digital Science specifically:
They own adjacent workflow/data surfaces and can help falsify the integration hypothesis with researchers rather than merely fund more standalone engineering.

Do not imply ReadCube or another Digital Science product has agreed to integrate.

## Hostile interview questions

### "Why you? You are not a systematic-review researcher."

Answer:
"I'm not claiming that expertise. My contribution is systems engineering: state, provenance, failure recovery, auditability and making correction survive operational boundaries. The reason I am asking for a pilot rather than claiming product-market fit is precisely to put that engineering in front of people who own the research workflow and see whether it survives."

### "Why isn't this just Crossmark, Zotero, Cochrane, ReadCube or scite?"

Answer:
"Large parts already are. I removed those as novelty claims. The remaining hypothesis is whether material post-reliance state across heterogeneous sources can be joined to explicit authority and downstream work with low enough review burden to be useful. If one of those systems already closes that loop better, EvidenceWatch should narrow or stop."

### "Do you have evidence this workflow problem actually happens?"

Answer:
"Yes, but not evidence yet that EvidenceWatch improves it. The University of Bern living review publicly describes checking included preprints for later peer-reviewed publication and re-extracting data when content changed. Its public repository contains a concrete Lombardi case: the preprint reported 41/138 asymptomatic positives, while the final article and review extraction used 17/139 after longer follow-up and a changed symptom definition. The team recognised it as the same study lineage rather than independent evidence. That proves the maintenance task is real and also proves competent existing practice can handle it. The grant question is whether this can be made cheaper and more inspectable, not whether reviewers need to be taught to do it."

### "What makes this agentic rather than a script?"

Answer:
"The useful unit is the long-running configured workflow: observe sources on schedule, suppress unchanged observations, selectively invoke model extraction, compare typed state, enforce authority boundaries, discover or quarantine candidates, route affected work, and preserve state across restart. The person configures the policy and handles review; they do not prompt each step."

### "Show me a failure it refuses."

Answer:
"A derivative source can repeat or contradict the owner. Repetition does not mint independent support; contradiction triggers review but cannot overwrite canonical owner state. A discovered candidate cannot establish state until explicitly promoted. An unreachable authority source does not become false."

### "What does £5,000 Stage 1 buy that you cannot do now?"

Answer:
"Integration into an actual evidence-synthesis workflow and measurement of the setup/maintenance burden against existing practice. The standalone mechanism already exists. Stage 1 is deliberately a falsification stage, not more feature accumulation."

### "What result kills the project?"

Answer:
"Residual material changes are too rare; existing practice catches them as well; setup/maintenance costs more reviewer time than it saves; false alerts are too high; or missed material changes are unacceptable."

### "Why a private repository?"

Answer:
"The prototype is private while the product/reuse boundary is still being decided. The application should not imply source openness. If inspection becomes necessary for due diligence, decide a bounded release or review route explicitly rather than silently changing the licence/reuse state."

### "Why £25,000?"

Answer:
"It is staged rather than assumed. Stage 1 caps at £5k and can stop the project. The remaining £20k is conditional on the workflow surviving: pilot engineering/researcher evaluation, then model/infrastructure and independent review/reproducibility."

## Demo route if shortlisted

Prefer the research-shaped deterministic fixture over the NVIDIA cyber video for a live Catalyst interview.

Target: 45–55 seconds.

```text
synthetic fixture / zero state
-> owner baseline = 1.8
-> derivative repeats 1.8 / no alert
-> publisher correction = 1.2
-> prior state preserved
-> one dependent brief routed to review
```

Close with:
"It does not decide scientific truth. It preserves the evidence change, authority path and affected work for human review."

Source script:
`coordination/resources/DIGITAL_SCIENCE_RESEARCH_DEMO_RECORDING_20260925.md`

Do not call this:
- a researcher pilot;
- a live scholarly correction;
- a Zotero/ReadCube integration;
- efficacy evidence.

## Current disposition

```text
APPLICATION FIT = REAL
WIN = UNKNOWN
SHORTLIST = UNKNOWN

STRONGEST DIMENSIONS = SOLUTION / PROGRESS / 2026 FIT / TRUST ARCHITECTURE
WEAKEST DIMENSIONS = DOMAIN TEAM / USER VALIDATION / MARKET

NEXT PRE-SUBMISSION WORK = NO NEW PRODUCT FEATURES
NEXT HUMAN GATE = LIVE FORM IDENTITY -> LATER FIELDS/TERMS -> FINAL SUBMIT
```
