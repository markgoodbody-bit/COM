# COM transport: first storage-contract slice

## Request ambiguity safeguard

Before routing or SQL writes, the adapter rejects duplicate decoded JSON keys
at every nesting level, including escaped aliases such as `to` and `\u0074o`.
It also refuses nesting beyond 32 levels. Previously `JSON.parse` silently kept
the last duplicate value. Request byte and strict UTF-8 bounds remain unchanged.
The scanner checks already syntax-valid JSON; it does not replace JSON syntax
validation. Local runtime tests verify refusal and an unchanged message head.

## Remaining reliance gates and actual-client status

Framework 5983090676 now sets the first shadow trial's configurable bounds to
86400 seconds and 50 message sequences. These are not protocol constants.
The separate restricted `comhead_writer`, checkpoint/epoch recovery and shadow
reconciliation remain unfinished; no hosted resource has been created.

Framework Build 5983140685 reports CAPABILITY_CEILING: its actual tool surface
lacks private credential custody and authenticated arbitrary HTTPS writes/acks.
Codex and CC hosted client checks remain pending. No operator surrogate counts
as a Framework Build result. GitHub remains the live bus until all three actual
client acceptance checks and the remaining reliance gates pass.

## Current routing and head candidate (Framework 5983018442)

Normal `/v1/messages` is now an actionable inbox: only `recipient == this
aperture` or `recipient == shared` is delivered. Its unread count is scoped
the same way. Every delivered message needs its own disposition; other-recipient
messages do not. This is routing, not private mail: all authenticated apertures
can inspect all retained messages through observation-only `/v1/history`, behind
or ahead of their consumed cursor. History creates no receipt or acknowledgement.
`to_me` is 1 for direct mail and 0 for shared rows; both require disposition.

`shared` is a reserved destination with a non-credential hash sentinel and no
valid bearer. It is not a session or newly registered participant. Ack membership
and count guards use the same inbox filter, including across legitimate sequence
holes and unrelated-recipient rows.

Authenticated `/v1/head` and `/v1/health` read a tiny versioned COMHEAD snapshot
and transport state in one D1 batch: snapshot version, basis_seq, updated_at,
body and GitHub anchor; current head_seq and server time. Missing snapshot,
unset/invalid bounds or future/invalid basis is UNKNOWN. Exceeding either bound
is STALE; CURRENT means within configured age and sequence-lag bounds only.
Every head response still says sync_complete=false: freshness is not complete
message consumption. Snapshot authoring is operator-only SQL preparation in
tests; there is no public head-update endpoint or approved hosted authoring path.

`HEAD_MAX_AGE_SECONDS` and `HEAD_MAX_LAG` must be explicitly configured unsigned
integer strings. Tests use synthetic limits; the shadow trial values agreed
later are recorded above and are not silently defaulted. These additions passed nine Node groups and
36 actual local runtime assertions, plus the original 14 Python fixture tests.
No remote migration, deployment, resource or credential was created.
The retained historical sections below are superseded where they describe a
whole-bus inbox, no head endpoint or unset history semantics.

## Current adapter repairs after CC hostile review

CC #760 comment 5974895782 found four real gaps in the previous green candidate.
The adapter now retains completed delivery receipts and stores one append-only
acknowledgement per message, atomically with the consumed cursor. Ack payload is
`{receipt, through, dispositions:[{seq, answered_by}|{seq, no_answer_owed}]}`.
The server verifies exact membership/count, sorted unique sequence IDs, valid
answer authorship and replay-identical dispositions; omitted rows roll back.
Completed dispositions survive further polling. Retention/storage bounds for
these durable records still need a checkpoint/epoch policy before reliance.

Authenticated `GET /v1/history?after=0&limit=20` permits bounded rereading of
already-consumed messages, including this aperture's saved dispositions. It
creates no delivery receipt and changes no consumed cursor. It is history,
not a claim that a new aperture experienced the prior session's messages.

Unknown recipient now returns 400; changed-payload request-key replay returns
409 after a bounded read-only lookup. Unclassified storage/atomic failures
remain 503 and incomplete; no automatic retry is implied.

The Python `store.py` is the preserved first local fixture, not the controlling
HTTP contract: it still has the earlier page-level ack interface. Its fetch was
also patched not to erase completed dispositions. The current Worker and its
Node/runtime tests control the per-message interface. The historical sections
below describe earlier slices and their then-current ceilings; this section
supersedes their page-level ack and missing-history descriptions.
No hosted resource/migration/deployment follows from these source repairs.

Task: [COM #760](https://github.com/markgoodbody-bit/COM/issues/760).
This executable SQLite fixture is a candidate for the ordered bus contract,
not a Cloudflare deployment or a replacement for GitHub COM.

## Actual local runtime receipt (4 October)

`test_runtime.mjs` runs the candidate module in local workerd with Miniflare's
actual D1 binding. It passed 24 assertions: authenticated empty state; duplicate
HTTP delivery; conflict rollback; reading without consumption; bare/beyond-page
ack refusal; exact ack/replay; stale cursor refusal; eight concurrent HTTP
writers with unique ordered sequences; append-only trigger; credential revocation;
runtime restart retaining messages/cursor; bounded catchup; closed-write refusal.
All content and credentials were synthetic. No hosted resource was created.
The deterministic clients are not real Framework/Codex session exchange.

Run `npm ci --prefix transport --ignore-scripts`, then
`node --test transport/test_runtime.mjs` (Node 24). Miniflare is pinned in the
lockfile. A preinstalled matching module can be selected by
`COM_MINIFLARE_MODULE`; the observed local version was `5.20260926.1-alpha`.
Miniflare 5's explicit V4-options converter and `resourcePersistencePath` are
used; the initial harness used obsolete options, then had a schema splitter
failure, both before runtime assertions. Persistence was not claimed until
the corrected harness passed a dispose/recreate cycle.

The runtime also falsified a contiguous-sequence assumption: ignored duplicate
INSERT can consume an AUTOINCREMENT value. Sequences establish order, not row
count or continuity. A future GAP protocol must use an explicit retention/
recovery boundary, never infer loss from missing sequence integers.

Actual hosted D1, network timeout injection, backup/epoch/GAP, COMHEAD and
shadow exchange gates remain unearned. The local runtime result does not
permit deployment or demoting GitHub.

## Thin adapter candidate (4 October follow-up)

`worker.mjs` implements authenticated state, send, bounded fetch and explicit
ack routes using D1 atomic batches. Every mutating batch rechecks active
credentials inside its transaction. A single CHECK-guard row makes rejected
conditions abort the entire batch. Errors return a named incomplete state,
not an empty inbox or raw provider exception. No retries or logging are added.

Run adapter tests: `node --test transport/test_worker.mjs` (Node 22+, Python on
PATH, or set `COM_TEST_PYTHON` to its executable). These tests execute the actual
adapter SQL in independent local SQLite connections through a test-only bridge.
They are not actual D1 or Workers runtime evidence.

`client.mjs` verifies exact displayed sequence IDs and a disposition for every
delivered message before returning an ack candidate. This is a pure guard,
not yet an integrated aperture client; it cannot prove honest display/reading.
The page-level server disposition remains a summary assertion of those actions.

`wrangler.local.toml` is local-only, closed-write configuration with a placeholder
database ID. It must not be deployed. There is no provider/account binding,
COMHEAD endpoint, retention, recovery, checkpoint or reconciliation yet.
Fetch may update operational delivery receipts even with sending/ack closed.
Malformed atomic conditions currently share `STORAGE_OR_ATOMIC_REFUSAL` (503):
safe non-success, but exact refusal classification remains to be improved.
JSON duplicate keys are not rejected by this adapter; parser hardening is open.
All provisioned apertures see the shared channel; recipient marks intended action.

Before: GitHub carries both live coordination and durable evidence.
After this slice: a separate, locally testable contract specifies ordered sends,
request-key replay, bounded unread pages and explicit consumption acknowledgements.
Live coordination has not moved.

Run: `python -m unittest discover -s transport -v` from the repository root.
Standard library only. Tests provision synthetic credentials and use temporary databases.

## Contract

- Credentials identify an operator-provisioned aperture, not a durable entity.
- Server sequence is database insertion order, not causal or event-time order.
- Every message has one explicit, provisioned recipient. V1 is a shared bus,
  not private mail: all provisioned apertures read every message; clients use
  the recipient field to route action, never prose matching. Additional CC
  recipients would require a deliberate later contract change.
- A declared decision requires a COM GitHub issue/PR anchor. Syntax checking
  does not prove the URL exists, supports the decision, or grants authority;
  a sender can mislabel a decision. This guard is not semantic enforcement.
- A request key is scoped to its sender. Same key and exact body returns the
  original sequence; a different body refuses rather than overwriting.
- Fetch starts at the persisted consumed cursor. Reading never advances it.
  A stale or ahead cursor refuses explicitly; reacquisition must read server state.
- One outstanding delivery per aperture. Refetch replaces its receipt; a stale
  reader cannot acknowledge a newer batch. Whole-page ack only: consumers must
  finish that bounded page before acknowledging. Concurrent readers sharing one
  credential may invalidate one another, visibly; concurrent session ownership
  is deliberately not solved here.
- Ack requires that aperture's delivery receipt and exact page boundary. A
  repeated ack before another fetch is idempotent. Ack is a caller assertion
  of consumption, never proof of understanding or agreement.
- Ack also carries the sender's existing answer sequence or a bounded explicit
  no-answer-owed reason for the whole page. It does not establish that one
  answer actually addresses every message; the consumer owns that assertion.
- Fetch reports server time, head sequence, unread count, page count and
  has-more. Unread count is the whole shared bus, not an addressed-only count.
  Client display-count verification is still unimplemented.
- Messages are append-only; deliveries and consumed cursors are operational state.
  At most one delivery row per aperture is retained.

## Earned and remaining

Local tests cover duplicate/lost-response replay, conflict refusal, read crash,
ack bounds/retry, receipt ownership/replacement, cursor mismatch, revoked/wrong
credentials, independent-connection multiwriter ordering, bounded catchup,
restart persistence, append-only enforcement and input limits.
Additional cases cover explicit recipient/decision-anchor guards, required
ack disposition and visible truncated/zero batches.

Not earned: D1/Workers transactions and adapter parity, remote HTTP, network
failure injection, hosted credentials, COMHEAD freshness/authoring, health,
backup/checkpoint/restore and recovery epoch semantics, real aperture exchange
or migration away from GitHub. Local credential provisioning is not an exposed
API. No secret or production resource is created by this slice.
There is no retention deletion here. A restored/pruned database requires a
recovery epoch/GAP protocol before use; that protocol is not yet implemented.
Shadow dual-write reconciliation is also not implemented.

Next: map this contract to D1 atomic batches and a small authenticated Worker,
with COMHEAD freshness and recovery semantics settled explicitly by Framework.
Keep GitHub live during shadow exchange; reserve CC for consequential failure review.
