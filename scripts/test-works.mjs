import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, mkdtemp, cp, writeFile, readdir, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { WORKS, verifyWorks, copyWorks } from './works.mjs';

test('normal output retains exactly the declared work pages, images and records', async () => {
  assert.equal(WORKS.source_review, 'dfe4b5fcfa279ef08a1d5aac5d3c3a1c59494175');
  const source = await verifyWorks('public'), built = await verifyWorks('out');
  assert.equal(source.size, 36);
  assert.deepEqual(Object.keys(WORKS.files).sort(), Object.keys(WORKS.reviewed_files).sort());
  for (const route of Object.keys(WORKS.files)) if (route !== 'works/index.html') {
    assert.deepEqual(WORKS.files[route], WORKS.reviewed_files[route], route);
  }
  assert.deepEqual(built, source);
  const root = await readFile('out/index.html', 'utf8');
  assert.equal((root.match(/href="\/works\/"/g) ?? []).length, 1);
  assert.equal((root.match(/<figure\b/g) ?? []).length, 1);
  assert.match(root, /camp-fire-1440.jpg/);
  const shelf = built.get('works/index.html').toString('utf8');
  assert.match(shelf, /not a ranking or representative survey/);
  assert.match(shelf, /href="\.\.\/"/);
  assert.equal((shelf.match(/<li>/g) ?? []).length, 5);
  const manifest = JSON.parse(await readFile('out/manifest.json'));
  assert.equal(manifest.routes.optional_human_art, '/works/');
  assert.equal(manifest.provenance.optional_human_art.optional, true);
  assert.match(manifest.provenance.optional_human_art.scope, /No required traversal or report-back/);
});

test('a changed record fails before the copier writes any output', async () => {
  const temp = await mkdtemp(path.join(tmpdir(), 'psfh-works-custody-'));
  try {
    const source = path.join(temp, 'input'), output = path.join(temp, 'output');
    await cp('public/works', path.join(source, 'works'), { recursive: true });
    await cp('public/art', path.join(source, 'art'), { recursive: true });
    await writeFile(path.join(source, 'art/atkins.json'), '{}');
    await assert.rejects(copyWorks(source, output), /identity mismatch/);
    await assert.rejects(readdir(output), { code: 'ENOENT' });
  } finally {
    assert.equal(path.dirname(temp), path.resolve(tmpdir()));
    assert.ok(path.basename(temp).startsWith('psfh-works-custody-'));
    await rm(temp, { recursive: true });
  }
});
