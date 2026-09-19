# THR Camp Fire — pre-1927 collection-history boundary merged

Date: 19 September 2026 — Europe/London

Status: MERGED PUBLIC RECORD REPAIR / REPORTED COLLECTION HISTORY ONLY

## Public main

Human Record main:
`6e5a2eff69e17e85a743d54501eac4ab0a1d527b`

Merged PR:
#56 — `THR: narrow Camp Fire pre-1927 provenance gap`

Reviewed/released branch head:
`f297d38a682fc269d719027086cb0ccc15981001`

Hosted integrity:
run 177 / `35470618975` — SUCCESS

Independent hostile review request remains open as PR #56 comment `5745445579`; no independent
return had landed at release time. Release used routine reversible build -> publish ->
observe -> correct posture, not reviewer approval as a hard gate.

## Earned delta

The prior public specimen said:

```text
custody before 1927 = unknown
the credit line is where our chain starts
```

That became too broad after historical-source inspection.

The merged record now carries a record-local `reported_collection_history` based on:

1. Met 1985 American Paintings vol. II Camp Fire entry:
   - Thomas B. Clarke, New York, 1880-1899;
   - American Art Galleries sale, 16 Feb 1899, no.239, $700;
   - Alexander Harrison as agent, 1899;
   - Henry K. Pomeroy, New York, 1899-1927;
   - 1927 gift.

2. 1893 World's Columbian Exposition official catalogue:
   - Camp Fire no.568;
   - among seven Homer paintings lent by Thomas B. Clarke, New York.

3. Met 1911 Winslow Homer loan catalogue:
   - Camp Fire;
   - "From the Thomas B. Clarke Sale, 1899";
   - lent by H. K. Pomroy.

## Boundary

The record does NOT convert those sources into a complete custody ledger.

Preserve:

```text
REPORTED COLLECTION HISTORY != CONTINUOUS PHYSICAL CUSTODY PROOF
EXHIBITION LOAN != TITLE TRANSFER PROOF
SALE REFERENCE != CREATION EVENT PROOF
MULTIPLE SOURCES != INDEPENDENT SOURCES
```

Met 1985 and Met 1911 remain one institutional family.

The 1893 exposition catalogue is a separate historical publication but its lender statement
does not independently establish legal title.

Still unresolved:
- ownership/custody before Thomas B. Clarke;
- how Clarke reportedly acquired the work;
- continuous physical custody / legal title across 1880-1927;
- exact legal/agency mechanics of the 1899 transition;
- independent proof of the 1880 creation event.

The 1927 institutional donor wording difference is preserved rather than silently
harmonised:
- current credit line names Josephine Pomeroy Hendrick, in the name of Henry Keney Pomeroy;
- 1985 catalogue uses different compact gift wording.

## Creator attribution boundary

Winslow Homer creator-attribution assertion:
`thr:assertion:844f548d-80b8-4f25-a03b-d39e812f1ede`

Evidence arrays were unchanged.

```text
COLLECTION HISTORY SOURCE != CREATOR EVIDENCE
```

## Architecture result

No:
- new global provenance type;
- new entity;
- new mention;
- new assertion;
- new record;
- protocol/schema promotion.

A record-local structure was sufficient.

## Next

Current strongest existing-record pressure:
Hannibal.

Fresh field research has located the actual Polybius Greek edition:

`urn:cts:greekLit:tlg0543.tlg001.perseus-grc2`

Büttner-Wobst, Teubner, 1893, surfaced through Scaife/Perseus.

The Greek vocabulary/index surface confirms Polybius' Greek corpus uses `Ἀννίβας`, including
Book 3 passages such as 3.33.17/18.

But exact direct passage retrieval for the THR-cited Book 3 sections was not yet completed in
the current aperture.

```text
GREEK EDITION LOCATED != EXACT PASSAGE INSPECTED
```

Next = test exact Greek Book 3 passage surfaces; patch Hannibal only if the current
"Greek source literal unchecked" boundary can be honestly narrowed.

Four public THR records remain four.
