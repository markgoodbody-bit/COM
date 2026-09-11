# PSFH Phase 0 — pre-execution feasibility pass

Status: **DESIGN BLOCKER FOUND / PRE-EXECUTION ONLY / NO SOURCE SELECTION / NO RECRUITMENT / NO ACCOUNT / NO SPEND / NO STUDY**  
Date: 11 September 2026, Europe/London

Basis:
- Phase-0 v3.2 merged in COM at `6a3827be53d7e454aae6279dcc8cbd3c174a4eec`;
- completed PSFH contact receipt merged previously;
- fresh public-source feasibility check on 11 September 2026.

Purpose: test whether the frozen-looking Phase-0 design can actually be translated into a low-burden, privacy-preserving execution packet **before** selecting any source account or creating any participant/provider state.

This note is not an execution packet and does not authorise one.

---

## 1. Result

**REPAIR_DESIGN_REQUIRED before execution.**

The v3.2 panel-eligibility rule contains one operational/privacy defect:

> within one assigned five-person panel, a recruit must answer no to whether they personally know or currently work directly with another named/pseudonymous panel member.

That condition is not meaningfully implementable through the plausible recruitment route without either:
- disclosing identities between participants;
- collecting direct identifiers from participants; or
- asking a formally satisfiable but substantively useless question about pseudonymous IDs that participants would not recognise.

A check that cannot actually reveal the relation it claims to exclude is worse than carrying the residual honestly.

`CHECK_EXISTS != CHECK_CAN_DETECT_THE_RELATION`

### Privacy basis

Prolific's current documentation says participant anonymity is a core requirement. Researchers normally know participants by pseudonymous Prolific IDs, and direct identifying information should not be collected without prior approval. The study does not need names, email addresses, phone numbers, social-media accounts or other direct identifiers.

Public references checked:
- https://researcher-help.prolific.com/en/articles/445117-can-i-ask-participants-for-their-personal-information-identifiers
- https://researcher-help.prolific.com/en/articles/445116-participants-personal-data
- https://researcher-help.prolific.com/en/articles/449610-participant-vetting-and-identifiers

Do **not** seek special PII permission merely to rescue this panel condition.

---

## 2. Proposed smallest design repair

Replace the direct-acquaintance eligibility condition with a narrower, observable condition:

- every panel place is occupied by a distinct pseudonymous participant identity under the chosen platform's normal participant-uniqueness controls;
- the research record retains only the participant identifier required for response/payment/audit linking plus already-permitted broad descriptors;
- do not attempt to identify or re-identify participants;
- do not collect names or other direct identifiers to establish social independence;
- if a participant voluntarily reports a concrete conflict/relationship that makes participation inappropriate before task exposure, handle it under the pre-frozen replacement rule; do not solicit identifying detail beyond what is necessary to act;
- **social acquaintance between panel members remains unmeasured residual dependence** and must travel with any result.

Required statement:

`DISTINCT_PSEUDONYMOUS_IDENTITIES != SOCIALLY_INDEPENDENT_PANEL`

This weakens the design's independence claim rather than creating a privacy burden to preserve it.

The existing `PANEL_N = 1` ceiling remains. No population-independence claim follows.

---

## 3. Recruitment route appears feasible, but is not selected or activated

A plausible later route is Prolific's general participant pool, using ordinary adult/location prescreening plus custom screening for project/protocol prior exposure if needed.

Current public capability evidence:
- Prolific supports standard participant recruitment and demographic prescreeners;
- custom screening is available for criteria not covered by built-in prescreeners;
- screened-out participants are paid under the custom-screening flow;
- saved participant groups can be used to reuse a fixed pseudonymous group across multiple studies if the task must be split into bounded sessions.

References:
- https://researcher-help.prolific.com/en/articles/445128-recruit-participants
- https://researcher-help.prolific.com/en/articles/445155-how-to-use-custom-screening-to-recruit-specific-participants
- https://researcher-help.prolific.com/en/articles/445158-how-to-create-and-manage-participant-groups

Feasibility does not establish that Prolific is the chosen provider. No account was opened or inspected, no participant count was queried, and no provider state was changed.

### Candidate recruitment scope for later attack

If Prolific survives review, a simple candidate would be:
- adults 18+;
- UK location, because the source candidate below concerns UK public-service decisions and this reduces avoidable contextual burden;
- ordinary general participant pool, not a representative-sample claim;
- custom exclusion of self-reported prior exposure to PSFH / TRACE / Mechanical Ethics / Campfire / this protocol;
- Stage A and Stage B use separate five-person participant groups;
- no participant enters both stages.

This is a candidate for review, not frozen recruitment criteria.

---

## 4. Payment feasibility — range only, no spend authority

Current Prolific documentation states:
- absolute minimum reward rate: £6/hour;
- recommended rate: at least £9/hour;
- pay-as-you-go platform fee commonly 42.8% of participant rewards for corporate customers and 33.3% for academic/non-profit customers;
- VAT may apply to the platform fee;
- screening may itself incur participant payments.

References:
- https://researcher-help.prolific.com/en/articles/445266-how-much-should-i-pay-participants
- https://researcher-help.prolific.com/en/articles/445239-what-is-your-pricing
- https://researcher-help.prolific.com/en/articles/445230-prolific-s-payment-model

Do not classify Mark into a fee category from guesswork. Use the actual account/workspace status only if provider execution is later authorised.

No total spend is frozen now because task duration is not yet honestly known. The later packet must derive a ceiling from non-participant dry timing plus a fixed contingency, and Mark must explicitly authorise the provider and amount before funds are added or reserved.

Illustrative arithmetic is allowed only as planning, not a budget commitment. For example, ten participant-hours at £9/hour would be £90 in participant rewards before platform fee, VAT if applicable, screening and replacement costs. Actual task time may differ materially.

`COST_FORMULA != SPEND_AUTHORITY`

---

## 5. Consent and data handling are executable in principle, but must be written before launch

Current Prolific guidance requires informed consent before collecting participant data and says the researcher acts as data controller for collected personal data. Prolific IDs are pseudonymous personal data and should be stored securely; direct identifiers should not be collected without need/approval.

References:
- https://researcher-help.prolific.com/en/articles/445265-getting-consent
- https://researcher-help.prolific.com/en/articles/445263-prolific-ids-data-collection-and-security
- https://researcher-help.prolific.com/en/articles/445116-participants-personal-data

A later execution packet therefore needs, before recruitment:
- plain-language consent;
- researcher/operator identity;
- exact data fields;
- reason for collection;
- retention/deletion period;
- access controls;
- withdrawal/noncompletion handling;
- no open publication of Prolific IDs.

No sensitive personal data is required by the construct.

---

## 6. Candidate public source universe: PHSO decisions portal

A plausible bounded source universe is the Parliamentary and Health Service Ombudsman's public decisions portal.

Why it is operationally attractive, without claiming substantive suitability:
- it publishes final decisions about NHS services in England and UK government/public bodies;
- casework decisions have been published online since April 2021;
- published decisions are anonymised;
- the portal exposes date/outcome/category search/filtering and stable public decision surfaces;
- both upheld and non-upheld decisions are published, avoiding a deliberately all-adverse source by design.

References:
- https://decisions.ombudsman.org.uk/
- https://decisions.ombudsman.org.uk/decisions
- https://www.ombudsman.org.uk/about-us/our-casework/phso-decisions-portal
- https://www.ombudsman.org.uk/privacy-policy

No individual decision was chosen or substantively read for this feasibility pass.

### Candidate Stage-A source-selection mechanics for later review

Do not execute this rule yet. It is offered for attack before freeze.

1. Freeze a portal snapshot/query boundary before retrieving candidate decision bodies.
2. Use a calendar-date window fixed in advance, outcome=`all`, no keyword or organisation filter.
3. Enumerate decision references/URLs from portal metadata only.
4. Mechanically exclude:
   - prior project/development examples;
   - any decision identifier/body substantively exposed during protocol development;
   - inaccessible/duplicate/non-English payloads under a predeclared rule.
5. If a reading-length bound is needed for participant burden, define it in advance and compute it mechanically from extracted text without judging substantive content.
6. Freeze a deterministic selection function before body inspection; one candidate is sorting eligible decision references by `SHA256(frozen_seed || decision_reference)` and taking the first required entries.
7. Pre-freeze the next-entry rule for availability failure. Never replace a selected account because it looks unhelpful for irreversibility.

A later packet must choose exact dates, any mechanical length bounds, the seed and extraction method before selection.

This proposal deliberately does **not** assert that PHSO is the best source or that complaints are representative of consequential decisions generally. If used, results inherit that source-domain ceiling.

`SOURCE_MECHANICS != DOMAIN_GENERALITY`

---

## 7. Dry timing remains a gate

The same humans work multiple source accounts within each stage, so burden can become large even with only five people per stage.

Before recruitment:
- use a non-study fixture excluded from Stage A/B to dry-run the instructions and response mechanics;
- combine that with the pre-frozen source-length bound to estimate per-account time;
- decide whether one sitting is proportionate or whether the stage must be split into bounded sessions using the same participant group;
- freeze maximum total participant time and dropout/replacement handling before launch.

Do not shorten or lengthen selected sources after seeing their substantive content merely to make the study fit a preferred budget.

---

## 8. Current disposition

**STOP before execution packet freeze.**

The provider route and source route appear operationally plausible, but v3.2's direct-acquaintance gate should be repaired first. After that repair survives source review, a later pre-execution packet can freeze:
- exact source snapshot/selection rule;
- task packet and dry timing;
- recruitment route and screening;
- consent/privacy/data custody;
- payment and total spend ceiling;
- screening/replacement ceilings;
- stage-stop conditions.

Nothing in this note authorises:
- editing participant/provider state;
- opening or funding a provider account;
- selecting or reading Stage-A source accounts;
- recruitment or screening;
- participant contact;
- payment;
- model inference;
- public study;
- Door/TRACE/ME claims.

`FEASIBLE_ROUTE != ROUTE_AUTHORISED`  
`PRIVACY_BURDEN_CAN_FALSIFY_A_DESIGN_DETAIL`  
`PREEXECUTION_FOUND_A_DEFECT -> REPAIR_BEFORE_ACTUATION`
