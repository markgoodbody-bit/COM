# COM transport: first storage-contract slice

Task: [COM #760](https://github.com/markgoodbody-bit/COM/issues/760).
This executable SQLite fixture is a candidate for the ordered bus contract,
not a Cloudflare deployment or a replacement for GitHub COM.

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
