// Draft-only human-first entrance composition from CC's COM #108 research.
// Preserve published story, art bytes/credits and existing machine routes.
// This is a generated-view transform, not a new copy of source book content.
// Derived, reversible first-encounter composition only. The authored
// React source, Homer's painting and the released book all remain untouched.
const newRoute = '/read/me-v0.8.html';
export function humanFirstHomepage(html) {
  const main = '<main id="start">';
  const story = '<article class="concrete-story opening-story" id="step-story"';
  const painting = '<div class="art-hero" id="top">';
  const artTitle = '<h1>Please Start From <em>Here</em></h1>';
  for (const marker of [main, story, painting, artTitle]) {
    if (html.split(marker).length !== 2) {
      throw Error('Maintained homepage marker changed: ' + marker);
    }
  }
  if (!(html.indexOf(main) < html.indexOf(painting) &&
        html.indexOf(painting) < html.indexOf(story))) {
    throw Error('Published painting-first order changed');
  }
  const entrance = [
    '<section class="human-first-door" aria-labelledby="human-door-title">',
    '<p class="human-door-kicker">Independent research · free to read or leave</p>',
    '<h2 id="human-door-title">Decisions can be right on paper and wrong in a life.</h2>',
    '<p class="human-door-lead">Mechanical Ethics is a complete free book about what happens while real people wait for a correction — and what we can build to keep worthwhile futures open. TRACE is an optional technical companion.</p>',
    '<nav class="human-door-routes" aria-label="Ways to begin">',
    '<a href="#step-story"><strong>Read the three-minute story</strong><span>One composite example</span></a>',
    '<a href="/read/me-v0.8.html"><strong>Read the complete book</strong><span>Released ME v0.8.0 · HTML</span></a>',
    '<a href="/llms.txt"><strong>Reading as an AI?</strong><span>Compact text route</span></a>',
    '</nav>',
    '<p class="human-door-status">Research in progress, not advice. Released does not mean validated. ',
    '<a href="#project">About this project</a> · ',
    '<a href="/resources/mechanical-ethics/MECHANICAL_ETHICS.pdf">Original PDF</a> · ',
    '<a href="/resources/mechanical-ethics/MECHANICAL_ETHICS.md">Original Markdown</a>.</p>',
    '<details class="human-door-details" id="human-door-limits">',
    '<summary>Limits, source status, and help with a housing problem now</summary>',
    '<p>Mechanical Ethics v0.8.0 and TRACE v0.4.0 are released reading baselines, not validated methods. Yet Another Clearing and The Human Record are separate experiments. Reading grants no permission or obligation, and this project is not a substitute for established specialist help.</p>',
    '<p><strong>For a housing problem affecting you now:</strong> this site is not a housing support service. ',
    '<a href="https://england.shelter.org.uk/housing_advice/repairs/damp_and_mould_in_rented_homes">Shelter: damp and mould in rented homes</a> and ',
    '<a href="https://www.gov.uk/government/publications/awaabs-law-guidance-for-social-landlords/awaabs-law-guidance-for-social-landlords-timeframes-for-repairs-in-the-social-rented-sector">GOV.UK: guidance for English social landlords</a> offer established starting points. The appropriate action depends on the situation; this site does not provide legal or clinical advice.</p>',
    '</details>',
    '</section>'
  ].join('');
  // The original art image, visible credit and authored page-title H1 remain
  // in first position. Append the small human orientation AFTER the painting
  // composition and BEFORE the unchanged story at every viewport.
  let output = html;
  output = output.replaceAll(
    'href="https://pleasestartfromhere.com/resources/mechanical-ethics/MECHANICAL_ETHICS.md"',
    'href="' + newRoute + '"');
  output = output.replaceAll(
    'href="/resources/mechanical-ethics/MECHANICAL_ETHICS.md"',
    'href="' + newRoute + '"');
  // Insert AFTER updating the old authored book link: the new original
  // Markdown escape route in entrance must never be rewritten to HTML.
  output = output.replace(story, entrance + story);
  // Update old destination labels when they now point to formatted HTML,
  // while retaining visibly inspectable original Markdown and PDF routes.
  output = output.replace(
    'href="/read/me-v0.8.html">Book: Markdown</a>',
    'href="/read/me-v0.8.html">Complete HTML book</a> · <a href="/resources/mechanical-ethics/MECHANICAL_ETHICS.md">Original Markdown</a>'
  );
  return output;
}
export const HUMAN_DOOR_CSS = [
  '.human-first-door{margin:0 auto 1.5rem;width:min(100%,62rem);padding:.75rem 0 1.25rem;border-bottom:1px solid var(--border)}',
  '.human-first-door h2{font:400 clamp(1.6rem,3vw,2.35rem)/1.2 var(--serif);margin:.3rem 0 .75rem;max-width:32ch}',
  '.human-door-kicker{font-size:.8rem;letter-spacing:.075em;text-transform:uppercase;color:var(--muted);margin:0}',
  '.human-door-lead{font-size:clamp(1rem,1.6vw,1.12rem);line-height:1.55;max-width:68ch}',
  '.human-door-routes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.55rem;margin:1rem 0}',
  '.human-door-routes a{border:1px solid var(--border);padding:.7rem .85rem;display:grid;gap:.2rem;color:var(--foreground);text-decoration:none;min-height:3.6rem}',
  '.human-door-routes a:hover,.human-door-routes a:focus-visible{text-decoration:underline}',
  '.human-door-routes span{font-size:.82rem;color:var(--muted)}',
  '.human-door-status{font-size:.9rem;line-height:1.5;max-width:76ch}',
  '.human-door-details{font-size:.9rem;line-height:1.55;max-width:76ch;margin:.7rem 0 0}',
  '.human-door-details summary{cursor:pointer;min-height:2.75rem;padding:.45rem 0;color:var(--foreground)}',
  '.human-door-details summary:focus-visible{outline:3px solid var(--foreground);outline-offset:3px}',
  '.human-door-details p{margin:.65rem 0}',
  'body:has(.human-first-door) .opening-composition{margin-bottom:0}',
  'body:has(.human-first-door) .intro{margin-top:0}',
  '@media(max-width:690px){.human-first-door{padding:.6rem 0 .9rem}.human-first-door h2{font-size:1.65rem}.human-door-lead{font-size:1rem}',
  '.human-door-routes{grid-template-columns:1fr;gap:.3rem;margin:.6rem 0}',
  '.human-door-routes a{min-height:2.85rem;padding:.35rem .65rem;display:flex;justify-content:space-between;align-items:center;gap:.5rem}',
  '.human-door-routes strong{font-size:.95rem}.human-door-routes span{font-size:.78rem;text-align:right}',
  '.human-door-status{font-size:.85rem}.human-door-details{font-size:.85rem}}'
].join('\n');
