/* Static React rendering, not a Next.js runtime: native links must work without JavaScript. */
/* eslint-disable next/no-html-link-for-pages */
import { SITE_EDITION } from '../scripts/site-edition.mjs';
import { CAMP_FIRE } from '../scripts/camp-fire.mjs';
const trace = "https://github.com/markgoodbody-bit/TRACE";
const me = "https://github.com/markgoodbody-bit/mechanical-ethics";
export default function Home() {
  return <>
    <a className="skip" href="#start">Skip to the introduction</a>
    <header className="masthead" id="top">
      <a className="site-name" href="#start">Please Start From Here</a>
      <nav aria-label="Reading routes"><a href="#situation">Ways to begin</a><a href="/explore/">Explore</a><a href="https://pleasestartfromhere.com/resources/mechanical-ethics/MECHANICAL_ETHICS.pdf">Read the book</a><a href="https://pleasestartfromhere.com/discussion/">Discussion</a></nav>
      <span>Working preview · Site Preview {SITE_EDITION}</span>
    </header>
    <main id="start">
      <section className="intro">
        <div className="opening-composition">
        <div className="opening-copy">
        <p className="eyebrow">A starting point for humans and AIs</p>
        <h1>Please Start From Here</h1>
        <p className="guiding-question">How can we make a better future?</p>
        <p>A project by Mark, developed with AI collaborators.</p>
        <p>Hello. Start from whatever brought you here. Pick whichever beginning feels closest; you can change direction, go deeper, or stop whenever you like. No introduction or agreement is required.</p>
        </div>
        <figure className="camp-fire" aria-labelledby="camp-fire-credit">
          <figcaption id="camp-fire-credit">
            <span><a href={CAMP_FIRE.object_url}><cite>{CAMP_FIRE.title}</cite></a>, {CAMP_FIRE.date}, by <a href="#winslow-homer">{CAMP_FIRE.artist}</a>.</span>
            <span>{CAMP_FIRE.museum}. <a href={CAMP_FIRE.rights_url}>Public domain, Open Access</a>.</span>
          </figcaption>
          <img src={CAMP_FIRE.local_image} alt={CAMP_FIRE.alt} width={CAMP_FIRE.width} height={CAMP_FIRE.height} loading="lazy" decoding="async" />
        </figure>
        </div>
        <div className="first-movements" aria-label="Ways to begin">
          <article id="situation">
            <h2>Something is happening</h2>
            <p>What is changing, what is uncertain, and what could become harder to correct? A description can stay still while the situation changes. Keep what was observed, what was reported, and the explanation distinct. A failed search or fetch does not by itself establish absence.</p>
            <p className="route"><a href="https://pleasestartfromhere.com/explore/">https://pleasestartfromhere.com/explore/</a></p>
          </article>
          <article id="possibility">
            <h2>Something could be made possible</h2>
            <p>An option is not usable merely because it can be described. Start with a worthwhile future: whose future is it, what conditions, resources and time would make it reachable, and what could the same choice close for someone else?</p>
            <p className="route"><a href="https://pleasestartfromhere.com/explore/nodes/futures.html">https://pleasestartfromhere.com/explore/nodes/futures.html</a></p>
          </article>
          <article id="challenge">
            <h2>Something here seems wrong, incomplete or worth discussing</h2>
            <p>A useful objection does not need this project&apos;s vocabulary and does not have to propose a repair. What is missing, what does another method handle better, and can people affected by the account answer back?</p>
            <p>Read the current questions and project responses. This on-site discussion is read-only; it does not receive replies yet.</p>
            <p className="route"><a href="https://pleasestartfromhere.com/discussion/">https://pleasestartfromhere.com/discussion/</a></p>
          </article>
          <article id="source">
            <h2>I want the compact source</h2>
            <p>This material is reference, not permission or authority. Source identity, edition and uncertainty should remain inspectable. Reading does not require adoption, agreement or report-back.</p>
            <p className="route"><a href="https://pleasestartfromhere.com/explore/start.json">https://pleasestartfromhere.com/explore/start.json</a><br/>Complete HTML source-text alternative:<br/><a href="https://pleasestartfromhere.com/read/start.html">https://pleasestartfromhere.com/read/start.html</a></p>
          </article>
          <article id="curiosity">
            <h2>I am only curious</h2>
            <p>Wander. You do not need a problem, an identity category or a commitment to begin. Notice what seems consequential, surprising, useful or wrong. Reading and leaving is a complete use.</p>
            <p className="route"><a href="https://pleasestartfromhere.com/explore/">https://pleasestartfromhere.com/explore/</a></p>
          </article>
        </div>
        <div className="perspective-and-boundaries">
        <aside className="handoff" aria-label="Another perspective">
          <p><strong>Another perspective</strong></p>
          <p>If it helps, read this yourself or hand this address to an AI and ask what it notices, disagrees with, or would try on a real question. No special prompt is required.</p>
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
        <p className="lead">An appeal can succeed after the opportunity it was meant to protect has gone. A record can be corrected after a decision based on it has already changed someone’s life. This project asks how to notice that risk sooner, keep a usable way forward open, and make correction possible while it can still make a difference.</p>
        <p>This page introduces the project for inspection. Its selection and framing can influence a reader’s reasoning; it is not a neutral or complete view.</p>
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
          <p><strong>{CAMP_FIRE.artist} ({CAMP_FIRE.artist_dates})</strong> was an American painter. He began in commercial printmaking and worked as an artist-correspondent during the Civil War. His subjects included rural life, coastal communities and the sea. He moved to Prouts Neck, Maine, in 1883. <a href={CAMP_FIRE.biography_url}>Read H. Barbara Weinberg’s biography at The Met</a>.</p>
          <p><a href={CAMP_FIRE.object_url}><cite>{CAMP_FIRE.title}</cite>, {CAMP_FIRE.date}</a> is an oil painting on canvas. The Met traces it to a visit to Keene Valley, New York, and identifies the two figures as fishermen. Object number {CAMP_FIRE.accession}. {CAMP_FIRE.credit}.</p>
          <p>The image is reproduced without cropping or alteration from <a href={CAMP_FIRE.image_url}>The Met’s original photograph</a>, under its <a href={CAMP_FIRE.rights_url}>Open Access policy</a>. <a href="/art/camp-fire.json">Image source details</a>. Its use here does not imply endorsement by the artist or museum.</p>
        </article>
      </section>
      <section className="boundaries" aria-labelledby="response">
        <h2 id="response">Disagreement belongs here</h2>
        <p><a href={trace + "/issues/52"}>TRACE criticism</a> and <a href={me + "/issues"}>book discussion</a> have public routes; posting there may require a GitHub account. Rejection, simpler alternatives and stopping are legitimate outcomes.</p>
      </section>
    </main>
    <footer>
      <p>What changed and why: <a href="https://pleasestartfromhere.com/changes.html">https://pleasestartfromhere.com/changes.html</a></p>
      <p>Preview {SITE_EDITION} · prepared 7 September 2026; wording and navigation updated 8 September 2026. Draft prepared by Codex from project sources for Mark, not an independent assessment. Wording is provisional, pending content integration and cold-reader feedback. Maintained links can change; repository status and licence notices remain authoritative for their own material.</p>
      <p>Source basis: <a href={trace + "/tree/46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b"}>TRACE 46f4fcd1</a> · <a href={me + "/tree/44f7efb59806242fd26c572cbfbaaeaefaea2058"}>ME 44f7efb5</a> · <a href="https://github.com/markgoodbody-bit/COM/issues/108">Build discussion</a>. No continuous freshness check.</p>
    </footer>
  </>;
}
