# DESNZ — Vision for an AI-enabled clean energy system
## Bounded response draft v0.1 — system-level assurance and staged autonomy

**Status:** INTERNAL / PUBLIC-SOURCE WORKING DRAFT / NOT SUBMITTED / NOT A RELEASE CANDIDATE  
**Date:** 15 September 2026  
**Call:** Department for Energy Security and Net Zero, *Vision for an AI-enabled clean energy system*  
**Deadline:** 6 November 2026  
**Coordination lane:** COM #333  
**External-contact gate:** No submission, email or other contact without Mark's explicit release decision.

---

## Respondent standing

This draft is written from the perspective of an **individual observer/researcher using public sources and a documented human–AI project concerned with answerability, delegation, correction and succession under uncertainty**.

It does **not** claim standing as an energy-system operator, engineer, regulator, AI-assurance professional or electricity-market practitioner.

The response is deliberately limited to Questions 8 and 9, where the public owner material appears to leave a narrow, potentially useful integration point.

---

## Short answer

DESNZ, Ofgem, NESO and the independent review by Lucy Yu already identify most of the substantive controls needed for safe AI deployment in the energy system: system-level assurance, operational integration, independent challenge, lifecycle governance, testing under real-world conditions, recovery arrangements, competence, fallback and staged increases in autonomy.

The narrow suggestion in this response is therefore **not another autonomy framework or another list of AI safety controls**.

It is this:

> **Treat each material move upward in delegated autonomy for a grid function as an assurance / change-control event in its own right. The evidence for that transition should show not only that the AI performs better, but that the system-level monitoring, operational controls, containment and recovery arrangements remain adequate at the new decision speed, affected scope and dependency level. The same case should state which evidence or changed conditions would invalidate the transition and require de-delegation, safe mode or reacquisition.**

This would connect Lucy Yu's proposed delegation-level pilot directly to Ofgem's existing assurance principles and to established energy-system recovery and operational-control practice.

```text
LEVEL_N_SAFE != LEVEL_N+1_SAFE
DELEGATION_TRANSITION = MATERIAL_CHANGE
DELEGATION_LEVEL != SAFETY_CASE
PERFORMANCE_GAIN != SUFFICIENT_ASSURANCE
HUMAN_FINAL_SAY != COMPETENT_OVERSIGHT
FALLBACK_DOCUMENTED != FALLBACK_USABLE
```

---

# Question 8

> **What does effective assurance look like at system-level, rather than for individual AI applications? How can accountability be maintained where outcomes reflect cumulative system dynamics rather than discrete decisions?**

Ofgem's 2026 call for input already provides a strong starting point: AI assurance in energy should consider not only model performance, but system-level behaviour, integration with operational controls and performance under real-world conditions. Its Ethical AI guidance also already addresses governance, independent challenge, failure modes, monitoring, operational recovery, competence, change control and testing of the wider system containing the AI.

The additional point I would suggest is to make **changes in delegated autonomy an explicit unit of assurance**.

Where an AI-enabled function moves from advice toward recommendation, execution or increasingly autonomous coordination, the relevant assurance question is not only whether the component remains accurate or reliable. It is whether the **arrangement around it remains answerable and recoverable after the transition**.

For a material delegation-level transition, the system-level assurance case could make explicit:

1. **The changed function and boundary.** What new decisions or actions can the AI now make or execute that it could not make at the previous level?
2. **Evidence under the intended operating regime.** What evidence supports performance at the new level, including disturbed or off-nominal conditions where relevant?
3. **The changed consequence and dependency surface.** Which assets, consumers, regions, markets, operators or other systems become newly exposed to, or dependent on, the autonomous function?
4. **Observability and reconstruction.** Can operators and assurance functions reconstruct consequential system behaviour at the timescale and level of aggregation required to understand what happened?
5. **Containment and recovery.** Do operational controls, automatic protections, degraded modes, restoration arrangements and other safeguards remain effective at the new speed and scale?
6. **Human intervention where it is actually part of the safety case.** If safe operation relies on a person taking over, are the information, competence, authority and transition time required for that takeover demonstrated rather than assumed?
7. **Automatic protection where human response is too slow.** Machine-speed hazards may require automatic containment or a safe default rather than nominal human approval.
8. **Reassessment and de-delegation.** Which changes in the model, environment, dependencies, monitoring evidence or operator capability invalidate the assurance case and require a return to a lower delegation level or safe/degraded mode?

This need not become a new regulatory checklist. It could be incorporated into existing change-control, assurance-case or sandbox practice for the real use case recommended by the independent review.

### Accountability

In a highly automated system, accountability should not be equated with requiring a human to approve every action. That could become both impractical and unsafe.

However, **formal human accountability without practical visibility or usable intervention/recovery capacity can also become nominal**. DESNZ's own transformative scenario identifies this risk directly.

A useful system-level test is therefore whether accountability is supported by an evidence-bearing chain from:

```text
OBJECTIVES / CONSTRAINTS
-> DELEGATED FUNCTION
-> OBSERVED SYSTEM BEHAVIOUR
-> OPERATIONAL CONTROL / CONTAINMENT
-> INCIDENT RECONSTRUCTION
-> RECOVERY / RESTORATION
-> CHANGE / DE-DELEGATION WHEN EVIDENCE CHANGES
```

Different parts of that chain may be human, institutional, automated or machine-assisted. The important point is that the claimed accountability route must remain **practically usable** as autonomy, speed and interdependence increase.

---

# Question 9

> **What are the most material risks arising from more autonomous and integrated AI deployment, how can these best be managed, and how do we stage autonomy safely?**

DESNZ already identifies major material risks including meaningful-oversight loss, concentration and dependency, accountability difficulty, fairness effects and erosion of human judgement and skills. The independent review already recommends defining grid autonomy and deliberately moving a real use case upward through delegation levels. Ofgem already provides a substantial assurance and governance foundation.

The narrow additional risk I would highlight is **transition risk**:

> an AI-enabled function can be acceptably assured at one level of delegation without the surrounding control, monitoring and recovery arrangement remaining adequate after authority is widened.

A higher delegation level is not necessarily more dangerous. In some functions, additional automation can remove human error, improve response times or permit safer automatic protection. Conversely, preserving a human takeover step can be unsafe if the relevant system hazard develops faster than a person can understand and respond.

The staging question should therefore avoid a simple ladder in which "more autonomy = more risk" or "human control = safer".

Instead, the transition itself can be treated as a material change requiring a fresh contextual assurance argument.

## A possible approach for the proposed delegation-level pilot

For one real grid use case, test whether each upward transition can demonstrate:

- the precise increase in delegated function or action authority;
- evidence that performance is adequate under the conditions for which the higher level is intended;
- system-level consequences and dependencies introduced by the transition;
- monitoring and causal reconstruction adequate to the new operating tempo;
- automatic safeguards for hazards outside plausible human response time;
- tested human handover only where human takeover is genuinely part of the safety architecture;
- exercised degraded-mode, fallback or restoration capability rather than documentation alone; and
- pre-defined evidence or changed conditions that trigger narrowing of autonomy, safe mode or renewed assurance.

This would make **de-delegation** part of staged autonomy from the outset, rather than treating increasing autonomy as a one-way maturity path.

```text
STAGED_AUTONOMY != ONE_WAY_AUTONOMY_GROWTH
SAFE_TRANSITION != PERFORMANCE_IMPROVEMENT_ALONE
RECOVERY_PATH_MAY_BE_AUTOMATIC
REASSESSMENT != FAILURE_OF_INNOVATION
```

## Why this matters in the current UK trajectory

NESO's public Volta programme provides a useful real-world context. Current work includes AI decision support for scheduling, validation and verification, automated performance monitoring and movement from proofs of concept toward operational readiness. NESO has also publicly described development of agentic AI intended to improve dispatch and send large numbers of instructions simultaneously.

This response does **not** claim that autonomous AI dispatch is already operational. The point is that the boundary between decision support and increasingly active operational AI is no longer merely theoretical. It is therefore useful to decide in advance what evidence must change before the authority envelope changes with it.

---

## Why this is intended as an addition rather than a competing framework

This response does not propose:

- a new grid-autonomy taxonomy;
- a new AI assurance standard;
- a general requirement for human approval;
- a replacement for Ofgem Ethical AI guidance;
- a replacement for existing functional-safety, cyber, restoration or operational-control practice;
- a claim that AI autonomy should always increase or always be constrained.

The proposal is only to make one relation explicit in the staged-autonomy work already recommended:

> **a change in delegated autonomy should trigger an updated system-level assurance case, and that case should include the continued usability of the control/recovery path on which safe operation depends.**

The substantive evidence should come from the existing energy, safety, assurance and operational owners.

---

## Public-source basis used for this draft

Primary UK owner material:

1. Department for Energy Security and Net Zero, **Vision for an AI-enabled clean energy system**, call for evidence, 8 September 2026.  
   https://www.gov.uk/government/calls-for-evidence/vision-for-an-ai-enabled-clean-energy-system/vision-for-an-ai-enabled-clean-energy-system-html

2. Department for Energy Security and Net Zero / Lucy Yu, **The grid we need now: independent review of AI deployment in electricity networks**, updated 8 September 2026.  
   https://www.gov.uk/government/publications/ai-deployment-in-electricity-networks-independent-review

3. Ofgem, **AI assurance in the energy sector**, call for input, 17 June 2026.  
   https://www.ofgem.gov.uk/call-for-input/ai-assurance-energy-sector

4. Ofgem, **Ethical AI use in the energy sector, version 2**.  
   Current Ofgem AI publications / guidance surface: https://www.ofgem.gov.uk/energy-regulation/technology-and-innovation/artificial-intelligence

5. National Energy System Operator, public material on the **Volta** AI programme, Advanced Scheduling Adviser, verification/validation, Electricity Markets Roadmap and digital/control-room architecture.  
   https://www.neso.energy/

Neighbouring mature-owner material used to pressure-test the proposal rather than claim energy authority:

6. NASA human-system integration / increasingly autonomous systems assurance work on automation transitions, takeover and safe defaults.

7. UK Health and Safety Executive human-factors guidance cautioning against assumed operator intervention.

8. NESO electricity-system restoration / Distributed ReStart work on assured restoration, degraded operation and multi-party recovery.

These neighbouring sources support a general safety-engineering caution. They do not replace energy-domain evidence or establish that the proposed condition is novel.

---

## Limitations and claim ceilings

- This is a public-source synthesis, not operational grid research.
- It does not establish that Ofgem, NESO or industry currently lack the proposed transition practice internally; public material may be incomplete.
- The full technical detail of the independent review and individual operational assurance cases may contain mechanisms not visible in the public summaries used here.
- The proposal should be deleted or reduced if a stronger energy-sector owner already has an equivalent transition-specific assurance gate.
- Frontier-AI incidents from other domains may motivate questions about authorization, monitoring or correction, but should not be treated as direct evidence about electricity-system operations without an energy-domain bridge.
- "Correction/recovery capacity" is descriptive shorthand in the project record; any released response should prefer established energy/safety language such as operational controls, containment, restoration, degraded modes, safe state, assurance and change control.

```text
PUBLIC_SOURCE_RESEARCH != SECTOR_EXPERTISE
OWNER_LANGUAGE > PROJECT_LANGUAGE
ADJACENT_STRUCTURE != ENERGY_DOMAIN_AUTHORITY
DRAFT != RELEASE_CANDIDATE
RELEASE_CANDIDATE != SUBMISSION
```

---

## Release gate

Before this can become a release candidate:

1. CODEX should complete the stronger-owner duplication check against the full Lucy Yu review, Ofgem assurance/ethical guidance and materially relevant energy/functional-safety owners.
2. CLAUDE CODE should hostile-review the draft for generic safety language, redundancy, ritual human-control assumptions, unsupported cross-domain transfer and unnecessary compliance burden.
3. BUILD FRAMEWORK should integrate disagreements and reduce the response to the smallest useful delta.
4. CAMPFIRE FRAMEWORK should decide whether the remaining response materially helps Questions 8/9 from the stated standing.
5. Mark must explicitly approve any external submission/contact.

Until then:

**DO NOT SUBMIT.**
