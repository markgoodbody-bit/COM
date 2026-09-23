// Presentation of controlled source pages, not a change to the example.
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#x27;');
const decode = value => value.replaceAll('<br>', '\n').replaceAll('&quot;', '"').replaceAll('&#x27;', "'").replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&amp;', '&');

export function appealPresentation(html, route) {
  const id = route.match(/^explore\/example\/(case|entry|route|affected|challenge)\.html$/)?.[1];
  if (!id) return html;
  const main = html.match(/<main><h1>[^<]+<\/h1>([\s\S]*?)(<nav aria-label="Optional routes">[\s\S]*?<\/nav>)<\/main>/);
  if (!main) throw Error('Appeal template changed');
  const sections = [...main[1].matchAll(/<section><h2>([^<]+)<\/h2><p>([\s\S]*?)<\/p><\/section>/g)];
  if (sections.map(s => s[0]).join('') !== main[1]) throw Error('Unrecognised appeal section');
  const byName = Object.fromEntries(sections.map(s => [s[1], s]));
  const isCase = route.endsWith('/case.html');
  const isView = !['case', 'entry'].includes(id);
  const expected = isView ? ['Case','Lens','Question','Supported by','Reading','Unknowns','Challenge','Stop','Status','Rendering note'] : isCase ? ['Status','Basis','Facts','Unknowns','Boundary','Rendering note'] : ['Status','Provenance','Offer','Shared case','Boundary','Reading boundary','Rendering note'];
  if (JSON.stringify(sections.map(s => s[1])) !== JSON.stringify(expected)) throw Error('Appeal fields changed');
  let content;
  if (isView) {
    const unknowns = JSON.parse(decode(byName.Unknowns[2]));
    if (byName.Case[2] !== 'case.json' || !Array.isArray(unknowns) || unknowns.some(u => typeof u !== 'string')) throw Error('Invalid perspective source');
    content = `<p>${byName.Reading[2]}</p><section><h2>What remains unknown</h2><ul>${unknowns.map(u => `<li>${escape(u)}</li>`).join('')}</ul></section>${byName.Challenge[0]}<p><a href="case.html">Read the shared situation</a></p>`;
  } else if (isCase) {
    const facts = JSON.parse(decode(byName.Facts[2]));
    const unknowns = JSON.parse(decode(byName.Unknowns[2]));
    if (!Array.isArray(facts) || facts.length !== 2 || facts.some((f,i) => f.id !== `F${i+1}` || typeof f.text !== 'string') || !Array.isArray(unknowns) || unknowns.some(u => typeof u !== 'string')) throw Error('Invalid appeal facts');
    content = `<section><h2>The situation</h2>${facts.map(f => `<p>${escape(f.text)}</p>`).join('')}</section><section><h2>What remains unknown</h2><ul>${unknowns.map(u => `<li>${escape(u)}</li>`).join('')}</ul></section>`;
  } else {
    if (byName['Shared case'][2] !== 'case.json') throw Error('Shared case changed');
    content = `<p>${byName.Offer[2]}</p><p><a href="case.html">Read the shared situation and its unknowns</a></p>`;
  }
  // Keep every original source section, including identifiers and provenance,
  // inspectable without putting the serialization before the example.
  const original = `<details class="appeal-source"><summary>Source details and limits</summary>${main[1]}</details>`;
  const title = isView ? byName.Question[2] : isCase ? 'An appeal that comes later' : 'One situation, several viewpoints';
  const formats = `<p><a href="${id}.md">Complete source text</a> · <a href="${id}.json">JSON</a></p>`;
  return html.replace(main[0], `<main><h1>${title}</h1><p class="example-label">Illustrative example</p>${content}${main[2]}${original}${formats}</main>`);
}
