# TRACE NEAREST-NEIGHBOUR AUDIT — 2026-08-30

Status: BOUNDED COMPARATIVE AUDIT — NON-CANON / NOT VALIDATION / NOT A SOURCE CHANGE

Purpose: test what, if anything, TRACE adds after established neighbouring
methods reclaim the problems they already know how to handle. This is a
falsification exercise, not a search for flattering precedents.

## 1. Exact objects and reading limits

TRACE was anchored at public `main` commit
[`46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b`](https://github.com/markgoodbody-bit/TRACE/tree/46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b):

- `README.md`: 6,563 bytes, 152 physical lines, SHA-256
  `2af757c5f819abeda0f5051bc9cc518c9605b47b77ea4d102276dd582615880d`;
- `TRACE-SPINE.md`: 25,795 bytes, 643 physical lines, SHA-256
  `9ee106e98a34643929f82fa3296adffac46e650e4e8d0b775016269f0fe50999`;
- `TRACE.md`: 180,511 bytes, 6,547 physical lines, SHA-256
  `1dfc668d3e3dc5d85dcfc8bed5a025672025aff3ce157205b55bbc5f54160a1f`.

The README and spine were read completely. The full reference was inspected
by structure and by targeted readings of the sections bearing on liveness,
routes, clocks, correction feasibility, burden, residue, record custody,
packet use, worked transfer, hostile compliance and misuse guards. It was not
read linearly from first line to last for this audit. The spine declares itself
the primary semantic review surface; the full reference remains the source for
technical and schema detail.

FPF was anchored at public `main` commit
[`f2f6f43bb92a3af81283977f06fb3fbac62f77a7`](https://github.com/ailev/FPF/tree/f2f6f43bb92a3af81283977f06fb3fbac62f77a7).
The relevant current patterns were inspected directly, especially A.10, B.3,
C.19.2, C.27, C.28 and the newly added
[`C.37 Use-Bounded Representation Selection and Co-Use`](https://github.com/ailev/FPF/blob/f2f6f43bb92a3af81283977f06fb3fbac62f77a7/FPF-Spec.md#c37---use-bounded-representation-selection-and-co-use).
The 13,831,470-byte FPF specification was not read end to end in this pass.
Earlier project audits already covered the named older patterns; this pass
checked their current object and C.37's material change.

The external comparison is selective rather than systematic. It uses primary
standards, handbooks and foundational papers where practical. A close
neighbour can defeat a broad novelty claim without proving that two methods
are interchangeable.

## 2. TRACE's own current claim ceiling

TRACE already makes several important concessions:

```text
TRACE OUTPUT != WORLD TRUTH
TRACE OUTPUT != CLEARANCE
TRACE OUTPUT != MORAL AUTHORITY
SCHEMA VALID != WORLD VALID
PACKET COMPLETED != DILIGENCE ESTABLISHED
```

Its README also says that v0.3.0 adds no new primitive, makes no superiority
claim over FPF, has no efficacy result, and should be used only when ordinary
prose or a specialist method loses material connections. A 32-call transfer
study found material burden and no evidence of practical advantage.

Those are not decorative caveats. They set the maximum honest claim for this
audit. TRACE cannot be rescued by calling a known component novel, by treating
internal coherence as efficacy, or by treating a complete packet as applied
discipline.

## 3. Territory with strong prior owners

### 3.1 System boundary, control, feedback and unsafe timing

The [MIT STPA Handbook](https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf)
already provides a system-theoretic process for defining analytical purpose,
constructing control structures, identifying unsafe control actions, building
causal scenarios, and deriving constraints. It explicitly treats human,
software and organizational controllers; feedback; actions that are not
provided, are provided unsafely, occur too early or too late, or last too long;
and refinement across levels.

This is a strong prior owner of much of TRACE's selective causal loop,
controller/action/feedback distinctions, control refusal, unsafe timing and
multi-scale refinement. TRACE's reminders that a control action does not prove
a transition and that a feedback path does not prove received, accurate
feedback are sound. They are not an unoccupied theory.

TRACE differs by carrying evidence status, route usability, burden, residue
and representation limits in the same reading. That is an integration choice,
not a replacement for STPA's hazard-analysis method.

### 3.2 Claims, evidence, context, argument and assurance

The [GSN Standard](https://scsc.uk/gsn-standard) and NASA's
[GSN assurance-case guidance](https://modelbasedassurance.org/seamdoc/docs/chapter5/)
already structure claims, subclaims, strategies, contexts, justifications and
evidence. NASA's account is explicit that an assurance case documents an
argument but does not make faulty reasoning or premises true.

FPF A.10 and B.3 go further than TRACE's compact claim/evidence fields in
governing provenance, bounded reliance, currentness, challenge, assurance
scope and disposition. TRACE therefore does not own a general evidence or
assurance calculus. Its representation-independent firing rule is a useful
local discipline: a load-bearing proposition does not become warrant-free
because it appears in configuration, metadata, schema or prose. That rule is
best treated as a profile guard over the stronger neighbouring machinery.

### 3.3 Provenance, records, activities and responsibility

The W3C [PROV-O Recommendation](https://www.w3.org/TR/prov-o/) supplies a
standard model of entities, activities and agents, including use, generation,
derivation, attribution, association, delegation, revision and invalidation.
It can represent timed activities and qualified influence relations.

PROV-O consequently owns much of the general provenance graph. TRACE's record
custody questions add a different concern: who can alter, delete, inspect,
challenge or safely disclose a record, and whether the challenged actor
controls storage. That is a practical adversarial review overlay, not a new
provenance foundation.

### 3.4 Requirements, traceability, verification and validation

The [NASA Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)
already separates verification from validation, carries bidirectional
requirements traceability, assigns owners and verification methods, and
relates decisions, assumptions, constraints, test plans and stakeholder
expectations across a lifecycle.

This absorbs broad claims that requirements, evidence, checks, ownership and
current system use need explicit relations. TRACE's sequence
`CHECK_EXISTS != CHECK_EXECUTED != CHECK_DETECTS_TARGET_FAILURE` is a compact
and useful warning, but not a new verification discipline.

### 3.5 Events, repeated process behaviour and conformance

[Process-mining conformance checking](https://www.processmining.org/conformance.html)
already compares observed behaviour with process models using event data.
[Object-centric process mining](https://doi.org/10.3390/math11122691) addresses
events involving multiple interacting object types rather than forcing every
event into one case notion.

These methods are stronger than TRACE for discovering, measuring and checking
recurrent process behaviour from logs. TRACE's stream/mechanism distinction
and `LOCAL_CORRECTION + STREAM_PERSISTENCE != MECHANISM_CHANGE` remain useful
diagnostic guards where logs are incomplete, controlled by the operator, or
not yet available. TRACE does not supply the empirical process-mining method
that would establish the pattern.

### 3.6 Clocks, transitions, safety and liveness

[Timed automata](https://doi.org/10.1016/0304-3975(94)90010-8) provide formal
state-transition systems with real-valued clocks and timing constraints.
Lamport's work on
[safety and liveness](https://www.microsoft.com/en-us/research/publication/proving-correctness-multiprocess-programs/)
established much stronger formal meanings for what must never happen and what
must eventually happen in concurrent systems.

TRACE's clocks are less formal and more socio-technical. Its useful emphasis
is on clock authorship and burden: who sets, controls, pauses and sees a
deadline, who gains speed, and who carries delay. Its interval-safe correction
rules are sensible bounded arithmetic. They should not be presented as an
alternative temporal logic or formal liveness proof.

### 3.7 Critical paths and feasible completion

Kelley's foundational account of the
[Critical Path Method](https://doi.org/10.1287/opre.9.3.296) already models
activity sequence, duration, cost, labour, budget, procurement limits and the
effects of delay. It therefore owns the general precedence-DAG and
critical-path method.

TRACE makes an earned local correction to casual use of that method:

```text
NO_PRECEDENCE_EDGE != CONCURRENCY_AVAILABLE
STRUCTURAL_PARALLELISM != FEASIBLE_PARALLELISM
ACYCLIC_SUPPORTED != FEASIBLE_SCHEDULE_ESTABLISHED
```

It also binds the timing result to a specific pathway, affected scope, target,
route, capability context, temporal basis and boundary condition. This is
disciplined synthesis. It is not a new scheduling theory, and TRACE currently
has no scheduler or resource model.

### 3.8 Causal models and intervention claims

Pearl's [structural causal-model tradition](https://bayes.cs.ucla.edu/BOOK-99/book-toc.html)
already supplies formal machinery for causal graphs, interventions and
counterfactuals. TRACE deliberately does not estimate causal effects, identify
confounding, or prove a causal model from data.

TRACE may expose where a causal or mechanism proposition is being relied on,
its evidence state, selector and uncertainty. It cannot replace causal
identification. A TRACE edge is a claim to be supported, not a causal result.

### 3.9 Future paths, viability and correspondence

[Viability theory](https://link.springer.com/book/10.1007/978-0-8176-4910-4)
has established mathematical machinery for viability kernels, exit tubes,
state constraints and regulation of control systems. Formal work on
[bisimulation and refinement](https://doi.org/10.1006/inco.1996.0057) gives
stronger criteria for matching behaviour and computation histories across
transition systems.

These are close prior owners of the formal territory near viable future-space
and path correspondence. TRACE's
`SAME_PATH_LABEL != SAME_TRAJECTORY` is correct, but its current
correspondence test is a review guard rather than a formal equivalence proof.
Its human-facing questions about whether a route is findable, intelligible,
affordable, safe enough to use, fast enough and backed by effective authority
are not supplied by a bare viability kernel. Again, the difference is in the
joined review surface.

## 4. FPF makes the boundary narrower

FPF C.37 now states the representation-selection problem directly: for one
receiver and one exact action, recover each candidate under its governing
method, name the exact claim relied on, state what the representation exposes
and loses, classify the bounded use as `select`, `decline` or `unresolved`, and
name the return trigger. Co-use does not create one integrated world model.

Applied to TRACE, C.37 blocks three shortcuts:

1. TRACE cannot be selected because it is called a structural language.
2. Its provenance, completeness or readability cannot supply a missing
   domain result, evidence disposition, permission or assurance result.
3. Selection for one review does not authorize TRACE for another action with
   different losses and burdens.

The honest FPF relationship is therefore:

> TRACE is one candidate representation for a bounded cross-domain review.
> Specialist methods retain authority for their subject results. FPF can
> govern why this representation, for this receiver and action, is selected
> despite what it omits and costs.

That is narrower than presenting TRACE as a general structural language which
neighbouring methods should enter. It is compatible with TRACE's own current
README, but should govern future outreach and evaluation.

## 5. What remains after displacement

The strongest surviving TRACE object is not a new ontology, causal calculus,
temporal logic, assurance method, provenance standard, process-mining method
or scheduling theory.

It is provisionally:

> a use-bounded cross-domain review profile that keeps several failure
> relations visible in one pass: aperture and affected scope; control and
> feedback; load-bearing claim status; route usability; authored clocks and
> correction feasibility; burden transfer; residue after reversal; recurrence;
> and the difference between a completed representation and a changed world.

Four features may justify retaining it:

1. **Joined omission lens.** Specialist tools can each answer their own
   questions while still leaving the relation between late evidence, an
   unusable appeal route, a closing correction window and residue invisible.
2. **Representation-independent firing.** The same evidential discipline is
   applied whether a proposition appears as prose, an edge, a field or a
   configuration value.
3. **Anti-clearance boundary.** TRACE repeatedly prevents a schema, packet,
   check, review or recorded brake from becoming authority or proof of world
   change.
4. **Mixed human/AI transfer surface.** A bounded carrier may preserve which
   claims, unknowns, selectors and limits survived a handoff.

These are synthesis, product-design and governance hypotheses. They are not
validation or theoretical novelty.

## 6. The strongest falsifier

TRACE fails as a separate method if matched reviewers using ordinary prose,
FPF, or one appropriate specialist checklist:

- find the same material omissions;
- produce equally actionable and challengeable results;
- preserve provenance and uncertainty at least as well;
- create less reader and recording burden;
- induce no more false confidence or packet theatre.

The present evidence does not defeat that falsifier. The earlier 32-call
transfer study found material burden and no practical-advantage result. The
180,511-byte full reference and 40-field minimum packet strengthen the burden
challenge. Five required `const: false` schema fields constrain syntax but do
not discriminate whether their distinctions were actually applied.

The likely useful unit is therefore much smaller than the full packet: a
case-specific review profile with only the load-bearing connections needed for
one receiver and one action. If that smaller unit performs no better than a
short checklist, TRACE should be narrowed again to a vocabulary, checklist or
archive format.

## 7. Risks that remain internal to TRACE

- **Integration tax:** keeping many distinctions together can require more
  work than the decision justifies.
- **Shallow breadth:** a general carrier can create the appearance of having
  done STPA, causal inference, assurance, process mining or scheduling when it
  has only named their questions.
- **Packet theatre:** TRACE can describe this failure but cannot prevent its
  own packet from becoming the diligence token.
- **False portability:** a guard that transfers linguistically may not retain
  the evidential or operational meaning of its source discipline.
- **Reader exclusion:** the apparatus may work only for unusually patient or
  well-resourced readers, reproducing the burden it aims to expose.
- **Selector concealment:** choosing the targets, boundaries, measures and
  stopping budget can dominate the output even when every packet field is
  valid.

## 8. Result classification

### Earned result

The broad components of TRACE have strong prior owners. TRACE's current value,
if any, lies in a deliberately bounded integration and transfer profile, not
in new primitives or replacement of specialist methods.

### Provisional idea

The joined sequence may catch cross-boundary omissions that separate methods
miss at handoff points, especially where institutional process, evidence,
timing, route usability and persistent human consequence interact.

### Wording improvement

No immediate source rewrite is necessary. The public README already states
the narrow use rule, non-superiority, non-clearance boundary and absent efficacy
result. Future descriptions should prefer “use-bounded cross-domain review
profile” over any implication of a general foundational method.

### Governance/process improvement

A later short `INTELLECTUAL_NEIGHBOURS.md` in TRACE would be justified after
the comparison is challenged and citations are checked. It should tell a new
reader which specialist method to use instead, where TRACE only records a
claim, and what exact integrated use remains under test.

### Unresolved problem

No comparative evidence yet shows that TRACE's integration improves omission
detection, correction timing, challenge quality or handoff fidelity after
burden and false confidence are counted.

## 9. Current decision

Do not alter TRACE RC1, its schema, release state or public claims on the basis
of this audit. Preserve this criticism in COM, invite independent disagreement,
and use the result to design one small comparative evaluation rather than more
internal tests.

The next earned experiment is not another full-packet exercise. It is a
matched, one-action comparison among:

1. ordinary structured prose;
2. the best-fit specialist method or checklist;
3. a minimal TRACE profile;

with omissions found, false positives, actionable corrections, retained
uncertainty, reader effort and recording burden measured. Null or adverse
results must be retained.
