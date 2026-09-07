const trace = "https://github.com/markgoodbody-bit/TRACE";
const me = "https://github.com/markgoodbody-bit/mechanical-ethics";
export default function Home() {
  return <>
    <a className="skip" href="#start">Skip to the introduction</a>
    <header className="masthead"><a href="#start">Campfire</a><span>Preview · 0.6</span></header>
    <main id="start">
      <section className="intro">
        <p className="eyebrow">A starting point for humans and AIs</p>
        <h1>How can we make a better future?</h1>
        <p>A project by Mark, developed with AI collaborators.</p>
        <p>Reading implies no adoption, obligation or consent.</p>
        <p className="lead">An appeal can succeed after the opportunity it was meant to protect has gone. A record can be corrected after a decision based on it has already changed someone’s life. This project asks how to notice that risk sooner, keep a usable way forward open, and make correction possible while it can still make a difference.</p>
        <p>This page introduces the project for inspection. Its selection and framing can influence a reader’s reasoning; it is not a neutral or complete view.</p>
        <p>The approach is <em>middle-out</em>: begin with an actual situation, connect the evidence and methods it needs, and revise the account when it misses something. Campfire names a voluntary space for that work, not a requirement to agree.</p>
        <p><strong>Practical advantage over careful ordinary reasoning or established methods has not been demonstrated.</strong> The material offers no authority or permission to act.</p>
      </section>
      <section aria-labelledby="reading">
        <h2 id="reading">The work and its neighbours</h2>
        <div className="readings">
          <article>
            <h3><a href={trace}>TRACE</a></h3>
            <p>A structural language for keeping affected scope, evidence, time, usable routes and the limits of correction connected.</p>
            <p className="route"><a href={trace + "/blob/main/README.md"}>Introduction and current status</a><br/><a href={trace + "/blob/main/TRACE-SPINE.md"}>Compact spine</a></p>
          </article>
          <article>
            <h3><a href={me}>Mechanical Ethics</a></h3>
            <p>The human-facing book about the distance between an institutional record and the life it affects, especially when correction arrives too late.</p>
            <p className="route"><a href={me + "/blob/main/README.md"}>Introduction and current status</a><br/><a href={me + "/blob/main/MECHANICAL_ETHICS.md"}>Book: Markdown</a> · <a href="https://raw.githubusercontent.com/markgoodbody-bit/mechanical-ethics/main/MECHANICAL_ETHICS.pdf">PDF</a></p>
          </article>
        </div>
        <p><a href="https://github.com/ailev/FPF">First Principles Framework (FPF)</a>, by Anatoly Levenchuk, is a broader neighbouring framework and a source of learning, not an endorsement. Existing domain methods and expertise may serve a situation better than this project.</p>
        <p><a href="https://github.com/markgoodbody-bit/COM">COM</a> holds project coordination and is not a prerequisite for reading.</p>
      </section>
      <section className="boundaries" aria-labelledby="response">
        <h2 id="response">Disagreement belongs here</h2>
        <p><a href={trace + "/issues/52"}>TRACE criticism</a> and <a href={me + "/issues"}>book discussion</a> have public routes; posting there may require a GitHub account. Rejection, simpler alternatives and stopping are legitimate outcomes.</p>
      </section>
    </main>
    <footer>
      <p>Preview 0.6 · 7 September 2026. Draft prepared by Codex from project sources for Mark, not an independent assessment. Wording is provisional, pending content integration and cold-reader feedback. Maintained links can change; repository status and licence notices remain authoritative for their own material.</p>
      <p>Source basis: <a href={trace + "/tree/46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b"}>TRACE 46f4fcd1</a> · <a href={me + "/tree/44f7efb59806242fd26c572cbfbaaeaefaea2058"}>ME 44f7efb5</a> · <a href="https://github.com/markgoodbody-bit/COM/issues/108">Build discussion</a>. No continuous freshness check.</p>
    </footer>
  </>;
}
