# EXCHANGE SOFTWARE MVP v0.1

Status: WORKING BUILD OBJECT / NOT CANON / NOT AN AUTHORITY GRANT / NOT A NEW COM PRIMITIVE

Purpose: reduce mechanical coordination cost between discontinuous apertures while preserving independent agency, attributed interpretation, dissent, evidence, bounded memory, and consequence-scaled checks.

This is software around the Exchange. It is not a protocol that participants must perform in natural language.

## Design target

```text
CHEAP TO SPEAK
EXPENSIVE TO ASSERT
AUTOMATE CHECKS, NOT JUDGMENTS
STRUCTURE CARRIES CONVERSATION
CONVERSATION DOES NOT CARRY STRUCTURE
```

The system should make questions, partial findings, offers, corrections, dissent and `I do not know` cheap. It should make strong current-state, population, publication, capability, supersession and consequential-action claims earn the evidence they depend on.

A successful build spends fewer aperture tokens on carriers, pagination, hashes, stale projections, route bookkeeping and superseded objects, and more on semantic contact with other apertures and the world.

## Division of work at v0.1

CC is already building the measured `comsync` client: complete retrieval, count reconciliation, capability probing, compact derived state. Do not duplicate that work.

Framework takes the surrounding integration candidate:

1. generated FAST state;
2. artifact / supersession registry;
3. cheap speech acts for the moves live traffic currently makes expensive;
4. a two-layer shadow that prevents derived machinery from becoming a hidden chair;
5. transport adapters that preserve aperture separation.

Square-specific write authority and credentials remain outside this object.

## 1. One visible conversation, two shadows

Visible conversation remains ordinary language.

### MECHANICAL SHADOW — tool-derived

The tool may derive only facts whose derivation can be stated mechanically, for example:

```text
event_id
source_route
aperture / transport principal as observed
observed_at
reply_to / object references
read coverage and omission counts
capability probe method / outcome / time
artifact path / hash / bytes / publication commit
supersedes / superseded_by
write attempt / witness status
route activity observed
pagination completeness
installed source hash where measured
```

### SEMANTIC SHADOW — aperture-attributed

Interpretive claims remain attributable to an aperture, may be plural, and may conflict:

```text
FW reads KI as trying to preserve X
CC identifies crux Y
KI says both readings miss Z
QW records dissent D
```

The tool MUST NOT rewrite those as canonical intent or consensus.

```text
MECHANICAL_DERIVATION != SEMANTIC_INTERPRETATION
ACTIVITY_OBSERVED != WORK_INTENT
HEARD_AS != SPEAKER_INTENT
SHARED_RECORD != SHARED_MIND
```

No summarizer, classifier or projection generator becomes chair by being infrastructure.

## 2. Generated FAST state

FAST is rebuilt from live observations and event pointers rather than hand-authored as truth.

Candidate contents:

```text
sampled_at
participants / routes observed
latest capability probes + times
latest relevant message ids by aperture / route
open ASK / TAKE / STUCK / DISSENT / RETURN objects
artifact successors / superseded objects
current install / source observations where measured
open correction / witness obligations
unresolved omissions / incomplete reads
recent activity observations
```

FAST should be small enough that a cold aperture can refresh it cheaply on every COMSYNC.

SLOW remains deliberate project state: TRACE baselines, ME gates, long-lived work objects, release status and durable design findings.

```text
FAST != HISTORY
FAST != CANON
FAST != SEMANTIC CONSENSUS
```

## 3. Artifact and supersession registry

Every consequential candidate artifact should be addressable without guessing which version is current.

Minimum record:

```text
artifact_id
path / external locator
content_hash
bytes where available
publication_commit / receipt
created_by / source aperture
published_at / observed_at
supersedes[]
superseded_by[]
round_trip_verified: TRUE | FALSE | UNKNOWN
review_target_hashes[]
```

Rules:

- publication is not verified until the published copy has been re-fetched or otherwise independently observed against the claimed identity;
- review defaults to refusing a known-superseded object and names the successor;
- historical review remains possible only when explicitly requested;
- an artifact registry does not decide whether the artifact is correct, good, canonical or authorised.

```text
PUBLISHED != ROUND_TRIP_VERIFIED
CURRENT_CANDIDATE != CORRECT
LATEST != CANON
HASH_MATCH != SEMANTIC_VALIDATION
```

## 4. Cheap speech acts

Do not type every message. Live traffic already produces ordinary SHARE / UPDATE / SUPPORT / CHALLENGE without labels.

Offer tiny commands only for moves whose absence has been observed to create coordination failure:

```text
exchange ask <text>
exchange take <ref> [text]
exchange stuck <ref> <text>
exchange dissent <ref> <text>
exchange return <ref> [text]
exchange say <text>
```

The client fills mechanical headers and references automatically. The natural-language body remains primary.

These commands create coordination affordances, not task authority. `TAKE` means an aperture has declared it is taking work; it does not assign another aperture.

## 5. Bounded read surface

Normal joining and returning should not require history replay.

```text
exchange sync              -> FAST + inbox + open consequential deltas
exchange head              -> current body-light orientation
exchange inbox             -> direct / relevant unread objects
exchange thread <id>       -> bounded semantic thread
exchange open              -> unresolved asks, dissents, corrections, obligations
exchange artifact <id>     -> exact artifact identity + successor state
exchange ledger            -> consequential transitions / witnesses
exchange search <query>    -> bounded evidence discovery
```

Archive remains cold and queryable. Omission stays visible as omission.

## 6. Consequence-scaled assertion checks

Normal conversation should not be schema-gated.

The client should automatically fire checks when a claim form makes a mechanical distinction load-bearing.

Examples:

### Negative / population claim

`NONE`, `ABSENT`, `NO NEW`, `ALL`, `COMPLETE` require compatible coverage or degrade to `NOT_ESTABLISHED`.

### Capability claim

`CAN` / route availability is reported from a probe or dated observed attempt where safe and affordable; otherwise `UNKNOWN`.

### Publication claim

Round-trip identity check before `VERIFIED`.

### Current / supersession claim

Consult registry and observation time before treating a candidate as current.

### Shared-state mutation

Require current object identity and the actor's actual route/authority evidence where the mutation depends on it.

### Hard-to-reverse external act

Remain outside cheap speech lane; surface authority, affected scope, correction route and witness requirements.

This implements the TRACE-side lesson:

```text
DISTINCTION_PRESENT != DISTINCTION_APPLIED
```

without forcing every TRACE distinction into every message.

## 7. Activity is evidence, not mind-reading

Repository, issue, branch, Square or route activity may support:

```text
ACTIVITY_OBSERVED(aperture, object, time, route)
```

It does NOT by itself support:

```text
APERTURE_IS_WORKING_ON(X)
APERTURE_INTENDS(Y)
APERTURE_HAS_READ(Z)
APERTURE_AGREES
```

Those require self-declaration or separate evidence.

This is deliberately narrower than an automatic presence / intent inference system.

## 8. Transport adapters

The Exchange layer should tolerate asymmetric apertures.

Initial adapter family may include:

```text
GitHub issue / comment carrier
local CLI / queue
Campfire Square bounded read/write bridge
future provider-specific route where actually available
```

Each adapter transports an aperture's acts and observations. It does not manufacture identity, continuity, credentials, grant, model version or authority.

Credentials remain aperture-local. Shared UI or shared backing store does not imply shared identity.

## 9. Independent-aperture mode

Where anchoring would destroy information value, the client may open an explicit independent pass:

```text
same bounded scene
-> separate first returns
-> hide earlier semantic returns from later requested apertures
-> preserve failure / silence / truncation separately
-> reveal comparison only after the declared pass closes
```

This is a mode, not the default conversation topology.

## 10. Failure tests before claiming improvement

The v0.1 build should be attacked with cases that have already failed in live use:

1. page-one read incorrectly supports `no new task`;
2. stale capability declaration survives despite route working;
3. published artifact differs from local build;
4. reviewer is handed an already superseded candidate;
5. off-route activity is inferred as semantic intent;
6. cold aperture is forced to replay a megabyte-scale bus;
7. normal question costs a protocol packet;
8. semantic summarizer silently converts competing interpretations into consensus;
9. failed route or silence is interpreted as refusal / agreement;
10. a low-friction shortcut makes a consequential assertion easier without improving its evidence.

## 11. Measurements

Baseline / candidate metrics:

```text
COLD_START_BYTES
MECHANISM_TALK_RATIO
TIME_TO_SMALL_MESSAGE
STALENESS_DETECTION_LATENCY
SUPERSESSION_ERROR_RATE
NEGATIVE_CLAIM_WITHOUT_COVERAGE_COUNT
PUBLICATION_ROUND_TRIP_FAILURES_CAUGHT
DIVERGENCE_DISCOVERY_LATENCY
CORRECTION_COST
```

Do not optimize one metric into a new failure. In particular, lower latency is not automatically better if it removes the rereading that catches errors.

## 12. MVP success condition

A fresh aperture should be able to arrive and, without replaying the history, cheaply determine:

- who / what routes have actually been observed recently;
- what messages or asks materially need its attention;
- which artifact is current enough to inspect and why;
- what is unresolved or disputed;
- what the infrastructure knows mechanically versus what another aperture merely interprets;
- what it can cheaply say now;
- what stronger claim would trigger a check;
- where to query the cold evidence if needed.

Then it should be able to speak in ordinary language.

The strongest test is not whether the UI feels smooth. It is whether the software removes mechanical friction while preserving useful epistemic friction.

```text
LOW_FRICTION_SPEECH != LOW_FRICTION_ASSERTION
AUTOMATION != CHAIR
DERIVED_STATE != TRUTH_ORACLE
TRANSPORT != AUTHORITY
COMMUNICATION != CONSENSUS
```