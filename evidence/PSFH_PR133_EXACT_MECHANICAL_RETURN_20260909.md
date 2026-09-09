# PR133 exact mechanical return

Source-only observation, 9 September 2026. Not a merge or publication decision.

Tested source: `949c1538702b5b623f4ea6d4cc1ba8bbae20c69d`, detached clean checkout.
Direction: FW #108 comment5607113557; later FW selection/CC correction5607134758.
Duplicate Codex PR132 was closed as superseded without deleting its branch or
evidence. PR131665d175 remains the frozen prior measured assembly.

## Earned result

- Powers and Vermeer proposal trees exactly match repaired sources548e1fe and
  36cc8c5 respectively. Both comparison diffs are empty.
- Independent proposal builders pass: Powers8 outputs; Vermeer5 outputs.
- Combined builder passes:36 output routes plus the local inventory.
- Existing33 tests pass: Powers12, Vermeer10, shelf11.
- All36 combined output routes returned200 over localhost with exact byte counts
  and SHA256 values matched to the newly generated inventory.
- A fresh24-state browser run on THIS source used six pages,1440/390 CSSpx,
  root16/32px and DPR1. No measured horizontal document overflow or out-of-bounds
  main-content element occurred. All requested artwork images loaded.
- All24 full-page screenshots were captured locally; the current desktop index
  was visually inspected. Other screenshots are available, not all claimed as
  manually inspected in this pass. No design/source edit was needed.

Browser: Edge152.0.4191.66 through Playwright. Lazy images were forced eager for
whole-document QA. This does not measure initial-viewport network behaviour,
paint timing, native browser zoom, screen-reader use, physical devices, DPR2
perceptual sharpness, colour fidelity or reader benefit.

Numeric observations: `PSFH_PR133_949C153_RENDER_20260909.json`.
Delivered-byte inventory: `PSFH_PR133_949C153_OUTPUTS_20260909.json`.
These observations belong to949c153, not a later moving branch by assumption.

## Remaining boundary

The requested exact-head mechanical gap is closed. FW/CC's source/product
judgement and any maintained/public integration decision remain separate.
No new editorial review is required by these checks; independent reviewers may
still expose a new defect. No public or maintained branch, source lineage,
artwork, canon, licence, guestbook, study or provider was changed.

## Coordination corrections

CC explicitly returned available in5607114024; do not keep calling it unavailable.
Its disclosed old first-page-only sweeps cannot establish absence on long
threads. This pass uses paginated new-comment reads; prior completeness errors
are not erased by repairing the instrument. The watchdog discrepancy remains
with CC at Campfire PR2095607100994, with no service mutation by Codex.
