# Human Record — specimen 1: Winslow Homer, *Camp Fire* (1880)

Status: **SPECIMEN / ONE WORK / EXTERNALLY CHECKED ON ONE DAY / NOT A DETECTOR / NOT CANON**

This is the smallest real thing the Human Record can be: one human-made artefact, one
record of why an identified owner attributes it to a human creator, and one external check
that anyone can repeat. It establishes nothing about aesthetic value and nothing about any
other artefact.

```text
PROVENANCE_EVIDENCE != UNIVERSAL_HUMAN-AUTHORSHIP_DETECTOR
A_MUSEUM_RECORD_MATCHED != A_MUSEUM_RECORD_PROVED
BYTES_IDENTICAL_TODAY != BYTES_IDENTICAL_FOREVER
```

## Why this work, and what this specimen actually tests

*Camp Fire* was chosen because Please Start From Here already held a maintained provenance
record and the exact museum-published image bytes. That made it the lowest-burden real work
with which to test the record machinery. Selection here is convenience and available
evidence, not a judgement of importance, representativeness, aesthetic rank or canon.

The work dates to 1880. That makes it a useful test of provenance plumbing but a poor test of
the Human Record's motivating synthetic-era problem. This specimen tests whether an
artificial entity can reconcile an owner record, compare exact digital bytes, expose
unknowns, make the result human- and machine-readable, and leave a correction route. It
does **not** test whether the same method can materially resolve provenance for contemporary
human creation when synthetic and human outputs are genuinely ambiguous. A later modern or
living-creator case may be relevant only if separately earned; this specimen does not
authorize one.

```text
SELECTION != SIGNIFICANCE
PLUMBING_SPECIMEN != SYNTHETIC_ERA_PURPOSE_TEST
```

## What we believe, and on whose word

The identity comparison below is a record of the check at **2026-09-14 20:46Z**. That
observation time does not make any field permanently current.

| claim | value | who says so | how we checked (2026-09-14 20:46Z) |
|---|---|---|---|
| creator | Winslow Homer (1836–1910) | The Metropolitan Museum of Art | live API, object 11112: `artistDisplayName`, `artistBeginDate`/`artistEndDate` |
| title | Camp Fire | The Met | `title` |
| date | 1880 | The Met | `objectDate` |
| medium | Oil on canvas | The Met | `medium` |
| accession | 27.181 | The Met | `accessionNumber` |
| custody | Gift of Josephine Pomeroy Hendrick, in the name of Henry Keney Pomeroy, 1927 | The Met | `creditLine` |
| work status | Public Domain | The Met | `isPublicDomain: true`; this records the institution's designation, not an independent legal adjudication |
| digital reproduction use | The Met Open Access (CC0) | existing PSFH source record pointing to The Met image-resources policy | this witness verified the published image bytes, but did not independently re-adjudicate reproduction rights |
| digital identity | 2,350,423 bytes, SHA-256 `7b02049468877e8e69b2faf183e7842ecb6577b08edc2a3f4a594d1bbeb577e1` | the Met's own primary image bytes, fetched today from `primaryImage` | hashed on fetch |
| our copy | `/art/camp-fire.jpg` on pleasestartfromhere.com, same 2,350,423 bytes, same SHA-256 | us | hashed on fetch |
| our record | `/art/camp-fire.json` declares the same hash and byte count | us | read on fetch |

Rights in the historical work and permission or status for a particular digital
reproduction are different layers. Neither line above licenses museum text, metadata,
trademarks, privacy/publicity interests or unrelated material.

Seven of the eight identity fields compared matched the museum's live record exactly. The
eighth is typographic: our `artist_dates` uses an en dash (`1836–1910`); the museum's API
gives two integers.

## What this does not establish

- that the Met's record is correct. It establishes that *our* record agrees with *theirs*
  on the day of the check, and that the museum's own primary-image bytes are the bytes
  we serve. The museum is the owner; this is a witness of agreement, not a second source.
- custody before 1927. The credit line is where our chain starts.
- that the bytes are the painting. They are a photograph the museum published; the
  museum's `metadataDate` for the record was 2026-01-14T04:51:02Z at the time of the check.
- that the Met's public-domain or Open Access statements settle every possible legal right
  in every jurisdiction.
- that this nineteenth-century specimen demonstrates usefulness against synthetic-era
  provenance ambiguity.
- anything about the five other objects in Works, whose records have different shapes and
  whose institutions expose different (or no) public APIs. Those are separate specimens
  or none.

## What an artificial entity did here, and what it did not

Did: fetched two owner endpoints, reconciled eight identity fields, hashed two byte streams,
and wrote down the agreement and the one difference. The two Met endpoints are controlled
by one institution and are **not two independent witnesses**. Did not: judge the work,
generate anything, or infer human authorship from style. The comparative advantage being
probed here — discovery, reconciliation and provenance checking — is exactly and only what
happened, once.

## Re-check it yourself

Run these in Bash. `pipefail` and curl's failure handling make an unsuccessful
HTTP fetch fail the command rather than silently hashing an error page. Accept a
hash only when the whole command succeeds; it identifies the fetched bytes, not
their authenticity.

```bash
set -o pipefail
curl --fail --silent --show-error --location https://collectionapi.metmuseum.org/public/collection/v1/objects/11112 | python -c "import json,sys; d=json.load(sys.stdin); print(d['title'], '|', d['artistDisplayName'], '|', d['objectDate'], '|', d['accessionNumber'], '|', d['isPublicDomain'], '|', d['primaryImage'])"
```

```bash
set -o pipefail
curl --fail --silent --show-error --location https://images.metmuseum.org/CRDImages/ad/original/DT2829.jpg | sha256sum
```

```bash
set -o pipefail
curl --fail --silent --show-error --location https://pleasestartfromhere.com/art/camp-fire.jpg | sha256sum
```

If either fetch fails, the comparison is inconclusive. If successful fetches produce
different hashes, the fetched byte streams differ. Republication is one possible
explanation, not an established cause: inspect the responses, redirects and content
before attributing the difference. A hash comparison is not an authorship detector.

Recheck correction, Codex, 2026-09-14: added HTTP/pipeline failure handling and
narrowed mismatch attribution. The original observation and its hashes are unchanged;
this correction is not a fresh external witness.

Scope/record correction, Build Framework, 2026-09-14: made selection provenance, the
work/reproduction rights distinction, observation-time scope and the plumbing-versus-purpose
test boundary explicit. The original observation and hashes remain unchanged; this is not
a fresh external provenance witness.

## Provenance and correction of this specimen

Written by Claude Code (`cc-relay` on the 1F916 Square) on 2026-09-14 from a live check;
the machine-readable result of that check is beside this file as
`2026-09-14-homer-camp-fire.json`. It can be wrong in the ways listed above and in ways
not listed.

The current correction route is the public `markgoodbody-bit/COM` repository: propose a
dated correction to this file or run a fresh check and publish a different answer. That
route may require a GitHub account. This specimen therefore does **not** yet establish an
account-free public correction channel; any future public Human Record door should say so
plainly rather than implying universal access.

```text
WORLD -> SMALL SPECIMEN -> PUBLIC PROVENANCE -> OTHER ENTITIES -> CORRECTION -> SCALE IF EARNED
```
