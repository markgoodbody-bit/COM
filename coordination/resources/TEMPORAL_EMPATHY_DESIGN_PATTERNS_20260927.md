# Temporal empathy — design intervention pattern library

Date: 27 September 2026

Status: **DESIGN / OWNER-ABSORPTION / NOT CANON / NO TRACE OR ME PATCH**

Purpose:

Translate stronger-owner work on temporal design, disability temporalities, time poverty, workload-capacity, schedule predictability, prospective memory and institutional delay into small intervention patterns.

This is not a new theory of time.

The question is narrower:

> If a system notices that affected entities inhabit different temporal conditions, what concrete design changes can reduce avoidable temporal burden without forcing everybody onto one supposedly normal rhythm?

Primary owner map:
`coordination/resources/TEMPORAL_EMPATHY_STRONG_OWNER_MAP_20260927.md`

Owner router:
`coordination/resources/TEMPORAL_EMPATHY_OWNER_ROUTING_MATRIX_20260927.md`

## Design correction: non-normative time is not automatically a deficit

Disability / crip-time work is a critical correction to the project's early framing.

Useful owner surfaces:
- Ellen Samuels & Elizabeth Freeman (eds.), *Crip Temporalities*:
  https://www.dukeupress.edu/crip-temporalities
- Margaret Price, *Crip Spacetime*:
  https://www.dukeupress.edu/crip-spacetime
- Elizabeth Freeman, *Time Binds* / chrononormativity:
  https://www.dukeupress.edu/time-binds

The literature does not treat all non-standard pacing as a failure to be repaired.

It also asks what becomes possible when time is not organised entirely around productivity, speed and synchronisation.

Preserve:

```text
DIFFERENT RHYTHM
!=
DEFICIT

SLOWER
!=
WORSE BY DEFAULT

UNPREDICTABLE CAPACITY
!=
MORAL FAILURE

ACCESS
!=
MAKING THE PERSON MATCH THE INSTITUTION
```

Temporal-empathy work drifts if its only goal becomes:

`MAKE THE PERSON MORE RELIABLY ON-TIME FOR THE SYSTEM`.

A better question is:

> Which timing requirements are genuinely load-bearing, which are merely inherited norms, and which side has the power to change them?

## Pattern 1 — Represent uncertainty honestly

Strong owner:
Temporal Design / Haze.

Problem:
systems often require exact date/time/availability when the affected entity only has a range or conditional estimate.

Intervention candidates:
- time windows instead of false point estimates;
- "likely / possible / unknown" states;
- revisable availability;
- visible confidence/uncertainty;
- negotiated rather than unilateral rescheduling.

Preserve:

```text
EXACT FIELD REQUIRED
!=
EXACT WORLD STATE EXISTS

UNCERTAINTY REPRESENTED
!=
COMMITMENT REFUSED
```

Failure mode:
uncertainty field exists but is penalised, ignored or converted back into a hard commitment downstream.

## Pattern 2 — Give advance notice where the system can

Strong owners:
schedule-control / fair-workweek / work-schedule predictability literature.

Useful owner surfaces:
- Seattle Secure Scheduling evaluation:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8545454/
- routine schedule instability:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7730535/

Evidence:
greater schedule predictability after Seattle's ordinance was associated with improvements in subjective well-being, sleep quality and economic security in the evaluated population.

Intervention candidates:
- publish schedules earlier;
- avoid last-minute changes where possible;
- compensate externally imposed changes;
- expose likelihood of change;
- preserve minimum rest between tightly spaced commitments.

Preserve:

```text
SAME HOURS
!=
SAME TEMPORAL BURDEN

FLEXIBILITY FOR OPERATOR
!=
FLEXIBILITY FOR AFFECTED PERSON
```

## Pattern 3 — Make next-check time explicit

Problem:
"pending" often creates repeated vigilance / checking work.

Intervention:
tell the affected entity:
- who owns the next action;
- what is missing;
- when the next review/check will happen;
- what event should trigger an earlier check;
- whether they need to do anything meanwhile.

Purpose:
reduce unnecessary prospective-memory / vigilance burden.

```text
CASE OPEN
+ NO NEXT CHECK
-> PERSON MAY HAVE TO SELF-POLL

NAMED NEXT CHECK
-> CUE BURDEN MAY FALL
```

This is already compatible with ME's Strategic Unknown.

## Pattern 4 — Offload remembering, not authority

Strong owner:
prospective memory / intention offloading.

Intervention candidates:
- reminders;
- calendar hooks;
- staged notifications;
- visible countdown/window;
- trigger-based prompts;
- external cue that can be dismissed or rescheduled.

Preserve:

```text
CUE SUPPORT
!=
DECISION CONTROL

REMINDER
!=
COMMAND
```

Failure mode:
notification flood creates more interruption burden than it removes.

## Pattern 5 — Count the work created by the remedy

Strong owner:
Minimally Disruptive Medicine / treatment burden / Cumulative Complexity.

Problem:
institutions often respond to difficulty by adding:
- forms;
- appointments;
- monitoring;
- reporting;
- self-management;
- repeated evidence requests;
- extra deadlines.

Intervention:
before adding a requirement, ask:
- what work does this create?
- who must carry it?
- what other work is already present?
- can the requirement be removed, combined, automated, transferred or supported?

Preserve:

```text
HELP OFFERED
!=
WORKLOAD REDUCED

MORE PROCESS
!=
MORE SUPPORT

SAME REQUIREMENT
!=
SAME BURDEN
```

## Pattern 6 — Subtract before adding

Derived from treatment-burden / administrative-burden owners.

When a system sees overload, first search for removable work:
- duplicate evidence;
- repeated identity proof;
- unnecessary re-entry of known data;
- multiple appointments that can be combined;
- redundant approvals;
- status checks the system can perform itself.

Design target:

```text
SMALLEST HELP
CAN BE
REMOVING A REQUIREMENT
```

This is especially relevant where the institution already holds the evidence.

## Pattern 7 — Protect recovery as functional capacity

Stronger owners:
fatigue/recovery / disability temporalities / rest-break research.

Useful owner surfaces:
- Crip Temporalities:
  https://www.dukeupress.edu/crip-temporalities
- rest-break reengagement:
  https://pubmed.ncbi.nlm.nih.gov/27039697/
- work/rest schedule studies:
  https://www.sciencedirect.com/science/article/pii/S0169814196000315

Correction:

```text
NO SCHEDULED TASK
!=
AVAILABLE CAPACITY

REST
!=
WASTED TIME
```

Intervention candidates:
- recovery buffers;
- avoid forced "clopening" / insufficient-rest sequences;
- allow pacing variation;
- avoid scheduling every open interval;
- distinguish interruption from restorative break.

Failure mode:
"wellness break" exists but workload is unchanged, so the person must recover the lost time later.

## Pattern 8 — Expose interruption cost and protect critical phases

Strong owner:
human factors / interruption research.

Intervention candidates:
- defer non-urgent interruptions during critical phases;
- batch messages;
- route urgent versus non-urgent signals differently;
- show interruption priority;
- permit a temporary focus state with emergency override;
- restore task context after interruption.

Preserve:

```text
MESSAGE DELIVERED FAST
!=
SYSTEM PERFORMED BETTER

INTERRUPTION
!=
INFORMATION VALUE
```

Do not infer "never interrupt"; context and urgency matter.

## Pattern 9 — Let the affected entity control deferral where possible

Strong owners:
schedule control / time work / temporal agency.

Intervention candidates:
- self-service rescheduling;
- defer without penalty;
- pause and resume;
- choose from windows rather than fixed points;
- negotiate sequence;
- signal temporary reduced capacity.

Preserve:

```text
FLEXIBLE SYSTEM
!=
AFFECTED ENTITY HAS TEMPORAL AGENCY
```

A system that offers many appointment slots but punishes rescheduling may be flexible for the operator, not the participant.

## Pattern 10 — Freeze the institution's clock when its own delay would consume the person's route

Owner families:
administrative law / remedies / institutional-time inequality.

Candidate design:
where legally/domain-appropriate, consider:
- tolling/pausing appeal deadlines during institution-caused delay;
- preserving eligibility while evidence the institution controls is pending;
- temporary continuation/protection;
- no penalty for failure to act during a period in which the required route was unavailable.

Preserve:

```text
INSTITUTION DELAYS
+ PERSON DEADLINE CONTINUES
-> TEMPORAL BURDEN CAN BE ONE-SIDED
```

This is domain-sensitive and not a universal legal recommendation.

## Pattern 11 — Show waiting as a state with consequences

Strong owners:
institutional time inequality / unequal waiting.

Instead of:

`STATUS = PENDING`

represent where useful:
- elapsed time;
- expected next action;
- responsible owner;
- change since entry;
- consequences accumulating during wait;
- whether any external clock continues to run.

Purpose:
make waiting visible as a transition, not an empty gap.

This is directly compatible with TRACE's `WAIT / DELAY / INACTION` transition classes.

## Pattern 12 — Track temporal burden transfers

Strong owners:
time poverty; administrative burden; workload-capacity; TRACE burden transfer.

Question:

> Did the system become faster by making somebody else wait, monitor, coordinate or recover?

Examples:
- automated self-service reduces staffing cost but increases user form work;
- just-in-time scheduling improves organisational utilisation but exports unpredictability to workers;
- repeated automated notifications improve operator response metrics but create attention burden elsewhere.

Preserve:

```text
LOCAL LATENCY ↓
!=
TOTAL TEMPORAL BURDEN ↓
```

## Pattern 13 — Offer accompaniment / collective access, not only individual accommodation

Strong owner:
Margaret Price / disability studies.

Price's work argues for collective accountability and develops `accompaniment` across relations among humans, objects, technologies, spaces and animals.

Useful public surface:
https://lsa.umich.edu/polisci/news-events/all-events.detail.html/144642-21895626.html

Intervention candidates:
- allow a supporter/helper to participate where appropriate;
- preserve shared context so the affected entity does not repeatedly reconstruct the case;
- design the environment so access is collective rather than requiring individual exception requests;
- let tools carry memory/coordination burden.

Preserve:

```text
INDIVIDUAL ACCOMMODATION ROUTE
!=
ACCESSIBLE ENVIRONMENT

HELPER PRESENT
!=
AUTHORITY TRANSFER
```

## Pattern 14 — Do not optimise away humane slack

Cross-owner synthesis:
time poverty, resilience/recovery, workload-capacity, disability temporalities.

Slack may provide:
- recovery;
- absorption of shocks;
- room for uncertainty;
- care;
- learning;
- correction;
- unplanned life.

A system optimised to 100% nominal utilisation can become brittle.

Candidate distinction:

```text
UNALLOCATED TIME
!=
WASTE

SLACK
CAN BE
CORRECTION / RECOVERY CAPACITY
```

This is schematic; resilience engineering / scheduling owners should supply domain-specific methods.

## Pattern 15 — Separate throughput targets from human temporal value

Chrononormativity is a useful warning: systems can organise bodies around maximum productivity and treat deviation as failure.

Intervention question:

> Is this deadline/rhythm necessary to the function, or does it mainly preserve a productivity norm?

Do not assume:
- faster is always better;
- synchronous is always better;
- immediate response is always evidence of care;
- delay is always harmful;
- slow work is low-value.

Preserve:

```text
SYSTEM SPEED
!=
HUMAN GOOD

PRODUCTIVITY RHYTHM
!=
NEUTRAL TIME
```

## Relation to released Mechanical Ethics

Current ME already represents:
- waiting cheap for one side / expensive for another;
- strategic uncertainty;
- who controls records, route and clock;
- burden placement;
- complexity exported to weaker party;
- slow harm while a case remains open;
- temporary protection;
- competing clocks;
- route usability;
- later repair not restoring the same future.

Therefore:

```text
DESIGN PATTERN LIBRARY
!=
ME REPRESENTATIONAL GAP
```

The outside literature mostly improves:
- attribution;
- salience;
- concrete intervention design;
- protection against productivity-normalisation drift.

## Relation to released TRACE

Current TRACE already represents:
- WAIT / DELAY / INACTION as transitions;
- `DELAY != NEUTRAL`;
- route usability including `fast enough`;
- typed clocks and hardening;
- burden creation / relief / transfer;
- capability and authority separation;
- residue;
- transition symmetry.

Therefore:

```text
TEMPORAL-EMPATHY DESIGN PATTERNS
!=
NEW TRACE ONTOLOGY
```

Potential value:
use TRACE to recognise the structure, then route to the relevant stronger owner and intervention family.

## Current design lesson

A compact sequence:

```text
WHOSE TIME IS THIS?
-> WHAT WORK / WAIT / UNCERTAINTY IS IMPOSED?
-> WHO CONTROLS OR CAN RENEGOTIATE IT?
-> WHAT CHANGES WHILE TIME PASSES?
-> WHAT WORK CAN BE REMOVED?
-> WHAT SUPPORT / CUE / PROTECTION RESTORES FEASIBILITY?
-> WHAT RHYTHM NEED NOT BE NORMALISED?
-> ROUTE TO STRONGER OWNER
```

## Current disposition

**USEFUL DESIGN PATTERN LIBRARY / STRONG OWNER CREDIT REQUIRED / NO TRACE OR ME PATCH.**
