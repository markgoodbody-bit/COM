# PSFH Phase 0 — irreversibility construct v3.3 privacy repair

Status: **DESIGN CANDIDATE / PRIVACY REPAIR ONLY / PRE-EXECUTION / NO RECRUITMENT / NO SPEND / NO STUDY**  
Date: 11 September 2026, Europe/London

This is a narrow normative amendment to the Phase-0 v3.2 design merged at COM `6a3827be53d7e454aae6279dcc8cbd3c174a4eec`.

Parent design object:
- `evidence/PSFH_PHASE0_IRREVERSIBILITY_CONSTRUCT_V3_2_FREEZE_CANDIDATE_20260911.md`
- merged source head before merge: `698615c65ef0f52c6c672d1b2fc32501e0995654`

Feasibility evidence is preserved separately in PR184 / `evidence/PSFH_PHASE0_PREEXECUTION_FEASIBILITY_20260911.md`; that note is evidence, not execution authority.

**Everything in v3.2 remains in force except where this file explicitly replaces it.**

`PRIVACY_REPAIR != CONSTRUCT_REDESIGN`

---

## 1. Defect being repaired

V3.2 currently requires, within one five-person panel, that a recruit answer **no** to whether they personally know or currently work directly with another named/pseudonymous panel member.

That condition is not meaningfully observable under the plausible privacy-preserving recruitment route without creating an unnecessary identity burden:

- Prolific ordinarily exposes participants to researchers through unique pseudonymous Prolific IDs, not names or direct identity;
- researchers must not attempt to identify or re-identify participants;
- direct identifying information must not be collected merely because it would make this panel check convenient; prior approval is required where identifying data is genuinely necessary;
- a participant cannot truthfully determine whether an unfamiliar pseudonymous ID belongs to somebody they know merely from that ID.

A formally present screen that cannot detect the relation it claims to exclude is not a valid independence control.

Current public provider references checked 11 September 2026:
- https://researcher-help.prolific.com/en/articles/445117-can-i-ask-participants-for-their-personal-information-identifiers
- https://researcher-help.prolific.com/en/articles/445116-participants-personal-data
- https://researcher-help.prolific.com/en/articles/449610-participant-vetting-and-identifiers
- https://researcher-help.prolific.com/en/articles/445158-how-to-create-and-manage-participant-groups

`CHECK_EXISTS != CHECK_CAN_DETECT_THE_RELATION`

---

## 2. Replacement panel-identity rule

Replace the v3.2 eligibility bullet:

> within one assigned five-person panel, a recruit must answer no to a direct question asking whether they personally know or currently work directly with another named/pseudonymous panel member. Missing/uncertain answer => do not place that person in that panel before task exposure.

with the following rule:

> Each panel place must be occupied by a **distinct pseudonymous participant identity** under the chosen recruitment platform's ordinary participant-uniqueness controls. Do not ask participants to identify, name, contact, or re-identify other panel members merely to establish social independence. Do not collect names, personal email addresses, phone numbers, social-media identifiers, employer identifiers, or other direct identifying data for this purpose. If a participant voluntarily discloses before task exposure a concrete conflict or relationship that makes their participation inappropriate, handle it under the pre-frozen withdrawal/replacement rule while collecting no more identifying detail than is necessary to act.

The study therefore makes **no claim that panel members are socially independent or mutually unacquainted**.

Required result qualifier:

> Social acquaintance, shared networks, or other unobserved relationships between panel members remain residual dependence not measured by this protocol.

`DISTINCT_PSEUDONYMOUS_IDENTITIES != SOCIALLY_INDEPENDENT_PANEL`

---

## 3. Consequential interpretation change

The v3.2 statements remain:
- `PANEL_N = 1` per stage;
- Stage A and Stage B use different five-person participant identities;
- nobody participates in both stages;
- broad self-described background descriptors may be retained for interpretation but not used to manufacture representativeness;
- no population-independence or general-population reliability claim follows.

V3.3 makes the ceiling sharper:

- distinct platform identities reduce duplicate-person risk but do **not** establish social independence;
- platform identity verification, if any, belongs to the provider's anti-fraud/identity process and is not evidence that participants are independent of one another;
- the protocol does not seek special permission to collect direct identifiers simply to make the discarded acquaintance gate observable;
- any result must carry the residual social-dependence limitation.

This weakens an unearned independence claim rather than increasing participant privacy burden to preserve it.

---

## 4. Provider-neutrality boundary

This repair does **not** choose Prolific.

Prolific is the feasibility case that exposed the defect. A later provider may be used only through the separate pre-execution packet and Mark's consequential authority. Regardless of provider, the design preference is:

1. use the platform's ordinary pseudonymous participant identity;
2. collect no direct identifying data unless the study genuinely requires it and the relevant approval/data-protection basis exists;
3. do not create a social-network mapping task merely to strengthen an independence claim this small construct-validity panel cannot earn anyway.

If a later provider offers a privacy-preserving, independently verifiable method of preventing known co-participants without disclosing identities, that capability may be recorded prospectively in the execution packet. It does not silently restore the discarded v3.2 gate or expand the current claim.

`POSSIBLE_FUTURE_CONTROL != CURRENTLY_MEASURED_INDEPENDENCE`

---

## 5. Contamination / conflict handling remains prospective

The existing prior-project-exposure exclusions remain unchanged.

If a participant voluntarily reports a conflict, relationship, or prior exposure before task content is shown:
- preserve withdrawal;
- apply only the replacement/noncompletion rule frozen before recruitment;
- do not ask for unnecessary identity details;
- record only the minimum pseudonymous audit fact needed to show why the place was not used;
- do not replace based on whether a participant's task answer looks favourable or unfavourable.

A relationship discovered after task exposure is recorded as a limitation/contamination event under the frozen protocol; do not erase the return and silently recruit a more convenient replacement.

---

## 6. No other v3.2 rule changes

This amendment does **not** change:
- the irreversibility-point definition;
- Stage-A source-selection freeze;
- A1 -> checkpoint -> A2 -> checkpoint -> A3 sequence;
- two-checkpoint semantic revision budget;
- Stage-B N=6;
- Stage-B-only per-builder order randomisation;
- `PANEL_N = 1`;
- source-sufficiency or matching/family rules;
- raw/discrete finite-panel reporting;
- A3 single-account versus Stage-B aggregate distinction;
- contact-run status;
- owner-comparator requirement for later efficacy work;
- provider/source selection, participant contact, payment, inference or execution authority.

No participant/provider/source state was changed to create this file.

---

## 7. Current boundary

V3.3 remains a **design candidate** until source-bounded review.

It does not authorise:
- opening or funding a provider account;
- recruitment, screening or participant contact;
- collecting direct identifiers;
- selecting or reading Stage-A cases;
- payment/spend;
- model inference;
- public study;
- any usefulness claim.

Next legitimate operation: source-bounded review of whether this is the smallest honest privacy repair and whether any v3.2 dependence claim still overstates what distinct pseudonymous identities establish.

CC is currently unavailable due token budget; no fresh CC approval is assumed.

`PRIVACY_BURDEN_CAN_FALSIFY_A_DESIGN_DETAIL`  
`DISTINCT_IDENTITY != INDEPENDENCE`  
`DESIGN_REPAIR != EXECUTION_AUTHORITY`
