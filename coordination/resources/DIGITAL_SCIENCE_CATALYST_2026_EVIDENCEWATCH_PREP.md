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

The initial user is a living systematic review team deciding whether an existing conclusion needs reopening after evidence already included changes: a dataset revision, authority update, replaced source page, or apparent corroboration from the same evidentiary root.

Formal retraction/correction handling is not the gap. Zotero and Crossmark expose formal status. Cochrane now matches newly retracted included studies to affected reviews and routes impact assessment; its update guidance also covers relevant corrections and additional information from previously included studies.

The residual is narrower: can a small agent catch material changes outside those well-owned paths and route only affected downstream work for human review?

A 2016 PLOS ONE study found textual drift in over 75% of comparable archived/live web references, but that does not establish consequential change. Whether residual changes are frequent enough to justify another monitor is a pilot question. Source: https://doi.org/10.1371/journal.pone.0167475

## 2. YOUR WORKFLOW

EvidenceWatch is a configured multi-step monitoring agent. Humans set the question, source policy and dependents; scheduled observation, analysis, state comparison and review routing then run without another prompt.

1. A researcher defines a bounded question, the sources relevant to it, which source has authority for which state, and the downstream item that relies on the claim.
2. EvidenceWatch fetches and fingerprints those sources on a schedule.
3. Identical observations are suppressed before model work while an append-only ledger preserves history.
4. When content changes, a model extracts only the bounded evidence needed for the monitored question.
5. The engine keeps source role separate from state authority: a derivative or supporting source cannot silently overwrite the configured owner state.
6. It compares the new typed evidence with prior canonical state.
7. Non-material paraphrase and derivative repetition stay quiet. Corrections, source loss/recovery, disagreement or genuinely new support can trigger review.
8. The human sees the before/after state, source role, revision history and affected downstream work, then decides whether to revise, escalate or leave it unchanged.

The current prototype is standalone Node.js. A new reversible adapter accepts standard CSL-JSON reference-manager exports and turns them into EvidenceWatch watch configurations. CSL JSON is an import/export format supported by Zotero. Imported references default to candidate/non-authoritative sources; authority and independence must be assigned explicitly.

The first proposed integration target is **Zotero**. A pilot would recruit one living systematic review team that already maintains its included-study library in Zotero or a compatible reference manager, then automate the current file handoff through a supported integration surface. No pilot partner is established yet.

This is currently a **file handoff, not a live Zotero or ReadCube integration**.

## 3. TRUST, AUDIT AND GOVERNANCE

Trust is carried by inspectable state rather than a model verdict.

EvidenceWatch rebuilds canonical state from an append-only ledger after restart. Observation fingerprints suppress duplicate model work without deleting history. Authority is explicit configuration, separate from evidentiary role. Discovered sources are quarantined as candidates rather than recursively gaining authority.

A concrete refuse/flag behaviour is tested: a derivative source repeating the owner stays quiet; if it diverges, EvidenceWatch flags review but refuses to overwrite canonical state. Discovered candidates likewise cannot establish or advance state until explicit promotion. If an authority source becomes unreachable, the last known state is preserved rather than converted into "false".

The user remains accountable. EvidenceWatch never rewrites a brief or declares truth. Tested disagreement, source-loss and candidate-discovery cases preserve state or route review without canonical overwrite; model errors can still go undetected.

The current suite has 54 deterministic tests, including correction, duplicate suppression, derivative disagreement, authority boundaries, restart reconstruction, outage/recovery, candidate quarantine, browser-demo behaviour and the CSL-JSON handoff.

## 4. TEAM

I am Mark Goodbody, a UK Senior IT and Telecoms Engineer with more than 25 years of professional experience across infrastructure, networking, support, troubleshooting and small-team leadership. My relevant expertise is systems rather than academic research: state, failure recovery, audit trails and operating under incomplete information.

I built EvidenceWatch from independent work on provenance, correction and human/AI answerability. I remain the human release and accountability gate. Multiple AI systems are used for implementation and adversarial review; model agreement is not treated as validation. The proposed pilot is deliberately where research-workflow expertise enters: it tests the engineering against a living review team's actual practice rather than treating my domain assumptions as validated.

## 5. WHERE YOU ARE TODAY

EvidenceWatch is a working prototype, not a validated research product.

The deterministic browser demo shows an owner claim moving from a baseline of three incidents, through derivative repetition that does not change canonical state, to an owner correction from three to four that creates one downstream-review alert while preserving the earlier state.

A one-watch/two-run live witness used NVIDIA Nemotron against real public owner pages; the second same-ledger run deduplicated unchanged observations. One model-status field was internally inconsistent and remains unresolved rather than being treated as validation.

Demo:
https://youtu.be/0hdwNc_t4pM

There are no claimed research customers or validated user-efficiency results. The CSL-JSON handoff, DOI-boundary repair and controlled restart/correction witness are merged. A predeclared shadow-mode pilot protocol and deterministic offline scorer are now also merged; the protocol requires human labels and configuration to be frozen before scoring, and the scorer measures material-change sensitivity, false-alert burden, downstream routing, time-to-flag and reviewer minutes without model calls. In the synthetic-content / real-format CSL witness, three references imported, one unfetchable reference was skipped, state survived an engine restart, and a controlled publisher correction changed the bounded result from 1.8 to 1.2 while routing the dependent brief for review. This is engineering/pilot instrumentation, not researcher validation.

Related public provenance work:
https://github.com/markgoodbody-bit/human-record
https://pleasestartfromhere.com/

## 6. ALTERNATIVES AND COMPETITORS

Stronger owners remove most of the mechanism as a novelty claim:

- **Zotero, Crossmark and Cochrane** own formal status and important retraction/correction-to-review paths: https://www.cochrane.org/about-us/news/cochrane-strengthens-systems-manage-retracted-publications-its-published-reviews
- **ReadCube and scite** own literature monitoring, shared libraries, systematic-review workflows, citation synchronisation/context and integrity alerts: https://about.readcube.com/ and https://scite.ai/
- **Refract** owns reproducible semantic change events from versioned public sources; **AIEP P170** already specifies evidence-dependency graphs and cascade impact analysis: https://github.com/refract-org/refract and https://aiep.dev/specs/p170_aiep_evidence_dependency_graph_protocol_os/
- Digital Science's **PostPub/VIRUS** track integrity events and downstream impact; **Perma.cc** preserves the relied-on web state.

EvidenceWatch is therefore not a new change detector or dependency-graph idea. The surviving hypothesis is integration: **can heterogeneous post-reliance source state, explicit authority, materiality filtering, an existing or human-approved dependency map and human review routing be joined inside a current research workflow with low enough burden to be useful?**

If a stronger workflow already provides that integration, or the residual change class is too rare to matter, EvidenceWatch should be killed or narrowed.

## 7. WHERE THIS GOES

The next stage is a bounded workflow-integration pilot, not a new evidence architecture.

One living systematic review team would use its existing reference library. Cochrane already owns new-evidence surveillance and a retraction-impact route, so the pilot would isolate residual changes not handled adequately by those processes and compare EvidenceWatch with existing practice on a pre-labelled material/non-material set, measuring:
- time to flag affected work;
- missed material changes and false alerts;
- reviewer minutes, duplicate suppression, and setup/maintenance time;
- whether users can reconstruct why an alert happened without trusting the model.

Stop or narrow if maintenance exceeds saved review time, residual changes are too rare, existing practice performs as well, or missed-change rate is unacceptable.

If later commercialised, the plausible buyer is an institution or research team paying for monitored workspaces/integrations. The initial adoption hypothesis is evidence-synthesis teams at universities, health evidence or guideline units, and similar organisations already maintaining updateable reviews. A workspace or monitored-collection subscription is a hypothesis only; pricing has not been tested.

## 8. FIT WITH DIGITAL SCIENCE

EvidenceWatch sits in evidence synthesis and research integrity.

Its mechanisms are not novel. The fit is a multi-step agent that must know when to stay quiet, flag a change, or refuse to act without authority, matching Digital Science's emphasis on embedded workflows with provenance, governance and accountability.

Digital Science also owns several strong adjacent systems, including ReadCube and the PostPub/VIRUS Catalyst work. That makes it a useful place to falsify the integration hypothesis: does joining residual post-reliance change monitoring to an existing workflow save enough reviewer work, at acceptable error and maintenance cost, to deserve a product?

## 9. BUDGET

Up to £25,000 would be staged.

- **Stage 1, £5,000 cap:** workflow integration and testing whether the review's own outcome→study structure can propose dependency mappings for human batch approval; matched-baseline fixtures and setup/maintenance measurement. Stop if burden or problem incidence makes the workflow implausible.
- **Stage 2, £14,000 cap:** only if Stage 1 survives; pilot engineering plus researcher observation/evaluation, including predeclared materiality labels and missed-change measurement.
- **Stage 3, £6,000 cap:** model/API/infrastructure, independent security/provenance review and reproducibility documentation as required.

This moves a working standalone prototype into a measured existing-workflow test while preserving a stop path.

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
