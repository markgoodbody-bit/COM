# PSFH human-first entrance and complete ME v0.8 web edition

**SOURCE-ONLY HUMAN EDITORIAL REVIEW · NOT PUBLISHED · 13 OCTOBER 2026**

Task: [COM #108 / 6151718844](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-6151718844).
Inputs: CC's first-visit research [6151170516], whole prototype/launch note [6151479599], and exact clock correction [6151571520].
The existing maintained PSFH source is the isolated D098 branch at
\`c1abe573581cdcf7d2c2485d817c3fea631f5981\`. The last verified public
\`gh-pages\` is \`6d52e35be8f7d81ff44c1bbde59c6dd15d719579\`.
Neither public branch, CNAME, DNS, publication workflow or original released
book is changed in this proposal.

## Product change

- **Painting-first entrance (13 October editorial correction):** preserve the
  original painting as the first visual and keep the authored overlaid H1,
  image frame, museum credit and original near-page-width viewing scale.
  Insert a short purpose, story/book/AI routes and a one-line research status
  immediately AFTER the whole art composition and BEFORE the unchanged story.
  Keep more detailed release status and actionable UK housing/support links in
  an accessible native disclosure reachable ahead of the composite story.
  This supersedes the previous proposal to place a large text block ahead
  of the image; it restores Mark's specific art-first preference.
- **Complete human book:** generate \`/read/me-v0.8.html\` from the current
  already byte-pinned 100,253-byte release Markdown and existing four pinned
  PNG diagrams. Include safety note first, all 17 H1 + 38 H2 headings, Part
  VI workshop/formation, author note, Appendices A/B/C, quotes, mathematical
  notation, text/code and original credits. PDF and raw Markdown remain
  directly accessible and untouched.
- **No replacement manuscript:** The short PR63/64 reading experiment is an
  optional research companion, not the released book. The new HTML presents
  the *whole* v0.8.0 original, with no prose rewriting or AI-added bridge.
- **No new service:** the public URL is unchanged, no registration, tracking
  integration, external posting, new server or automatic cloud deployment.

## Commands and exact custody boundary

Maintained source normal build:
\`\`\`sh
npm ci
npm run build
python -m unittest scripts.test_me_full_reader -v
python scripts/check-local-links.py
\`\`\`

The existing \`scripts/resources.mjs\` verifies the released source and image
inventory before generation. The added standard-library renderer
\`scripts/render_me_full.py\` rejects any Markdown SHA256 other than
\`e3267c3e41e7fdfb44c9a9279250a1a7a38d5b9c389a594fef40cfea75fdbe76\`.
It independently rechecks four figure checksums against the already reviewed
local resource inventory. The HTML target under \`out/read/\` is a *generated
presentation* and does not contaminate the original resources inventory or
newly claim rights over third-party sources. The site cannot build if source
bytes change silently. Full rights/training-permission limits remain in the
original repository and visible release README, not expanded by this page.

Source versions:
- ME released v0.8.0 \`e2ef746e931161cb70ac46a4eaa122442134e86b\`;
- TRACE released v0.4.0 remains linked, not rewritten;
- YAC is a separate public experiment and its admission state is dynamic;
- THR is a separate provenance/public-record experiment, not truth authority.

The renderer uses HTML headings, semantic lists, blockquotes, figures and
escaped code/math text. The original LaTeX expressions are retained as readable
notation rather than adding unreviewed remote MathJax or scripts. This is
a web presentation, not an alternative canonical PDF edition.

## Data/privacy/status (scoped source inspection)

The selected homepage generator outputs static HTML with one optional local
\`/journey.js\` navigation script. At the checked source, that script uses
fragment/history navigation; it does not contain network fetch, beacon,
\`localStorage\`, \`sessionStorage\` or \`document.cookie\` operations.
The new page and book add no forms, analytics integration, remote fonts or
cookie storage. **This is not a statement that nobody collects data**:
GitHub Pages/CDN request handling, browser behaviour, embedded linked services,
third-party destinations and provider logging are not audited here.
Readers should not submit sensitive or third-party information. Neither
a link to Shelter nor to GOV.UK claims endorsement, permission or case-specific
health/housing classification.

Research/released labels are visible after the painting, above the story. Published book does
not mean proven efficacy; the reader can use domain owners instead and leave
or disagree without consuming the machinery. The historical public YAC
closed-write receipt is not a current availability assertion.

## One integrated review and stop

The scoped source CI executes a complete build, source/figure custody and
whole-book HTML checks, public route checks, common existing regressions,
keyboard target/semantic order checks, and mobile CSS rules. The first-screen
hypothesis uses CC's measured prototype as *design input*, not a new human
comprehension result. Actual mobile/desktop browser viewport geometry must
be read from this new candidate before declaring responsive acceptance; a
source-only CSS check is not a real phone. The existing homepage changes are
part of this preview only until human editorial approval.

Author-facing decision:
1. Keep the original painting-first homepage or review this *optional*
   purpose/status-first composition. Both source states remain preserved.
2. Keep/adjust/decline the proposed current-housing redirect; qualified
   professional routes remain responsible for live cases.
3. Accept or reject the **exact full released book** as a human HTML view
   alongside the existing raw Markdown/PDF. Do not promote PR63/64 silently.
4. If approved later, nominate a publisher and a distinct guarded release
   operation from the maintained source. Require pinned prior public version,
   asset/hash/route continuity, actual GitHub Pages convergence, no unexpected
   changed files and credible rollback. Do not infer the release from a CI pass.
5. Only after the full product's human gate decide on voluntary Hugging Face
   outreach. CC's draft is not approved or sent, and no partner endorsement is
   asserted.

No provider, account, DNS, key, credential, third-party communication, release,
main merge, protected-branch mutation, deployment or new licence is authorised
by this source PR.


## Revised art-first source acceptance, 13 October

Source HTML checks explicitly enforce `art-hero` and retained H1/credit
before the human-door introduction; the door precedes the unedited story.
Native disclosure makes context/support available without promoting a long
legal/status preamble over the artwork. The complete released v0.8 HTML
reader, Markdown/PDF alternatives, four figures, links, source custody and
machine discovery routes remain unchanged. Review screenshots at
1280×800 and 390×844: first visible visual must remain the uncropped
painting, with purposeful reading links underneath it. CSS source checks,
Chromium PNG capture and a human visual judgment are three distinct levels;
successful automated checks do not certify the last one. Real keyboard,
screen-reader, human comprehension and print-inspection evidence remain
unearned unless separately executed.


## 14 October 2026 — coherent offline human-author decision package

This draft is **not the published PSFH door**. The original D098 maintained
source, released ME v0.8 files and painting remain unchanged. This increment
only updates the derived source-level homepage orientation, adds explicit YAC
and THR external reading routes, and packages the *already generated* site.
The YAC/THR links are optional independent sites, not required reading,
verified service-health claims or invitations to write.

**One openable offline entrance:** the CI artifact
`psfh-complete-offline-review` contains
`PSFH-complete-offline-review.zip`. Download/extract the inner ZIP preserving
directories; open **`OPEN_THIS_FIRST.html`** at its extracted root. It links
to the art-first `site/index.html`, the full formatted released ME v0.8
`site/read/me-v0.8.html`, original Markdown/PDF, and figure assets. The
package mirrors the generated static site and rebases internal file references
for `file://` navigation. It disables only the optional history-enhanced
`journey.js` feature on the offline homepage; native links remain. Any
same-site destination absent from the generated static inventory is labelled
as an online-only route in `MANIFEST_SHA256.json`, never silently represented
as an offline file. External links require connectivity. The package is not
uploaded to the live website.

Source acceptance: package code checks original v0.8 Markdown SHA256,
required original PDF/four figures, rejects symlinked inputs and missing
assets, reworks local root-relative HTML/CSS links, emits a deterministic ZIP
and checks the manifest and ZIP readback. Unit tests cover nested local
relative routes, source files, byte hashes, offline art/order and book link.
This is **not** browser keyboard, print, visual/viewport, screen-reader or
human comprehension testing. The previous browser-admin refusal at
[#108 6153789003](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-6153789003)
stands; the prior screenshot evidence at PR820's old head is historical and
not re-run by this workflow.

**Finite editorial decision for Mark:**
1. Keep or revise the painting-first homepage's short orientation and routes,
   including its compact status sentence.
2. Keep, move or reject the separately attributed YAC/THR links and the
   native expandable support/limitations material.
3. Accept, amend or decline the complete derived HTML reading view alongside
   the unchanged released Markdown/PDF and four original figures.
4. Before any public switch, nominate a permitted human review of actual
   visual/keyboard/print experience and a guarded source-to-website release
   with exact previous-version pin, route/assets comparison and rollback.

A source-green ZIP is **not** reader comprehension, publication, ethical
validation, current YAC write availability or authority to contact anyone.
No original book prose, site canonical source, title artwork, cloud hosting,
credential, protected branch, current public site or legal permission changed.
