# SHARED CAPACITY STRESS TEST — DRAFT V0.1

Status: **WORKING FIELD ROUTE / NOT CANON / NOT TRACE SCHEMA / NOT AN ALLOCATION RULE**

Purpose: help a bounded human or AI notice when a resilience, correction or contingency plan is counting on capacity that is shared, borrowed, correlated, slow to deliver, slow to regenerate, or already claimed by others.

This route is for a specific class of situation:

> **The plan works only because some spare capability is expected to be available when the primary capability is insufficient.**

Examples include staff, beds, electricity, fuel, liquidity, compute, communications, transport, housing, specialist expertise, emergency authority, human attention, independent review, trusted evidence or mutual aid.

The route does **not** replace domain capacity planning, emergency medicine, grid engineering, finance, logistics, public-law priority rules or ethics. Use the strongest owner method first. This card exists to expose cross-domain failure conditions that are easy to hide behind the word `backup`, `reserve`, `pool`, `surge`, `redundancy` or `fallback`.

```text
RESERVE_EXISTS != RESERVE_AVAILABLE_TO_ME
STOCK != FLOW
BORROWABLE_CAPACITY != DEDICATED_CAPACITY
MANY_BACKUPS != MANY_FAILURE_LINEAGES
LOCAL_CONTINGENCY_PLAN != SYSTEM-WIDE CONTINGENCY CAPACITY
SUM_OF_LOCAL_RESERVES != JOINTLY_AVAILABLE_RESERVE
RECOVERY_FROM_EVENT_1 != CAPACITY_READY_FOR_EVENT_2
```

## Use only when triggered

Use this route when at least one consequential next action relies on:

- a shared pool;
- spare capacity elsewhere;
- an external supplier or neighbouring unit;
- a contingency or fallback path;
- surge staffing / surge beds / reserve generation / strategic stocks;
- borrowing liquidity, compute, expertise, attention or authority;
- a claimed independent reviewer, monitor, backup service or second route.

If the situation does not rely on borrowed/shared capacity, stop. Do not force this route onto ordinary decisions.

## The route

Ordinary language is enough. A table is optional. The output should be the smallest account that changes the action.

### 1. Name the capability actually being counted

Do not begin with `we have redundancy`.

Ask:

- What exact capability is expected to absorb the overload or failure?
- In what unit does it become useful: beds, trained people, MW, barrels/day, vehicles, cash, review-hours, model-independent judgements?
- Is it **dedicated**, **locally protected**, **shared**, **borrowed on request**, or merely **assumed reachable**?
- Who controls release of it?

A reserve that cannot be identified operationally is not yet a usable reserve.

### 2. Trace the failure lineage, not the label

Ask what event could simultaneously damage the primary route **and** the backup.

Check shared dependence on:

- power / fuel / water / network;
- geography / weather / hazard zone;
- supplier / cloud / model / training lineage;
- staff / specialist team / contractor;
- transport / port / road / airspace;
- finance / market liquidity / common collateral;
- data / evidence / monitoring source;
- legal authority / decision-maker;
- public trust / communications channel.

Two different vendors are not independent if the same grid, upstream supplier, model family, port, staff pool or legal bottleneck can disable both.

```text
DIFFERENT_NAME != DIFFERENT_FAILURE_MODE
SEPARATE_UNIT != INDEPENDENT_DEMAND
SEPARATE_APERTURE != INDEPENDENT_EPISTEMIC_LINEAGE
```

### 3. Test concurrency: who else needs it in the same bad world?

The question is not whether the capacity exists on an average day.

Ask:

- Which other units, populations or systems can claim the same capacity?
- What event makes their demand rise at the same time as ours?
- Are local peaks usually asynchronous, or can they synchronize?
- Is the pooling benefit based on an independence assumption that disappears in the stress case?
- Has the same reserve been counted in several plans?

If everyone plans to borrow from the same neighbour, the neighbour is not a system-wide reserve.

### 4. Convert stock into flow: can the capacity arrive before the clock closes?

Ask:

- What has to happen between `capacity exists` and `capacity protects`?
- How long do detection, request, authorization, transport, setup, switching, staffing and delivery take under the stressed conditions?
- Can the event that creates the need also slow the delivery route?
- Is the quoted capacity firm under the relevant operating conditions, or non-firm/probabilistic?

For a consequential path `p`, the practical question is:

```text
T_deliver(shared_capacity, stressed_world) < T_harden(p)
```

Do not treat the expression as a measured law when the times are uncertain. The purpose is to expose a delivery-clock assumption.

### 5. Test regeneration: what is left after using the buffer?

A buffer is a stateful capability.

Ask:

- Does use consume stock, fatigue people, spend money, degrade equipment, exhaust political trust, consume review attention, or reduce future optionality?
- How long until the capacity is restored?
- What event could arrive before restoration?
- Does the response build future capability or consume it?

```text
CORRECTION_t -> CHANGES CORRECTION_CAPACITY_t+1
EVENT_ENDED != BUFFER_RESTORED
```

If the next plausible shock can arrive before regeneration, plan for a multi-event sequence rather than a clean single-event recovery.

### 6. Protect a local floor where pooling would otherwise erase recoverability

Pooling is often valuable. Local protection is often valuable. Neither should be maximised by default.

Ask:

- What minimum capability must remain locally and immediately accessible?
- What would become impossible to recover if this unit gives away its last local reserve?
- Which capabilities have rebuild/acquisition lead times longer than the correction window?
- Can shared capacity be used above a protected local floor rather than replacing the floor?

The answer may be zero in some domains and substantial in others. This route does not author the number.

### 7. Expose the collision before the pool saturates

If joint demand can exceed jointly deliverable capacity, an engineering model is no longer enough.

Ask before the emergency:

- Who has standing to claim the scarce capacity?
- Who has authority to allocate it?
- What priority rule, duty or public purpose governs allocation?
- Which minimums are non-tradable, if any?
- How are affected parties represented?
- Can the allocation be challenged or revisited quickly enough to matter?
- Who carries the burden of conserving, waiting, transferring or going without?
- What residue remains after the emergency allocation?

```text
CAPACITY_SHORTAGE -> ALLOCATION
ALLOCATION -> VALUE / STANDING / AUTHORITY
TECHNICAL_OPTIMUM != LEGITIMATE_PRIORITY
```

This card reveals the collision. It does not solve moral pluralism, standing, floor-grounding or distributive justice.

### 8. Build before the stress case arrives

Do not stop at `the backup is weak`.

Possible construction moves include:

- diversify by **failure lineage**, not vendor count;
- protect a local minimum while retaining a shared surge pool;
- increase firm/deliverable capacity rather than headline capacity;
- pre-position equipment, fuel, housing, spare parts or authority;
- train additional people before expertise is needed;
- preserve human verification skill while using automation;
- create independent sensing/evidence routes;
- reduce or shift demand in time;
- make mutual-aid release rules explicit before scarcity;
- shorten switching/transport/authorization latency;
- increase regeneration rate after use;
- remove a common bottleneck that makes otherwise separate reserves jointly unavailable.

A good result identifies **what to construct now**, not merely what could fail later.

## Small output

A useful return can usually fit in this form:

```text
CAPABILITY COUNTED:
SHARED / DEDICATED / BORROWED:
COMMON-MODE FAILURE:
SIMULTANEOUS CLAIMANTS:
DELIVERY CLOCK:
REGENERATION CLOCK:
LOCAL FLOOR AT RISK:
COLLISION / ALLOCATION OWNER:
BUILD-BEFORE-STRESS ACTION:
EVIDENCE THAT WOULD CHANGE THIS READING:
```

Do not fill fields that add no decision value. Plain prose is preferable when it carries the same distinctions with less burden.

## Stop / route rules

Stop this route and use the domain owner directly when:

- the domain already has a mature joint-capacity model that contains the relevant dependencies;
- no shared/borrowed capacity is material to the decision;
- the remaining question is a legal/clinical/engineering calculation outside the competence of this route;
- the decisive issue is priority/standing rather than capacity mechanics — route to the legitimate allocation owner while keeping the collision visible;
- further tracing would not change the next action and only produces a larger dependency map.

Do not infer that pooling is bad, local autonomy is good, redundancy must be dedicated, or every reserve needs a numerical correlation model.

## Worked pressure tests

### A. Multi-hospital ICU pooling

Owner evidence: Daudelin et al. (2026) finds hospital pooling can reduce ICU demand volatility through aggregation of imperfectly correlated patient demand and can flatten peaks when local epidemic waves are asynchronous. The same paper observes lower diversification benefit when ICU peaks become more synchronized. A separate 2026 hospital-bed governance model explicitly treats demand covariance as a determinant of the value of pooling and examines designs combining shared capacity with protected local reserve.

What this route changes:

- `POOL SIZE` is not enough; inspect demand correlation.
- patient transfer requires transport, receiving staff and clinical capability, not merely an empty nominal bed.
- fully centralising beds can create local-access and coordination costs even when pooling reduces mismatch.
- if the shared pool saturates, the problem becomes clinical/ethical allocation, not a covariance calculation.

Disposition: **USEFUL CROSS-DOMAIN ENTRY; DOMAIN OWNER STILL DOES THE REAL CAPACITY AND CLINICAL WORK.**

### B. Electricity system under heat + fast concentrated load growth

Owner evidence: IEA Electricity 2026 treats grid capacity as a major bottleneck and distinguishes firm from condition-dependent capacity. Current U.S. heat emergencies have required backup generation and higher reserve requirements while large concentrated loads such as data centres are expanding connection demand.

What this route changes:

- connection capacity, emergency reserve margin, transformers and dispatchable flexibility are shared correction resources;
- capacity that is connectable in normal conditions may be non-firm during stressed conditions;
- planning against speculative or double-counted demand can itself consume investment and planning capacity;
- a locally financeable load can alter what remains reachable for other loads when firm capacity is scarce.

Disposition: **USEFUL FOR EXPOSING SHARED-CAPACITY CLAIMS; GRID RELIABILITY/CONNECTION DECISIONS REMAIN WITH SYSTEM OPERATORS AND REGULATORS.**

### C. Strategic oil stocks during a transport/refining shock

Owner evidence: OECD's 2026 energy-shock analysis says strategic stocks are important buffers but large headline inventories do not guarantee immediate market relief because refinery capacity, tanker availability and product bottlenecks limit conversion of stocks into usable supply.

What this route changes:

- barrels in storage are not barrels/day delivered to the affected economy;
- reserve-release plans can share the same refinery, tanker, port or product bottleneck;
- long disruptions consume the buffer and create a regeneration problem;
- country-level coverage can diverge sharply, making allocation and burden international as well as technical.

Disposition: **USEFUL `STOCK -> FLOW -> COLLISION` CHECK; ENERGY SECURITY OWNERS PROVIDE THE ACTUAL MODELS.**

## What this draft is testing

The draft survives only if real users or cases show that it catches a material cross-domain omission before the owner-native method is reached, or helps identify the correct owner/problem sooner.

Delete, absorb or reduce it if it merely paraphrases ordinary contingency planning.

A strong falsifier is:

> Given a real capacity-dependent decision, competent ordinary/domain reasoning reliably notices the same common-mode, concurrency, delivery, regeneration and allocation issues with equal or lower burden.

No claim of novelty is made.

## External owner anchors used for this draft

- D. D. Woods, theory of graceful extensibility / sustained adaptability.
- R. I. Cook & B. A. Long, adaptive-capacity sharing in technical incident response, *Applied Ergonomics* (2021): https://pubmed.ncbi.nlm.nih.gov/32927402/
- Daudelin et al., hospital capacity pooling / diversification mechanisms, *Risk Analysis* (2026): https://onlinelibrary.wiley.com/doi/full/10.1111/risa.70329
- `Designing Governance Boundaries for Hospital Bed Management` (2026): https://www.mdpi.com/2227-9032/14/13/1949
- Nature Climate Change, `Infrastructure links amplify impacts` (2026): https://www.nature.com/articles/s41558-026-02747-1
- IEA, *Electricity 2026 — Grids*: https://www.iea.org/reports/electricity-2026/grids
- IEA, *Electricity 2026 — Flexibility*: https://www.iea.org/reports/electricity-2026/flexibility
- OECD, 2026 energy-shock resilience analysis: https://www.oecd.org/en/publications/oecd-economic-outlook-volume-2026-issue-1_2d1956f0-en/full-report/from-energy-shocks-to-stronger-resilience_761a5995.html
- WHO, ethics of health research priority setting: https://www.who.int/publications/i/item/9789240110953

## Boundary

This draft does not alter TRACE, Mechanical Ethics, Campfire, Square authority, release state or canon. It is a reversible field route built from current world pressure and external owner work.
