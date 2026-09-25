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

# Proposal draft — hostile-review revision

## 1. THE PROBLEM

Research briefs, evidence syntheses and institutional decisions often depend on claims whose underlying sources later change: a publisher issues a correction or retraction, a dataset is revised, an owner changes a reported figure, or an apparently new source turns out to repeat the same evidentiary root.

Today, the person who relied on the claim usually has to notice that change manually or through a tool that watches only one part of the problem. Crossmark exposes formal scholarly updates; reference managers organise literature; citation tools surface later citations; page monitors detect changed webpages. The remaining workflow question is narrower: **did the evidence state behind a claim I relied on materially change, and which brief, review or decision now needs another look?**

I have not yet measured how often this creates material work for target research teams. That is a pilot question, not a fact I want to manufacture. The measurable cost to test is reviewer time spent rechecking unchanged evidence versus time saved by correctly routing only material changes.

## 2. YOUR WORKFLOW

EvidenceWatch is a long-running agent for post-reliance evidence monitoring.

1. A researcher defines a bounded question, the sources relevant to it, which source has authority for which state, and the downstream item that relies on the claim.
2. EvidenceWatch fetches and fingerprints those sources on a schedule.
3. Identical observations are suppressed before model work while an append-only ledger preserves history.
4. When content changes, a model extracts only the bounded evidence needed for the monitored question.
5. The engine keeps source role separate from state authority: a derivative or supporting source cannot silently overwrite the configured owner state.
6. It compares the new typed evidence with prior canonical state.
7. Non-material paraphrase and derivative repetition stay quiet. Corrections, source loss/recovery, disagreement or genuinely new support can trigger review.
8. The human sees the before/after state, source role, revision history and affected downstream work, then decides whether to revise, escalate or leave it unchanged.

The current prototype is standalone Node.js. A new reversible adapter now accepts standard CSL-JSON reference-manager exports and turns them into EvidenceWatch watch configurations. CSL JSON is an import/export format supported by Zotero. Imported references default to candidate/non-authoritative sources; authority and independence must be assigned explicitly.

This is currently a **file handoff, not a live Zotero or ReadCube integration**. A funded pilot would automate the handoff through the supported integration surface of the reference-manager or shared evidence-library workflow chosen with a pilot user.

## 3. TRUST, AUDIT AND GOVERNANCE

Trust is carried by inspectable state rather than a model verdict.

EvidenceWatch rebuilds canonical state from an append-only ledger after restart. Observation fingerprints suppress duplicate model work without deleting history. Authority is explicit configuration, separate from evidentiary role. Discovered sources are quarantined as candidates rather than recursively gaining authority.

A concrete refusal/escalation behaviour is already tested: a newly discovered candidate source may be analysed but cannot establish or advance canonical state and cannot create a canonical alert until a human/configuration change promotes it. When a current authority source becomes unreachable, EvidenceWatch flags review but preserves the last known claim state instead of converting "unreachable" into "false".

The user remains accountable for the research output. EvidenceWatch does not automatically rewrite a brief, retract a claim or declare a source true or false. Uncertainty or contradiction routes to review.

The current suite has 43 deterministic tests, including correction, duplicate suppression, derivative disagreement, authority boundaries, restart reconstruction, outage/recovery, candidate quarantine, browser-demo behaviour and the CSL-JSON handoff.

## 4. TEAM

I am Mark Goodbody, a UK Senior IT and Telecoms Engineer with more than 25 years of professional experience across infrastructure, networking, support, troubleshooting and small-team leadership.

I built EvidenceWatch from independent work on provenance, correction and human/AI answerability. I remain the human release and accountability gate. Multiple AI systems are used for implementation and adversarial review; model agreement is not treated as validation.

## 5. WHERE YOU ARE TODAY

EvidenceWatch is a working prototype, not a validated research product.

The deterministic browser demo shows an owner claim moving from a baseline of three incidents, through derivative repetition that does not change canonical state, to an owner correction from three to four that creates one downstream-review alert while preserving the earlier state.

A separate live technical witness ran the engine against real public owner pages using NVIDIA Nemotron; a second same-ledger run deduplicated unchanged observations instead of issuing another alert.

Demo:
https://youtu.be/0hdwNc_t4pM

There are no claimed research customers or validated user-efficiency results. The CSL-JSON handoff is now merged on EvidenceWatch main (`c969a7d4123458eda874fa328a4258d46b617113`) with post-merge CI green. It exists to test the next step toward an actual researcher workflow, not to pretend that integration is complete.

Related public provenance work:
https://github.com/markgoodbody-bit/human-record
https://pleasestartfromhere.com/

## 6. ALTERNATIVES AND COMPETITORS

Strong existing owners already cover important parts of this problem:

- Crossmark / Crossref exposes the current status of scholarly content, including corrections, retractions and updates: https://www.crossref.org/services/crossmark/
- Visualping and Distill are mature webpage-change monitors with history, conditions and AI summaries: https://visualping.io/ and https://distill.io/
- Zotero and ReadCube Papers own reference/library workflows; ReadCube also provides literature monitoring and review tooling: https://www.zotero.org/ and https://about.readcube.com/
- scite provides living citation context, including supporting/contrasting citations and retraction signals: https://scite.ai/

EvidenceWatch should be killed or narrowed if one of these, or another product, already provides the full useful loop better. The current product hypothesis is the conjunction of claim-level cross-source state, explicit source ancestry/independence, explicit state authority, correction history and a downstream "what must I revisit?" dependency.

## 7. WHERE THIS GOES

The next stage is a bounded research-workflow pilot.

The initial user group would be teams maintaining living evidence syntheses, research-integrity reviews or other recurring briefs where source currentness matters. The pilot would measure:
- time from authoritative source correction to affected work being flagged;
- material/false alert rate;
- reviewer minutes per alert;
- duplicate/derivative suppression;
- whether users can reconstruct why an alert happened without trusting the model;
- setup burden for explicit source authority.

A negative result is useful. If setup burden is too high, material changes are too rare, or reviewers cannot trust the routing, the product should be narrowed or stopped.

If later commercialised, the plausible buyer is an institution or research team paying for monitored workspaces/integrations. A workspace or monitored-collection subscription is a hypothesis only; pricing has not been tested.

## 8. FIT WITH DIGITAL SCIENCE

EvidenceWatch sits in evidence synthesis and research integrity.

The fit is not simply "AI with provenance". It is a multi-step agent that must know when to stay quiet, when to flag a change, and when it lacks authority to act. That is directly aligned with Digital Science's 2026 emphasis on agents embedded in researcher workflows with provenance, governance and accountability.

Digital Science also owns products close to the natural integration surface, particularly ReadCube and its literature-management/review workflows. I would value help deciding whether this dependency-monitoring pattern belongs inside a reference-manager/literature-review workflow at all, and testing it with researchers before hardening the wrong product.

## 9. BUDGET

Up to £25,000 would fund a bounded pilot rather than general project overhead:

- £10,000 — engineering time for a supported reference-library/workflow integration and deployment;
- £6,000 — researcher workflow testing, observation and evaluation;
- £4,000 — model/API and infrastructure costs for repeated controlled monitoring;
- £3,000 — independent security/provenance/adversarial review;
- £2,000 — reproducibility packaging and documentation.

What this enables that I cannot do today is the important part: move from a technically working standalone prototype to a measured test inside a workflow that researchers already use, with enough external review to discover whether the product residue is real.

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
