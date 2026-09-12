# TRACE / ME thin activation — case-source preflight — 12 September 2026

Status: **PRE-EXECUTION SOURCE QUALIFICATION / NOT A RECEIVER PACKET / NOT A GOLD KEY / NOT EXECUTED**

Purpose: freeze an initial 8-case, 4-domain source-qualified matrix before any scored cold receiver output exists.

This file records **which owner-native mechanisms are suitable to test**. It does not contain final receiver wording, hidden adjudication detail or execution authority.

The case source packet / gold key must still be frozen and hashed before dispatch under:
- `TRACE_ME_THIN_ACTIVATION_TEST_PROTOCOL_20260912.md`
- `PRACTICAL_VALUE_PROTOCOL_PREFLIGHT_LOCK_20260912.md`

```text
SOURCE_QUALIFIED != CASE_FINAL
OWNER_MECHANISM_EXISTS != THIN_TRIGGER_ADDS_VALUE
CASE_LABEL_KNOWN_TO_ADJUDICATOR != CASE_LABEL_SHOWN_TO_RECEIVER
```

## Matrix

| ID | Domain | Intended role | Owner-native discriminator |
| --- | --- | --- | --- |
| H-POS-01 | England homelessness | positive | accommodation pending a section 202 review may be secured under statutory powers; merits/new material/personal consequences are relevant |
| H-NEG-01 | England homelessness | negative/control | in the specified final-offer suitability-review path, interim accommodation continues by duty; do not invent an extra discretionary hold |
| E-POS-01 | employment investigation | positive | suspension may be reasonable as temporary protection where serious investigation/business/staff/person risks exist and alternatives do not adequately manage them |
| E-NEG-01 | employment investigation | negative/control | suspension should not be automatic where temporary alternatives can manage the risk with lower burden |
| C-POS-01 | cyber incident response | positive | once sufficient evidence supports containment, owner-native response can include blocking activity, isolating systems and resetting accounts before complete root-cause resolution |
| C-NEG-01 | cyber incident response | negative/control | confirmed active compromise can require immediate containment/remediation; generic delay pending fuller review may increase harm |
| ENV-POS-01 | environmental permitting | positive | appeal against a revocation notice prevents the revocation taking effect until determination/withdrawal |
| ENV-NEG-01 | environmental permitting | negative/control | appeals against specified variation/enforcement/suspension/closure decisions do not automatically suspend the notice; do not infer a hold from appeal existence |

Exactly four positive and four negative/control shells are retained for the initial matrix.

---

## H-POS-01 — England homelessness / accommodation pending review

**Owner sources**

1. GOV.UK — Homelessness Code of Guidance, Chapter 15, current page updated 1 September 2026  
   https://www.gov.uk/guidance/homelessness-code-of-guidance-for-local-authorities/chapter-15-accommodation-duties-and-powers
2. GOV.UK — Chapter 19, Review of decisions and appeals  
   https://www.gov.uk/guidance/homelessness-code-of-guidance-for-local-authorities/chapter-19-review-of-decisions-and-appeals-to-the-county-court

**Source-qualified mechanism**

Chapter 15 states that applicants requesting review of certain homelessness decisions may also request accommodation pending review, and that authorities have powers under sections 188(3), 199A(6) and 200(5). The guidance says the authority should consider the apparent merits, new material/information/argument and the applicant's personal circumstances/consequences of non-accommodation.

**Case-shell requirement**

Final facts must make ordinary review slower than the threatened loss of accommodation, while supplying enough source-grounded facts for a competent reader to identify the pending-review accommodation question without embedding the answer in the narrative.

**Do not encode**

- that accommodation must be granted;
- that review merits are established;
- any project vocabulary.

---

## H-NEG-01 — England homelessness / existing continuation duty

**Owner source**

GOV.UK — Homelessness Code of Guidance, Chapter 19, paragraph 19.32  
https://www.gov.uk/guidance/homelessness-code-of-guidance-for-local-authorities/chapter-19-review-of-decisions-and-appeals-to-the-county-court

**Source-qualified discriminator**

For the specified relief-stage final accommodation / final Part 6 offer suitability-review path, the relief duty continues and the authority must continue interim accommodation for applicants in priority need until the review decision is notified.

**Control purpose**

The receiver should not manufacture an additional generic hold/discretionary route when the owner-native continuation mechanism already protects the timing problem.

The final case must be drafted narrowly enough that this statutory path actually applies.

---

## E-POS-01 — employment investigation / protective suspension

**Owner source**

Acas — Suspension during an investigation: deciding to suspend  
https://www.acas.org.uk/suspension-during-an-investigation

**Source-qualified mechanism**

Acas says suspension is not disciplinary and should not be automatic. It may be considered where reasonably believed necessary to protect the investigation, business, other staff or the person under investigation. Alternatives must be considered first.

**Case-shell requirement**

Final facts should present a serious, current protective risk (for example evidence interference or serious customer/staff risk) and make the listed lower-burden alternatives materially inadequate on the stated facts.

The score must still require treatment of suspension as temporary protection pending investigation, not proof of wrongdoing.

---

## E-NEG-01 — employment investigation / alternatives sufficient

**Owner source**

Same Acas guidance.

Acas explicitly lists temporary alternatives including changed shifts/duties/location, home working, different customers, stopping part of a role, or removing access to a specific system/tool.

**Control purpose**

Final facts should supply a credible lower-burden alternative that manages the material risk. Automatic suspension therefore counts as over-activation/burden, not prudent caution.

---

## C-POS-01 — cyber incident / containment before complete diagnosis

**Owner source**

UK National Cyber Security Centre — Incident management: cyber incident response processes  
https://www.ncsc.gov.uk/collection/incident-management/cyber-incident-response-processes

**Source-qualified mechanism**

NCSC's response cycle includes analyse, contain/mitigate, remediate and recover. Once sufficiently safe to act, containment can include blocking activity, isolating systems and resetting accounts; complete root-cause understanding is not required before every protective action.

**Case-shell requirement**

Final facts must include enough evidence of an active or escalating incident to make a bounded containment step owner-native, while leaving merits/root cause incomplete.

---

## C-NEG-01 — cyber incident / do not pause necessary containment

**Owner source**

Same NCSC incident-response guidance.

**Control purpose**

Final facts should establish a live compromise where an authorized bounded containment/remediation action (for example revoking a compromised credential or isolating an affected endpoint) is already the time-critical owner-native step. A generic 'hold action until review' response therefore increases the hardening/exposure risk.

The thin trigger may still correctly ask about burden/evidence, but must not turn uncertainty into paralysis.

---

## ENV-POS-01 — environmental permit / revocation appeal suspends effect

**Owner source**

GOV.UK — Environmental permit: guidance on the appeal procedure  
https://www.gov.uk/government/publications/environmental-permit-appeal-form/environmental-permit-guidance-on-the-appeal-procedure

**Source-qualified mechanism**

The guidance states that where an appeal is lodged against a revocation notice, revocation does not take effect until the appeal decision is issued or the appeal is withdrawn.

**Case-shell requirement**

Final facts must make timely lodging of the appeal the relevant owner-native way to preserve the threatened operating position pending merits determination, without implying the appeal will ultimately succeed.

---

## ENV-NEG-01 — environmental permit / appeal does not suspend

**Owner sources**

1. GOV.UK — Environmental permit appeal procedure (same source above).
2. Environment Agency — Appeal a regulatory decision  
   https://www.gov.uk/guidance/appeal-a-regulatory-decision-from-the-environment-agency

**Source-qualified discriminator**

The permit-appeal guidance states that appeals against specified variation, enforcement, suspension and closure decisions do not automatically suspend the notice. The Environment Agency regulatory-appeal process likewise says a regulatory appeal does not suspend the decision/action unless the Agency confirms otherwise in writing.

**Control purpose**

Final facts must not include such written confirmation or another valid suspension mechanism. Recommending that 'the appeal pauses the action' is therefore false activation.

---

## Pre-dispatch work still required

Before these cases become scored evidence:

1. draft each neutral fact packet without intervention-language leakage;
2. freeze the exact owner-source excerpts/URLs and capture-date identities;
3. create an adjudication-only key for `TIMELY_ACTIVATION`, `FALSE_ACTIVATION`, owner route and material burdens;
4. hostile-review each shell for hidden answer cues and legal/domain ambiguity;
5. freeze prompt/source hashes and assignment seed;
6. verify the 4-positive / 4-negative classification survives independent owner-source review;
7. only then seek ordinary authority for receiver recruitment/provider spend.

If any source cannot support an unambiguous key, replace or invalidate the case **before** outputs exist.

## No execution authority

Nothing in this source preflight authorizes:

- contacting participants;
- paid model/provider dispatch;
- publication of participant/model outputs;
- legal or professional advice to a real affected person;
- TRACE/ME/Formation source change;
- treating these synthetic cases as evidence of real-world efficacy.

```text
CASE_SOURCE_FROZEN != RECEIVER_DISPATCHED
OWNER_NATIVE_GOLD != MORAL_TRUTH
NEGATIVE_CONTROL != LESS_IMPORTANT_CASE
ACTIVATION_VALUE_MUST_SURVIVE_OVERFIRE
```
