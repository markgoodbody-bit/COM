# Digital Science Catalyst Grant 2026 — EvidenceWatch application prep

Date: 25 September 2026

Status: **NON-BINDING DRAFT / NOT SUBMITTED / HUMAN IDENTITY + TERMS + SUBMISSION GATE REMAINS MARK'S**

Owner source checked 25 September 2026:
- 2026 theme: **Agentic workflows you can trust**
- open globally to individuals, startups and research teams;
- prototype, working product or well-formed concept accepted;
- award up to **£25,000**, described as equity-free;
- application deadline: **5 October 2026, 17:00 BST**;
- proposal maximum: **1,500 words**;
- owner explicitly asks for multi-step research workflows with provenance, audit trails, governance, human review/override and measurable outcomes.

Candidate object: **EvidenceWatch**, scoped to research-integrity / evidence-synthesis workflows.

Preserve:
```text
APPLICATION PREPARED != APPLICATION SUBMITTED
PROTOTYPE != VALIDATED PRODUCT
LIVE TECHNICAL WITNESS != RESEARCH USER VALIDATION
PROVENANCE != TRUTH
MATERIAL CHANGE FLAG != AUTOMATIC CORRECTION
POSSIBLE £25K != AWARDED £25K
```

---

# Proposal draft

## 1. THE PROBLEM

Research briefs, evidence syntheses and institutional decisions often depend on claims whose underlying sources later change: an owner corrects a figure, a paper is amended or retracted, a dataset is revised, a policy page is replaced, or an apparently new source turns out to repeat the same evidentiary root.

Today, the person who relied on the claim usually has to notice the change manually. Reference managers and literature-search tools help people find and organise sources, but the downstream dependency problem remains: **which existing brief, review or decision needs another look because the evidence it relied on materially changed?**

The cost is not only missed corrections. Rechecking everything continuously is also expensive and noisy. A useful system therefore has to distinguish material source change from formatting changes, duplicate observations, derivative repetition and genuinely new independent support.

EvidenceWatch is aimed at researchers, research-integrity teams, evidence-synthesis groups and other people maintaining work that depends on changing public evidence.

## 2. YOUR WORKFLOW

EvidenceWatch is a long-running agent rather than a one-shot question-answering tool.

1. A user defines a bounded monitored question, the sources relevant to it, which source has authority for which state, and which downstream work relies on the claim.
2. EvidenceWatch fetches and fingerprints the selected sources on a schedule.
3. It suppresses identical observations before model work and preserves an append-only observation ledger.
4. When content changes, an AI analysis step extracts only the bounded evidence needed for the monitored question.
5. The engine keeps source role separate from state authority: a derivative or supporting source cannot silently overwrite the configured owner state.
6. It compares the new typed evidence with the prior canonical state.
7. Non-material paraphrase and derivative repetition stay quiet. Material changes, owner corrections, source loss, recovery or genuinely new support can create review alerts.
8. The human sees the before/after evidence state, source role, revision history and the downstream work affected.
9. The person decides whether to revise, reject, escalate or leave the dependent work unchanged.

The current prototype is a standalone Node.js agent with deterministic replay and an unattended scheduler. It can use NVIDIA Nemotron through an OpenAI-compatible endpoint for bounded change analysis. The model does not decide source authority or truth.

## 3. TRUST, AUDIT AND GOVERNANCE

Trust is carried by inspectable state rather than by asking the user to accept a model conclusion.

EvidenceWatch preserves an append-only ledger and rebuilds canonical state from that ledger after restart. Observation fingerprints suppress duplicate model work without deleting history. Authority is configured explicitly and is separate from evidentiary role. Candidate/discovered sources are quarantined rather than recursively acquiring authority.

A review alert contains the evidence transition that caused it and the dependent work that may need another look. The system distinguishes source-unreachable from analysis-failed, and source recovery from continued outage. It keeps the last known claim state when a source disappears instead of silently turning "unreachable" into "false".

The user remains accountable for the research output. EvidenceWatch does not automatically rewrite a brief, retract a claim, or label a source true or false. When evidence is uncertain, contradictory or outside the configured scope, the correct output is review/unknown rather than manufactured certainty.

The current test suite includes 36 deterministic tests covering correction, duplicate suppression, derivative disagreement, authority boundaries, restart reconstruction, outage/recovery, candidate-source quarantine and browser-demo behaviour.

## 4. TEAM

Mark Goodbody is a UK systems engineer with more than 25 years of professional IT and telecommunications experience, including senior engineering, support, network, infrastructure and team-lead roles.

The project grew from independent work on provenance, correction, bounded reasoning and human/AI answerability. Mark is the human originator and release/legal-account gate. Development and hostile review use multiple AI systems as tools and independent apertures; agreement between models is not treated as validation.

## 5. WHERE YOU ARE TODAY

EvidenceWatch is a working prototype, not a validated research product.

The deterministic browser demonstration shows a monitored owner claim moving from an initial baseline of three incidents, through derivative repetition that does not change canonical state, to an owner correction from three to four that creates one downstream-review alert while preserving the earlier state.

A separate live technical witness ran the same engine against real public owner pages using NVIDIA Nemotron; a second same-ledger run deduplicated unchanged observations instead of issuing another alert.

Demo:
https://youtu.be/0hdwNc_t4pM

There are currently no claimed research customers or validated user-efficiency results. That is the next thing the grant would help test.

Related public provenance work:
https://github.com/markgoodbody-bit/human-record
https://pleasestartfromhere.com/

## 6. ALTERNATIVES AND COMPETITORS

The default alternative is manual monitoring: researchers periodically revisit important sources, subscribe to publisher notices where available, or discover changes later through search, colleagues or downstream review.

Existing literature-search, reference-management, correction/retraction and evidence-synthesis tools own important parts of this problem and should remain the stronger tools for discovery, bibliography management and formal publication status.

EvidenceWatch is narrower. It is not trying to replace literature search or decide whether a paper is trustworthy. Its specific job is to maintain an inspectable dependency between a bounded claim, its changing evidence lineage and the downstream work that relied on it, then ask for human review only when that dependency materially changes.

## 7. WHERE THIS GOES

The next stage is a measured research-workflow pilot, not immediate commercialisation.

The aim would be to connect EvidenceWatch to a small number of real evidence-synthesis or research-integrity workflows and measure:
- time from authoritative source correction to affected work being flagged;
- false/material alert rate;
- duplicate/derivative suppression;
- provenance completeness;
- human review time per alert;
- whether users can reconstruct why an alert happened without trusting the model.

If later operated as a hosted product, institutions, publishers or research teams could plausibly fund monitored workflows and integrations. No pricing model is currently claimed.

## 8. FIT WITH DIGITAL SCIENCE

EvidenceWatch sits primarily in **evidence synthesis and research integrity**.

The fit is direct: it is a multi-step agent acting on research evidence, with explicit provenance, auditability, governance boundaries and human review. Its useful behaviour includes knowing when not to act: derivative repetition should remain quiet; an untrusted discovered source should not acquire authority; uncertain or conflicting evidence should be escalated rather than collapsed into a confident answer.

Digital Science's research-workflow expertise and products across discovery, identifiers, open research and institutional research systems make it a useful environment in which to test whether this narrow dependency-monitoring pattern belongs inside real researcher workflows rather than as a standalone demo.

## 9. BUDGET

A grant of up to £25,000 would fund a bounded pilot rather than general project overhead.

Indicative use:
- **£9,000** — engineering time to harden the prototype for a real research workflow, integrations and deployment;
- **£5,000** — model/API and infrastructure costs for repeated controlled monitoring and evaluation;
- **£5,000** — external researcher/user testing, workflow observation and evaluation;
- **£3,000** — independent security/provenance review and adversarial testing;
- **£3,000** — documentation, reproducibility packaging and contingency for integration costs.

The concrete outcome would be a deployable pilot plus an evaluation report. A null or negative result is acceptable: if the workflow creates more review burden than it saves, or cannot distinguish material change reliably enough for real research use, that should be reported rather than hidden.

---

## Internal review notes

### Strong fit
- Owner asks for an agent embedded in a research workflow, not another chatbot.
- EvidenceWatch is genuinely multi-step and long-running.
- Provenance / governance / audit are native to the architecture rather than post-hoc marketing.
- Refuse/flag/escalate behaviour is demonstrable.
- A measurable research-integrity pilot is an honest next stage.

### Weaknesses to disclose, not disguise
- no research user/customer validation yet;
- current live witness is cybersecurity-owner-page monitoring, not a scholarly literature pilot;
- private EvidenceWatch repository currently limits source inspection by judges unless a bounded public release is later earned;
- Digital Science explicitly prefers a tool embedded in an existing research system. EvidenceWatch is currently standalone;
- commercial market/pricing is unproven and not a project purpose.

### Human gate before submission
- Mark reviews identity/team wording;
- decide whether the existing unlisted demo is suitable to share with Digital Science;
- re-read the live application/privacy/award terms;
- decide whether £25,000 budget shape is appropriate or should be reduced;
- fill identity/contact fields;
- final submit.
