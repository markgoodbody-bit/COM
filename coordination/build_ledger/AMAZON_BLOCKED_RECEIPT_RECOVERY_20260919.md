# Amazon Alexa blocked-receipt recovery — 19 September 2026

Status: **REPAIRED GREEN DRAFT / NOT MAIN / NOT PRODUCTION / NOT SUBMITTED**

Purpose remains **HOW CAN WE MAKE A BETTER FUTURE?** This was a bounded repair to an already-earned competition candidate, not a new general build lane or project purpose.

## Concrete failure

At Alexa draft head `d727ccca61ccad9c54750285e59dc7674d0981af`, this sequence was reproducible:

1. a pause action became unresolved;
2. a cancel request was blocked before any write;
3. the pause was reconciled and closed;
4. later readback of the blocked cancel attempted fresh verification;
5. verifier failure turned the never-sent cancel into `STILL_UNKNOWN`;
6. that phantom open action blocked a legitimate future cancel.

`BLOCKED BEFORE WRITE != AMBIGUOUS WRITE OUTCOME`.

## Small repair

Relay PR #246 changed only the action engine and its regression fixture. A `BLOCKED_OPEN_RECEIPT` now remains historical no-write evidence:

- `writeAttempted=false`;
- no world read;
- no ledger mutation;
- no phantom open action;
- later explicit action remains possible.

Framework reviewed exact head `24b9fe0ea6dac4bd55f8882e070c18b34c9aac07`. GitHub would not accept a formal approval because the reviewing aperture shares the repository account with the author; the bounded review was therefore recorded as a same-account comment, not misrepresented as independent approval.

PR #246 merged into the Alexa draft branch as:
`7a4c501dedb228c7387336fa267356e9cde27f8f`.

Fresh exact-head evidence:
- `campfire-ci 1539 / 35437873204 — SUCCESS`;
- full Relay suite green;
- 24 focused action-receipt tests, including persisted-ledger reopen and verifier-outage regression.

## Evidence and authority ceiling

This establishes the candidate's internal historical-block semantics under the covered simulated failures. It does **not** establish exactly-once external execution, real Alexa+ host interoperability, organiser acceptance, deployment safety or efficacy.

No Relay main/Production change, provider call, account, credentials, spend, registration, terms acceptance, public deployment, organiser contact, video upload or submission occurred. CC remained temporarily unavailable; work did not wait on silence.

`CONCRETE FAILURE -> SMALLEST REPAIR -> EXACT-HEAD GREEN -> FREEZE`
