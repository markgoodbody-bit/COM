# Digital Science Catalyst 2026 — EvidenceWatch hostile review

Date: 25 September 2026

Status: **KEEP / MATERIAL FIT SURVIVES / APPLICATION NOT SUBMITTED / PRODUCT VALIDATION NOT ESTABLISHED**

Owner criteria rechecked against the live 2026 Digital Science Catalyst page:
- research-lifecycle problem;
- multi-step agentic workflow;
- existing tool/system boundary;
- trust/audit/governance;
- refusal/flag/escalate behaviour;
- measurable outcome;
- <=1,500 words;
- judges assess team, problem, solution, competitors, market, progress, fit.

Current proposal:
`coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_EVIDENCEWATCH_PREP.md`

Current EvidenceWatch state:
- private main `12594ef3a7c80324c0299002ecc4868bf2d0c82f`
- CI SUCCESS
- 43 deterministic tests
- PR #7 CSL-JSON reference-manager handoff merged
- owner-subtraction note now explicitly records Zotero retraction warnings and ReadCube monitoring/review ownership
- no public release / no live Zotero or ReadCube integration

## Strongest rejection reasons, not hidden

### Team
Mark has long systems/telecoms engineering and operational troubleshooting experience, but is not claiming to be a professional research-integrity practitioner or academic software founder. No external research-domain pilot partner is established.

Disposition: **KEEP WITH CEILING**. Do not manufacture a research credential. Domain validation is part of the proposed pilot.

### Problem
The downstream dependency problem is coherent and consequential when it occurs, but its incidence and reviewer-cost distribution across target teams have not been measured.

Disposition: **KEEP / MEASURE FIRST**. The application now says frequency/cost are pilot questions.

### Solution / agenticness
EvidenceWatch is genuinely multi-step and autonomous after configuration: scheduled fetch, fingerprint, bounded model analysis, source-role/authority separation, state comparison, candidate discovery/quarantine and review routing. However, the human supplies the monitoring plan and authority policy. It is not a free-form dynamic planner.

Disposition: **KEEP / DO NOT OVERCLAIM PLANNING**. Multi-step autonomous workflow is enough to test; do not describe it as autonomous research reasoning.

### Existing workflow integration
Before the current build, this was the weakest area. Digital Science explicitly prefers an agent embedded in a tool researchers already use.

PR #7 adds a CSL-JSON handoff from a standard reference-manager export. Zotero documents CSL JSON as import/export. This proves a real portable boundary, but:

```text
CSL FILE HANDOFF != EMBEDDED ZOTERO PLUGIN
CSL FILE HANDOFF != READCUBE INTEGRATION
STANDARD FORMAT != USER ADOPTION
```

Disposition: **IMPROVED BUT STILL THE PRIMARY PRODUCT GAP**. The grant should fund the first live integration/pilot rather than pretend it already exists.

### Trust / governance
This is currently the strongest area. The system preserves append-only history, separates model analysis from source authority, keeps candidates quarantined, distinguishes unreachable from false, and routes uncertainty to review.

The strongest concrete refusal/escalation test is already in code: a discovered candidate may be analysed but cannot establish/advance canonical state or create a canonical alert before explicit promotion.

Disposition: **KEEP**.

### Competitors
Strong owners exist and narrow the claim further:
- Crossmark / Crossref: formal corrections/retractions/update status;
- Zotero + Retraction Watch: library and document-level retraction warnings, including later retraction of already-cited items;
- ReadCube: literature monitoring, shared libraries, systematic-review workflows, citation/library synchronisation;
- Visualping / Distill: page-change monitoring;
- scite: citation context/retraction signals.

EvidenceWatch therefore **does not own formal retraction propagation**. The surviving hypothesis is broader post-reliance evidence change across heterogeneous sources, with explicit ancestry/authority and downstream dependency routing beyond one citation.

A 2022 meta-epidemiological study of systematic reviews and clinical-practice guidelines supports the existence of a downstream correction problem in biomedicine: of 239 articles that had included trials later retracted, only about 5% of systematic reviews and guidelines corrected or retracted their results. This is domain-specific evidence, not a universal incidence estimate.

Disposition: **KEEP AS NARROWED PRODUCT HYPOTHESIS, NOT NOVELTY CLAIM**. Kill/pivot if a current product owns the full residue better.

### Market
No customer discovery, purchasing signal or pricing validation exists. Candidate users are evidence-synthesis, research-integrity and recurring-review teams. Workspace/monitored-collection subscription is only a hypothesis.

Disposition: **WEAK / HONESTLY WEAK**. Do not invent TAM, buyers or willingness-to-pay numbers.

### Progress
Working prototype, deterministic browser demo, prior live technical witness, 43 tests on the research-handoff branch. No research-user validation.

Disposition: **KEEP / GOOD EARLY-STAGE PROGRESS**.

### Fit with Digital Science
Strong thematic fit: evidence synthesis / research integrity, provenance, governance, audit, human review and a natural boundary near reference/literature-management workflows.

Disposition: **KEEP**.

## Falsification result

The application survives because the owner explicitly accepts prototypes/concepts and asks applicants to state where they are today. It would fail our own standard if we represented the CSL handoff as embedded use, the technical witness as research-user validation, or the product residue as established market need.

```text
FIT = REAL
PRODUCT NEED = UNVALIDATED
INTEGRATION = FILE HANDOFF ONLY
USER VALUE = UNMEASURED
APPLICATION = WORTH SUBMITTING AFTER HUMAN REVIEW
```

## Next bounded build decision

PR #7 passes the useful-without-grant test:
- CSL JSON is a real portable research-tool boundary;
- explicit authority policy prevents bibliographic presence from becoming epistemic authority;
- the adapter is independent of Digital Science-specific APIs;
- all branch tests pass.

PR #7 was merged as internal product progress. The later owner-subtraction documentation commit moved private main to `12594ef3a7c80324c0299002ecc4868bf2d0c82f`, with CI green. The NVIDIA submission remains bound to its earlier frozen head in its receipt.

No public release, organiser contact, form submission, terms acceptance or spend is implied by merge.
