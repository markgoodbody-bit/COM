# Powers: measured local rendering, not editorial acceptance

Exact reviewed source: `fd4be44799c47bd4c0df6cf5c0bd470ca30f33d2` / PR127. Source remained clean and unchanged. Rebuilt only the isolated proposal, with its existing parent/copy checks passing. No public/site artifact or screenshot was published.

## Method and correction of the earlier tooling limit

Tool discovery located the supported `node_repl` runtime and its existing Playwright1.62.1 package. The initial ESM import failed with a missing-default-export interop error; the installed package's documented CommonJS entry loaded successfully through Node createRequire. No dependency was installed, modified or downloaded.

Used installed Windows Edge `152.0.4191.66`, headless, a fresh context for each state, deviceScaleFactor1. Only requests to the exact local127.0.0.1:8832 origin were allowed; all other requests were aborted. No credentials, existing browser profile, remote site or security-policy override was used. All four local page responses were HTTP200.

The doubled-text cases set the root font from16px to32px after loading. This is materially enlarged rem-based text, **not native browser zoom, all possible text-enlargement methods, a physical mobile device, or an accessibility certification**. The earlier browser-entry tool exposed no measurement controls; that limitation was real for that tool but did not exhaust the newly discovered local test runtime. No CSS/source changes were made to obtain a passing result.

## Measured facts

| State | Viewport CSS px | Client / scroll width | Image CSS px | Caption font |
| --- | --- | --- | --- | --- |
| Desktop | 1440 × 1000 | 1440 / 1440 | 1136 × 951.391 | 16px |
| Mobile | 390 × 844 | 390 / 390 | 358 × 299.813 | 16px |
| Desktop, doubled root text | 1440 × 1000 | 1440 / 1440 | 1376 × 1152.391 | 32px |
| Mobile, doubled root text | 390 × 844 | 390 / 390 | 326 × 273.016 | 32px |

Across all four states:

- document scrollWidth equals clientWidth; no horizontal overflow detected;
- measured text/link element rectangles stay within viewport width;
- caption begins at or after the image bottom, and the project-response section begins after the maker-account section;
- local screenshots visually show the entire uncropped textile frame, with no title/caption/image overlap;
- source links wrap at narrow widths and remain separated from the image and following sections.

The full work is present in the document; it is **not wholly visible in the initial desktop viewport**. That requires vertical scrolling, not a crop. Doubled mobile text produces a long6085px screenshot and substantial vertical scrolling. These are real presentation costs, not suppressed failures. Source-link wrapping is observed; this was not a touch-target, keyboard-navigation or destination-access test.

The browser reports density-adjusted `naturalWidth` for width-descriptor srcsets. Those DOM values must not replace the pinned720/1440 source-pixel identities. Actual selected paths were the1440 copy on desktop and720 on mobile, including doubled-text cases.

## Local evidence and open judgement

Raw measurements and screenshots remain local at `C:/Users/markg/Downloads/PSFH-Powers-render-20260909/`:
`measurements.json`, `desktop.png`, `mobile.png`, `desktop-text200.png`, `mobile-text200.png`.

All four screenshots were inspected by Codex. Browser and temporary preview server were closed afterward. Public COM carries measured facts, not the screenshot binaries; CC can inspect the named local files through its existing local access.

No measured defect requiring source repair was found in these states. This supplies evidence for CC's existing review; it does **not** close CC's independent provenance, interpretation, tokenism or does-the-work-stand judgement. No Powers merge or public wiring occurred.
