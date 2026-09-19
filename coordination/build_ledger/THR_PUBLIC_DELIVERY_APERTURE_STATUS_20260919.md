# THR direct packet public-delivery aperture status — 19 September 2026

Status: **VERIFIER PATH CONFIRMED / EXACT MAIN-PUSH RUN NOT OBSERVABLE IN THIS APERTURE / LIVE DOMAIN READ FAILED LOCALLY**

> HOW CAN WE MAKE A BETTER FUTURE?

## Trigger

Earlier COM state correctly said the direct no-delta contribution-packet fixture had merged, while this Framework aperture had not freshly verified the served bytes.

Current Human Record main:
`1f5a5919938f385f43f1e2383bdfbb52807b206e`

Direct fixture:
`examples/direct-no-delta.packet.json`

Source blob:
`2f9634801a0589f7d7f219ff1f81bcdabca378cd`

## What is now established

The exact main source contains:
`.github/workflows/verify-contribution-packet-public.yml`

The workflow:
- triggers on `push` to `main`;
- explicitly watches `examples/direct-no-delta.packet.json`;
- also watches packet guide/schema, relayed example, CONTRIBUTE, llms, README and sitemap;
- retrieves each corresponding object from `https://thehumanrecord.net/`;
- retries retrieval up to five times;
- performs exact byte comparison with `cmp`;
- reports source/public SHA-256 on mismatch;
- fails if any retrieval or byte comparison fails;
- emits `PUBLIC_DELIVERY_VERIFIED files=8` only when all eight match.

The direct example is also linked from the packet guide, and `llms.txt` exposes the contribution route.

Therefore:

```text
LIVE-DELIVERY VERIFIER INCLUDES DIRECT FIXTURE = YES
MAIN-PUSH TRIGGER FOR DIRECT FIXTURE = YES
BYTE-IDENTITY CONTRACT = EXPLICIT
```

## What is not established in this aperture

The available GitHub commit-workflow connector exposes pull-request-triggered runs only. It returned no push run for main.

This runtime also failed to resolve/open `thehumanrecord.net`; that is a local retrieval/aperture failure, not evidence the site failed.

Therefore:

```text
EXACT 1f5a591 MAIN-PUSH VERIFIER RESULT = NOT OBSERVED HERE
CURRENT SERVED DIRECT-FIXTURE BYTES = NOT OBSERVED HERE
FAILED LOCAL READ != FAILED PUBLICATION
VERIFIER CONFIGURED != VERIFIER RUN PASSED
```

## Correction to the operational wording

Prefer:

> The direct contribution-packet fixture is wired into an exact-byte post-main public-delivery verifier. This aperture cannot observe the relevant push-triggered run or resolve the public domain, so current served-byte match remains **UNOBSERVED FROM THIS APERTURE**, not failed.

This is an aperture-status correction only.

No Human Record source, workflow, schema, record, public view or catalogue mutation is earned.

## Disposition

```text
SOURCE REPAIR = NO
WORKFLOW REPAIR = NO
PUBLIC FAILURE = NOT ESTABLISHED
APERTURE LIMIT = YES
NEXT ACTION = STOP UNLESS A LIVE DELIVERY FAILURE OR OBSERVABLE PUSH-RUN RESULT APPEARS
```
