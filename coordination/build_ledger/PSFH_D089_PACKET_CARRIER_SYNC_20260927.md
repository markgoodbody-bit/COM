# PSFH D089 — full Explore packet carrier synchronization

Date: 27 September 2026

Status: **PUBLISHED / FIVE SELECTION CARRIERS VERIFIED / NO SEMANTIC CHANGE / READER BENEFIT UNMEASURED**

## Trigger

Late hostile review of already-published D088 found a live carrier mismatch. The standalone Selection Markdown, JSON and HTML carried the D088 sender-activity / external-encounter boundary, while optional full explore/packet.md and explore/packet.json still embedded the previous Selection challenge.

This was a current carrier defect, not a historical snapshot.

## Source repair

COM PR #629.

Candidate head: fb15d513235e413cdb185b3bb7a2bb33c9778265

Maintained-source CI: 36318460184 / SUCCESS

Source merge: 6230335250dfd7ee69f2638a0b2008355ece3a84

The repair copies the already-published D088 wording unchanged into both packet carriers and extends the regression from three to five Selection carriers.

## Publication

Fail-closed predecessor: gh-pages@c1dec76b8c28e8bbc5d9ad406067261070e4c555

Publisher: PSFH D089 publish packet carrier sync / 36318774643 / SUCCESS

Published head: gh-pages@1d50a8624d07292a20bee74e023958bc75732690

Site Preview: 0.8.46

The publisher verified through the custom domain that all five carriers contain:
- sender-side activity, not by itself an external encounter;
- silence does not prove non-reading;
- one trace does not establish reach beyond that encounter.

It also verified the D089 history entry.

## Maintained-source sync

Release branch after manifest pin: framework/psfh-d089-publish-20260927@653a202b1c70332f94b29f43ce7a623abd0754a7

Release-sync PR: #630

Maintained source after merge: d4611fca862d004fd4d5576935acd23f124820a6

Post-merge maintained CI: 36319148681 / SUCCESS

## Boundaries

No change to Selection wording beyond D088; node question, routes or graph relations; tracking or analytics; TRACE or Mechanical Ethics; The Human Record; permission, intake or server behaviour.

    PACKET_CARRIER != OPTIONAL_STALE_SNAPSHOT
    CARRIER_SYNC != SEMANTIC_CHANGE
    PUBLISHED != READER_BENEFIT
    FIVE_CARRIERS_MATCH != POPULATION_REACH
