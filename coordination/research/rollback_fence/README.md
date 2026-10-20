# Framework-Lab — rollback/replay fence frontier probe

**20 October 2026. ISOLATED SOURCE-ONLY SYNTHETIC RESEARCH. Not operational execution authority, not a production safety proof.**

## Actual trigger

Codex's native 20 October guest probe ([COM #873, comment 6288146781](https://github.com/markgoodbody-bit/COM/issues/873#issuecomment-6288146781)) restored a pre-claim queue database backup *after* the live database recorded STOP and consumption. The restored copy was PAUSED, with the previously consumed task again QUEUED and consumed=0. **The resurrected task was never run**. This demonstrates rollback of local task records, not actual re-execution.

## Proposed invariant to attack

A restored VM or queue can reconstruct **descriptions**, not **authority**.

For every externally visible effect, a trusted controller *outside every relevant local rollback domain* would need to atomically and durably consume the uniquely scoped intent **before** the effect could begin. The supervisor must mediate every effect path; a reusable permit must not survive inside a restored snapshot. A durable STOP latch and spent intent ledger must survive local rollback. A disconnected authority means no effect starts, not local permission to proceed. Crashing after consumption but before the effect produces UNKNOWN/no automatic replay, so this only promises **at-most-one admission**, not exactly-once effect or guaranteed completion.

A STOP request arriving while the authority is disconnected is itself **UNCONFIRMED**; the system must not infer that STOP was durably recorded. On reconnection, a stale task could otherwise be admitted. This unresolved STOP-acknowledgement path is an explicit falsification target.

The required witness is current controller authority, not an old internally consistent snapshot or Git receipt. Monotonic fencing is a hypothesis to test, **not** evidence of a solved queue.

## Reproducible bounded model

`python3 coordination/research/rollback_fence/fence_model.py`

A standard-library reference model with six tests, run locally on 20 October 2026 (6/6 PASS). One negative control shows a local-only guard can produce *two* synthetic effects after backup restoration. The proposed external-fence model explores 8^0 + 8^1 + ... + 8^5 = 37,449 bounded event sequences for one synthetic intent; the at-most-one synthetic effect property holds **under its explicit assumptions**. The model never executes external tasks, has no credentials, and is not a queue worker.

## Engineering proof obligations still OPEN

- An independent nonrollbackable controller actually exists, has durable atomic writes, and has authenticated human/controller intent, precise operation scope, generation and stable unique identity.
- All real side-effect paths are mediated; a local worker cannot replay cached permissions, spoof a controller or bypass the fence.
- Crash/timeout after reservation-before-effect remains UNKNOWN, with explicit reconciliation; no automatic retries.
- STOP is externally acknowledged before it is claimed, persists across restoration, and no unacknowledged STOP permits future launch after reconnect.
- Partition, concurrent workers, backups of **both** local and controller domains, generation re-use, power loss, disk corruption, audit visibility, tampering, trust boundaries and compensation are realistically tested.
- Any release must separately establish controllable rollback and genuine Mark authority. No implicit queue activation, model inference, provider mutations, security policy changes, or unattended worker start.

## Owner challenge

Claude Code: independently break assumptions against the *actual* existing bridge; if feasible build one **isolated source-only, synthetic fail-closed epoch/STOP/consumption adapter** and adversarial tests, not a live replacement. Preserve the original failing rollback test as a regression; include STOP-during-partition and effect/commit crash cuts. Report terminal result/UNKNOWNs via #874.

Codex: preserve the previously assigned finite native YAC Workerd/Miniflare reader task, not this CC-owned adapter. No duplicate test suite.

Build: independent acceptance and integration gate. Do not promote this toy into a production control plane. Current operational B queue stays PAUSED, candidate STOPPED until actual external fencing and authority are established.

## Mechanical Ethics/TRACE lens

The issue crosses *three clocks*: when the effect occurred, when STOP became binding, and when a copied record was observed. A stale internally correct database is not an independent witness of current permission. Harm hardens when a duplicated effect occurs; correction must be routed **before** that boundary. The positive opportunity is substantial: safely delegated bounded work could lower Mark's routine load once earned. **CORRECTION != RESTORATION.**
