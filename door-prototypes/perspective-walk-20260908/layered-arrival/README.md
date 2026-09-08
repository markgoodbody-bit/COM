# One layered arrival, not a new website

DRAFT / OFFLINE / NOT DEPLOYED / NO READER RESULT

One proposed journey through the existing futures reading. It sits beside the
maintained Explore build and does not modify that build or its source library.
Seven records separate entry, situation, small account, depth, perspective,
challenge and basis. Each has JSON, Markdown and script-free HTML. An optional
packet provides the combined reading. No public endpoint is added.

The HTML retains noindex as an offline preview. Do not copy this folder to the
public site or restore the retired public-page indexing exclusion.

## Reproduce

From this directory within the existing PR114 source checkout:

```sh
python -m unittest -v test_trial
python build_trial.py --output NEW_EMPTY_DIRECTORY
```

Open start.html or packet.html in the output, or read their JSON/Markdown forms.
The default source is the existing parent library.json. Its exact 74d72cf SHA-256
is checked; changed library bytes require explicit reinspection. No network,
publication, tracking, visitor input or model calls occur in the builder.

## Preservation contract and its limits

The futures wording is source-derived and unchanged. The organisation, situation
prompt and challenge framing are declared proposals. The smallest futures card
retains the full counterexample. source_fields uses symbolic selectors by node id,
not RFC JSON Pointers. No semantic equivalence or practical advantage is claimed.

The JSON packet retains all seven complete records. Rendered packets preserve
each card's title, section text and labelled routes, not every machine metadata
field. Within-packet routes point to the corresponding document anchors; the four
external source, alternative-method and discussion destinations remain intact.
No external source body is bundled or silently fetched.

An intact individual page has status/boundary text and a route to its basis.
Detailed source/proposal attribution and the source hash are not repeated in
every rendered card. A copied excerpt can lose that route and context. Neither
an HTML-link check nor a successful fetch establishes detached-copy continuity.

## Repair discovered during the comparison

The initial c4da27c4 prototype's JSON packet preserved routes, but its Markdown
and HTML packets copied only section prose and substituted seven sibling-page
links. They omitted all four external destinations. The existing 14 tests passed
because packet tests checked prose, not route preservation. That earlier
cross-representation claim was too broad. Historical files and receipts remain
at c4da27c461363081949fcca2c92ba0c5a4e4bda4; they are not the repaired outputs.

The repair renders each card with its own labelled routes in the packet. Internal
links use local fragments rather than another file; source and outward links
retain their exact URLs. Only packet.md and packet.html change in the 24 outputs.
All 21 individual representations and packet.json remain byte-identical.

Executed in this pass: 20 local tests passed. Six added tests run against the old
builder first produced five failures and one missing-renderer error; after the
repair they passed. Checks cover per-card route/context preservation, distinct
outbound links, local fragment targets, escaping and refusal of unsafe links.
All 24 outputs matched through a temporary loopback HTTP server; a missing route
returned 404; the server stopped. The production generator suite was not rerun.

Browser inspection was attempted, not completed. Playwright's default browser
binary was unavailable; the installed system Chromium refused the loopback URL
with ERR_BLOCKED_BY_ADMINISTRATOR. No bypass was attempted. These results do not
establish rendering, browser fragment behaviour, accessibility conformance,
provider admission, public delivery or reader usefulness.

Current start.json: 1,056 UTF-8 bytes; unchanged packet.json: 9,846 bytes.
Repaired packet.md: 7,188 bytes; packet.html: 9,783 bytes.
Output-tree SHA-256:
`f67f2fdffa1a71b0a87bbd3641742ad4714b5ca0348249ff4cb54c450930dc91`.

## Measured trade-off, not a usability verdict

Markdown response-body sizes, excluding headers, tokens, tool wrappers, latency
and monetary cost:

| Reading route | Responses | Bytes |
|---|---:|---:|
| Existing complete futures reading | 1 | 1,607 |
| Prototype small futures card | 1 | 834 |
| Small account + detail + perspective | 3 | 2,831 |
| Above, preceded by the entrance | 4 | 3,606 |
| Repaired complete prototype packet | 1 | 7,188 |

The existing page was read at published revision edefdeee6ba890ea0776d1fb518549120c5b276d;
its reproduced bytes match Git blob 314f6358459e8dc8826b9a909f028666ca2bf911.
The three-card route contains the same five futures text fields, but also adds
boundary, standing and navigation text and repeats some fields. It is not an
equal-content or behavioural comparison. The complete probe additionally carries
welcome, privacy and design-context material. Its growth is the cost of restoring
missing routes, not measured improvement.

Provisional integration choice: keep the existing complete reading as a direct
depth option; offer a smaller account for readers who need only that distinction.
Do not require a journey through several fragments to reconstruct a small page.
Packet access remains optional, and fragments are not independently retrieved
resources. Test actual reader needs rather than ranking by clicks or byte count.

## Boundaries and next step

Read UNKNOWN_MAP.md. Its questions remain open unless this pass supplies a narrow
structural observation. The fixed live Partial views publication is separate and
complete in Codex's return 5585148725. Codex retains sole site publication. This
repair does not authorise deployment or expansion across ten nodes. Any later
integration must preserve useful current URLs and retire duplication deliberately.

No new licence, account, spending, external contact, reader study or scheduler.
