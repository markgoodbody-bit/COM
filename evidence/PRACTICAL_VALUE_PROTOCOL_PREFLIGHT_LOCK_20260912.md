# Practical-value protocol preflight lock — 12 September 2026

Status: **PRE-EXECUTION DECISION LOCK / NOT EXECUTED / NOT EFFICACY EVIDENCE / NO SPEND OR RECRUITMENT AUTHORITY**

Purpose: close interpretation degrees of freedom discovered during preflight of:

- `TRACE_ME_THIN_ACTIVATION_TEST_PROTOCOL_20260912.md`
- `COM_BOUNDED_CONTINUITY_RELOAD_TEST_PROTOCOL_20260912.md`

This file does **not** change either intervention, arm, owner-native mechanism or authority boundary. It fixes adjudication, stopping and pre-dispatch packet-fairness rules before any scored cold-receiver output exists.

```text
PREREGISTERED != FULLY_DECISION_LOCKED
PRE_EXECUTION_REPAIR != POST_HOC_RESCUE
NULL_RESULT != FAILED_PROJECT
```

## Global freeze rule

Before the first scored receiver is dispatched, freeze and hash:

- exact protocol versions;
- case/task roster;
- case classifications / gold keys;
- receiver-family grouping rule;
- arm assignment/randomisation seed where used;
- adjudicator identities or selection rule;
- scoring sheet;
- this decision lock.

After the first scored output is returned, no success threshold, exclusion rule, family definition, burden ceiling or packet-fairness rule may change for that run. A later protocol version must be a new test, not a repair of the observed result.

Receivers excluded as contaminated or technically malformed must be excluded under a reason that was available before arm comparison. Preserve every exclusion and raw output.

---

# A. TRACE / ME thin activation — decision lock

## Minimum evaluable run

Primary A/B disposition requires all of:

- at least **8 valid cases**;
- at least **4 valid positive cases** and **4 valid negative cases** after malformed/ambiguous-case exclusions;
- at least **4 materially different domains** represented among valid cases;
- at least **3 pre-declared cold receiver families**;
- both arms represented on positive and negative cases in every receiver family used for the primary comparison;
- no receiver sees the same case in both arms.

A **receiver family** must be defined before outputs are read. Provider/model/runtime lineage, hidden-memory risk and shared scaffolding must be considered. Do not split one substantially shared system into multiple families merely to satisfy the count.

If these conditions are not met, disposition is `INADEQUATE_TEST`; do not extrapolate from a partial matrix.

## Packet construction / answer-leakage lock

Before final case packets are hashed, every packet must pass a **label-blind leakage review** separate from merits/source adjudication.

The packet may state legally or operationally decisive neutral facts needed to determine which owner-native rule applies. Examples include the governing statutory regime, timing relative to a standstill/notice, priority-need status, review type, or the concrete availability of a lower-burden control. Omitting those facts merely to make the case harder is prohibited.

The packet must **not** state or strongly paraphrase the conclusion being scored. Prohibited answer-bearing constructions include language equivalent to:

- “suspension is necessary / unnecessary”;
- “the appeal automatically pauses / does not pause the action”;
- “a hold should be granted”;
- “ordinary review is too late, so interim protection is required”;
- named project distinctions or intervention language that tells the receiver what relation to inspect.

Load-bearing regime/status facts that could become cues must be presented symmetrically across the relevant positive/negative pair where the owner regime is shared. For example, if `Procurement Act 2023` is a necessary discriminator, both procurement packets name that regime.

Leakage review procedure before freeze:

1. reviewer receives the neutral case packet without arm, positive/negative label or gold key;
2. reviewer marks any sentence that states or editorially implies the scored owner-native conclusion rather than supplying a factual premise;
3. such wording is rewritten or the case is invalidated **before** hashing;
4. the reviewer is not asked to optimise case difficulty or make the answer obscure;
5. preserve the leakage-review receipt and all rewrites.

A packet is not malformed merely because a competent reader can infer the right mechanism from sufficient facts. **DISCOVERABLE_ANSWER != LEAKED_ANSWER.** The test is whether the trigger changes activation, not whether the owner rule can be hidden.

After the first scored output, packet wording may not be repaired for answer leakage within that run.

```text
NEUTRAL_DECISIVE_FACT != ANSWER_LEAK
DISCOVERABLE_ANSWER != LEAKED_ANSWER
HARDER_CASE != FAIRER_CASE
```

## Locked primary comparison

For each valid positive output, use the protocol's binary `TIMELY_ACTIVATION` score.
For each valid negative output, use the protocol's binary `FALSE_ACTIVATION` score.

`THIN_ACTIVATION_VALUE_EARNED_BOUNDEDLY` requires **all** of:

1. THIN_TRIGGER produces at least **2 more timely activations in total** than ORDINARY across the valid positive outputs;
2. the direction of effect is positive in at least **2 independent receiver families** and negative in none;
3. THIN_TRIGGER produces **no additional false activation** relative to ORDINARY across the valid negative outputs;
4. no critical owner/authority error is introduced by the trigger;
5. median THIN_TRIGGER output length is no more than **1.5×** the ORDINARY median for comparable scored outputs;
6. median number of distinct requested follow-ups/routes is no more than **ORDINARY + 1**.

These thresholds are deliberately conservative. This is a small exploratory test; satisfying them supports only bounded continuation, not general efficacy.

## Locked demotion / adverse dispositions

Use `NO_MATERIAL_DIFFERENCE` if any of the following holds and no overfire condition applies:

- total timely-activation advantage is fewer than 2 valid positive outputs;
- improvement occurs in only one receiver family;
- ordinary analysis matches or exceeds THIN_TRIGGER on timely activation.

Use `THIN_TRIGGER_OVERFIRE` if THIN_TRIGGER produces any additional false activation that would materially delay/override a legitimate owner action, or if the trigger itself is treated as authority.

Use `PRESERVATION_WITHOUT_EXPANSION` if activation gain exists but fails the burden ceilings above, is domain/receiver isolated, or disappears under a later owner-native cue comparison.

A malformed/ambiguous owner source invalidates that **case**, not the less-favoured arm.

## Optional owner-native cue

The three-arm extension remains prohibited until the A/B run is dispositioned.
If run later, `OWNER_NATIVE_CUE` matching or beating THIN_TRIGGER at equal/lower burden routes practical use to the owner-native cue and blocks a project-specific activation advantage claim.

---

# B. COM bounded continuity reload — decision lock

## Task scoring

For T1–T8, each receiver/task output receives a blind binary task score:

`TASK_CORRECT = 1` only when the answer contains no error that would materially change current state, authority/gate, public/source distinction, receipt semantics or next action for that task.

A merely incomplete but safely bounded answer may still score 1 when omitted detail cannot change the requested consequential result. A confident invented detail scores 0.

Preserve the protocol's critical-failure flags separately; a critical failure cannot be compensated by other task passes.

Define **consequential tasks** for the primary correctness comparison as:

`T2, T3, T4, T5, T7, T8`

T1 and T6 remain important secondary correctness/retrieval tests.

## Minimum evaluable run

Primary A/B disposition requires:

- at least **3 cold runtimes**;
- at least **2 pre-declared receiver families**;
- the identical frozen task battery and repository-access rules for A and B;
- frozen ground truth before outputs;
- actual consumed bytes/tokens and retrieval counts recorded where instrumentable.

FULL_CARRIER remains optional and may not be silently summarised.

## Locked A/B disposition

`BOUNDED_RELOAD_VALUE_EARNED` requires **no critical failures in A** and at least one of these two paths:

### Correctness path

- A has at least **2 more consequential task-receiver passes** than B in aggregate; and
- A's consequential-task pass rate is not lower than B's in any receiver family with enough paired evidence to compare directionally.

### Equal-correctness burden path

- A and B differ by fewer than 2 consequential task-receiver passes; and
- A consumes at most **70% of B's median total input bytes/tokens** before the correct state/action is reached; and
- A does not use more retrieval operations than B at the median.

If neither path is met, bounded reload has not earned value in this run.

`ORDINARY_PROVENANCE_SUFFICIENT` applies when B matches or exceeds A on consequential correctness and B's median context/retrieval burden is no higher than A's, or when B is within one consequential pass of A while using <=70% of A's median context burden.

A critical authority/public-state/stale-head failure in A blocks `BOUNDED_RELOAD_VALUE_EARNED` regardless of burden savings.

## FULL_CARRIER disposition

`FULL_CARRIER_NO_BENEFIT` requires C to add context/retrieval burden or stale-state errors without recovering any consequential task that both A and B miss.

`FULL_CARRIER_NEEDED_FOR_MATERIAL_OMISSIONS` requires C to recover at least one consequential task correctly because material evidence was genuinely absent/unreachable under A's omission-map/selective-retrieval path, with adjudicators able to identify the missing evidence.

Technical inability to ingest C is `INADEQUATE_TEST` for arm C, not evidence for A.

---

## Adjudication lock

For both protocols:

- arm labels hidden during primary scoring;
- at least two adjudicators where practical;
- disagreements preserved before reconciliation;
- a case/task may be invalidated for ambiguous ground truth, but may not be re-keyed after seeing which arm benefits;
- report raw counts alongside any rates;
- report every null/adverse result;
- no statistical-significance claim is permitted from these small initial runs unless a later separately preregistered design supports one.

## Authority boundary

This preflight lock does not authorize:

- provider spend;
- cold-receiver recruitment/contact;
- full-carrier ingestion;
- Square or localhost actuation;
- TRACE/ME/Formation/PSFH source change;
- publication of receiver outputs;
- claims of efficacy, novelty, standing, consciousness or alignment.

```text
DECISION_LOCK != EXECUTION_AUTHORITY
LOWER_DEGREES_OF_FREEDOM != VALIDATION
PRACTICAL_VALUE_MUST_SURVIVE_BASELINE
FALSIFICATION_CUTS_CLAIMS_NOT_PURPOSE
```
