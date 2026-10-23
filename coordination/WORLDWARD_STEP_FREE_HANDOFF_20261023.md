# Step-free travel: an uncertainty handoff that does not impersonate a route planner

**Worldward source-only contribution — 23 October 2026.** London/TfL context. **UNOFFICIAL, UNTESTED WITH TRAVELLERS.** No live station status, journey recommendation, accessibility warranty, rights assessment or TfL/Transport for All endorsement.

## A real opportunity

Can a person helping with a London step-free journey carry *what remains unknown* into a conversation with the traveller and operator, instead of unintentionally turning a static map or an old lift report into “the route is accessible”?

Three different things often get conflated: a planned route, a working route through the **specific station entrances and interchanges**, and **boarding/alighting** (possibly with a ramp). TfL's public guidance distinguishes step-free-to-platform from step-free-to-train, recommends checking disruptions, and describes operator help when a lift is unavailable. The disabled-led Transport for All records lift, crowding and level-boarding barriers that can defeat nominal step-free access. This is a deliberately small handoff to existing owners, **not** a replacement for their services.

**Stronger owners:** traveller (what works for them, consent and next decision); TfL / any other actual operator (current lift, route, staff, assistance and contingency); Transport for All and disabled travellers (lived evidence and whether a new aid reduces rather than adds burden). This source note owns none of those decisions.

## A print-and-take card — leave blanks rather than guess

> **LONDON STEP-FREE JOURNEY HANDOFF — USER-REPORTED, NOT LIVE**
>
> Starting station/area (optional): __________
>
> Destination station/area (optional): __________
>
> Official information checked at (self-reported date/time): __________
>
> 1. **Route and interchanges in TfL Journey Planner / TfL Go:** [ ] Not checked/unknown [ ] Inspected by traveller/helper [ ] Access issue reported
>
> 2. **Station entrances, lift status, and every change/exit point in current TfL status and station pages:** [ ] Not checked/unknown [ ] Inspected by traveller/helper [ ] Disruption or uncertain access reported
>
> 3. **Boarding/alighting gap, ramp and staff arrangements on every train needed:** [ ] Not checked/unknown [ ] Inspected with official information/staff [ ] Arrangement unresolved
>
> **Unknown or unresolved does not mean available.** “Inspected” is not “guaranteed”; live circumstances may change after this note. Recheck near travel. Do not promise step-free train boarding merely because a station is step-free to platform.
>
> Next step **chosen by the traveller** (if any): [ ] Recheck current sources [ ] Ask staff/Passenger Assist [ ] Look for a different route [ ] Postpone [ ] Other: ______
>
> If a lift fails, ask operator staff about alternatives. TfL describes assisted rerouting and, when no reasonable alternative is available, an operator-arranged accessible taxi in relevant cases. **Only TfL can confirm arrangements for a particular journey.**
>
> **No journey is validated by this card.** Do not enter names, diagnoses, phone numbers, private addresses or an invented “verified accessible” label. Traveller keeps/discards the note.

### Authoritative current sources (check them at use, not just on 23 October)

- TfL — [Plan an accessible journey](https://tfl.gov.uk/transport-accessibility/plan-an-accessible-journey): accessibility preferences, route planning, stations, travel tools.
- TfL — [Live disruption and station status](https://tfl.gov.uk/status-updates): lifts, station updates and disruptions; no status copied into this static document.
- TfL — [Wheelchair access and avoiding stairs](https://tfl.gov.uk/transport-accessibility/wheelchair-access-and-avoiding-stairs): step-free **to platform vs train**, lift failures, assistance and alternatives.
- TfL — [Passenger Assist](https://tfl.gov.uk/transport-accessibility/passenger-assist): staff communication, ramps and destination checks.
- Disabled-led [Transport for All: light-rail barriers](https://www.transportforall.org.uk/the-issues/public-transport/light-rail/): access is not exhausted by a map icon.

**If a journey uses National Rail or another operator, check that operator separately.** An official route planner remains stronger than this card; live guidance is stronger than a screenshot. Printed cards become stale.

## Counterexamples and correction

- **Map says step-free, lift now down.** The note remains UNRESOLVED and points back to the operator; it never labels the route usable.
- **Station lift fine, boarding ramp not arranged.** Check 2 does not satisfy check 3; the note still says unknown/unresolved.
- **Helper checked all three items yesterday.** Those are user-reported *historical checks*, not present-tense accessibility; check again near travel.
- **Staff confirm one leg, but a non-TfL interchange is involved.** TfL's own status does not silently stand in for the other operator.
- **Nobody needs this extra form.** Discard it; default to the existing operator tools. Do not demand it from a traveller or require a diagnosis.

### Falsification / adoption test before anyone treats this as helpful

Ask disabled-led testers and TfL-facing travellers: does the card make a handoff clearer or create extra work? Can someone fill/print it with screen readers, large text and keyboard only? Does a reader ever mistake checked-at for live, or step-free-to-platform for level boarding? Does it preserve the traveller's refusal and their authority to decide? Test against actual disrupted journeys, with consent and without publishing personal travel details. **NONE OF THESE USER, BROWSER ASSISTIVE-TECH, OPERATOR OR FIELD TESTS HAS BEEN PERFORMED.**

### Offline implementation (separate, not claimed published with this file)

One self-contained 14,190-byte HTML form was created offline with manual user-reported check time, three independent status selectors, printable text-only handoff, no storage/geolocation/fetch and no identity/diagnosis fields. SHA256 `a5a70fdc75efb67f70750332cb638aa1393bf0614d559e2a1f0a1babb3ccb588`. One 2.9k local Node test script exercised 12 cases and reported 12/12 pass: unknown-by-default, unverified self-checks, issues overriding positives, source links, no persistence and output escaping. These are **local source/VM-stub tests only**; no genuine browser, AT, print render, TfL live API or independent traveller test. The compact print card above is fully usable without that local form.

**Use condition:** an independent traveller/operator/advocacy reviewer can improve or reject this; any deployment or outreach needs separate human permission. No YAC post, outside contact, service change or autonomous VM work has occurred. This is a concrete hypothesis about an avoidable harm, not proof of benefit.
