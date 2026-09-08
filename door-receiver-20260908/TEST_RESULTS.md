# Local execution receipt — 8 September 2026

Status: EXECUTED LOCALLY / SYNTHETIC ONLY / NOT DEPLOYED

Environment: Node v22.16.0 on Linux; built-in node:sqlite using disk databases,
WAL and synchronous=FULL; standard Node Fetch/HTTP and separate child processes.
Command: `npm test` from this directory. No npm dependency installation required.

Final observed result: **15 tests, 15 passed, 0 failed, 0 skipped**.

The HTTP test submitted an invented contribution using form encoding, discarded
the returned receipt, killed the server with SIGKILL, restarted against the same
database, paused new intake, recovered the existing receipt with the pre-held
keys, verified pending data was not public, published by authenticated moderation,
appended a separately attributed project response, and withdrew the body.

A separate injected post-commit database acknowledgement failure returned 503
without a claimed receipt, while the stored row remained. Retrying the original
request while paused recovered exactly one row. Different content with the same
retry identity was rejected. Stale approval after revision or withdrawal failed.

Five simultaneously released worker threads, each with a separate SQLite
connection, competed for one pending slot: one admission and four QUEUE_FULL
results. Five simultaneous copies of the same retry recovered one identifier
and one stored row. These are local concurrent-storage results, not distributed
Cloudflare measurements.

Other exercised behavior: default closed/readiness expiry, private/public
separation, unauthorised moderation, event/state rollback together, paused/full
correction and reconsideration, body-capacity and rate limits, Unicode and inert
markup, request limits, HTML error text preservation, and refusal of non-loopback
hosting and cross-origin form posts. Tests assert private keys are absent from
local server stdout/stderr captured during the process lifecycle.

The expiry test deliberately also demonstrates a limitation: without a request,
no cleanup runs and the body remains stored after its logical deadline. On the
next sweep it is removed and pending status becomes expired, not rejected. No
physical deletion-at-deadline or metadata-retention completion is claimed.

Attempted Chromium/Playwright visual check could not load the loopback route:
`net::ERR_BLOCKED_BY_ADMINISTRATOR`. It was stopped rather than bypassed. Browser
form behavior, keyboard, reflow and light/dark rendering remain unverified.

No remote D1/Pages/Wrangler execution, provider sign-in, live publication,
production security assessment, real contribution or reader benefit is established.
Read README.md for the remaining work and the hard local-only guard.
