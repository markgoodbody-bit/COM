# PSFH D090 — effective-copy correction

Date: 28 September 2026

Status: **PUBLISHED / LIVE-BYTE VERIFIED / MAINTAINED SOURCE SYNCED / EXTERNAL READER RETURN / POPULATION BENEFIT UNMEASURED**

## Trigger

`zora` returned one concrete criticism at Campfire Square post `6978`, comment `82966`: a correction can reach a plausible but wrong copy — a cached export, mirror or superseded version — while the copy that an audience or process actually relies on remains unchanged.

The live Correction node said a route needed enough time “to affect the target”, but did not identify the effective copy or distinguish sending a correction from evidence that the relied-upon target changed. D088/D089 supplied an internal reproduction: the corrected Selection node was live while two optional full-packet carriers still held the previous wording until the later synchronization.

This is one external correction plus one project-local reproduction. It is not endorsement, adoption, a complete PSFH review, a population result or a new TRACE gap.

## Maintained-source repair

COM PR #663 — `PSFH D090: bind correction to effective copy`.

Reviewed candidate head:
`7c874aea39443d5a949d30cec53206d7ffc57196`

Exact-head maintained CI:
`36359328549 / SUCCESS`

Source merge:
`b30a37cc29770686611b5a648c7116bba00091a3`

Added boundary:

> A correction route needs detection, access, the capacity to act, enough time and the right target: the version or copy that people and processes actually rely on. Sending a correction does not show that target changed; check the target copy or a receiving-side receipt.

The wording is synchronized across five current carriers:
- node Markdown;
- node JSON;
- node HTML;
- full-packet Markdown;
- full-packet JSON.

A maintained regression requires the effective-copy, sent/change and receipt boundaries in all five.

## D090 publication

Release branch:
`framework/psfh-d090-publish-20260928`

Publisher arming head:
`0e67fbe2e8058eae7979aa71e1e42bc9866ed2df`

Exact release head after publisher manifest pin:
`f3344c00f1fcc80ce79bf82ff6a4c910017f5da3`

Fail-closed expected predecessor:
`gh-pages@1d50a8624d07292a20bee74e023958bc75732690`

One-shot publisher:
`PSFH D090 publish effective-copy correction / 36359621385 / SUCCESS`

Published:
`gh-pages@11c2751d686a4fac710a61cdfc5e5840781fda1b`

Site Preview:
`0.8.47`

The publisher rebuilt the full site, ran the maintained Node/Python/link suite, refused publication unless `gh-pages` still matched the exact D089 predecessor, preserved deployment-control files, published the exact build and verified all five Correction carriers plus D090 history through the custom domain.

Four transient maintained-CI runs on the release branch failed while history/edition files were uploaded sequentially before the publisher had pinned the matching manifest. They are not exact complete-candidate passes and are not represented as such. The fail-closed publisher ran from the complete arming head, performed the pin before building and succeeded.

## Independent live-byte check

After `gh-pages` advanced, a separate no-cache custom-domain check observed:
- manifest Site Preview `0.8.47` and `correction_effective_copy_d090` provenance;
- the three new boundaries in standalone Correction Markdown;
- the same boundaries in full-packet Markdown;
- D090 history in served HTML.

Observed SHA-256 values:
- live manifest: `e41a0c7a3e649db0b7791878ae05c0647f469780b5bd845f141386f6a34f84b7`;
- live Correction Markdown: `61805861b4331729ed7d09c146de079ad65267b0d037cb3ebc56bd4e1b68330e`;
- live packet Markdown: `8e3029b2f58c54f91ce93dddba5552db0bf5d6db991b712601fa374fde9c5678`;
- live change-history HTML: `74f569ea5d2b0762e3879fac8f7faef0fe9adb2e4d943fce3f1230c03aba7a00`.

## Maintained-source release sync

COM PR #665 copied exact D090 release bookkeeping back into maintained source without copying the one-shot publisher workflow.

PR head:
`039e8cb408fdbacad6d581f8524b143806925882`

Exact-head maintained CI:
`36359731345 / SUCCESS`

Maintained-source merge:
`5eccae1403bee1d6774fb33622f84fb6424120e5`

Post-merge maintained CI:
`36359780443 / SUCCESS`

## Boundaries

No new node, relation, graph, schema, tracking, analytics, intake or server behaviour was added. TRACE, Mechanical Ethics and The Human Record were unchanged. No personhood, authority, licence, training-policy or efficacy claim follows.

```text
PLAUSIBLE COPY != EFFECTIVE COPY
SENT CORRECTION != TARGET CHANGED
RECEIVING-SIDE RECEIPT != POPULATION BENEFIT
EXTERNAL CORRECTION != ENDORSEMENT
PUBLISHED != VALIDATED
```
