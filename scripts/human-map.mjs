import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const escape = value => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#x27;');

const NAV_RE = /<nav aria-label="Optional routes"><ul>([\s\S]*?)<\/ul><\/nav>/g;
const ITEM_RE = /<li><a href="([^"]+)">([^<]+)<\/a><\/li>/g;

function simpleLinks(markup) {
  const matches = [...markup.matchAll(ITEM_RE)];
  if (matches.map(match => match[0]).join('') !== markup) throw Error('Explore route list is no longer a simple link list');
  return matches.map(match => ({ html: match[0], href: match[1], label: match[2] }));
}

export function renderHumanMap(html, index, records) {
  const navs = [...html.matchAll(NAV_RE)];
  if (navs.length !== 1) throw Error('Expected one Explore optional-routes list');
  if (!index || !Array.isArray(index.nodes) || index.nodes.length !== 10) throw Error('Expected ten graph nodes');

  const ids = index.nodes.map(node => node.id);
  if (new Set(ids).size !== ids.length || ids.some(id => !/^[a-z]+$/.test(id))) throw Error('Invalid or duplicate graph node id');
  const idSet = new Set(ids);
  const links = simpleLinks(navs[0][1]);
  const nodeLinks = new Map();
  const otherLinks = [];

  for (const link of links) {
    const match = link.href.match(/^nodes\/([a-z]+)\.html$/);
    if (!match) { otherLinks.push(link); continue; }
    const id = match[1];
    if (!idSet.has(id)) throw Error('Explore contains a node route outside the question index: ' + id);
    if (nodeLinks.has(id)) throw Error('Duplicate Explore node route: ' + id);
    nodeLinks.set(id, link);
  }
  if (nodeLinks.size !== ids.length) throw Error('Explore node routes do not cover the question index');

  const byId = Object.fromEntries(index.nodes.map(node => [node.id, node]));
  const items = index.nodes.map(item => {
    const record = records[item.id];
    const link = nodeLinks.get(item.id);
    if (!record || record.id !== item.id || record.title !== link.label || record.question !== item.question) {
      throw Error('Explore/question/node identity disagrees: ' + item.id);
    }
    if (!Array.isArray(item.next) || !Array.isArray(record.next) || JSON.stringify(item.next) !== JSON.stringify(record.next.map(edge => ({ ...edge, path: 'nodes/' + edge.path })))) {
      throw Error('Question graph disagrees with node source: ' + item.id);
    }
    const fromHere = item.next.map(edge => {
      if (!/^[a-z_]+$/.test(edge.relation) || edge.path !== 'nodes/' + edge.target + '.json') throw Error('Unsafe map edge: ' + item.id);
      const target = byId[edge.target];
      if (!target) throw Error('Missing map edge target: ' + edge.target);
      return `<li><a data-relation="${escape(edge.relation)}" href="nodes/${escape(edge.target)}.html">${escape(target.question)}</a></li>`;
    }).join('');
    return `<li data-reading-node="${escape(item.id)}"><h3>${escape(record.title)}</h3><p><a href="nodes/${escape(item.id)}.html">${escape(item.question)}</a></p><details><summary>From here</summary><ul>${fromHere}</ul></details></li>`;
  }).join('');

  const replacement = `<nav aria-label="Optional routes"><section aria-labelledby="reading-map-title"><h2 id="reading-map-title">Ten questions</h2><p>Choose whichever question helps. There is no required order, ranking or preferred route.</p><ul class="reading-map-list">${items}</ul></section><section aria-labelledby="other-routes-title"><h2 id="other-routes-title">Other routes</h2><ul>${otherLinks.map(link => link.html).join('')}</ul></section></nav>`;
  return html.replace(navs[0][0], replacement);
}

export async function writeHumanMap(sourceRoot, outputRoot) {
  const index = JSON.parse(await readFile(path.join(sourceRoot, 'explore/questions.json'), 'utf8'));
  const records = {};
  for (const item of index.nodes) records[item.id] = JSON.parse(await readFile(path.join(sourceRoot, 'explore/nodes', item.id + '.json'), 'utf8'));
  const file = path.join(outputRoot, 'explore/index.html');
  const html = await readFile(file, 'utf8');
  await writeFile(file, renderHumanMap(html, index, records));
}
