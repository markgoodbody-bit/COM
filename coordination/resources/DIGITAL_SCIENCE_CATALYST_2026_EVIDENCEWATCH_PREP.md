# Digital Science Catalyst Grant 2026 — EvidenceWatch application prep

Date: 25 September 2026

Status: **NON-BINDING DRAFT / NOT SUBMITTED / HUMAN IDENTITY + TERMS + SUBMISSION GATE REMAINS MARK'S**

Owner source checked 26 September 2026:
- 2026 theme: **Agentic workflows you can trust**
- open globally to individuals, startups and research teams;
- prototype, working product or well-formed concept accepted;
- award up to **£25,000**, described as equity-free;
- application deadline: **5 October 2026, 17:00 BST**;
- proposal maximum: **1,500 words**;
- owner explicitly asks applicants to name the affected research decision, existing workflow/tool, refusal-or-escalation behaviour and measurable outcome, alongside provenance, audit trails, governance and human review/override.

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

The residual is narrower: can an agent catch a material change to an already-relied-on source that arrives as neither a new study nor a formal status event, then route only affected downstream work for human review?

A public baseline from the University of Bern shows this is recurring work: its living review ran weekly automated searches that added 100–200 records, checked preprint publication status in each update, and re-extracted data when content changed. One Lombardi preprint reported 41/138 asymptomatic positives; after longer follow-up, the final article reported 17/139. A separate six-review evaluation reported 3–300 citations screened and 5 minutes–32 hours of author-team work per month. That is total living-review workload, not the narrower burden EvidenceWatch might reduce. Existing practice can handle this; the pilot must measure whether EvidenceWatch reduces reviewer burden without adding unacceptable misses or false alerts. Sources: https://doi.org/10.1186/s13643-023-02325-y, https://doi.org/10.1016/j.cmi.2020.06.013 and https://doi.org/10.1186/s13643-019-1248-5

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

The adapter is reference-manager-neutral: a pilot uses the team's existing library rather than requiring migration. Zotero is only the current tested CSL-JSON handoff. With Digital Science, ReadCube is an obvious stronger-owner test: if it already handles the residual at equal or lower burden, stop. There is **no live Zotero or ReadCube integration, access agreement or pilot partner**.

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
- **EPPI-Reviewer** already links Zotero libraries and uses OpenAlex-based auto-update suggestions for living reviews; **MAGICapp** already supports structured guideline updating with audit trails and current living-guideline surveillance; **ALEC/Monash** is developing an AI-supported Living Evidence Architecture. These are direct subsumption tests, not validation targets: https://eppi.ioe.ac.uk/cms/er4/help/openalex-in-eppi-reviewer/keeping-a-review-up-to-date-auto-update, https://www.magicevidence.org/magicapp/ and https://www.monash.edu/mada/research/project/living-evidence-architecture
- **Refract** owns reproducible source-change events; **AIEP P170** specifies evidence-dependency graphs and cascade impact analysis: https://github.com/refract-org/refract and https://aiep.dev/specs/p170_aiep_evidence_dependency_graph_protocol_os/
- Digital Science's **PostPub/VIRUS** track integrity events/downstream impact; **Perma.cc** preserves relied-on web states.

EvidenceWatch is not a new change detector or dependency-graph idea. Its surviving hypothesis is integration: can heterogeneous post-reliance source state, explicit authority, materiality filtering, a human-approved dependency map and review routing fit an existing workflow with low enough burden to be useful?

If a stronger workflow already does this, or the residual change class is too rare, stop or narrow.

## 7. WHERE THIS GOES

The next stage is a bounded workflow-integration pilot.

One living systematic review team would use its existing reference library. Because Cochrane and related workflows already own surveillance and important correction routes, the pilot would isolate residual changes and compare EvidenceWatch with existing practice on a pre-labelled set.

Primary outcome: **reviewer minutes per correctly handled material-change episode versus existing practice**.

Secondary outcomes:
- time to flag affected work;
- missed material changes and false alerts;
- setup and maintenance minutes;
- whether users can reconstruct why an alert happened without trusting the model.

Stop or narrow if maintenance exceeds saved review time, residual changes are too rare, existing practice performs as well, or misses are unacceptable.

If later commercialised, the plausible buyer is an institution or research team paying for monitored workspaces/integrations. Initial adoption is hypothesised around evidence-synthesis teams, health-evidence/guideline units and similar organisations maintaining updateable reviews. Pricing is untested.

## 8. FIT WITH DIGITAL SCIENCE

EvidenceWatch sits in evidence synthesis and research integrity. Its mechanisms are not novel; the fit is a multi-step agent that can stay quiet or refuse unauthorized state changes, with provenance and audit built in.

The missing capability is research-workflow ownership, not another model feature. Digital Science's ReadCube and prior integrity work make it a strong place to falsify the adapter against real practice. If the portfolio already solves the residual, stop; if not, measure whether the adapter lowers burden. No ReadCube access or partnership is claimed.

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
