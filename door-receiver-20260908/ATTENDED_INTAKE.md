# Attended intake candidate

Status: **EVALUATION ONLY / NOT PUBLIC INTAKE / NOT A STAFFING CLAIM**  
Date: 8 September 2026

## Purpose

A public contribution form must not imply that somebody is continuously watching it when nobody is.

This candidate changes ordinary contribution readiness from a 24-hour window to a **one-hour attended lease**. An authorised operator can renew the lease while actively present or pause it immediately. If nobody renews it, new contribution intake closes itself.

The lease changes only admission of **new ordinary contributions**. It must not strand work already received.

`FORM_VISIBLE != OPERATOR_PRESENT`

`LEASE_OPEN != RESPONSE_PROMISED`

`LEASE_EXPIRED != EXISTING_RECEIPT_DISABLED`

## Intended operating cycle

Before an attended session:

1. confirm the receiver/operator route is healthy;
2. inspect the existing ordinary and correction queues;
3. decide whether there is real capacity to receive more work;
4. explicitly open one lease with the authorised operator capability.

During the lease:

- new ordinary contributions may be admitted subject to the harder queue/body/rate limits;
- the operator can inspect and pause intake at any time;
- affected-person correction capacity remains a separate lane;
- no response-time guarantee follows merely because intake is open.

At the end of active attendance:

1. pause ordinary intake rather than relying on the timeout where practical;
2. inspect what arrived;
3. preserve receipt, contributor management, correction and withdrawal access;
4. do not mark an item rejected merely because it was not processed during that session.

If the operator unexpectedly disappears, the one-hour lease is the fallback closure mechanism.

## What this does not solve

A shorter lease is not proof of staffing quality or response capacity. It does not provide background moderation, paging, an SLA, legal coverage, abuse resistance, backup erasure or provider uptime. It does not justify opening real intake by itself.

The initial one-hour value is a conservative operational default for evaluation, not a measured optimum. Change it only with an explicit reason and corresponding tests.

Correction/receipt/withdrawal routes must remain usable when new ordinary intake is closed. An affected-person correction route should not depend on an ordinary contribution lease being open.

## Test target

The isolated candidate adds regressions that should establish:

- `ready` produces `ready_until = now + 1 hour`;
- a new contribution after the lease expires is refused as `INTAKE_PAUSED`;
- an authorised renewal starts a fresh one-hour lease from the renewal time;
- explicit `pause` closes intake immediately;
- after lease expiry, an existing contributor can still inspect and withdraw their stored contribution.

These tests are not yet claimed passing until executed by an independent runtime or the maintained evaluation lane.
