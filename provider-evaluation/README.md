# Remote D1 binding evaluation, 8 September 2026

SYNTHETIC ONLY. LOCAL TEST HARNESS. DO NOT DEPLOY.

The original run imported PR116 source f06967a103d9f5c952b10bce56c00b0e88acc49f.
The checkout now incorporates PR1167b0aa944 plus repair c8fb095; old results below
remain pinned to their original source. Record the actual checkout on each run.
This imports the receiver, rather than implementing another receiver.
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

POST `/run`, `/lost-ack` or `/correction` at the printed loopback URL with
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

## Correction evaluation, 17:15 UTC

Migration0002 was applied once, after a remote schema query established that both
correction tables and service.correction_limit were absent. Existing database
UUID85c6f402-da0b-4c52-a1ad-445dc999c3b0 was reused. No database was created.
The first schema query failed7403; account identity and D1 info still succeeded,
and one repeated schema query succeeded. This was observed as transient, not a
diagnosis of its provider cause. No re-login or scope changes were made.

PR1167b0aa944 integrated baseline passed34/34 on Windows. Two new regressions
failed before repair: correction input buffered all1000 synthetic chunks before
rejecting an oversized unlabelled stream; failed browser form dropped the chosen
misattribution reason. Repair c8fb095 bounds stream reading, sends correction
admin actions through the existing bounded parser/authentication before dispatch,
and preserves reason/keys on failure. Complete suite36/36 passes.

`/correction` PASS: six groups through the real router in local workerd with remote
D1. Ordinary intake paused/correction accepted; one receipt on same retry and409
on changed retry; unauthorised operator401 and wrong reporter key404; private
queue/receipt with unchanged public JSON; explicit resolution leaves the full
target row and public view unchanged; pending withdrawal clears its note; hard
non-loopback guard remains. The six groups combine the two access checks.

Separate remote SQL readback after stopping the server confirms:
- service enabled0/ready_until0/correction_limit100 and zero published rows;
- target e08910e1-92a2-4480-b5fc-f8dbf5cc2351 withdrawn/bodyNULL;
- report94792df5-e0d3-4006-bd8b-c4c5d9e3de92 resolved/no_change, synthetic note retained;
- reportcdc207e9-1594-439b-a062-6fc1e54619fc withdrawn/empty note;
- exact correction events received/resolved and received/withdrawn respectively.

The existing five implicit callback types in the older harness failed TypeScript
7.0.2 checking; explicit row types repair those checks without changing runtime
behaviour. Generated Wrangler4.129.1 types and current config schema were read.
No strict checking of imported JavaScript is claimed. Older `/run` and `/lost-ack`
were NOT rerun as part of the correction result.

## Remaining work

Keep public receiving closed. Review retention/notice and operational controls;
exercise remote concurrent admission and a deployed-but-closed integration only
within the established account/domain scope. Preserve the existing site, original
database and local-only guard. Preview0.8 first-contact/style work is delivered;
this evaluation does not change it. Correction resolution currently prevents the
reporter from clearing the private note: Framework owns that narrow follow-up.
Operator disposition is a recorded assertion, not proof that content changed.
No standalone CLI over provider HTTP, remote concurrency, live receiving,
reader-benefit, backup purge or operational response guarantee is established.
