import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { ENABLED_ROOMS } from './change-room.mjs';

const textOnly = new Set(['change','care','wisdom','selection','power','correction']);
const artNodes = new Set(['aperture','significance','hardening','futures']);

test('all ten reading rooms use the shared reading-room grammar', async () => {
  assert.equal(ENABLED_ROOMS.length, 10);
  for (const id of ENABLED_ROOMS) {
    const html = await readFile('out/explore/nodes/' + id + '.html', 'utf8');
    assert.match(html, /class="reading-room(?: contextual-room)?"/, id);
    assert.match(html, /class="reading-room-nav"/, id);
    assert.match(html, /class="reading-room-header"/, id);
    assert.match(html, /class="reading-room-counterpoint"/, id);
    assert.match(html, /class="reading-room-detail"/, id);
    assert.match(html, /class="reading-source-links"/, id);
    assert.match(html, /class="reading-room-directions"/, id);
    assert.match(html, /class="reading-room-footer"/, id);
    assert.doesNotMatch(html, /style="/, id);
    assert.ok(html.indexOf('class="reading-room-nav"') < html.indexOf('class="context-window"'), id);
    assert.ok(html.indexOf('class="reading-room-header"') < html.indexOf('id="question"'), id);
    assert.ok(html.indexOf('id="question"') < html.indexOf('class="reading-room-counterpoint"'), id);
  }
});

test('six text-only rooms remain deliberately text-only while four node rooms keep contextual art', async () => {
  assert.equal(textOnly.size, 6);
  assert.equal(artNodes.size, 4);
  for (const id of textOnly) {
    const html = await readFile('out/explore/nodes/' + id + '.html', 'utf8');
    assert.doesNotMatch(html, /class="art-room/, id);
    assert.doesNotMatch(html, /<img\b/, id);
    assert.match(html, /class="reading-room"/, id);
    assert.doesNotMatch(html, /class="reading-room contextual-room"/, id);
  }
  for (const id of artNodes) {
    const html = await readFile('out/explore/nodes/' + id + '.html', 'utf8');
    assert.match(html, /class="reading-room contextual-room"/, id);
    assert.match(html, /class="art-room/, id);
    assert.match(html, /<img\b/, id);
  }
});

test('reading-room presentation preserves node text, authored routes and raw sources', async () => {
  for (const id of ENABLED_ROOMS) {
    const record = JSON.parse(await readFile('public/explore/nodes/' + id + '.json', 'utf8'));
    const html = await readFile('out/explore/nodes/' + id + '.html', 'utf8');
    for (const key of ['title','short','question','perspective','challenge','detail','status','boundary']) {
      const escaped = String(record[key])
        .replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')
        .replaceAll('"','&quot;').replaceAll("'",'&#x27;');
      assert.ok(html.includes(escaped), id + ': ' + key);
    }
    assert.ok(html.includes('href="' + id + '.md"'), id + ': md');
    assert.ok(html.includes('href="' + id + '.json"'), id + ': json');
    for (const edge of record.next) assert.ok(html.includes('href="' + edge.path.replace('.json','.html') + '"'), id + ': ' + edge.path);
    for (const key of record.sources) assert.ok(html.includes(record.source_pointers[key].url), id + ': ' + key);
  }
});

test('shared stylesheet owns reading-room presentation', async () => {
  const css = await readFile('app/globals.css', 'utf8');
  assert.match(css, /body\.reading-room \{ max-width: none; padding: 0; \}/);
  assert.match(css, /body\.reading-room:not\(\.contextual-room\) \.context-window/);
  assert.match(css, /body\.contextual-room > \.reading-room-nav \{ display: none; \}/);
  assert.match(css, /\.reading-room-footer \{/);
});
