# PSFH title and Camp Fire candidate

Prepared from maintained source `e03759f85a99b5eb5601df4ad400171d525307ed`.
Prepared for publication under FW5592807329 as Preview 0.8.1. The eventual COM
return and gh-pages README carry the deployment identity and delivery limits.
The separate non-public teaching/index prototype is not included.

## Before and after

- Before: the main heading was the guiding question. After: **Please Start From Here**
  is the primary title; **How can we make a better future?** remains directly beneath.
  The existing page/document title and human navigation already use PSFH and remain.
- Added Homer's actual *Camp Fire* after the existing opening choices, handoff and
  boundaries. No overlay, crop, recolouring, generated art or compulsory interaction.
- Added a small artist/source entry within the existing “The work and its neighbours”
  section, reached from the visible artist credit. No additional library/page tree.
- The unmodified museum JPEG is served locally and lazy-loaded. No museum hotlink or
  tracking request is required to read this page. It costs 2,350,423 image bytes if loaded.
- Optional source record: `/art/camp-fire.json`. The existing seed/orientation/Explore
  machine readings remain byte-identical except the orientation's site edition label
  and that label's HTML source view. The site manifest gains a small source pointer.

## Provenance

[The Met object record](https://www.metmuseum.org/art/collection/search/11112)
identifies *Camp Fire*, Winslow Homer, 1880, oil on canvas, object 27.181, and marks
the work Public Domain. The exact original
[museum JPEG](https://images.metmuseum.org/CRDImages/ad/original/DT2829.jpg)
was acquired unchanged on 8 September 2026: 3801 × 2368 pixels,
SHA-256 `7b02049468877e8e69b2faf183e7842ecb6577b08edc2a3f4a594d1bbeb577e1`.
The [Met Open Access policy](https://www.metmuseum.org/policies/image-resources)
supplies the CC0 basis. It does not change rights in other site material.

The short biography is paraphrased from H. Barbara Weinberg's
[Winslow Homer (1836–1910)](https://www.metmuseum.org/essays/winslow-homer-1836-1910),
published by The Met in October 2004. Work-specific context comes from its object
record. The original museum credit remains visible. These are source references,
not endorsement of PSFH by Homer or the museum.

The image/provenance module supplies the caption and optional machine source record
from one object. Ordinary builds are offline and reject a mismatched image hash.
The existing preview server gained JPEG MIME support; no writes or external access
were added to that server. `downloads/Campfire-preview.html` embeds the JPEG and CSS
for an offline review copy, rather than requiring a new service to view it.

## Checks and limits

- Build succeeds. Existing resource and exact-HTTP-output checks pass, including the
  two added art files. First-contact/navigation checks retain the old assertions and
  add title, credit, alt text, image identity, optional placement and source-link checks.
- Existing generated resources, source-view payloads, Explore readings and machine
  seed are preserved, apart from the orientation edition label. The four source-view
  wrappers carry Preview 0.8.1. No TRACE/ME, DNS, receiver, licence or production task edit.
- Browser readback in the current dark-themed 1077 × 818 viewport: one PSFH h1,
  53.86px title versus 20px guiding question; first choice begins at y=438.39; no
  horizontal overflow. Image loaded at its original dimensions and displayed without
  cropping. Clicking the artist credit reached the correct biography/source section.
- This is one observed desktop viewport, not mobile, enlarged-text, keyboard-complete
  accessibility, reader-benefit or cross-browser verification. No artwork is used as
  evidence that PSFH helps people.

Final release-preparation checks: 10 Node and 17 Python tests passed, including
exact local HTTP responses for all 113 generated files. The existing history
renderer reproduced the previous input exactly before rendering D012. Against
published 0cff0265, 101 generated files remain byte-identical, ten change (root,
CSS, edition-labelled orientation and four source-view wrappers, manifest and two
history files), and two art files are added. No generated path is removed.

The final 0.8.1 build was also inspected at 320 × 800 in the native dark-themed
browser. No horizontal overflow: document width 305 CSS pixels. The image loaded,
retained its proportions and displayed at about 273 × 170 CSS pixels; its title,
creator and public-domain credit remained visible and linked. The first starting
point begins at y=543.88, about 72 pixels later than the previous published opening
because the work's title now precedes the guiding question. This is a cost of the
requested hierarchy, not a claim that first access became faster. The temporary
viewport override was reset. Enlarged text, light-theme browser behaviour and full
keyboard/accessibility checks remain unestablished.

After the explicit live-update direction, the temporary candidate marker was removed,
the site edition became 0.8.1, and D012 was appended to the existing reader history
without rewriting earlier entries. Working-preview and non-validation status remain.
These preparation changes do not establish that the live website has changed.

The small `.gitattributes` repair preserves pinned discussion/history LF endings,
verbatim CSS output and binary art across Windows checkouts, without rewriting
earlier committed source text or weakening integrity checks.
