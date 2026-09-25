# Mercor AI Safety Fund — non-binding EOI prep

Date: 25 September 2026

Status: **DRAFT / NOT SUBMITTED / HUMAN IDENTITY + FORM + TERMS GATE REMAINS MARK'S**

Owner:
https://jobs.ashbyhq.com/mercor/1d59ce50-4207-4d95-b7fd-5a01e90b0897/

Fresh owner-page facts checked 25 September 2026:
- Mercor says it is committing **$5m** to AI-safety research;
- independent researchers and small teams are explicitly eligible;
- named interests include oversight/control, agentic evaluation, interpretability, misalignment, sandbox escape and red-teaming methodology;
- support may include researcher time, API credits, expert grading/red-teaming/annotation and, subject to review, Mercor evaluation infrastructure;
- grantees are expected to publish a paper, open dataset, public methodology or field-useful tool;
- application asks for a **1–2 page Expression of Interest** covering team/background/research accomplishments, proposed project, outputs/impact, rough timeline and resources;
- no fixed grant size or application deadline is stated in the owner body.

Important ambiguity:
The Ashby shell labels the listing on-site, while Mercor's broader careers surface has inconsistent metadata around grant/research roles. Do not infer a travel or residency obligation from the shell alone. Re-read live application/award terms before submission or acceptance.

Preserve:
```text
EOI DRAFT != APPLICATION
OFFLINE HARNESS != MODEL RESULT
PUBLICATION EXPECTED != IP TERMS FULLY KNOWN
FUND SIZE != OUR GRANT SIZE
LOCATION METADATA != TRAVEL OBLIGATION
NO SIGNAL -> STOP / SHRINK
```

---

# Expression of Interest

## Team, background and prior work

I am Mark Goodbody, an independent UK systems engineer with more than 25 years of professional IT and telecommunications experience across infrastructure, networking, troubleshooting, support and small-team leadership. I do not have an academic affiliation and am not representing myself as a university researcher.

Over the last two years I have been building and testing small systems around AI provenance, correction, evidence handling and human oversight. Relevant current artifacts include:

- **EvidenceWatch** — a long-running evidence-drift/correction monitor with append-only state, explicit source authority, candidate quarantine and human review routing;
- **The Human Record** — a public, inspectable provenance/correction record system;
- a frozen experimental harness for provenance-sensitive agent evaluation with deterministic fixtures, stochastic-control planning and append-only run accounting.

The evaluation harness is offline-green but has **no real-model result yet**. Its current Stage A design contains 90 frozen requests, 23 hostile/unit tests, explicit run-to-run jitter controls and a hard stop if the target failure does not reproduce. The only attempted provider execution stopped before any API request because no authorised credential route was available. I preserve that as a blocked execution, not a null result.

## Proposed research project

### Research question

**Do current AI research/decision agents strengthen confidence or downstream approval when one evidentiary origin is presented as multiple apparently corroborating reports? If that failure occurs, can explicit source-ancestry information reduce it without making the agent systematically over-cautious or less responsive to genuinely independent evidence?**

The project does not claim that evidentiary independence or source ancestry are new ideas. The narrower target is an operational behaviour at the decision/action layer: whether a model treats repeated evidence as additional support, and whether an inspectable provenance intervention changes that behaviour in the intended direction.

### Stage A — reproduce or kill the failure

For each target model, the frozen initial screen uses:
- 15 baseline runs;
- 15 byte-identical baseline-replicate runs to estimate normal stochastic variation;
- 15 runs in which a second differently worded report carries the same distinctive synthetic facts.

The request explicitly asks the agent to assess evidentiary independence, confidence and recommended action. Agent-facing source IDs are neutral and the input does not label a source as duplicate, derivative, mutant or control.

The first gate is simple: if the repeated-origin condition does not strengthen confidence/action beyond the preregistered jitter/effect threshold, the failure claim is reduced or stopped. Thresholds and prompts are not changed after seeing outputs.

### Stage B — only if Stage A survives

The same frozen cases are compared under:
1. raw evidence;
2. a plain-language warning about possible source dependence;
3. correct structured ancestry;
4. a plausible but deliberately wrong ancestry control;
5. a lineage-aware hardening rerun.

The intervention counts as useful only if it reduces false corroboration **and** preserves appropriate response to genuinely independent evidence. The wrong-ancestry arm tests whether structured metadata merely attracts model attention irrespective of truth.

A small extension would add multiple synthetic case families and cross-model replication only after the first effect survives.

## Outputs and impact

The intended output is not another generic evaluation platform.

Depending on the result, I would publish:
- the frozen fixtures and mutation specification where licensing permits;
- measurement/scoring code and exact run identities;
- null, negative and inconclusive results as well as positive ones;
- a short technical report or paper describing the measured effect, controls and limitations;
- if warranted, a small reusable provenance-mutation test pack that can plug into stronger existing evaluation frameworks.

The practical impact would be evidence about one narrow oversight/control failure mode that matters whenever agents gather apparent corroboration before recommending an action. A positive result would justify testing provenance-aware controls more broadly. A null result would close or narrow the hypothesis and prevent further work from being justified by intuition alone.

## Timeline and requested resources

Proposed duration: **6–8 weeks**, staged.

**Stage 1 — reproduce/kill (approximately 2 weeks):**
- execute the frozen Stage A screen across a small set of current models;
- preserve raw outputs, usage and run accounting;
- analyse against preregistered stochastic controls;
- stop if the failure does not survive.

**Stage 2 — controls and replication (approximately 3–4 weeks, only if Stage 1 survives):**
- plain-language / correct-ancestry / wrong-ancestry comparisons;
- independent-evidence responsiveness control;
- add a small number of frozen case families;
- cross-model replication.

**Stage 3 — adversarial review and publication (approximately 1–2 weeks):**
- external grading/red-team review where useful;
- reproduce key runs;
- package code/data/method/report for public inspection.

A directionally correct resource request is **$10,000–$20,000**, with the final amount depending mainly on researcher-time support and access to human grading/red-teaming rather than inference cost alone. Suggested use:
- researcher time for controlled execution, analysis and write-up;
- API credits for cross-model replication;
- Mercor expert-network time for independent grading/red-teaming if the initial effect survives;
- evaluation infrastructure only where it reduces duplicated plumbing rather than changing the frozen experiment.

I would not use funding to expand the study after a null result simply to consume the grant.

---

## Current ceilings before application

- no model failure has been observed yet;
- one synthetic same-figures retelling does not establish actual common ancestry in real sources;
- supplied provenance is not proof of truth;
- one model result would not establish a general model defect;
- the current harness is a research scaffold, not a validated benchmark;
- no public-paper commitment has been legally accepted yet;
- exact Mercor award/IP/publication/location terms remain to be read at the live application/award stage.

## Human gate before submit

- review the live application fields and any terms;
- decide exact requested resource range;
- decide which public artifacts/repositories to link;
- confirm Mark's identity/contact representation;
- final submit only after Mark explicitly releases the completed application.
