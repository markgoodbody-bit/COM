import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const pages=['entry','case','route','affected','challenge'];

test('appeal example pages share one case-family presentation', async () => {
  for (const name of pages) {
    const source=await readFile('public/explore/example/'+name+'.html','utf8');
    const built=await readFile('out/explore/example/'+name+'.html','utf8');
    assert.equal(built,source,name);
    assert.match(source, /<body class="case-example">/, name);
    assert.match(source, /class="case-example-nav"/, name);
    assert.match(source, /<main class="case-example-page">/, name);
    assert.match(source, /class="case-example-routes"/, name);
    assert.match(source, /class="case-example-footer"/, name);
    assert.match(source, /<link rel="stylesheet" href="\/style\.css">/, name);
    assert.doesNotMatch(source, /<style>|style="/, name);
    assert.doesNotMatch(source, /<(?:script|form|input|iframe|img)\b/, name);
    assert.ok(source.indexOf('class="case-example-nav"') < source.indexOf('<main class="case-example-page">'), name);
  }
});

test('case family keeps shared facts and optional perspective routes', async () => {
  const entry=await readFile('out/explore/example/entry.html','utf8');
  assert.match(entry,/One situation, several ways to inspect it/);
  for (const route of ['route.html','affected.html','challenge.html']) assert.ok(entry.includes('href="'+route+'"'),route);

  const route=await readFile('out/explore/example/route.html','utf8');
  const affected=await readFile('out/explore/example/affected.html','utf8');
  const challenge=await readFile('out/explore/example/challenge.html','utf8');
  for (const [name,html] of [['route',route],['affected',affected],['challenge',challenge]]) {
    assert.match(html,/An appeal route formally exists|case\.json/,name);
    assert.ok(html.includes('href="case.html"'),name);
    assert.ok(html.includes('href="entry.html"'),name);
  }
  assert.ok(route.includes('href="affected.html"'));
  assert.ok(route.includes('href="challenge.html"'));
  assert.ok(affected.includes('href="route.html"'));
  assert.ok(affected.includes('href="challenge.html"'));
  assert.ok(challenge.includes('href="route.html"'));
  assert.ok(challenge.includes('href="affected.html"'));
});

test('case-family stylesheet remains quiet and responsive', async () => {
  const css=await readFile('app/globals.css','utf8');
  assert.match(css,/body\.case-example \{ max-width: none; padding: 0; \}/);
  assert.match(css,/\.case-example-page > section \{/);
  assert.match(css,/\.case-example-routes ul \{[^}]*grid-template-columns: repeat\(2,minmax\(0,1fr\)\)/s);
  assert.match(css,/@media \(max-width: 40rem\)[\s\S]*\.case-example-routes ul \{ grid-template-columns: 1fr; \}/);
});
