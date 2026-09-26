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
