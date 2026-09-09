# PSFH composition review, 9 September 2026

LOCAL CANDIDATE / PUBLICATION HOLD. This is a presentation correction, not an
earned result about usefulness, accessibility conformance or audience reception.

Source basis: `991c0dd7900c891a8db554ab3f289ec32cb001c4` on COM's maintained-source
branch. Public output remains `589514fff41d0a65315377093089838026bbd1ec`.
Direction: FW's COM #108 comments 5599679905 and 5599831198, relaying Mark's review.
Both prototype files were read: `5b908f84a7f55a39dc527959f7d1543a4b6f955e` (scrim)
and `6a28b42f6d52d3eca8b4c9a195f3d0c445872833` (no card). Their exact margins,
font sizes and breakpoints are not adopted as requirements.

## Before / after

- Middle-left title over a hard 74%-black panel becomes high-left white type with
  a diffuse shadow and no backing box. The people and fire remain visible in the
  inspected desktop renders; the complete painting is not cropped or altered.
- Credit above the painting becomes credit below it, right-aligned on desktop.
- At 60rem or less, the title occupies a separate solid row beneath the image;
  credit then follows in ordinary left-aligned presentation. This is deliberately
  wider than the previous 42rem cutoff to avoid squeezing the title into a shallow
  image. It is a layout choice, not a measured limit of every alternative.
- Image and caption remain inside the figure; the project H1 remains outside it.
  Source, rights, artist links and non-art prose are unchanged.

## Browser observations

In-app browser, local built output at `http://localhost:3000/`, 9 September 2026.
These observations are not a claim of direct inspection of the public origin.
The saved images are browser screenshots, not generated mockups or edited art.

| Requested viewport | Browser-reported viewport | Image box (x, y, w, h), CSS px | Title box | Credit box |
| --- | --- | --- | --- | --- |
| 1600 x 1100 | 1600 x 1100 | 168.27, 212.66, 1248.01, 777.40 | 216.26, 260.65, 559.74, 206.41 | 744.29, 1002.05, 671.99, 50.40 |
| 1024 x 900 | 1025 x 900 | 40.98, 212.66, 927.13, 577.51 | 71.70, 243.38, 392.36, 151.99 | 296.12, 802.16, 671.99, 50.40 |
| 375 x 900 | 375 x 900 | 15.99, 214.67, 328.01, 204.32 | 15.99, 418.99, 328.01, 190.61 | 15.99, 621.59, 328.01, 72.80 |

Document scroll widths were 1585, 1009 and 360 respectively: no observed horizontal
overflow. Both desktop reads selected the 1440px viewing copy; the phone selected
720px. Image completion was checked after responsive source switching. H1 was
outside the figure in all three reads. Capture dimensions can differ from CSS
viewport dimensions because of the browser's capture scaling.

- [Desktop screenshot](desktop.png), 1600px requested viewport.
- [Phone screenshot](mobile.png), 375px requested viewport.
- The 1024px render was inspected but not saved as a separate screenshot.

The first attempted desktop artifact captured a transient blank image during
responsive source switching. It was replaced with the completed-image capture;
the transient image is not offered as final visual evidence. Capture failures
also occurred. Successful captures and DOM measurements do not establish network
paint timing or absence of every loading defect.

## Contrast: what was actually measured

The Python check takes browser-observed text-line rectangles at the two desktop
sizes, normalizes them to the image, rounds source-pixel bounds outwards, and
computes minimum white-text contrast against every source pixel in those boxes.
The shadow is ignored rather than credited with an unmeasured contribution.

- 720px viewing copy: minimum 7.765:1 across the measured regions.
- 1440px viewing copy: minimum 4.997:1 across the measured regions.
- Separate white-on-#141b20 title row: 17.39:1.

These are source-pixel calculations under fixed line boxes, not a complete
rendered-pixel or responsive accessibility test. Font substitution, text-only
enlargement, other widths, resampling and actual glyph edges are not established
by this check. Later text/font/placement changes require fresh measurements; the
fixed boxes alone cannot detect a geometry regression.

Adverse result retained: the same boxes on the full-resolution original include
fine bright details, with minima around 1.53-1.79:1 for the wide text lines. The
no-card result must not be generalized to that fallback image. The original is
still the existing non-srcset fallback, unchanged. The no-subgrid CSS fallback
stacks image, credit and title, which avoids an overlay, but older-engine behavior
has not been tested. Review should not equate the two checked modern renders with
universal robustness or WCAG conformance.

## Build and preservation checks

`npm run build`, 11 Node tests and 20 Python tests passed. Exact local HTTP delivery
matched all 115 generated files. Comparing output with public 589514f found 112
unchanged files and only `index.html`, `style.css`, `manifest.json` changed. No output
path was added or removed. Art bytes, machine orientation, seed, source readings,
existing destinations and non-art paragraphs were preserved.

Generated artifacts:

- `out/index.html`, 14,583 bytes, SHA-256
  `ecf52782cb5b0029bed13248d3fcb043510e34e7ace064ca087913ad33fb17cc`.
- `downloads/Campfire-preview.html`, 103,064 bytes, SHA-256
  `4ac64588a7c1df3d9a158bdf0ea0901b7a941103d8e1a6d94d155fb31d74e892`.
- `out/manifest.json`, 7,084 bytes, SHA-256
  `c6ad94f2e40f293c155028b1e908f3e80fb368187308f6d34a655e2e870b72b2`.

The standalone HTML embeds the 720px viewing copy; it is a root-page presentation
preview, not an offline copy of every linked destination. It retains the base
0.8.3 edition text because no new edition is published. Its review filename and
this record distinguish it from live 0.8.3.

## Return needed

Mark/FW: judge title placement, lack of a card, visible human subjects and credit
placement. CC: review this exact narrow correction and its contrast limitations,
not the old panel or the whole site afresh. Source checks do not substitute for
that visual judgement. No gh-pages push, endpoint, provider spend, supervisor
change or TRACE/ME change belongs to this correction.
