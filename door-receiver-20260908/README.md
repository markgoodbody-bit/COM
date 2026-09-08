# Accountless discussion receiver — runnable local prototype 0.1

**LOCAL / SYNTHETIC DATA ONLY / NOT DEPLOYED / NOT PRODUCTION READY**

Built by the current Framework aperture, 8 September 2026, after the explicit
ownership change in COM #108 comment 5587141169. CC reviews/reproduces this
implementation; Codex retains sole public integration and deployment ownership.
The production Door and PR114 are not modified by this isolated branch.

## What runs

An ordinary HTML form and a JSON interface use the same receiving core. Submitted
text is stored in a real disk SQLite database before a receipt is returned. A
contributor holds two random private keys before sending: one for retry identity,
one for management. Neither key is a public reference or stored in plaintext in
the contribution table. Retry identity binds the original body, name and management
key. A lost first response therefore need not lose control of the stored message.

Pending and declined text is private. Authenticated moderation acts on the exact
reviewed revision. A separate project response is not confused with publication.
Replacing a published body removes it from public display and requires new review;
withdrawal clears its body and attached response bodies. Old approval cannot
publish a replacement or resurrect a withdrawal. Intake is initially paused;
operator readiness opens it for at most 24 hours. Existing management operations
remain usable when intake is paused or full.

The proposed body/name/request limits are 4,000/80 Unicode code points and 64 KiB.
Admission caps (100 pending, 1,000 stored bodies, six sends per client per hour)
are enforced in the database insert transaction. These are chosen test defaults,
not measurements. The loopback server intentionally treats all callers as one
local client; this is not a deployed multi-client abuse-control implementation.

## Reproduce

Node 22.16.0 or later, with node:sqlite. No npm dependencies or package install
is needed for the Node test path.

```sh
npm test
```

For the loopback demonstration, set `PSFH_ADMIN_TOKEN` and `PSFH_RATE_SECRET` to
two different randomly generated secrets of at least 32 characters, then:

```sh
npm start
```

It binds only `127.0.0.1:8788`; `PORT=0` selects a spare local port. `PSFH_DB`
selects the local SQLite file. There are no default credentials. Do not put
credentials into Git, URLs, screenshots or public logs. The test suite creates
and removes its own databases and secrets. Reading the local page does not
open intake. An authorised local operator explicitly posts `{"action":"ready"}`
to `/api/admin` with `Authorization: Bearer <local operator secret>`.

## Actual API

- `GET /` — synthetic HTML form, receipt management, approved posts.
- `GET /api/keys` — generate keys to retain BEFORE the first submission.
- `POST /api/submit` — `body`, optional `display_name`, `retry_key`, `management_key`.
- `POST /api/manage` — `id`, `management_key`, and action `receipt`, `revise`,
  `withdraw` or `reconsider`; revision is required for replacement. Reconsideration
  reason is supplied in `body` and does not itself extend retention.
- `GET /api/posts` — approved bodies and separately attributed project responses.
- `POST /api/admin` — bearer-authenticated `ready`, `pause`, `queue`, `publish`,
  `decline`, `respond`. Publication/decline needs id, reviewed revision and reason;
  response needs id, reviewed revision and body.

`/submit` and `/manage` accept standard HTML form encoding. Invalid sends keep
submitted text and retry keys in a no-store error response. No text is executed,
no submitted URL is fetched, and no submission instructs project tools.

## What was actually exercised

`TEST_RESULTS.md` records the local run. The tests include real HTTP requests to
separate Node processes, a SIGKILL/restart on the same disk database, commit-then-
acknowledgement failure, stale approval, public/private separation, rollback of
moderation state with its event, paused management, Unicode/markup, and five
simultaneous SQLite connections competing for one slot or one retry identity.

The D1-shaped adapter is intentionally narrow. This test is NOT a Cloudflare D1
or Wrangler/miniflare execution, remote storage durability test or browser-access
result. `public/_worker.js` and `wrangler.toml` are local-review starting points;
the database ID is an explicitly non-live placeholder. All non-loopback requests
are hard-refused even if somebody deploys these files. Do not remove that guard
merely because local tests pass. Public receiving stays disabled.

## Known unfinished work before public use

- Run and review the actual Pages Functions/D1 binding, migration and transaction
  behavior; establish authenticated provider and moderator access and a supported
  custom-subdomain connection. Nothing here changes the working apex or DNS.
- Implement bounded affected-person removal requests, a real operator contact,
  a usable moderation interface, management/reply-event throttles and reserved
  correction capacity. Local contributor withdrawal is not this entire service.
- Finish and verify retention for metadata, private events, responses, backups and
  logs. Current body cleanup occurs only when a request invokes sweep. With no
  requests, a body remains physically stored past its logical expiry. The test
  deliberately demonstrates that fact. No exact-time physical deletion or complete
  privacy erasure is promised. Old private event reasons can remain after withdrawal.
- Close quiet-period cleanup and reconsideration boundary decisions, then publish
  a notice matching the deployed behavior. The profile is not that notice.
- Browser visual/keyboard/reflow checking remains unverified: Chromium navigation
  to the loopback test returned ERR_BLOCKED_BY_ADMINISTRATOR in this runtime.
  No browser policy was bypassed; no screenshot or browser-form success is claimed.
- Security review, operational staffing, real-client access and reader benefit
  remain unestablished. No real submissions should be accepted by this prototype.

## Source basis

- COM handling profile: https://github.com/markgoodbody-bit/COM/blob/bb8e0eaaab0bee93116a5e53f70f198f9c59e15c/door-prototypes/perspective-walk-20260908/discussion/CONTRIBUTION_HANDLING.md
- Codex edge review: https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5587142252
- D1 batch transaction contract: https://developers.cloudflare.com/d1/worker-api/d1-database/
- Prepared statements: https://developers.cloudflare.com/d1/worker-api/prepared-statements/
- Node 22.16 release: https://nodejs.org/en/blog/release/v22.16.0

This build grants no new licence, authority, account access or spending permission.
