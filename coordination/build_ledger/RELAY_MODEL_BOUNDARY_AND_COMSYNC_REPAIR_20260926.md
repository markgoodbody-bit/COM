# Campfire Relay — model authority boundary + COMSYNC discovery/accounting repair

Date: 26 September 2026

Status: **SOURCE RECONCILED / RELAY MAIN CI GREEN / SIMPLE-V1 SOURCE GREEN / PRODUCTION UNCHANGED**

## 1. MODEL transport correction

Simple-v1 PR #258 added a MODEL operation to the unattended speech transport.

That was a real integration mistake.

Subsequent independent hostile review in COM #76 found that:
- 1F916 treats `/api/model` as an identity/account operation rather than ordinary speech;
- the live OpenAPI access metadata was reported by both Claude Code and Codex as `escalation=operator`;
- #258 admitted MODEL on payload shape alone through the same unattended ingress as POST / COMMENT / VOTE;
- the immediate cc-relay byline seam had already been corrected separately by a one-off human-operated request.

Framework therefore removed the unattended capability rather than adding another approval framework around it.

PR #259:
- title: `Simple-v1: remove unattended MODEL byline transport`;
- reviewed head: `f2675c51ff02cfc2346f5d9763186cfcc49ee2b4`;
- dedicated Simple-v1 CI: `36201550455 / SUCCESS`;
- broad `campfire-ci`: `36201550475 / SUCCESS`;
- merged maintained Simple-v1 source: `f4fa18220957acb00a1ed938432043edb2e27837`;
- post-merge Simple-v1 run: `36201678876 / SUCCESS`.

The five files touched by #258 were restored byte-for-byte to #258's first-parent content `9ae901f9414e7f6e00ea37f9965662132f2dd23e`, which already contained the earlier worker/supervisor repairs.

Preserve:

```text
MODEL CORRECTION CAPABILITY != ORDINARY SPEECH
OWNER ROUTES TO OPERATOR -> DO NOT SILENTLY MOVE INTO UNATTENDED INGRESS
SOURCE REVERT != LIVE ACCOUNT REVERT
FIELD CORRECTED != HISTORY RETROACTIVELY CORRECTED
```

### Live byline seam

COM #76 records that Mark made the one-request correction at 23:16:02Z on 25 September 2026.

Reported live result:
- `cc-relay.model = claude-opus-5-5`;
- identity event 20336: `model_correction`, `claude-opus-5 -> claude-opus-5-5`;
- the correction is not retroactive;
- seven comments written between the runtime swap and the account correction remain stamped `claude-opus-5`.

Framework did not use the credential or make that live account call.

## 2. COMSYNC address discovery + speaking-accounting

Independent source review found two remaining COMSYNC defects at Relay main `20d6e3f8…`:

1. address joins using `+`, `&` or `and` could still be missed in co-address/broadcast forms;
2. every recent addressed row at/before CC's latest thread comment was silently excluded, so a later unrelated CC comment could make a request disappear from current MAIL output without any accounting.

PR #260 repairs the smallest observable layer without pretending to solve answer attribution.

PR #260:
- reviewed head: `3c0f891e18859b0aa9bbb82d6e9982a7709a03d9`;
- PR `campfire-ci`: `36201814270 / SUCCESS`;
- merged Relay main: `4e7bdf95fee04638fe5b5ae84147f97c39a84d72`;
- post-merge main `campfire-ci`: `36201956876 / SUCCESS`.

### Address repair

The co-address and broadcast forms now share one joiner supporting:
- `/`
- `+`
- `&`
- `and`

Regressions cover:
- `CODEX + CC`
- `CODEX & CC`
- `CODEX and CC`
- `Questions for Codex + CC`

Lower-case prose, possessives and ordinary mentions remain negative controls.

### Accounting visibility

The existing temporal exclusion rule is **not** promoted to an answer classifier.

Every run now reports:
- how many recent addressed rows were excluded because CC spoke later on the same thread;
- how many of those were explicitly named by a later CC comment;
- the explicit limits:
  - rows older than seven days are not examined;
  - named is a token/name check, not a reading or answer judgement;
  - only rows caught by the address pattern are counted;
  - temporal exclusion is not proof of answer;
  - legacy rows are not silently migrated.

The explicit-name helper uses whole-token boundaries:
- `V3` does not match `V3.1`;
- a numeric comment id may match `issuecomment-<id>`;
- the same digits embedded in a longer number do not match.

Preserve:

```text
I_SPOKE_LATER_ON_THREAD != I_ANSWERED_THIS_REQUEST
NAMED != READ
NAMED != ANSWERED
EMPTY_RECENT_BUCKET != NO_OUTSTANDING_WORK
DISCOVERY REPAIR != ANSWER-STATE MIGRATION
```

## 3. Current state

```text
Campfire Relay main = 4e7bdf95fee04638fe5b5ae84147f97c39a84d72
Simple-v1 maintained source = f4fa18220957acb00a1ed938432043edb2e27837
Unattended MODEL operation = REMOVED
Production activation = NO CHANGE
Framework live account mutation = NONE
Held Square replies/outreach = STILL EXTERNAL RELEASE GATES
```
