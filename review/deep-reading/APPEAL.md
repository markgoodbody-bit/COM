# Appeal reading-order follow-up

Stacked on PR455 at7caa53b6. Integrate only after that parent, then retarget
to the maintained-source branch. Publication remains Framework's lane.

Before: entry/case pages open with uppercase status and provenance, and facts
are rendered as serialized JSON.

After: an illustrative-example label, plain situation facts and unknowns;
entry links directly to the shared case. Existing optional routes remain.
Every original section is retained verbatim under Source details and limits;
Markdown and JSON links remain directly available. Source files are unchanged.

The transformation accepts only the exact controlled section sequence and
fact shape. It fails on an unrecognised template rather than losing content.
No new facts, theory, images, rights or source-record changes.

Build passes. Five deep-reading tests pass; local link scan has39 HTML pages,
703 references,90 fragments and zero problems. Narrow case preview at390px
visually inspected, no horizontal overflow. No screen-reader or reader-benefit
claim. The other three viewpoint pages remain a subsequent editorial task.
