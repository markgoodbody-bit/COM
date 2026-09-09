# Observed local rendering, 9 September 2026

Earned result: five exact output files built and ten targeted integrity/mutation checks passed. Browser instrument: installed Edge152.0.4191.66 / Playwright1.62.1; fresh headless contexts, deviceScaleFactor1, only localhost8833 allowed. No live-site fetch, user profile or public mutation.

| View | Root font | Client/scroll width | Image width × height |
|---|---:|---:|---:|
| 1440×1000 | 16px | 1440 / 1440 | 640 × 716.234375 |
| 390×844 | 16px | 390 / 390 | 358 × 400.640625 |
| 1440×1000 | 32px | 1440 / 1440 | 640 × 716.234375 |
| 390×844 | 32px | 390 / 390 | 326 × 364.828125 |

Actual defect preserved: initial doubled-mobile heading split Geographer into Geographe / r even though scrollWidth passed. Small repair: at the existing narrow breakpoint, h1 now uses1.75rem (28px ordinary /56px doubled). Rechecked all four states. Afterward the doubled-mobile title wraps between The and Geographer, not inside Geographer. This is a wording-neutral presentation correction, not new content.

The credit follows the full image in all four measured states. Local image and both record links returned200. The disclosure opens with a pointer; the later check also confirmed Enter opens it and the first Tab reaches the skip link. No horizontal overflow was observed with the disclosure open in the initial pass. Source image bytes and routes were unchanged by the heading-only repair.

Before/after full-page screenshots and raw measurements stay local at `C:/Users/markg/Downloads/PSFH-Vermeer-render-20260909/`. All four initial views and repaired doubled-mobile view were visually inspected. Other repaired views were measured; they were captured but not separately re-inspected visually. Screenshots are not public assets.

Limits: root-font doubling is not native browser zoom, screen-reader testing, high-DPR or physical-mobile validation. The enlarged mobile page is long (3254px with the disclosure closed), not cost-free to navigate. Ordinary desktop's complete painting reaches near the bottom of the initial1000px viewport; its credit requires scrolling. No universal first-viewport or colour-fidelity claim. Museum destinations were not activated by browser QA; the official object record was read separately. Tests preserve selected identities and boundaries, not all possible misattribution or CSS regressions.

No public or normal-build wiring. Independent editorial/source review remains open.
