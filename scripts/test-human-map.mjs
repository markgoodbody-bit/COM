import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
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
    assert.ok(rendered.includes('<h3>' + escape(record.title) + '</h3>'));
    assert.ok(rendered.includes('href="nodes/' + item.id + '.html">' + escape(item.question) + '</a>'));
    for (const edge of item.next) {
      const target = index.nodes.find(node => node.id === edge.target);
      assert.ok(target, edge.target);
      assert.ok(rendered.includes('data-relation="' + edge.relation + '" href="nodes/' + edge.target + '.html">' + escape(target.question) + '</a>'));
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
  assert.equal((rendered.match(/<nav aria-label="Optional routes">/g) ?? []).length, 1);
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
});
