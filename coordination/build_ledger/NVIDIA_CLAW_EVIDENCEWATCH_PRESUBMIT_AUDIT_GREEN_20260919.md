# NVIDIA Claw EvidenceWatch — pre-submit audit GREEN — 19 September 2026

Status: **PRE-SUBMIT AUDIT COMPLETE / ONE UNATTENDED SCHEDULER WITNESS + VIDEO REMAIN**

Relay PR #248 current audit head:
`ee362ce0105565815ad2695f12db0481fab5f638`

Hosted:
`campfire-ci 1598 / 35452177273 — SUCCESS`

## Audit findings repaired

1. **Private repository visibility**
   - Campfire Relay is private.
   - Previous GitHub project-link fallback would not be judge-accessible.
   - Submission strategy changed to public YouTube/Loom demo rather than making Campfire Relay public by momentum.

2. **Internal Airtable form map in competition branch**
   - contained Mark's submission email and internal coordination details;
   - removed from judge-facing branch;
   - mapping remains preserved in COM.

3. **Stale rules/T&C state**
   - challenge brief/submission docs still said terms unresolved after Mark supplied them;
   - corrected to reference completed rules review.

4. **Broken documented scheduler command**
   - README documented `npm run live`;
   - package did not expose `live`;
   - repaired: `live -> node src/live.mjs`;
   - scheduler now refreshes watch config append-only on startup.

5. **Standalone-export data hygiene**
   - competition-local `.gitignore` added:
     - `.env`
     - `.env.*`
     - `data/`
     - `*.log`
   - root ignore already protected data, but standalone export now carries its own guard.

6. **Third-party attribution**
   - explicit Anthropic source + NVIDIA provider/model attribution added;
   - deterministic fixture distinguished from live source text;
   - no third-party content ownership claim.

7. **Secret/PII static diff check**
   - no NVIDIA-key-like strings;
   - no Bearer credential strings;
   - no real submission email remains in final branch diff;
   - only deliberate test fixture email `test@owner.test`.

8. **Current docs**
   - README updated to live-witnessed evidence ceiling;
   - private-repo visibility stated;
   - unusable private project-link suggestion removed from submission copy.

## Publication disposition

Do **not** make Campfire Relay public for this contest by momentum.

Registered form accepts:
`demo video OR project link`.

Preferred:
- unlisted/public-by-link YouTube or Loom video;
- no public code publication required.

A separate public EvidenceWatch code surface remains possible later but would require an explicit publication/licence decision.

## Remaining technical check

Challenge specifically asks for a long-running agent that operates without babysitting.

Current evidence:
- two separate live process runs: PASS;
- scheduler code exists and is now runnable;
- unattended scheduler itself has not yet been live-witnessed.

One bounded unattended scheduler witness is therefore earned before recording.

## Remaining gates after scheduler witness

1. record 60–90 second demo;
2. inspect video for secrets/personal data;
3. inspect exact Job Role / Industry dropdown choices if needed;
4. paste final Airtable payload;
5. Mark checks Official Rules box;
6. Mark submits.

```text
ENGINE FEATURE CHURN = STOP
PRE-SUBMIT AUDIT = GREEN
PUBLIC REPO = NOT REQUIRED
UNATTENDED SCHEDULER WITNESS = NEXT
VIDEO = AFTER THAT
SUBMISSION = NOT YET
```
