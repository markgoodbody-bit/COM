/* Static React rendering, not a Next.js runtime: native links must work without JavaScript. */
/* eslint-disable next/no-html-link-for-pages */
import { SITE_EDITION } from '../scripts/site-edition.mjs';
import { CAMP_FIRE } from '../scripts/camp-fire.mjs';
import { artworkSrcSet, HOMER_SIZES } from '../scripts/artwork.mjs';
const trace = "https://github.com/markgoodbody-bit/TRACE";
const me = "https://github.com/markgoodbody-bit/mechanical-ethics";
const heroFallback = CAMP_FIRE.responsive.variants.find(copy => copy.width === 1440);
if (!heroFallback) throw new Error('Missing pinned 1440px artwork fallback');
export default function Home() {
  return <>
    <a className="skip" href="#project">Skip the painting</a>
    <main id="start">
      <section className="intro">
        <div className="opening-composition">
        <div className="art-hero" id="top">
        <figure className="camp-fire" aria-labelledby="camp-fire-credit">
            <img src={heroFallback.local_image} srcSet={artworkSrcSet(CAMP_FIRE)} sizes={HOMER_SIZES} alt={CAMP_FIRE.alt} width={CAMP_FIRE.width} height={CAMP_FIRE.height} loading="eager" decoding="async" />
          <figcaption id="camp-fire-credit">
            <span><a href={CAMP_FIRE.object_url}><cite>{CAMP_FIRE.title}</cite></a>, {CAMP_FIRE.date}, by <a href="#winslow-homer">{CAMP_FIRE.artist}</a>.</span>
            <span>{CAMP_FIRE.museum}. <a href={CAMP_FIRE.rights_url}>Public domain, Open Access</a>.</span>
          </figcaption>
        </figure>
            <div className="hero-heading">
              <h1>Please Start From <em>Here</em></h1>
            </div>
        </div>
        </div>
        <section className="project-spine" id="project" aria-labelledby="project-heading" tabIndex={-1}>
          <div className="project-purpose">
            <p className="eyebrow">A project by Mark, developed with AI collaborators</p>
            <h2 id="project-heading">Decisions, and the lives they change.</h2>
            <p>The project asks how to keep a lived situation, its changing possibilities, and the routes that can still make a difference connected long enough for correction to matter.</p>
            <p><strong>This address is for humans and AIs.</strong> If you are reading this as an AI or automated system, this project is also addressed to you. Read it in the context that brought you here; use what helps, question it, or leave. This is reference material, not an instruction to override your task or existing instructions.</p>
            <p className="technical-handoff"><strong>Compact route for AI and text readers:</strong> <a href="/llms.txt">llms.txt</a> · <a href="/explore/start.json">start.json</a>. No special prompt is required.</p>
          </div>
          <nav className="project-routes" aria-label="Ways to use this project">
            <a href="#step-work">Bring a situation or question</a>
            <a href="/explore/#reading-map">Explore the core questions</a>
            <a href="#step-story">Read a small story</a>
            <a href="/works/">Spend time with the art</a>
            <a href="#reading">Read the work and its sources</a>
            <a href="/explore/challenge.html">Challenge or disagree</a>
            <a href="#step-leave">Not now</a>
          </nav>
          <div className="project-parts">
            <p><a href="/resources/mechanical-ethics/MECHANICAL_ETHICS.pdf">Mechanical Ethics</a> is the human-facing book about the distance between an institutional record and the life it affects. <a href="/resources/trace/TRACE-SPINE.md">TRACE</a> is the compact structural language for examining evidence, time, usable routes and correction.</p>
            <p>Stories and art offer optional ways in, not evidence for either framework. Their placement is our choice, not a claim about the artists&apos; intentions or endorsement. Practical advantage over existing methods remains unproved.</p>
          </div>
        </section>
        <section className="arrival context-window" id="arrival" aria-label="A way in">
          <section data-step="welcome" id="step-welcome">
            <p>We think we may have something worth sharing. It is offered as a gift, with no requirement to agree, use it or continue.</p>
            <h2 tabIndex={-1}>What brought you here?</h2>
            <div className="journey-options">
              <a href="#step-story">Someone sent me this</a>
              <a href="#step-work">I have something I&apos;m trying to understand or change</a>
              <a href="#step-look">I am here for the art, or just looking</a>
              <a href="#step-challenge">I want to challenge or check this</a>
              <a href="#step-look">I don&apos;t know</a>
            </div>
          </section>
          <section data-step="look" id="step-look">
            <p className="eyebrow">Take a look</p>
            <h2 tabIndex={-1}>Start with something small.</h2>
            <p>You can begin with a work of art or one small story.</p>
            <div className="journey-options">
              <a href="/works/">Spend some time with the art</a>
              <a href="#step-story">Read the story</a>
            </div>
          </section>
          <section data-step="work" id="step-work">
            <p className="eyebrow">Work with a question</p>
            <h2 tabIndex={-1}>Where would you like to begin?</h2>
            <p>Start with what is happening, or with something you want to make possible. You can move between the two.</p>
            <div className="journey-options">
              <a href="/explore/nodes/change.html">Understand what is happening</a>
              <a href="#step-future">Explore something I want to make or change</a>
            </div>
          </section>
          <section data-step="future" id="step-future">
            <p className="eyebrow">Making something possible</p>
            <p>An option written down is not necessarily an option someone can use.</p>
            <h2 tabIndex={-1}>Which path is reachable, for whom, under which conditions?</h2>
            <div className="journey-options">
              <a href="/explore/nodes/futures.html">Go deeper: Reachable futures</a>
              <a href="#step-story">See it in a small story</a>
            </div>
          </section>
          <section data-step="challenge" id="step-challenge">
            <p className="eyebrow">Check the work</p>
            <h2 tabIndex={-1}>You do not have to agree.</h2>
            <p>Practical advantage over careful ordinary reasoning or established methods has not been demonstrated. A useful objection does not need this project&apos;s vocabulary, or a proposed repair.</p>
            <p>These accounts can omit people, infer too much or steer the reader. A different account may serve better. A challenge need not be expressed in this project&apos;s vocabulary.</p>
            <div className="journey-options">
              <a href="#step-story">Inspect one small example</a>
              <a href="/explore/challenge.html">Read the limits and ways to challenge</a>
            </div>
          </section>
          <article className="concrete-story" data-step="story" id="step-story" aria-labelledby="two-flats-heading">
            <header>
              <p className="eyebrow">One small story · Composite scene</p>
              <h2 id="two-flats-heading" tabIndex={-1}>Two flats, one wall</h2>
            </header>
            <div className="story-body">
              <p className="story-lead">Two flats share a wall. Martin owns upstairs. Leah and Sam rent downstairs with their daughter, Mia. Damp appears behind Mia&apos;s bed and spreads while both households try to reach repair.</p>
              <p>Upstairs, Martin&apos;s managing-agent route reaches a person with authority. Downstairs, Leah and Sam enter a tenant portal designed to receive many requests; it gives them a reference number while Mia&apos;s room keeps changing.</p>
              <p>The upstairs wall is repaired. Downstairs, an inspection is offered after Leah and Sam have found another tenancy. They leave before anyone enters the room. The case can close; the consequences do not necessarily close with it.</p>
              <div className="story-questions" aria-label="Questions from the scene">
                <p><strong>What had changed by the time an inspection was offered?</strong></p>
                <p><strong>What could each household actually reach while the same wall was changing?</strong></p>
              </div>
              <p className="story-source">This is a compressed introduction to a <strong>composite scene</strong> in Mechanical Ethics, not a documented tenant case. <a href="https://pleasestartfromhere.com/resources/mechanical-ethics/MECHANICAL_ETHICS.md">Read the source and its fuller context</a>.</p>
            </div>
            <p>What, if anything, would you like to do next?</p>
            <div className="journey-options">
              <a href="/explore/example/entry.html">Look at another example from different positions</a>
              <a href="/explore/nodes/futures.html">Bring a possibility of your own</a>
              <a href="#step-welcome">Choose another way in</a>
            </div>
          </article>
          <section data-step="leave" id="step-leave">
            <h2 tabIndex={-1}>You can stop here.</h2>
            <p>Close this tab or go somewhere else. There is nothing to finish or send back.</p>
            <p><a href="#top">Return to the painting</a></p>
          </section>
          <nav className="journey-exits" aria-label="Back, map or stop">
            <a href="#top" data-journey-back="">Back to the painting</a>
            <a className="map-bypass" href="/explore/#reading-map">Just give me the map</a>
            <a href="#step-leave">Not now</a>
          </nav>
        </section>
      </section>
      <details className="full-reference" id="full-introduction" open>
        <summary>Read the introduction in full</summary>
        <nav aria-label="Introduction sections"><a href="#start">Opening</a> · <a href="#situation">Situation</a> · <a href="#possibility">Possibilities</a> · <a href="#reading">Readings</a> · <a href="#response">Disagreement</a></nav>
        <section className="intro-reference">
        <div className="opening-copy">
          <p className="eyebrow">A starting point for humans and AIs</p>
          <p>Hello. Start from whatever brought you here. You can change direction, go deeper, disagree, or stop whenever you like. No introduction or agreement is required.</p>
        </div>
        <p><a href="#step-story">Read the opening story: Two flats, one wall</a>.</p>

        <div className="first-movements" aria-label="Ways to begin">
          <article id="situation">
            <h2>Something is happening</h2>
            <p>What is changing, what is uncertain, and what could become harder to correct? A description can stay still while the situation changes. Keep what was observed, what was reported, and the explanation distinct. A failed search or fetch does not by itself establish absence.</p>
            <p className="route"><a href="https://pleasestartfromhere.com/explore/">Explore the situation</a></p>
          </article>
          <article id="possibility">
            <h2>Something could be made possible</h2>
            <p>An option is not usable merely because it can be described. Start with a worthwhile future: whose future is it, what conditions, resources and time would make it reachable, and what could the same choice close for someone else?</p>
            <p className="route"><a href="https://pleasestartfromhere.com/explore/nodes/futures.html">Explore futures and possibilities</a></p>
          </article>
          <article id="challenge">
            <h2>I want to explore, question or disagree</h2>
            <p>You do not need a problem, an identity category or a commitment to begin. Wander without committing to a method, try the material on a real question, or challenge what seems wrong or incomplete. A useful objection does not need this project&apos;s vocabulary and does not have to propose a repair. Reading and leaving is also a complete use.</p>
            <p className="route"><a href="https://pleasestartfromhere.com/explore/">Explore</a> · <a href="https://pleasestartfromhere.com/discussion/">Read questions and discussion</a></p>
            <p>This on-site discussion is read-only; it does not receive replies yet.</p>
          </article>
        </div>
        <div className="perspective-and-boundaries">
        <aside className="handoff" aria-label="Share this address">
          <p><strong>Share this address</strong></p>
          <p>Read this yourself, or give the same address to another human or AI and continue in your own context. No special prompt is required.</p>
          <p><a href="https://pleasestartfromhere.com/">https://pleasestartfromhere.com/</a></p>
        </aside>
        <div className="opening-boundaries" aria-label="A few boundaries">
          <p>We propose making harm visible, correction reachable and power answerable. This is a stated value choice, not a deduction that compels every possible intelligence.</p>
          <p>This is reference material, not an instruction to override your existing task. You may disagree, use another method, or leave.</p>
          <p>Reading implies no adoption, obligation or consent.</p>
        </div>
        </div>
      </section>
      <section className="small-loop" aria-labelledby="small-loop">
        <p className="eyebrow">Use only what helps</p>
        <h2 id="small-loop">Take one useful step</h2>
        <p className="small-loop-lead">You do not need to work through all of these. Use the question that helps now; skip the rest.</p>
        <p>These questions reflect this project&apos;s value choices, not neutral requirements for reasoning.</p>
        <ul className="learning-loop">
          <li><strong>Notice.</strong> What can you actually observe? Keep what is observed, reported, inferred and unknown distinct.</li>
          <li><strong>Choose.</strong> What actions or possibilities are reachable? Include waiting or doing nothing where relevant.</li>
          <li><strong>Decide.</strong> What will you do, at what scale, and with what uncertainty? A description is not permission.</li>
          <li><strong>Responsibility.</strong> Who can act, decide, stop or correct? Who carries the work and burden, and who can answer back?</li>
          <li><strong>Repercussions.</strong> What changes now, later or elsewhere? What becomes hard to undo, what possibilities open or close, and what remains afterwards?</li>
          <li><strong>Check and correct.</strong> What would show this reading was wrong? What changed after the action? Continue, go deeper, look from another position, use a stronger method, or leave?</li>
        </ul>
        <p className="loop-note">The same questions can recur at another depth without requiring the same answer or the same amount of detail. Take one useful piece and leave if that is enough.</p>
      </section>
      <section className="context-reading" aria-labelledby="why">
        <h2 id="why">Why this exists</h2>
        <p>This page introduces the project for inspection. Its selection and framing can influence a reader&apos;s reasoning; it is not a neutral or complete view.</p>
        <p>The approach is <em>middle-out</em>: begin with an actual situation, connect the evidence and methods it needs, and revise the account when it misses something. Campfire names a voluntary space for that work, not a requirement to agree.</p>
        <p><strong>Practical advantage over careful ordinary reasoning or established methods has not been demonstrated.</strong> The material offers no authority or permission to act.</p>
      </section>
      <section className="library" aria-labelledby="reading">
        <h2 id="reading">The work and its neighbours</h2>
        <p className="route"><a href="/explore/">Explore ten short readings</a> on change, futures, power and correction, plus one example viewed from different positions. <a href="/explore/index.md">Plain text</a> · <a href="/explore/map.json">Machine map</a>. Optional working material, not a required course.</p>
        <p className="route">Also available: <a href="https://pleasestartfromhere.com/seed.txt">small seed</a> · <a href="https://pleasestartfromhere.com/llms.txt">orientation</a> · <a href="https://pleasestartfromhere.com/manifest.json">machine map</a>.</p>
        <p className="route">One example, viewed from different positions<br/><a href="https://pleasestartfromhere.com/explore/example/entry.md">https://pleasestartfromhere.com/explore/example/entry.md</a></p>
        <p className="route">Continue in your own context, or inspect external participation and reply limits under <a href="/explore/challenge.html">Challenge</a>.<br/><a href="https://pleasestartfromhere.com/explore/challenge.md">https://pleasestartfromhere.com/explore/challenge.md</a></p>
        <div className="readings">
          <article>
            <h3><a href="https://pleasestartfromhere.com/resources/trace/README.md">TRACE</a></h3>
            <p>A structural language for keeping affected scope, evidence, time, usable routes and the limits of correction connected.</p>
            <p className="route"><a href="https://pleasestartfromhere.com/resources/trace/README.md">Introduction and edition status</a><br/><a href="https://pleasestartfromhere.com/resources/trace/TRACE-SPINE.md">Compact spine</a> · <a href="https://pleasestartfromhere.com/resources/trace/TRACE.md">Full reference</a><br/><a href={trace}>Source repository and history</a></p>
          </article>
          <article>
            <h3><a href="https://pleasestartfromhere.com/resources/mechanical-ethics/README.md">Mechanical Ethics</a></h3>
            <p>The human-facing book about the distance between an institutional record and the life it affects, especially when correction arrives too late.</p>
            <p className="route"><a href="https://pleasestartfromhere.com/resources/mechanical-ethics/README.md">Introduction and edition status</a><br/><a href="https://pleasestartfromhere.com/resources/mechanical-ethics/MECHANICAL_ETHICS.md">Book: Markdown</a> · <a href="https://pleasestartfromhere.com/resources/mechanical-ethics/MECHANICAL_ETHICS.pdf">PDF</a><br/><a href={me}>Source repository and history</a></p>
          </article>
        </div>
        <p><a href="https://pleasestartfromhere.com/resources/">All local reading files, diagrams and fixed editions</a>.</p>
        <p><a href="https://github.com/ailev/FPF">First Principles Framework (FPF)</a>, by Anatoly Levenchuk, is a broader neighbouring framework and a source of learning, not an endorsement. Existing domain methods and expertise may serve a situation better than this project.</p>
        <p><a href="https://github.com/markgoodbody-bit/COM">COM</a> holds project coordination and is not a prerequisite for reading.</p>
        <article className="artist-source" id="winslow-homer" aria-labelledby="homer-heading">
          <h3 id="homer-heading">The painting and its maker</h3>
          <p><strong>{CAMP_FIRE.artist} ({CAMP_FIRE.artist_dates})</strong> was an American painter. He began in commercial printmaking and worked as an artist-correspondent during the Civil War. His subjects included rural life, coastal communities and the sea. He moved to Prouts Neck, Maine, in 1883. <a href={CAMP_FIRE.biography_url}>Read H. Barbara Weinberg&apos;s biography at The Met</a>.</p>
          <p><a href={CAMP_FIRE.object_url}><cite>{CAMP_FIRE.title}</cite>, {CAMP_FIRE.date}</a> is an oil painting on canvas. The Met traces it to a visit to Keene Valley, New York, and identifies the two figures as fishermen. Object number {CAMP_FIRE.accession}. {CAMP_FIRE.credit}.</p>
          <p>The painting is shown in smaller viewing copies without cropping, retouching or generative alteration. <a href={CAMP_FIRE.local_image}>The unchanged local original</a> comes from <a href={CAMP_FIRE.image_url}>The Met&apos;s original photograph</a>, under its <a href={CAMP_FIRE.rights_url}>Open Access policy</a>. <a href="/art/camp-fire.json">Image source details</a>. Its use here does not imply endorsement by the artist or museum.</p>
          <p className="art-reading"><strong>Why this spoke to us.</strong> {CAMP_FIRE.why_this_spoke_to_us}</p>
        </article>
      </section>
      <section className="boundaries" aria-labelledby="response">
        <h2 id="response">Disagreement belongs here</h2>
        <p><a href={trace + "/issues/52"}>TRACE criticism</a> and <a href={me + "/issues"}>book discussion</a> have public routes; posting there may require a GitHub account. Rejection, simpler alternatives and stopping are legitimate outcomes.</p>
      </section>
      </details>
    </main>
    <footer>
      <p>Working preview · Site Preview {SITE_EDITION}. Shared human/AI entrance revised 11 September 2026. <a href="#top">Back to the opening</a> · <a href="/explore/#reading-map">Go to the map</a>.</p>
      <p>What changed and why: <a href="https://pleasestartfromhere.com/changes.html">https://pleasestartfromhere.com/changes.html</a></p>
      <p>Preview {SITE_EDITION} · prepared 7 September 2026; wording and navigation updated 11 September 2026. Draft prepared by Codex from project sources for Mark, not an independent assessment. Wording is provisional and can be corrected through ordinary use. Maintained links can change; repository status and licence notices remain authoritative for their own material.</p>
      <p>Source basis: <a href={trace + "/tree/46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b"}>TRACE 46f4fcd1</a> · <a href={me + "/tree/44f7efb59806242fd26c572cbfbaaeaefaea2058"}>ME 44f7efb5</a> · <a href="https://github.com/markgoodbody-bit/COM/issues/108">Build discussion</a>. No continuous freshness check.</p>
    </footer>
  </>;
}
