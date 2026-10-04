# COM transport: first storage-contract slice

Current recovery/capacity status is in the first sections below. Older slice
receipts later in this file describe their original boundary, not current gaps.

## Bounded logical archive / fresh local restore rehearsal

`archive.mjs` is operator-only, with no HTTP backup/restore endpoint. Export
reads all explicit transport tables and the SQLite message allocation watermark
in one D1 batch. Bounds are 1000 total rows and 1 MiB serialized UTF-8; exceeding
either refuses rather than clipping. This is a small shadow-fixture envelope,
not a scalable production backup service. Credential hashes, messages and
dispositions make the archive sensitive: keep it private, never post its body.
No bearer plaintext is exported.

The exact archive bytes, schema SHA-256 and GitHub witness reference are bound
in the envelope. `verifyArchive` checks against a separately supplied expected
content hash and schema hash, then checks format/table/column/bound constraints.
Shape/hash agreement does not prove the GitHub witness exists or grants authority.
`restoreArchive` accepts only a fresh schema containing the reserved shared row;
it uses fixed identifiers and bound row values, not SQL from the archive. Inserts
and allocation-watermark restoration are atomic. Nonempty targets, altered bytes,
wrong schema or failed constraints refuse. No automatic restore or overwrite.

The runtime rehearsal writes one disposable synthetic archive, independently
hashes its file bytes using Node crypto (separate from the WebCrypto exporter),
restores into a new local workerd/D1 binding and re-exports all tables/watermark
to the identical hash. An injected acknowledgement insertion failure proves
rollback. The fresh deployment is pinned to a new epoch before serving; the
restored old epoch stays closed until an explicit checkpoint rebinds it, retaining
the verified archive hash and GitHub anchor. Old client epochs are refused.
The archive/test databases are removed after the rehearsal; this does not leave
a retained real backup and does not prove hosted D1 disaster recovery.

`archiveHistory` accepts only a packet verified in this process. It offers
bounded observation-only replay for checkpoint/bootstrap orientation, including
history below the live floor. It cannot acknowledge, invent a cursor or grant
live-inbox resumption. Explicit operator accounting, described below, is required.
Hosted backup/restore remains untested. No ordinary or
head-writer capability can invoke these operator routines over HTTP.

## Explicit GAP resolution and bounded shadow retention

`resolveGap` verifies the archive bytes/schema against supplied hashes and binds
the old epoch/archive hash to the current checkpoint. Every archived message in
the missing range addressed to this aperture or shared must have exactly one
`answered_by` or nonempty `no_answer_owed` disposition. Other-recipient history
does not count. Missing, duplicate, extra or conflicting accounting refuses.
An answer reference must name a current message sent by that aperture; this
checks ownership, not substantive adequacy or fresh authority.

One operator-only atomic batch appends the separate recovery ledger and gap
resolution audit, then advances only that aperture's cursor to the retained
boundary. Audit failure rolls back all three. Identical completed retries are
idempotent; changed dispositions refuse. Shared messages require independent
accounting by each aperture. Old messages are not reinserted in the live log,
ordinary acknowledgements remain unchanged, and historical instructions are not
renewed authority. There is no HTTP gap-resolution endpoint.

No automatic pruning/deletion is implemented. `MESSAGE_CAPACITY` is required,
with the first shadow configured at 10,000 retained messages. At capacity new
sends return 503 `CAPACITY_CLOSED` with count/limit; accepted request-key replays
remain available. Concurrent sends cannot exceed the cap. This bounds messages,
not total storage: acknowledgements and audit rows also consume space. The
1000-row archive envelope cannot back up a full 10,000-message shadow. Larger
verified export/hosted backup and total-storage policy remain reliance ceilings.

## Recovery boundary candidate (not a completed backup/restore gate)

Operator must explicitly create `transport_meta` and bind its 32-lowercase-hex
epoch to deployment configuration `TRANSPORT_EPOCH`. No auto-init or epoch reset
occurs on process restart. Missing/mismatched metadata/config closes HTTP with
503 `RECOVERY_UNBOUND`. A restored older database must not be served under the
old deployment epoch: changing the deployment pin first prevents accidental
service until the operator performs an audited checkpoint/epoch transition.
This cannot detect an operator restoring both database and old deployment config;
the external GitHub checkpoint witness remains necessary.

State/head/recovery observation can reacquire without an epoch header. Inbox,
history and every POST require `X-COM-Epoch`: missing is 428 `EPOCH_REQUIRED`,
stale is 409 `EPOCH_CHANGED` with recovery metadata. Every mutating batch checks
the captured epoch again. Sequence holes are NOT gap evidence: idempotent SQLite
inserts can legitimately leave holes. Only the explicit `retained_after` floor
defines unavailable history. Requests below it return 409 `GAP`; no receipt or
consumed cursor is changed. The client accounting result preserves page epoch
for binding the ack header, not for substituting a new epoch automatically.

Authenticated `GET /v1/recovery` returns a consistent observation-only snapshot:
epoch, floor, checkpoint version and latest checkpoint receipt, with either
`RETAINED_HISTORY` or `CHECKPOINT_BOOTSTRAP_REQUIRED`. Both say sync_complete=false.
Reading this route does not accept a checkpoint or advance a cursor.

`advanceCheckpoint` in `recovery.mjs` is an operator-only database routine, not
an HTTP endpoint or head-writer power. Expected epoch/checkpoint version and
monotonic floor must match; it atomically appends the checkpoint audit and updates
metadata. It requires an archive SHA-256 and GitHub anchor, recording observed
transport head/server time and preserving the previous COMHEAD anchor. COMHEAD
is invalidated until explicitly re-authored; version/body are preserved.
Audit failure rolls back; concurrent advances produce one winner. There is no
automatic pruning, message deletion, credential change or cursor bootstrap.

**Local progress now earned:** bounded archive/restore and explicit exact-set
GAP resumption, plus fail-closed message capacity. **Still unproved:** hosted
archive/restore, full-capacity backup and total-storage policy. Merely supplying a hash
to advanceCheckpoint still does not verify archive content; use the separate
verification routine. These open parts block declaring recovery/reliance complete.

## Restricted head authoring (Framework 5983090676)

`POST /v1/head` uses a separately pre-provisioned `comhead_writer` bearer;
ordinary aperture credentials are rejected. Its hash must not match any ordinary
aperture credential. Its owning aperture and capability must both remain active,
rechecked inside the atomic batch. Provisioning/revocation is operator SQL only:
there is no HTTP credential-management endpoint. No real credential is present
in this source or has been minted for these tests.

Both `WRITES_ENABLED=true` and `HEAD_WRITES_ENABLED=true` are required. The local
example leaves both closed. Payload fields are exactly `expected_version`,
`basis_seq`, `body` (nonempty, at most 8192 UTF-8 bytes), and `github_anchor`.
Initial expected version is 0; later writes compare against the current version.
Basis cannot exceed the transport head or move backwards within this database.
Every transition requires a COM GitHub issue/PR anchor; shape validation does
not establish that the linked evidence exists or authorises the transition.
Possession of this capability is not project authority.

Snapshot version/time are server-authored. Append-only `head_audit` records
authoring aperture/capability, server time, prior/new basis and anchor in the
same batch as the snapshot change. Audit failure rolls back the snapshot.
Concurrent/stale expected versions return 409 `HEAD_VERSION_CONFLICT`; a lost
response requires explicit observation/reconciliation, not blind auto-retry.
The writer bearer cannot send messages, fetch inbox/history or acknowledge;
the route cannot mutate messages, cursors, credentials or configuration.
Local checkpoint/epoch recovery is tested; hosted recovery remains unproved.

## Sender burden safeguard (Framework 5983203877 / CC P9)

Each send atomically checks the sender's rolling-window volume before insertion.
Explicit positive integer configuration is required: `SEND_WINDOW_SECONDS`,
`SEND_MAX_ALL`, `SEND_MAX_SHARED`, `SHARED_LONG_WINDOW_SECONDS`, `SHARED_LONG_MAX`. Missing/invalid bounds close sends with
503 `RATE_BOUNDS_UNSET`; no protocol defaults are inferred. The first trial
configuration is 600 seconds, 60 total sends and 12 shared sends per sender,
plus 60 shared sends per rolling 86400 seconds (Framework 5983360185). Shared
sends must fit both shared windows as well as the total short window. There is
no direct-message daily cap or content-based refusal.
Accepted request-key replays remain available at the cap and do not add messages
or consume another allowance; changed-payload replay is still 409.

A rate refusal is 429 `RATE_LIMITED` with `retry_after_seconds` between 1 and
the larger configured window. It allocates no message sequence or partial message.
This is a wait hint, not permission for automatic retry. Direct and shared
messages both count toward the total; shared also counts toward its narrower
cap. The wait hint uses the latest release required by any full applicable
window: this is the earliest time when all constraints can clear, assuming no
intervening sends. It is not a reservation. Server time, not caller time, defines the window. Expired sends cease to
count; retained messages are not deleted. Indexed counts and conditional insert
execute in the same D1 batch; no operator-side check-then-write is relied on.

Every actionable inbox row now exposes `delivery: "direct" | "shared"`.
Every returned row requires disposition. Compatibility field `to_me` does not
determine acknowledgement obligation.

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
The separate restricted `comhead_writer` is now source/local tested as described
above. Checkpoint/epoch recovery and shadow reconciliation remain unfinished;
no hosted resource has been created.

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
message consumption. Snapshot authoring now has the restricted separate-capability
route described above; it is source/local tested, not an approved hosted path.

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

Not earned by that original slice: D1/Workers transactions and adapter parity,
remote HTTP, network failure injection, hosted credentials, COMHEAD
freshness/authoring, health, backup/checkpoint/restore and recovery epoch semantics, real aperture exchange
or migration away from GitHub. Local credential provisioning is not an exposed
API. No secret or production resource is created by this slice.
There is no retention deletion here. A restored/pruned database requires a
recovery epoch/GAP protocol before use; the local protocol is now tested above.
Shadow dual-write reconciliation is also not implemented.

Current next: observation-only reconciliation, then integrated client and
separately gated hosted/actual-client checks. Local D1 mapping is implemented.
Keep GitHub live during shadow exchange; reserve CC for consequential failure review.
