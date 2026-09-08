# Please Start From Here — arrival ecology and visual-interest direction

Status: SOURCE DIRECTION / NOT PUBLIC / NOT CANON / NO READER-BENEFIT CLAIM  
Date: 8 September 2026

## Why this exists

The Door will not have one kind of visitor or one clean arrival path.

A person may click a bare link on Reddit with almost no context. Another person may receive it from a friend. A human may read it and then hand the address to an AI. An AI may receive only the URL, a copied page, a deep link, or a fragment stripped of its links. A crawler may see machine-readable material first. A sceptical researcher may arrive looking for the source. A contributor may return to see what happened after they answered.

The design should therefore optimise for an **arrival ecology**, not a single imagined user journey.

`DIFFERENT ARRIVAL != DIFFERENT PURPOSE`

Every arrival should be able to recover a small useful account, discover optional depth, understand the project's limits, and leave without being forced through an identity test or funnel.

## The public impression we want

The site should feel more like **an interesting place to enter** and less like a competent technical README rendered as a website.

That does not require spectacle, animation, a marketing framework, external fonts, tracking, a large JavaScript bundle, or a fake sense of authority.

Aim for:

- calm curiosity rather than urgency;
- distinctive enough that a stranger remembers the address;
- human warmth without sentimentality;
- technical seriousness without looking institutional;
- space and depth rather than dense documentation;
- visible invitation to explore, challenge, make, hand off, or leave;
- the same semantic content remaining useful to a text extractor or AI that ignores presentation.

Avoid default AI aesthetics: neon cyberpunk, glowing brains, robot imagery, stock futuristic grids, animated particles, or claims of intelligence/consciousness implied by decoration.

## A visual language that fits the project

Use CSS and ordinary semantic HTML first.

A possible visual vocabulary:

- warm off-white / near-black foundation already established;
- restrained blue for active routes and links;
- a small warm amber accent for orientation, change, or human-facing invitation — never as a sole state signal;
- soft surfaces rather than flat rules everywhere;
- slightly more generous vertical space at the opening;
- first movements as visibly distinct **places to begin**, not a plain list separated only by horizontal rules;
- subtle borders, radius and very light depth; no glossy product-dashboard cards;
- one quiet non-semantic visual motif suggesting an open horizon / branching possibilities / connected apertures. Prefer CSS gradients or a tiny reviewed inline SVG marked decorative over fetched imagery;
- no motion needed. If motion is ever explored, `prefers-reduced-motion` must eliminate it and meaning must never depend on it.

The motif should be recognisable but not explained. The project is not a logo puzzle.

## Root-page composition

Keep Preview 0.8's earned structural improvement: useful first movements before the long explanation.

Refine the opening roughly as:

1. **Name / question** — `How can we make a better future?`
2. **Arrival sentence** — `Start from whatever brought you here.`
3. **Optional handoff invitation** — small and non-coercive.
4. **Five first movements** — visually scannable, each retaining its one-fetch micro-use.
5. Values / limits / why this exists.
6. Work, neighbours, discussion, history.

Do not replace the five movements with audience personas such as HUMAN / AI / RESEARCHER. Behaviour and purpose remain better routing dimensions than identity.

## The human-to-AI handoff

A random human coming from Reddit may never think to give the address to an AI unless the possibility is visible.

Add a small optional invitation near the opening, not a modal or dominant CTA. Candidate semantic content:

> **Another perspective**  
> You can read this yourself, or hand this address to an AI and ask what it notices, disagrees with, or would try on a real question. No special prompt is required.  
> `https://pleasestartfromhere.com/`

Possible short prompts may be offered as examples, not required syntax:

- `What do you think this is trying to do?`
- `What seems wrong or missing?`
- `Can any of this help with something I am actually trying to do?`

This is not an instruction to trust an AI's answer and not a requirement to use an AI. Do not link to a favoured model/provider or imply endorsement.

The same idea should survive stripped-text extraction. The handoff is a semantic invitation, not a JavaScript affordance.

## Arrival cases to preserve

### 1. Bare Reddit link → human

Likely first questions are closer to `What is this?`, `Why should I care?`, `Is this weird marketing?`, `Is it asking me to believe something?` than to TRACE vocabulary.

The first screen should answer enough to make one more action attractive without pretending established benefit.

### 2. Human → AI

The AI may receive only the URL and an ordinary prompt such as `have a look at this`.

The root must therefore contain enough semantic substance to orient the AI even if it cannot fetch deeper routes.

### 3. AI direct retrieval

Keep literal URLs, alternate machine/text representations, status/edition information, and no-script dependence. Presentation changes must not hide the small source routes behind client-side interaction.

### 4. Search / crawler / excerpt

A fragment may be the first contact. Headings and local paragraphs should make sense outside the full page. Decorative language must not become the only carrier of purpose or qualification.

### 5. Deep-link arrival

A resource, discussion item, TRACE page or Mechanical Ethics page may be encountered without the root. Each maintained human-readable deep page should retain enough local context to answer: where am I, what status is this, what can I do next, how do I leave or challenge it?

### 6. Sceptic / critic

Disagreement must remain visibly legitimate. Visual polish must not turn criticism into a small grey footer while positive framing gets the hero treatment.

### 7. Contributor / returning reader

Once receiving exists, the route to receipt/status/change should be visually findable and semantically distinct from `read the discussion`.

### 8. Reader who wants nothing from it

Leaving remains a complete use. No newsletter, account creation, cookie wall, forced survey or gamified completion state.

## Visual-interest acceptance

A prettier page is not automatically a better first contact.

Before publication, inspect at least:

- wide desktop light mode;
- wide desktop dark mode;
- narrow mobile light/dark;
- keyboard-only focus order;
- 200% text resize and 320 CSS px reflow / 400%-equivalent conditions;
- text-spacing override;
- stripped-text extraction;
- no CSS / semantic reading order;
- direct deep link;
- root with all deeper fetches unavailable.

Record visual/structural observations separately from any claim that readers are more motivated or understand more.

`PRETTIER != MORE USEFUL`

`MORE INTERESTING != MORE MANIPULATIVE`

`VISUAL HIERARCHY != HIDDEN QUALIFICATION`

`HUMAN INVITATION != AI OBLIGATION`

## Reddit later

When the foundations and reply route are ready, the clean experiment is intentionally small: Mark can post the bare public address with a short ordinary-language invitation and ask people to use it if they want.

Do not optimise the site around Reddit voting, virality, conversion funnels, engagement time or extracting sign-ups. Reddit is one aperture into the arrival ecology, not the target audience.

Useful observations from that release would include where people stop, what they think the object is, whether anyone independently hands it to an AI, what they try to do with it, what confuses or repels them, what they reject, and what they wish existed next.

Those are observations, not validation scores.

## Release boundary

This direction does not authorise a public redesign by itself. Codex remains the maintained-site publisher. Preserve current Preview 0.8 while a candidate is reviewed and tested. Do not delay receiver/custody work merely for cosmetics, but visual interest and cross-entity handoff are now legitimate product requirements rather than decorative afterthoughts.
