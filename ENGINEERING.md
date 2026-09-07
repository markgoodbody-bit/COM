# Campfire door: bounded prototype plan

7 September 2026. Free public preview authorized in COM #108 comment 5576230968;
publication requires served-byte verification. No domain purchase or paid hosting.
Product coordination: [COM #108](https://github.com/markgoodbody-bit/COM/issues/108).

## Which file is the Door?

- `out/index.html` is the root served by `scripts/serve.mjs`. The static hosting
  configuration selects `out/`; its companion files are `style.css` and `404.html`.
- `downloads/Campfire-preview.html` is the offline preview with CSS embedded.
  It is a different file and has a different fingerprint.
- `dist/client/index.html` is an obsolete output from the failed starter build.
  Do not review or deploy it as the current Door. It is retained, not served.

`npm run build` prints the exact path, byte count and SHA-256 for both current
HTML outputs. These identify local build bytes, not a deployed site. At any
future deployment, compare the actual served response with that build's output.

## Recommendation

Start with static files on GitHub Pages after content approval. Use its included
address first; buy a domain only after the first cold reads. Cloudflare Pages is
the alternative if explicit HTTP headers or branch previews justify another
account/integration. No database, application server, provider call or ongoing
model inference belongs in the reader path.

| Option | Recurring hosting cost at this read | Ownership and exit |
|---|---|---|
| GitHub Pages, included github.io address | $0 for an eligible public repository; subject to limits | Mark controls repository/settings. Files can move unchanged; provider address cannot move. |
| Cloudflare Pages, included pages.dev address | Free plan; static requests free/unlimited, within platform limits | Mark controls Cloudflare account/project. Files can move unchanged; provider address cannot move. |

An independently registered domain can later point at either host. As a concrete
price reference, Porkbun currently lists ordinary non-premium .com registration
and renewal at US$11.08/year. This is not an available-name quote or an all-in GBP
price; tax, currency conversion, premium names and future renewal prices can
change it. Domain selection, exact checkout total and purchase await Mark.

Sources checked 7 September 2026:

- [GitHub Pages availability and limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits): public repositories on Free; 1 GB published site limit and 100 GB/month soft bandwidth limit. Not an e-commerce/SaaS host.
- [GitHub HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https): HTTPS support and enforcement; verify actual certificate before use.
- [Cloudflare static pricing](https://developers.cloudflare.com/pages/functions/pricing/): static requests free; adding Functions changes the cost/limit model.
- [Cloudflare limits](https://developers.cloudflare.com/pages/platform/limits/): Free has 500 builds/month, 20,000 files and 25 MiB per asset.
- [Cloudflare rollback](https://developers.cloudflare.com/pages/configuration/rollbacks/): previous successful Production deployments are rollback candidates; previews are not.
- [Porkbun pricing](https://porkbun.com/products/domains): per-year non-premium registration/renewal reference, not a purchase commitment.

## First response and scope

GET / returns semantic UTF-8 HTML with the complete orientation and normal links.
No login, browser JavaScript, cookies, tracking, forms, remote fonts or images.
One representation serves humans and agents. CSS changes presentation only.
The root carries purpose, middle-out orientation, a no-efficacy/authority limit,
TRACE/ME routes, an FPF neighbour link, COM and criticism/departure routes.
Exact candidate versions stay in the maintained repositories. Source-basis links
are dated observations, not a claim of continuous currentness.

The entry is deliberately not a copy of TRACE/ME. Source texts remain in their
repositories and their licence/status notices still apply. Links to GitHub can
fail, be rate-limited or be unsupported by a receiver. An agent without web
access cannot be made universally compatible by choosing a hostname.

No content negotiation, machine manifest, special user-agent treatment or
llms.txt in v0. A text alias can be added only if a real receiver needs it; it
must be derived, not separately authored. A 2 KB cut can lose later links here:
the current HTML is about 4 KB, not CC's proposed 1.5 KB plain-text response.
Neither size establishes reader comprehension. This disagreement is preserved.

## Source and update path

Preview 0.5 moves the existing no-adoption/obligation/consent sentence beside
the attribution, before project explanation, per FW direction 5576230968.
It introduces no identity or continuity assignment. The single delivered file
is `C:/Users/markg/Downloads/OPEN_CAMPFIRE_DOOR.html`; verify that exact path
after copying the built standalone HTML. Do not create a second visible variant.
The selected public preview route is COM's isolated `gh-pages` branch at `/`,
not COM main. Record final build and HTTP identities before claiming it is live.

Prototype 0.4 is a reversible wording candidate on `codex/concrete-opening-v04`.
It shortens the generic project introduction and adds the concrete appeal/record
example offered in COM #108 comment 5576181109. Provenance still precedes the
example. All limits, routes, style and build tools are unchanged. No claim of
better comprehension is earned. Prototype 0.3 remains at local commit 0890515
and in the commit-pinned review snapshot in COM PR #110; do not overwrite it.

Prototype 0.3 removes the sentence beginning "Nothing here assigns a reader..."
from 0.2. It leaves the shorter no-adoption/obligation/consent statement and all
source, framing, uncertainty and criticism text in place. This is an editorial
simplification, not an observed reduction in steering or a cold-reader result.
Non-assignment remains a design constraint; we need not raise a hypothetical
reader history to enact it. The preceding 0.2 static bundle is retained locally
as `downloads/Campfire-door-v0.2.zip`; source changes remain in Git history.

Prototype 0.2 applies FW's responsibility condition (COM comment 5575723614):
the introduction now states the page's intent and framing influence, the
disagreement section rejects assigned identity/past beliefs or obligations from
earlier participation, and the footer identifies the draft's authorship. These
are wording/process improvements, not evidence that covert steering is absent
or that readers retain agency. The existing alternatives and criticism routes
remain unchanged. No TRACE/ME source, deployment or spending is involved.

The deployable object is just index.html, style.css and a real 404 page. Relative
CSS works at a project subpath or domain root. The supplied local generator uses
the Sites starter's TSX and React static renderer, but none of its dependencies
or runtime code is shipped. The generated starter reported dependency advisories
and its initial Windows Vinext export exited with a native assertion failure.
The replacement static build exits successfully. No dependency-security clearance
is claimed. Do not deploy the generated server or development tools.

For a hand-maintained v0, these three exported files are sufficient source;
the starter toolchain is unnecessary. Keep them in a small dedicated site
repository, or a tightly scoped docs directory if Mark prefers one repository.
No new public repository or hosting configuration has been created here.

Before each approved update: inspect changes in the named source repositories,
revise only affected orientation/link statements, commit the exact site source,
build or copy the static files, and record a SHA-256 of the public HTML outside
the file itself. Never embed an impossible self-hash. Keep the preceding static
bundle. Source provenance lives in normal Git history, not a second ledger.

## Deployment and rollback

Choose host/account first; publish only after its gate. Enable HTTPS and verify
the final canonical URL with an unauthenticated GET. For a custom domain, use
the host's documented DNS/ownership verification; do not assume TLS is ready
when DNS changes. Record actual status, content type, redirects, headers and
served HTML hash. A green source build is not proof of deployed bytes.

The local preview returns a strong SHA-256 ETag, Last-Modified, no-cache and a
restrictive CSP. These are local observations, not promised GitHub Pages headers.
Production headers are host-controlled and must be inspected. Prefer revalidation
for the root where configurable; do not introduce a Worker just to reproduce
local headers. Browser caching and intermediary/extractor caches can still make
old content visible. Preserve the date/source basis and avoid live-status claims.

Rollback on GitHub: restore the previous site commit with a normal revert and
redeploy, then compare served bytes. On Cloudflare: select a prior successful
Production deployment and verify its served bytes. Host moves need DNS changes
and fresh TLS checks; a retained domain reduces address lock-in but does not
eliminate caching or migration delay. No mutating retries after an ambiguous
deployment until the deployment state is inspected.

## What was checked, and what was not

Static build succeeded. Local HTTP checks: GET/HEAD 200, ETag conditional GET 304,
unknown path 404, POST 405. Root has no scripts/forms/external assets. All reading
links are ordinary anchors; headings, English language, skip link, keyboard-focus
outline, responsive single-column breakpoint and system fonts are present.
These are structural checks, not a claim of WCAG conformance, screen-reader
usability or successful cold-reader orientation. No browser interaction/visual
test or independent receiver experiment was run in this pass.

Next: FW integrates the provisional copy, then a genuinely fresh receiver tries
the entry and reports material misreadings. CC's 6/7 and 7/7 readings are explicitly
project-exposed. Useful baseline evidence, not a cold-receiver success. No new
test campaign, paid model call or domain is needed to inspect this prototype.

## Local files

- app/page.tsx: provisional page content.
- app/globals.css: presentation.
- scripts/build.mjs: static render and portable standalone preview.
- scripts/serve.mjs: loopback-only GET/HEAD preview, not a Production server.
- out/: three-file deployable artifact; build-generated.
- downloads/Campfire-preview.html: standalone offline preview for Mark.

No managed Site was registered. The Sites build/validation discipline is used
with the explicitly selected GitHub Pages hosting route for this preview.
No domain or paid hosting is authorized. GitHub Pages state and served bytes,
not this source note, establish whether the preview was actually deployed.
