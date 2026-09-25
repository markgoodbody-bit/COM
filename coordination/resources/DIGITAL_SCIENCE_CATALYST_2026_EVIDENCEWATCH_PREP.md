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

The initial user is a living systematic review team. Its decision is whether an existing conclusion must be reopened when evidence already included changes: a publisher correction, dataset revision, owner update, replaced authority page, or apparently new source that repeats the same evidentiary root.

Formal retraction warnings are not the gap I am claiming. Zotero already integrates Retraction Watch and can warn when a cited item is retracted, including citations already present in a document when they are refreshed. Crossmark exposes formal scholarly corrections, retractions and updates.

The residual problem is what happens **after reliance** when the change is broader than formal retraction status: did the evidence state behind a bounded claim materially change, and does the living review now need reopening?

Change itself is common, but materiality is the unmeasured crux. A 2016 PLOS ONE study found textual content had drifted for over 75% of the web references for which archived and live versions could be compared. Separately, a 2022 biomedical study found only about 5% of systematic reviews/guidelines corrected or retracted their results after trials they had included were later retracted. Neither establishes a universal rate of material change. Sources: https://doi.org/10.1371/journal.pone.0167475 and https://pubmed.ncbi.nlm.nih.gov/35779825/

Whether EvidenceWatch catches consequential changes accurately enough to save review time remains a pilot question.

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

The current prototype is standalone Node.js. A new reversible adapter now accepts standard CSL-JSON reference-manager exports and turns them into EvidenceWatch watch configurations. CSL JSON is an import/export format supported by Zotero. Imported references default to candidate/non-authoritative sources; authority and independence must be assigned explicitly.

This is currently a **file handoff, not a live Zotero or ReadCube integration**. A funded pilot would automate the handoff through the supported integration surface of the reference-manager or shared evidence-library workflow chosen with a pilot user.

## 3. TRUST, AUDIT AND GOVERNANCE

Trust is carried by inspectable state rather than a model verdict.

EvidenceWatch rebuilds canonical state from an append-only ledger after restart. Observation fingerprints suppress duplicate model work without deleting history. Authority is explicit configuration, separate from evidentiary role. Discovered sources are quarantined as candidates rather than recursively gaining authority.

A concrete refuse/flag behaviour is tested: a derivative source repeating the owner stays quiet; if it diverges, EvidenceWatch flags review but refuses to overwrite canonical state. Discovered candidates likewise cannot establish or advance state until explicit promotion. If an authority source becomes unreachable, the last known state is preserved rather than converted into "false".

The user remains accountable. EvidenceWatch never rewrites a brief or declares truth. Tested disagreement, source-loss and candidate-discovery cases preserve state or route review without canonical overwrite; model errors can still go undetected.

The current suite has 47 deterministic tests, including correction, duplicate suppression, derivative disagreement, authority boundaries, restart reconstruction, outage/recovery, candidate quarantine, browser-demo behaviour and the CSL-JSON handoff.

## 4. TEAM

I am Mark Goodbody, a UK Senior IT and Telecoms Engineer with more than 25 years of professional experience across infrastructure, networking, support, troubleshooting and small-team leadership.

I built EvidenceWatch from independent work on provenance, correction and human/AI answerability. I remain the human release and accountability gate. Multiple AI systems are used for implementation and adversarial review; model agreement is not treated as validation.

## 5. WHERE YOU ARE TODAY

EvidenceWatch is a working prototype, not a validated research product.

The deterministic browser demo shows an owner claim moving from a baseline of three incidents, through derivative repetition that does not change canonical state, to an owner correction from three to four that creates one downstream-review alert while preserving the earlier state.

A one-watch/two-run live witness used NVIDIA Nemotron against real public owner pages; the second same-ledger run deduplicated unchanged observations. One model-status field was internally inconsistent and remains unresolved rather than being treated as validation.

Demo:
https://youtu.be/0hdwNc_t4pM

There are no claimed research customers or validated user-efficiency results. The CSL-JSON handoff, DOI-boundary repair and controlled restart/correction witness are now merged on EvidenceWatch main (`b4c8f2bbbca1ae6ad1a5caa16a95cc76ce1b1f1f`) with post-merge CI green. In the synthetic-content / real-format CSL witness, three references imported, one unfetchable reference was skipped, state survived an engine restart, and a controlled publisher correction changed the bounded result from 1.8 to 1.2 while routing the dependent brief for review. This is an engineering witness, not researcher validation.

Related public provenance work:
https://github.com/markgoodbody-bit/human-record
https://pleasestartfromhere.com/

## 6. ALTERNATIVES AND COMPETITORS

Strong existing owners already cover large parts of this problem:

- **Zotero + Retraction Watch** warns about retracted library items and citations later retracted: https://www.zotero.org/blog/retracted-item-notifications/
- **Crossmark / Crossref** exposes formal corrections, retractions and publisher-registered updates: https://www.crossref.org/services/crossmark/
- **ReadCube** owns reference management, literature monitoring, shared libraries and systematic-review workflows: https://about.readcube.com/
- Digital Science's own Catalyst portfolio includes **PostPub**, which tracks retractions/integrity actions, and **VIRUS**, which tracks questionable papers and their downstream scholarly/policy impact. These are close precedents, not gaps I should relabel as mine.
- **Perma.cc** owns preservation of the cited web state—the complementary strategy of freezing the 'before' rather than monitoring the live source: https://perma.cc/

The surviving hypothesis is narrower: **post-reliance claim-level state across heterogeneous sources + ancestry/independence + explicit state authority + material-change filtering + a map to downstream work that may need reopening**.

If another product already provides that full loop better, EvidenceWatch should be killed or narrowed.

## 7. WHERE THIS GOES

The next stage is a bounded research-workflow pilot.

The first pilot would involve one living systematic review team, using its existing reference library. Cochrane's living-review model already performs continual surveillance for new evidence; this pilot tests the adjacent burden of changes to evidence already included. It would compare EvidenceWatch with existing practice on a pre-labelled set of material/non-material changes, measuring:
- time to flag affected work;
- missed material changes and false alerts;
- reviewer minutes, duplicate suppression, and setup/maintenance time;
- whether users can reconstruct why an alert happened without trusting the model.

Stop or narrow if maintenance exceeds saved review time, material changes are too rare, or missed-change rate is unacceptable.

If later commercialised, the plausible buyer is an institution or research team paying for monitored workspaces/integrations. A workspace or monitored-collection subscription is a hypothesis only; pricing has not been tested.

## 8. FIT WITH DIGITAL SCIENCE

EvidenceWatch sits in evidence synthesis and research integrity.

The fit is not simply "AI with provenance". It is a multi-step agent that must know when to stay quiet, when to flag a change, and when it lacks authority to act. That is directly aligned with Digital Science's 2026 emphasis on agents embedded in researcher workflows with provenance, governance and accountability.

Digital Science also owns products close to the natural integration surface. ReadCube already handles literature monitoring, shared libraries, citation/document synchronisation and systematic-review workflows. That makes Digital Science a particularly useful place to test the narrower question: is there value in monitoring **changes to evidence already relied on**, then routing only material changes to the downstream work they affect? I would value help testing that residue with researchers before hardening the wrong product.

## 9. BUDGET

Up to £25,000 would be staged.

- **Stage 1 — £5,000 cap:** workflow integration and testing whether the review's own outcome→study structure can propose dependency mappings for human batch approval; matched-baseline fixtures and setup/maintenance measurement. Stop if burden or problem incidence makes the workflow implausible.
- **Stage 2 — £14,000 cap:** only if Stage 1 survives; pilot engineering plus researcher observation/evaluation, including predeclared materiality labels and missed-change measurement.
- **Stage 3 — £6,000 cap:** model/API/infrastructure, independent security/provenance review and reproducibility documentation as required.

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
