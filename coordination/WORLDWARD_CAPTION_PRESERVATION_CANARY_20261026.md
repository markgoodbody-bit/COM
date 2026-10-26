# Worldward | Captions can be well-formed and still lose meaning

**26 October 2026 — noncanonical, source-only accessibility workflow canary**

## The outside-world problem

A volunteer editing captions for a local video may run a tidy-up or format conversion and obtain a syntactically plausible `.vtt` file while silently losing *who spoke* and an important sound. Structural timestamp tests cannot establish that the resulting captions preserve the audio information. This matters especially to viewers who rely on captions rather than audio.

**Stronger owners:** W3C Web Accessibility Initiative and the WebVTT specification for published normative and educational guidance; Deaf and hard-of-hearing caption users and the organisation publishing the video for judging whether a caption edit is genuinely useful. This note is neither a conformance tool nor their endorsement.

**Primary sources inspected 26 October 2026:**

- W3C, [WebVTT: The Web Video Text Tracks Format](https://www.w3.org/TR/webvtt1/) — cues must have nondecreasing start times and end after start; **overlapping cues are permitted**. A timestamp-overlap warning is not, by itself, proof of an invalid caption file.
- W3C WAI, [Understanding WCAG 2.2 SC 1.2.2](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html) — captions of prerecorded synchronized media convey speech *and* meaningful non-speech audio; speaker identity may matter.
- W3C WAI, [Captions/Subtitles](https://www.w3.org/WAI/media/av/captions/) — creating accurate captions requires human judgment and review.
- Existing tools already perform structural WebVTT checks, e.g. [Subtitle Preflight](https://subtitlepreflight.com/webvtt-validator/) and [TimedSubs](https://timedsubs.com/en/tools/subtitle-checker). **Do not create another validator just to count more tests.** Their descriptions cannot be used to infer they detect every semantic loss.

## Minimal regression fixture A — *before* editing

Synthetic audio scene; not derived from an actual video. Cues 1 and 2 intentionally overlap, which WebVTT allows.

```vtt
WEBVTT

00:00:00.000 --> 00:00:02.400
[door opens]
VOICE A: The corridor is clear.

00:00:01.200 --> 00:00:03.000
VOICE B: Stop, the stairs are blocked.
[alarm sounds]

00:00:03.100 --> 00:00:04.800
VOICE A: Use the side entrance.
```

## Minimal regression fixture B — *after* a harmful tidy-up

The timestamps remain valid and unchanged, and every spoken sentence is still there. But the door and alarm sounds and speaker labels have disappeared. **A structure-only PASS is not a semantic PASS.**

```vtt
WEBVTT

00:00:00.000 --> 00:00:02.400
The corridor is clear.

00:00:01.200 --> 00:00:03.000
Stop, the stairs are blocked.

00:00:03.100 --> 00:00:04.800
Use the side entrance.
```

## The useful human handoff — before publishing

1. Preserve the source caption file and the media. Review the edited version **alongside the actual audio** at affected cue times; don't infer meaning solely from timestamps.
2. Check separately: speaker attribution; meaningful sound effects; spoken wording; synchronization/placement; and whether overlaps are intentionally needed. Don't automatically remove hearing-access annotations as “noise”.
3. Record exactly what was reviewed and by whom. If the audio or a qualified reviewer is unavailable, say **CONTENT NOT VERIFIED**; do not publish an accessibility assurance based on the structural test.
4. The producer and affected viewers may reject this canary as too narrow. An existing trusted caption editor may offer better workflows. Do not use this as an accessibility certificate.

## Bounded verification and falsifiers

An independent local *subset parser* was exercised on the exact fixture strings before this note was committed: **8/8 synthetic checks PASS**. Both fixtures had three strictly parsed cues, equal timestamps and nondecreasing starts; the first two overlapped. A simple string comparison proved that the second lost both sound annotations and speaker markers while retaining the spoken sentences. Those tests **do not** prove complete WebVTT conformance, browser/player presentation, transcription accuracy, WCAG compliance or any benefit to an actual caption user.

**What would falsify usefulness:** Deaf reviewers find the example misleading or an unhelpful substitute for actual audio review; a trusted existing captioning workflow already catches this semantic regression more effectively; overlap handling behaves differently in the actual player; or the scene-specific annotations are not meaningful to its audience. The correct response is to revise or retire this note, not enlarge the tooling.

**Release and contact:** informational draft only. No media file, user data, real video, accessibility decision, external contact, publisher deployment or YAC action. There is no claim that volunteers used it. An actual producer and Deaf caption user would be the next legitimate reviewers.

**Source evidence clock:** external references inspected 26 October 2026; fixtures synthetic and author-designed; independent field effect NOT OBSERVED.
