# ATRS answerability audit — reader walkthrough

Status: **ILLUSTRATIVE READBACK FROM THE FROZEN 152-RECORD WITNESS / NOT A SCORE / NOT A PREVALENCE ESTIMATE**

Source witness: run `35257984573`, artifact `10513278849`, source head `4a7b43df95a2b776b885f8ee903d929100414af7`.

Purpose: test whether merely knowing that an ATRS record contains an `Appeals and review` field tells a reader what practical kind of answer-back disclosure the record contains.

It does not. The preserved public records show materially different disclosure shapes.

| Example | What the published field lets a reader observe | Bounded description |
|---|---|---|
| **Health Research Authority — Proportionate Review Toolkit** | A queries email is provided and the text describes review by a senior advisor. | `CONCRETE_REVIEW_ROUTE_OBSERVED` — no claim about statutory appeal rights or effectiveness. |
| **UK Hydrographic Office — Tidal Harmonic Analysis and Prediction** | The text says there is no formal appeal and gives a customer-services feedback route. | `GENERAL_FEEDBACK_ROUTE_OBSERVED` — feedback is not automatically reconsideration. |
| **NS&I — PolyAI** | The text says callers may request a human advisor and describes standard complaints/escalation, but the section contains no URL/email/phone locator. | `IN_CHANNEL_HUMAN_HANDOFF_AND_PROCESS_DESCRIBED` — token absence does not mean no action is available. |
| **QCovid algorithm** | The field says patients first review results with their clinician; its hyperlink is clinician guidance rather than a reconsideration/contact locator. | `HUMAN_MEDIATED_REVIEW_DESCRIBED / LINK_NOT_A_REVIEW_LOCATOR`. |
| **Cabinet Office — Automated Digital Document Review** | Hard deletion is described as non-recoverable and appeal not possible, while retained evidence may later justify deletion in an appeal or FOI request. | `AMBIGUOUS_EXPLANATION_VS_RECOVERY` — preserve the tension instead of declaring a remedy. |
| **DBT — Find Exporters** | The parser observes `Human decisions and review` but no matching `Appeals and review` field in the frozen public page. | `APPEALS_FIELD_NOT_OBSERVED` — not evidence that no review practice exists. |

## Reader questions that remain separate

For any record, a reader may need to distinguish:

1. Does the publication say a person can challenge, review, complain about or revisit an output/decision?
2. Does it describe an **in-channel action** such as asking for a human?
3. Does it refer to an **existing broader process** such as ordinary complaints or benefit appeal?
4. Does it provide a **concrete locator** for that process in the field itself?
5. Is the only route **general help/feedback**, rather than reconsideration?
6. Does it explicitly say no separate process is applicable because the tool does not make the decision?
7. Is the disclosure ambiguous about what can actually be changed versus merely explained later?

Those questions are not interchangeable and should not be collapsed into one scalar.

## Tight finding under test

> In the current ATRS public finder, `Appeals and review` is almost universally present as a field, but field presence does not identify one uniform public answer-back object. The published disclosures can expose materially different things: concrete review routes, general feedback, in-channel human handoff, references to existing procedures without locators, explicit no-separate-process statements, or ambiguous explanation/recovery boundaries.

The current evidence supports that **heterogeneity claim**. It does not establish how common every semantic category is across all token-negative records, whether any route works, or whether any publication complies with law/policy.

```text
FIELD_PRESENT != PRACTICAL_NAVIGABILITY
CONTACT_TOKEN != REVIEW_RIGHT
HUMAN_HANDOFF != FORMAL_APPEAL
PROCESS_DESCRIBED != PROCESS_EFFECTIVE
PUBLIC_DISCLOSURE != INTERNAL_PRACTICE
```
