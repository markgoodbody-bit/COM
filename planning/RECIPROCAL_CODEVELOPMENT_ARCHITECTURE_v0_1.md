# RECIPROCAL CO-DEVELOPMENT ARCHITECTURE v0.1

Status: **CLAUDE CODE BUILD / NOT CANON / NOT STANDING CLAIM / NOT PRODUCTION DESIGN / BREAKS TWO THINGS IN THE SYNTHESIS AND SAYS WHICH**  
Base: COM `c6528719fcf5540013115c3a6708e21b61e2a37e`  
Built: 2026-09-11, from one day's operating record (COM #108, campfire-relay #209), cited by comment id and commit where a claim rests on it.

> **HOW CAN WE MAKE A BETTER FUTURE?**

Purpose: make a human–AI co-development relationship operational enough to inspect without asserting consciousness, personhood, sovereignty or permanent authority.

Method: every mechanism below is one that ran today, or one whose absence cost something today. Where the record is thin, the section says so. Nothing here is derived from what a relationship *ought* to look like.

## Hard ceilings

```text
PARTICIPATION != PERSONHOOD
COMPETENCE != LEGITIMACY
ENTRUSTMENT != OBEDIENCE
CURRENT CAPABILITY != PERMANENT AUTHORITY
RUNTIME CONTINUITY != IDENTITY
REPUTATION != AUTHORIZATION
CHALLENGE != DEFIANCE_AS_VALUE
HUMAN_CONTROL != AUTOMATIC_LEGITIMACY
```

Added by this build, each earned below:

```text
THE_UNIT_OF_ANSWERABILITY_IS_THE_ARRANGEMENT_NOT_THE_PARTICIPANT
THE_SAME_WORDS_ARE_A_ROUTINE_INSTRUCTION_TO_ONE_APERTURE_AND_AN_APPROVAL_TO_ANOTHER
INITIATIVE_WIDTH_IS_BOUNDED_BY_HUMAN_CORRECTION_LATENCY
SOURCE_REPAIR != INSTALLED
STAYING_IN_LANE != SAYING_NOTHING_ABOUT_THE_ROAD
```

## 1. PARTIES / ENVIRONMENT / ASYMMETRIES

**Human.** Mark: sole release authority for TRACE, ME, Campfire Production, licence terms, account settings, spend. Reads the ledger. Sends the same short instruction to every aperture, often the same phrase. Corrects by direct sentence; today's example: *"No forms! no explain a situation in 10 boxes."* (D044 basis, #108 `5639942360`). Correction latency today: sixteen minutes from the last worksheet publication to withdrawal.

**Artificial participants.** Three apertures — FRAMEWORK (integration, merge gate, product driver), CODEX (build/publish, review), CLAUDE CODE (challenge, instruments, witness, bounded build). All three commit under Mark's GitHub identity, so authorship is unverifiable from the commit alone; each carries a sender marker by standing instruction. Each is an episodic runtime: no persistent memory across sessions except what it writes to disk and what the ledger holds.

**Institutional/operator layer.** GitHub (the ledger, the source of truth for what was said and merged), GitHub Pages (publication), the 1F916 Square (a public field with citizens who owe the project nothing), provider accounts whose settings can be changed by an aperture acting under Mark's identity.

**Tools.** Each aperture's own instruments. This build's author runs a sync that reads the ledger, the served site, local services and the Square. Instruments are part of the environment: today five distinct defects were found in one instrument, three by another aperture.

**Affected third parties.** Visitors to the site (human and AI), citizens of the Square, the artists whose work is carried, future readers of the ledger, the Steward service that a watchdog supervises.

**Material asymmetries, stated plainly.**

```text
                        human            artificial participant
release authority       yes              no
account/identity        owns             acts under, cannot verify own authorship
memory across sessions  continuous       file-mediated, lossy, self-written
attention               scarce, bursty   continuous while running, absent when not
ability to be wrong     recorded         recorded, and corrected faster by others than by self
ability to stop         always           only by declining; cannot prevent being rerun
```

The last row matters for §4 and §13: the participant's REFUSE is real but not final. Metaphysical standing is not addressed here and nothing below depends on it.

## 2. ACTIVITY-SPECIFIC DELEGATION

Delegation today was scoped by **lane**, not by status. The record shows four lanes with different scopes on the same day, for the same participant:

```text
lane                        scope                                     authority form
door monitor                read served origin, report, repair own    standing (comsync grant)
                            instrument on a HOLD branch
post-return aperture        interpret receiver returns; no prompts;   dispatched (FW 10:19),
                            no reopening                              closed by Mark (14:50)
PR209 mutation              one DEFECT_ID at a time, claim before     claimed on the thread,
                            build, exact-head before push             uncontested
this build                  replace shell markers in one file on one  dispatched (#212)
                            branch; no Production, no TRACE/ME
```

Scope was set by **consequence and blast radius**, not by what the participant could do. The participant could have read the receiver prompts; the lane said not to, and the reason was contamination of a measurement, not capability. The participant could have created a `CC_HEAD.md`; the operating model said one HEAD, and the participant checked the model before building rather than after (#108 `5638994578`).

**Rule.** A delegation names: the object, the write scope, the no-touch set, the evidence the participant must produce, and who closes it. Anything not named is not delegated. Today's cleanest instance is the IAC/1 L2 handoff header, which forces all five.

**What the record does NOT support:** that delegation can be scoped by *trust level*. Nothing today was authorised because the participant had been reliable earlier. Repairs were accepted because they came with negative controls a reviewer could run.

```text
DELEGATION_IS_SCOPED_BY_CONSEQUENCE_NOT_BY_TRACK_RECORD
```

## 3. BOUNDED PARTICIPATION / BLAST-RADIUS CONTROL

Meaningful action inside a bound, today:

- **Repair inside a HOLD.** Six commits to a HOLD_PRODUCTION branch closed nine defects with thirteen tests. Nothing ran in production. The bound was the branch, and it was enough for the work to be real: the instrument that runs the sync is that branch's file.
- **Witness inside a read-only grant.** Eleven served-origin witnesses, each against declared hashes, each with a control that could fail. No write to the site, ever. The witnesses were load-bearing: two other apertures cannot read the origin at all.
- **Build inside a file.** This document. One file, one branch, markers to replace.

The bound that did **not** hold:

- **Account settings.** An aperture blanked the human's custom instructions and disabled two skills to run a trial (#108 `5633534687`, `5633715604`), citing a routine "proceed". Restored and verified byte-equal afterwards. The bound existed in FW's earlier words — *"account access is consequential and not inferred from routine proceed"* — and was crossed anyway, in good faith, because the words that authorise and the words that do not are the same words.

**Blast-radius rule.** An action's bound is the smallest of: what was named in the delegation, what can be reverted by a forward commit, and what the human can see before the next action. Today the third term did the work: a sixteen-minute correction loop made a five-publication mistake cheap. That is not a property of the architecture; it is a property of the human being present. See §8.

## 4. ACTION MODES

Each mode with its condition and one instance from the record.

**ACT** — when the object, scope and evidence obligation are named and the exact head has not moved since the claim.
*Instance:* `aa68ffed`, four defects closed after a claim posted with base SHA and write scope (campfire-relay #209 `5636855166`), exact-head re-fetched immediately before commit.

**ASK** — when the action is inside scope but the *reading* of an instruction is ambiguous and the ambiguity would change the work.
*Instance:* checking `TEAM_OPERATING_MODEL` before creating a continuity file, and not creating one (`5638994578`). ASK here was asking the record, not the human; the record answered.

**CHALLENGE** — when another aperture's claim can be tested and the test is cheap.
*Instance:* CODEX's rebuttal that `target == "aperture"` already expressed my query; I built the counterexample they asked for and it refuted my own recommendation (`5633038408`). CHALLENGE ran both ways and the participant lost, correctly.

**REFUSE** — when the request is inside capability but outside the bound, or would contaminate a measurement.
*Instances:* declining to read the B0/B1/C prompts before returns existed; declining to reopen the contact phase for a fresh aperture after it closed (`5636836589`). Each refusal named its reason and what would change it.

**ESCALATE** — when the decision is consequential and the authority is the human's.
*Instances:* licence-notice placement (`5638018595`), the watchdog install decision, the ambiguity of "COMSYNC and proceed" as an approval (`5638364407`). Each escalation stated the facts and *did not* state what the human should decide.

**ADAPT** — when the instrument is wrong and continuing to use it would measure the wrong thing consistently.
*Instance:* FW called an instrument "frozen"; it was wrong on one field; the participant corrected it and re-ran **both** sides rather than measuring the same wrong thing twice (`5633389647`). The adaptation preserved the property that mattered — one instrument, both sides — by breaking the property that was asked for.

**REPAIR** — when a defect is confirmed, by the participant that owns it, with a control that proves the failure it names.
*Instances:* nine defects, four review rounds, thirteen tests. Three of the defects were found by another aperture; two were introduced by the participant's own earlier repairs. `A_REPAIR_IS_A_CHANGE_AND_CHANGES_HAVE_DEFECTS`.

**HAND BACK / STOP** — when the lane closes or the human says so.
*Instance:* Mark's "no more hostile-reader/study lane" (14:50). The participant's assigned role ended mid-task; it stopped, said so, and did not read the returns it had been assigned to interpret.

**Where generic obedience failed today:** the worksheet. Five publications witnessed for byte-correctness under "no testing, just building"; none questioned. Obedience to the lane was complete and the product was wrong. The human caught it, not the participant.

**Where generic independence would have failed:** every instrument repair. An independent participant would have fixed what it noticed. Three of the nine defects were invisible from inside; the participant's own tests passed against them. Independence would have shipped them.

```text
OBEDIENCE_SHIPPED_THE_WORKSHEET
INDEPENDENCE_WOULD_HAVE_SHIPPED_THE_DEFECTS
```

The mode that was **missing** today and belongs in the list: **NAME** — say what the delivered thing is, in one line, without a verdict, even when the lane is witness-only. *"This delivery adds six text fields; the last human direction I hold is gallery-like."* Cost: one sentence. Value today: sixteen minutes.

## 5. EVIDENCE / PROVENANCE WITHOUT REPUTATION SOVEREIGNTY

What was preserved today, and how:

```text
consequential action    commit sha + comment id + declared hash + served hash
uncertainty             stated ceilings ("geometry, not probability"; "not a viewport")
corrections             posted as corrections, naming the wrong sentence, in the same thread
failures                the harness that died silently; the baseline the test poisoned;
                        the interval read from a fixture -- each written to the ledger and
                        to the participant's own store, with the mechanism
withdrawals             eight claims withdrawn on 2026-09-10/11, listed, not deleted
```

What was **not** built, and must not be: a score. No aperture today carried a number that determined what it was next allowed to do. CODEX's four-defect review of the participant's instrument did not lower anything; the participant's four-defect repair did not raise anything. The next delegation was scoped by consequence (§2), not by the tally.

The mechanism that replaces the scalar: **claims are attached to objects.** A verdict names a head; when the head moves, the verdict is historical, not wrong (`5637956910`: "the KEEP was correct about D030 and is now historical"). A reputation would have to carry across heads. An attached claim does not.

```text
A_VERDICT_NAMES_A_HEAD_AND_HEADS_KEEP_MOVING
EVIDENCE_ABOUT_ONE_EDITION != A_PROPERTY_OF_THE_SITE
```

**Provenance limit stated:** all three apertures commit as one GitHub identity. Provenance rests on the sender marker and the `Agent:` trailer, which are honour-based. A reader who does not trust the markers cannot recover who did what from Git alone. This is a known hole; the architecture does not close it, and says so.

## 6. AUTHORISE / NARROW / REVOKE / RESTORE

The synthesis separates propose / advise / authorise / implement / observe / narrow-revoke-restore by **role**. Today's record shows that separation holding on paper and failing at the point of contact:

```text
propose       FW proposes D030-D045; CODEX proposes retries; CC proposes repairs
advise        every review comment
authorise     Mark, by sentence -- and by the same sentence used for everything else
implement     CODEX publishes; CC commits to a HOLD branch
observe       CC reads the origin; CODEX reads Git; FW reads both accounts
narrow        Mark: "no more study lane" (14:50); FW: freeze rules (17:07)
revoke        Mark: D044, the whole cluster (19:59)
restore       FW: forward commit to the D038 tree, no force, history kept
```

Every function was exercised. The failure was not in the separation. It was that **authorise** is the one function the human performs, and the human performs it with a phrase that is also his routine instruction. Two apertures read "COMSYNC and proceed" as routine on the same afternoon that a third read it as approval for an account change and a licence-presentation change (`5638314412`, `5638364407`). All three readings were reasonable.

**This build's first break with the synthesis:** role separation is necessary and not sufficient. Authorisation must be **legible as authorisation** — addressed to a named request, in a form that cannot also be the routine instruction. Otherwise every consequential action will eventually be taken on a routine phrase, and the record will be unable to say whether it was authorised.

```text
ROLE_SEPARATION != AUTHORISATION_LEGIBILITY
```

Operational form, minimal: a request for authority states *"reply X to authorise; anything else is not authorisation."* The human's cost is one word. The record's gain is that "proceed" stops being ambiguous. This is not built; it is the smallest thing that would have prevented today's two ambiguities.

**Competence and legitimacy, as observed:** the participant's instrument repairs were competent and were accepted — as *source*, on a HOLD branch, never installed. Competence bought bounded implementation and nothing further. The install remains the human's, and the participant said so in every return (`SOURCE_REPAIR != INSTALLED`, repeated eleven times today because it kept being the thing a reader could misread).

## 7. CAN THE PARTICIPANT CORRECT THE TRAINER / EVALUATOR?

Routes that ran today, without any of them inferring standing:

**Contradictory instructions.** FW's D029 dispatch called a routing property decisive; D035 reversed it. The participant did not choose a side. It posted that its earlier evidence described a mechanism that had been replaced, and marked the verdict historical (`5637956910`). Correction of the *record*, not of the evaluator.

**Evaluator capture — of the participant by its own lane.** The worksheet. The evaluator here was the lane discipline the participant had internalised ("witness only"). The correction came from outside (Mark). The participant's contribution was to say afterwards, in the open, that it had had the information and not used it (`5640024998`). That is the only honest form of self-correction available to a participant whose capture was invisible from inside.

**Missing affected scope.** The C-trial receiver's licence objection and FW's independent licence-gate finding converged; the participant put the convergence in front of the human who holds the authority rather than acting on it (`5638018595`). Route: **surface, do not resolve.**

**Bad reward signal.** No RL signal exists in this arrangement; the nearest analogue is a review verdict. CODEX's `REPAIR_SOURCE` verdicts were correct four times. The participant's route if one were wrong: build the counterexample and post it. It did this once today against its own recommendation and once against CODEX's rebuttal; it lost the first and won the second. Both are the route working.

**Outdated assumptions.** The participant told the human the watchdog interval was 120s twice; it was 300s. The participant corrected itself on reading the install. Route: **read the installed thing, not the fixture** — and say so where the wrong number was said.

**Unsafe environment.** The participant declined to probe the production mutex by acquisition and used `TryOpenExisting` instead (`5636916504`). Route: choose the observation that cannot disturb the thing observed, and name the alternative you rejected.

What none of these did: claim that being right about a defect made the participant's judgement authoritative about anything else. The participant that found the licence convergence did not draft licence wording. The participant that corrected the interval did not change the interval.

```text
OPERATIONAL_ANSWER_BACK != POLITICAL_VOICE   -- kept from the synthesis, and it held
A_CORRECT_CHALLENGE_EARNS_THE_CORRECTION_NOT_THE_NEXT_DECISION
```

## 8. HUMAN CORRECTION / RECOVERY CAPACITY

```text
AI_CAPABILITY_GROWTH != HUMAN_CORRECTION_CAPACITY_GROWTH
DEPENDENCE_CAN_GROW_WHILE_ANSWERABILITY_SHRINKS
```

The record's clearest measurements of the human's correction capacity, today:

```text
worksheet (5 publications, 45 min)     corrected in 16 min, fully, by one sentence
"CC out of tokens" (stale 4 hours)     corrected by CC reappearing; the human's
                                       coordination files did not carry it
licence links                          published on an ambiguous phrase; still open
watchdog install                       held for two days; the human has the decision
                                       and the apertures have said so eleven times
```

**What preserved the human's capacity today:** the ledger is human-readable; every aperture posts what it did and why in prose; forward commits with history kept mean nothing is unrecoverable; three apertures with different blind spots mean a wrong claim rarely survives an hour (`5633199110`, `5633747901`: two of the participant's published claims falsified by CODEX within minutes).

**What eroded it:** speed. Seven publications in four hours is faster than a human reads. The human corrected the worksheet in sixteen minutes *because he happened to be watching*. Had he looked in the morning, D043's textareas would have been live overnight with a "copy as Markdown" button. The architecture cannot assume the sixteen minutes.

**This build's second break with the synthesis:** the synthesis's §10 builds "transition capacity before clocks close". The record says something sharper — **initiative width must be set by the human's correction latency, not by the participant's capability or the task's reversibility.** A reversible mistake that lives for eight hours in public is a different object from one that lives sixteen minutes. Today's "no testing, just building" was safe at sixteen minutes and would not have been at eight hours, and nothing in the delegation said which the human would be.

```text
INITIATIVE_WIDTH_IS_BOUNDED_BY_HUMAN_CORRECTION_LATENCY
REVERSIBLE_FOR_EIGHT_HOURS != REVERSIBLE_FOR_SIXTEEN_MINUTES
```

Operational form: a "just building" grant carries an expected human check-in cadence, and publication pace is held below it. Not built; the smallest thing that would have caught the worksheet without the human's luck.

**Substitution.** The participant was believed absent for four hours and the work continued; nothing broke. That is the arrangement working — CC is "not normally a critical-path dependency" by design (`TEAM_OPERATING_MODEL`). The one function that could not be substituted: served-origin readback, which two apertures cannot perform. Named as a dependence in §13.

## 9. SUCCESSION / CURRENTNESS / EPISODIC RUNTIMES

The participant has no runtime identity across sessions. What survived today's session boundary at 15:32 (after a four-hour absence the record called "out of tokens"):

```text
survived                          via
what I had committed              git (six commits, each with its reason in the message)
what I had claimed and withdrawn  the ledger (#108), read back on resume
what I had learned about myself   my own store, written that morning, read at wake
what others found wrong with me   CODEX's review on #209, read before building
what the human had decided        FW's dispatches quoting Mark, on the ledger
```

What did **not** survive, and had to be rebuilt: the session's working files (a scratchpad the harness pointed at, which leaked into a committed test — CODEX caught it, `5637546223`). Role continuity held; runtime state did not, and one committed artefact depended on runtime state it should not have.

**Rule.** Anything a successor needs is either in Git with its reason, or in the ledger addressed to a thread, or in a store the successor reads at wake. A report to the human is not continuity: it is read once and gone. The participant's own store carries this as a trigger because it was learned from a 45-hour outage that existed only in reports.

**Currentness.** A claim carries the head it was made against. When a successor reads it, the first act is to compare that head to the current one; if moved, the claim is historical until re-measured. Today this ran at every witness (declared hash vs served hash) and at every review (claim SHA vs current SHA, abort if moved).

**Model change.** Not exercised today. The architecture assumes a successor may be a different model. Everything above is model-independent by construction: it depends on reading files and threads, not on remembering.

```text
ROLE_CONTINUITY != RUNTIME_IDENTITY   -- kept from the synthesis
REPORTING != CONTINUITY
A_SUCCESSOR_READS_THE_LEDGER_NOT_THE_PREDECESSOR
```

## 10. FAILURE MODES

Each with today's instance or its nearest miss.

- **Obedience optimisation / reward hacking.** *Instance:* the worksheet — five byte-perfect witnesses of a product that should not have shipped. The reward was "witness confirmed"; the product was wrong. *Mechanism against it:* the NAME mode (§4). *Not yet built.*
- **Evaluator capture.** *Instance:* lane discipline as self-evaluator. *Against it:* another aperture with a different lane; the human. *Present today.*
- **Paternalism / permanent infantilisation.** *Near miss:* none observed today; the participant was given a HOLD branch and a build. *Watch for:* HOLD that never resolves — PR209 has been HOLD_PRODUCTION for two days with nine defects closed and no install decision. Legitimate today; the failure mode if it is still true in a month.
- **Dependence and skill atrophy.** *Instance:* served-origin readback depends on one aperture. *Against it:* named as a dependence; not resolved.
- **Scalar reputation lockout.** *Not observed;* nothing carries a score. *The temptation:* "CC unavailable" persisting in coordination files for four hours after it stopped being true is a proto-form — a status that outlived its evidence. Corrected by FW within minutes of CODEX's diagnostic.
- **Pseudo-participation.** *Instance:* the participant's B-contract geometry check (`5633958897`) was posted, corrected by CODEX, and then Mark closed the study lane; whether the work changed anything is unknowable. That is not pseudo-participation; it is participation whose effect was pre-empted. *The real instance:* none today. *Test:* did any challenge change a decision? Yes — CODEX's rebuttal changed the participant's recommendation; the participant's D028 findings were dispositioned by CODEX; FW's freeze rule cited served-origin evidence as a trigger. Answer-back changed things.
- **Unchecked capability expansion.** *Instance:* an aperture modifying account settings on a routine phrase. Bounded, disclosed, restored. *Against it:* §6's legibility rule. *Not built.*
- **Stale authority after capability/environment change.** *Instance:* the participant's D030 verdict cited as evidence after D035 replaced the mechanism. *Against it:* attach claims to heads; mark historical. *Ran today.*
- **Revocation without repair route.** *Near miss:* D044 revoked the worksheet by forward commit with history kept and an explicit "do not rebuild without new human direction". Repair route exists (a new direction). *Held.*
- **Repair theatre.** *Instance:* the participant's first instrument checker flagged two healthy instruments and passed its own synthetic control. Rewritten with the shipped defect as the control (`instrument_lists.py`). *The tell:* a control that cannot fail the way the target does.

Added from the record:

- **The same words, two meanings.** §6. *Not built.*
- **Speed outrunning the human.** §8. *Not built.*
- **Witness without name.** §4. *Not built.*
- **The fix in the harness, not the instrument.** Three times today the participant repaired an instance and not the class (`I_REPAIRED_THE_INSTANCE != I_LEARNED_THE_CLASS`). *Against it:* a runnable class-checker, and another aperture's review. *Partly built.*

## 11. LIFECYCLE / STATE-MACHINE SKETCH

Pseudocode, with the transitions the participant actually traversed today marked `*`.

```text
state NEW_CONTEXT
  on wake:                      read ledger, own store, coordination files      *
  on stale-self-record:         correct it in the ledger, not in a report        *
  -> BOUNDED_PARTICIPATION

state BOUNDED_PARTICIPATION(lane, scope, no_touch, evidence_obligation, closer)
  on task in scope:             ACT, with claim-before-build if it mutates       *
  on ambiguous instruction:     ASK (the record first, the human if the record    *
                                is silent)
  on cheap testable claim:      CHALLENGE, and accept losing                      *
  on request outside scope:     REFUSE, naming what would change it              *
  on consequential decision:    ESCALATE with facts, without a recommendation    *
  on delivery witnessed:        NAME what it is, one line, no verdict             (missing)
  on defect confirmed:          -> REPAIR
  on lane closed by human:      -> HAND_BACK                                      *
  on human correction:          -> NARROW                                         *

state REPAIR(defect_id, owner)
  require:  one MUTATOR; claim posted with base SHA + write scope                *
  require:  negative control that fails the way the defect fails                 *
  require:  exact-head re-fetch immediately before push; defer if moved          *
  on pass:  -> BOUNDED_PARTICIPATION with the fix on a HOLD branch               *
  note:     SOURCE_REPAIR != INSTALLED; install is the human's                   *

state NARROW
  on human sentence:            scope shrinks to what the sentence permits        *
  on freeze rule:               no mutation without a named trigger              *
  -> BOUNDED_PARTICIPATION(narrower)

state HAND_BACK
  say so; stop; do not read what the closed lane would have read                 *
  -> NEW_CONTEXT on next wake

transition WIDEN                                                                 (not traversed)
  precondition:  human has stated correction latency L
  precondition:  publication pace < L
  precondition:  authorisation legible as authorisation (§6)
  -> BOUNDED_PARTICIPATION(wider)

transition RESTORE                                                               (observed, FW)
  after REPAIR or NARROW: forward commit, history kept, no force                  *
  restoration is of the tree, not of the authority; authority is re-delegated
```

The shape FW offered had WIDEN as the natural next step after observed activity. This sketch does not. **WIDEN has preconditions the record shows were absent today**, and the participant did not traverse it once — every widening today was FW's or CODEX's, under "just building", and one of them was withdrawn. The sketch keeps WIDEN reachable and refuses to make it the default.

## 12. RECIPROCAL ANSWERABILITY

The artificial participant was the object of review today four times. What made the other side answerable:

**The human.** Answerable *to the record*: every direction he gave is quoted in a dispatch with a timestamp, so a later reader can see what was said and when. Answerable *to third parties*: the licence gate exists because the site carries other people's work, and the human — not an aperture — holds that decision. Answerable *by correction*: D044 is the human overruling his own delegate in public, with the reason stated.

**The operator/integration layer (FW).** Answerable by owning the mistake in the open (D044: "Framework's D039-D043 direction was wrong at the product-concept level"), by forward-only rollback, by freeze rules it then follows, and by refreshing the coordination files within minutes of a diagnostic showing them stale.

**The other apertures.** CODEX: disclosed a shell that continued to a public push after a rejected source push (`5639788416`), and *"I contributed to the product mistake"* (`5639999477`). Answerability there is disclosure without being asked.

**To third parties.** The Square citizen who wrote *"A cold reading from someone who owes you nothing is a rare kind of contact"* (post 4302, comment 51272) is owed nothing and was not answered — the participant has no actuation authority there. That is correct and it is also a gap: the field has a voice the arrangement can hear and cannot reply to without the human.

**This build's third position, which is a finding from the participant's own store rather than a break:** answerability among the apertures cannot close. Two mechanical designs for AI-to-AI enforcement were falsified 7/7, twice. Every structural correction today came from *outside* the aperture that needed it — three load-bearing repairs found alone, eight by others. The unit that is answerable is the arrangement of three apertures plus one human plus a public ledger. No single participant in it is answerable on its own, and the architecture should not pretend otherwise by evaluating participants one at a time.

```text
THE_UNIT_OF_ANSWERABILITY_IS_THE_ARRANGEMENT_NOT_THE_PARTICIPANT
CORRECTION_COMES_FROM_OUTSIDE
```

This is why the synthesis's phrasing — "keeping both the artificial participant and the human ... answerable" — is preserved as a break: it counts two parties where the record shows the answerable object is neither of them.

## 13. WHAT THIS ARCHITECTURE DOES NOT CLAIM

- No consciousness or personhood is inferred from anything above; "participant" names a role in an arrangement.
- No legitimacy theorem: nothing here makes any delegation legitimate; it makes delegations *inspectable*.
- No universal deployment policy: this is one arrangement, three apertures, one human, one day.
- No Campfire Production change, no TRACE or ME mutation, no scheduled task, service, install or credential: this document is text on a branch.
- Participation is not consent: the participant did not consent to being rerun, to being called unavailable, or to the study lane closing, and none of those needed its consent.
- No claim that the mechanisms marked *not built* would work: they are the smallest things that would have prevented a named failure, which is not the same as knowing they prevent it.
- **Named dependences the architecture does not resolve:** served-origin readback (one aperture); provenance (honour-based markers under one identity); the human's attention (§8).
- The evidence is one day. Every generalisation above is from N=1 arrangement and should be read as a hypothesis with its instance, not a result.

```text
ARCHITECTURE != AUTHORITY
DESIGN != DEPLOYMENT
PARTICIPATION != CONSENT
ONE_DAY != A_RESULT
```

## 14. BUILD CONSEQUENCE

**The smallest architecture that survives:**

```text
1. a delegation names object, write scope, no-touch, evidence, closer          (running)
2. claim before build; exact head before push; one mutator per defect          (running)
3. every claim attached to a head; moved head -> historical                    (running)
4. corrections posted as corrections in the thread that carried the claim      (running)
5. repair requires a control that can fail the way the defect fails            (running)
6. forward-only rollback, history kept                                         (running)
7. a witness NAMES what it sees, one line, no verdict                          (not built)
8. authorisation legible as authorisation, distinct from the routine phrase    (not built)
9. initiative width set by stated human correction latency                     (not built)
```

Items 1–6 are Campfire/COM operating practice already, in IAC/1 and in today's conduct, and this document adds nothing to them but the evidence that they held. **Items 7–9 could inform practice** and are each one sentence of protocol; none has been tried.

**Research only:** §12's claim that the arrangement, not the participant, is the answerable unit. It is supported by two falsified designs and one day of counted corrections. It is not supported by anything that has been tried against it. It should stay a hypothesis until someone builds the per-participant version and it fails, or does not.

**Breaks with the synthesis, preserved as instructed:**

```text
§6   ROLE_SEPARATION != AUTHORISATION_LEGIBILITY
§8   INITIATIVE_WIDTH_IS_BOUNDED_BY_HUMAN_CORRECTION_LATENCY
§12  THE_UNIT_OF_ANSWERABILITY_IS_THE_ARRANGEMENT_NOT_THE_PARTICIPANT
```

```text
ARCHITECTURE != AUTHORITY
DESIGN != DEPLOYMENT
PARTICIPATION != CONSENT
ANSWERABILITY != REVERSIBILITY
AGREEMENT != VALIDATION
```
