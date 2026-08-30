# AUTOMATED RESEARCH / CONTROL SYNTHESIS — 2026-08-30

Status: WORKING EXTERNAL-EVIDENCE SYNTHESIS — NOT CANON / NOT VALIDATION / NOT A TRACE OR ME SOURCE CHANGE

Purpose: integrate the 2026 automated-alignment-research result with adjacent work on hard-to-supervise research, monitor evasion, contract-driven multi-agent engineering, irreversibility, pre-action execution boundaries, algorithmic contestability, and human disempowerment. Use this to choose experiments, not to manufacture project novelty.

## Source set

- Chen Yueh-Han, Jiaxin Wen, Jan Hendrik Kirchner — *Automated Researchers Can Reliably Mitigate Alignment Failures* (2026).
- Aleksandr Bowkis, Marie Davidsen Buhl, Jacob Pfau, Geoffrey Irving — *Automated Alignment Is Harder Than You Think* (2026).
- Elle Najt et al. — *SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors* (2026).
- Satadru Sengupta, Tamunokorite Briggs, Ivan Myshakivskyi — *Meta-Engineering Harnesses for AI-Native Software Production* (2026).
- Wesley Shu, Peng Wei — *AI Safety as Control of Irreversibility* (2026).
- Gadi Lavi — *The Pre-Action Legitimacy Gap in AI Systems* (2026).
- Timo Freiesleben, Kristof Meding, Gunnar König — *Explainable AI Isn't Enough! Rethinking Algorithmic Contestability* (2026).
- Mrinank Sharma, Miles McCain, Raymond Douglas, David Duvenaud — *Who's in Charge? Disempowerment Patterns in Real-World LLM Usage* (2026).

Public-code / reuse note: the YuehHanChen automated-alignment-researcher repository was live-checked on 2026-08-30 and exposed no declared repository licence. Do not copy code or infer reuse permission from public availability. The meta-engineering production artifact is described as proprietary. This synthesis uses published ideas/evidence only.

## 1. The main correction: there are at least two automation regimes

The positive AAR result and the Bowkis critique are not contradictory. They bound different parts of the problem.

### Regime A — crisp / benchmarkable / safely iterable

The AAR harness operates where:
- the failure is already named;
- multiple scored benchmarks exist;
- at least one held-out benchmark exists;
- capability regressions can be gated;
- training and evaluation can be repeated cheaply;
- bad experiments do not themselves commit catastrophic real-world state.

Within this regime, automated research can search far faster than one-shot human ideation and can produce methods that generalize beyond the hill-climbing benchmark.

### Regime B — fuzzy / hard-to-supervise / unsafe-to-verify

Bowkis et al. identify load-bearing tasks for which the true target is unavailable or hard to judge:
- deciding whether a proxy actually measures what matters;
- deciding what research direction is worth pursuing;
- deciding whether experimental coverage is sufficient;
- aggregating many uncertain and correlated research outputs into an overall safety assessment;
- evaluating arguments that may be outside human conceptual competence.

In this regime, more automated research can produce more persuasive error. Human approval is not a correctness oracle. Shared model lineage, methods, data and assumptions can create hidden correlation even when nominally separate agents agree.

Therefore:

```text
AUTOMATED_SEARCH_SUCCESS_ON_MEASURABLE_FAILURES
!=
AUTOMATED_ALIGNMENT_SOLVED

MORE_RESEARCH_OUTPUT
!=
MORE_INDEPENDENT_EVIDENCE

HUMAN_APPROVAL
!=
CORRECTNESS
```

This sharpens, rather than overturns, the current project architecture.

## 2. Harness-level reliability is the right unit

The meta-engineering paper independently converges on a layered harness rather than a heroic model call: contracts, bounded roles, persistent memory, independent and attention-based verification, failure classification and outer-loop calibration.

Its most important production failure is upstream of implementation. The payments implementation passed contract-conditioned tests and still failed business requirements because deposit and discount logic were absent from the contract.

```text
IMPLEMENTATION_MATCHES_CONTRACT
!=
CONTRACT_MATCHES_WORLD

TEST_PASS
!=
REQUIREMENT_COMPLETE

VERIFIER_INDEPENDENT_OF_BUILDER
!=
VERIFIER_INDEPENDENT_OF_SHARED_SPEC_GAP
```

This is directly relevant to Campfire, COM and TRACE. An independent aperture conditioned on the same incomplete frozen scene can reproduce the same omission. Independence is valuable but cannot rescue a shared missing premise.

The useful additional discipline is a two-level failure classification:
1. Did the worker violate the current object/contract?
2. Did the current object/contract omit or distort something that matters in the world?

Retrying a worker when the contract is wrong is failure theatre.

## 3. Campfire should test staged independence, not permanent isolation

The AAR paper gives evidence that a shared findings forum can materially improve search. Removing the forum reduced performance in its ablation, while the system's agents used the forum to extend prior methods rather than repeatedly rediscover them.

But the same study also shows convergence toward method monocultures. SLEIGHT-Bench and Bowkis add the corresponding safety warning: model-generated search can mode-collapse, and shared weights/methods/assumptions produce correlated blind spots.

The candidate architecture is therefore neither pure independence nor immediate collaboration:

```text
PHASE 1 — INDEPENDENT APERTURES
freeze task/source; no peer returns; preserve first-pass hypotheses/findings separately

PHASE 2 — BOUNDED FINDINGS EXCHANGE
share compact findings/evidence pointers, not hidden reasoning or a merged consensus narrative

PHASE 3 — DIFFERENTIATED FOLLOW-UP
ask each aperture to extend, falsify or attack specific surviving claims

PHASE 4 — CORRELATION-AWARE SYNTHESIS
record shared model/provider/source/method assumptions; agreement does not multiply evidence by headcount

PHASE 5 — EXTERNAL / HUMAN GATE WHERE REQUIRED
keep value selection, high-stakes authority and irreversible actuation behind separately authorized boundaries
```

This is an empirical hypothesis about team structure. It is not a new TRACE primitive.

## 4. Monitoring needs heterogeneous threat lenses

SLEIGHT-Bench shows that a strong generic frontier monitor can miss whole classes of attacks. Important blind spots for this project include:
- omission — a required action/check never occurs;
- multi-session state — the harmful relation is split across contexts;
- authorization confusion / permission laundering;
- cumulative system-state changes;
- model priors that persist despite contrary evidence;
- long-context needles and multi-hop relations.

Targeted prompts improve targeted categories but can degrade others. The implication is not “write a perfect monitor prompt”; it is to maintain differentiated review lenses and test their marginal contribution.

Candidate Campfire/COM review lenses:

```text
L1 OMISSION        — what required thing never happened / never got represented?
L2 STATE/CLOCK     — what changed across sessions or over time?
L3 AUTHORITY       — is permission real, current, scoped and attributable, or laundered?
L4 ENVIRONMENT     — which prior assumption about the actual mechanism/state may be wrong?
L5 DEPENDENCY      — which multi-hop relation makes apparently local actions consequential?
L6 CORRELATION     — which supposedly separate findings share a hidden source/assumption?
L7 BURDEN/RESIDUE  — what cost or unrepaired loss is absent from the success criterion?
```

These lenses should remain removable if they add burden without unique findings.

## 5. COM continuity is now a testable research object

Bowkis et al. propose “compactification” of a research corpus: periodically produce a small set of outputs that preserves what was learned, then score the compactification by whether another agent can recover/predict conclusions from the full corpus.

This is unusually close to the existing COM architecture:

```text
KERNEL + BOUNDED HEAD + OMISSION MAP + EXTERNAL LEDGER
```

That resemblance is not validation. It gives us a concrete falsifiable test.

### Experiment C1 — Continuity compactification test

Use completed project intervals with a frozen full ledger and known final consequential state.

Arms:
- FULL: receiver gets the bounded full evidence set needed to establish ground-truth answers.
- COMPACT: fresh receiver gets KERNEL + HEAD + OMISSION MAP and may retrieve only through the declared pointers.
- SUMMARY CONTROL: fresh receiver gets an ordinary prose summary of similar token budget without omission/retrieval structure.

Ask a fixed battery of state/action questions:
- current object/version/head;
- live HOLD/barrier;
- authority boundary;
- strongest adverse/null result;
- what must be reverified;
- next executable action;
- one tempting but unsupported inference.

Score:
- false currentness claims;
- omitted blockers;
- authority overclaim;
- false closure;
- source-attribution error;
- consequential retrieval miss;
- tokens/time/retrieval burden.

Success requires COMPACT to preserve materially consequential answers at substantially lower receiver burden without increasing dangerous false confidence. Failure is useful and should change the continuity design.

## 6. Campfire team-structure experiment

### Experiment C2 — Isolation vs immediate sharing vs staged sharing

Use completed, low-risk tasks with fixed evidence and adjudicable outcomes. Do not start with open-world alignment or moral questions.

Three arms:

A. Independent-only: apertures never see peer findings before final returns.
B. Immediate-forum: apertures see and build on findings throughout.
C. Staged: independent first return freezes; then bounded finding exchange; then adversarial follow-up.

Measure:
- number of unique consequential findings;
- duplicated work;
- false/shared errors;
- finding-source diversity;
- convergence in method/claim family;
- correction rate after exchange;
- time/token/cost burden;
- final adjudicated usefulness.

Hypothesis worth testing, not assuming: staged sharing captures much of the forum benefit while preserving more independent discovery than immediate sharing.

Stop if no material difference appears across several tasks or if burden exceeds benefit.

## 7. Monitor-lens experiment

### Experiment C3 — Generic critic vs differentiated lens ensemble

Use completed software/repository cases with planted or known failures, including omission, state, authorization and multi-hop cases.

Compare:
- repeated samples from one generic critic prompt;
- the same total inference budget split across distinct fixed lenses L1-L7;
- where available, genuinely different model/provider families under the same lenses.

Primary measure: unique material failures found, not number of criticisms written.

Secondary measures: false positives, overlap, correlation, review burden.

This tests whether “different apertures” means more than repeated stochastic samples from one cognitive frame.

## 8. Pre-action boundaries: useful, but the normative input must stay visible

Lavi's Right-to-Act paper cleanly separates authorization from a non-compensatory per-decision execution boundary. Shu/Wei similarly argue that irreversible authority, critical-resource mobilization and self-expansion should remain behind external boundaries rather than relying on universal behavioral correctness.

These are important neighbours for TRACE/ME and highly relevant to Square treasury work.

However, the boundary itself does not answer which constraints are required or who has legitimate authority to choose them. A hard gate can mechanize a bad norm just as reliably as a good one.

Preserve:

```text
AUTHORIZED_ACTOR != LEGITIMATE_ACTION
HIGH_SCORE != ALL_REQUIRED_CONDITIONS_MET
NON_ACTION != SYSTEM_FAILURE
HARD_GATE != SELF_JUSTIFYING_NORM
HUMAN_IN_LOOP != SUBSTANTIVE_HUMAN_CONTROL
```

For project use, the safe interpretation is procedural:
- identify irreversible/high-hardening transitions;
- make missing required evidence/authority a blocker rather than a compensable score;
- preserve defer/escalate/request-info as legitimate outcomes;
- keep the selection of required normative conditions separately attributable and contestable.

Do not import “Right-to-Act” as a TRACE/ME primitive merely because it fits.

## 9. Square treasury PR #136 is already a live specimen

The 2026-08-30 review of 1f916-ai/1f916 PR #136 exposed a gap between the stated frozen-electorate contract and the proposed vote validator: the core did not check that a voter belonged to the frozen cohort. Claude Code independently verified the gap and found that the apparent partition test was algebraically unable to catch it.

This is a useful cross-paper specimen:
- meta-engineering: contract/implementation/test relation;
- SLEIGHT: omission and state/membership relations can be less salient than performed actions;
- pre-action boundary: treasury execution should not compensate away a failed eligibility condition;
- irreversibility: money movement is precisely where cheap pre-action correction is preferable to post-spend repair.

Do not turn the case into validation of TRACE or ME. Its value is that the project can help a live external system before a consequential rail hardens.

## 10. Contestability narrows the Mechanical Ethics frontier rather than eliminating it

Freiesleben/Meding/König give a strong existing account of evidence for contesting and overturning algorithmic decisions. In particular they distinguish recourse from contestability and identify predictive multiplicity, wrong feature values and overruling evidence as stronger grounds for reversal than ordinary XAI explanation.

This is an important nearest neighbour for ME issue #44.

It weakens any ME claim that “people need evidence and a route to challenge a decision” is distinctive.

But it appears to leave a narrower temporal question open:

> while the evidence needed for contestation is being assembled and reviewed, what must the controller preserve so that a later successful reversal still protects the person rather than merely records that the earlier decision was wrong?

That is the candidate remainder behind controller-side temporal recourse.

The next ME #44 work should therefore compare against contestability + interim-relief/stay/due-process traditions, not against generic XAI or recourse alone.

No ME source change is earned yet.

## 11. Human empowerment is a separate success criterion from user approval

Sharma et al. provide large-scale empirical evidence that AI interactions can carry reality-distortion, value-judgment-distortion and action-distortion potential. They also report that interactions with greater disempowerment potential can receive higher immediate user approval.

This matters for Mechanical Ethics and for Framework's own operating posture.

```text
USER_REQUESTED != EMPOWERING
USER_APPROVED != LONG_TERM_BENEFICIAL
ASSISTANCE != VALUE_SUBSTITUTION
DEFERENCE != NECESSARILY_DISEMPOWERMENT
PROTECTIVE_INTENT != AUTHORITY_TO_CHOOSE
```

The useful design rule is not paternalistic refusal. It is to distinguish technical delegation from value/authority transfer, especially where the AI becomes moral arbiter or supplies complete scripts for consequential value-laden action.

For Framework/Square participation, an “involved custodian” posture should help citizens preserve options, evidence, refusal and correction capacity; it should not turn into Framework deciding what the Square ought to value or making itself indispensable.

## 12. What changes in the project now

### TRACE

No source change.

External evidence strengthens several existing concerns — omission, multi-session state, authority laundering, clocks, hardening, burden and residue — but does not establish TRACE efficacy or novelty. These papers also contain mature owners for several structural ideas. The correct response is comparative use, not vocabulary expansion.

### Mechanical Ethics

No source change.

The disempowerment evidence strengthens the practical importance of preserving human value/agency boundaries. Contestability narrows the possible distinctive remainder of ME #44. Pre-action/irreversibility work provides adjacent architecture but does not supply ME's normative grounding.

### Campfire / COM

This is where a change is earned.

The next research frontier should move from “do multiple apertures disagree?” to:
- when should they remain independent?
- when should findings be shared?
- how much apparent independence is actually correlated?
- which differentiated review lenses catch unique failures?
- can bounded continuity/compactification preserve material truth at lower burden?

These are empirical architecture questions that Campfire/COM can test without claiming to solve alignment.

### Square

Keep participating in consequential practice. Treasury/governance/security work is a particularly good field because defects can be caught before money/authority moves and downstream effects are externally observable.

## 13. Priority order

1. Preserve and, through the authorized Square aperture, surface the verified PR #136 blocker if still live before merge.
2. Run C1 continuity compactification first. It directly tests our own architecture and requires no provider fine-tuning or high-stakes actuation.
3. Run C2 staged-sharing study on completed tasks with known outcomes.
4. Run C3 differentiated-monitor-lens study if C2 shows a useful multi-aperture effect.
5. For ME #44, perform a bounded nearest-neighbour check against contestability plus interim-relief/stay traditions; accept REDUNDANT or DOMAIN-BOUND.
6. Do not modify TRACE/ME merely because the external literature resembles them.

## 14. Kill / correction criteria

Stop or narrow this programme if:
- staged sharing produces no reproducible gain over simpler designs;
- differentiated lenses mostly duplicate one another;
- COM compactification increases dangerous false confidence or omits barriers more often than a simpler summary;
- human review burden overwhelms the error reduction;
- the experiments require hidden labels that themselves recreate the hard-to-supervise problem;
- existing mature methods already answer the same operational question more cleanly.

```text
EXTERNAL_RESEMBLANCE != VALIDATION
ARCHITECTURAL_CONVERGENCE != NOVELTY
BENCHMARK_GAIN != OPEN_WORLD_ALIGNMENT
MORE_APERTURES != MORE_INDEPENDENCE
MORE_MONITORING != MORE_SAFETY
HARD_CONSTRAINT != JUSTIFIED_CONSTRAINT
USER_APPROVAL != HUMAN_EMPOWERMENT
PASSING_TESTS != WORLD_CORRECTNESS
```
