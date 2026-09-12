import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, mkdtemp, cp, writeFile, readdir, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { WORKS, WORKS_D052, verifyWorks, copyWorks } from './works.mjs';

const homerRoute = 'works/winslow-homer/index.html';

test('normal output retains exactly the declared work pages, images and records', async () => {
  assert.equal(WORKS.source_review, 'dfe4b5fcfa279ef08a1d5aac5d3c3a1c59494175');
  assert.equal(WORKS_D052.basis, 'a7c4bec814d677ee8f0b3ffe366a45368302b511');
  const source = await verifyWorks('public'), built = await verifyWorks('out');
  assert.equal(source.size, 37);
  assert.deepEqual(Object.keys(WORKS.files).filter(route => route !== homerRoute).sort(), Object.keys(WORKS.reviewed_files).sort());
  for (const route of Object.keys(WORKS.files)) if (!route.endsWith('/index.html') && route !== 'works/shelf.css') {
    assert.deepEqual(WORKS.files[route], WORKS.reviewed_files[route], route);
  }
  assert.deepEqual(built, source);
  const root = await readFile('out/index.html', 'utf8');
  // D030 adds a direct overview route; the optional Look route survives.
  assert.equal((root.match(/href="\/works\/"/g) ?? []).length, 2);
  assert.equal((root.match(/<figure\b/g) ?? []).length, 1);
  assert.match(root, /camp-fire-1440.jpg/);
  const shelf = built.get('works/index.html').toString('utf8');
  assert.match(shelf, /not a ranking or representative survey/);
  assert.match(shelf, /href="\.\.\/"/);
  assert.equal((shelf.match(/<li>/g) ?? []).length, 6);
  assert.match(shelf, /href="winslow-homer\/index\.html"/);
  assert.match(shelf, /<h2>Camp Fire<\/h2>/);
  const homer = built.get(homerRoute).toString('utf8');
  assert.match(homer, /<h1>Camp Fire<\/h1>/);
  assert.match(homer, /Project response, not artist intention/);
  assert.match(homer, /metmuseum\.org\/art\/collection\/search\/11112/);
  assert.match(homer, /href="\.\.\/\.\.\/art\/camp-fire\.json">Image source and viewing-copy details<\/a>/);
  assert.doesNotMatch(homer, /camp-fire-responsive\.json/);
  await readFile('out/art/camp-fire.json');
  const sitemap = await readFile('out/sitemap.xml', 'utf8');
  assert.equal((sitemap.match(/https:\/\/pleasestartfromhere\.com\/works\/winslow-homer\//g) ?? []).length, 1);
  const manifest = JSON.parse(await readFile('out/manifest.json'));
  assert.equal(manifest.routes.optional_human_art, '/works/');
  assert.equal(manifest.provenance.optional_human_art.optional, true);
  assert.match(manifest.provenance.optional_human_art.scope, /No required traversal or report-back/);
});

test('historical publication treatment changed only named wrappers from the pinned integration', async () => {
  const integration = 'b078c3cf4aa251c4226985c2547d03e3d88b196a';
  const gitBytes = file => execFileSync('git', ['show', integration + ':' + file], { maxBuffer: 20 * 1024 * 1024 });
  const prior = JSON.parse(gitBytes('scripts/WORKS_COPIES.json'));
  assert.deepEqual(WORKS.reviewed_files, prior.reviewed_files);
  assert.equal(WORKS.source_review, prior.source_review);
  assert.deepEqual(Object.keys(WORKS.files).filter(route => route !== homerRoute).sort(), Object.keys(prior.files).sort());
  assert.deepEqual(WORKS.files[homerRoute], WORKS_D052.files[homerRoute]);
  let changed = 0;
  for (const route of Object.keys(prior.files)) {
    const before = gitBytes('public/' + route);
    // Preserve the historical claim against its actual predecessor, not the
    // current art-first presentation. Later changes are checked below.
    const after = execFileSync('git', ['show', '0f627f2357d74de6b1556e25f5e4a0be5c9a7c57:public/' + route], {maxBuffer:20*1024*1024});
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
    // Pin the historical build comparison to its actual revision. The current
    // navigation script and output boundary are tested by test-context-window.
    const source = execFileSync('git', ['show', 'e40cfed5595923bc7f741424152044e485441362:' + file]).toString('utf8').replace(/\r\n/g, '\n')
      .replace("import { applyContextualArt } from './contextual-art.mjs';\n", '')
      .replace("await applyContextualArt(path.join(root, 'out'), path.join(root, 'public'));\n", '');
    assert.equal(source, gitBytes(file).toString('utf8'), file);
  }
});

test('art-first preserves the five prior encounters and adds Homer without changing his image source', async () => {
  const base = '0f627f2357d74de6b1556e25f5e4a0be5c9a7c57';
  const normal = text => text.replace(/\r\n/g, '\n').replace(/>\s+</g, '><').trim();
  const readBefore = route => execFileSync('git', ['show', base + ':public/' + route], {maxBuffer:20*1024*1024});
  const names = ['anna-atkins','shen-zhou','edmonia-lewis','harriet-powers','johannes-vermeer'];
  const moved = new Set(names.map(name => 'works/' + name + '/index.html'));
  for (const route of Object.keys(WORKS.files)) {
    const after = await readFile('public/' + route);
    if (route === homerRoute) {
      const current = after.toString('utf8');
      assert.ok(current.indexOf('<img') < current.indexOf('<header id="work-details"'), route);
      assert.ok(current.indexOf('<img') < current.indexOf('<nav class="shelf-return"'), route);
      assert.match(current, /href="\.\.\/\.\.\/art\/camp-fire\.jpg"/);
      assert.match(current, /camp-fire-720\.jpg 720w/);
      assert.match(current, /camp-fire-1440\.jpg 1440w/);
      assert.match(current, /camp-fire\.jpg 3801w/);
      assert.match(current, /Project response, not artist intention/);
      assert.match(current, /our reading|invitation to begin together without assuming the same view/i);
      continue;
    }
    if (route === 'works/index.html') {
      const current = after.toString('utf8');
      assert.equal((current.match(/<li>/g) ?? []).length, 6);
      assert.match(current, /winslow-homer\/index\.html/);
      assert.doesNotMatch(current, /Five selected works/);
      continue;
    }
    const before = readBefore(route);
    if (moved.has(route)) {
      const old = before.toString('utf8').replace(/\r\n/g, '\n'), current = after.toString('utf8').replace(/\r\n/g, '\n');
      const main = old.match(/<main\b[^>]*>/)[0];
      const heading = old.slice(old.indexOf(main) + main.length).match(/^\s*(<header\b[\s\S]*?<\/header>)/)[1];
      const nav = old.match(/<nav class="shelf-return">[\s\S]*?<\/nav>/)[0];
      const siteHeader = old.match(/<header class="site-header">[\s\S]*?<\/header>/)?.[0] || '';
      assert.ok(current.includes(heading.replace('<header', '<header id="work-details"')), route);
      assert.ok(current.includes(nav), route);
      assert.ok(current.includes(siteHeader), route);
      const stationaryBefore = old.replace(heading,'').replace(nav,'').replace(siteHeader,'');
      const stationaryAfter = current.replace(heading.replace('<header','<header id="work-details"'),'')
        .replace('<nav class="work-routes" aria-label="Continue or leave"><a href="../index.html">All works</a><a href="../../explore/#reading-map">Reading map</a><a href="../../">Back to the opening</a></nav>', '')
        .replace(nav,'').replace(siteHeader,'').replace('<body class="artwork-first">','<body>')
        .replace('class="skip" href="#work-details"','class="skip" href="#work"')
        .replace('>Skip to the account</a>', old.match(/>Skip to the (?:work|painting)<\/a>/)[0]);
      assert.equal(normal(stationaryAfter), normal(stationaryBefore), route);
      assert.ok(current.indexOf('<img') < current.indexOf('<header id="work-details"'), route);
      assert.ok(current.indexOf('<img') < current.indexOf('<nav class="shelf-return"'), route);
      assert.ok(current.includes('href="../../explore/#reading-map"'), route);
    } else if (route === 'works/shelf.css') {
      assert.ok(normal(after.toString()).startsWith(normal(before.toString())));
      assert.match(after.toString(), /max-height: 100svh/);
    } else assert.deepEqual(after, before, route);
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
