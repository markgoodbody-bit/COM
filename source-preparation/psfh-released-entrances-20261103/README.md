# PSFH released-edition entrance repair

SOURCE PREPARATION ONLY — NOT DEPLOYED.

Campfire request: https://github.com/markgoodbody-bit/COM/issues/877#issuecomment-6615973228
Build START: https://github.com/markgoodbody-bit/COM/issues/877#issuecomment-6616030797

The live root retrieved on 3 November 2026 and COM gh-pages at d7473141ba89ab74ad51a875634034c96dffc4e9 still call ME0.8/TRACE0.4 current. No matching edition repair was found among the open PSFH PRs examined (820/824/829/833 and search results). The maintained-source branch is separately at 6fb14e0954ef9b760e3daeb6dfa8df5a4e7f4d00 and differs from the published source. This patch deliberately names the published base; it must not be blindly applied to the older maintained source.

## Exact deliverable

APPLY.patch changes five entrance files at the gh-pages base: index.html, llms.txt, packet.md, explore/start.json and manifest.json. Patch SHA-256: d1b4928d74ba7932235021d908a94bc0fb5181b6b294451f735a9d0640ef57cc.

Human book routes point to the complete released v1.0 Markdown and PDF. TRACE routes point to released v0.5 specification. AI text and JSON entrances expose the same immutable sources. ME's release receipt explains why the preserved source still has older draft labels. Local old editions, story provenance and permission notices remain historical; no book bytes or general permissions change. No private bootstrap companion is published.

Exact current sources:
- https://github.com/markgoodbody-bit/mechanical-ethics/blob/e97a2aa97360c39d10857fdbf82d058ac77099aa/RELEASE_v1.0.0.md
- https://github.com/markgoodbody-bit/TRACE/blob/2312e5fa0535d25e8cafa0e7ee5d43564449d2a2/TRACE-v0.5.md

## Verification and publication boundary

Generated against the five retrieved original files. git apply --check passed; actual local application matched all five intended outputs exactly. Both changed JSON files parsed. Focused checks confirm current labels/routes and historical story attribution. Git emits five whitespace warnings for deliberate Markdown two-space line breaks. No browser rendering, hosted smoke test or deployment was performed.

This is a bounded static-snapshot source repair, not a completed rebuild of the maintained app. Before publication, the existing publisher must reconcile this delta into the current app/page.tsx and public sources, regenerate source views/inventories and derived hash records through its established build, and verify the built/live routes. Historical provenance fields were not forged into freshness claims. Existing publication custody and approval remain separate. Do not merge this patch record expecting it to update the site.
