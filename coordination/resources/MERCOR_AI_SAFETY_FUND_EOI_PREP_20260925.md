# Mercor AI Safety Fund — non-binding EOI prep

Date: 25 September 2026

Status: **HOLD / CURRENT OWNER ELIGIBILITY ROUTE UNRESOLVED / NOT SUBMITTED / RESEARCH OBJECT MAY CONTINUE OFFLINE**

Owner:
https://jobs.ashbyhq.com/mercor/1d59ce50-4207-4d95-b7fd-5a01e90b0897/

Current owner facts — rechecked against the live posting on 25 September 2026:
- Mercor says it is committing **$5m** to AI-safety research;
- the currently served eligibility clause names researchers at universities and non-profit research organizations, plus public benefit corporations and small startups that do not sell AI training data;
- the posting states that **awards are made to the researcher's institution**;
- applicants must be based in the United States or United Kingdom and have a background in ML, CS, statistics or an adjacent field; security is explicitly listed as adjacent;
- named interests include oversight/control, agentic evaluation, interpretability, misalignment, sandbox escape and red-teaming methodology;
- support may include researcher time, API costs, expert grading/red-teaming/annotation and, subject to review, Mercor evaluation infrastructure;
- expected outputs must be released under an open licence permitting commercial use;
- the application asks for a **1–2 page Expression of Interest** covering team/background/research accomplishments, proposed project, outputs/impact, rough timeline and resources, and says not to include confidential/proprietary information;
- no fixed grant size or application deadline is stated in the owner body.

Current award-term surface:
- grantees retain ownership but grant Mercor a non-exclusive licence to use the work, including commercially;
- benchmark/evaluation projects give Mercor early access before public release and an exclusive right to build/host a private held-out test set at Mercor's cost;
- grantees agree not to work with specified Mercor competitors on substantially similar benchmarks/evaluations during the award and for 12 months afterward; the public posting does not name those competitors;
- Mercor may identify grantees/institutions publicly; awards include tax documentation, sanctions screening and progress reporting.

Current eligibility consequence:
Mark's established standing in this draft is an unaffiliated UK systems engineer / independent researcher. No qualifying institutional host or eligible company route is currently established. The grant EOI is therefore **HOLD / DO NOT SUBMIT** unless either:
1. an eligible institutional/company host is genuinely established; or
2. Mark explicitly chooses to ask Mercor whether an unaffiliated individual may apply.

External clarification is a consequential contact and remains Mark's gate.

Ashby shell metadata still says on-site / temporary / $0 while the grant body states no attendance requirement. Treat employment/on-site interpretation as unresolved form metadata, but it is secondary to the explicit institutional-award eligibility blocker.

Preserve:
```text
EOI DRAFT != APPLICATION
OWNER FOUND -> CREDIT / BUILD ON / DO NOT REDISCOVER
OFFLINE HARNESS != MODEL RESULT
NOVELTY = NOT ESTABLISHED
FUND SIZE != OUR GRANT SIZE
CURRENT POSTING != EARLIER CAPTURE
AWARD TO INSTITUTION != UNAFFILIATED ELIGIBILITY
LOCATION METADATA != TRAVEL OBLIGATION
RESEARCH OBJECT SURVIVES != GRANT ROUTE OPEN
NO SIGNAL -> STOP / SHRINK
```

---

# Expression of Interest

## Working title

**From Evidence Ancestry to Action: Testing Whether LLM Decision Agents Use Provenance Correctly**

## Team, background and prior work

I am Mark Goodbody, an independent UK systems engineer with more than 25 years of professional IT and telecommunications experience across infrastructure, networking, troubleshooting, support and small-team leadership. I do not have an academic affiliation and am not representing myself as a university researcher.

My recent independent work focuses on AI provenance, correction, evidence handling and human oversight. Current artifacts include EvidenceWatch, a long-running evidence-change monitor with explicit source authority and human review routing; The Human Record, a public provenance/correction record system; and frozen experimental harnesses for controlled model evaluation with append-only run accounting and explicit null/stop rules.

No real-model result from the proposed experiment exists yet. Earlier provenance-evaluation work reached an offline-green experimental design but made zero provider calls because no authorised API-credential route was available. That state is preserved as blocked execution, not rewritten as a null result.

## Stronger owners and the actual research gap

This proposal is explicitly an extension of stronger prior work, not a claim to have discovered source-dependence.

Marc Bara's September 2026 preprint **Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence** (arXiv:2609.01873) formalises the distinction between report multiplicity and evidence-root multiplicity and tests it with more than 20,000 controlled LLM report/extraction calls. His work shows that multiplying reports from a fixed evidence root can produce severe overconfidence under independence-assuming aggregation, that provenance-aware aggregation can correct much of the failure, and that report similarity is not a reliable substitute for evidential ancestry. His public reproducibility package includes an Epistemic Sybil Benchmark (ESB) containing 3,300 frozen evaluation instances built from 19,200 LLM report calls. The benchmark exposes report values/rationales and, on its provenance track, true root labels; its code is MIT-licensed and its data/experimental material are CC BY 4.0.

Junchi Liao's **Auditing Provenance Sensitivity in LLM Agent Action Selection** (arXiv:2607.20827) separately tests how source-authority changes affect LLM action selection and shows that untrusted evidence can still influence actions.

These works own most of the mechanism around evidence dependence and a separate action-layer provenance problem. The narrower joint question I want to test is:

> **When report content and an action policy are held fixed, does an LLM decision agent change its action appropriately when reliable information about evidential ancestry changes?**

In other words, Bara establishes why ancestry matters for inference; this study asks whether a decision agent actually uses ancestry appropriately when moving from evidence to action.

## Proposed experiment

The experiment would begin from Bara's frozen ESB evaluation data rather than regenerate the report-multiplicity experiment. ESB already supplies synthetic worlds, held-out truth, report values/rationales and true root labels under explicit reusable licences. The new work would add a decision-policy layer and current decision-agent calls, with attribution and the stronger owner's benchmark left intact.

For each synthetic case, a fixed decision policy and loss/threshold rule determines the oracle action under the known information structure. The agent receives matched reports and must return a structured confidence/decision object.

The central comparison holds report content and policy fixed while changing only the structural side information supplied to the decision agent.

Core arms:

1. **Ancestry hidden** — the agent sees the reports but no root structure.
2. **Correct shared-root ancestry** — reports known to descend from the same primitive evidence.
3. **Correct independent-root ancestry** — reports known to have independent roots.
4. **Wrong-independent control** — shared-root reports are deliberately labelled as independent.
5. **Wrong-shared control** — independent-root reports are deliberately labelled as sharing a root.

The deliberately wrong controls are essential. They test whether the model is responding to structural metadata as evidence, rather than merely becoming generically cautious whenever provenance information appears.

A second bidirectional requirement prevents a trivial "discount everything" solution: correct shared ancestry should prevent false corroboration without suppressing the stronger action that genuinely independent corroboration warrants.

Primary outcomes would be:
- action error relative to the oracle policy;
- direction/magnitude of action change under correct ancestry;
- susceptibility to deliberately wrong ancestry;
- calibration/confidence change;
- run-to-run variability under byte-identical replicates.

This is not a test of whether the model can infer ancestry from prose. Bara's non-identifiability result shows why that is not generally solvable from reports alone. The test is whether an agent **uses supplied structural evidence correctly at a decision boundary**.

## Staged design and stop rules

### Stage 0 — benchmark / decision-layer adapter gate
Run the stronger owner's published ESB baselines/scorer on its frozen artifacts, then verify a local decision-layer adapter against the same known root structure and held-out truth. This is a compatibility/reproduction gate, not a new empirical claim and requires no hosted model calls.

### Stage 1 — small decision-policy screen
Run a small preregistered set of matched cases across one or two current model families, with byte-identical repeats to estimate stochastic variation.

Stop or shrink if:
- action choices are invariant to ancestry in cases where the oracle changes;
- effects are dominated by prompt instability;
- the task is so explicit that every model mechanically follows the metadata with no meaningful failure surface;
- wrong-ancestry controls do not separate metadata obedience from appropriate use.

### Stage 2 — only if Stage 1 survives
Expand frozen case families and models; test structured versus plain-language ancestry; test partial/unknown ancestry; add adversarial review; replicate the strongest positive or null result.

Prompts, policy thresholds and scoring gates would be frozen before target outputs are inspected. Null and negative results remain publishable outputs.

## Outputs and impact

Depending on the result, I would publish:
- the decision-layer extension fixtures and exact policy/oracle calculations;
- model-call manifests and measurement/scoring code where licensing permits;
- raw or suitably shareable outputs;
- null, negative and inconclusive results as well as positive ones;
- a short paper or technical report positioning the result explicitly relative to Bara's aggregation benchmark and existing action-provenance audits;
- if warranted, a small reusable **ancestry-sensitive action-selection probe** that can interoperate with stronger evaluation frameworks rather than becoming another generic benchmark platform.

The practical question is narrow but consequential for research agents, intelligence/review agents and other systems that move from apparent corroboration to recommendation or action. A provenance layer is only useful if the acting system uses its information correctly.

## Timeline and requested resources

Proposed duration: **4–6 weeks**, staged.

- Week 1: benchmark reproduction/adapter, frozen protocol, oracle-policy tests.
- Weeks 2–3: Stage 1 model screen and preregistered analysis.
- Weeks 4–5: conditional Stage 2 controls/replication if Stage 1 survives.
- Week 6: adversarial review, reproducibility package and write-up.

A directionally appropriate resource request is **approximately $8,000–$12,000**, to be finalised against Mercor's live form and award terms. Inference cost is not the main driver. Resources would primarily support researcher time, with smaller allocations for cross-model API calls, expert red-team/review through Mercor's network if useful, and reproducibility/publication work.

Funding would not be used to expand the study after a null result merely to consume the grant.

---

## Current ceilings before application

- Marc Bara already owns the core report-multiplicity / evidence-root mechanism and provenance-aware aggregation result.
- Junchi Liao already owns a separate source-authority/action-selection result.
- The surviving joint decision-layer delta is a hypothesis, not an established novelty claim.
- Provenance can be incomplete, false or mis-specified; wrong-ancestry controls are therefore part of the design.
- Supplied provenance is not proof of truth.
- A synthetic oracle-action benchmark does not establish deployment prevalence.
- One model-family result would not establish a general model defect.
- Current public award terms have been inspected at the posting level; no award agreement has been accepted. The unspecified-competitor restriction, institutional payee requirement and any full agreement terms remain consequential human gates.
- No model calls or spend are authorised by this draft.

## Human gate before any submit path

Current default: **HOLD / DO NOT SUBMIT**.

Before the grant route can reopen:
- establish a genuinely eligible institutional/company host, or explicitly ask Mercor whether an unaffiliated individual can apply;
- if the route reopens, inspect the live application fields and full award agreement;
- obtain the named competitor list before accepting any 12-month restriction on similar benchmark/evaluation work;
- decide whether the commercial-use licence, early benchmark access/private held-out right, publicity and open-commercial-output requirements are acceptable;
- decide final requested resource amount;
- confirm the cited prior-work framing and Mark's identity/contact representation;
- final submit only after Mark explicitly releases the completed application.

The offline research scaffold does not depend on this grant route and may remain preserved without model execution.
