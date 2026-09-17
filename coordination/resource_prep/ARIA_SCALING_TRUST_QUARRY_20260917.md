# ARIA Scaling Trust — bounded resource / owner-subtraction note

Date: 17 September 2026
Status: **RESOURCE ROUTE SURVIVES / NO PROPOSAL THESIS YET / NO APPLICATION OR CONTACT**

> HOW CAN WE MAKE A BETTER FUTURE?

This note preserves a funding route and one possible technical seam. It does **not** create a project merely because money is available.

## Current owner-source position

ARIA's live Scaling Trust funding page is accepting rolling proposals for Tracks 2 and 3. The current quarterly cut-off is **31 October 2026, 14:00 GMT**.

Programme scale:
- nearly £50m total programme funding;
- Track 2 Tooling: 4–6 teams, approximately **£200k–£2m** each;
- Track 3 Fundamental Research: research centres plus 4–12 smaller teams, approximately **£100k–£3m** each;
- individuals, universities, research institutions, companies, charities and public-sector research organisations may apply;
- UK-based applicants are a primary focus.

The February solicitation remains useful for scope/terms even though its first-call deadline is historical. It says:
- Track 2 includes requirement gathering, negotiation, security reasoning and verifiable reporting;
- requirement gathering explicitly includes turning fuzzy user requirements into a security policy/goal and interactive methods that extract missing details, resolve ambiguities and help users discover their goals;
- Track 3 includes open-ended Bluesky research;
- exploratory Track 3 projects are roughly **£100k–£300k**, for lean cross-disciplinary teams (described as 4–5 researchers or less), over roughly 6–18 months;
- funded foreground software under Tracks 2/3 must use permissive open licensing, specified as **MIT + Apache-2.0 dual licensing**; pre-existing/background IP remains owned by the applicant;
- proposal guidance allows up to 10 pages and asks for differentiation, risks/unknowns, milestones, team/time commitment, budget/IP and commercial hypothesis;
- ARIA usually prefers leads/key researchers spending at least 50%, ideally 80%, of their time on the project.

## Fit to the project — what survives

The programme thesis is unusually close to the project's broad alignment direction: multiple agents, different principals, negotiation, verification, privacy/plurality, and secure coordination without a single omniscient authority.

That thematic overlap is **not** enough for an application.

Current owner subtraction says generic versions of the most obvious ideas are already active:
- preference / requirement elicitation for LLM agents;
- formal and fuzzy preference representations for negotiation;
- LLM multi-agent consensus frameworks;
- repository-native intent/specification layers;
- contestability / authorization-binding protocols;
- generic contracting / negotiation / audit infrastructure.

Therefore do **not** pitch:
- "TRACE for multi-agent coordination";
- generic preference elicitation;
- generic negotiation agent;
- generic contestability or audit receipt layer;
- broad 'human values to machine policy' language without a falsifiable gap.

## Narrow quarry seam worth testing

Potential question — **not yet a proposal claim**:

> Can a requirement-capture component compile messy human instructions into a machine-negotiable security policy while preserving unresolved uncertainty, explicit refusal, withheld information, authority limits and conflicts as first-class states rather than silently filling them in?

Candidate invariants to test:

```text
UNKNOWN != ABSENT
UNRESOLVED != DEFAULT_PERMISSION
REFUSAL != MISSING_VALUE
WITHHELD != FALSE
PREFERENCE != AUTHORITY
NEGOTIABLE != MAY_BE_TRADED_AWAY
POLICY_COMPILED != HUMAN_INTENT_FULLY_CAPTURED
```

The potentially consequential gap is not extracting more preferences. It is whether policy compilation loses the very states that should prevent unsafe negotiation or false consensus.

Before build or proposal work, require evidence that existing owners do **not** already cover this exact boundary in a deployable/falsifiable form.

## Falsifiers

Kill or route this seam if:
1. a current security-policy/intent system already preserves these states and verifies their survival through negotiation;
2. ARIA-funded teams already own the same component;
3. the contribution reduces to a vocabulary/schema without measurable behavioural/security effect;
4. it requires TRACE/ME canon changes or project-purpose distortion to sound novel;
5. a team/time commitment cannot be made honestly;
6. the required MIT+Apache-2.0 foreground licensing conflicts with the intended deliverable or background-IP boundary.

## Practical resource disposition

**ARIA Scaling Trust: KEEP / HIGH UPSIDE / HIGH LOAD / OWNER-SUBTRACTION FIRST.**

Do not open an application portal, join a team list, contact ARIA, accept terms, commit Mark's time, name collaborators, or propose a budget without an explicit human gate.

Near-term order:
1. continue owner subtraction on the narrow requirement-capture seam;
2. if it survives, produce a one-page technical concept and hostile review it;
3. identify the minimum credible team and time commitment before writing a full proposal;
4. only then decide whether the 31 October cycle is worth Mark's application load.

## Resource portfolio comparison

- **BlueDot Rapid Grants:** fastest/lowest-load route for small compute/API needs; keep first for immediate burn relief.
- **Foresight Coordination & Accountability:** strong thematic fit, typical $30k–$100k; higher in-person/community expectation.
- **ARIA Scaling Trust:** much larger upside and unusually strong structural fit, but requires a genuinely differentiated R&D seam, team/time credibility and substantial proposal work.
- **OpenAI Codex for Open Source:** only where an actually licensed, maintained OSS vehicle truthfully fits the maintainer programme; public repo alone is insufficient.

```text
FUND_FIT != PROJECT_GAP
THEMATIC_OVERLAP != DIFFERENTIATED_CONTRIBUTION
OWNER_FOUND -> STOP
RESOURCE_AVAILABLE != AUTHORITY_TO_APPLY
PROJECT_PURPOSE > FUNDING_PROGRAMME
```
