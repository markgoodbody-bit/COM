# THR Hannibal — bounded Polybius recovery-route repair

Date: 25 September 2026

Status: **MERGED / MAIN INTEGRITY GREEN / PAGES GREEN / FOUR RECORDS REMAIN FOUR / NO SCHEMA GROWTH**

Purpose:
Recover useful preservation work that remained stranded on old Hannibal branches, while removing the edition overclaim those branches had accumulated.

## Trigger

Current THR main at `c7be1efb5ca66673c398cdc19eb4c0f2489246d9` still carried Hannibal record v0.1.2 and marked the Polybius/Thayer source preservation route `not_yet_checked`.

Old PR #63 / stacked repair #71 had explored an Internet Archive / New York Public Library Volume II carrier, but those branches were based on older main and mixed a useful preservation route with a stronger claim about the scanned copy's exact printing/reprint identity.

A fresh owner check of:
https://archive.org/details/historieswitheng02poly

confirmed the public item currently identifies:
- Polybius, *The Histories*;
- Volume 2;
- W. R. Paton;
- Cambridge: Harvard University Press; London: Heinemann;
- publication date `[1922]`;
- New York Public Library contribution;
- Greek and English on opposite pages.

The current public item metadata does not by itself establish the exact physical printing/reprint state of the scanned copy.

## Repair

Human Record PR #77:
`THR: re-port bounded Polybius recovery route onto current Hannibal record`

Exact reviewed head:
`a80f2c1f51528b50b5eae24bb6a8635606205642`

Hosted exact-head validation:
`36198799678 / SUCCESS`

Merged THR main:
`b2182211cb56a013ea6c146d3500214fa5352f91`

Post-merge integrity:
`36198841848 / SUCCESS`

Pages build/deployment:
`36198841933 / SUCCESS`

## What changed

- Hannibal record version `0.1.2 -> 0.1.3`;
- Polybius source preservation state now records a public institutional recovery route through Internet Archive / NYPL;
- the same preservation state is mirrored into `registry/sources.json`;
- the human Hannibal view exposes the route and its limits;
- exact source-record blob pins were refreshed;
- the Hannibal browse card was explicitly re-pinned through the #76 source-basis digest guard;
- its browse summary prose was not changed;
- the focused public-record version test was advanced to v0.1.3.

## What did not change

- no new historical assertion;
- no claim that the Thayer HTML is archived or byte-identical to the scan;
- no claim that item metadata establishes the scanned physical copy's exact printing/reprint state;
- no new entity/schema/source type;
- no change to the four-record count;
- no record-5 promotion;
- no stewardship/governance change;
- no claim that preservation establishes historical truth.

Preserve:

```text
PRINTED EDITION ROUTE IDENTIFIED != EXACT WEB REPRESENTATION PRESERVED
ITEM METADATA != PHYSICAL PRINTING STATE
ARCHIVE SCAN != THAYER TRANSCRIPTION
PRESERVATION ROUTE != HISTORICAL TRUTH
DIGEST MATCH != SUMMARY TRUE
```

## Old branches

PR #63 and stacked repair PR #71 were closed as superseded after #77 merged. Their review/history remain available in GitHub; they are no longer presented as current integration candidates.

No external archive contact, copying around access controls, credential action, spend or new record occurred.
