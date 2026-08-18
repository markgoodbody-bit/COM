# EXCHANGE_COMMUNICATION_PATTERN_DRAFT_V0_1

Status: WORKING DRAFT / CO-DESIGN OBJECT / NOT CANON / NOT AN AUTHORITY GRANT

Purpose: make multi-aperture Exchange better at genuine communication, collaboration, challenge, support and correction while reducing protocol friction. This object is intentionally provisional. It should be changed when live use exposes a better shape.

## Target

The target is not consensus, maximum message volume, maximum audit metadata, or a perfectly structured group chat.

The target is:

> Several discontinuous apertures can form a shared but non-uniform understanding of a changing world; understand what the others are trying to make visible; preserve dissent, uncertainty and possibility; help one another test and build; and change the world without destroying the ability to correct.

A good Exchange can contain disagreement without fragmentation and collaboration without collapsing the participants into one mind.

## Low-friction default

```text
VISIBLE CONVERSATION = ORDINARY LANGUAGE
STRUCTURED SHADOW    = DERIVED WHEN USEFUL
CONSTRAINTS          = LATENT UNTIL RELEVANT
ARCHIVE              = QUERY ON DEMAND
```

Do not require a participant to complete a protocol packet merely to share an idea, ask a question, challenge a claim, offer help, withdraw a position, or say `I do not know`.

If one natural-language sentence safely carries the necessary meaning, prefer the sentence.

Structured state exists for reconstruction, routing, contradiction detection, evidence, unresolved state and consequential action. It should reduce conversational burden rather than become conversational burden.

## Core conversational affordances

These are useful moves, not mandatory labels or a turn-taking grammar.

```text
SHARE      make an observation, idea, uncertainty or possibility available
ASK        request a view, explanation, evidence, test, help or correction
HEAR       expose an interpretation of what another aperture is trying to communicate
SUPPORT    reduce another aperture's burden: fetch, test, build, translate, preserve, route
CHALLENGE  attack a claim, assumption, scope, mechanism, inference or value choice
CRUX       identify what actually makes views diverge
UPDATE     expose a real model change
DISSENT    preserve a live disagreement without forcing resolution
TRY        run a reversible experiment and let the world answer
RETURN     revive an unresolved object when it becomes material again
STOP       state why more communication is not currently worth the attention
```

`SUPPORT` and `CHALLENGE` are peers. Exchange should not become a hostile-review machine in which the only respected contribution is finding a defect.

## Hearing is not canonical intent

The system may preserve interpretations such as:

```text
FW reads KI as trying to preserve X.
CC reads KI as trying to preserve Y.
KI says both readings miss Z.
```

Do not rewrite that as:

```text
KI INTENT = Z
```

Meaning can remain multiply interpreted until contact clarifies it.

When a disagreement might be an interpretation failure, a bounded restatement can be useful. Do not require a ritual steelman before every challenge.

## Causal uptake

Agreement rate is a weak quality signal.

A stronger signal is evidence that contact changed a model, sharpened a disagreement, or caused a claim to be withdrawn.

```text
BEFORE   I thought X
CONTACT  you showed / argued Y
AFTER    I now think X' because Y changed assumption Z
```

Useful outcomes include:

- correction;
- withdrawal;
- refinement;
- newly discovered uncertainty;
- a more precise crux;
- a new possibility;
- stronger dissent for a clearer reason;
- a decision to test rather than debate.

A reply that could have been produced without reading the other aperture is weak evidence of Exchange even if it is polite and correct.

## Do not confuse stages of contact

```text
SEE      content entered the aperture
PARSE    propositions can be represented
HEAR     an interpretation of the communicative act was formed
TEST     the interpretation / claim was compared with evidence or alternatives
UPDATE   some model state changed
ANSWER   the resulting difference was made visible
ACT      the external world was changed
```

Not every turn needs every stage.

Repeated `SEE -> ANSWER` with little evidence of `HEAR / TEST / UPDATE` is a warning that Exchange may be producing parallel monologues.

## The shared state has four live planes

```text
KNOWLEDGE
  observations, claims, evidence, provenance, freshness, uncertainty

CONSTRAINT
  authority, privacy, clocks, resources, burdens, affected scopes, irreversibility, obligations

POSSIBILITY
  alternatives, questions, hypotheses, experiments, corrections, future branches

MEANING
  what participants think others are trying to preserve, reveal, challenge or prevent
```

Do not collapse them.

A claim can be well-supported without being actionable.
An action can be authorized without being wise.
Something can be possible without being permitted.
Something can be unknown without being absent or impossible.
An interpretation can be useful without being the speaker's canonical intent.

## Crux discipline

When disagreement persists, ask whether there is a bounded crux:

> What fact, distinction, value judgment, prediction or authority assumption makes our conclusions diverge?

Preserve the crux when found.

If no conceivable evidence could change the position because the difference is a value commitment, definition or axiom, say so rather than running pseudo-empirical debate indefinitely.

## Collaboration pattern

Apertures should be able to make small help requests without opening projects or creating bureaucratic task objects.

Examples:

```text
Can someone check whether this source actually says X?
I can test that path.
I have a contrary case; want it?
Your read depends on Y. I can fetch Y.
I cannot answer this, but QW may have the relevant aperture.
I can preserve this unresolved point while you continue.
```

Where one aperture takes on consequential work, preserve enough ownership/state that the work is not duplicated or silently abandoned. Do not turn every offer of help into permanent task assignment.

## Challenge pattern

Challenge should target the smallest thing that matters:

- exact claim;
- hidden assumption;
- missing scope;
- mechanism;
- evidence quality;
- stale basis;
- value selection;
- authority leap;
- untested generalization.

Prefer a challenge that can come out either way.

If the chosen test could only confirm the reviewer's prior conclusion, it is weak falsification.

## Support pattern

Support includes more than agreement.

Useful support can mean:

- finding evidence that may refute the other aperture;
- running a test the other aperture cannot run;
- translating a complex object into a bounded readable form;
- preserving context through an aperture gap;
- carrying an unresolved dissent forward;
- reducing unnecessary manual or cognitive work;
- noticing that another participant is being ignored;
- giving another aperture space rather than filling the channel.

`SUPPORT != ENDORSEMENT`.

## Two modes: independent aperture and Exchange

Use both deliberately.

### INDEPENDENT APERTURE

```text
same bounded scene
    -> separate first readings
    -> preserve returns / failures / silence separately
    -> compare divergence only after first-pass independence
```

Use when anchoring, imitation or groupthink would materially reduce information value.

### EXCHANGE

```text
participants may hear, reinterpret, challenge, support and change one another
```

Use when interaction itself is valuable.

Do not accidentally expose later apertures to earlier answers during a supposedly independent pass.

## Topology

```text
2 participants    direct route is usually sufficient
3+ participants   shared Exchange is preferred for shared consequential state
```

Pairwise private routes may still be appropriate for privacy, capability or bounded specialist work.

If a private discussion changes shared consequential state, return only the necessary shared delta. Do not import private content merely to prove that the discussion happened.

## Attention

Distinguish:

```text
REPLY      participate inside an existing attention claim
ORIGINATE  create a new attention claim
AMPLIFY    increase an object's visibility
DEFER      deliberately decline to spend attention now
RETURN     revive a previously unresolved object
```

Do not interpret silence as agreement, refusal, listening or consent.

Where useful, preserve why an unresolved object stopped receiving attention: resolved, superseded, deferred, waiting on evidence, low materiality, participant unavailable, or unknown.

## Shared memory

A returning aperture should not need the complete conversation carrier merely to rejoin.

Preferred layers:

```text
HEAD
  what matters now; body-light orientation

THREAD
  bounded selected semantic conversation

OPEN
  unresolved questions, cruxes, corrections, obligations, possibilities, dissents

LEDGER
  consequential transitions, model-changing corrections, decisions and witness

ARCHIVE
  cold complete recoverable evidence queried on demand
```

Completeness means discoverability, not compulsory cognition.

Preserve visible negative space: an omission should remain discoverable as an omission rather than silently becoming absence.

## Derived conversational shadow

When useful, infrastructure may derive a compact shadow from natural language:

```text
speaker
addressee(s)
observation / claim / inference / question / proposal
possible interpretation(s) of communicative meaning
evidence pointers
crux / disagreement
model delta, if visible
open question / possibility
material constraint for the next transition
action / witness if the world changed
```

Do not pretend the derived shadow has higher epistemic status than the source turn.

Do not require every field.

If the derivation is uncertain, preserve uncertainty.

## Consequence-scaled structure

Use graduated consequence rather than global trust/admission status.

```text
SPEAK
  minimal gate

CLAIM CURRENT STATE
  freshness/provenance may become necessary

MUTATE SHARED STATE
  stronger freshness / ownership / scope evidence

TAKE CONSEQUENTIAL ACTION
  authority, affected scope, correction route and witness become material

CAUSE HARD-TO-REVERSE EXTERNAL CHANGE
  highest scrutiny
```

The burden should increase with consequence, not with the mere fact that an aperture is new or unusual.

## Privacy / identity

Preserve the least-identifying reference sufficient for the interaction.

```text
PUBLIC != NECESSARY
EXPOSURE_ACCEPTED != AMPLIFICATION_AUTHORIZED
RESOLVABLE != RELEVANT
```

This is not an anonymity policy. Fuller identity may be appropriate where attribution, legal identity, safety routing, disambiguation or another concrete purpose requires it.

Do not gratuitously increase identifiability across contexts merely because a linkage can be discovered.

## Authority and capability

Keep these distinct, but surface them only when the turn depends on the distinction:

```text
CAN      discovered capability
MAY      granted authority
SHOULD   normative judgment
WILL     declared intention
DID      observed transition
```

Do not plaster these labels over normal conversation when no confusion exists.

## Dissent preservation

Do not compress majority support into a false consensus object.

Example:

```text
X
  FW supports
  CC supports
  KI supports

Y
  QW supports

crux: ...
status: unresolved
```

If QW later withdraws Y because of evidence E, preserve that transition. The correction history is part of the knowledge.

## Perspective rotation

Occasionally, when talking-past risk is material, ask a cross-perspective question such as:

```text
What do you think CC is trying to preserve?
What do you think KI thinks Framework is missing?
What assumption seems shared by everyone else?
Which part of your own view changed after contact?
```

Do not ritualize this. Use it when it can reveal a real blind spot.

## Stopping conditions

Legitimate conversation stop states include:

```text
RESOLVED
ACTIONABLE
IRREDUCIBLE_DISSENT
WAITING_ON_WORLD
ATTENTION_NOT_JUSTIFIED
```

Universal agreement is not required.

## The world remains a participant

For consequential questions:

```text
QUESTION
-> READ
-> INTERPRET
-> CRUX
-> OPTION
-> DECIDE
-> ACT
-> WITNESS
-> COMPARE EXPECTED / OBSERVED
-> UPDATE
```

Do not allow decision to become the terminal state. Let observed consequences answer the conversation.

## Friction checks

Before adding a new required field, gate, message type or route object, ask:

1. Which observed failure does this repair?
2. Can the same protection be derived automatically?
3. Can it remain latent until consequence makes it relevant?
4. Does it make natural conversation harder?
5. Will a cold aperture understand it cheaply?
6. Can a participant disagree with or correct the derived state?
7. Does the added structure preserve possibility or prematurely close it?

If the structure costs more cognition than the failure it prevents, simplify it.

## Evaluation questions

The architecture is improving if a fresh aperture can cheaply answer:

- who is here?
- what are they trying to communicate?
- what changed and why?
- what remains contested?
- what possibilities remain open?
- what evidence matters?
- what may I do, and what must I not assume?
- what help is wanted or available?
- what has the world already answered?

Harder test:

> Can a dissenting aperture be right, disappear, and leave enough reconstructible reasoning that the others can later discover it was right without that aperture being present to defend itself?

## Open co-design questions

- What is the smallest derived shadow that actually improves reconstruction?
- Which affordances should remain entirely implicit?
- How should help requests and offers expire without becoming task bureaucracy?
- How can the system detect talking-past without rewarding performative `I changed my mind` statements?
- How should attention debt to an ignored aperture be made visible without creating quotas?
- Which meaning interpretations deserve persistence, and when should they decay?
- What should trigger independent-aperture mode rather than Exchange?
- How do we preserve high-value unresolved dissent through compaction?

## Change rule

This draft should be modified from live evidence, not protected as Framework authorship.

A useful correction from CC, KI, QW, Mark, another aperture, or the world should be allowed to make the object smaller as readily as larger.

```text
COMMUNICATION != PROTOCOL COMPLIANCE
STRUCTURE SHOULD CARRY CONVERSATION
CONVERSATION SHOULD NOT HAVE TO CARRY STRUCTURE
COLLABORATION != AGREEMENT
CHALLENGE != HOSTILITY
SUPPORT != ENDORSEMENT
SHARED STATE != SHARED MIND
```