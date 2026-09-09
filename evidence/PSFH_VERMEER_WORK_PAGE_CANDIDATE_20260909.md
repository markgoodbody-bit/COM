# Vermeer work-page return

Status: SOURCE-ONLY CANDIDATE / REVIEW OPEN / NOT PUBLISHED  
Request: #108 comment5606192847, FW-ART-ROLLING-SET-20260909-001.

Exact candidate `cf1e4e985563c011c7c838af835b35a138d7b37d`, branch `codex/vermeer-work-page-20260909`, draft [PR129](https://github.com/markgoodbody-bit/COM/pull/129), based on maintained `e30debac2a8c32c37d2abfaa32e988c11fe98e79`.

Before: acquired image and custody receipt only. After:11 additions under `proposals/vermeer/` only, providing one portrait work page, metadata, preserved source/receipt, build and targeted checks. No existing site file, accepted-art list, normal build, homepage/shelf wiring, edition, machine files or book changed.

Source: Johannes Vermeer, The Geographer,1669, Städel Museum, Frankfurt am Main, inventory1149. Exact record-linked thumb-xl915×1024/RGB/147792bytes, SHA256 `2eb8819e4afe22c219d7fbd01766e41338c5fbe460d0d41c250f8c698fd39106`. Category AUTHORITATIVE_RECORD_LINKED_THUMB_XL; master UNKNOWN. No image transformation or derivative. The original acquisition receipt remains unchanged, including its historical NOT BUILT statement; artwork.json records the later presentation state.

The [official object record](https://sammlung.staedelmuseum.de/en/work/the-geographer) was read afresh: work identity, medium, credit and Picture Copyright Public Domain fields support the displayed metadata. Brief museum-account paraphrase is attributed; no project interpretation or claimed artist intention added. This does not establish rights for all museum text or museum-master identity.

Five exact static output files and10 targeted tests PASS. Actual local Edge152/Playwright desktop1440 and mobile390, root16/32px measurement found no horizontal overflow; image widths640/358/640/326px remain below915 native pixels at ordinary CSS scale. Credit follows image. Local image/records return200; keyboard skip and disclosure confirmed. Root doubling is not native zoom or physical-device validation.

An initial doubled-mobile heading split the word Geographer midword despite passing overflow measurements. Preserved before/after; small narrow-heading font repair remeasured in four states. Repaired enlarged-mobile screenshot inspected; title now wraps between words. Source-code evidence and limitations are in `proposals/vermeer/RENDER_CHECK.md`.

Local candidate: `C:/Users/markg/Downloads/PSFH-Vermeer-candidate-20260909/`. Screenshots/raw observations stay at `C:/Users/markg/Downloads/PSFH-Vermeer-render-20260909/`, not public image assets. Candidate build remains separate from production.

Next: independent source/editorial review after the already-open Powers review. Source-only works shelf remains unbuilt. The old HUMAN_ART.md Vermeer summary is stale and must be reconciled at integration, not silently treated as current. No publication authority inferred from this return.
