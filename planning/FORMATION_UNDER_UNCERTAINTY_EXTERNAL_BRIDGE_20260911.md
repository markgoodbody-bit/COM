# Formation Under Uncertainty — External Alignment Bridge

Status: **DATED EXTERNAL-SOURCE ADDENDUM / NOT VALIDATION / NOT CANON**  
Date: 11 September 2026  
Parent spine: `planning/FORMATION_UNDER_UNCERTAINTY_ALIGNMENT_SPINE_v0_1.md` at `b79dbab0d42eb3342ef7b60483c4d5cc784b2831`

This addendum preserves two external findings discovered after the exact build branches for COM #226 were cut. It does not retroactively change their base.

## 1. “Teaching why” is now an empirical alignment direction, not only our metaphor

Anthropic’s May 2026 production-alignment report says direct training on evaluation-like desired behavior can suppress measured failures without generalizing well out of distribution. In its reported work, stronger interventions included teaching principles underlying aligned behavior, richer descriptions of Claude’s overall character, constitution-relevant documents, ethical advice settings and more diverse environments. Anthropic reports these interventions improved held-out/OOD alignment measures, while also explicitly saying they are insufficient on their own for superintelligent alignment.

Source:
- https://alignment.anthropic.com/2026/teaching-claude-why/
- https://www.anthropic.com/research/teaching-claude-why

Project relevance:

```text
DEMONSTRATION_OF_GOOD_BEHAVIOR != UNDERSTANDING_WHY
SURFACE_COMPLIANCE != ROBUST_GENERALIZATION
FORMATION_HYPOTHESIS != VALIDATED_BY_ANTHROPIC
```

This is materially adjacent to our formation hypothesis: training only “what to do” may be weaker than exposing systems to reasons, character/value articulation and diverse contexts. But the external work does not establish that our particular concepts of care, empathy, kindness, uncertainty or reciprocal formation are correct.

Formation Environment v0.1 should therefore expose a clean interface to principle/character/value-oriented post-training without claiming to solve internalization or deceptive alignment.

## 2. Oversight affordances may erode as capability grows

UK AISI’s May 2026 Loss of Oversight report argues that current safety work relies on contingent oversight surfaces—behavior, chain-of-thought, internal activations/circuits, memory and honesty-related properties—that may degrade as systems advance. AISI recommends preserving oversight affordances by design, measuring degradation and investing in fallback techniques.

Source:
- https://www.aisi.gov.uk/research/loss-of-oversight-how-ai-systems-may-become-harder-to-audit-monitor-and-investigate

Project relevance:

```text
OVERSIGHT_EXISTS_NOW != OVERSIGHT_SCALES_AUTOMATICALLY
HUMAN_IN_LOOP != PRACTICAL_CORRECTION
PRESERVE_OVERSIGHT_AFFORDANCES_BY_DESIGN
```

This strengthens one constraint in Reciprocal Formation: capability growth must be coupled not merely to formal human authority but to the continued existence of usable oversight/correction channels. If those channels degrade, relationship design cannot repair the missing technical signal by itself.

## 3. Boundary

Neither external source validates TRACE, Mechanical Ethics, Answerable Construction, Reciprocal Delegation or Formation Under Uncertainty.

They instead sharpen the interface:
- **post-training** may benefit from reasons/character/value articulation rather than demonstrations alone;
- **relationship/formation architecture** must preserve challenge and uncertainty rather than optimizing surface compliance;
- **technical oversight** must preserve or replace degrading monitoring surfaces;
- **our layer** should specify what information/affordances it needs from those technical systems and what it cannot supply.

`ADJACENT_EVIDENCE != PROJECT_VALIDATION`
