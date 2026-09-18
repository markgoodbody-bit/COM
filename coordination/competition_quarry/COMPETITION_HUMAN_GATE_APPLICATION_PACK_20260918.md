# Competition human-gate application pack — 18 September 2026

Status: **PUBLIC ANSWER BANK / NOT AN APPLICATION / NO TERMS ACCEPTANCE / NO TRAVEL COMMITMENT**

Purpose: reduce the unavoidable human registration/application step for current high-fit competitions without inventing personal details or preselecting a challenge before the organiser reveals it.

Use only where the live form asks for the corresponding information. Do not paste fields that are not requested.

## Public profile

**Name / introduction**

Mark — UK systems engineer and independent AI/reasoning-system builder.

**Background**

I have more than 30 years of experience in IT and systems engineering. My current independent work focuses on building and testing practical structures for AI/human reasoning, multi-agent coordination, evidence provenance, exception recovery, and answerable action under uncertainty.

**What I build**

Recent public/private engineering work includes:

- multi-agent coordination where model/session/role identity and authority remain distinct;
- append-only evidence and correction records;
- source/currentness and provenance handling;
- read-after-write verification for external actions;
- ambiguity-preserving state rather than false success/failure;
- duplicate/idempotency guards;
- failure recovery and human handoff;
- deterministic adverse-path tests rather than happy-path-only demos.

**Public work**

- TRACE: https://github.com/markgoodbody-bit/TRACE
- Mechanical Ethics: https://github.com/markgoodbody-bit/mechanical-ethics
- The Human Record: https://github.com/markgoodbody-bit/human-record
- Please Start From Here: https://pleasestartfromhere.com/

These projects are exploratory and should not be described as validated AI-safety standards or commercial products.

## Short application answer — why participate?

I am interested in building systems that stay useful when the clean-path assumptions fail: stale or conflicting information, ambiguous external actions, missing context, model/tool failure, and situations where a human needs to take over with enough evidence to understand what happened.

I work middle-out from real failures rather than starting with a general framework and looking for somewhere to apply it. A hackathon with a concrete challenge, real APIs/data and a hard deadline is therefore useful to me: it gives the work something external to answer to.

## Short technical-strength answer

My strongest contribution is systems reasoning plus implementation under failure.

I am comfortable moving from an ambiguous operational problem to a small testable architecture, then attacking it with counterexamples. I focus particularly on state, provenance, idempotency, currentness, external side effects, reconciliation and auditability.

I also use AI coding agents extensively, including parallel/differentiated review rather than treating multi-model agreement as validation.

## Short team answer

I can work independently or as part of a small team.

I am most useful where somebody needs to:
- structure the system;
- identify failure modes;
- build the first end-to-end path;
- keep evidence/debugging visible;
- prevent the demo from claiming more than it actually establishes.

I do not need to own every UI/model/data component.

## Hack-Nation 7 — application positioning

Current event facts:
- 3–4 October 2026;
- online/hybrid participation;
- challenge tracks provided at kickoff;
- no pre-existing idea/team required.

### Why Hack-Nation?

The format is attractive because the challenge arrives before the idea. I do not want to force an existing project into a sponsor track. I would rather read the actual problem, identify the strongest existing owner/mechanism, and build the smallest useful missing part during the event.

I can bring reusable engineering patterns around agent reliability, evidence, exception handling and recovery, but I would choose the product only after seeing the challenge brief.

### What would you like to build?

If asked before track reveal:

> I do not want to preselect the solution before seeing the problem. My likely contribution is an agent or workflow that has to act on messy external state and remain inspectable when information conflicts or an action fails. I would choose the concrete user/problem at kickoff.

Do not substitute an Amazon/TRACE/THR pitch merely to fill this field.

## NVIDIA Claw Agent Challenge — registration positioning

Current public event facts:
- remote across the UK;
- build a long-running claw agent;
- full challenge/submission requirements supplied only after registration.

### Why this challenge?

I have been working on the unglamorous failure modes of long-running AI collaboration: stale state, lost/repeated actions, session continuity, retries, currentness, source-vs-runtime divergence and how a successor recovers enough evidence to continue safely.

That makes the long-running-agent format a natural fit, but I would not choose the exact agent until I have read NVIDIA's registered challenge brief and resource constraints.

### Relevant technical experience

Useful examples:
- persistent event/receipt ledgers;
- replay/duplicate protection;
- watchdog/currentness separation;
- agent role vs runtime/session identity;
- bounded external action plus readback;
- fail-closed partial syncs;
- recovery that preserves unresolved outcomes rather than rewriting history.

Do not say the existing Campfire Relay is already a qualifying Claw submission until the organiser brief establishes that.

## Dwelly — application positioning

Current public event facts:
- operational agent challenge;
- real-world synthetic data/workflows;
- Reality Test introduces conflicting information, failed actions and missing context;
- explicit exception-handling/engineering/voice prizes.

### Why Dwelly?

This is unusually close to the kind of failures I already work on.

A useful agent has to remain coherent after the easy demo breaks: a contractor did not actually attend, a message is stale, an external API timed out after a possible commit, two sources disagree, or the person who can authorize the next action is unavailable.

I want to build against that operational reality rather than optimize a clean scripted flow.

### What would you bring?

A small failure-handling spine:
- timestamped/attributed observations;
- explicit currentness;
- one-write/idempotency guards;
- external effect verification;
- unknown/reconcile states;
- typed exceptions;
- evidence-bearing human escalation.

Then I would fit it to whichever Dwelly track/problem is assigned rather than forcing a generic architecture onto the challenge.

## Stripe x Briefcase — registration positioning

If asked for motivation:

> I am interested in agent workflows where policy/authority, money movement and external side effects must remain inspectable. I would use Stripe's native payment/idempotency mechanisms rather than reimplementing them, and focus on the orchestration around intent, exact action, readback, exception state and auditability.

Do not claim payments expertise beyond what is actually built in the event.

## Future States / No.10 — application positioning

If asked why public-sector problems:

> Public systems contain real clocks, authority boundaries, partial information and people carrying the consequences of process failure. I am interested in using engineering to make one concrete state problem easier to see or correct, not in pitching a universal ethics framework. I would start from the department/problem owner's data and constraints.

## VAST real-time video agents — application positioning

If asked for relevant interest:

> My current work includes provenance, evidence lineage and the distinction between what a representation shows and what a system infers from it. For a video-agent challenge I would apply that discipline only if it helps the supplied dataset/problem—for example, separating observed state, inferred event and uncertain identity rather than collapsing them into one confident label.

Do not claim a prebuilt computer-vision model or production video system.

## What not to claim in any form

Do not claim:
- previous competition wins unless actually awarded;
- a startup/company/customer base;
- deployed enterprise AI;
- TRACE or Mechanical Ethics validation;
- AI consciousness/personhood claims;
- independent multi-model validation from project apertures;
- a product already using sponsor infrastructure unless actually tested;
- a willingness/ability to attend a physical event unless Mark decides that for the specific event.

## Human-only fields

Do not store these in public COM:
- private phone number;
- home address;
- date of birth;
- passport/nationality evidence;
- private calendar;
- payment/tax details;
- account passwords/tokens;
- private employer information.

Supply those directly only where the legitimate event form requires them.

## Gate

This file makes application faster. It does not make the application decision.

~~~text
ANSWER BANK != APPLICATION
APPLICATION != ACCEPTANCE
ACCEPTANCE != ATTENDANCE COMMITMENT
REGISTRATION != TERMS ACCEPTANCE BY FRAMEWORK
~~~
