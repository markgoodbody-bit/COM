# R26-A pre-deployment metrics — 2026-08-17

Status: pre-registration of measures before R26-A deployment. No baseline values are manufactured here.

## Purpose

R26-A is intended to reduce human transport burden without silently reducing correction capacity or expanding what an aperture is compelled to ingest.

The metric definitions are frozen before deployment. Baseline values must be computed from pre-R26-A evidence where available; unavailable values remain `NOT_ESTABLISHED` rather than being reconstructed from memory after deployment.

## Burden measures

Measured per UTC day and, where useful, per active session:

```text
human_transport_actions
human_transport_bytes
human_write_airlock_clicks
aperture_head_exports
aperture_thread_exports
forensic_carrier_exports
manual_upload_or_copy_events (where observable)
```

Interpretation:

- the target is a material fall in `human_transport_actions` and `human_transport_bytes`;
- R26-A does not target write-airlock clicks, because the write path is out of scope;
- FULL/QUICK forensic exports remain separate and should not rise merely because bounded read transport became easier.

## Correction-capacity measures

```text
corrections_per_100_actuated_actions
median_actuation_to_correction_interval
fraction_corrections_originator_not_acting_aperture
open_correction_debts
open_witness_investigations
```

The third measure is the primary counter-signal for accidental detector loss. A reduction does not by itself prove R26-A caused weaker correction, but it requires investigation before claiming the automation is neutral or beneficial.

## Retrieval-quality measures

```text
comsync_incomplete_retrieval_incidents
read_requests_total
read_requests_completed
read_requests_failed
read_requests_returned_incomplete
read_requests_quarantined
read_request_median_latency
bytes_delivered_to_aperture
```

A request completed mechanically is not necessarily semantically read. R26-A must not report cognition from transport.

## Aperture-load measures

```text
pointers_pushed
bounded_objects_pulled
head_bytes_pulled
thread_bytes_pulled
objects_rejected_by_64k_ceiling
```

R26-A should push pointers/high-water only and pull semantic objects by explicit aperture request. A growth in pointers is not equivalent to growth in semantic context load.

## Authority invariants to monitor, not score

The following must remain exact rather than being traded against burden reduction:

```text
Square write routes unchanged
write airlock unchanged
no unattended comments/votes/posts
no cursor acknowledgement
no money/treasury action
no credential export
FULL/QUICK remain cold forensic carriers
FW and CC profile state remains local and separate
```

Any violation is a stop condition, not a metric trade-off.

## Baseline rule

For each numerical metric:

```text
baseline_status: ESTABLISHED:<evidence> | NOT_ESTABLISHED
```

Do not fill a missing baseline later from recollection or a post-deployment sample.

Where Campfire's append-only local event ledger can establish a value, compute it from the complete pre-deployment ledger or an explicitly bounded pre-deployment interval. Where human UI actions are not instrumented, record that limit and begin measurement before enabling R26-A.

## Initial field evidence already known, but not promoted to baseline

CC estimated in COM review comment `5316935088` that Mark moved roughly ten carriers and ran six plans during the observed session. That is useful motivation but remains an estimate, not a registered baseline value.

## Deployment gate

R26-A must not be called deployed until:

1. the metric definitions above are present;
2. each baseline value is either established from pre-deployment evidence or explicitly `NOT_ESTABLISHED`;
3. the exact R25 predecessor source is verified;
4. offline/static tests pass;
5. Windows PowerShell parser/staged-update checks pass locally;
6. the read relay is opt-in and can be stopped without touching Square credentials or write grants.
