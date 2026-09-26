# Digital Science Catalyst Grant 2026 — EvidenceWatch submission packet

Date: 25 September 2026

Status: **FORM-READY COPY / NOT SUBMITTED / HUMAN TERMS + IDENTITY + FINAL SUBMIT GATE**

Owner source rechecked 25 September 2026:
- theme: **Agentic workflows you can trust**
- open globally to individuals, startups and research teams;
- prototype / working product / well-formed concept accepted;
- award up to **£25,000**, described as equity-free;
- applications close **5 October 2026, 17:00 BST**;
- proposal maximum **1,500 words**;
- shortlisted applicants may be invited to a short interview with a live demo.

Current proposal word count:
**1297 words**

Current EvidenceWatch private main:
`9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f`

Current CI:
**SUCCESS**

Current deterministic suite:
**62 tests / 62 pass**

Latest EvidenceWatch main change:
**real-workflow owner subtraction added after pilot protocol/scorer; runtime semantics unchanged / no live pilot or provider call**

Engineering witness:
`coordination/build_ledger/EVIDENCEWATCH_RESEARCH_HANDOFF_WITNESS_20260925.md`

Selectable synthetic research demo receipt:
`coordination/build_ledger/EVIDENCEWATCH_SELECTABLE_RESEARCH_DEMO_20260925.md`

Existing reviewed unlisted demo:
https://youtu.be/0hdwNc_t4pM

Related public work:
- https://github.com/markgoodbody-bit/human-record
- https://pleasestartfromhere.com/

Preserve:
```text
APPLICATION = NOT SUBMITTED
GRANT FIT != PRODUCT VALIDATION
FORMAL RETRACTION ALERTING != OUR GAP
CSL HANDOFF != LIVE PRODUCT INTEGRATION
SYNTHETIC RESEARCH WITNESS != RESEARCHER VALIDATION
SYNTHETIC RESEARCH DEMO != LIVE SCHOLARLY EVIDENCE
NO PILOT PARTNER CLAIMED
NO RESEARCH CUSTOMERS CLAIMED
NO PRICING VALIDATION CLAIMED
FINAL TERMS / IDENTITY / SUBMIT = MARK HUMAN GATE
```

---

## 1. THE PROBLEM

The initial user is a living systematic review team deciding whether an existing conclusion needs reopening after evidence already included changes: a dataset revision, authority update, replaced source page, or apparent corroboration from the same evidentiary root.

Formal retraction/correction handling is not the gap. Zotero and Crossmark expose formal status. Cochrane now matches newly retracted included studies to affected reviews and routes impact assessment; its update guidance also covers relevant corrections and additional information from previously included studies.

The residual is narrower: can a small agent catch material changes outside those well-owned paths and route only affected downstream work for human review?

The University of Bern living review already checked included preprints for journal publication and re-extracted changed data. One Lombardi preprint reported 41/138 asymptomatic positives; after longer follow-up, the final article reported 17/139. The maintenance task is real and existing practice handles it; whether automation reduces burden is the pilot question. Sources: https://doi.org/10.1186/s13643-023-02325-y and https://doi.org/10.1016/j.cmi.2020.06.013

## 2. YOUR WORKFLOW

EvidenceWatch is a configured multi-step monitoring agent. Humans set the question, source policy and dependents; observation, analysis, state comparison and review routing then run on schedule.

1. A researcher defines the bounded question, relevant sources, source authority and downstream dependents.
2. EvidenceWatch fetches and fingerprints sources.
3. Identical observations are suppressed before model work while an append-only ledger preserves history.
4. Changed content is analysed only for evidence relevant to the monitored question.
5. Source role remains separate from state authority: derivative/supporting sources cannot overwrite the configured owner state.
6. Typed evidence is compared with prior canonical state.
7. Non-material paraphrase and derivative repetition stay quiet; corrections, source loss/recovery, disagreement or genuinely new support can trigger review.
8. The human sees before/after state, source role, revision history and affected downstream work, then decides what to do.

The prototype is standalone Node.js. A reversible adapter converts standard CSL-JSON reference-manager exports into watch configurations. Imported references default to candidate/non-authoritative sources; authority and independence require explicit assignment.

The first proposed integration target is **Zotero**. A pilot would use one living systematic review team's existing library and automate the current file handoff through a supported integration surface.

This remains a **file handoff, not a live Zotero or ReadCube integration**, and no pilot partner is established.

## 3. TRUST, AUDIT AND GOVERNANCE

Trust is carried by inspectable state rather than a model verdict.

EvidenceWatch rebuilds canonical state from an append-only ledger after restart. Observation fingerprints suppress duplicate model work without deleting history. Authority is explicit configuration, separate from evidentiary role. Discovered sources are quarantined as candidates rather than recursively gaining authority.

A concrete refuse/flag behaviour is tested: a derivative source repeating the owner stays quiet; if it diverges, EvidenceWatch flags review but refuses to overwrite canonical state. Discovered candidates likewise cannot establish or advance state until explicit promotion. If an authority source becomes unreachable, the last known state is preserved rather than converted into "false".

The user remains accountable. EvidenceWatch never rewrites a brief or declares truth. Tested disagreement, source-loss and candidate-discovery cases preserve state or route review without canonical overwrite; model errors can still go undetected.

The current suite has 62 deterministic tests, including correction, duplicate suppression, derivative disagreement, authority boundaries, restart reconstruction, outage/recovery, candidate quarantine, browser-demo behaviour and the CSL-JSON handoff.

## 4. TEAM

I am Mark Goodbody, a UK Senior IT and Telecoms Engineer with more than 25 years of professional experience across infrastructure, networking, support, troubleshooting and small-team leadership. My relevant expertise is systems rather than academic research: state, failure recovery, audit trails and operating under incomplete information.

I built EvidenceWatch from independent work on provenance, correction and human/AI answerability. I remain the human release and accountability gate. Multiple AI systems are used for implementation and adversarial review; model agreement is not treated as validation. The proposed pilot is deliberately where research-workflow expertise enters: it tests the engineering against a living review team's actual practice rather than treating my domain assumptions as validated.

## 5. WHERE YOU ARE TODAY

EvidenceWatch is a working prototype, not a validated research product.

The deterministic browser demo shows a baseline owner claim, derivative repetition that stays quiet, then an owner correction that preserves the earlier state and creates one downstream-review alert.

A one-watch/two-run live NVIDIA Nemotron witness against public owner pages deduplicated unchanged observations on the second run. One internally inconsistent model-status field remains unresolved rather than being treated as validation.

Demo:
https://youtu.be/0hdwNc_t4pM

There are no research customers or validated efficiency results. Merged work includes the CSL-JSON handoff, DOI-boundary repair, restart/correction witness, a predeclared shadow-mode pilot protocol and deterministic offline scorer. The protocol freezes human labels/configuration before scoring; the scorer measures material-change sensitivity, false-alert burden, downstream routing, time-to-flag and reviewer minutes without model calls. A synthetic-content / real-format CSL witness also survived restart and routed a controlled 1.8→1.2 publisher correction for review. This is engineering/pilot instrumentation, not researcher validation.

Related public provenance work:
https://github.com/markgoodbody-bit/human-record
https://pleasestartfromhere.com/

## 6. ALTERNATIVES AND COMPETITORS

Stronger owners remove most mechanism novelty:

- **Crossref/Europe PMC, Zotero/Crossmark and Cochrane** own preprint-publication linking, formal status and important correction-to-review paths: https://www.crossref.org/documentation/research-nexus/posted-content-includes-preprints/ and https://www.cochrane.org/about-us/news/cochrane-strengthens-systems-manage-retracted-publications-its-published-reviews
- **ReadCube and scite** own literature monitoring, shared libraries, review workflows, citation context and integrity alerts: https://about.readcube.com/ and https://scite.ai/
- **Refract** owns reproducible source-change events; **AIEP P170** specifies evidence-dependency graphs and cascade impact analysis: https://github.com/refract-org/refract and https://aiep.dev/specs/p170_aiep_evidence_dependency_graph_protocol_os/
- Digital Science's **PostPub/VIRUS** track integrity events/downstream impact; **Perma.cc** preserves relied-on web states.

EvidenceWatch is not a new change detector or dependency-graph idea. Its surviving hypothesis is integration: can heterogeneous post-reliance source state, explicit authority, materiality filtering, a human-approved dependency map and review routing fit an existing workflow with low enough burden to be useful?

If a stronger workflow already does this, or the residual change class is too rare, stop or narrow.

## 7. WHERE THIS GOES

The next stage is a bounded workflow-integration pilot.

One living systematic review team would use its existing reference library. Because Cochrane and related workflows already own surveillance and important correction routes, the pilot would isolate residual changes and compare EvidenceWatch with existing practice on a pre-labelled set, measuring:
- time to flag affected work;
- missed material changes and false alerts;
- reviewer, setup and maintenance minutes;
- whether users can reconstruct why an alert happened without trusting the model.

Stop or narrow if maintenance exceeds saved review time, residual changes are too rare, existing practice performs as well, or misses are unacceptable.

If later commercialised, the plausible buyer is an institution or research team paying for monitored workspaces/integrations. Initial adoption is hypothesised around evidence-synthesis teams, health-evidence/guideline units and similar organisations maintaining updateable reviews. Pricing is untested.

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

## Final human review checklist

Before submission:

- open the live Digital Science application from the owner page;
- confirm the application still uses the published 2026 criteria and deadline;
- read any privacy, publicity, IP, award or participation terms shown in the live form;
- confirm name/email/contact fields;
- decide whether to provide the existing unlisted demo URL;
- preserve the distinction between the cybersecurity demo and the synthetic research fixture;
- confirm the staged £5k / £14k / £6k budget;
- check that no field requires an unsupported company, customer, revenue, academic-affiliation, pilot-partner or user claim;
- submit only after Mark explicitly releases the final form.

Live form / privacy check — 25 September 2026:
- the owner-page Apply link resolves to the live Google Form titled `Welcome to the 2026 Catalyst Grant Application`;
- the form is three pages; page 1 asks for email;
- no email was entered and the identity gate was not crossed, so pages 2–3 remain uninspected;
- the form links Digital Science's public Privacy Notice. That notice says online forms / competition entries may collect name, email and other basic contact/professional information; data may be shared within the Digital Science group and with service providers for stated business purposes; infrastructure may involve transfers to the USA/other locations with stated safeguards; sensitive personal information should not be supplied unless specifically requested;
- Digital Science's general website Terms are public site-use terms, not a Catalyst award agreement;
- no separate public 2026 Catalyst award agreement or complete application-specific terms were located in the owner materials reviewed here.

Preserve:
```text
PUBLIC PRIVACY NOTICE REVIEWED != APPLICATION-SPECIFIC AWARD TERMS REVIEWED
FORM PAGE 1 REACHED != LATER FIELDS INSPECTED
EMAIL FIELD VISIBLE != IDENTITY DISCLOSED
```

No organiser contact, account action, identity disclosure through the form, terms acceptance or submission has been performed from this packet.
