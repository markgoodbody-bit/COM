// Draft-only human-first entrance composition from CC's COM #108 research.
// Preserve published story, art bytes/credits and existing machine routes.
// This is a generated-view transform, not a new copy of source book content.
const newRoute = '/read/me-v0.8.html';
export function humanFirstHomepage(html) {
  const marker = '<main id="start">';
  if (!html.includes(marker) || html.split(marker).length !== 2)
    throw Error('Maintained homepage structure changed; no blind injection');
  const intro = [
    '<section class="human-first-door" aria-labelledby="human-door-title">',
    '<p class="human-door-kicker">Independent human-first entrance · free research</p>',
    '<h1 id="human-door-title">Please Start From Here</h1>',
    '<p class="human-door-lead">A free book and small research project about a familiar problem: a decision can be right in the record while someone’s real options close before help arrives. It also asks what worthwhile futures we can create and sustain.</p>',
    '<nav class="human-door-routes" aria-label="Three clear ways to begin">',
    '<a href="#step-story"><strong>Read a three-minute story</strong><span>An ordinary composite case</span></a>',
    '<a href="#project"><strong>What is this project?</strong><span>Purpose, limits and neighbouring work</span></a>',
    '<a href="/llms.txt"><strong>AI and text reading</strong><span>A compact independent reader route</span></a>',
    '</nav>',
    '<p class="human-door-status"><strong>Research in progress, not advice.</strong> Mechanical Ethics v0.8.0 and TRACE v0.4.0 are released reading baselines, not validated methods. ',
    '<a href="/read/me-v0.8.html">Read the complete released Mechanical Ethics book online</a>. ',
    'Yet Another Clearing and The Human Record are separate, experimental projects. Reading grants no permission or obligation and makes no claim that this works better than ordinary specialist practice.</p>',
    '<p class="human-door-safety"><strong>If a housing problem is affecting you now:</strong> use existing help rather than this research: ',
    '<a href="https://england.shelter.org.uk/housing_advice/repairs/damp_and_mould_in_rented_homes">Shelter’s damp and mould guidance</a>',
    ' and <a href="https://www.gov.uk/government/publications/awaabs-law-guidance-for-social-landlords/awaabs-law-guidance-for-social-landlords-timeframes-for-repairs-in-the-social-rented-sector">GOV.UK guidance for social landlords in England</a>. ',
    'Your route depends on your circumstances; this site does not classify hazards or provide legal advice.</p>',
    '</section>'
  ].join('');
  let output = html.replace(marker, marker + intro);
  const artTitle = '<h1>Please Start From <em>Here</em></h1>';
  if (!output.includes(artTitle)) throw Error('Original art title changed');
  output = output.replace(artTitle, '<p class="hero-title">Please Start From <em>Here</em></p>');
  output = output.replaceAll(
    'href="https://pleasestartfromhere.com/resources/mechanical-ethics/MECHANICAL_ETHICS.md"',
    'href="' + newRoute + '"');
  output = output.replaceAll(
    'href="/resources/mechanical-ethics/MECHANICAL_ETHICS.md"',
    'href="' + newRoute + '"');
  // The old Markdown link now targets HTML; do not mislabel the new format.
  // Retain a direct route to the byte-identical original Markdown beside it.
  output = output.replace(
    'href="/read/me-v0.8.html">Book: Markdown</a>',
    'href="/read/me-v0.8.html">Complete HTML book</a> · <a href="/resources/mechanical-ethics/MECHANICAL_ETHICS.md">Original Markdown</a>'
  );
  return output;
}
export const HUMAN_DOOR_CSS = [
  '.human-first-door{margin:0 auto 1.5rem;width:min(100%,62rem);padding:1rem 0;border-bottom:1px solid var(--border)}',
  '.human-first-door h1{font:400 clamp(2.15rem,4.5vw,3.5rem)/1.1 var(--serif);margin:.4rem 0 1rem;letter-spacing:-.035em}',
  '.human-door-kicker{font-size:.82rem;letter-spacing:.075em;text-transform:uppercase;color:var(--muted);margin:0}',
  '.human-door-lead{font-size:clamp(1.1rem,2.1vw,1.38rem);line-height:1.45;max-width:58ch}',
  '.human-door-routes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.55rem;margin:1.1rem 0}',
  '.human-door-routes a{border:1px solid var(--border);padding:.8rem .85rem;display:grid;gap:.2rem;color:var(--foreground);text-decoration:none;min-height:4rem}',
  '.human-door-routes a:hover,.human-door-routes a:focus-visible{text-decoration:underline}',
  '.human-door-routes span{font-size:.83rem;color:var(--muted)}',
  '.human-door-status{font-size:.94rem;line-height:1.5;max-width:74ch}',
  '.human-door-safety{font-size:.88rem;line-height:1.5;max-width:75ch}',
  'body:has(.human-first-door) main{margin-top:0}',
  'body:has(.human-first-door) .intro{margin-top:0}',
  'body:has(.human-first-door) .art-hero{width:min(100%,44rem);min-height:0}',
  'body:has(.human-first-door) .hero-heading .hero-title{font:italic 400 clamp(1.2rem,3vw,2rem)/1.1 var(--serif);margin:0;color:inherit}',
  '@media(max-width:690px){.human-first-door{padding:.6rem 0 .8rem}.human-first-door h1{font-size:2.1rem}.human-door-lead{font-size:1.02rem;margin-bottom:.65rem}',
  '.human-door-routes{grid-template-columns:1fr;gap:.28rem;margin:.6rem 0}',
  '.human-door-routes a{min-height:2.9rem;padding:.35rem .65rem;display:flex;justify-content:space-between;align-items:center;gap:.5rem}',
  '.human-door-routes strong{font-size:.95rem}.human-door-routes span{font-size:.75rem;text-align:right}',
  '.human-door-status{font-size:.87rem}.human-door-safety{font-size:.82rem}',
  'body:has(.human-first-door) .art-hero{width:min(100%,22rem)}}'
].join('\n');
