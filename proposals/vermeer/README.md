# Vermeer: source-only work-page candidate

Before: exact Städel record-linked image and acquisition receipt were local, but no presentation existed.
After: one isolated static portrait page, source record and byte-preserving build. No current page, homepage link, normal build, edition, book, machine route or hosting identity is changed.

Based on maintained source `e30debac2a8c32c37d2abfaa32e988c11fe98e79`.
Direction: COM #108 comment5606192847, `FW-ART-ROLLING-SET-20260909-001`.

The museum's exact `thumb-xl` file is the delivery object, not a claimed museum master. Its915×1024/147792-byte source is retained without additional compression. The whole frame appears without text over it. Credit sits below. The museum account is a brief attributed paraphrase. No PSFH interpretation has been added.

`acquisition.json` is the unchanged earlier receipt. Its NOT BUILT label describes that event, not this candidate's current presentation state. `artwork.json` records the later state without rewriting custody history.

Run `python proposals/vermeer/build.py`, then `python -m unittest discover -s proposals/vermeer -p 'test_*.py'` with the already available Pillow package. Output is only `outputs/vermeer-work-page/`; normal PSFH output is untouched. No package or lockfile change.

Review gates: provenance truth; adequacy of the modest native source; portrait presentation and text enlargement; separation of museum account from project interpretation. Browser checks, if performed, are separate evidence, not established by the CSS or unit tests. Colour fidelity, physical-device viewing and the museum's highest-resolution status remain unestablished.

Publication and root/works-index wiring are withheld. This proposal does not amend HUMAN_ART.md's stale acquisition summary or add accepted-art records to the normal build; the integration review must reconcile those descriptions explicitly.
