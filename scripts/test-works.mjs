import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, mkdtemp, cp, writeFile, readdir, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { WORKS, verifyWorks, copyWorks } from './works.mjs';

test('normal output retains exactly the declared work pages, images and records', async () => {
  assert.equal(WORKS.source_review, 'dfe4b5fcfa279ef08a1d5aac5d3c3a1c59494175');
  const source = await verifyWorks('public'), built = await verifyWorks('out');
  assert.equal(source.size, 36);
  assert.deepEqual(Object.keys(WORKS.files).sort(), Object.keys(WORKS.reviewed_files).sort());
  for (const route of Object.keys(WORKS.files)) if (!route.endsWith('/index.html')) {
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

test('publication treatment changes only the named wrappers from the pinned integration', async () => {
  const integration = 'b078c3cf4aa251c4226985c2547d03e3d88b196a';
  const gitBytes = file => execFileSync('git', ['show', integration + ':' + file], { maxBuffer: 20 * 1024 * 1024 });
  const prior = JSON.parse(gitBytes('scripts/WORKS_COPIES.json'));
  assert.deepEqual(WORKS.reviewed_files, prior.reviewed_files);
  assert.equal(WORKS.source_review, prior.source_review);
  assert.deepEqual(Object.keys(WORKS.files).sort(), Object.keys(prior.files).sort());
  let changed = 0;
  for (const route of Object.keys(prior.files)) {
    const before = gitBytes('public/' + route);
    const after = await readFile('public/' + route);
    if (route.endsWith('/index.html')) {
      const expected = before.toString('utf8')
        .replace(/^[ \t]*<meta name="robots" content="noindex(?:,nofollow)?">\r?\n/gm, '')
        .replace(/^[ \t]*<span>Unpublished work-page proposal<\/span>\r?\n/gm, '')
        .replace(/<meta name="robots" content="noindex(?:,nofollow)?">/g, '')
        .replace('<p>Please Start From Here · Unpublished collection preview</p>', '')
        .replace('Five works selected for this preview,', 'Five selected works,')
        .replace('This is a local review collection, not a published edition. ', '')
        .replace(' · Unpublished preview', '')
        .replace('<span>Unpublished work-page preview</span>', '')
        .replace('<span>Unpublished work-page proposal</span>', '');
      assert.deepEqual(after, Buffer.from(expected), route);
      assert.notDeepEqual(after, before, route);
      changed++;
    } else assert.deepEqual(after, before, route);
  }
  assert.equal(changed, 6);
  assert.match(await readFile('out/works/index.html', 'utf8'), /The works are not endorsements of this project\./);
  assert.match(await readFile('out/404.html', 'utf8'), /noindex/);
  // Homepage layout is now intentionally revised in the human foyer. Its output
  // boundary is checked against the published edition in test-favicon.mjs.
  for (const file of ['scripts/build.mjs']) {
    // These are Git text sources, unlike the byte-pinned Works copies above.
    const source = (await readFile(file, 'utf8')).replace(/\r\n/g, '\n')
      .replace("import { applyContextualArt } from './contextual-art.mjs';\n", '')
      .replace("await applyContextualArt(path.join(root, 'out'), path.join(root, 'public'));\n", '');
    assert.equal(source, gitBytes(file).toString('utf8'), file);
  }
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
