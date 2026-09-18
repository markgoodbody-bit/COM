# Please Start From Here — Shipaton mobile feasibility spike

Status: **ISOLATED MOBILE SPIKE / NOT PUBLIC APP / NOT STORE SUBMISSION / NOT PSFH CANON / NO REVENUECAT ACCOUNT OR PRODUCT CONFIGURED**

This is deliberately small. It tests whether the useful core of Please Start From Here survives translation into a phone-sized interaction without becoming a worksheet, a moral score, a WebView or a paywall.

## What exists

A single-screen Expo / React Native app with a short guided flow:

1. **What is happening?**
2. **What do you know?**
   - observed
   - reported
   - inferred
   - unknown
3. **What matters now?**
4. **What is reachable?**
5. **What changes with time?**
6. **What is one next move?**
7. a plain-language summary that can be copied/shared later.

The spike keeps the core free.

A RevenueCat adapter is wired only as an **optional supporter-theme seam**. If no RevenueCat public SDK key is supplied, the app remains fully usable and no purchase UI is active. No secret keys belong in this repository.

## Why this is not the website in a wrapper

The mobile object is intentionally narrower than pleasestartfromhere.com.

It does not try to carry:
- the full PSFH journey;
- TRACE;
- Mechanical Ethics;
- the Works room;
- COM;
- a framework tutorial.

It asks whether one small useful act can stand on its own:

> help a person separate what is happening, what they know, what matters, what remains reachable, what time changes, and one next action.

If that is not independently useful on a phone, the Shipaton route should die.

## Run locally

Current stable basis chosen for the spike:
- Expo SDK 57;
- React Native 0.86;
- RevenueCat React Native SDK 10.x.

```bash
cd competition/shipaton_psfh_mobile_spike
npm install
npm run typecheck
npx expo start
```

Expo Go can preview the interaction. RevenueCat documents that its React Native SDK runs in Preview API Mode in Expo Go; real purchases require a development build.

## Optional RevenueCat configuration

The spike reads public SDK keys from environment variables:

```text
EXPO_PUBLIC_REVENUECAT_IOS_KEY
EXPO_PUBLIC_REVENUECAT_ANDROID_KEY
```

No key -> no RevenueCat configuration.

If configured, the adapter looks for entitlement:

```text
supporter
```

and the current offering's first package. A successful purchase enables an alternate in-app supporter theme. Core guidance remains free.

This is only a technical seam. Creating a RevenueCat account, store products, pricing, tax/payment configuration, promo codes or store listing remains a separate human/account/terms gate.

## What this spike can establish

It can answer:
- can we get a credible native interaction quickly?
- does the mobile flow have a reason to exist separate from the website?
- can the monetisation requirement be isolated from the gift?
- is the codebase small enough to polish before 30 September if store infrastructure already exists?

It cannot establish:
- App Store / Play Store acceptance;
- Shipaton eligibility;
- Peace Prize competitiveness;
- store review time;
- whether Mark has the necessary developer accounts;
- whether the supporter purchase is acceptable under final store policy/Shipaton terms;
- user benefit.

## Kill conditions

Kill the Shipaton route if any of these hold:

1. the interaction feels like a worksheet rather than help;
2. the store-account/review path cannot credibly complete before the deadline;
3. RevenueCat forces core help behind payment;
4. the app is merely the website inside a native shell;
5. sufficient polish would consume more important work for a weak Peace Prize fit;
6. store/account/payment obligations create disproportionate human burden.

```text
SPIKE_WORKS != STORE_PATH_WORKS
STORE_PATH_WORKS != PRIZE_FIT
MOBILE_EXISTENCE != USER_BENEFIT
```
