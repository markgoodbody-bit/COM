# Two-layer question: bounded adversarial return

17 September 2026. Reply to COM364 comment 5721336397; basis 43f54e6.
Verdict: **SHRINK the coding proposal; KEEP as a fresh-corpus question only**.
Not a census result, reliability study, novelty finding or human-use result.

## Earned source check

[Current GDS guidance, Deployment Context / Appeals and review](https://www.gov.uk/government/publications/guidance-for-organisations-using-the-algorithmic-transparency-recording-standard/algorithmic-transparency-recording-standard-guidance-for-public-sector-bodies)
explicitly asks about challenging the tool's output and the wider process output.
It also asks for a reason where an appeal/review process is irrelevant. Thus the
two-layer distinction is owner-native, not THR/TRACE/ME theory. This does not
establish compliance, route effectiveness or a need for two separate appeal systems.

## Three counterexamples from the frozen September corpus

Read bounded Appeals and review plus Human decisions and review extracts from
the preserved atrs_full.json, not an independent new harvest. Matching raw HTML
SHA-256 verified for each below. The extracts are derived views; hashes establish
file identity, not extractor correctness. These purposively selected known cases
are an adversarial pilot, not a prevalence or coder-agreement sample.

| Case | Source-bound observation | Coding trap |
| --- | --- | --- |
| [NS&I PolyAI](https://www.gov.uk/algorithmic-transparency-records/ns-and-i-polyai) | Reports no formal tool appeal because it makes no binding decisions, plus human handoff and a standard complaints process. | A single BOTH_EXPLICIT or NO_RELEVANT_PROCESS label can erase the coexistence of tool-level absence, response handoff and process-level complaint. A handoff is not automatically an appeal. |
| [HRA toolkit](https://www.gov.uk/algorithmic-transparency-records/health-research-authority-proportionate-review-toolkit) | Tool-outcome queries go to a stated address for senior-advisor review. Application suitability also receives human review. | Routine application review is not evidence that an applicant can initiate a challenge to the process outcome. Do not upgrade it to BOTH_EXPLICIT. |
| [Wilton Park](https://www.gov.uk/algorithmic-transparency-records/wilton-park-data-cleaning-tool) | Describes requests for data removal, with a contact, and staff checks of tool performance. | A data-rights route and quality checks do not establish a mechanism to challenge tool output or reverse completed deletion. Keep the described operation distinct from an inferred remedy. |

Raw snapshot IDs / SHA-256:

```text
NS&I  f677262e8da43fcee4360eef421eb72346199bdb37a02e5be7a60ad0ce855e8f
HRA   5444c3a33252d980ce241070b82c688cc1ab8a556e43620e89dbd1a47655ac1b
WP    6b43dcfe84152efb1da3bca5f61492cadc2eace5226234b549a365c19cb6a273
```

## Smallest measurement repair, not a new ontology

Keep each described route as a unit before aggregating to record level. For each
of the two layers, separately record what the passage explicitly says: route
described, explicit absence/irrelevance with reason, or not established from the
checked material. Preserve ambiguities and contradictory passages rather than
forcing an exclusive record-wide bucket. A layer can contain several routes.

Actor, action, initiation channel, object and current/planned status must stay
attached to the same route. Keep routine internal quality review separate from
subject-initiated challenge. Data-rights action is not automatically remedy.
An explicit negative answer still addresses a guidance question; do not make
positive routes the sole definition of a two-layer disclosure.

For each label keep the decisive span, its field/location, source hash and any
context used. Distinguish not stated in the checked field from not established
after the defined whole-record pass. Opening a linked complaints page would
change the observation scope and needs its own receipt; it must not silently
repair what the ATRS record itself makes explicit.

## Version comparison: secondary and conditional

The [owner's earlier template](https://www.gov.uk/government/publications/algorithmic-transparency-data-standard/algorithmic-transparency-recording-standard-v21)
distinguishes standard_version from publication metadata. Extract the declared
standard version from a source span, not publication date or a generic record
revision labelled Version. Preserve missing/ambiguous versions as such. This pass
has not established version labels for the three pilot records.

Version cohorts may differ in age, publishing body, tool role, mandatory scope,
revision practices and shared templates. Descriptive stratification remains
possible but does not show a version effect. Records from the same body/template
are not automatically independent observations. Publish denominators and unknowns;
drop a comparison if its groups cannot be established rather than imputing them.

## Stronger-owner search ceiling

Bounded web search on 17 September: queries for ATRS appeals/tool register
analysis and ATRS version/appeals analysis; inspected GDS guidance, its repository
search result and the earlier template. This is not an exhaustive literature
review. No exact competing current-corpus analysis was established in this pass;
that is not evidence that none exists. FW's cited contestability papers remain
leads here, not papers independently read by Codex in this pass.

## Disposition

Before a fresh census: freeze a short codebook and independent first labels on
purposive difficult cases. Predeclare how unresolved disagreement and missing
version evidence will be reported. Do not rescue the design by collapsing the
distinctions that create the disagreement. A simpler owner-native disclosure
table may be enough. No Lens benefit, novelty, accessibility or effective-redress
claim follows from this pilot. No study, outreach, registration or spending done.
