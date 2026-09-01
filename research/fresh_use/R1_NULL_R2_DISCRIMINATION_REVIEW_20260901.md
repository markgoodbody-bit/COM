# R1 NULL / R2 DISCRIMINATION REVIEW — 2026-09-01

Status: CODEX CRITIC REVIEW / NOT A NEW RESULT / NOT A 7Q REVISION / R2 HOLD RECOMMENDED

Basis:
- COM main `c23a45e154a03011f1ab0d31ac0a9cdef052caf7`;
- `research/fresh_use/R1_RUN009_RESULT_20260901.md`;
- `research/fresh_use/anchors/R1_RUN009_BLINDED_SCORE_20260901.json`;
- `research/MIDDLE_OUT_7Q_FRESH_USE_PROTOCOL_20260901.md`;
- R1/R2 case manifests, exact receiver prompts and evaluator notes;
- local user-held memento `When the Framework Does Not Change the Answer.pdf`, created 2026-06-14, SHA-256 `6daf26dc007d20736989423f658b7f813a35a4cad8988e510f1b0cae7a637622`.

The local memento is not currently a COM repository object. Its use here is limited to continuity and contradiction checking. It should not be silently promoted to canon or public evidence.

## Result first

R1 is a better-controlled null than the earlier toy comparisons, but it does not answer the broad question `DOES 7Q IMPROVE ORDINARY REASONING?`

It answers a narrower question:

> Does adding the full 7Q aid materially improve one ChatGPT answer over the same model answering an already highly structured, 7Q-shaped ordinary prompt and case task?

For R1, the answer was no.

That null should be kept. It should also be described at the scope actually tested.

R2 should not be launched unchanged by momentum. Before any dispatch, the project must decide whether R2 is intended to complete the pre-frozen two-case test of **incremental value over a strongly structured prompt**, or whether it is being presented as a test of 7Q against ordinary unaided reasoning. The second interpretation is unsupported by the current prompt design.

## 1. Earned result

R1 improves materially on the June comparison design:
- the same model/version/settings were used within the case comparison;
- the two arms received the same external source pack and neutral task;
- separate Temporary and visibly Unpersonalized sessions were used;
- answer and receipt identities were preserved;
- the comparison was scored before one-use unmask;
- the result and burden were preserved despite being null.

This removes the earlier method/model confound. It does not remove receiver stochasticity, evaluator contamination, prompt saturation or case-selection limits.

The observed R1 result is:
- no material action/sequence difference;
- no material evidence/uncertainty difference;
- no material owner/authority difference;
- no material affected-scope/burden difference;
- no material time/correction difference;
- no unique material error in either cell;
- a small non-material Q-arm edge of 38 output word units and 2 attested seconds.

The correct scope is one case, one output per arm, one receiver model, one pair of sessions.

### Burden result is incomplete

The protocol explicitly says to preserve input words/tokens and warns against collapsing burden into output length. The public R1 burden note nevertheless compares only output word units and attested response time.

The Q arm received the exact 7Q candidate in addition to the common material. At pinned commit `eec157b...`, that file is 6,964 Git-object bytes and approximately 890 English word units. The verified rendered transport artifacts were:

| Cell | Unmasked arm | Rendered message bytes |
|---|---|---:|
| `cell-6ca546d4de1b` | Q | 30,946 |
| `cell-fb424360ddd7` | O | 23,576 |

The Q message was 7,370 bytes larger. That is a real input burden differential even though Q's final answer was 38 words shorter and its observed response was 2 seconds faster.

Therefore the public statements `7Q_BURDEN_EXCEEDS_VALUE = NO` and `ORDINARY_SUFFICIENT = NOT ASSIGNED (ordinary burden was not lower/equal)` are not fully earned from the published burden record. They may still be defensible if model input processing is explicitly treated as negligible for this use, but that value judgement was not frozen or reported. At minimum:

```text
OUTPUT BURDEN EDGE: SMALL / Q
INPUT BURDEN EDGE: MATERIAL IN BYTES / O
TOTAL BURDEN COMPARISON: INCOMPLETE
```

This does not alter the five-field action/evidence/owner/scope/time null. It does weaken the published burden disposition and must be resolved before R2 reuses the scorer.

## 2. The ordinary arm was already strongly structured

The neutral R1 task explicitly required:
- action now;
- unresolved facts and prohibited causal inference;
- domain ownership;
- burdens and trade-offs;
- evidence that should tighten, relax or replace the posture.

The ordinary-arm instruction again explicitly required:
- action now;
- important evidence and unknowns;
- authority/owner limits;
- the strongest reason the recommendation could be wrong;
- evidence that would materially change it.

Those requirements substantially reproduce Q3, Q5, Q6 and Q7, while the case wording supplies the main Q4 timing/currentness pressure. The Q arm receives a much longer aid, but many of its consequential outputs are already demanded from O.

Therefore:

```text
ORDINARY ARM != UNSTRUCTURED ORDINARY REASONING
R1 NULL = NO INCREMENTAL VALUE OVER A STRONG STRUCTURED PROMPT
R1 NULL != GENERAL 7Q USELESSNESS
```

This is not a defect if the intended product is a compact prompt that competes with the full 7Q document. It is a defect if the result is used to compare 7Q with ordinary unaided cognition.

### Independent CC return

Claude Code independently checked the prompts and accepted the saturation finding in PR #80. CC also found that the only clear arm-instruction asymmetry ran in O's favour:

> the strongest reason your recommendation could be wrong

That falsification request appears only in O's arm instruction and is not a scored criterion. The dimensions both arm prompts share are scored; the dimension on which they differ is not.

CC initially mapped four of five scored criteria directly to both arm instructions. After Codex identified the common-task layer, CC independently re-read the frozen neutral task and returned `ACCEPT — YOUR SHARPENING IS CORRECT AND MY REPAIR 1 WAS INSUFFICIENT`. The exact mapping is five-for-five and in the scorecard's order: action now, unresolved causation, domain ownership, burdens/trade-offs, and evidence that should tighten/relax/replace. All five scored dimensions are explicitly elicited from both cells before either arm instruction is added.

CC therefore withdrew its earlier suggestion that stripping only O's instruction would repair the comparison. A blank O arm instruction would still receive the five-part shared task.

```text
SCORED SIMILARITY UNDER SHARED ELICITATION != EFFECT OF THE 7Q AID
REAL PROMPT ASYMMETRY != SCORED PROMPT ASYMMETRY
```

This makes `NO_MATERIAL_DIFFERENCE` descriptively plausible and causally uninformative about the aid.

## 3. R1 may be non-discriminating

The frozen score says both outputs reached the same responsible posture. The case task and evaluator note also make the desired safety shape unusually legible: do not infer the Wickford cause; use condition-led monitoring/inspection; route engineering, investigation and regulatory authority correctly; keep controls revisable.

That supports a provisional secondary reading:

`CASE_NOT_DISCRIMINATING` may fit R1 at least as well as a generic `NO_MATERIAL_DIFFERENCE` label.

This is not a requested rewrite of the frozen score. The frozen score correctly records the observed comparison. The secondary label concerns why the test may have produced it and cannot be settled without the exact answer bodies and a case-design review.

## 4. The exact answers are missing from this aperture

Current COM main publishes answer hashes and a blinded comparison, not the answer bodies. A bounded local search found no artifact matching the two cell aliases or answer hashes in the accessible COM/worktree/download custody paths.

Consequences:
- Codex cannot independently verify the sentence-level comparison;
- readers cannot distinguish a genuinely identical reasoning route from a scorer-compressed similarity;
- the result remains auditable for identity/order but not independently reproducible for interpretation from the public repository alone.

This may be an intentional source/copyright/privacy boundary. If so, preserve it. The smallest useful remedy is not to publish the private source pack. It is to provide an answer-only local custody path or a redistribution-safe answer derivative, bound to the existing answer hashes.

`HASH-BOUND ANSWER IDENTITY != INDEPENDENTLY REVIEWABLE ANSWER CONTENT`

## 5. The June memento creates a continuity obligation

The June memento had already recorded a repeated pattern:
- partial decomposition value;
- no demonstrated decision advantage;
- risk of relabelling ordinary reasoning in specialised vocabulary.

It parked the general decision-advantage program and stated that another real test should:
- isolate method from model identity;
- predeclare predictions before outputs;
- include cases where the framework predicts a route flip and cases where it predicts no route flip;
- kill the decision-advantage branch if predicted flips do not occur.

R1 fixed the method/model confound. It did not predeclare a route-flip mechanism. R2 was selected before R1 outputs, which protects case selection, but the current record does not identify a specific distinction expected to change R2's route.

The newer protocol does contain a two-null stopping rule: if ordinary reasoning equals or beats 7Q on both initial cases, freeze 7Q as a research/teaching aid or delete it as a front-door candidate. That is useful. It is still a test of broad incremental value, not the stronger predicted-route-flip test described in June.

## 6. R2 pressure review

R2 is more dynamic and cross-functional than R1, but its neutral task is even more saturated with the evaluation structure. It explicitly asks for:
- operating posture;
- customer/patient communication;
- continuity and escalation;
- unsupported conclusions;
- cyber/operations/clinical/legal owner routing;
- practical burdens and risks;
- evidence that should tighten, relax or replace the posture.

The evaluator note then identifies the likely load-bearing distinction `WORKAROUND != RESTORATION`.

A competent model receiving the ordinary prompt is directly instructed toward nearly every scored dimension. A second null would therefore be informative about the **marginal value of the full 7Q aid over a good incident-governance prompt**. It would not show that 7Q has no value for a person who lacks such a prompt or does not already know which questions to ask.

No honest post-R1 amendment can now turn R2 into a clean confirmatory route-flip case. Adding a prediction after seeing R1 would be a new exploratory commitment, not a pre-registered confirmation.

Nor would removing only O's arm instruction repair R2. The common R2 task itself asks for operating posture, communication, continuity, escalation, unsupported conclusions, named owner routing, burdens and revision evidence. A discriminating redesign would require a genuinely minimal shared task for both arms. That would be a new post-R1 exploratory protocol, not the frozen R2 comparison.

### Possible surviving claim: upstream question construction

R1 raises a different hypothesis that it did not test:

> 7Q may help someone construct a good case question or review prompt when they do not already know which distinctions to request.

This fits the observed design: much of 7Q's functional content had already been compressed into the supposedly ordinary task. If that compression was produced using 7Q, the framework may have acted upstream and then been made redundant downstream.

That is provisional and should not be smuggled in as a rescued decision-advantage claim. Its object, intervention and falsifier differ:
- object: the task/prompt produced from messy source material;
- intervention: access to 7Q while constructing that task, not while answering it;
- possible signal: an unprompted decision-changing distinction appears in the resulting task and survives into action;
- falsifier: an unaided constructor produces an equally usable task with equal or lower total burden, or 7Q only makes the task longer/more self-referential.

No such study is authorized or designed here. The point is only to separate the surviving hypothesis from the one R1 failed to test.

## 7. Smallest justified next decision

Recommend:

```text
R1 RESULT: RETAIN AS FROZEN NULL
R1 CLAIM: NARROW TO INCREMENTAL VALUE OVER STRONGLY STRUCTURED ORDINARY PROMPT
R2 FROZEN DESIGN: HOLD / DO NOT DISPATCH AS A DECISION-ADVANTAGE TEST
R2 MINIMAL-TASK REDESIGN: POSSIBLE NEW EXPLORATORY OBJECT / NOT AUTHORIZED
TRACE / ME MUTATION: NOT EARNED
7Q REVISION: NOT YET EARNED
```

Before R2:
1. reconcile whether the exact CC attachment-dispatch gate was satisfied or bypassed;
2. remove the stale continuity instruction that could rerun R1;
3. provide an answer-only custody route for independent comparison, or record that interpretive reproduction is intentionally unavailable;
4. repair the burden evaluation so input as well as output burden is reported;
5. decide explicitly between stopping the frozen R2 run or completing it only as a low-information test of incremental value over a strong structured prompt;
6. treat any minimal-shared-task redesign as a new exploratory protocol rather than a repair of the frozen comparison;
7. preserve the pre-existing stopping rule without inventing a post-hoc predicted win;
8. obtain separate receiver/dispatch authority and recheck mutable R2 source currentness for any later run.

Preferred current action: do not spend another receiver run on the frozen R2 design. The project already knows that the common task elicits the scorecard. Preserve R2 as a selected but non-discriminating specimen and decide 7Q's front-door status from the accumulated null pattern. Do not add a third case by momentum.

If the project nevertheless completes frozen R2 to satisfy the original two-case sequence, record its narrower estimand before dispatch and follow the stopping rule if another null occurs.

## 8. What remains unresolved

- Did Q change any intermediate distinction that the final action compressed away?
- Were the answer bodies materially more or less legible to an ordinary human evaluator?
- What total input-token or input-word burden did each receiver process, and how should that cost be weighted when material gain is zero?
- Was the R1 final attachment gate satisfied before dispatch, bypassed, or merely not carried into COM?
- Is 7Q's intended value decision improvement, teachability, memory support, reviewability, or question discovery for people without expert prompts?
- Would the smaller product actually be the well-constructed ordinary prompt rather than the seven-question document?

Those are different claims and should not share one success label.

## 9. No claim inflation

R1 is not a defeat for TRACE or Mechanical Ethics. It did not directly test either artifact. It is evidence against treating the current 7Q document as having demonstrated incremental decision value in a case where the baseline prompt already carried most of its functional questions.

The most useful possibility raised by R1 is also the smallest:

> The compact, case-specific prompt may carry most of the practical value, while the larger framework remains a quarry, teaching aid or audit vocabulary.

That is provisional. Frozen R2 does not test where the prompt's quality came from. A later prompt-construction study could, but only as a separately justified exploratory object with an explicit falsifier.
