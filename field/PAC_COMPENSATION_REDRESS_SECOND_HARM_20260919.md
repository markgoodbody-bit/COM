# PAC government compensation schemes — redress as a second harm surface — 19 September 2026

Status: **FIELD WITNESS / OWNER-GROUNDED / CROSS-SCHEME CORRECTION PRESSURE / NOT TRACE OR ME CANON**

> HOW CAN WE MAKE A BETTER FUTURE?

## Trigger

The UK House of Commons Committee of Public Accounts published **Government compensation schemes**, Twelfth Report of Session 2026–27, on 9 September 2026.

Primary report:
https://publications.parliament.uk/pa/cm5902/cmselect/cmpubacc/88/report.html

Committee summary:
https://committees.parliament.uk/committee/127/public-accounts-committee/news/217740/system-failure-in-govt-compensation-schemes-pac-joins-victims-in-call-for-change/

The report examines operational experience across prominent government compensation / financial-recognition schemes, including Windrush, Post Office Horizon, LGBT Financial Recognition and Infected Blood.

This record treats the PAC / NAO / scheme owners as the domain owners. It does not infer one common legal cause, culpability or remedy across all schemes.

## Evidence boundary

The PAC survey is useful but not a representative population sample.

- 572 people responded.
- The survey was disseminated through organisations representing or supporting people with relevant scheme experience.
- Infected Blood Compensation Scheme applicants formed the majority of respondents.
- Respondents were not asked to describe the circumstances that led to their compensation claim because of the sensitive and potentially retraumatising subject matter.

Therefore:

```text
SURVEY RESPONDENTS != ALL CLAIMANTS
REPEATED THEMES != POPULATION PREVALENCE ESTIMATE
CROSS-SCHEME PRESSURE != ONE SHARED CAUSE
```

The Committee also took oral and written evidence from victim representatives, experts and administering public bodies.

## Owner findings relevant to this project

The report concludes that:

1. **Same-body redress can undermine trust.**
   The Committee reports that compensation schemes are often designed or administered by bodies responsible for the original wrong. It recommends an independent body to design/administer future schemes.

2. **The correction process can itself create additional burden and distress.**
   Among PAC survey respondents, 76% reported the claim process as distressing or retraumatising.

3. **Evidence burden can be exported back to the harmed person.**
   The report says evidence can be excessive, outdated, difficult to obtain or already held by the body administering the scheme. 53% of survey respondents said evidence requested felt unreasonable or too difficult to provide.

4. **Delay and uncertainty are part of the consequence, not merely administrative latency.**
   Some claims have remained open for long periods; the Horizon Shortfall Scheme's longest settled claim cited by PAC took 1,395 working days. Respondents describe uncertainty about invitation, decision and payment times as anxiety-producing and closure-preventing.

5. **Communication/currentness is a correction mechanism.**
   The PAC reports that most victims are not given clear progress/timing information. 53% of survey respondents felt timescales and next steps were not regularly communicated, with a further 13% reporting that this seldom occurred.

6. **Local scheme learning does not guarantee institutional learning.**
   A cross-Whitehall network exists, but PAC says there is no permanent central body overseeing/retaining compensation-scheme knowledge and warns that lessons can be lost and mistakes repeated.

7. **Co-design is not equivalent to implementation fidelity.**
   The report records evidence that affected groups may participate in co-design but the delivered scheme can still diverge materially from what was discussed.

These are PAC findings / reported evidence, not independent Framework adjudications.

## Mechanical Ethics relation

The released Mechanical Ethics v0.7.0 already contains the relevant structures:

- formal availability != practical route usability;
- a route can demand proof work, delay, exposure or fear from the person seeking help;
- the process designer controls categories, evidence formats, clocks and escalation points;
- an independent reviewer may be necessary where the original decision-maker should not judge their own work;
- burden of complexity and delay should not automatically sit with the less-powerful affected person;
- collective correction should not force each isolated person to prove recurrence from zero;
- correction theatre occurs when the appearance of answerability improves faster than the next person's conditions;
- investigation / monitoring / recorded lessons != changed path;
- a correction arriving after hardening may remain truthful without restoring what was lost.

The PAC case therefore strengthens existing ME claims rather than exposing an immediate wording defect.

## TRACE relation

TRACE v0.3.0 can represent this case without a new primitive.

Conceptual mapping:

```text
E[victim]         = affected claimant / family / estate
E[originator]     = body whose action/inaction caused the original compensable harm
E[administrator]  = body controlling the redress route
E[independent]    = proposed / existing independent redress body where evidenced

PHI_0             = original harmful transition(s), domain-specific
ROUTE[c]          = compensation / redress route
PHI_c             = claim-process transitions
CLOCKS            = detection / entry / evidence / decision / payment / hardening clocks
BURDEN[victim]    = time, proof work, navigation, uncertainty, money, pain, exposure
RESIDUE[victim]   = lost time, health/fear/debt/avoidance or other evidenced persistence
C                 = coupling among claimant, administrator, record holders and decision authority
STREAM            = ordered cross-case observations
PATTERN           = common-mechanism hypothesis only where separately supported
```

The crucial representation is recursive:

```text
CORRECTION ROUTE
-> MAY ITSELF BE ZOOMED INTO
-> ACTIONS / DELAYS / RECORD CUSTODY / BURDEN TRANSFERS / NEW TRANSITIONS
```

Thus the route is not forced to remain a neutral arrow. If the correction process creates additional burden or harm, that is represented as new transition/burden state, not hidden inside a label called "appeal" or "compensation".

Existing TRACE guards also fit:

```text
ROUTE_LABEL_DIVERSITY != CORRECTION_INDEPENDENCE
VISIBLE_AUTHORITY != CONTESTABLE_AUTHORITY
ROUTE_TO_BRAKE != CORRECTION_COMPLETED
LOCAL_CASE_REPAIRED != GENERATING_MECHANISM_REPAIRED
LOCAL_CORRECTION + STREAM_PERSISTENCE != MECHANISM_CHANGE
TRANSFERRED_BURDEN != REMOVED_BURDEN
CORRECTED != RESIDUE_ZERO
```

## Falsification pressure

The case was used to ask:

1. Can ME distinguish a correction route from a usable correction route? **YES.**
2. Can ME see the route itself as burden/harm-producing? **YES**, through process/maze, complexity, delay/fear and Correction Theatre structures.
3. Can TRACE represent the correction route as a stateful object rather than a neutral edge? **YES**, route reification + recursive zoom.
4. Can TRACE record new burden created during correction rather than treating all burden as residue of the original event? **YES**, burden creation/transfer/relief are separate.
5. Can TRACE distinguish claimant payment / local resolution from correction of the mechanism producing repeated problems? **YES.**
6. Does either system establish that PAC's preferred institutional design is normatively correct? **NO.** Domain/policy selection remains outside TRACE; ME can reason about burden/answerability but does not substitute for public-law or compensation-policy expertise.
7. Does this case earn a new TRACE/ME primitive? **NO.**
8. Does it earn a released-baseline wording change? **NO CURRENT EVIDENCE.**

## Portable relation

```text
REDRESS OFFERED != REDRESS USABLE
REDRESS ROUTE != HARM-FREE ROUTE
PAYMENT / CASE CLOSURE != RESIDUE ZERO
LESSON RECORDED != LESSON RETAINED / APPLIED
SAME BODY CONTROLS HARM + REDRESS
  -> CORRECTION INDEPENDENCE NOT ESTABLISHED
```

The first four relations are strongly grounded by the report and existing project grammar.

The final relation is structural rather than an automatic moral verdict: same-body control is a reason to test independence/trust/contestability, not proof that every same-body scheme is invalid.

## Owner subtraction / disposition

PAC, NAO, the Post Office Horizon IT Inquiry, compensation-scheme administrators and affected-community organisations already own the compensation-policy / redress-design problem.

Project delta:

```text
NEW POLICY SOLUTION = NO
NEW TRACE/ME PRIMITIVE = NO
ME EMPIRICAL WITNESS = YES
TRACE TRANSFER / REPRESENTATION WITNESS = YES
CORRECTION-AS-SECOND-HARM FIELD CASE = KEEP
CANON PATCH = STOP
```

No external contact, political advocacy, submission, baseline change or release follows from this record.
