# Campfire door: bounded prototype plan

7 September 2026. Local prototype only; no public deployment or purchase.
Product coordination: [COM #108](https://github.com/markgoodbody-bit/COM/issues/108).

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

No Site was registered or deployed. The local-preview scope was retained under
the Sites skills' local-only exception.
