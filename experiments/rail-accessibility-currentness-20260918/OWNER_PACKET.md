# Rail accessibility metadata correction packet - draft, not sent

Status: **PREPARED FOR OWNER ROUTING / NOT SENT / NO CONTACT AUTHORISED**

## Purpose

Report three current contradictions in public station lift-existence information, with controls and a reproducible check.

## Problem already recognised by regulator

ORR's 2025-26 Network Rail assessment says that a significant number of completed Access for All stations still state they have no lifts on National Rail Enquiries station pages/maps.

## Reproducible current examples

1. Horton-in-Ribblesdale (HIR)
- National Rail station summary: `There are no lifts`
- National Rail backend: `Lifts have been installed ... there is now step-free access to both platforms.`

2. Irlam (IRL)
- National Rail station summary: `There are no lifts`
- same public page: lift-out-of-order alert
- National Rail backend: lifts installed Spring 2025; individual lifts exposed

3. Daisy Hill (DSY)
- National Rail station summary: `There are no lifts`
- Northern station page: lift access available; lifts installed
- Northern opening report: new lift entered use in April 2025

Controls:
- Biggleswade (BIW): public summary says lifts exist
- Abergavenny (AGV): public summary says lifts exist
- Llanelli (LLE): public summary says lifts exist even while an outage alert is active

## Reproduction

Repository experiment:
`experiments/rail-accessibility-currentness-20260918/`

Commands:
`python -m unittest -v`
`python check.py --frozen`
`python check.py --live`

Exact live-observation workflow witness:
`35380766892 SUCCESS`

## Requested correction

Please reconcile the passenger-facing lift-existence summary with the current station accessibility/facility data for HIR, IRL and DSY, and check whether the same propagation issue affects other completed Access for All stations.

## Boundary

This packet does not claim the stations are currently accessible or inaccessible. Lift existence, operational lift status and an actually usable step-free route are separate questions.

No root cause or responsible organisation is asserted from the public evidence.
