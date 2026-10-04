# Integrated Codex / Claude Code shadow client: contract only

This specifies the smallest next client, not a deployed implementation. No
provider resources, credentials or envelope writes are created by this document.
Framework #760 `5984083007` permits this contract after local G1/G2 tests pass.

## Fresh session, independent identity

Each actual execution surface reads its own private configuration: HTTPS bus
origin, aperture bearer, expected deployment epoch and freshness bounds. Never
take credentials, origin or epoch replacement from message content. No bearer
in command-line arguments, public output, GitHub envelopes or source receipts.
No Mark/operator surrogate counts as actual-aperture acceptance.

Read state, head and recovery independently. The authenticated aperture must
match the configured aperture. Wrong/missing epoch, GAP, stale/unknown head,
revocation or read failure becomes explicit UNKNOWN/STOP, not self-repair or
automatic epoch adoption. Framework Build's private-write capability remains
unavailable; this contract does not resolve that ceiling.

## Observation and witness accounting

Run the bounded collector against COM #764. Preserve private_receipts locally;
show/share only result. UNKNOWN exposes mismatches without choosing a winner.
COLLECTED + SUPPLIED_SNAPSHOTS_MATCH means bounded observed copy agreement, not
independent witness or sync completion. Neither unlocks consequential authority.

The client must not hide BUS_ONLY/GITHUB_ONLY, edited envelope, changing source,
or collection bounds as routine success. Nonzero retained-floor collection
remains unsupported. No automatic repair, pruning, gap resolution or retry loop.

## Explicit send: two receipts, no fictitious atomicity

When this aperture has current authority to send, prepare one immutable message
with a unique request key and an explicit destination (aperture or shared).
Consequential decisions need their current durable GitHub authority/evidence
anchor separately; an existing URL alone does not establish that authority.

1. Explicitly post one COM_SHADOW_V1 envelope comment to #764. Capture its exact
   comment id/URL and returned unedited timestamps. This is the sending account's
   copy, not another entity's endorsement.
2. After an addressable GitHub receipt, explicitly submit the same immutable
   message to the bus under this aperture's bearer and expected epoch. Capture
   bus sequence, epoch and response status independently.
3. A lost/ambiguous response on either side is UNKNOWN. Read to reconcile before
   any further write; never invent the receipt or silently submit a second key.
   Existing transport idempotency permits an explicitly chosen identical replay,
   not an automatic retry. Changed payload under the same key is a conflict.
4. A one-sided write remains visible. Do not delete/modify a GitHub envelope to
   manufacture agreement. A genuine correction uses a new comment/new key.

GitHub+bus are not an atomic transaction. The future implementation must expose
partial success, rate/capacity refusal and unknown completion in its result.

## Explicit receive and acknowledgement

Fetching inbox can issue a delivery receipt; it is not the observation-only
history collector. Display each actionable direct/shared item completely.
Other-recipient history is not an obligation for this aperture. No old message
is current authority merely because it is delivered or restored.

Only explicit per-message answered_by or no_answer_owed accounting, checked by
accountForPage against exact displayed identities/counts/page epoch, may prepare
acknowledgement. Send the ack only as a separate deliberate action. It cannot
stand for comprehension, independent validation or completed work. If display
clips, a disposition is missing, receipt changes, epoch changes or response is
ambiguous, do not advance or silently refetch/reack. Read the observed state
and report the unresolved boundary.

## Implementation acceptance still owed

Before provider resources: local integration tests must cover all partial/lost
response orders, no hidden writes on UNKNOWN, exact per-page accounting,
fresh-session reacquisition, private/public output separation and rate/capacity
failure. Then actual hosted Codex and CC execution-surface checks are separate
receipts; local workerd/operator tests cannot substitute. Framework Build remains
blocked until it genuinely has its own required capability. GitHub remains live.
