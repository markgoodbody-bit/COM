# THR Hannibal — bounded Greek source-literal candidate

Date: 19 September 2026 — Europe/London

Status: DRAFT PUBLIC-RECORD REPAIR / NOT MERGED / NOT CANON

## Public baseline

Public THR main at branch point:

`6e5a2eff69e17e85a743d54501eac4ab0a1d527b`

Four public records remain four.

## Field pressure

The Hannibal public record explicitly said the checked Polybius surface rendered
"Hannibal" in English and that THR had **not inspected the Greek source literal**.

Perseus identifies Greek edition:

`urn:cts:greekLit:tlg0543.tlg001.perseus-grc2`

Passage-specific vocabulary/token lists were inspected for:
- Polybius 3.33.17
- Polybius 3.33.18

Each list contains `Ἀννίβας` once.

The full Scaife reader redirect was inaccessible through this aperture.

Attempts to retrieve the other THR-cited Polybius passage word-list endpoints were
not reliable enough to support any wider claim.

Therefore the earned delta is only:

```text
POLYBIUS 3.33.17-18
-> GREEK DIGITAL-EDITION TOKEN LISTS
-> Ἀννίβας ATTESTED
```

not:

```text
WHOLE PASSAGE VERIFIED
MANUSCRIPT VERIFIED
ALL POLYBIUS PASSAGES VERIFIED
HISTORICAL IDENTITY PROVED
```

## Draft PR

PR #57:
THR: narrow Hannibal Greek source-literal boundary

Current exact head:
`b40e071e5b443311f32593f442d92d776da92410`

Hosted:
`Validate Human Record integrity — run 181 / 35471618313 — SUCCESS`

First hosted run at `ff77cdd...` correctly failed two public-record contract tests:
1. record version was still frozen to 0.1.0;
2. machine-record Greek source copy did not exactly match registry source copy.

Both were repaired:
- test now expects public record version 0.1.1;
- machine record carries the exact canonical registry source object;
- human view and catalogue pins point to final record blobs.

## Candidate changes

- new bounded Greek digital-edition/index source + observation;
- Hannibal entity/mention notes narrow the Greek source-literal boundary;
- public machine/full record candidate version 0.1.1;
- human reader aligned;
- catalogue view basis aligned;
- no fifth record;
- no historical identity resolution change;
- no new ontology/type.

## Ceilings

```text
GREEK NAME FORM ATTESTED != HISTORICAL IDENTITY PROVED
PASSAGE TOKEN LIST != MANUSCRIPT WITNESS
ONE PASSAGE CHECK != WHOLE BOOK VERIFIED
DIGITAL EDITION != ANCIENT CARRIER
```

## Review

Bounded hostile review requested on PR #57 comment:
`5745550856`

Target:
- evidence over-upgrade;
- identity over-upgrade;
- English/Greek source conflation;
- scope creep;
- registry/view/catalogue inconsistency;
- test contract drift.

Disposition pending:
`PASS_WITH_CEILINGS` or smallest concrete `REPAIR`.

## Next

```text
DO NOT MERGE BY MOMENTUM

REVIEW PASS
-> MERGE DECISION MAY BE RECONSIDERED

REVIEW REPAIR
-> SMALLEST FIX

MEANWHILE
-> CONTINUE REAL FIELD PRESSURE ELSEWHERE
```
