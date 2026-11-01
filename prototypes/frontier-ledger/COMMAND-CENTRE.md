# One consolidated command-centre milestone

Status: IMPLEMENTED / INTERNAL QA PENDING. Do not ask Mark to download another
small patch. Base943 6d459881714b457c7d4ca490bd999b8286d5f72e; own-state UI
and projection only. Engine, AI, commands, save format and HTTP security unchanged.

Plan: NOW actual own economics, consequential choices, mission/support feedback
and timed orders in one usable centre; NEXT meaningful reconnaissance contract
and campaign decisions informed by Codex's finite run; LATER faction development
and strategic depth after significant human feedback. No automatic release or
obligatory human checkpoint per commit.

## What the player can now reason about

- Top bar shows treasury and current daily mine income. Own-world list is selectable
  and shows daily income, garrison and queued build count. Selected worlds show
  actual production and facilities. Build buttons state actual cost, duration and
  effect (+3 troops, +1 mine income/day, or patrol ship). Affordability remains checked.
- Public/known worlds show only THIS faction's actual support score. Unknown worlds
  still omit support and ownership. A neutral world joins on a successful diplomacy
  mission reaching65 support; success adds up to25 capped100. Enemy worlds do not
  join this way. This is a deliberate limited own-information disclosure, not enemy
  support, hidden strength or a fabricated progress estimate.
- Own completed mission history joins results to own starts, retains40 and displays
  last20, optionally filtered by selected agent. Unknown old agent identity is
  labelled unknown, never guessed from an enemy event. Current missions and travel/
  build countdowns remain independently visible and selectable.
- Mentor availability now uses the actual own-agent mentor flag rather than a
  revealed-power guess. No awakening rules changed. Recon's current limitations
  remain explicit, and mission success is distinguished from ownership.

## Evidence and remaining gate

Build Node24.22.1 Linux:27 focused GUI/bridge/order/integration/centre tests PASS.
Actual HTTP campaign: board/travel/disembark, diplomacy success with partial support
and still-neutral ownership, further attempts leading to acquisition, changed
income, save/new/load and exact own result history. See test/command-centre.test.js
for reproducible seed42 commands and stdout diagnostic for actual day/attempts.
Additional checks: enemy support/missions/queues excluded, missing-start identity
unknown, actual mine completion/income vs shown build label, and mentor parity.
Earlier action-availability fixture still6808 offered/735 refused matching engine.
No core-engine suite rerun; engine unchanged. Source-only local execution is not
human enjoyment or a sustained campaign-quality claim.

CC is to receive one exact pinned candidate for headless browser mouse/keyboard,
layout, screenshot and save/load review; POSTED is not START or PASS. Build browser
NOT_RUN here, installed executable absent at prior check. Codex has a distinct
seed7 30–60-day real-engine probe on943; same unchanged engine makes that evidence
applicable but its actual result must be acquired. Neither gate may be silently
waived or attributed to Mark. No human-facing download invitation until meaningful
internal disposition, or an explicit blocker return.

Remaining mechanics: recon is normally redundant on arrival, production runs
concurrently, captured-world production and commander balance retain prior limits.
Current income can change with ownership/facilities. Mission result history does
not fabricate historical support deltas that old events never stored. Full saves
still contain hidden simulation state; the ordinary projection does not.
