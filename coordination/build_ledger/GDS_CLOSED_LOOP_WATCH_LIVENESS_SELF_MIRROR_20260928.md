# GDS closed-loop pressure — COM watch-liveness self-mirror

Date: 28 September 2026

Status: **INTERNAL HONESTY REPAIR / EXISTING COM RULE MADE HOT-SURFACE EXPLICIT / NO NEW PRIMITIVE / NO AUTOMATION CREATED**

External pressure:
- GOV.UK Service Standard assessment, *Assess and manage your council’s cyber resilience – alpha reassessment*, published 24 September 2026:
  https://www.gov.uk/service-standard-reports/assess-and-manage-your-councils-cyber-resilience-alpha-reassessment

## Why this earned a self-mirror

The external assessment is useful not because the project needs a local-government cyber method.

It explicitly asks for a closed evidence loop:

~~~text
WHAT WAS TESTED
-> WHAT WAS LEARNED
-> WHAT DECISION WAS MADE
-> WHAT CHANGED IN THE SERVICE
~~~

It also distinguishes:
- plans from observed accessibility evidence;
- fallback channels from a joined-up journey back into the main service;
- ad hoc iteration from systematic `insight -> prioritisation -> delivery -> re-test`;
- performance measures from baselines, owners, targets and governance.

Those are already familiar project distinctions.

The useful pressure landed on COM itself.

Recent hot-surface field dispositions use phrases such as:
- `WATCH OWNER RESPONSE OR REINSPECTION`;
- `WATCH IMPLEMENTATION`;
- `WATCH PILOT OUTCOME`.

But no scheduler, standing agent or continuously running observer was created for those cases.

Without a visible guard, `WATCH` can be read as stronger operational liveness than actually exists.

## Existing stronger internal owner

`COM_PROTOCOL_WORKING.md` already requires delegated/asynchronous work to carry:

~~~text
observation_owner
next_check
~~~

and explicitly states:

> `MANUAL` is allowed when no scheduler is available, but it makes **no autonomous-liveness claim**.

Therefore no protocol invention is earned.

The defect is narrower:

~~~text
STRONG RULE EXISTS IN PROTOCOL
+
HOT SURFACE USES AMBIGUOUS SHORTHAND
=
CURRENTNESS / HONESTY REPAIR
~~~

## Repair

On current hot routing surfaces, interpret:

~~~text
WATCH CONSEQUENCES
=
REOPEN ON NAMED EVENT / FRESH EVIDENCE
BY DEFAULT

WATCH
!=
ACTIVE MONITORING

WATCH
!=
SCHEDULED CHECK

WATCH
!=
AUTONOMOUS LIVENESS
~~~

A real standing watch requires an explicit current mechanism such as:

~~~text
observation_owner
+
next_check / event trigger / schedule
+
reachable source/route
~~~

If those are absent, say **EVENT-TRIGGERED / NO STANDING MONITOR** where ambiguity matters.

## Current cases corrected by interpretation

### Probation public-protection witness

Wake conditions:
- HMIP/HMPPS publishes a materially relevant national response/action-plan update;
- a future public-protection reinspection materially changes the observed state;
- stronger owner evidence corrects the current field note.

Current state:

~~~text
EVENT-TRIGGERED WATCH
NO STANDING MONITOR
~~~

### Keep Britain Working witness

Wake conditions:
- published pilot/Vanguard evidence;
- materially specified WHIU governance/data architecture;
- concrete co-production evidence or affected-group correction;
- official programme update that changes the current design state.

Current state:

~~~text
EVENT-TRIGGERED WATCH
NO STANDING MONITOR
~~~

### FSA voice-to-text pilot and similar older `WATCH` notes

Do not silently reinterpret historical `WATCH` as a background job.

Unless a file/task explicitly records an observation owner and next check/schedule, treat it as a documented wake condition only.

## What this does not do

This repair does not:
- create an automation;
- promise background work;
- add a new COM event type;
- change TRACE or Mechanical Ethics;
- require every field note to carry a calendar date;
- turn a public source into a task;
- make Mark responsible for manually polling every case.

It makes the absence of autonomous liveness explicit.

## Result

~~~text
EXTERNAL GDS PRESSURE = USEFUL SELF-MIRROR
COM PROTOCOL GAP = NO
HOT-SURFACE AMBIGUITY = YES
SMALLEST REPAIR = EXPLICIT WATCH SEMANTICS
AUTOMATION = NONE
TRACE PATCH = NO
ME PATCH = NO
~~~

Freeze after hot-surface repair. Reopen only if an actual monitoring mechanism is commissioned or a later continuity failure shows the distinction is still being lost.
