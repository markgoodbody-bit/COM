# Codex: frozen 16-record relation coding, first pass

Status: **PROVISIONAL CODING / NOT ADJUDICATED / NOT A POPULATION RESULT**

Date: 18 September 2026. Prepared in response to COM #364 comment 5727300183.
Method basis: `RELATION_CALIBRATION_PROTOCOL_20260918.md`, relation method and
hostile-review addendum; adjudication plan read before return. Branch base:
`e582b709e025f2907bb850cb2b3c681101504aef`.

## Evidence and independence limits

- Frozen run 35257984573 / artifact 10513278849; retained HTML, not live pages.
- All 16 selected HTML byte hashes matched the sample manifest in this pass.
- Sample digest reproduced as
  `c97ea5548ccc26b130a8ffe2783569d6d365897fcf0e04a35fba033486012b54`.
  Serialization is UTF-8 `URL<TAB>source_sha256`, joined by LF **without a final LF**.
  Adding a final LF gives a different digest; this is serialization, not a different sample.
- Source URLs and full hashes are in `relation_calibration_sample_20260918.json`.
  IDs below refer exclusively to that manifest. Headings/phrase locators refer to
  the HTML, not to current GOV.UK content or a linked complaints page.
- No live government refetch, linked-site reading, or external process knowledge
  was used for these labels. No later CC calibration return was read before freezing.
- This is separately produced coding, **not a blind or naive-reader experiment**.
  Codex previously reviewed some records, read FW's earlier dry-run summaries and
  helped criticize the method. Prior exposure cannot be undone by calling it independent.
- Sections covering process, human review, appeals, maintenance and risks were read;
  detailed descriptions and relevant technical/data sections were also inspected.
  Keyword-assisted discovery outside those sections is not proof of exhaustive route
  discovery. Truncated retrievals were not counted as complete reads. Route omissions
  remain challengeable, especially peripheral governance and data-access propositions.

## Table conventions

Each row is one provisional material proposition. Repeated descriptions of the
same mechanism are grouped; different initiators or action targets are separated.
The evidence column is a paraphrase plus exact section/phrase locator, not a claim
that the institution actually performs the action. `NOT STATED` is retained even
where a generic contact email appears elsewhere: contact details are not silently
borrowed as route instructions.

For readability, target/binding cells use the protocol's full labels. Actor,
action, channel/initiation, target, form, effect/status and evidence remain together.
Source statements of successful mitigation are not independently verified effects.
Routine testing is included where a review/correction action and object are stated;
bare performance numbers, general maintenance schedules and access permissions are
not automatically new routes. This inclusion boundary itself needs adjudication.

## V4-01 — FCDO: Correspondence Triage

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 01-A | Assigned Correspondence team member | Review and overwrite predicted case type/fields | Assigned-correspondence workflow; correction interface NOT STATED | TOOL_OUTPUT | INTERNAL_REVIEW | Can overwrite predictions | DIRECT; 3.2 Human review, predictions monitored and fields overwritten |
| 01-B | Project team | Monitor tool performance | Monitoring mechanism NOT STATED | OTHER_STATED_TARGET | INTERNAL_REVIEW | Performance monitoring; corrective consequence NOT STATED | DIRECT; 3.2, final sentence |
| 01-C | Individual receiving response | Review or appeal the response provided | NOT STATED | BROADER_OPERATIONAL_PROCESS | PROCESS_REFERENCE | Existing right said to be unaffected; exercise/result not shown | DIRECT; 3.5 Appeals and review, response provided |
| 01-D | NOT STATED as an initiator | No separate appeal mechanism supplied for triage; all emails reviewed | Not applicable to an initiation route | NO_RELEVANT_CHALLENGE_WITH_REASON | NO_SEPARATE | N/A justified by post-triage review, not absence of all remedies | DIRECT; 3.5, first two sentences |
| 01-E | CEOX receives automated alerts | Receive alert of RPA error | Weekly User Acceptance Testing alerts | OTHER_STATED_TARGET | INTERNAL_REVIEW | Automated detection/alert; investigation and repair NOT STATED | DIRECT; 4.1.4 Maintenance, alert CEOX if error found |
| 01-F | Human peer reviewers / user | Review information before response; manually review offensive-classified cases | Pre-response peer review / offensive classification trigger | TOOL_OUTPUT | INTERNAL_REVIEW | Review before submission; no automatic correction guarantee | EXPLICIT_CROSS_FIELD; 5.2 Risks and mitigations plus 3.2 identifies predicted correspondence fields |

RECORD_LEVEL_NOTES: 01-F could be split into peer review and moderation fallback;
I grouped them as checks in the same pre-response workflow but preserve both triggers.
01-D is a contextual N/A proposition, not a demonstrated legal exclusion. Nothing
links the general contact mailbox specifically to an appeal.

OUTSIDE_KNOWLEDGE_REQUIRED: no for these labels; yes to establish actual appeal procedure or efficacy, which is not attempted.

## V4-02 — Crown Prosecution Service: Correspondence Drafting Tool

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 02-A | Trained CPS authors, reviewers and approvers | Adjust draft; review and approve | Text editor and multi-layer workflow | TOOL_OUTPUT | INTERNAL_REVIEW | Human finalisation before correspondence sent; beta context | DIRECT; 2.1 Detailed description, 3.4 Human decisions and review |
| 02-B | NOT STATED | Give feedback / complain about issued CPS correspondence | Existing CPS policies/procedures, not described | BROADER_OPERATIONAL_PROCESS | PROCESS_REFERENCE; HELP_FEEDBACK | Existing procedures apply; outcome NOT STATED | DIRECT; 3.6 Appeals and review, correspondence issued by CPS |
| 02-C | NOT STATED | Decision-making appeal not presented as applicable to this tool | Not an initiation channel | NO_RELEVANT_CHALLENGE_WITH_REASON | NO_SEPARATE | Only rationale stated: not used for decision making | DIRECT; 3.6 first sentence; contextual negative, not literal prohibition |
| 02-D | Tool users / development evaluators | Give feedback on content and language during testing | Iterative user feedback; collection interface NOT STATED | TOOL_OUTPUT | HELP_FEEDBACK; INTERNAL_REVIEW | Model performance reportedly improved in development; no live remedy implied | DIRECT; 4.2.7 Model performance, qualitative feedback on content/language |
| 02-E | Management / auditors, individual role NOT STATED | Audit quality and compliance with processes | Regular audits and management checks | BROADER_OPERATIONAL_PROCESS | INTERNAL_REVIEW | Assurance stated; individual correction not stated | DIRECT; 5.2 Risks and mitigations, regular audits and management checks |
| 02-F | Users | Report feedback | Established feedback channel; mechanism NOT STATED | LAYER_NOT_STATED | HELP_FEEDBACK | Current maintenance context, specific object/effect NOT STATED | LAYER_NOT_STATED; 4.1.3 Maintenance, users can report feedback |

RECORD_LEVEL_NOTES: An issued letter is not automatically identical to its initial
AI draft. 02-B does not prove a route to change the tool's draft or the prosecution
decision. 02-C is weaker than an explicit statement that no appeal exists.

OUTSIDE_KNOWLEDGE_REQUIRED: no; CPS complaint eligibility/channel remains NOT STATED.

## V4-03 — DSIT: GOV.UK Chat

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 03-A | Tool user | Check answer against cited GOV.UK pages | Links supplied with answer | TOOL_OUTPUT | SELF_CORRECTION | Verification encouraged; cannot infer amendment of stored answer | DIRECT; 3.2 Human review and 3.4 Required training |
| 03-B | NOT STATED as initiator | No decision appeal described: guidance summaries only | Not an initiation channel | NO_RELEVANT_CHALLENGE_WITH_REASON | NO_SEPARATE | Record says no decisions made or assisted | DIRECT; 3.5 Appeals and review |
| 03-C | GOV.UK Chat team | Evaluate answers and probe safety failures | Structured manual evaluation, test sets and red teaming | TOOL_OUTPUT | INTERNAL_REVIEW | Development/assessment activity described, no individual correction commitment | DIRECT; 4.2.7 Model performance; 5.2 Risks and mitigations |

RECORD_LEVEL_NOTES: User verification is not an institutional correction request.
The negative in 03-B is a supplied rationale, not evidence that summaries cannot
influence decisions. Automated guardrails alone are not a human challenge route.

OUTSIDE_KNOWLEDGE_REQUIRED: no; no appeal channel is invented.

## V4-04 — NS&I: PolyAI

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 04-A | Service delivery partners | Audit chatbot responses, feed back and update training data | Conversation monitoring, sample audits, analytics dashboards | TOOL_OUTPUT | INTERNAL_REVIEW | Regular QA described; not a customer appeal | DIRECT; 3.2 Human review |
| 04-B | Customer dissatisfied with response / needing help | Request human assistance | Request human agent or other NS&I contact channels; exact alternative contact NOT STATED here | TOOL_OUTPUT | IN_CHANNEL_HANDOFF; HELP_FEEDBACK | Further help, not guaranteed reversal/correction | DIRECT; 3.5, unsatisfied with its response |
| 04-C | Customers | Pursue complaints / unresolved issues | Standard complaints process, Customer Care Team, possible Financial Ombudsman referral | BROADER_OPERATIONAL_PROCESS | PROCESS_REFERENCE | Escalation described; eligibility/outcome not verified | DIRECT; 3.5, complaints or unresolved issues and NS&I process |
| 04-D | Customers | Formal appeal not available for PolyAI answers as binding decisions | Not an initiation channel | NO_RELEVANT_CHALLENGE_WITH_REASON | NO_SEPARATE | Stated reason: provides information, not binding decisions | DIRECT; 3.5 first sentence |
| 04-E | System initiates; human agent receives | Escalate complex/sensitive or unsupported query | Topic/intent routing to human support | BROADER_OPERATIONAL_PROCESS | IN_CHANNEL_HANDOFF | Customer enquiry handled elsewhere; no objection required | DIRECT; 2.1 Detailed description and 3.1 Integration, query escalation |
| 04-F | NS&I / Atos staff | Review source information when terms change | Regular and ad-hoc documentation review | OTHER_STATED_TARGET | INTERNAL_REVIEW | Knowledge assets reviewed to address outdated information | DIRECT; 4.3.8 Data access and storage; 5.2 Risks and mitigations |

RECORD_LEVEL_NOTES: 04-B and 04-E have different initiation conditions. 04-C is
not recoded as appeal of the AI output merely because it follows 04-B in the field.
Unresolved complaints have a broad service target; no specific legal jurisdiction
or available remedy has been inferred.

OUTSIDE_KNOWLEDGE_REQUIRED: no; linked complaints details not inspected.

## V4-05 — Environment Agency: Regulatory Guidance Assistant

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 05-A | Permitting officer | Review RGA output every use | Officer workflow | TOOL_OUTPUT | INTERNAL_REVIEW | Mandatory in 3.2; conflicting scope statement in 5.2 retained | DIRECT; 3.2 Human review, every time; 5.2 Hallucinations or misattribution, no reviewer validation for high-impact outputs |
| 05-B | NOT STATED | Appeal permitting decision/process | Normal permitting appeals processes | BROADER_OPERATIONAL_PROCESS | PROCESS_REFERENCE | Reference only; actor, steps, remedy NOT STATED | DIRECT; 3.5 Appeals and review explicitly names permitting appeals; 3.1 corroborates permitting integration |
| 05-C | Data subject; eligibility details NOT STATED | Exercise data-subject rights | Established EA/Defra routes, specifics NOT STATED | OTHER_STATED_TARGET | DATA_RIGHTS; PROCESS_REFERENCE | Rights route mentioned in transcript privacy mitigation | DIRECT; 5.2, Privacy risk: inadvertent capture of personal data in transcripts |
| 05-D | Pilot users / governance reviewers; specific allocation NOT STATED | Give structured feedback, test and oversee review quality | FAT, weekly RAID/CIA sessions, Steering Committee | OTHER_STATED_TARGET | INTERNAL_REVIEW; HELP_FEEDBACK | Pilot assurance / review quality, not an affected-person appeal | DIRECT; 3.2, review quality assured through named mechanisms |
| 05-E | NOT STATED | Escalate concerns associated with over-automation | Described only as clear escalation routes | LAYER_NOT_STATED | PROCESS_REFERENCE; AMBIGUOUS | No actionable target/channel or effect stated | LAYER_NOT_STATED; 5.2, Over-automation or inadequate human oversight |
| 05-F | Operational governance; individual NOT STATED | Periodically check performance/accuracy after pilot | Formal schedule not yet defined | OTHER_STATED_TARGET | INTERNAL_REVIEW; PLANNED_NOT_OPERATING | Future governance commitment, not an operating route | DIRECT; 4.1.4 Maintenance, once pilot concludes |

RECORD_LEVEL_NOTES: 05-A's target is clear even though its coverage is contradictory.
I retain TOOL_OUTPUT and mark the conflict in status rather than erase a known
target with UNBOUND_OR_CONTRADICTORY. The codebook needs to specify which dimension
a contradiction invalidates. Also, its permitting example says cross-field even
though 3.5 itself names the target; I choose DIRECT and expose that disagreement.
Pilot wording varies between present and future; do not infer production operation.

OUTSIDE_KNOWLEDGE_REQUIRED: no for the retained labels; would be needed to complete 05-E, so it remains unspecified.

## V4-06 — MoJ: E-Supervision

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 06-A | Practitioners | Review all check-ins and assess identity | Normal workflow, independent of system output | BROADER_OPERATIONAL_PROCESS | INTERNAL_REVIEW | Practitioner retains check-in decision | DIRECT; 3.1 Integration and 3.2 Human review |
| 06-B | Practitioner | Review non-match and perform additional checks/follow-up | Mismatch notification | TOOL_OUTPUT | INTERNAL_REVIEW | Non-match does not itself prevent service use; extra scrutiny available | DIRECT; 3.2 and 3.5, not matching reviewed by practitioner |
| 06-C | NOT STATED as initiator | No formal appeal | Not an initiation channel | NO_RELEVANT_CHALLENGE_WITH_REASON | NO_SEPARATE | Tool not determining access is supplied reason | DIRECT; 3.5 first sentence |
| 06-D | Reporting actor NOT STATED; AWS named recipient | Recognition mistakes are not sent back to AWS | Explicitly no feedback route | OTHER_STATED_TARGET | NO_SEPARATE | Negative model/vendor-feedback proposition, not absence of practitioner review | DIRECT; 3.5 final sentence |
| 06-E | MoJ | Log and monitor service operational issues | Service-use issue logging | OTHER_STATED_TARGET | INTERNAL_REVIEW | Service monitoring, not retraining AWS models | DIRECT; 4.1.4 Maintenance |

RECORD_LEVEL_NOTES: 06-A/B may be nested rather than independent routes. Keep their
different triggers and objects visible during matching. The existing NO_SEPARATE
label fits 06-D imperfectly because it is not an appeal negative; no replacement
label has been introduced.

OUTSIDE_KNOWLEDGE_REQUIRED: no; no inference about probation sanctions or remedies.

## V4-07 — Welsh Government: Ancient Woodland segmentation

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 07-A | Internal testers | Review outputs before release | Pre-publication review, interface NOT STATED | TOOL_OUTPUT | INTERNAL_REVIEW | Output review described | DIRECT; 3.2 Human review |
| 07-B | Any dataset user | Download polygons and inspect | Standard geospatial software | TOOL_OUTPUT | SELF_CORRECTION | User inspection possible; no publisher correction power implied | DIRECT; 3.2 |
| 07-C | External users / others | Provide feedback to improve future model versions | Feedback submission channel NOT STATED | OTHER_STATED_TARGET | HELP_FEEDBACK | Future model improvement; not current-output reversal | DIRECT; 3.2 final clause |
| 07-D | Expert geographers | Inspect predictions and flag repeated mispredictions | QGIS manual inspection | TOOL_OUTPUT | INTERNAL_REVIEW | Flags patterns to inform development | DIRECT; 4.1.4 Maintenance, Manual Inspection |
| 07-E | Expert geographers | Suggest ground-truth label improvements | QGIS inspection | OTHER_STATED_TARGET | INTERNAL_REVIEW; HELP_FEEDBACK | Training data improvement | DIRECT; same maintenance paragraph, suggested improvements to ground truth labels |

RECORD_LEVEL_NOTES: Appeals field 3.5 is bare N/A. It is recorded here as an
unexplained negative token, NOT NO_RELEVANT_CHALLENGE_WITH_REASON. I do not create a
route row from bare N/A or infer its reason from unrelated context. Nor does N/A
erase the review/feedback propositions in 3.2 and maintenance.

OUTSIDE_KNOWLEDGE_REQUIRED: no for routes; explanation of N/A cannot be completed from the field and is left open.

## V4-08 — TrustID

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 08-A | TrustID Document Analyst team | Manually reassess failed / low-confidence face match | Automatic escalation below threshold | TOOL_OUTPUT | INTERNAL_REVIEW | Human reassessment, not candidate-initiated appeal | DIRECT; 2.1 Detailed description, 3.2 and 3.5 |
| 08-B | Users who believe tool failed | Submit review request to HOS | HOS named recipient; submission medium NOT STATED | TOOL_OUTPUT | PUBLIC_INITIATION | Review can be requested; result/deadline NOT STATED | DIRECT; 3.5 final sentence |
| 08-C | Data subject / candidate | Choose or request manual checking instead | Request mechanism NOT STATED | BROADER_OPERATIONAL_PROCESS | REFUSAL_OR_OPT_OUT | Alternative right-to-work checking; timing risk acknowledged | EXPLICIT_CROSS_FIELD; 2.2 Benefits option for manual service; 2.1 right-to-work purpose; 5.2 manual process can be requested |
| 08-D | Data subject | Request verification report through right of access | Art 15 request; submission channel NOT STATED | OTHER_STATED_TARGET | DATA_RIGHTS | Report could be shared; no correction or outcome reversal stated | DIRECT; 4.4.5 Data sharing agreements, data subject request |

RECORD_LEVEL_NOTES: 08-C is not a reversal of a match score. 08-D's object is access
to a report, not necessarily changing it. The general portal used to submit identity
documents is not assumed to be the channel for 08-B/C/D.

OUTSIDE_KNOWLEDGE_REQUIRED: no; legal sufficiency of the stated routes not assessed.

## V3-01 — MoJ: Data First (Splink)

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 31-A | Internal reviewers; individual NOT STATED | Review sampled records/person clusters before release | Release-cycle manual review | TOOL_OUTPUT | INTERNAL_REVIEW | Check linkage models performed as expected | DIRECT; 3.4 Human decisions and review |
| 31-B | Researchers | Report error or anomaly | Feedback channel NOT STATED | TOOL_OUTPUT | HELP_FEEDBACK | Said to be addressed in next model iteration, not immediate correction | EXPLICIT_CROSS_FIELD; 3.6 link/error/anomaly discussion and 3.2 linked-dataset output |
| 31-C | Data First staff, data-owner representatives and review panels | Scrutinise research proposals and resulting outputs | Proposal and output review | BROADER_OPERATIONAL_PROCESS | INTERNAL_REVIEW | Feasibility, ethics, scope and misuse checks | DIRECT; 5.1 Impact assessment |
| 31-D | Research-service monitoring actors NOT STATED | Monitor activity and revoke access for non-permitted uses | ONS Secure Research Service monitoring | BROADER_OPERATIONAL_PROCESS | INTERNAL_REVIEW | Access revocation stated; not an appeal route | DIRECT; 5.2 Risks and mitigations, Misuse of Data |

RECORD_LEVEL_NOTES: Researchers are explicitly not expected to verify individual
links from identifying information; 31-B is nevertheless allowed. Choosing a
confidence-threshold dataset is a research choice, not itself a correction request.
31-C/D test whether the broad protocol includes research-governance reviews outside
the tool-output challenge question; preserve as peripheral, not as positive appeal findings.

OUTSIDE_KNOWLEDGE_REQUIRED: no; linked privacy/research-service guidance not opened.

## V3-02 — NHSBSA: Residency Checker

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 32-A | Applicant failing automated check | Supply documentary residency evidence | Automated email with acceptable-document list and upload link to application record | BROADER_OPERATIONAL_PROCESS | PUBLIC_INITIATION; PROCESS_REFERENCE | Acceptable evidence leads to entitlement; original score revision NOT STATED | DIRECT; 2.1 Detailed description, 3.4 Human decisions and review, 3.6 Appeals and review |
| 32-B | Customer unable/unwilling to use document procedure | Enter complaints process | Linked Overseas Healthcare Services complaint policy; linked page not read | BROADER_OPERATIONAL_PROCESS | PUBLIC_INITIATION; PROCESS_REFERENCE | No entitlement if residency cannot be proved / cooperation refused | DIRECT; 3.6 |
| 32-C | Operational user following some complaints | Perform manual residency check and decide application progression | Third-party portal; occasional complaint trigger | BROADER_OPERATIONAL_PROCESS | INTERNAL_REVIEW | Pass progresses application; fail returns to document procedure | DIRECT; 3.4; 2.2 Scope explicitly says end decision by human |
| 32-D | Customer wishing to query failed check | Ask third-party provider why it failed | Direct provider contact; details NOT STATED | TOOL_OUTPUT | EXPLANATION_ONLY | Information request; NHSBSA does not seek explanation on customer's behalf | DIRECT; 3.2 Provided information |
| 32-E | Manual-review actor NOT STATED; supplier involved where appropriate | Investigate decision matrix if acceptance rate below 85% | Aggregate-rate trigger | OTHER_STATED_TARGET | INTERNAL_REVIEW | Distinguish system error from genuine rejections | DIRECT; 4.2.7 Model performance |
| 32-F | Testing/monitoring actor NOT STATED; supplier receives report | Report response-time outliers and UAT discrepancies | Supplier reporting; channel NOT STATED | OTHER_STATED_TARGET | INTERNAL_REVIEW; HELP_FEEDBACK | Service/test discrepancy reporting, not applicant reconsideration | DIRECT; 4.2.7 Model performance |

RECORD_LEVEL_NOTES: This is a deliberate challenge to the method's earlier example
that failing a check then supplying documents necessarily targets TOOL_OUTPUT.
The output triggers the route; the stated thing it changes is application/entitlement.
No text says the original automated result is overwritten. 32-C likewise produces
a fresh manual decision, not necessarily correction of the old output. These labels
are provisional target interpretations, not claims that no output-targeted route exists.
The 85% number is copied as a published trigger, not independently verified performance.

OUTSIDE_KNOWLEDGE_REQUIRED: no; whether underlying provider data/score is corrected is not supplied and not inferred.

## V3-03 — DSIT: GOV.UK site search

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 33-A | Search user | Refine query or decline results | Search interface | TOOL_OUTPUT | SELF_CORRECTION | Different retrieval attempt / user judgement, not a publisher remedy | DIRECT; 3.4 Human decisions and review |
| 33-B | Users | Give feedback on site-search page | Feedback form at page bottom | OTHER_STATED_TARGET | HELP_FEEDBACK | Page feedback; response/correction NOT STATED | DIRECT; 3.6 Appeals and review |
| 33-C | GOV.UK team | Give Google feedback on VAIS product | Regular interactions; exact interface NOT STATED | OTHER_STATED_TARGET | HELP_FEEDBACK | Supplier product feedback; no individual review commitment | DIRECT; 3.6 second sentence |
| 33-D | GOV.UK / Google | Detect result-quality degradation and remediate cause | Continuous monitoring, judgement lists, behaviour metrics and supplier work | TOOL_OUTPUT | INTERNAL_REVIEW | Internal handling or supplier feedback; intended relevance repair | DIRECT; 4.1.3 Maintenance; 5.2 Risks and mitigations |

RECORD_LEVEL_NOTES: The site-search page is explicitly named, so 33-B is not
LAYER_NOT_STATED merely because its effect is unspecified. Feedback on the page
does not establish a right to change rankings.

OUTSIDE_KNOWLEDGE_REQUIRED: no; no linked form submission or provider inspection.

## V3-04 — DfE: Apprenticeship Withdrawal Rate AI

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 34-A | NOT STATED as initiator | No appeal/review required, according to publisher | Not an initiation channel | NO_RELEVANT_CHALLENGE_WITH_REASON | NO_SEPARATE | Reason: personalised content generally available regardless of prediction | DIRECT; 3.6 Appeals and review |
| 34-B | Future model/data operators, exact role NOT STATED | Review input data/features and decide updates | Planned data-quality dashboards | OTHER_STATED_TARGET | INTERNAL_REVIEW; PLANNED_NOT_OPERATING | Production plan, not current review route | DIRECT; 3.4 Human decisions and review, input features |
| 34-C | Future model/data operators, exact role NOT STATED | Review accuracy/precision/recall across new training | Planned metrics dashboards and retained model iterations | OTHER_STATED_TARGET | INTERNAL_REVIEW; PLANNED_NOT_OPERATING | Model calibration/maintenance plan | DIRECT; 3.4 and 4.1.3 Maintenance |

RECORD_LEVEL_NOTES: Development/POC is explicit. Neither planned review becomes a
live apprentice appeal. Risk language about harmful third-party reuse is not an
actual route for an apprentice to challenge a classification.

OUTSIDE_KNOWLEDGE_REQUIRED: no; deployment and actual effects not inferred.

## V3-05 — HMRC: Logo Detection and Classification Toolkit

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 35-A | Data analyst | Flag poor results/model faults to developer/data-science team | Internal report; medium NOT STATED | OTHER_STATED_TARGET | INTERNAL_REVIEW | Model/programme review and possible retraining, not per-URL appeal | DIRECT; 3.4 and 3.6, faults/errors and model performed poorly |
| 35-B | Analyst | Inspect each generated URL and validate risk; allow-list legitimate URL | Manual review of generated list | TOOL_OUTPUT | INTERNAL_REVIEW | Avoid repeated checking of legitimate URLs; human action before takedown | DIRECT; 5.2 Risks and mitigations |
| 35-C | Organisations | Appeal URL-takedown action | HMRC Cybersecurity legal processes; filing channel NOT STATED | BROADER_OPERATIONAL_PROCESS | PROCESS_REFERENCE | Appeal availability stated, result NOT STATED | DIRECT; 3.6 second sentence |
| 35-D | Public | Report phishing sites, emails or calls separately | HMRC website, linked from record | BROADER_OPERATIONAL_PROCESS | PUBLIC_INITIATION; HELP_FEEDBACK | Parallel reporting so HMRC need not rely on tool alone | DIRECT; 5.2 last sentence |

RECORD_LEVEL_NOTES: 35-D concerns threat reports, not challenging a classification
about the reporter. It tests the broad inclusion rule and must not be counted as a
decision-subject remedy. 35-A targets model/programme behaviour; output examples
are its trigger/evidence, not necessarily the thing changed.

OUTSIDE_KNOWLEDGE_REQUIRED: no; legal appeal procedure not supplemented from outside.

## V3-06 — HMT: HERMeS

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 36-A | HMT staff user | Verify generated answer, ask clarification or search again | Source-document links and chatbot interface | TOOL_OUTPUT | SELF_CORRECTION | User verification and refined answer, not guaranteed corrected information | DIRECT; 3.4 Human decisions and review |
| 36-B | HMT users | Give general feedback | Form linked within tool | LAYER_NOT_STATED | HELP_FEEDBACK | Target/effect of general feedback not specified | LAYER_NOT_STATED; 3.6 Appeals and review, general feedback |
| 36-C | Tool users | Report bugs for maintenance | Linked form or email; exact address NOT STATED here | OTHER_STATED_TARGET | HELP_FEEDBACK | Ad-hoc maintenance on reported bugs | DIRECT; 4.1.3 Maintenance; 3.6 report issues corroborates |
| 36-D | Evaluation actors NOT STATED / development focus groups | Assess output relevance and adjust prompt/retrieval/search | Evaluations and development focus groups | TOOL_OUTPUT | INTERNAL_REVIEW; HELP_FEEDBACK | Adjustments reportedly made from some evaluations | DIRECT; 5.1 Impact assessment |
| 36-E | Tool management team | Review usage and development requirements | Weekly review | OTHER_STATED_TARGET | INTERNAL_REVIEW | Development planning; individual correction NOT STATED | DIRECT; 4.1.3 |

RECORD_LEVEL_NOTES: The same form can carry generic feedback and an explicit bug
report without the first borrowing the second's target/effect. 36-D also names
model/configuration changes as effects; a coder choosing OTHER_STATED_TARGET may
be coding intervention rather than evaluated object. Preserve that distinction.

OUTSIDE_KNOWLEDGE_REQUIRED: no; general feedback target remains unstated.

## V3-07 — Standards and Testing Agency: Reception Baseline Assessment Routing

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 37-A | QA actors NOT STATED | Check routing implementation, test scenarios and alert unexpected operation | Functional trials, scripted inputs and planned live automatic alerts | TOOL_OUTPUT | INTERNAL_REVIEW | QA described; live alerts future-tense; repair response NOT STATED | DIRECT; 3.4 Human decisions and review; 5.2 Risks and mitigations |
| 37-B | Parents / teachers as discussed by publisher | Publisher says appeal should not be needed | Not an initiation channel | NO_RELEVANT_CHALLENGE_WITH_REASON | NO_SEPARATE | Reason offered: no individual judgement/consequence; expectation, not a ban | DIRECT; 3.6 Appeals and review, first part |
| 37-C | Parents | Request child's narrative statement | Request from school; medium NOT STATED | OTHER_STATED_TARGET | PUBLIC_INITIATION; EXPLANATION_ONLY | Access to statement, not numerical score or correction | DIRECT; 3.6, parents can request to receive this |
| 37-D | Parents with broader issue | Speak to school first | School contact; medium NOT STATED | LAYER_NOT_STATED | HELP_FEEDBACK; PROCESS_REFERENCE | Initial contact only; issue/alterable target unspecified | LAYER_NOT_STATED; 3.6 last sentence |
| 37-E | Standards and Testing Agency | Review annual numbers subject to routing | Annual cycle | OTHER_STATED_TARGET | INTERNAL_REVIEW | No intended periodic rule reassessment while assessment format stays same | DIRECT; 4.1.3 Maintenance |

RECORD_LEVEL_NOTES: Narrative statements are downstream from routing, but the
generic broader issue in 37-D does not explicitly identify narrative correction
or routing reconsideration. Do not make school contact into a specified appeal.
37-A contains assurance of both rules and their execution; granular separation is
an admissible discovery disagreement. Automatic alerts are not human actuation.

OUTSIDE_KNOWLEDGE_REQUIRED: no for retained labels; yes to name the target/effect of 37-D more specifically, so left unstated.

## V3-08 — BDUK: Project Gigabit Voucher Eligibility Engine

| Route | Actor | Action | Channel / initiation | Target site | Route form | Status / effect stated | Binding / evidence locator |
|---|---|---|---|---|---|---|---|
| 38-A | Telecommunications organisations | Challenge eligibility of a premise | Mechanism said to exist; channel NOT STATED | TOOL_OUTPUT | PUBLIC_INITIATION | Challenge availability stated; correction/remedy NOT STATED | EXPLICIT_CROSS_FIELD; 3.6 eligibility challenge; 3.2 output eligibility true/false; 3.1 separates it from later checks |
| 38-B | BDUK voucher operations team | Review commercial viability/projects and subsequent voucher conditions | Subsequent voucher-process reviews | BROADER_OPERATIONAL_PROCESS | INTERNAL_REVIEW | Eligibility does not guarantee voucher; no review of ineligible premises asserted | DIRECT; 3.4 Human decisions and review |
| 38-C | BDUK team | Monitor/manage voucher scheme as mitigation for poor criteria/data | Scheme monitoring; mechanism NOT STATED | BROADER_OPERATIONAL_PROCESS | INTERNAL_REVIEW | Mitigation assertion, no particular score-correction procedure supplied | DIRECT; 5.2 Risks and mitigations |

RECORD_LEVEL_NOTES: 38-A is my strongest explicit cross-field binding: identical
premise-eligibility referent, explicitly distinguished from later project checks.
It does not establish resident initiation or a channel. 38-B cannot be borrowed as
an appeal for premises that failed the gateway check.

OUTSIDE_KNOWLEDGE_REQUIRED: no; challenge procedure is not completed from the linked subsidy guidance.

## CODEBOOK_DEFECTS / bounded repair proposals

These are separate from the frozen assignments above. Do not silently recode them.

1. **Trigger versus object reviewed versus thing changed.** Before: a target-site
   label can attach to whichever of those a coder has in mind. After (proposal):
   record in plain English which object the route reviews, and separately what
   change is actually stated; do not infer correction of the triggering output.
   NHSBSA 32-A/C, HMRC 35-A and HERMeS 36-D expose this. It may change earlier
   TOOL_OUTPUT labels for documentary-evidence routes; it does not require a new
   target category or prove an output is unchallengeable.
2. **DIRECT precedence is inconsistent in the worked example.** A named permitting
   appeal can be DIRECT under the definition but cross-field in the method's
   example. Prefer DIRECT when the same proposition names the target; cite other
   fields as corroboration. Use cross-field only when needed for assignment to the
   tool/process layer (BDUK). This would change binding labels, not the route.
3. **Contradiction is not always in the target.** EA 05-A has a clear output target
   and incompatible review-scope statements. Preserve contradiction in status and
   evidence rather than replacing a known target. The closed target vocabulary
   currently encourages losing this distinction.
4. **Unknown categories overlap.** An unstated target also requires adding a link
   to assign one. Precedence proposal: LAYER_NOT_STATED for absent specification;
   UNBOUND_OR_CONTRADICTORY for an attempted explicit join that fails or conflicts.
   Generic HERMeS feedback, EA escalation and school contact expose the boundary.
5. **Negative status is mixed into target vocabulary.** NO_RELEVANT_CHALLENGE_WITH_REASON
   does not identify what has no challenge. Preserve named object and reason in
   prose and separate other positive routes. Bare N/A is not this category. MoJ's
   explicit no-appeal is stronger than CPS/Chat's no-decision rationale; the table
   preserves wording strength rather than declaring them equivalent.
6. **Material-route inclusion and splitting need a stopping rule.** Model QA,
   data-access rights, governance audit, bug report and public threat report all
   fit some existing labels, but are not all remedies for affected people. Examples:
   Splink 31-C/D, HMRC 35-D, TrustID 08-D and FCDO 01-E. Adjudicate inclusion before
   producing any count. Prefer a narrower published question if peripheral rows
   dominate; do not invent target categories to preserve every monitoring activity.

## SYSTEMATIC_FAILURES / limitations

- Case-local targets often remain legible while channel, effect or implementation
  status does not. No single successful-target fraction represents answerability.
- Review of output is not public initiation; initiation is not access in practice.
- Development and production statements can coexist. Future commitments must not
  become current routes merely because the rest of a record uses present tense.
- Separating route discovery from label agreement is essential: the method leaves
  discretionary splitting of nested review processes and peripheral QA.
- No independent agreement, general reliability or route efficacy has been shown
  by this first pass. No comparison to CC's later table has yet been performed.
- No population estimates or version effects are calculated. This selected pressure
  sample and a previously exposed coder cannot support those claims.

## DISPOSITION

**REPAIR, with a possible SHRINK of the inclusion rule.**

The 16 records support source-bound propositions without external process research.
That is a useful first-pass object, not proof that the coding is reproducible. The
load-bearing defect is what a target refers to when an output triggers a route but
the published action changes a broader decision. Preserve these first reads; align
propositions with CC before changing definitions. If consistent targets require an
invented process model, shrink to explicit relations rather than complete the gaps.

No production code, source corpus, reader-use answer key, public record, TRACE/ME
baseline, study gate, or external institutional contact is changed by this file.
