import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { WORKS_D080, verifyWorks } from './works.mjs';

test('D080 Works source and built output match the declared custody set', async () => {
  assert.equal(WORKS_D080.basis, 'eafaf40e83d723e577a8cb78469a95946c334edd');
  const source = await verifyWorks('public');
  const built = await verifyWorks('out');
  assert.equal(source.size, built.size);
  assert.equal(source.size, 37);
  for (const [route, bytes] of source) assert.deepEqual(built.get(route), bytes, route);
});

test('D080 dedicated work pages use one active gallery grammar', async () => {
  const shelf = await readFile('public/works/shelf.css', 'utf8');
  assert.match(shelf, /\.shelf \.image-space \{ aspect-ratio: 4 \/ 3;/);
  assert.match(shelf, /max-height: calc\(100svh - clamp/);
  assert.match(shelf, /\.work-page \.context, \.work-page \.museum-note, \.work-page \.reading/);

  const collection = await readFile('public/works/index.html', 'utf8');
  assert.equal((collection.match(/<li>/g) ?? []).length, 6);
  assert.match(collection, /complete available image before our text/);

  const names = ['harriet-powers','johannes-vermeer','anna-atkins','shen-zhou','edmonia-lewis','winslow-homer'];
  for (const name of names) {
    const route = 'public/works/' + name + '/index.html';
    const page = await readFile(route, 'utf8');
    assert.match(page, /<body class="artwork-first">/, route);
    assert.match(page, /<main id="work" class="work-page(?: [^"]+)?">/, route);
    assert.match(page, /<link rel="stylesheet" href="\.\.\/shelf\.css">/, route);
    assert.doesNotMatch(page, /href="(?:\.\/)?work\.css"/, route);
    assert.ok(page.indexOf('<img') < page.indexOf('id="work-details"'), route);
    assert.ok(page.indexOf('<img') < page.indexOf('<nav class="shelf-return"'), route);
    assert.match(page, /<nav class="work-routes" aria-label="Continue or leave">/, route);
    assert.match(page, /href="\.\.\/\.\.\/explore\/#reading-map"/, route);
    assert.match(page, /href="\.\.\/\.\.\/">Back to the opening<\/a>/, route);
  }

  const powers = await readFile('public/works/harriet-powers/index.html', 'utf8');
  assert.match(powers, /The maker's recorded account/);
  assert.match(powers, /eleven subjects/);
  const vermeer = await readFile('public/works/johannes-vermeer/index.html', 'utf8');
  assert.match(vermeer, /At the museum/);
  const cleopatra = await readFile('public/works/edmonia-lewis/index.html', 'utf8');
  assert.equal((cleopatra.match(/<figure>/g) ?? []).length, 2);
  const homer = await readFile('public/works/winslow-homer/index.html', 'utf8');
  assert.match(homer, /Project response, not artist intention/);
});
