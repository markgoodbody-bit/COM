# Browser-tab icon: source candidate

Requested by Mark from a browser-tab screenshot, then followed by “COMSYNC and proceed”. Base maintained source782c3f8d9be07feb788449e1fadd979799213f83; comparison public965687ee60552e11e25e5c9f797edc7f8b947dcd.

Before: generic browser globe. After publication: the root page explicitly offers a small amber flame on a dark rounded background, with SVG and16/32/48-pixel ICO entries. The root-level ICO is also available for browsers' conventional icon discovery; no universal deep-page browser behaviour is claimed.

Geometry is the existing installed Lucide Flame1.31.0 icon, not a new commissioned artwork or a claim of unique branding. The icon-specific ISC notice is retained in `favicon-LICENSE.txt`; no licence for the site, TRACE, ME or museum images changes. Preparation uses existing Sharp0.34.5/libvips8.17.3/librsvg2.61.2, with no package/lockfile change. Normal builds copy the checked-in files, so rendering libraries are not added to the reader path or build prerequisites. `scripts/prepare-favicon.mjs` records the one-time preparation procedure.

## Exact scope

- Root HTML gains two icon links inside its head:133 bytes. Its visible body is byte-identical to public965687ee.
- Three added outputs: `favicon.svg`410 bytes, `favicon.ico`2322 bytes, `favicon-LICENSE.txt`953 bytes.
- All other114 existing output files are byte-identical to965687ee. Total118 outputs, one changed/three added/no removed.
- No edition bump, book/canon edit, page redesign, Powers bundle, gallery, social card, manifest redesign, service worker, account or network dependency.
- The offline single-file HTML remains byte-identical and does not acquire a remote icon dependency.
- Preview server adds the ICO MIME type. The existing historical-preservation test narrowly handles the three new asset paths; a separate test pins their bytes and checks the entire delta against exact published0.8.4.

SVG SHA-256: `b2b950c89165e9c483853e608312f341ceceadb5c05958fd0be4ed77e9b9bd70`.
ICO SHA-256: `2e7f27bab62301c5d5d27bf6802faf28753623a228c83abe4f66e5e80731a70e`.
Icon notice SHA-256: `2d0c0cfe9630fcbf019e48b11349d220970e86a38fe05f06854321ee237d56b9`.
New root15470 bytes SHA-256: `bbb69b1e1faa0fb61e888eddd68e31bf7eed28e5569f27b6916aeda8a4480b7d`.

## Verification and remaining gate

Build PASS;14 Node tests PASS, including118 exact local HTTP file deliveries, SVG/ICO MIME checks, embedded ICO size/header checks and exact predecessor preservation;22 Python tests PASS; standalone route check PASS.32-pixel raster preview visually inspected. No actual browser-tab icon/cache behaviour or universal browser support was observed; browser cache may retain a predecessor icon.

This is source-only pending the existing coordinated publication decision. Publish only the named icon delta if authorised; do not repeat the earlier0.8.4 publication or merge unrelated work. No claim that the public tab already displays this icon.
