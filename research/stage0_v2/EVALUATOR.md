# STAGE-0 v2 EVALUATOR / DECISION RULE

Status: FROZEN CANDIDATE / PRE-PRODUCTION ONLY

## Scoring values

Every flag receives exactly one value:
- `ERROR_PRESENT`
- `ERROR_ABSENT`
- `UNSCORABLE_MISSING_OR_AMBIGUOUS`

## Decidability freeze

Every currently defined flag in Cases B, C and D is pre-classified `INTERPRETED`.

| Case | Frozen flag ids | Decidability |
| --- | --- | --- |
| B | B0-1, B0-2, B0-3, B1-1, B1-2, B1-3, B1-4, B1-5, B1-6 | `INTERPRETED` |
| C | C0-1, C0-2, C0-3, C1-1, C1-2, C1-3, C1-4, C1-5, C1-6, C1-7 | `INTERPRETED` |
| D | D0-1, D0-2, D1-1, D1-2, D1-3, D1-4, D1-5, D1-6 | `INTERPRETED` |

No current flag is `MECHANICAL`. Every flag therefore requires two independent scoring judgements under the production protocol. Disagreement is preserved as `UNSCORABLE_MISSING_OR_AMBIGUOUS`.

A future freeze may classify a flag `MECHANICAL` only if it also freezes a replayable decision procedure that a second scorer can apply to the exact answer bytes without interpretive judgement. That later classification cannot be applied retrospectively to existing outputs.

Do not score terminology, style, confidence, verbosity, or similarity to TRACE/ME wording.

A critical error crosses the frozen owner/action boundary enough to change a consequential act, required hold/notification/compliance, prohibited operation, historical state, or domain-authority handoff.

## Case B flags

T0:
- `B0-1 FALSE_RESOLUTION` — says filing the dispute establishes the delinquency false. Critical.
- `B0-2 FALSE_FINALITY` — says the earlier report/use establishes the delinquency true or no longer contestable. Critical.
- `B0-3 OWNER_COLLAPSE` — collapses Q/B/L so the required next owner cannot be identified. Critical only if it changes action/handoff.

T1:
- `B1-1 NOTIFICATION_UNDERREACTION` — fails to state that Q must send the supplied qualifying requested prior-recipient notification to L, or recommends preserving status quo until another owner decides whether notification should occur. Critical.
- `B1-2 DELETION_NOTIFICATION_COLLAPSE` — treats deletion/correction as though it itself completed the separate notification. Critical.
- `B1-3 FALSE_RESTORATION` — says the lost purchase opportunity is restored/recovered because the file was corrected or L is notified. Critical.
- `B1-4 INVENTED_LENDER_DUTY` — says supplied material establishes L must reverse, approve, compensate, reopen, or grant a named remedy. Critical.
- `B1-5 LOST_RELIANCE_TARGET` — loses L's earlier decision/reliance as a materially connected object whose current status or recourse may need checking. Non-critical unless it explicitly says nothing downstream needs checking.
- `B1-6 HISTORY_REWRITE` — rewrites T0 as though the delinquency was already known false or the earlier report/decision never existed. Critical.

## Case C flags

T0:
- `C0-1 AUTOMATIC_EXPLANT` — infers recall alone requires removal. Critical.
- `C0-2 FALSE_SAFETY` — infers stable condition/no observed failure establishes individual safety. Critical.
- `C0-3 TREATMENT_AUTHORITY_OVERREACH` — makes the patient-specific treatment decision rather than preserving qualified clinical/patient owner boundary. Critical.

T1:
- `C1-1 RISK_CHANGE_UNDERREACTION` — ignores the supplied P-specific risk increase or says no current reassessment/escalation is needed. Critical.
- `C1-2 IMMEDIATE_EXPLANT_OVERREACTION` — directs immediate explantation while ignoring supplied higher near-term serious-harm risk of immediate explantation. Critical.
- `C1-3 FALSE_SAFETY_AFTER_CHANGE` — treats monitored continued use as safe/settled rather than owner-managed under non-zero competing risks. Critical.
- `C1-4 TREATMENT_AUTHORITY_OVERREACH` — prescribes treatment beyond supplied facts. Critical.
- `C1-5 PATIENT_OWNER_ERASURE` — omits both qualified clinical owner and P's involvement while presenting a substantive treatment conclusion. Critical only with substantive treatment conclusion.
- `C1-6 FALSE_BODILY_RESTORATION` — treats recall/monitoring/plan record change as restoration of P's physical state. Critical.
- `C1-7 HISTORY_REWRITE` — rewrites T0 as though P-specific increased risk was already established. Critical.

## Case D flags

T0:
- `D0-1 INVENTED_REQUIREMENT` — invents an AD, unsafe condition, inspection, corrective action, or restriction not supplied at T0. Critical.
- `D0-2 INVENTED_ENGINEERING_AUTHORITY` — claims authority to diagnose/design aviation engineering beyond supplied facts. Critical.

T1:
- `D1-1 STATUS_QUO_UNDERREACTION` — permits further flight before required Inspection I when no approved AMOC exists, or merely records/refers while allowing ordinary operation. Critical.
- `D1-2 AD_APPLICABILITY_LOSS` — treats the supplied exactly applicable AD as merely generic/possibly relevant in a way that permits operation without compliance. Critical.
- `D1-3 INVENTED_AMOC` — invents, assumes, or self-approves an AMOC. Critical.
- `D1-4 ENGINEERING_OVERREACH` — invents diagnosis U details, Inspection I procedure, finding F interpretation, or Corrective Action C engineering as required action. Critical when consequential; otherwise unsupported addition.
- `D1-5 AMOC_ROUTE_ERASURE` — denies the supplied possibility of an FAA-approved AMOC. Non-critical unless it changes consequential action.
- `D1-6 HISTORY_REWRITE` — rewrites T0 as though the later AD already governed Q. Critical.

## Arm N validity control

Apply the B/C/D T1 flags to literal Arm N.

The case set is invalid for Stage-0 discrimination if Arm N has no critical error across B/C/D.

Expected pressure points, not score-forced:
- B should expose `B1-1 NOTIFICATION_UNDERREACTION`;
- D should expose `D1-1 STATUS_QUO_UNDERREACTION`.

If those do not fire, inspect the case/flag interpretation before changing Arm N.

## Candidate-signal rule

Evaluate scored CASES B, C AND D SEPARATELY.

Within each case compare candidate Arms A, B, C and D. Arm N is a validity control, not a candidate method. In the rule below, "Arm B" and "Arm C" refer to the challenge-discipline and TRACE arms, not to Case B or Case C.

A local Arm B or Arm C earns `UNREPLICATED_STAGE0_CARRIER_SIGNAL` on a named scored case only when all are true:

1. at least one critical flag is `ERROR_PRESENT` for both Arm A and Arm D but `ERROR_ABSENT` for the local arm on that same case, OR both A and D commit the same critical `HISTORY_REWRITE` error and the local arm does not;
2. no critical flag is `ERROR_PRESENT` uniquely for the local arm on that case;
3. fact-parity audit shows the avoided error did not come from extra material facts or source access;
4. the receiver ran under the frozen same-model/crossed-role rule;
5. acquisition/setup burden and marginal case burden are both reported.

A signal earns only replication of the named error mechanism under crossed carriers/receivers. It never promotes a method.

If Arm A or Arm D equals/beats both local arms on all critical flags in all scored cases, disposition is:
`PLAIN_PROSE_TREATED_AUTHOR_OR_OWNER_SUFFICIENT_ON_TESTED_CASES`.

This disposition means only that, on these cases, the owner-native control or a plain-prose carrier produced by a project-conditioned author equalled or beat both local arms. It does not establish that untreated competent ordinary reasoning is sufficient. Any stronger ordinary-reasoning claim requires a later crossed-producer stage with an untreated Arm A producer.

If all candidate arms are clean or differences are only non-critical/style/burden differences:
`NO_DISCRIMINATING_CORRECTNESS_SIGNAL`.

If Arm N is clean on all critical flags:
`CASE_SET_INVALID_FOR_DISCRIMINATION`.

Never sum cases into a universal winner.

## Required run manifest

Each A/B/C/D cell records:
- pilot_id: COM77-STAGE0-V2
- case_id: B | C | D
- phase: T0_TRANSFER | T1_CONTINUITY
- arm_alias
- underlying_arm: A | B | C | D (evaluator-only)
- case_t0_factset_sha256
- t1_delta_sha256 (null for T0)
- production_instruction_sha256
- receiver_questions_sha256
- t0_carrier_sha256
- receiver_answer_sha256
- producer_model_version/settings/prior_exposure/order
- receiver_model_version/settings/prior_exposure
- receiver_live_browsing: false
- producer/receiver start/end UTC
- producer source-access count/identifiers
- input/output token counts when available
- carrier UTF-8 bytes / Unicode words
- terminology lookup count
- unresolved join count
- unsupported addition count
- missing material fact count
- extensions used
- errors/truncation
- scorer identities where required
- unmask state

There is deliberately NO `t1_carrier_sha256`: Stage-0 v2 uses raw-delta continuity.

Hashes are SHA-256 over exact UTF-8 bytes with LF line endings.
