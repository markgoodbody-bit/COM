import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {addArtRoom, ROOMS} from './contextual-art.mjs';
import {WORKS} from './works.mjs';
import {createHash} from 'node:crypto';

test('five contextual rooms preserve canonical art and share one handoff grammar', async () => {
  assert.equal(ROOMS.length, 5);

  for (const room of ROOMS) {
    const record = JSON.parse(await readFile('public/art/' + room.record + '.json'));
    const images = room.images ? JSON.parse(await readFile('public/art/' + room.images + '.json')) : null;
    const html = await readFile('out/' + room.page, 'utf8');
    const expectedFigures = room.mode === 'views' ? 2 : 1;

    assert.equal((html.match(/<figure>/g) ?? []).length, expectedFigures, room.page);
    assert.ok(html.includes('/works/' + room.work + '/'), room.page);
    assert.ok(html.includes(record.institution), room.page);
    assert.ok(html.includes('href="#' + room.anchor + '"'), room.page);
    const skips = [...html.matchAll(/<a class="skip"[^>]*href="([^"]+)"[^>]*>([^<]+)<\/a>/g)];
    assert.equal(skips.length, 1, room.page + ' must expose one first-action skip link');
    assert.equal(skips[0][1], '#' + room.anchor, room.page);
    assert.ok(html.indexOf('class="skip"') < html.indexOf('class="room-stage'), room.page);
    assert.ok(html.indexOf('class="room-stage') < html.indexOf('class="room-credit"'), room.page);
    assert.ok(html.indexOf('class="room-credit"') < html.indexOf('class="room-heading"'), room.page);
    assert.ok(html.indexOf('class="room-heading"') < html.indexOf('class="room-nav"'), room.page);
    assert.ok(html.indexOf('class="room-nav"') < html.indexOf('id="reading"'), room.page);
    assert.match(html, /This placement is our choice, not the artist's argument or an endorsement/, room.page);
    assert.doesNotMatch(html, /class="room-stage room-stage-pair" style=/, room.page);

    let variants = [];
    if (room.mode === 'legacy') variants = images[0].variants;
    else if (room.mode === 'responsive') variants = images.variants;
    else if (room.mode === 'views') variants = images.flatMap(view => view.variants);
    else if (room.mode === 'direct') variants = [{file:String(record.file).replace(/^\/art\//, '')}];
    else assert.fail('unknown mode: ' + room.mode);

    for (const variant of variants) {
      const route = 'art/' + variant.file;
      const pin = WORKS.files[route];
      assert.ok(pin, 'untracked art route ' + route);
      const bytes = await readFile('out/' + route);
      assert.equal(createHash('sha256').update(bytes).digest('hex'), pin.sha256, route);
      assert.ok(html.includes('/' + route), room.page + ' missing ' + route);
    }

    assert.throws(() => addArtRoom(html, room, record, images), /already present/);
    assert.throws(() => addArtRoom('<body>unexpected shape</body>', room, record, images), /template/);
  }

  const css = await readFile('app/globals.css', 'utf8');
  assert.match(css, /\.room-stage-pair \{ display: grid;/);
  assert.match(css, /\.room-image img \{[^}]*width: auto;[^}]*max-height: 82svh;/s);
  assert.match(css, /\.room-credit \{[^}]*max-width: 52rem;/s);
  assert.doesNotMatch(css, /object-fit: cover/);
});

test('D016 has the same seven paragraphs in Markdown and HTML', async () => {
  const md = (await readFile('public/changes.md', 'utf8')).split('### D016\n\n')[1].split('\n\n### D015')[0].split('\n\n');
  const html = (await readFile('public/changes.html', 'utf8')).split('<h3 id="d016">D016</h3>')[1].split('<h3 id="d015">')[0];
  const paragraphs = [...html.matchAll(/<p>(.*?)<\/p>/g)].map(m => m[1].replaceAll('&amp;', '&').replaceAll('&lt;', '<').replaceAll('&gt;', '>'));
  assert.equal(md.length, 7);
  assert.deepEqual(paragraphs, md);
  assert.ok(html.includes('Opening a door does not submit an answer to the site.'));
  assert.ok(!html.includes('Nothing is submitted or remembered'));
});
