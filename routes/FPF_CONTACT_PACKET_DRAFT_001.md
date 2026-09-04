# FPF contact packet — draft 001

**Status:** PREPARED / NOT SENT / NO FPF ISSUE OR PR CREATED
**Date:** 2026-08-29
**Last identity verification:** 2026-08-29; FPF `main` still resolves to the compared commit
**Intended channel:** one bounded GitHub issue in `ailev/FPF`, because issues are enabled and no Discussions or contribution/governance file was observed
**Purpose:** ask for correction of a bounded external reading; not validation, endorsement, conformance, integration, or source change

## 1. Frozen identities

FPF object actually read:

```text
repository: ailev/FPF
commit:     72222c13cc1bba009f1ee1f1aca47654db8e5716
file:       FPF-Spec.md
Git blob:   1ce815ab5037924f11e3739db06ca24bf889f10d
SHA-256:    7d7e55c84cfff2b152eeea5f1254b78e209cffc27f05482205990c3aaa5d153b
bytes:      13,809,254
```

TRACE object presented for criticism:

```text
repository: markgoodbody-bit/TRACE
commit:     8635438c7d5cd600dd2c8d50322353e59d27b70e
file:       PROJECT/TRACE_v0_3_0_SPINE_CANDIDATE_v0_11.md
Git blob:   1ae5e8b8640b9506db585599a6cae5192087d870
SHA-256:    de35637f1a6db1648f725db0e533c4b4f8e2eb1f40c817ed24de9039e1525084
bytes:      25,355
PR:         https://github.com/markgoodbody-bit/TRACE/pull/38
```

ME object presented for criticism:

```text
repository: markgoodbody-bit/mechanical-ethics
commit:     a27319fdab9a8dbb0b2d0ac58dddc61fba8aca43
file:       work/v0_7_0/MECHANICAL_ETHICS_HUMAN_READER_v0_7_0_NEXT_WORKING_CANDIDATE_v0_2.md
Git blob:   2fba2371099a5f8dd1cf6e04ee3a90f2ce7798cc
SHA-256:    56b09d5a1f7f0db5102ad47a636c60273cd2ddc325d216b4414e5359f21604a7
bytes:      87,177
PR:         https://github.com/markgoodbody-bit/mechanical-ethics/pull/34
```

No `LICENSE` file or GitHub-detected licence was observed in the pinned FPF
repository. We have therefore not identified a reuse grant and are treating
copying, adaptation, redistribution or product packaging as unresolved pending
clarification. Source-level comparison and citation are not being treated as a
reuse permission.

## 2. Proposed issue title

```text
Request for correction: bounded external reading of FPF against TRACE / Mechanical Ethics
```

## 3. Proposed issue body

We have been testing two working projects against FPF rather than
assuming they are novel or compatible:

- **TRACE** is a structural reading/packet grammar for exposing boundaries,
  claims, evidence, routes, clocks, burden, residue and unresolved structure.
- **Mechanical Ethics (ME)** is a human normative argument about timely
  protection, usable routes, burden placement, answerability and residue. It
  does not supply a complete priority rule, theory of standing, collision
  resolver or enforcement authority.

We read `FPF-Spec.md` at commit
`72222c13cc1bba009f1ee1f1aca47654db8e5716` (blob
`1ce815ab5037924f11e3739db06ca24bf889f10d`). We are not asking FPF to
validate, adopt, endorse or become compatible with either project.

Our current adverse/narrow findings are:

1. We established **zero TRACE-unique semantic primitives** in the comparison.
2. FPF A.10 and neighbouring reliance/publication machinery appear to recover
   the practical evidence/access/custody/disclosure distinction that TRACE
   states compactly.
3. FPF A.2.9 plus A.10 appear to recover the ceiling that response or silence
   alone does not establish meaning, cause, authority, consent or permission.
4. FPF C.27/C.27.TA and neighbouring window, constraint, resource, evidence and
   reopen machinery appear to contain most ingredients of TRACE's
   correction-window construction. TRACE may still provide a useful compiled
   cross-domain product, but we no longer treat that as a novel timing
   principle.
5. A 32-call TRACE comparison established execution and material carrier burden,
   but no efficacy disposition. The compact-carrier/base median total byte
   ratio was [`2.798448`](https://github.com/markgoodbody-bit/TRACE/blob/8635438c7d5cd600dd2c8d50322353e59d27b70e/PROJECT/TRACE_v0_3_0_OUTWARD_API_EXECUTION_RESULT_20260829_v0_2.md);
   blind adjudication did not complete.
6. A 100-item hostile ME↔FPF audit did not earn an FPF-native plug-in, DPF, LPF or
   conformance claim. At most, a loose external normative companion survives
   with material narrowing.
7. In the bounded RAIB-2 case comparison, the ME aperture changed no concrete
   action, constraint, evidence demand, stop or reopen condition beyond the
   FPF-only reading. We retained that adverse result as `ME_NOT_NEEDED`; the
   reviewer had prior exposure to expected ME pressures, so it is warm,
   contaminated evidence rather than a cold primary result.

The shortest supporting records are the [TRACE nearest-neighbour
disposition](https://github.com/markgoodbody-bit/TRACE/blob/8635438c7d5cd600dd2c8d50322353e59d27b70e/PROJECT/TRACE_v0_3_0_FPF_NEAREST_NEIGHBOUR_DISPOSITION_20260828_v0_1.md),
the [TRACE readiness audit](https://github.com/markgoodbody-bit/TRACE/blob/8635438c7d5cd600dd2c8d50322353e59d27b70e/PROJECT/TRACE_v0_3_0_READINESS_AUDIT_20260829_v0_1.md),
the [ME hostile audit](https://github.com/markgoodbody-bit/mechanical-ethics/blob/a27319fdab9a8dbb0b2d0ac58dddc61fba8aca43/work/v0_7_0/ME_FPF_COMPATIBILITY_FALSIFICATION_X100_20260828.md),
and the [RAIB-2 adverse comparison](https://github.com/markgoodbody-bit/mechanical-ethics/blob/a27319fdab9a8dbb0b2d0ac58dddc61fba8aca43/work/v0_7_0/ME_FPF_MIDDLE_OUT_RAIB2_COMPARISON_20260829.md).
They are optional; the questions below are intended to stand on their own.

Could you correct us on four bounded questions?

1. Are any of the three FPF readings above materially wrong—especially our use
   of A.10, A.2.9 and C.27/C.27.TA?
2. If TRACE is retained only as a compact external compilation of these
   distinctions—not as novel semantics—is FPF's nearest category a specialised
   view/profile/publication, or is even that framing misleading?
3. Is it accurate that FPF can represent standing, burden allocation,
   non-beneficiary closure, collisions and protection floors without itself
   settling ME's normative claims about them? If not, which exact governing
   pattern settles one of those claims or shows that we have misplaced it?
4. What licence/reuse terms govern `FPF-Spec.md`? We found no repository
   licence and will not copy or adapt FPF text into another product without an
   explicit basis.

A short answer naming a mistaken pattern reading or the first exact FPF locator
is enough. We would rather record a null or correction than create an
interoperability layer by momentum.

## 4. Further material only if requested

Do not make the maintainer read the full project quarry before answering.
Provide these only if requested:

1. TRACE full nearest-neighbour crosswalk;
2. TRACE legacy casebook architecture reanalysis;
3. ME 100-item hostile compatibility audit;
4. ME bounded RAIB-2 comparison;
5. exact candidate/source identities and line-level citations.

## 5. Send gate

Before sending:

```text
[ ] Mark approves the issue body and sender identity
[ ] FPF main head is reacquired; pinned comparison identity remains disclosed
[ ] no newer FPF contribution/contact instruction supersedes GitHub issues
[ ] links resolve to immutable or clearly labelled working objects
[ ] no claim says FPF validated, endorsed or authorized TRACE/ME
[ ] no FPF text is copied beyond short cited phrases needed for criticism
[ ] burden remains one issue / four questions / no unsolicited PR
```

After sending, preserve the exact issue URL and body in COM. Treat silence as no
observed response, not refusal, agreement or permission.
