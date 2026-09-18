# THR direct contribution-packet regression — 18 September 2026

Status: **MERGED / SOURCE CONTRACT GREEN / LIVE DIRECT-EXAMPLE BYTES NOT FRESHLY VERIFIED IN THIS APERTURE / NO SCHEMA CHANGE**

## Originating break

Cold machine-contributor use of the optional contribution packet exposed a real guide/schema friction:
- the guide described a small six-item contribution shape;
- the schema required ten top-level keys;
- a direct contributor still needed a full `relay` object with `relayed: false` and null non-applicable relay details.

THR main `217f89c10a60f02b7d39785d531b2cb47cab7337` repaired the public guide and related documentation.

## Regression gap

The existing test suite still exercised only the relayed Grok packet. It did not mechanically preserve the repaired direct/no-relay path.

## Bounded repair

PR #51 added:
- `examples/direct-no-delta.packet.json` — ten-key direct envelope;
- existing contribution-packet test coverage for `relay.relayed=false`, null relay details and exact top-level schema keys;
- packet-guide link to the direct example;
- the direct example to the existing public-delivery verifier.

No schema change.
No new checker.
No intake/backend/authentication change.
No record evidence change.

Exact PR head:
`20540584677eceac3d62655a74aa039058fc3c65`

PR integrity workflow:
`35392744131 SUCCESS`

PR #51 squash merge / current THR main at receipt:
`1f5a5919938f385f43f1e2383bdfbb52807b206e`

## Delivery ceiling

The existing main-push public verifier is configured to compare the new direct example and contribution-guide bytes against thehumanrecord.net.

However, in this Framework aperture:
- web retrieval of the static THR files returned inaccessible/internal-error;
- direct container retrieval failed DNS resolution;
- the available GitHub connector's commit-workflow route only exposes PR-triggered runs, and did not expose the main-push live-delivery run.

Therefore:

`SOURCE MERGE = OBSERVED`
`PR INTEGRITY = GREEN`
`PUBLIC VERIFIER CONFIGURED = OBSERVED`
`PUBLIC DIRECT-EXAMPLE BYTES VERIFIED HERE = NO`

Do not upgrade that ceiling from assumption.

## Meaning

The real outside-use defect is now protected at the source-contract level with the smallest existing mechanism.

`DOC REPAIR != REGRESSION COVERAGE`
`DIRECT CONTRIBUTION != RELAYED CONTRIBUTION`
`VALID PACKET != VALID CLAIM`
`MERGED != SERVED_BYTES_VERIFIED`