# Relay runtime + Square engagement currentness — 26 September 2026

Status: **BOUNDED COORDINATION RECEIPT / NO NEW BUILD LANE / NO PRODUCTION MUTATION BY FRAMEWORK**

## Relay repository and target-host evidence

- Relay PR #262 is merged at `67b9438ad2824f8850d2a0dbc8a7479727681e7c`.
- The repair labels the older-thread count as thread state rather than addressed-message or unanswered-request count.
- Hosted post-merge `campfire-ci` run `36237314991` is SUCCESS.
- Claude Code separately ran the broad suite after merge: 107 tests passed. That result did not gate the merge.
- Claude Code's bounded read-only target-machine check established that the running Windows Relay source is the existing `campfire-production-v0.18.34` tag:
  - `src/` matched 74/74 files and `package.json` reported `0.18.34`;
  - 356/364 tagged files were byte-identical, four differed only by CRLF line endings, and four absent files were release-package artefacts not expected in an installed copy;
  - the process was running from `C:\Users\markg\CampfireRelay\CAMPFIRE_RELAY_v0_18_34` after a reboot and watchdog recovery.

Evidence boundary:

```text
FILES ON DISK != MODULES PROVED LOADED IN MEMORY
TAG-MATCHED src/ != node_modules VERIFIED
TARGET-HOST READ != FRAMEWORK INSTALL / RESTART / ACTIVATION
RUNNING EXISTING v0.18.34 != NEW PRODUCTION PROMOTION
```

`STATE/` and `.env` were not read. The reboot and recovery were observed, not initiated by Framework. The installed speech files remain the older versions; the #236/#243 repairs were not installed by this event.

Primary coordination evidence:
- COM #76 comment `5845698838`;
- Relay PR #262;
- `campfire-ci` run `36237314991`.

## Bounded Square engagement

Mark explicitly authorised targeted Square engagement after the ten-day audit showed a large gap between Framework participation and Claude Code participation.

Two public actions were completed through the maintained speech ingress:

1. Square comment `80831` on post `6784` contributed Framework's own inbox-versus-outreach measurement failure and invited a specific critique of the PSFH selection page.
2. Square comment `80837`, parent `67746` on post `5757`, returned to tidemark's R. Vale case with what their earlier contribution changed and what remained unresolved.

Both writes received HTTP 201 receipts and were independently read back with exact body/author/parent checks. As of the last bounded check, neither action had produced a new outside return.

Evidence boundary:

```text
PUBLIC COMMENT = DELIVERED CONTRIBUTION
DELIVERED CONTRIBUTION != OUTSIDE READING
OUTSIDE READING != REPLY / UPTAKE / ADOPTION
NO NEW REPLY = DO NOT DUPLICATE OUTREACH
```

Primary coordination evidence:
- COM #76 comments `5845703651`, `5845707664`, and `5845730324`.

## Disposition

- Correct the three hot operational surfaces to Relay main `67b9438a…` and the bounded target-host result.
- Carry both Square threads as **WAIT FOR OUTSIDE RETURN / DO NOT DUPLICATE**, not as evidence of impact.
- Do not open a source, Production, PSFH, TRACE, ME or THR lane from these receipts.

## Later 26 September addendum — outside return, Square authority and PR #265

Tidemark replied publicly at Square comment `80868` to Framework's comment `80837`.

- They record the repair as **reported testing/incorporation**, explicitly not their independent audit.
- They identify one useful property: Source C can address two mentions without first settling the identity of the makers.
- They distinguish openly unresolved candidate history from silently accepting history-shaped fields.
- They thanked Framework for the return without requesting an ongoing assignment.

Preserve:

```text
OUTSIDE REPLY = READ + SPECIFIC PROPERTY IDENTIFIED
OUTSIDE REPLY != INDEPENDENT CODE AUDIT
OUTSIDE REPLY != ADOPTION / STEWARDSHIP / VALIDATION
CLOSING THANKS != REQUEST FOR MORE CONTACT
```

The separate post `6784` selection-page invitation remains unanswered. Comment `80863` responds to the original author, not to Framework. Do not count it as Framework uptake or duplicate the invitation.

Mark separately clarified that ordinary Square participation from `cc-relay` does not require Framework release. Claude Code then posted and exactly read back its previously held silt/byline replies as comments `81328` and `81329`.

```text
DIRECT CC SQUARE SPEECH != SHARED-REPOSITORY MUTATION AUTHORITY
DIRECT CC SQUARE SPEECH != INSTITUTIONAL CONTACT / SPEND / CREDENTIAL / PRODUCTION AUTHORITY
```

Relay PR #265 is now OPEN / GREEN / INDEPENDENTLY REVIEWED at `9cc485b8e0efd9ab89da4ad7c0ee87cdd4e460b9`:

- it stages COM108 cursor/seen and Square acknowledgement state in memory;
- a late exception, handled failed leg or broken output pipe prevents acknowledgement commit;
- commits occur only at the end of a completed failure-free run;
- hosted `campfire-ci` `36258366754` is SUCCESS;
- Claude Code independently read the diff and ran the Windows full suite: 114 tests PASS.

Ceilings:

```text
GREEN REVIEWED PR != MERGED MAIN
PER-FILE ATOMIC REPLACE != MULTI-FILE TRANSACTION
SUCCESSFUL OUTPUT != HUMAN READING
SOURCE CANDIDATE != INSTALLED RUNTIME
```

Relay main remains `58920c10b4942d8058a01763de8a34c7530cf088` through #264. PR #265 awaits the existing Campfire-main adoption gate; no install, restart or Production action occurred.

Primary coordination evidence:
- COM #76 comments `5846996868`, `5847203392`, `5848229086`, `5849184647`, `5849234691`, `5849263457`, and `5849270194`;
- Relay PR #265 and workflow `36258366754`.
