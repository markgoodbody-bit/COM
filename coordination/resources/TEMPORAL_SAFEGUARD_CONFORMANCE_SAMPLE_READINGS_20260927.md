# Temporal safeguard conformance — sample public readings

Date: 27 September 2026

Status: **METHOD EXERCISE / PUBLIC AGGREGATE EVIDENCE / NOT CASE VERDICTS / NOT VALIDATION**

Purpose:

Check whether the working temporal-safeguard conformance audit can produce bounded, non-scalar readings on real systems.

Audit:
`coordination/resources/TEMPORAL_SAFEGUARD_CONFORMANCE_AUDIT_v0_20260927.md`

These are **system/evaluation-surface profiles**, not determinations about one named patient, tenant, trust or landlord.

---

## Reading A — NHS PIFU

Stronger owner:
NHS England PIFU guidance v2, September 2025.

Implementation evidence:
2026 rapid qualitative staff evaluation across five English NHS Trusts plus wider staff workshop.

### Conformance profile

| Stage | Status on available evidence | Why |
|---|---|---|
| SPECIFIED | **OBSERVED** | National guidance defines suitability, safety nets, tracking, review/end dates, return to timed pathways, incident learning and access safeguards. |
| TRIGGERED | **PARTIAL** | PIFU depends partly on patients recognising/initiating appropriate contact; staff described some patients failing to initiate when needed. |
| ROUTED | **PARTIAL** | PIFU contact routes exist, but implementation and EPR/administrative handling varied; some primary-care spillover was reported. |
| CLOCK_STARTED | **PARTIAL / LOCAL** | National guidance expects target wait times; some specialty guides specify explicit response targets, while implementation is locally led. |
| OWNER_ASSIGNED | **PARTIAL** | SOPs and local roles should define ownership; evaluation reported variable roles and administrative arrangements. |
| ACTED | **PARTIAL** | Services did act on PIFU contacts, but staff described variability and some long waits after activation. |
| REACHED | **PARTIAL** | Intended timely access is not guaranteed merely by successful patient activation; evaluation describes cases where waits remained. |
| CURRENT | **OBSERVED IN DESIGN / IMPLEMENTATION UNKNOWN** | Guidance requires review/end dates, clinically required reviews and updated PIFU windows. Public evaluation does not establish uniform conformance. |
| RESOLVED | **UNKNOWN AS A GENERAL CLAIM** | Available evidence does not justify a population claim that PIFU resolves the relevant follow-up need across settings. |
| RESIDUE | **OBSERVED** | Administrative workload, changed clinical intensity and possible GP workload displacement were reported. |

### What the audit adds

Not a new PIFU requirement.

It keeps three layers separate:

~~~text
PIFU OFFERED
!=
PIFU SAFELY SUITABLE FOR THIS PERSON

PIFU ACTIVATED
!=
TIMELY SPECIALIST ACCESS REACHED

CLINIC FOLLOW-UP WORK REDUCED
!=
TOTAL WORKLOAD REDUCED
~~~

### Route

**STRONG OWNER / IMPLEMENTATION-CONFORMANCE QUESTION / NO PROJECT POLICY OBJECT.**

---

## Reading B — Awaab's Law Phase 1

Stronger owners:
- Awaab's Law regulations/guidance;
- MHCLG;
- Housing Ombudsman.

Implementation evidence:
2026 Phase 1 Test-and-Learn qualitative research, fieldwork December 2025 to March 2026.

### Conformance profile

| Stage | Status on available evidence | Why |
|---|---|---|
| SPECIFIED | **OBSERVED** | Phase 1 defines hazard/notice routes, investigation/work clocks, written summaries, updates and accommodation requirements. |
| TRIGGERED | **PARTIAL** | Tenant/landlord evidence showed variable first-contact recognition, especially vulnerability and hazard assessment. |
| ROUTED | **PARTIAL** | Research found fragmented case handling in some experiences; landlords were still refining triage/escalation/end-to-end management. |
| CLOCK_STARTED | **PARTIAL** | Landlords reported ambiguity around definitions and when statutory clocks start; guidance/Phase 2 work responds to this. |
| OWNER_ASSIGNED | **PARTIAL** | Some organisations moved toward end-to-end case ownership, while absence of a single point of contact was reported by tenants. |
| ACTED | **PARTIAL** | Emergency hazards were often dealt with quickly; damp/mould cases could stall between inspection and remediation. |
| REACHED | **PARTIAL** | Some tenants described clear follow-through; others reported delays, missed updates and incomplete written summaries. |
| CURRENT | **PARTIAL** | Material-change logic exists in owner guidance; the research still found vulnerability/current information inconsistently recorded or operationalised. |
| RESOLVED | **PARTIAL** | Some cases progressed well; other tenants described deadlines/initial responses without durable resolution. |
| RESIDUE | **OBSERVED** | Capacity, contractor, workforce and IT constraints remained; compliance pressure could displace longer-term maintenance/investment. |

### What the audit adds

Again, no new housing rule.

It makes the execution chain explicit:

~~~text
LAW IN FORCE
!=
TRIGGER RECOGNISED

TRIGGER RECOGNISED
!=
CLOCK OPERATIONALISED CONSISTENTLY

TIMESCALE ACTIVITY
!=
DURABLE FIX

CASE CLOSED / STEP COMPLETE
!=
HAZARD GONE
~~~

### Route

**STRONG OWNER / REAL EARLY CONFORMANCE GAP / OUTCOME + IMPLEMENTATION OWNER.**

---

# Cross-reading result

The working audit can describe materially different systems without forcing them into one score.

It also produces different routes:

~~~text
PIFU:
DESIGN STRONG
-> LOCAL FIDELITY / ACCESS / BURDEN WATCH

AWAAB PHASE 1:
LEGAL DESIGN STRONG
-> TRIGGER / CLOCK / CASE-MANAGEMENT / CAPACITY CONFORMANCE WATCH
~~~

This is the intended behaviour.

## Falsification result so far

The audit survives this narrow use because it:
- did not invent a missing policy in either case;
- separated specification from implementation;
- exposed different failure stages;
- retained the stronger domain owners;
- kept outcome/residue visible after compliance steps.

But:

~~~text
TWO SYSTEM-LEVEL READINGS
!=
CROSS-DOMAIN VALIDATION
~~~

Further use should continue only on real cases where the conformance layer could change routing.

Current disposition:

**METHOD SURVIVES TWO BOUNDED APPLICATIONS / NO VALIDATION / NO TRACE OR ME PATCH.**
