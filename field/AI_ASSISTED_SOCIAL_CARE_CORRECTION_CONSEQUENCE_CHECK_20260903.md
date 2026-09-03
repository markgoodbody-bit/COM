# Social-care record correction — consequence check

Status: **FIELD / OWNER-NATIVE / NON-CANONICAL / NOT POLICY**  
Related case: COM #99.

## Use only when

A **material error in an official social-care record is discovered after the inaccurate version may already have informed an assessment, plan, risk judgement or action**.

Do not use this for an AI draft corrected before it enters the system of record, a harmless typo, or a disagreement with a supportable professional opinion.

This problem predates AI. AI-assisted recording is the live use case, not a new category of correction duty.

## Existing owner protections

Start with them; do not replace them.

- **Social Work England:** accurate/up-to-date records, documented decision reasoning and professional accountability.
- **UK GDPR / ICO:** rectify inaccurate personal data and notify recipients where required.
- **ATRS / UK Data & AI Ethics guidance:** document how algorithmic output relates to decisions; provide review/redress and auditability.
- **NHS health-and-care records guidance:** when inaccurate information is corrected, consider who viewed it and may have relied on it for care/treatment decisions.

## The one question

> **If a material error in a case record is discovered after the record has been used, can you identify which consequential assessments, plans, risk judgements or actions relied on the earlier version, and who is responsible for reviewing those downstream effects?**

## Bounded use

1. **Correct / dispute the authoritative record** using the existing record-integrity process. Preserve the audit/history required by that system.
2. **Notify external recipients** through the existing data-protection / information-governance route where required.
3. **Identify only material internal reliance points** where the earlier version could plausibly have changed an assessment, plan, risk judgement, placement/service decision, referral, closure or other consequential act.
4. **Route each material reliance point to its existing human/professional owner.** This check has no authority to reverse a decision.
5. The owner either leaves the prior act unchanged with reasons, revises/reopens it, routes remedy, or records that materiality remains unknown.

Do not reconstruct every read of the record. Proportionality is part of the check.

```text
HUMAN_REVIEW_OCCURRED != ERROR_IMPOSSIBLE
RECORD_RECTIFIED != PRIOR_DECISION_RECONSIDERED
RECIPIENT_NOTIFIED != INTERNAL_RELIANCE_REVIEWED
CORRECTED_RECORD != RESTORED_RESULT
TRACEABLE_CONSEQUENCE != AUTOMATIC_REVERSAL
```

## Why this is grounded

**Current AI use:** Newcastle's public Magic Notes ATRS says practitioners review/edit AI drafts before official entry and that the resulting official notes inform care planning, assessments and follow-up actions. Its public `appeals and review` entry describes opting out of Magic Notes use; it does not establish a post-entry correction/reliance process. That is a transparency limit, not proof that Newcastle lacks one.

**Real children's-social-care failure:** LGSCO decision `20 013 496` records significant false/unverified statements in case records that were being used to make decisions affecting a family. Recommendations included correcting historical records and telling relevant agencies the statements were false.

**Adjacent owner:** current NHS England guidance explicitly considers who may already have viewed and relied on inaccurate health/care information; imaging guidance uses audit evidence to trigger safety processes where incorrect information may already have influenced care.

## Falsifier

Close/delete this candidate if:

- strong current social-care practice already operationalises materially equivalent downstream reliance review;
- the question changes no real action beyond ordinary rectification/complaints practice;
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
