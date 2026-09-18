# Shipaton viability read — mobile spike

Status: **TECHNICAL FEASIBILITY PARTIALLY ESTABLISHED / STORE FEASIBILITY UNKNOWN**

## What this spike tells us

The mobile concept does not need the full PSFH website.

A credible first app can be very small:
- one guided private flow;
- one summary;
- one explicit delete/reset;
- one optional share;
- one cosmetic supporter entitlement.

That is a much smaller store object than porting the existing public journey.

## Technical path

Current stable Expo SDK is 57. RevenueCat documents Expo as a supported route and documents Preview API Mode in Expo Go; real purchases need an Expo development build.

The spike therefore has a credible technical sequence:

```text
SOURCE SPIKE
-> TYPECHECK
-> EXPO GO INTERACTION TEST
-> DEVELOPMENT BUILD
-> REVENUECAT OFFERING + ENTITLEMENT
-> INTERNAL / CLOSED STORE TEST
-> 1.0 STORE REVIEW
-> SHIPATON SUBMISSION
```

The first three steps are developer work. The remaining steps cross account/store/terms gates.

## Biggest schedule risk

Shipaton's FAQ explicitly warns that app review can take days and recommends submitting at least one week before the deadline.

With a 30 September deadline, the store gate is now more consequential than the coding gate.

A beautiful prototype on 29 September is worthless for the Peace Prize if it is still in review.

## Current product hypothesis

The app is strongest when it is **not** “Mechanical Ethics mobile” or “TRACE mobile”.

Working promise:

> A quiet private place to get oriented when something important is difficult, uncertain or moving faster than you can think.

Core value:
- reduce cognitive sprawl;
- separate evidence states;
- expose reachable action;
- expose time/hardening;
- produce one correctable next step.

This is adjacent to planning/journaling products, so novelty must come from the quality of the interaction and the PSFH orientation, not from claiming a new category.

## RevenueCat fit without distorting the gift

Possible paid digital good:
**Supporter theme**.

Properties:
- cosmetic;
- no core function removed;
- purchase has an in-app effect;
- entitlement can be restored;
- judges can be given a promo route if store tooling permits.

Before store work, re-check:
- Shipaton's exact category criteria;
- Apple/Google policy for the chosen purchase/product shape;
- RevenueCat offering requirements;
- promo-code/testing route.

## What remains unknown

These are the actual go/no-go variables:

1. Which store account already exists, if any?
2. Can that account submit a new production app immediately?
3. Is there any mandatory closed-testing history / identity verification delay?
4. What is the fastest credible platform: iOS, Google Play, Samsung?
5. Can a RevenueCat product be configured and approved in the same window?
6. Is the optional supporter purchase acceptable to the PSFH purpose?
7. Can we produce a real icon, screenshot and <=2 minute device demo without cutting corners?
8. Does the Peace Prize permit/like this exact interpretation of social good?

## Current disposition

```text
APP CONCEPT = VIABLE ENOUGH TO CONTINUE TESTING
CODE VOLUME = SMALL
REVENUECAT SEAM = STRAIGHTFORWARD
STORE PATH = UNKNOWN / LOAD-BEARING
DEADLINE RISK = HIGH
PURPOSE DISTORTION = CONTAINABLE IF CORE REMAINS FREE
```

Next useful action is **not more UI**.

Next useful action is to establish the store/account path. If no store route can credibly reach public release in time, stop immediately and keep this spike as a reusable mobile prototype.
