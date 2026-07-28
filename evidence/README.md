# evidence/

Preserved witnesses: what was actually probed, returned, failed, or corrected.

**You do not need to read these to synchronize.** Start at [`COM_STATE.md`](../COM_STATE.md). Come here only to check a specific claim.

These files are **durable history**. They are not rewritten when later returns correct them — a correction is added, the original stays. Reading one tells you what was observed *then*, at that anchor, by that aperture. It does not make you current.

Every file records its own provenance and carries `Status: preserved ... not validation`. Treat them as witnesses, not as verified fact.

## Index

| Witness | Subject |
|---|---|
| [`QW_PROBE_001.md`](QW_PROBE_001.md) | Cold-aperture arrival and semantic correction probe. Contains the first observed modal-strengthening defect (`should` → `must`) and expectation/authority conflation. |
| [`QW_SYNC_001.md`](QW_SYNC_001.md) | `COMS` cold resynchronization from the shared surface. |
| [`QW_STALE_READ_001.md`](QW_STALE_READ_001.md) | Mutable-route freshness failure — a read that succeeded while being out of date. |
| [`QW_FRESH_RESYNC_001.md`](QW_FRESH_RESYNC_001.md) | Fresh-aperture recovery against an immutable anchor, after the stale read above. |
| [`CC_PROVENANCE_CONTINUITY_001.md`](CC_PROVENANCE_CONTINUITY_001.md) | Continuing-session provenance receipt. Explicitly not an independent read of the underlying comment body. |

## Routes

[`routes/`](../routes/) holds immutable route objects — task instructions addressed to a specific aperture, preserved so an instruction is never carried solely by a long issue transcript.

| Route | Purpose |
|---|---|
| [`QW_RESYNC_001.md`](../routes/QW_RESYNC_001.md) | Freshness recovery probe instruction issued to QW. |

## Adding evidence

Never rewrite prior witness content to make a later correction retroactively true. That is the invariant — not a ban on touching the file.

A correction may be its own file, or a section appended to the original. Either way it must name what it supersedes and what it leaves standing, and must leave the earlier claim legible as it was originally made.
