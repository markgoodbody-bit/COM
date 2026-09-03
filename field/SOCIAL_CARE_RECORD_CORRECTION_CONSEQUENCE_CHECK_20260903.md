# Social-care record correction — consequence check

Status: **FIELD / OWNER-NATIVE / NON-CANONICAL / NOT POLICY**  
Related case: COM #99.

## Use only when

A **material factual error in an official social-care record is discovered after the inaccurate version may already have informed an assessment, plan, risk judgement or action**.

Do not use this for a draft corrected before it enters the system of record, a harmless typo, a dispute where falsity has not been established, or a disagreement with a supportable professional opinion.

This problem predates AI. Human entry, transcription, imported data and AI-assisted recording are possible sources of error; none creates a distinct correction duty here.

## Existing owner protections

Start with them; do not replace them.

- **Social Work England:** accurate/up-to-date records, documented decision reasoning and professional accountability.
- **UK GDPR / ICO:** rectify inaccurate personal data and notify recipients where required, subject to the owner's proportionality limits.
- **ATRS / UK Data & AI Ethics guidance:** document how algorithmic output relates to decisions; provide review/redress and auditability where those systems are used.
- **NHS health-and-care records guidance:** when inaccurate information is corrected, consider who viewed it and may have relied on it for care/treatment decisions.

This prompt joins existing owner duties. It does not establish a new duty or a sector-wide implementation gap.

## The one owner action

> **After correcting a material factual error, record whether any still-consequential assessment, plan, risk judgement or action used it. If so, send only those items to the accountable professional owner for a recorded decision on whether reconsideration is needed. If use cannot be established proportionately, record that limit and stop.**

## Bounded use

1. **Correct or formally dispute the authoritative record** using the existing record-integrity process. Preserve the audit/history required by that system.
2. **Notify external recipients** through the existing data-protection or information-governance route where required.
3. **Look only for still-consequential internal reliance points** where the earlier version could plausibly have changed an assessment, plan, risk judgement, placement/service decision, referral, closure or other consequential act.
4. **Route an identified material reliance point to its existing human/professional owner.** This check cannot adjudicate truth, overturn professional judgement or reverse a decision.
5. Record one bounded disposition for the attempted check:
   - `NO_MATERIAL_RELIANCE_FOUND` — the proportionate review found no still-consequential reliance point;
   - `OWNER_LEFT_UNCHANGED_WITH_REASONS` — a reliance point was reviewed and the prior act stands;
   - `OWNER_REVISED_OR_REOPENED`;
   - `REMEDY_ROUTE_OPENED`;
   - `REVIEWED_MATERIALITY_INDETERMINATE` — reliance points were identified, but their materiality remains genuinely unresolved;
   - `RELIANCE_NOT_IDENTIFIABLE_FROM_AVAILABLE_RECORDS` — available records cannot establish the reliance relation proportionately.

The last two outcomes are not interchangeable. A record-access log is not proof of reliance, and a route that does not expose reliance is not proof that no reliance exists.

Do not reconstruct every read of the record, require retention of material that should lawfully have been deleted, or replay every historical decision. Proportionality is part of the check. Repeated `RELIANCE_NOT_IDENTIFIABLE_FROM_AVAILABLE_RECORDS` is a limitation of the deployment, not evidence that every case needs new infrastructure.

```text
HUMAN_REVIEW_OCCURRED != ERROR_IMPOSSIBLE
RECORD_RECTIFIED != PRIOR_DECISION_RECONSIDERED
RECIPIENT_NOTIFIED != INTERNAL_RELIANCE_REVIEWED
NO_MATERIAL_RELIANCE_FOUND != RELIANCE_NOT_IDENTIFIABLE
RECORD_ACCESSED != RECORD_RELIED_UPON
CORRECTED_RECORD != RESTORED_RESULT
TRACEABLE_CONSEQUENCE != AUTOMATIC_REVERSAL
```

## Why this is grounded

**Current AI use:** Newcastle's public Magic Notes ATRS says practitioners review/edit AI drafts before official entry and that the resulting official notes inform care planning, assessments and follow-up actions. Its public `appeals and review` entry describes opting out of Magic Notes use; it does not establish a post-entry correction/reliance process. That is a transparency limit, not proof that Newcastle lacks one.

**Real children's-social-care failure:** LGSCO decision `20 013 496` records significant false/unverified statements in case records that were being used to make decisions affecting a family. Recommendations included correcting historical records, telling relevant agencies the statements were false, and warning future social workers to verify the disputed material afresh.

**Adjacent owner:** current NHS England guidance explicitly considers who may already have viewed and relied on inaccurate health/care information; imaging guidance uses audit evidence to trigger safety processes where incorrect information may already have influenced care.

These sources establish correction, notification, future-use controls and consideration of reliance. Public material checked for this artifact does **not** establish the absence of a general social-care prior-act review mechanism.

## Falsifier

Close/delete this candidate if:

- strong current social-care practice already operationalises materially equivalent downstream reliance review;
- the prompt changes no real action beyond ordinary rectification/complaints practice;
- `RELIANCE_NOT_IDENTIFIABLE_FROM_AVAILABLE_RECORDS` dominates and the prompt produces no useful owner decision;
- finding reliance points costs more than the harm it prevents;
- it causes indiscriminate replay of historical decisions;
- an owner-native mechanism expresses the need more clearly or cheaply.

Allowed disposition:

```text
DOMAIN_ALREADY_OWNS_IT
SMALL_OWNER_NATIVE_DELTA
AI_ADDS_NO_DISTINCT_DELTA
INSUFFICIENT_PUBLIC_EVIDENCE
DELETE
```

## Source pointers

Social Work England professional standards + 2026 AI research; ICO right to rectification; GOV.UK ATRS guidance + Data and AI Ethics Framework; Newcastle Magic Notes ATRS; NHS England *Amending patient and service user records*; LGSCO `20 013 496`.

ME/TRACE gets no novelty credit merely for making this join visible. No external contact, policy submission, procurement action, TRACE/ME mutation or authority follows.
