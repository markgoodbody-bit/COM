# Campfire Door public preview

Publishing branch only. COM `main` remains the coordination repository.

Preview 0.6, prepared 7 September 2026 from local source commit
`7f20b46d64cbacb90bd1fcbf19af89e071865a64`.
Authority and discussion: [COM #108](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5576230968).
The previous 0.3/0.4 comparison objects remain in [PR #110](https://github.com/markgoodbody-bit/COM/pull/110).

GitHub Pages serves this branch's root. No Jekyll processing, application server,
JavaScript, credentials, forms or analytics are part of the page. The preview
does not promote TRACE/ME status or prove the material helps a reader.

Static machine-reading additions 0.1, prepared 8 September 2026 under
[Framework's bounded direction](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5577437335).
Local maintained source commit: `379c11456b3ffd78c734d236ea772e6833358f6f`.
The human preview keeps its text and styling, with one discovery-link paragraph
and an HTML `describedby` link added. Its existing `noindex,nofollow` remains;
the sitemap advertises routes but does not override indexing preferences.
The five machine files are working orientations, not new project canon or an
efficacy result. The manifest is project-specific, not a Web App Manifest.

Intended `index.html`: 4,841 bytes, SHA-256
`f0efbab5789c7d46a337c74f103bf061cc104255b118fb2a6c1acdc569d2b6f4`.
CSS SHA-256: `4487822f7ac1369ae16cac356e3c5301b0b9e4ed89b5e5fc1a3746f414bdef98`.
Served bytes must be checked separately after publishing.

## Update and rollback

The existing local source project is `campfire-door-preview`; use its normal
build, then copy only `index.html`, `style.css`, `404.html`, `llms.txt`,
`seed.txt`, `manifest.json`, `robots.txt`, and `sitemap.xml` from `out/`
into this checkout. Review and
commit the diff on this branch. A push updates the public preview, so it needs
the applicable publication authority. Do not copy the source project's entire
directory, its dependencies, or the COM tree into the reader path.

Keep the root `CNAME` file containing `pleasestartfromhere.com` when updating
content. This custom-domain connection was configured on 8 September 2026;
it does not change the preview's content or evidential status. The old
`markgoodbody-bit.github.io/COM/` address redirects to the custom domain, so
it is not an independent fallback while that connection is enabled.

DNS uses an apex ALIAS and an explicit `www` CNAME, both targeting
`markgoodbody-bit.github.io`, with TTL 600. Do not introduce wildcard routing
or change unrelated email records. Account-level GitHub domain verification
is still pending; custom-domain configuration alone does not establish it.
Check HTTPS certificate readiness and enforcement separately before reporting
the new address live.

Keep exact build hashes in the update receipt. After GitHub reports a successful
build, verify the canonical HTTPS root, CSS and five machine files with
unauthenticated GETs. Check UTF-8, JSON/XML parsing, route existence and links;
the source build keeps the seed under 1 KiB. A
successful Git push or cached page alone is not deployment verification.

For a content rollback, revert the relevant publishing commit normally, push,
and verify the resulting public bytes. This first publication has no earlier
live version: withdrawing it means disabling Pages, not deleting COM or its
history. Before disabling Pages or removing its custom domain, remove or
repoint the GitHub-directed DNS records to avoid leaving an unclaimed route.
The pre-connection publishing head was
`0f6a0ac5bca782de58be5ae47b8c49daaee84ab8`; a domain rollback is a separate
DNS/Pages operation, not just a content revert.
Disabling Pages also requires applicable authority. No automatic
rollback, public update or deletion is authorized by this README.
