# WORLD / REAL USE — HMRC statistics correction-propagation owner pass

Date: 20 September 2026 — Europe/London

Status: **OWNER FOUND / NO THR RECORD / NO NEW TYPE / NO ME-TRACE PATCH**

## World pressure

HMRC published `HMRC Statistics: Raising our performance` on 15 September 2026
after two major errors in autumn 2025 propagated into downstream market-sensitive
statistics produced by ONS and HMT.

Bounded cases in the owner report:

1. VAT receipts:
   - £2.4bn upward correction for Apr-Aug 2025;
   - downstream effect on joint ONS/HMT Public Sector Finances;
   - HMRC exceptional release and joint ONS/HMT correction on 8 Oct 2025.

2. Trade in goods:
   - approx £5.1bn upward revision to 2024 exports and £6.5bn for Jan-Oct 2025;
   - downstream effects on ONS UK Trade, GDP and other trade releases;
   - correction announced Nov 2025 and published with ONS Jan 2026.

The report also identifies direct HMRC data feeds into ONS as a separate assurance
problem and recommends a specific cross-department process for communicating errors.

## Strongest owner

HMRC / ONS / HMT / Office for Statistics Regulation already own:
- source statistical production;
- downstream dependency/use;
- correction publication;
- quality assurance;
- interdepartmental notification;
- distinction between errors and routine revisions;
- future assurance recommendations.

The owner report explicitly maps correction consequences across departmental
publication boundaries.

## Project delta

Useful transferable compression:

```text
UPSTREAM ERROR
-> DOWNSTREAM MARKET-SENSITIVE PUBLICATIONS
-> CORRECTION ROUTING
-> COORDINATED PUBLICATION / COMMUNICATION

ERROR != ROUTINE REVISION
SOURCE CORRECTED != DOWNSTREAM CONSEQUENCES AUTOMATICALLY CLOSED
```

But no THR object or generic dependency machinery is earned.

Why:
- the strongest domain owners already preserve the material correction chain;
- THR would mostly duplicate an active official accountability record;
- the case does not expose a missing THR semantic distinction beyond existing
  source ancestry / correction / downstream-impact concepts;
- the `ERROR != ROUTINE REVISION` distinction is domain-owned and does not
  justify a new global THR state.

ME / TRACE:
- the case is representable as upstream change, downstream burden, correction
  routing, ownership and clocks;
- successful representation does not earn a wording or formal patch.

## Result

```text
OWNER FOUND = YES
THR RECORD 5 = NO
THR TYPE/SCHEMA DELTA = NO
ME PATCH = NO
TRACE PATCH = NO
PROJECT LESSON = PRESERVE CORRECTION FAN-OUT + ERROR/REVISION DISTINCTION WHEN MATERIAL
```

No external contact.
No account.
No institutional request.
