import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { ROOMS } from './contextual-art.mjs';
import { ENABLED_ROOMS } from './change-room.mjs';
import { SUPPORT_READINGS, addReadingNavigation } from './house-style.mjs';
import { appealPresentation } from './appeal-presentation.mjs';

const escape = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#x27;');

test('eight support readings gain direct exits with the declared presentation only', async () => {
  assert.equal(SUPPORT_READINGS.size, 8);
  for (const route of SUPPORT_READINGS) {
    const source = await readFile('public/' + route, 'utf8');
    const output = await readFile('out/' + route, 'utf8');
    assert.equal(output.match(/<main>[\s\S]*?<\/main>/)[0], appealPresentation(source, route).match(/<main>[\s\S]*?<\/main>/)[0]);
    assert.match(output, /class="support-reading"/);
    assert.match(output, /href="\/">Opening<\/a>/);
    assert.match(output, /href="\/explore\/#reading-map">Explore questions<\/a>/);
    assert.throws(() => addReadingNavigation(output, route), /template changed/);
  }
  assert.equal(addReadingNavigation('<body>archive</body>', 'resources/snapshots/example.html'), '<body>archive</body>');
});

test('appeal entry and case keep original sections behind the readable example', async () => {
  for (const id of ['case', 'entry']) {
    const source = await readFile(`public/explore/example/${id}.html`, 'utf8');
    const output = await readFile(`out/explore/example/${id}.html`, 'utf8');
    const details = output.split('<summary>Source details and limits</summary>')[1].split('</details>')[0];
    for (const section of source.matchAll(/<section>[\s\S]*?<\/section>/g)) assert.ok(details.includes(section[0]));
    assert.match(output, /Illustrative example/);
    assert.ok(output.indexOf('aria-label="Optional routes"') < output.indexOf('Source details and limits'));
  }
  const facts = JSON.parse(await readFile('public/explore/example/case.json'));
  const rendered = await readFile('out/explore/example/case.html', 'utf8');
  for (const fact of facts.facts) assert.ok(rendered.includes(`<p>${escape(fact.text)}</p>`));
  for (const unknown of facts.unknowns) assert.ok(rendered.includes(`<li>${escape(unknown)}</li>`));
  assert.throws(() => appealPresentation('<main>changed</main>', 'explore/example/case.html'), /template changed/);
});

test('all ten readings retain their accounts, questions, source links and one title', async () => {
  for (const id of ENABLED_ROOMS) {
    const node = JSON.parse(await readFile(`public/explore/nodes/${id}.json`));
    const html = await readFile(`out/explore/nodes/${id}.html`, 'utf8');
    assert.match(html, /class="reading-room/);
    assert.equal((html.match(/<h1\b/g) || []).length, 1);
    for (const key of ['short', 'detail', 'perspective', 'challenge', 'question', 'boundary']) {
      assert.ok(html.includes(escape(node[key])), `${id}: ${key}`);
    }
    assert.ok(html.includes(`href="${id}.md"`));
    assert.ok(html.includes(`href="${id}.json"`));
    assert.ok(html.indexOf('Sources and other formats') < html.indexOf('>JSON source</a>'));
    for (const edge of node.next) assert.ok(html.includes(`href="${edge.target}.html"`));
  }
});

test('five art entrances retain image metadata and rights without a duplicate title', async () => {
  assert.equal(ROOMS.length, 5);
  for (const room of ROOMS) {
    const html = await readFile(`out/${room.page}`, 'utf8');
    const record = JSON.parse(await readFile(`public/art/${room.record}.json`));
    assert.equal((html.match(/<img\b/g) || []).length, room.mode === 'views' ? 2 : 1);
    assert.ok(html.includes(`href="/works/${room.work}/"`));
    assert.ok(html.includes(`href="#${room.anchor}"`));
    assert.doesNotMatch(html, /class="room-heading"/);
    assert.ok(html.indexOf('<figure>') < html.indexOf('class="room-nav"'));
    assert.match(html, /<details><summary>About this placement<\/summary>/);
    const rights = typeof record.rights === 'string' ? record.rights : (record.rights?.designation ?? record.rights?.label);
    if (rights) assert.ok(html.includes(escape(rights)), room.key + ' rights');
    for (const image of html.matchAll(/<img\b[^>]+>/g)) {
      assert.match(image[0], /width="\d+"/);
      assert.match(image[0], /height="\d+"/);
      assert.match(image[0], /alt="[^"]+"/);
      const width = image[0].match(/width="(\d+)"/)[1];
      assert.ok(image[0].includes(`style="max-width:${width}px"`));
      assert.ok(image[0].includes(`sizes="min(calc(100vw - 2rem), 76rem, ${width}px)"`));
    }
  }
});

test('Explore presents its questions before the preserved orientation', async () => {
  const original = await readFile('public/explore/index.html', 'utf8');
  const html = await readFile('out/explore/index.html', 'utf8');
  const sections = [...original.matchAll(/<section>[\s\S]*?<\/section>/g)].map(m => m[0]);
  assert.equal(sections.length, 6);
  for (const section of sections) {
    assert.ok(html.includes(section));
    assert.ok(html.indexOf(section) > html.indexOf('About this reading space'));
  }
  assert.ok(html.indexOf('id="reading-map"') < html.indexOf('About this reading space'));
  assert.equal((html.match(/data-reading-node=/g) || []).length, 10);
  assert.equal((html.match(/data-relation=/g) || []).length, 30);
});
