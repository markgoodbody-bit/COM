# AI-assisted social-care records — correction consequence check

Status: **FIELD / OWNER-NATIVE TRANSFER / NON-CANONICAL / NOT POLICY**

Related field case: COM #99.

## Purpose

Use this only when a **material error in an official social-care record is discovered after that record may already have informed a consequential assessment, plan, risk judgement or action**.

It is not a generic AI governance framework. It does not assume AI made the decision. It does not require retaining every transient AI draft.

```text
AI_NOT_FINAL_DECISION_MAKER != AI_NOT_CAUSALLY_ACTIVE
HUMAN_REVIEW_OCCURRED != ERROR_IMPOSSIBLE
RECORD_RECTIFIED != PRIOR_DECISION_RECONSIDERED
```

The check is mostly assembled from existing owner practice:

- Social Work England: accurate/up-to-date records, documented decision reasoning, professional accountability and communication of assessment implications;
- UK GDPR / ICO: rectify inaccurate personal data and notify recipients where required;
- UK public-sector AI guidance: end-to-end auditability, redress and review of erroneous outcomes;
- ATRS: explain the relationship between algorithmic output and decisions, plus human/appeal review;
- NHS health-and-care records guidance: when inaccurate information is corrected, consider who viewed it and may have relied on it for care/treatment decisions.

Mechanical Ethics / TRACE receives no novelty credit merely for making the join visible.

## Trigger

Run the check only when all three are true:

1. a material inaccuracy or omission in the **authoritative record** is established or formally disputed strongly enough to require review;
2. the inaccurate version existed long enough that another consequential process could have consumed it;
3. the downstream effect is not already known to be zero.

Do **not** run it merely because:

- an AI draft contained an error that the practitioner corrected before it entered the system of record;
- a typo with no material effect was corrected;
- the record was corrected before any relevant recipient/process used it;
- someone disagrees with a professional opinion that remains factually and procedurally supportable.

## The check

### 1. Record

Has the authoritative record been corrected, annotated or formally disputed using the owner system's normal record-integrity process?

Preserve the audit/history required by that system. Do not rewrite history merely to make the current record look clean.

### 2. External recipients

Was the inaccurate information disclosed outside the authority?

If yes, use the existing data-protection / information-governance route to determine which recipients must be informed of the correction.

### 3. Internal reliance

Identify only **material reliance points** that could plausibly have used the inaccurate version, for example:

- assessment;
- care / child-in-need / safeguarding plan;
- risk judgement;
- placement or service decision;
- referral / escalation / closure;
- report to a decision-making forum;
- consequential follow-up action.

Do not reconstruct every read of the record. The question is whether the error could have changed a consequential act.

### 4. Review owner

For every material reliance point, identify the existing human/professional owner with standing to reconsider it.

```text
ERROR_FOUND != FRAMEWORK_AUTHORITY
TRACEABLE_CONSEQUENCE != AUTOMATIC_REVERSAL
```

This check does not decide the case outcome.

### 5. Disposition

The owner records one bounded result for each material reliance point:

- `UNCHANGED_AFTER_REVIEW` — earlier act remains supportable after correction; record why;
- `REVISED` — assessment/plan/judgement/action changed;
- `REOPENED` — further evidence or process required;
- `REMEDY_REQUIRED` — prior consequence cannot be fully undone and a remedy route is needed;
- `NOT_MATERIAL` — correction cannot materially affect this reliance point;
- `UNKNOWN / ESCALATE` — consequence or authority cannot yet be established.

The vocabulary is illustrative, not a required schema.

## One-line assurance question

> **If a material error in an AI-assisted record is discovered after the record has been used, can you identify which consequential assessments, plans, risk judgements or actions relied on the earlier version, and who is responsible for reviewing those downstream effects?**

That single question is the actual candidate artifact. Everything else on this page exists to stop it being over-read.

## Grounded use cases

### Current AI-assisted recording

Newcastle's public Magic Notes ATRS says practitioners review/edit AI drafts before official entry, while the resulting case notes inform care planning, assessments and follow-up actions. Its published `appeals and review` field describes opting out of Magic Notes use, but does not establish a post-entry correction/reliance process.

This is a public-transparency gap only. It is **not evidence that Newcastle lacks an internal process**.

### Historical children’s social-care record failure

LGSCO decision `20 013 496` records significant unverified/factually inaccurate statements in children's social-care records that were being used to make decisions affecting a family. The remedy included correcting historical records and notifying relevant agencies that statements were false.

That case demonstrates:

```text
INACCURATE_RECORD -> REAL_DECISION_EFFECT
```

It does not establish a universal downstream-decision review mechanism.

### Adjacent owner counterexample

Current NHS England guidance on amending patient/service-user records explicitly says organisations should consider who viewed inaccurate information and may have relied on it for care/treatment decisions. Current imaging-safety guidance uses audit evidence to trigger local safety protocols where incorrect information may already have influenced care.

That means the underlying principle is already owned elsewhere. The only question is whether an equally usable practice is explicit and operational in social-care record workflows.

## AI-specific ceiling

This problem predates AI. Manual case records can be false, incomplete or misleading too.

AI may alter scale, speed, formation conditions and source-retention patterns, but it does not create a new moral category of record error.

```text
AI_ASSISTED != AI_CAUSED
AI_CAUSED != AI_SOLE_CAUSE
AI_ERROR != UNIQUE_CORRECTION_DUTY
```

If ordinary social-care correction practice already handles the causal cone adequately, retire this artifact.

## Falsifier

Delete / close this candidate if any of the following is established:

1. current strong social-care practice already requires and operationalises materially equivalent downstream reliance review;
2. the one-line question never changes a real action beyond ordinary rectification/complaints practice;
3. identifying reliance points adds more burden than it prevents under realistic case-record systems;
4. the question encourages indiscriminate replay of historical decisions rather than material/proportionate review;
5. an owner-native mechanism expresses the need more clearly and cheaply.

Allowed disposition:

```text
DOMAIN_ALREADY_OWNS_IT
SMALL_OWNER_NATIVE_DELTA
AI_ADDS_NO_DISTINCT_DELTA
INSUFFICIENT_PUBLIC_EVIDENCE
DELETE
```

## Source pointers

- Social Work England, *Professional standards* and *The emerging use of Artificial Intelligence (AI) in social work*.
- ICO, *Right to rectification*.
- GOV.UK, *Algorithmic Transparency Recording Standard* guidance and *Data and AI Ethics Framework*.
- GOV.UK ATRS, *Newcastle City Council: Magic Notes*.
- NHS England Digital, *Amending patient and service user records*.
- Local Government and Social Care Ombudsman, decision `20 013 496`.

No external organisation has been contacted and no policy submission, procurement action, TRACE/ME mutation or authority claim follows from this field artifact.
