import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {addArtRoom, ROOMS} from './contextual-art.mjs';
import {WORKS} from './works.mjs';
import {createHash} from 'node:crypto';

test('two placements use exact canonical work identity and whole-frame delivery copies', async () => {
  assert.equal(ROOMS.length, 2);
  for (const room of ROOMS) {
    const record = JSON.parse(await readFile('public/art/' + room.key + '.json'));
    const images = JSON.parse(await readFile('public/art/' + room.key + '-images.json'));
    const html = await readFile('out/' + room.page, 'utf8');
    assert.equal((html.match(/<figure>/g) ?? []).length, 1);
    assert.ok(html.includes('/works/' + room.work + '/'));
    assert.ok(html.includes(record.credit));
    assert.ok(html.includes(record.rights));
    assert.ok(html.includes('href="#' + room.anchor + '"'));
    assert.ok(html.indexOf('<figure>') < html.indexOf('class="room-nav"'));
    assert.ok(html.indexOf('class="skip"') < html.indexOf('<figure>'));
    assert.ok(html.indexOf('<figure>') < html.indexOf('class="room-heading"'));
    assert.match(html, /This placement is our choice, not the artist's argument or an endorsement/);
    for (const v of images[0].variants) {
      const route = 'art/' + v.file, bytes = await readFile('out/' + route);
      assert.equal(createHash('sha256').update(bytes).digest('hex'), WORKS.files[route].sha256);
      assert.ok(html.includes('/' + route + ' ' + v.width + 'w'));
    }
    assert.throws(() => addArtRoom(html, room, record, images), /already present/);
    assert.throws(() => addArtRoom('<body>unexpected shape</body>', room, record, images), /template/);
  }
  const css = await readFile('app/globals.css', 'utf8');
  assert.match(css, /object-fit: contain/);
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
