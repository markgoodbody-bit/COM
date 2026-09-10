import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { renderHumanMap } from './human-map.mjs';

const html = await readFile('public/explore/index.html', 'utf8');
const index = JSON.parse(await readFile('public/explore/questions.json', 'utf8'));
const records = Object.fromEntries(await Promise.all(index.nodes.map(async item => [item.id, JSON.parse(await readFile('public/explore/nodes/' + item.id + '.json', 'utf8'))])));

const escape = value => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#x27;');

test('human map derives ten equal question doors and exact authored next questions', () => {
  const rendered = renderHumanMap(html, index, records);
  assert.equal((rendered.match(/data-reading-node=/g) ?? []).length, 10);
  assert.ok(rendered.includes('<h2 id="reading-map-title">Ten questions</h2>'));
  assert.ok(rendered.includes('There is no required order, ranking or preferred route.'));
  for (const item of index.nodes) {
    const record = records[item.id];
    assert.ok(rendered.includes('<li data-reading-node="' + item.id + '">'));
    assert.ok(rendered.includes('<p class="map-topic">' + escape(record.title) + '</p><h3><a'));
    assert.ok(rendered.includes('href="nodes/' + item.id + '.html">' + escape(item.question) + '</a>'));
    const entry = rendered.split('<li data-reading-node="' + item.id + '">')[1].split('</details></li>')[0];
    for (const edge of item.next) {
      const target = index.nodes.find(node => node.id === edge.target);
      assert.ok(target, edge.target);
      assert.ok(entry.includes('data-relation="' + edge.relation + '" href="nodes/' + edge.target + '.html">' + escape(target.question) + '</a>'));
    }
  }
  assert.equal((rendered.match(/data-relation=/g) ?? []).length, 30);
});

test('all eight existing non-node routes survive exactly once and no new interaction machinery appears', () => {
  const rendered = renderHumanMap(html, index, records);
  const original = [...html.matchAll(/<li><a href="([^"]+)">([^<]+)<\/a><\/li>/g)].map(match => ({ href: match[1], label: match[2] }));
  const nodeIds = new Set(index.nodes.map(item => item.id));
  const other = original.filter(link => {
    const match = link.href.match(/^nodes\/([a-z]+)\.html$/);
    return !match || !nodeIds.has(match[1]);
  });
  assert.equal(other.length, 8);
  for (const link of other) {
    const exact = '<li><a href="' + link.href + '">' + link.label + '</a></li>';
    assert.equal(rendered.split(exact).length - 1, 1, link.href);
  }
  assert.doesNotMatch(rendered, /<(?:script|form|input|iframe)\b/);
  assert.equal((rendered.match(/<nav aria-label="Optional routes" tabindex="-1">/g) ?? []).length, 1);
});

test('source, question index and node records must agree; ambiguous source fails closed', () => {
  const wrongQuestion = structuredClone(index);
  wrongQuestion.nodes[0].question += ' changed';
  assert.throws(() => renderHumanMap(html, wrongQuestion, records), /identity disagrees|graph disagrees/);

  const wrongTitle = structuredClone(records);
  wrongTitle.change.title = 'Changed title';
  assert.throws(() => renderHumanMap(html, index, wrongTitle), /identity disagrees/);

  const duplicateNav = html.replace('</main>', '<nav aria-label="Optional routes"><ul></ul></nav></main>');
  assert.throws(() => renderHumanMap(duplicateNav, index, records), /Expected one Explore optional-routes list/);

  const unknownNode = html.replace('nodes/change.html', 'nodes/unknown.html');
  assert.throws(() => renderHumanMap(unknownNode, index, records), /outside the question index/);

  const secondNav = html.replace('</main>', '<nav aria-label="Optional routes">ambiguous</nav></main>');
  assert.throws(() => renderHumanMap(secondNav, index, records), /Expected one Explore/);
  const duplicateRoute = html.replace('<li><a href="questions.txt">', '<li><a href="start.json">');
  assert.throws(() => renderHumanMap(duplicateRoute, index, records), /Duplicate Explore route/);
  assert.throws(() => renderHumanMap(html.replace('nodes/change.html', 'nodes/change.html?extra'), index, records), /Unsupported Explore node/);
  for (const route of ['nodes/change.htm','nodes/change.html?x','nodes/change/']) {
    const withExtra = html.replace('</ul></nav>','<li><a href="'+route+'">Unexpected node</a></li></ul></nav>');
    assert.throws(() => renderHumanMap(withExtra, index, records), /Unsupported Explore node/);
  }
  const duplicateId = structuredClone(index);
  duplicateId.nodes[1].id = duplicateId.nodes[0].id;
  assert.throws(() => renderHumanMap(html, duplicateId, records), /duplicate graph node/);
  const unsafeId = structuredClone(index);
  unsafeId.nodes[0].id = '../change';
  assert.throws(() => renderHumanMap(html, unsafeId, records), /Invalid or duplicate/);
  const wrongEdges = structuredClone(index);
  wrongEdges.nodes[0].next.pop();
  assert.throws(() => renderHumanMap(html, wrongEdges, records), /graph disagrees/);
});

test('final map retains the exact art entrance and all content outside the replaced catalogue', async () => {
  const before = execFileSync('git',['show','89dbc4dbafb64b8af92edaed203a2a59d6311920:explore/index.html']).toString('utf8');
  const after = await readFile('out/explore/index.html','utf8');
  const nav = /<nav id="reading-map" aria-label="Optional routes"[^>]*>[\s\S]*?<\/nav>/;
  assert.equal(after.replace(nav,'<MAP>'),before.replace(nav,'<MAP>'));
  assert.match(after,/<nav id="reading-map" aria-label="Optional routes" tabindex="-1">/);
  const ids = [...after.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(ids.length,new Set(ids).size);
  assert.equal((after.match(/<figure>/g)??[]).length,1);
  assert.equal((after.match(/<details>/g)??[]).length,10);
  for (const item of index.nodes) {
    const room = await readFile('out/explore/nodes/'+item.id+'.html','utf8');
    assert.ok(room.includes(escape(item.question)));
  }
  assert.doesNotMatch(after,/<(?:script|form|input|iframe)\b/);
});
