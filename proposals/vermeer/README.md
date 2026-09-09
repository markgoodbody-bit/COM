# Vermeer: source-only work-page candidate

SOURCE ONLY / NOT PUBLISHED / NOT WIRED INTO MAINTAINED PSFH

Base maintained source: `e30debac2a8c32c37d2abfaa32e988c11fe98e79`.
Original candidate reviewed at `cf1e4e985563c011c7c838af835b35a138d7b37d`.
Claude Code narrow review: PR129 comment `5606540501` → `REPAIR_SMALL`, bytes exact and rights independently confirmed.

The acquired file remains the exact Städel record-linked `thumb-xl` JPEG: 915×1024, 147792 bytes, SHA-256 `2eb8819e4afe22c219d7fbd01766e41338c5fbe460d0d41c250f8c698fd39106`. It is retained unchanged and uncropped. `acquisition.json` remains the immutable earlier acquisition receipt.

## Review repair

CC established an important distinction that the original candidate did not carry strongly enough:

`THE_TIER_WE_TOOK != THE_SIZE_THE_WORK_COMES_IN`

The museum page's ordinary viewer exposes a Deep Zoom representation reported by CC at 16557×18526 pixels (~306.7 MP). That does **not** make the tile pyramid a single acquired source file, does not establish museum-master status, and does not authorise reconstructing an image from tiles. No tiles were assembled or downloaded for this repair.

The repaired `artwork.json` and page therefore say:
- the 915×1024 file is the tier acquired for this preview;
- the museum demonstrably publishes a much higher-resolution representation;
- master status remains UNKNOWN;
- a documented single-file higher-resolution route or museum-provided file would be a separate acquisition decision;
- at a 640 CSS-pixel layout width the thumbnail can undersample a DPR2 display and appear soft.

The page remains deliberately bounded to the acquired thumbnail rather than pretending the viewer pyramid is a file we possess.

## Presentation repair

CC also found the same text-enlargement defect seen on Powers: `main { padding: 0 1rem; }` made the 390px mobile image shrink from 358px to 326px when the root font doubled.

The repaired CSS keeps the max width in `rem` but changes only the page gutter to fixed `16px`.

The original PR129 rendering record preserves the pre-gutter measurement. The later four-work shelf fixture used this repaired Vermeer CSS and exact 915×1024 image and measured:
- mobile root16: 358 × 400.640625;
- mobile root32: 358 × 400.640625;
- desktop root16/root32: 640 × 716.234375;
- no horizontal overflow in those states.

That later measurement is evidence for the repaired geometry, while remaining subject to the recorded DPR1/root-font-doubling limitations.

## Editorial boundary

The full painting remains first, followed by museum credit and a short Städel-attributed paraphrase. `project_response` remains `null`: the work is not required to illustrate PSFH. The higher-resolution finding changes source honesty, not the work's meaning.

No crop, upscale, retouch, synthetic derivative, Deep Zoom reconstruction, public wiring, homepage change, edition change, book change or museum contact is part of this repair.

## Build

The existing isolated builder and ten mutation/integrity tests remain the same contract. They pin the exact thumbnail bytes, acquisition receipt, source category, master UNKNOWN, museum routes, no active content, no crop/wallpaper and `project_response: null`.

The repaired source files are intended to run with:

```text
python proposals/vermeer/build.py
python -m unittest discover -s proposals/vermeer -p 'test_*.py'
```

PR131's corrected four-work fixture already ran the same Vermeer validator against the repaired provisional copy before emitting the measured page. This PR remains a source/review object; merge/publication are separate decisions.

`EXACT_BYTES != BEST_AVAILABLE_BYTES`
`SOURCE_REPAIR != PUBLICATION`
