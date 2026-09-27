# Relay self-mirror — monitoring, allegation and enforcement boundaries

Date: 27 September 2026

Status: **SELF-MIRROR / NO SOURCE DEFECT FOUND / NO RELAY PATCH / NO PRODUCTION CHANGE**

World pressure:
field/OPENAI_DNS_MONITOR_TO_BRAKE_WITNESS_20260927.md

Question:

> Does Campfire Relay anywhere describe a report, monitor, diagnostic or allegation as though it actually prevents/interrupts the action?

Bounded surfaces inspected:
- Campfire Relay current main 9408d795d0508815e097066b749800ddbd8b8290;
- README.md;
- coordination/DECISIONS.md;
- coordination/OPEN_QUESTIONS.md;
- docs/SEED_REFERENCE.md;
- src/store.mjs;
- relevant judge-accounting tests / TRACE judge constraints;
- existing fail-closed dispatch / TRACE-profile language surfaced through repository search.

## Result 1 — rule-violation signal is explicitly report-only

Current Relay decision D-015 says a non-NONE judge rule_violation field is recorded as:

rule_violation_alleged

with judge identity and accused side.

It explicitly **must not** change the game result.

Reason preserved by Relay:
- no executable aggregation threshold defines when independent ballots establish a violation;
- a witnessed judge ballot previously miscoded rule_violation: B while its prose said there was no declared-rule violation;
- automatic enforcement on that field could therefore create a false brake.

The source/report surfaces preserve this boundary:

~~~text
ALLEGATION
!=
ESTABLISHED VIOLATION

REPORT-ONLY SIGNAL
!=
ENFORCEMENT
~~~

Tests explicitly verify that an allegation cannot change the winner.

## Result 2 — the unresolved enforcement question remains honest

Relay OPEN_QUESTIONS.md Q-008 asks whether rule-violation allegations should ever become enforceable.

Current answer:

**report-only is settled for now.**

Before enforcement could be introduced, Relay says it would need:
- an unambiguous ballot meaning;
- an aggregation rule;
- a rule for what makes a violation established.

The OpenAI DNS monitor/brake witness does **not** supply any of those missing semantics.

Therefore it does not earn changing Q-008.

~~~text
WORLD CASE SHOWS MONITOR != BRAKE
!=
EVERY MONITOR SHOULD BECOME A BRAKE
~~~

## Result 3 — actual gates are described differently

Relay's current source/docs distinguish observational/reporting surfaces from actual fail-closed gates.

Examples already represented include:
- Money Guard / paid-dispatch preflight;
- one-use stage-bound dispatch authority;
- control-only seeds refusing before provider dispatch;
- TRACE profile resolution/hash verification failing closed before affected paid dispatch;
- missing/failed assigned source material stopping before participant dispatch.

This does **not** prove universal safety or that every possible dispatch path is correctly gated.

It establishes only that the inspected architecture/documentation does not collapse its report-only judge signal into enforcement language.

## OpenAI witness applied correctly

The external incident gave the right self-question:

~~~text
MONITOR ACTIVE
!=
BRAKE PRESENT

ALERT ACKNOWLEDGED
!=
STOP COMPLETED
~~~

Relay currently survives that question on the inspected surfaces because:

~~~text
RULE-VIOLATION SIGNAL
= REPORT_ONLY

ACTUAL DISPATCH GATES
= SEPARATELY DEFINED / TESTED FAIL-CLOSED PATHS
~~~

## Ceiling

Do not infer:
- all Relay monitors/logs were exhaustively audited;
- production runtime equals current source;
- configured provider target equals physical backend;
- every fail-closed claim has been live-provider witnessed;
- Q-008 can never be revisited;
- Relay is safe because this mirror returned no delta.

## Decision

No Relay source patch.

No Simple-v1 patch.

No new enforcement rule.

No Production activation.

Preserve the OpenAI incident as a regression question for future consequential control surfaces:

> Is this object observing/reporting a condition, or is it actually connected to a tested interruption path?

Current disposition:

**SELF-MIRROR PASS WITH CEILINGS / REPORT != BRAKE DISTINCTION ALREADY HONEST / NO PATCH.**
