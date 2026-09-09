# Observed local rendering, 9 September 2026

## Original PR129 observation

The original exact candidate `cf1e4e985563c011c7c838af835b35a138d7b37d` built five files and passed ten targeted integrity/mutation checks. Browser instrument: Edge 152.0.4191.66 / Playwright 1.62.1, fresh headless contexts, DPR1, localhost only.

The initial measured table was:

| View | Root font | Client/scroll width | Image width × height |
|---|---:|---:|---:|
| 1440×1000 | 16px | 1440 / 1440 | 640 × 716.234375 |
| 390×844 | 16px | 390 / 390 | 358 × 400.640625 |
| 1440×1000 | 32px | 1440 / 1440 | 640 × 716.234375 |
| 390×844 | 32px | 390 / 390 | 326 × 364.828125 |

That 326px doubled-mobile result is now preserved as a **defect observation**, not a current passing state. It came from `main { padding: 0 1rem; }`: at a 32px root font the horizontal gutter doubled.

The same original run also found the doubled-mobile heading splitting `Geographe / r` even though scroll width passed. The narrow heading repair changed the mobile h1 to 1.75rem, after which the title wrapped between words.

## Later repaired geometry

Claude Code review `5606540501` independently identified the 358→326 artwork shrink and requested the same shelf-wide gutter repair as Powers. The source now uses:

```css
main { max-width: 60rem; padding: 0 16px; margin: auto; }
```

The later corrected four-work shelf fixture used this repaired Vermeer CSS with the same exact 915×1024 JPEG and recorded these Vermeer states in `proposals/works/evidence/render-measurements.json`:

| View | Root font | Client/scroll width | Image width × height |
|---|---:|---:|---:|
| desktop | 16px | 1440 / 1440 | 640 × 716.234375 |
| mobile | 16px | 390 / 390 | 358 × 400.640625 |
| desktop | 32px | 1440 / 1440 | 640 × 716.234375 |
| mobile | 32px | 390 / 390 | 358 × 400.640625 |

No horizontal overflow was measured in those four repaired states. This closes the specific root-font gutter regression.

The shelf fixture dynamically adds only its return navigation/shared shelf link around the imported page; it does not replace the Vermeer image or figure geometry. The current PR129 wording changes in the image disclosure do not alter the figure width.

## Source-resolution consequence

CC also established that the museum viewer publishes a reported 16557×18526 Deep Zoom representation while this page deliberately uses the acquired 915×1024 thumbnail. At the page's 640 CSS-pixel desktop width:

- DPR1 needs 640 physical samples: 915 source pixels are sufficient;
- DPR2 needs 1280: the 915px source supplies about 71% of that horizontal sampling requirement.

This is a sampling consequence, not a performed high-DPR perceptual test. No Deep Zoom tiles were assembled and no higher-resolution source file was fabricated.

## Limits

Root-font doubling is not native browser zoom, screen-reader testing, high-DPR or physical-device validation. The enlarged mobile page remains long. No universal first-viewport, colour-fidelity or museum-master claim is made. The page's source image and museum links remain unchanged; the museum record is the route for deeper inspection.

No public or normal-build wiring.
