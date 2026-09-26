# Digital Science Catalyst 2026 — judge rehearsal

Date: 26 September 2026

Status: **INTERNAL REVIEW / NOT SUBMITTED / NOT A CLAIM OF SHORTLISTING**

Purpose: pressure-test the actual current EvidenceWatch application against Digital Science's published judging areas and likely interview questions without adding product churn or inventing validation.

Current proposal:
`coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_SUBMISSION_PACKET.md`

Current proposal body:
**1,426 whitespace-delimited words**. Final form-editor recount remains required.

Current EvidenceWatch:
`9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f`

Current deterministic suite:
**62 / 62 green on Windows + Ubuntu CI**

Current ceiling:

```text
WORKING PROTOTYPE != VALIDATED RESEARCH PRODUCT
RETROSPECTIVE TEST PREPARED != RETROSPECTIVE RESULT
PUBLIC WORKFLOW SPECIMEN != USER BENEFIT
GRANT FIT != PRODUCT VALIDATION
```

## External selection signals

### 2026 owner criteria

Digital Science says judges assess:
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
- FigureTwo stood out because of the team's relevant publishing/product background and an elegant solution;
- Pathfinder brought bibliometrics/science-mapping pedigree and strong alignment with Digital Science products/customers.

Source:
https://www.digital-science.com/press-releases/digital-science-awards-2025-catalyst-grants/

### 2024 research-integrity winners

PostPub and VIRUS were already rooted in research-integrity work and proposed concrete tools tied to scholarly-data/workflow surfaces.

Source:
https://www.digital-science.com/press-releases/digital-science-catalyst-grant-winners-research-integrity/

### Negative comparator — OpenRefine 2025

OpenRefine publicly showed a mature product, established usage and a full delivery plan, was shortlisted, and later recorded that the award was not received.

Do not infer why. The bounded lesson is:

```text
TRACTION + MATURE TEAM + DELIVERY CAPACITY != AUTOMATIC CATALYST WIN
THEME / DISTINCTIVE FIT / PRODUCT DIRECTION STILL MATTER
```

Sources:
- https://forum.openrefine.org/t/funding-opportunity-2025-digital-science-catalyst-grant/2574
- https://openrefine.org/funding

## Current EvidenceWatch position after stronger-owner subtraction

EvidenceWatch no longer claims novelty in:
- new-study surveillance;
- formal retraction/correction handling;
- preprint -> publication monitoring;
- dataset-version identity/provenance;
- generic webpage change detection;
- web-state preservation;
- generic dependency graphs;
- generic living-guideline materiality routing;
- Zotero/library sync/version plumbing.

Stronger owners include:
- Cochrane;
- Crossref / Europe PMC;
- Zotero / Crossmark;
- ReadCube / scite;
- EPPI-Reviewer;
- MAGICapp / GRADEpro;
- ALEC / LEAPP-AI;
- DataCite / Figshare / Zenodo;
- Memento / Perma.cc;
- Visualping / changedetection.io;
- Refract;
- AIEP P170.

The surviving hypothesis is integration:

> Can owner change/version/currentness signals be bound to the exact source state actually relied upon, filtered for bounded materiality, and routed to affected downstream review work at lower burden than current practice?

If a strong existing workflow already does this adequately, EvidenceWatch should narrow, interoperate or stop.

## Judging pressure

### TEAM

Evidence:
- Mark Goodbody: 25+ years IT/telecoms/systems engineering;
- current work demonstrates state management, restart/recovery, audit trails, authority boundaries and operational failure handling;
- multiple AI systems are used for implementation/adversarial review, with Mark as human release/accountability gate.

Risk:
- no academic research appointment;
- no systematic-review domain expert currently on the team;
- no pilot partner.

Best answer:

> "My relevant expertise is systems engineering: state, provenance, failure recovery, auditability and correction under incomplete information. I am not claiming systematic-review expertise. The pilot is deliberately where that domain expertise enters and where my assumptions can be falsified before they harden."

Do not:
- inflate systems engineering into research-methods expertise;
- imply AI collaborators are professional advisors;
- invent a pilot partner.

### PROBLEM

Current decision:
Does a living evidence team need to reopen already-relied-on work because an underlying source state materially changed?

Owner subtraction:
- formal retractions/corrections are already handled by stronger systems;
- new-study surveillance is already handled;
- ALEC explicitly owns preprint -> peer-reviewed monitoring/data recheck;
- DataCite/Figshare/Zenodo own much ordinary version identity;
- Memento/Perma/Visualping/changedetection.io own generic web-state preservation/change monitoring;
- AIEP/MAGIC/GRADEpro own substantial dependency/evidence-to-decision structure.

Residual:
The connection between an external changed source state and the exact relied-on extraction/synthesis/recommendation object may still be fragmented across systems.

Risk:
We do not know how often that residual creates meaningful burden in a current workflow.

Public evidence:
- University of Bern living review checked included preprints for later publication and re-extracted data when content changed;
- Lombardi moved from 41/138 in the preprint state to 17/139 in the final/review extraction after longer follow-up and a changed symptom definition;
- competent existing practice handled it correctly.

Best answer:

> "The maintenance task is real, but the public case also proves reviewers already know how to handle it. The question is not whether they need our method. It is whether binding trusted source-state signals to already-relied-on work can make that maintenance cheaper and more inspectable without increasing misses or noise."

### SOLUTION

Current multi-step loop:

```text
bounded question + source policy
-> observe / fingerprint
-> consume owner currentness/version signals where available
-> selectively analyse residual change
-> enforce source-role / authority boundaries
-> compare typed evidence state
-> bind to approved downstream dependencies
-> route human review
-> preserve append-only history
```

Trust behavior already demonstrated:
- duplicate suppression;
- derivative disagreement without canonical overwrite;
- candidate quarantine;
- source-loss/recovery while preserving last known state;
- restart reconstruction;
- correction history.

Current reference-manager state:
- CSL-JSON file handoff only;
- no live Zotero or ReadCube integration.

Proposed first host:
**Zotero**, but using Zotero's own API v3/local-API/object-version machinery rather than building parallel sync.

Stage 1 begins read-only:
- bind owner source-state/currentness signals to items in one existing library;
- present shadow alerts outside the library;
- defer write-back until benefit and authority are established.

Boundary:

```text
ZOTERO ITEM VERSION != SOURCE PUBLICATION / DATASET VERSION
READABLE INTEGRATION != WRITE AUTHORITY
```

### COMPETITORS / STRONGER OWNERS

The application should not answer "why are you better than all these systems?"

Better answer:

> "Large parts are already solved by stronger owners. EvidenceWatch survives only as an integration/burden hypothesis across those systems. If an existing workflow already closes the loop cheaply, we should use it or stop."

This is stronger than a novelty claim because it makes the grant fund a falsifiable integration test instead of another parallel platform.

### MARKET

Current state:
- buyer hypothesis only: institutions/research teams maintaining updateable reviews/guidelines;
- pricing untested;
- no customers;
- no validated adoption evidence.

Risk:
Still one of the weakest judging dimensions.

Do not manufacture TAM figures.

Interview answer:

> "The first commercial question is not price. It is whether this reduces reviewer burden at acceptable miss and false-alert rates inside a real existing workflow. Pricing and market size come after that survives."

### PROGRESS TO DATE

Engineering:
- working Node.js prototype;
- 62 deterministic tests green on Windows and Ubuntu;
- append-only/restart behavior;
- one live two-run Nemotron witness on public owner pages;
- deterministic research-shaped demo;
- CSL-JSON handoff;
- controlled restart/correction fixture;
- predeclared shadow-mode pilot protocol + offline scorer.

Real-workflow evidence:
- public Bern historical specimen;
- recurring living-review workload context;
- no willing current research partner and no matched burden result.

Retrospective falsification pipeline:
- Brierley v2 frozen before model output;
- 22 owner-labelled major-change pairs;
- 22 clean reconstructable matched no-change controls;
- blinded packet/key SHA receipts;
- full 22+22 trivial lexical baselines around AUC 0.79–0.80;
- fail-closed local harness;
- first `ANALYSIS_FAILED` aborts and seals a partial receipt;
- comparator integrity checks are now fail-closed;
- result-routing rule is predeclared;
- **no model/provider run has occurred**.

Interpretation:

```text
PREDECLARED HOSTILE TEST = PROGRESS
UNRUN TEST != RESULT
GREEN PIPELINE != MODEL QUALITY
```

### FIT WITH DIGITAL SCIENCE

This remains a strong dimension.

Direct alignment:
- evidence synthesis / research integrity;
- long-running multi-step agent;
- provenance/audit/governance native to the architecture;
- explicit stay-quiet / flag / refuse behavior;
- measurable workflow outcome;
- integration surface overlaps Digital Science products/workflows.

Digital Science is also a particularly useful falsifier because it owns adjacent systems including Figshare and ReadCube and has already funded research-integrity work such as PostPub/VIRUS.

Best answer:

> "Digital Science is valuable here not because it validates the idea, but because its own workflow products and research users are strong enough to show quickly whether this integration layer is redundant."

## Hostile interview questions

### "Why you? You are not a systematic-review researcher."

> "Correct. My contribution is systems engineering: state, provenance, failure recovery, auditability and correction. I am asking to test that engineering inside a workflow owned by research-method experts rather than presenting my domain assumptions as validated."

### "Why isn't this just Zotero, Crossmark, Cochrane, ReadCube, scite, EPPI, MAGIC or ALEC?"

> "Much of it is. I have removed those mechanisms from the novelty claim. The remaining question is whether their change/currentness signals can be connected to the exact prior state a team relied upon and the downstream work that should be reopened, with low enough burden to matter. If their existing workflow already does that well, EvidenceWatch should narrow or stop."

### "Why isn't this just Visualping or changedetection.io?"

> "Generic webpage change detection is already owned. A changed page is not automatically a changed evidence state, and a changed evidence state is not automatically a reason to reopen a recommendation. The proposed test is the binding/materiality/routing layer inside an existing evidence workflow."

### "Why isn't dataset versioning already solved by DataCite or Figshare?"

> "Version identity is largely solved for well-versioned repositories. The question is whether the version signal reaches the exact evidence object already relied upon and whether that consequence is routed to the affected work. EvidenceWatch should consume DataCite/Figshare signals, not compete with them."

### "Why Zotero?"

> "It is a plausible first host because it is already present in research workflows and exposes mature API/local-API and object-version primitives. Stage 1 can therefore be read-only and focus on the actual hypothesis rather than rebuilding sync. If the partner uses a stronger host, we should use that instead."

### "What makes this agentic rather than a script?"

> "The useful object is the long-running configured workflow: observe, suppress unchanged states, consume version signals, selectively analyse residual change, enforce authority boundaries, preserve state across restart, quarantine discovered candidates and route affected work for human review. The human defines policy and makes the decision; they do not prompt every step."

### "Show me something it refuses."

> "A derivative source cannot overwrite canonical owner state. A discovered candidate cannot gain authority automatically. Source unreachability does not become evidence that the claim is false. Stage 1 Zotero integration is read-only until benefit and authority are established."

### "What does £5,000 Stage 1 buy?"

> "Read-only integration into one actual workflow, source-state-to-item binding, a human-approved dependency map, matched baseline episodes and measurement of setup and recurring burden. It can stop there if the problem is too rare or existing practice is better."

### "What result kills the project?"

> "Residual changes are too rare; existing practice catches them as well or better; setup and maintenance cost more time than they save; false alerts make the queue unusable; or material changes are missed."

### "What has the retrospective benchmark proved?"

> "Nothing yet about the model—the live run has not happened. What is useful is that the corpus, trivial baselines, failure handling and interpretation routes were frozen before output. If simple lexical change weakly dominates the model, the semantic-value claim narrows or stops."

### "Why is the repository private?"

> "The prototype is private while product/reuse boundaries are still being decided. I do not want an accidental licence decision to masquerade as validation. If due diligence requires inspection, I would use an explicit bounded review or release route."

## Demo route if shortlisted

Prefer the research-shaped deterministic fixture over the NVIDIA cyber video for a live interview.

Target: about 45–55 seconds.

```text
synthetic fixture / zero state
-> owner baseline = 1.8
-> derivative repeats 1.8 / no alert
-> publisher correction = 1.2
-> prior state preserved
-> one dependent brief routed to review
```

Close with:

> "It does not decide scientific truth. It preserves the evidence change, authority path and affected work for human review."

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

STRONGEST DIMENSIONS =
  TRUST ARCHITECTURE
  SOLUTION SHAPE
  2026 THEME FIT
  PREDECLARED FALSIFICATION

WEAKEST DIMENSIONS =
  DOMAIN TEAM
  USER VALIDATION
  MARKET
  NO CURRENT PILOT PARTNER

NEXT PRODUCT WORK = NONE BY MOMENTUM
NEXT EVIDENCE = REAL WORKFLOW OR FROZEN RETROSPECTIVE RUN
NEXT HUMAN GATE = LIVE FORM IDENTITY -> LATER FIELDS/TERMS -> FINAL SUBMIT
```
