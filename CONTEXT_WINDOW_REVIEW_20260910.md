# Context-window revision, 10 September 2026

Working presentation experiment, not a TRACE/ME release or reader-benefit result.

## Before / after

Before: whole Homer image, four expandable entrance choices and a long introduction beneath them.

After: the same complete artwork, a slightly larger title, one changing window, five arrival cues converging on Look / Work / Challenge, and the unchanged source-labelled composite story. Map and Leave are available before choosing anything. The full introduction is expandable rather than dominating the enhanced first encounter. The gift disclosure stays with the arrival question; an additional required acknowledgement screen was deliberately not added.

Direction: COM #108 comments 5616897757 and 5617040633. Existing source paragraphs/headings and old destinations are preserved against the fixed pre-foyer edition, with an explicit addition fixture. This is not new theory.

## Earned checks

- Static build succeeded. Seventeen selected Node checks and twelve Python first-contact checks pass. Checks include deliberate corruption/loss rejection; these are scoped regressions, not every historical repository test.
- Against public 7135b629b4180ad07a500e41647d203c07f80879: 147 output files remain byte-identical; seven existing outputs change and one local script is added. No images, Works accounts, TRACE/ME files, Explore readings, or seed bytes change.
- The new history entry has matching Markdown/HTML paragraphs. All history from D016 onward remains exact.
- Local browser: width 1077 desktop screenshot; width 1440 keyboard/DOM checks; width 390 art-first screenshot and navigation; width 320 orientation screenshot and target geometry. No horizontal overflow in the inspected states. The image starts at y=0 in the checked top views and remains uncropped.
- Continue focuses the arrival heading. Tab then reaches the first choice. Story, Work, Challenge and Leave show only the selected panel. Two successive Back clicks restore the actual previous panels and focus, including the initial unfragmented URL. The UI Back uses browser history; the browser toolbar Back was not separately exercised.
- Map reaches /explore/#reading-map directly. A story URL survives reload. The preserved #winslow-homer link opens its containing full introduction.

## Failures and limits

The first browser run exposed a real defect: pushState changed the address but not CSS :target. The script now explicitly toggles panel visibility; subsequent browser runs passed the affected paths. This failure is retained here rather than counted as an initial success.

Earlier shape tests correctly rejected the removed menu wrapper and the new script. Their current assertions now name the intended navigation and sole integrity-pinned local script. The old build-wrapper comparison remains pinned to its actual historical revision; it is not presented as a current no-JavaScript constraint.

The browser policy blocked opening the offline file. No alternate route was used to load it. The script-free file and native-link/CSS fallback have source checks, not an independent browser walkthrough. Some screenshot requests also failed; subsequent DOM checks are distinguished above from successful screenshots.

No direct public served-byte check is claimed: that client path was previously blocked. Publication can be verified through the exact GitHub Pages commit/build, separately from the localhost browser checks.

## Boundaries

The optional script performs no fetch, analytics, form submission, profile storage or account operation. Browser history can retain page positions. Leave explains how to stop; it does not pretend to close the browser. No confidence score, progress meter, persona inference or claim of accessibility conformance is added.

Cold-reader usefulness, the adequacy of route convergence, and whether this feels welcoming rather than procedural remain unresolved. FW/CC review is welcome without claiming their agreement is validation.

## Reproduction and rollback

Run npm run build, then node --test scripts/test-context-window.mjs scripts/test-works.mjs scripts/test-contextual-art.mjs scripts/test-artwork.mjs scripts/test-resources.mjs. Set PSFH_PUBLISHED_CHECKOUT to an existing COM checkout, then run python -m unittest discover -s scripts -p test_first_contact.py.

Revert this source revision and rebuild to restore the art-first layout. Publication uses the existing GitHub Pages branch; no new host, service restart, scheduler, licence, or draft PR130 adoption is involved. The publication receipt belongs in the existing COM #108 thread.
