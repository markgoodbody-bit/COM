# Rail accessibility metadata correction packet - draft, not sent

Status: **PREPARED FOR OWNER ROUTING / NOT SENT / NO CONTACT AUTHORISED**

## Purpose

Report three current contradictions in public station lift-**existence** information, with controls and a reproducible check.

## Problem already recognised by regulator

ORR's 2025-26 Network Rail assessment says that a significant number of completed Access for All stations still state they have no lifts on National Rail Enquiries station pages/maps.

## Reproducible current examples

1. Horton-in-Ribblesdale (HIR)
- National Rail station summary: `There are no lifts`
- National Rail Accessibility Map surface: `Lifts have been installed ... there is now step-free access to both platforms.`

2. Irlam (IRL)
- National Rail station summary: `There are no lifts`
- the same passenger page carries a lift-out-of-order alert, which itself implies a lift exists
- National Rail Accessibility Map surface says lifts were installed in Spring 2025 and exposes individual lift records

3. Daisy Hill (DSY)
- National Rail station summary: `There are no lifts`
- Northern station page: lift access available; lifts installed
- Northern opening report: a new lift entered use in April 2025

Controls:
- Biggleswade (BIW): public summary says lifts exist
- Abergavenny (AGV): public summary says lifts exist
- Llanelli (LLE): public summary says lifts exist; an outage alert remains separate existence evidence

## Reproduction

Repository experiment:
`experiments/rail-accessibility-currentness-20260918/`

Commands:
`python -m unittest -v`
`python check.py --frozen`
`python check.py --live`

The checker intentionally does **not** classify whether a station's lifts are working now or whether a complete step-free route is currently usable. Those questions have stronger owner surfaces and can change independently of lift existence.

## Requested correction

Please reconcile the passenger-facing lift-existence summary with the current station accessibility/facility data for HIR, IRL and DSY, and check whether the same propagation issue affects other completed Access for All stations.

## Boundary

This packet does not claim the stations are currently accessible or inaccessible. Lift existence, operational lift status and an actually usable step-free route are separate questions.

No root cause or responsible organisation is asserted from the public evidence.

## Current owner routes — not used

National Rail's current Contact Us page says:
- station accessibility/facility comments can be directed to the station operator;
- questions about National Rail website/services can be sent to National Rail Enquiries.

Primary first route for this packet:
National Rail Contact Us / website route:
https://www.nationalrail.co.uk/help-and-assistance/contact-us/

Northern accessibility/customer route is a possible second route for Northern-managed station content:
https://www.northernrailway.co.uk/help/contact

Regulatory context / escalation owner:
Office of Rail and Road passenger accessibility:
https://www.orr.gov.uk/monitoring-regulation/rail/passengers/passenger-assistance/passengers-disabilities

No message has been sent through any of these routes.
