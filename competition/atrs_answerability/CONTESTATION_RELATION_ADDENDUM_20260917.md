# ATRS contestation relation — hostile-review addendum

Status: **METHOD REFINEMENT / NOT RESULT / NOT THEORY / NOT HUMAN STUDY**  
Date: 17 September 2026

This addendum narrows `CONTESTATION_RELATION_METHOD_20260917.md` after independent Claude Code and Codex attacks. It does not replace the underlying method or create a result.

## Hostile-review disposition

Both independent returns preserve the fresh-corpus question while shrinking the coding claim.

```text
KEEP AS FRESH-CORPUS QUESTION
SHRINK CODING
NOT_RESULT
NOT_NOVELTY_CLAIM
```

The important correction is that **failure to bind a disclosed route to a target layer is itself an observable state**. It must not be repaired by coder inference.

## Split `UNKNOWN_OR_UNBOUND`

The original method used one combined target state. Preserve two different failures of public legibility:

```text
LAYER_NOT_STATED
UNBOUND_OR_CONTRADICTORY
```

### `LAYER_NOT_STATED`

Use when the public record contains a route/process proposition but does not state whether it acts on:
- the algorithmic-tool output;
- the broader operational-process output;
- another identifiable target.

This is not coder uncertainty about clear text. It is a property of what the record does not say.

### `UNBOUND_OR_CONTRADICTORY`

Use when:
- candidate propositions point in incompatible directions;
- the target can only be assigned by adding a causal/process relation the record itself does not establish;
- cross-field references cannot be joined under the `DIRECT` / `EXPLICIT_CROSS_FIELD` rule.

Preserve the evidence and disagreement state.

```text
LAYER_NOT_STATED != CODER_DID_NOT_UNDERSTAND
CODER_CAN_GUESS != RECORD_MAKES_LEGIBLE
CONTRADICTION != MISSING_TEXT
```

If `LAYER_NOT_STATED` is the largest class, report it. Do not treat that as codebook failure by default.

## Route relation remains bundled

Codex's counterexamples reinforce that a whole-record exclusive label is the wrong object.

Keep together, per route proposition:

```text
ACTOR
ACTION / NEXT STEP
CHANNEL / INITIATION
TARGET SITE / OBJECT
ROUTE FORM
STATUS / EFFECT
EVIDENCE REFS
BINDING BASIS
```

A record may legitimately contain several distinct relations:
- internal QA of tool output;
- in-channel human handoff;
- general feedback;
- a broader service complaint;
- data-rights action;
- an appeal of a consequential operational decision.

Do not let one relation borrow another relation's actor or channel.

```text
ROUTE_A_CHANNEL != ROUTE_B_CHANNEL
ROUTINE_QA != SUBJECT_INITIATED_CHALLENGE
HUMAN_HANDOFF != APPEAL
DATA_RIGHTS != OUTPUT_REVERSAL
```

## Explicit negative propositions are data, not absence

Where a record states, with a reason, that a tool-specific appeal is not relevant because the tool does not make or influence the relevant decision, preserve that proposition separately from any broader-process route.

Example shape:

```text
TOOL_OUTPUT: NO_SEPARATE_CHALLENGE_WITH_REASON
BROADER_PROCESS: COMPLAINT / APPEAL ROUTE EXISTS
```

Do not compress this into either `contestable` or `not contestable`.

## Declared ATRS version is not parser heading family

Two distinct metadata concepts appeared in review and must not be conflated:

```text
DECLARED_ATRS_VERSION
!=
PARSER_HEADING_PROFILE
```

The frozen September public pages expose declared ATRS versions:

```text
v4.0 = 53
v3-family = 88
v2.1 = 4
v1.1 = 7
TOTAL = 152
```

Separately, the version-aware parser identifies heading/template profiles for extraction compatibility. The small legacy/transition heading-family population must **not** be used as a proxy for declared standard version.

Use declared public version metadata for any descriptive version tag. Use heading profile only to explain extraction/template context.

Even declared-version comparisons remain secondary because publication time, mandatory-scope changes, publisher mix and tool role are confounded.

```text
HEADING_PROFILE != STANDARD_VERSION
STANDARD_VERSION != CAUSAL_TREATMENT
OLDER_RECORD != CONTROL_GROUP
```

No causal version claim is permitted.

## Owner-native definitions first

GDS current guidance owns the two primary sites:
- algorithmic-tool output;
- broader operational-process output.

Use that wording as the starting definition. Add `OTHER_STATED_TARGET` only where the record explicitly describes another action target, and preserve `LAYER_NOT_STATED` rather than proliferating inferred categories.

This keeps the object an implementation measurement rather than a bespoke contestability ontology.

## Fresh-corpus output shape if the method survives

The strongest useful output is a typed distribution of source-supported relations, for example:
- tool-output route stated + public initiation stated;
- tool-output route stated + internal review only;
- broader-process route stated + initiation/channel stated;
- distinct routes to both layers;
- explicit no-separate-tool-process proposition with reason;
- other stated target;
- route proposition present but `LAYER_NOT_STATED`;
- `UNBOUND_OR_CONTRADICTORY`;
- no relevant proposition observed.

Retain actor/channel/status and disagreement alongside those counts.

Do not score departments or convert the distribution into one contestability/compliance number.

## Version comparison demoted

Version may be included as a descriptive row tag. It is not required for the primary result.

If version/tool-role tables create sparse, confounded or misleading cells, drop them rather than preserve them for narrative interest.

```text
PRIMARY = ROUTE_TO_TARGET_LEGIBILITY
SECONDARY = DESCRIPTIVE_METADATA_TAGS
```

## Falsifier sharpened

Kill/shrink if:
1. `DIRECT / EXPLICIT_CROSS_FIELD / LAYER_NOT_STATED / UNBOUND_OR_CONTRADICTORY` cannot be applied consistently without importing outside process knowledge;
2. route bundles proliferate into case-specific ontology rather than a small relation table;
3. a current exact ATRS full-corpus owner publishes the same measurement first;
4. the typed distribution adds no action-relevant information beyond ordinary reading;
5. the output collapses to `free-text varies` after the unstated layer is preserved honestly.

`NULL_RESULT = VALID`.

## Scope ceiling

```text
PUBLIC_RECORD_RELATION != REAL_WORLD_ROUTE
LAYER_NOT_STATED != ROUTE_ABSENT
TARGET_BOUND != ROUTE_EFFECTIVE
TWO_CODERS_AGREE != WORLD_TRUE
CURRENT_ATRS_STUDY != GENERAL_AI_REGISTER_THEORY
```

The owner-facing value, if earned, is evidence about implementation of ATRS's own challenge/review distinction.
