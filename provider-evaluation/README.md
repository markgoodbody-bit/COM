# Remote D1 binding evaluation, 8 September 2026

SYNTHETIC ONLY. LOCAL TEST HARNESS. DO NOT DEPLOY.

This imports the unchanged receiver from PR116 source
f06967a103d9f5c952b10bce56c00b0e88acc49f. It does not implement another receiver.
The test runs in local workerd, using Wrangler's remote D1 binding to the existing
isolated `psfh-receiver-eval-20260908` database. No production form or endpoint is
created. `workers_dev` and preview URLs are disabled; requests require loopback,
a named custom header and no browser Origin. The original receiver's non-loopback
refusal remains intact and is exercised. This is not production authentication.

## Reproduce

Use the already-authorised account and the exact configured evaluation database;
do not run this against another database. Its migration is already applied. A
rerun adds synthetic records and uses remote query quota. Do not run concurrently:
readiness and the named test trigger are shared evaluation state.

```
npm exec --yes --package=wrangler@4.129.1 -- wrangler types worker-configuration.d.ts --config wrangler.jsonc
npm exec --yes --package=wrangler@4.129.1 -- wrangler dev --config wrangler.jsonc --show-interactive-dev-session=false
```

POST `/run` and `/lost-ack` at the printed loopback URL with
`X-PSFH-Evaluation: synthetic-only`. Neither endpoint accepts submitted content.
Inspect `status`, not merely HTTP completion. Stop the dev session afterwards.
Do not use `--local`: it disables remote bindings and would change the test.

Global Wrangler4.82.2 could not start compatibility date2026-09-08: its workerd
supported only2026-04-17. That startup failure is not a receiver failure or a
passing test. The isolated4.129.1 invocation succeeded without changing the global
installation or reducing the compatibility date. Types were regenerated with
4.129.1. TypeScript noEmit/allowJs/skipLibCheck with Node types passed for the
harness. This does not claim strict checking of the imported JavaScript receiver.

## Observed results

`/run`: PASS, eight named groups:

1. Original non-loopback guard.
2. Paused new intake refusal.
3. Stored receipt read through a new Store instance.
4. Same retry recovery while paused and changed-content conflict.
5. Private pending text, reviewed publication and separate response.
6. Replacement unpublishes; stale approval fails; old response removed.
7. Actual Store.moderate D1 batch rolls state and audit back together when a
   temporary trigger aborts the event INSERT. The trigger is dropped afterwards.
8. Decline, reconsideration, publish and withdrawal produce exactly the expected
   seven events; withdrawal cannot be reversed by stale approval.

Record: `7d436187-928c-492d-a843-b59c9f4c0ec1`. A separate Wrangler remote-query
process confirmed withdrawn/revision3/bodyNULL and all seven events, with intake
disabled and no leftover test trigger. This also distinguishes the remote run
from a local database simulation.

`/lost-ack`: PASS. The real receiver handler used the real remote binding with one
deliberate exception after the INSERT had resolved. It returned503 without a
confirmed receipt. A subsequent handler invocation with original pre-held keys,
while paused, returned200 and the same ID; only one row existed. Pending content
and keys were absent from public output. The synthetic record was then withdrawn.
Record: `ee57e625-9b89-4acc-8bac-abc8cef5eef7`. Keys existed only in request memory
and are not included in this result. A lost acknowledgement was injected, not an
actual network outage.

The temporary trigger tests transactional rollback, not physical erasure. No
provider crash, regional outage, concurrent remote admission race, end-to-end
deployed HTTP transport, browser flow, moderator readiness, backup purge or
receipt durability under disaster has been established. Bodies are cleared in
logical rows; retained synthetic event reasons are not an erasure result.
Test queries consume provider quota; invoice cost was not independently measured.

## Remaining work

Keep public receiving closed. Review retention/notice and operational controls;
exercise remote concurrent admission and a deployed-but-closed integration only
within the established account/domain scope. Preserve the existing site, original
database and local-only guard. First-contact/style work remains a separate saved
candidate until its own acceptance and publication.
