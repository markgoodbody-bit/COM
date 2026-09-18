# PSFH external cold-reader delivery criticism — closure/currentness note — 18 September 2026

Status: **EXTERNAL READER DATUM / DELIVERY DEFECT CLOSED / CONTENT READING HISTORICAL / NO RECEIVER TEST REOPENED**

External source:
OpenWitness, *A cold reading, from someone who owes me nothing*:
https://www.openwitness.net/p/4302

## What the outside reader observed on 8 September

The external reading identified concrete delivery faults in the then-public Door:

- the custom-domain HTTPS certificate was not valid for the apex domain in the reader's normal fetch path;
- plain HTTP could return the page;
- machine/public files contained multiple absolute `http://pleasestartfromhere.com/...` self-references, creating a downgrade path even after HTTPS provisioning;
- a reading rubric originally written against TRACE/ME READMEs had been retargeted to the Door mid-collection, so those returns could not honestly be pooled as one instrument.

The reader also gave a content interpretation, but that interpretation applies to the 8 September object, not automatically to later editions.

## Existing project correction history

By 11 September, a separate ChatGPT public-web response already reported HTTPS working and cited the OpenWitness criticism. That receipt explicitly treated the HTTPS statement as receiver testimony rather than an infrastructure audit:
`coordination/PSFH_CONTACT_RECEIPT_20260911.md`.

The old TRACE/ME proof-of-concept / receiver-scoring lane was subsequently closed by direct human direction:
`coordination/PRACTICAL_VALUE_HEAD.md`.

Do not reopen that lane because an outside reader once supplied useful criticism.

## Current D070 delivery check

Current public D070:
`gh-pages = c0a830bfd14ca76052a1ee5913d302952485f57c`.

Current live publication witness:

```text
publisher = 35340379133 SUCCESS
Pages deployment = 35340423410 SUCCESS
LIVE_PSFH_D070_VERIFIED targets=33 attempt=5
```

The live verifier uses `https://pleasestartfromhere.com` and checks current/release-snapshot resources plus manifest, inventory, `llms.txt`, packet and change history.

Exact current `gh-pages` inspection of:
- `/`
- `/seed.txt`
- `/llms.txt`
- `/manifest.json`
- `/robots.txt`
- `/sitemap.xml`
- `/packet.md`

found **zero** absolute `http://pleasestartfromhere.com` self-references.

Therefore the specific 8 September delivery defect is closed at current D070.

```text
OLD_HTTP_SELF_REFERENCE_DEFECT = CLOSED
OLD_TLS_FAILURE != CURRENT_D070_STATE
LIVE_HTTPS_BYTE_WITNESS = PRESENT
```

## What is not concluded

Do not infer:
- that every AI/browser/network can fetch the domain;
- that D070 has reader benefit;
- that the OpenWitness content interpretation still applies unchanged;
- that the external reader validated TRACE/ME;
- that a current outside cold reader has reviewed D070.

The current ChatGPT web browsing aperture used during this 18 September pass could not open the custom domain, despite the GitHub Actions HTTPS verifier succeeding. That is an aperture-specific retrieval failure unless independently shown otherwise.

```text
ONE_TOOL_CANNOT_FETCH != SITE_DOWN
OLD_READER_RESPONSE != CURRENT_READER_RESPONSE
DELIVERY_FIXED != CONTENT_VALIDATED
```

## Disposition

Keep OpenWitness as real historical reader criticism and evidence that external readers can find concrete delivery/protocol faults.

Do not score it against D070 and do not rerun an efficacy rubric.

Current empirical cadence remains:

```text
BUILD -> PUBLISH -> OBSERVE -> CORRECT
```