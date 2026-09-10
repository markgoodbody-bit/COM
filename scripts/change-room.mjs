import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';

const escape = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#x27;');
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const localHtml = route => route.replace(/\.(?:json|md)$/, '.html');
const ROOM_IDS = new Set(['change', 'aperture']);

function semanticExit(node) {
  if (node.id === 'change') return '<a href="/#step-understand">Understand route</a>';
  return '';
}

// Two-node presentation proof over the existing graph. Raw sources and every
// other node remain unchanged; adding another room requires an explicit edit.
export function renderReadingRoom(node, index, targets) {
  if (!ROOM_IDS.has(node.id)) throw Error('Only Change and Partial views proofs are enabled');
  for (const key of ['title','short','detail','perspective','challenge','question','kind','status','boundary']) {
    if (typeof node[key] !== 'string' || !node[key].trim()) throw Error(`Missing ${node.id} field: ${key}`);
  }
  const indexed = index.nodes.filter(item => item.id === node.id);
  if (indexed.length !== 1 || indexed[0].question !== node.question) throw Error('Question index disagrees');
  const expectedEdges = node.next.map(edge => ({...edge, path: 'nodes/' + edge.path}));
  if (JSON.stringify(indexed[0].next) !== JSON.stringify(expectedEdges)) throw Error('Graph edges disagree');
  const moves = node.next.map(edge => {
    if (!/^[a-z_]+$/.test(edge.relation) || edge.path !== edge.target + '.json' || !/^[a-z]+$/.test(edge.target)) throw Error('Unsafe graph edge');
    const target = targets[edge.target];
    if (!target || target.id !== edge.target || typeof target.title !== 'string' || typeof target.question !== 'string' || !target.question.trim()) throw Error('Missing edge target');
    const verb = edge.relation.replaceAll('_', ' ');
    const label = verb[0].toUpperCase() + verb.slice(1) + ': ' + target.title;
    return `<a data-relation="${escape(edge.relation)}" href="${escape(localHtml(edge.path))}" title="${escape(label)}">${escape(target.question)}</a>`;
  }).join('\n');
  const sources = node.sources.map(key => {
    const source = node.source_pointers[key];
    if (!source || !source.url.startsWith('https://github.com/')) throw Error('Missing source pointer');
    return `<li><a href="${escape(source.url)}">${escape(source.label)}</a></li>`;
  }).join('\n');
  const stem = escape(node.id);
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(node.title)} · Please Start From Here</title><link rel="stylesheet" href="/style.css"><link rel="alternate" type="text/markdown" href="${stem}.md"><link rel="alternate" type="application/json" href="${stem}.json"><link rel="describedby" href="../llms.txt"></head>
<body style="max-width:none;padding:0"><a class="skip" href="#question">Skip to the question</a>
<main><article class="context-window" aria-labelledby="room-title">
<header><h1 id="room-title" style="margin-top:0">${escape(node.title)}</h1><p>${escape(node.short)}</p></header>
<h2 id="question" tabindex="-1">${escape(node.question)}</h2>
<div aria-label="Another position and challenge">
<h3>Another position</h3><p>${escape(node.perspective)}</p>
<h3>Challenge</h3><p>${escape(node.challenge)}</p></div>
<details id="full-account"><summary style="padding:.75rem 0;cursor:pointer">Read the full account</summary>
<h3>Expand</h3><p>${escape(node.detail)}</p>
<h3>Status</h3><p>${escape(node.kind)}. ${escape(node.boundary)}</p></details>
<p><a href="${stem}.md">Complete text</a> · <a href="${stem}.json">JSON source</a></p>
<nav aria-label="Optional directions"><h3>If you want to follow this further</h3><div class="journey-options">${moves}</div></nav>
<nav class="journey-exits" aria-label="Return or stop">${semanticExit(node)}<a href="/">Opening</a><a href="/explore/#reading-map">Map</a><a href="/#step-leave">Not now</a></nav>
<details><summary style="padding:.75rem 0;cursor:pointer">Sources and other routes</summary><ul>${sources}
<li><a href="${escape(localHtml(node.routes.sources))}">Source terms and snapshots</a></li>
<li><a href="${escape(localHtml(node.routes.example))}">Same facts, different views</a></li>
<li><a href="${escape(localHtml(node.routes.challenge_access))}">Challenge the account or the route</a></li>
<li><a href="${escape(node.routes.map)}">Source map (JSON)</a></li></ul></details>
</article></main><footer style="max-width:48rem;margin-inline:auto;padding-inline:1rem">${escape(node.status)}. Same source as the machine representations. No sign-in, personal disclosure or report-back is needed.</footer></body></html>\n`;
}

// Compatibility export for existing focused consumers during the two-room proof.
export const renderChangeRoom = renderReadingRoom;

async function loadRoom(sourceRoot, index, id) {
  const nodePath = path.join(sourceRoot, 'explore/nodes', id + '.json');
  const nodeBytes = await readFile(nodePath);
  const node = JSON.parse(nodeBytes), targets = {};
  for (const edge of node.next) {
    if (!/^[a-z]+\.json$/.test(edge.path)) throw Error('Unsafe target path');
    targets[edge.target] = JSON.parse(await readFile(path.join(sourceRoot, 'explore/nodes', edge.path)));
  }
  return { id, node, nodeBytes, html: renderReadingRoom(node, index, targets) };
}

export async function writeChangeRoom(sourceRoot, outputRoot) {
  const indexBytes = await readFile(path.join(sourceRoot, 'explore/questions.json'));
  const index = JSON.parse(indexBytes);
  const rooms = [];
  for (const id of ROOM_IDS) {
    const room = await loadRoom(sourceRoot, index, id);
    await writeFile(path.join(outputRoot, 'explore/nodes', id + '.html'), room.html);
    rooms.push(room);
  }
  const manifestPath = path.join(outputRoot, 'manifest.json');
  const manifest = JSON.parse(await readFile(manifestPath));
  const change = rooms.find(room => room.id === 'change');
  const aperture = rooms.find(room => room.id === 'aperture');
  manifest.provenance.change_room = {
    direction: 'https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5618521193',
    node: '/explore/nodes/change.json', node_sha256: sha(change.nodeBytes),
    graph: '/explore/questions.json', graph_sha256: sha(indexBytes),
    scope: 'Change-only presentation proof. Existing account and graph, no new semantics or measured reader benefit. Raw sources remain directly reachable.',
  };
  manifest.provenance.aperture_room = {
    direction: 'https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5618750426',
    node: '/explore/nodes/aperture.json', node_sha256: sha(aperture.nodeBytes),
    graph: '/explore/questions.json', graph_sha256: sha(indexBytes),
    scope: 'Second-room transition proof for Partial views. Existing account and graph, no new semantics or measured reader benefit. Raw sources remain directly reachable.',
  };
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
}
