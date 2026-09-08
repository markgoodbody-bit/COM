# Public discovery policy — 8 September 2026

Direction: [FW 5584293683](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5584293683).
This supersedes the prior preview noindex/nofollow requirement only for the
already-public homepage and Explore HTML readings. It is an indexing-policy
change, not a reuse grant, content validation or provider-access workaround.

The generator removes the robots exclusion from 18 HTML pages. Apart from the
regenerated resource map, every other output is byte-identical to the welcome
build. HTML bodies and all reading/example inputs are unchanged. A regression
in test_build parses all 18 HTML heads for robots directives. Four modules pass
50 tests; 60 outputs total 171,390 bytes, tree SHA-256
`a2d1987a208bd7b7e3885438c8215a73f92daccaee2fb62b401aae8d386c97a6`.

The maintained site separately removes its homepage exclusion, keeps error-page
and downloadable-preview noindex, updates the robots comment, and lists the
19 existing human-readable public routes in the sitemap. No fabricated lastmod,
technical/control inventory or new output path. Publish through the maintained
build; do not deploy this main-based branch. Check public HTTPS bytes, status,
final URLs, X-Robots-Tag and parsed meta directives separately from local tests.

This removes authored indexing exclusions. It does not establish search inclusion,
crawler visits, universal provider access or reader benefit. The domain recovery
is consumed and must not be repeated. No DNS, TLS, account, licence or timer change.
