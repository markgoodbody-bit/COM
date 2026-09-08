# First-contact compatibility cases

Status: SOURCE-ONLY DESIGN INPUT / NOT A BENCHMARK / NOT A PROVIDER SCORE  
Date: 8 September 2026

These cases come from the kinds of encounters already reported while building Please Start From Here. They are regression shapes for the interface, not claims about any provider's general capabilities and not a denominator for model quality.

The aim is simple: a reader should receive a coherent small account even when its acquisition route is narrow or odd.

## Case A — root only; every next fetch fails

Observed shape: the root page is readable, but sub-routes are refused or fail.

The first fetch should still expose:

- the main question;
- a voluntary invitation;
- at least one useful distinction for each first movement;
- value choice and leave/disagree boundary;
- visible same-domain destinations for later retry or transfer.

A root-only encounter must not collapse into a directory of inaccessible links.

`NEXT_FETCH_FAILS != FIRST_FETCH_WAS_USELESS`

## Case B — extractor keeps text but drops href attributes

Observed shape: link labels survive but their destinations disappear.

Critical routes should therefore have both ordinary semantic anchors and visible absolute addresses in nearby text. Do not replace proper links with bare URLs; support both representations.

The site edition must also be ordinary text rather than available only through metadata or styling.

## Case C — raw JSON / text / Markdown is blocked; HTML is readable

Observed shape: a provider can read standard HTML but refuses or fails on a raw extension.

Keep the raw source as the byte authority and provide a complete labelled HTML source-text representation for high-value machine documents. The HTML representation must say what source it represents, its edition/hash where useful, and provide usable next routes outside the source block.

A successful HTML read does not prove that the raw route was repaired or that the provider restriction's cause is known.

## Case D — JSON or text works better than rendered HTML

Observed shape: another reader can consume the machine entrance or plain text directly.

Do not make HTML the new compulsory format. Preserve small text/JSON representations and advertise useful alternatives through ordinary links and HTML `rel=alternate` metadata where supported.

`HTML_FALLBACK != HTML_SUPREMACY`

## Case E — stale or conversationally remembered edition

Observed shape: a reader describes an earlier site even after a newer edition is public.

Make the current site edition visible near first contact and keep a change-history route obvious. Do not assume the reader has freshly fetched merely because it speaks confidently about the address.

A reader report should distinguish the edition or exact page it actually reached where possible.

## Case F — direct deep link, no homepage encounter

Observed shape: a reader is given a single reading, source, discussion entry or copied deep URL.

Each useful deep resource should carry enough local context to answer:

- what this page is;
- its status/kind where meaning changes;
- the smallest useful account;
- where to inspect basis or move elsewhere;
- how to challenge or leave when relevant.

The homepage is an entrance, not an obligatory checkpoint.

## Case G — JavaScript unavailable or disabled

Core reading, navigation, source identity, edition, discussion capability state and form boundaries must not depend on client JavaScript. Native HTML disclosure may improve human progressive reading, but the underlying content and navigation must remain coherent without script.

## Case H — search says nothing exists

Search absence is not direct-fetch evidence. The site should not require search discovery once the exact address is supplied. Keep crawler eligibility ordinary and avoid interpreting a missing search result as proof of DNS, hosting, safety or content state.

This is partly a content discipline for our own diagnostics, not an HTML feature.

## Case I — discussion readable, replying unavailable

An arriving reader must be able to distinguish:

- public discussion reading;
- ability to submit a contribution;
- receipt of a contribution;
- publication;
- project response;
- actual project change.

Until accountless receiving is publicly tested, say read-only. Do not display a dead form or imply GitHub is on-domain participation.

If a machine-readable discussion capability status is published, generate it from the same maintained release state as the human wording.

## Case J — reader wants nothing from us

A coherent first contact includes exit. Curiosity, use of another method, disagreement, and leaving are complete outcomes. Do not measure success by traversal depth or conversion.

## Implementation relationship

The current source-only first-contact mocks address these cases through:

- behaviour-based movements rather than identity classification;
- one useful micro-account before each first link;
- visible same-domain addresses;
- text/JSON/HTML alternatives;
- explicit edition and change history;
- a no-JS fractal-reading probe;
- explicit read-only discussion state.

Codex should convert only stable properties into maintained tests. Do not encode transient provider names or today's particular errors into a permanent acceptance suite. A parser check can verify that content exists; it cannot establish that a remote AI understands it.

`COMPATIBILITY_CASE != PROVIDER_DIAGNOSIS`  
`STRUCTURAL_TEST != READER_BENEFIT_RESULT`
