import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const proposals = path.join(root, 'proposals');

const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const requireValue = (ok, message) => { if (!ok) throw new Error(message); };
const e = value => String(value)
  .replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;').replaceAll("'", '&#x27;');

const expected = {
  powers: {
    html: 'c388ce783d9a5198204a4aa1a1d1cf8fffd8038803fbbb5b1d6eaa4db46ac472',
    css: 'e75f79f1a0bd04380fbcda400ce76dcad023cf6ee34a15ffd3ef4b38839ae773',
    record: 'b513b49ac8a4003f66e2f7ed5e6d5471525c9287a2a0072d888f66f3f4147a09',
    responsive: 'c92839a5243f67eedda8197f47425b6c338182f09e455848a07cc6bc7a3bdc7b',
    acquisition: 'b0593fbb2ed82f7ab621eb0f71865c731b5ae2158f4269c46ab7045bb4f1fd22',
  },
  vermeer: {
    html: '16375d4cbccd1591015cd89818d01450b0877f4714707458f07cad0007bacedd',
    css: 'd825fe3c487103a463497f871fdd5d44e3622e6cf8abcf6c589c0722add2877a',
    record: '847f2aeadd89289cc8160353485bc1202933b4bc51da1dcb3fd07c5868fc7293',
    acquisition: '2740dd8d2284044f17415db2f08f6edeb7b7b2f9d9df2b6327c9500724540867',
  },
  atkins: {
    html: '4b287a3560b72bed607581a2d7865bf90e11091648ec4cc0307858995632177a',
    record: 'b4f7169bd8b0d9cbf8451ff729671efcc6b7befcc997a2aca8bddb3ad4519537',
    images: '46ba4513922878cbdb8beee4fd795dc198b209cdbe56dbbd9485a3ae26a40609',
  },
  shen: {
    html: 'def115614cfef6c4011ac3a35777d819d587b768ee06520dfe958936fa10e06a',
    record: '3d51bad571ee18945f74f16bee7e639bc27332e2a9ad01c62ef70847e83f503f',
    images: '220425096232b578e002cc51eacff6938335dc705f54a77e790d22f889d3109c',
  },
  lewis: {
    html: 'b7d7f55f53c08707b8b22da5bee1004442c4824fde9189c8486c8c2141a4efac',
    record: '3970ecc6db3a9f5b39cdd33679e2487eaf17b7bc0591ba546b54bbe58baef211',
    images: '05c808d154529f5d7953877003a81682043a735c24564c61f10631d4992b2c8f',
  },
  shelfCss: 'b3ea5b5c1d3a05e7adab591890703ccd98f3a4d2bfd87b8a64798f3df26fb0ab',
};

const identities = {
  atkins: ['Anna Atkins', 'Ulva lactuca', '291638'],
  shen: ['Shen Zhou', 'Anchorage on a rainy night', '49549'],
  lewis: ['Edmonia Lewis', 'The Death of Cleopatra', 'saam_1994.17'],
};

const outputs = new Map();
function put(route, data) {
  const bytes = Buffer.isBuffer(data) ? data : Buffer.from(data, 'utf8');
  requireValue(!outputs.has(route), `Works route collision: ${route}`);
  outputs.set(route, bytes);
}
async function sourceBytes(...parts) { return readFile(path.join(proposals, ...parts)); }
async function sourceText(...parts) { return readFile(path.join(proposals, ...parts), 'utf8'); }
function pin(bytes, digest, label, count = null) {
  if (count !== null) requireValue(bytes.length === count, `${label} byte count changed`);
  requireValue(sha(bytes) === digest, `${label} SHA-256 changed`);
}

function withShelfNavigation(html) {
  requireValue(html.includes('</head>') && html.includes('<main '), 'Work page source structure changed');
  return html.replace('</head>', '<link rel="stylesheet" href="../shelf.css"></head>')
    .replace('<main ', '<nav class="shelf-return"><a href="../index.html">All works</a></nav><main ');
}

async function powers() {
  const recordBytes = await sourceBytes('powers', 'artwork.json');
  const responsiveBytes = await sourceBytes('powers', 'responsive.json');
  const acquisitionBytes = await sourceBytes('powers', 'acquisition.json');
  const css = await sourceBytes('powers', 'work.css');
  pin(recordBytes, expected.powers.record, 'Powers work record');
  pin(responsiveBytes, expected.powers.responsive, 'Powers responsive record');
  pin(acquisitionBytes, expected.powers.acquisition, 'Powers acquisition record');
  pin(css, expected.powers.css, 'Powers work CSS');
  const record = JSON.parse(recordBytes);
  requireValue(record.creator === 'Harriet Powers' && record.title === 'Bible Quilt', 'Powers identity changed');
  requireValue(record.maker_recorded_title === 'Adam and Eve in the Garden of Eden', 'Powers maker-recorded title changed');
  requireValue(record.master_status === 'UNKNOWN' && record.source_tier?.master_status === 'UNKNOWN', 'Powers master claim changed');
  requireValue(record.creator_account?.panel_subjects?.length === 11, 'Powers panel account incomplete');
  requireValue(record.creator_account?.statement?.includes('insisted'), 'Powers agency wording lost');
  requireValue(typeof record.project_response?.text === 'string' && record.project_response.text.length > 0, 'Powers labelled project response missing');

  const files = [
    ['assets/bible-quilt-delivered.jpg', 'art/bible-quilt-delivered.jpg', 'fd8280dd502f0fb21c4c030f9a018560d1928fe66a671edfccaadf9a13b0197d', 2671829],
    ['assets/bible-quilt-720.jpg', 'art/bible-quilt-720.jpg', 'c424b6927b35b4546850b317a303699cad952d1852d1e9c6d77dc246e29ba802', 201415],
    ['assets/bible-quilt-1440.jpg', 'art/bible-quilt-1440.jpg', '816b56a1f0f650c882fa151b7c30d0a6e5d32fe218a70bfee675004b9bb9c59f', 862531],
  ];
  for (const [source, route, digest, count] of files) {
    const bytes = await sourceBytes('powers', ...source.split('/'));
    pin(bytes, digest, `Powers ${source}`, count); put(route, bytes);
  }
  put('works/harriet-powers/work.css', css);
  put('art/harriet-powers.json', recordBytes);
  put('art/harriet-powers-responsive.json', responsiveBytes);
  put('art/harriet-powers-acquisition.json', acquisitionBytes);
  const html = withShelfNavigation(await sourceText('powers', 'index.html'));
  pin(Buffer.from(html), expected.powers.html, 'Powers emitted HTML');
  requireValue(html.indexOf("The maker's recorded account") < html.indexOf('Our response · PSFH'), 'Powers source order changed');
  put('works/harriet-powers/index.html', html);
}

async function vermeer() {
  const recordBytes = await sourceBytes('vermeer', 'artwork.json');
  const acquisitionBytes = await sourceBytes('vermeer', 'acquisition.json');
  const css = await sourceBytes('vermeer', 'work.css');
  pin(recordBytes, expected.vermeer.record, 'Vermeer work record');
  pin(acquisitionBytes, expected.vermeer.acquisition, 'Vermeer acquisition record');
  pin(css, expected.vermeer.css, 'Vermeer work CSS');
  const record = JSON.parse(recordBytes);
  requireValue(record.creator === 'Johannes Vermeer' && record.title === 'The Geographer', 'Vermeer identity changed');
  requireValue(record.project_response === null, 'Vermeer project response must remain null');
  requireValue(record.master_status === 'UNKNOWN', 'Vermeer master status changed');
  requireValue(record.later_source_report?.reported_zoom_extent?.join('x') === '16557x18526', 'Vermeer higher-resolution viewer report lost');
  const image = await sourceBytes('vermeer', 'assets', 'staedel-1149-thumb-xl.jpg');
  pin(image, '2eb8819e4afe22c219d7fbd01766e41338c5fbe460d0d41c250f8c698fd39106', 'Vermeer image', 147792);
  put('art/staedel-1149-thumb-xl.jpg', image);
  put('art/vermeer.json', recordBytes);
  put('art/vermeer-acquisition.json', acquisitionBytes);
  put('works/johannes-vermeer/work.css', css);
  const html = withShelfNavigation(await sourceText('vermeer', 'index.html'));
  pin(Buffer.from(html), expected.vermeer.html, 'Vermeer emitted HTML');
  requireValue(html.includes('tier acquired for this preview, not a limit on what the museum offers'), 'Vermeer acquired-tier disclosure lost');
  put('works/johannes-vermeer/index.html', html);
}

function imageHtml(view, alt, width) {
  const last = view.variants.at(-1);
  const srcset = view.variants.map(v => `../../art/${v.file} ${v.width}w`).join(', ');
  return `<a href="../../art/${e(view.parent_file)}"><img src="../../art/${e(last.file)}" srcset="${e(srcset)}" sizes="(max-width: ${width + 32}px) calc(100vw - 32px), ${width}px" width="${last.width}" height="${last.height}" alt="${e(alt)}"></a>`;
}

function renderWork(work, slug, kind, record, views) {
  const credit = `<p>${e(record.institution)}. ${e(record.credit)}. ${e(record.accession)}.</p><p><a href="${e(record.object_url)}">Museum record</a> · ${e(record.rights)}</p>`;
  let art;
  if (kind === 'sculpture') {
    art = '<div class="views">' + views.map((view, i) => `<figure>${imageHtml(view, record.alts[i], 578)}<figcaption class="view-label">Museum view ${i + 1} · ${e(view.source.view_id)}</figcaption></figure>`).join('') + '</div><div class="credit">' + credit + '<p>Two photographs of one sculpture. Open either image for its unchanged museum file. These are not all possible views.</p></div>';
  } else {
    art = `<figure>${imageHtml(views[0], record.alt, work === 'atkins' ? 720 : 600)}<figcaption>${credit}</figcaption></figure>`;
  }
  let context = '';
  if (work === 'atkins') context = `<section class="context"><p>From <cite>${e(record.book)}</cite>.</p><p>The supplied photograph includes the page and book edges. They are retained here.</p></section>`;
  if (work === 'shen') context = `<section class="context"><h2>Painting and inscription</h2><p>${e(record.museum_account)}</p><p><a href="${e(record.object_url)}">Read the poem and museum account</a></p><p>The complete supplied photograph is retained, including the pictured inscriptions. It is not a claim to show every part of the physical mounting.</p></section>`;
  const info = `<details><summary>Source and viewing copies</summary><p>Smaller full-frame viewing copies are shown; the unchanged museum files remain linked from the images. No crop, retouch or generated view. Museum-master status is unknown.</p><p><a href="../../art/${work}-images.json">Image identities and preparation</a> · <a href="../../art/${work}.json">Work record</a></p></details>`;
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${e(record.title)} · ${e(record.creator)}</title><link rel="stylesheet" href="../shelf.css"></head><body><a class="skip" href="#work">Skip to the work</a><nav class="shelf-return"><a href="../index.html">All works</a> · Unpublished preview</nav><main id="work" class="work-page ${kind}"><header><p>${e(record.creator)}</p><h1>${e(record.title)}</h1><p>${e(record.date)} · ${e(record.medium)}</p></header>${art}${context}${info}</main></body></html>`;
}

async function newWork(work, slug, kind) {
  const recordBytes = await sourceBytes(work, 'artwork.json');
  const imagesBytes = await sourceBytes(work, 'images.json');
  pin(recordBytes, expected[work].record, `${work} record`);
  pin(imagesBytes, expected[work].images, `${work} image record`);
  const record = JSON.parse(recordBytes), views = JSON.parse(imagesBytes);
  const [creator, title, objectId] = identities[work];
  requireValue(record.creator === creator && record.title === title && record.object_id === objectId, `${work} identity changed`);
  requireValue(record.master_status === 'UNKNOWN' && record.project_response === null, `${work} value/source ceiling changed`);
  for (const view of views) {
    const all = [{ ...view.source, file: view.parent_file }, ...view.variants];
    for (const item of all) {
      const bytes = await sourceBytes(work, 'assets', item.file);
      pin(bytes, item.sha256, `${work} ${item.file}`, item.bytes); put(`art/${item.file}`, bytes);
    }
    requireValue(view.variants.every(v => v.parent_sha256 === view.source.sha256), `${work} derivative detached from source`);
  }
  put(`art/${work}.json`, recordBytes); put(`art/${work}-images.json`, imagesBytes);
  const html = renderWork(work, slug, kind, record, views);
  pin(Buffer.from(html), expected[work].html, `${work} emitted HTML`);
  put(`works/${slug}/index.html`, html);
  return { record, views };
}

function references(html) {
  const refs = [];
  for (const match of html.matchAll(/\b(?:href|src)="([^"]+)"/g)) refs.push(match[1]);
  for (const match of html.matchAll(/\bsrcset="([^"]+)"/g)) for (const item of match[1].split(',')) refs.push(item.trim().split(/\s+/)[0]);
  return refs;
}
function resolveLocal(route, ref) {
  if (ref.startsWith('#') || ref.startsWith('https://') || ref.startsWith('http://')) return null;
  if (ref.startsWith('/')) return ref.slice(1).replace(/\/$/, '/index.html');
  const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(route), ref));
  return resolved.endsWith('/') ? resolved + 'index.html' : resolved;
}

export async function copyWorks(outRoot) {
  outputs.clear();
  await powers(); await vermeer();
  const atkins = await newWork('atkins', 'anna-atkins', 'cyanotype');
  const shen = await newWork('shen', 'shen-zhou', 'scroll');
  const lewis = await newWork('lewis', 'edmonia-lewis', 'sculpture');

  const shelfCss = await sourceBytes('works', 'shelf.css');
  pin(shelfCss, expected.shelfCss, 'Works shelf CSS'); put('works/shelf.css', shelfCss);
  const entries = [
    { creator: 'Harriet Powers', title: 'Bible Quilt', date: '1885–1886', medium: 'Quilt / textile', slug: 'harriet-powers', image: 'bible-quilt-720.jpg', width: 720, height: 603 },
    { creator: 'Johannes Vermeer', title: 'The Geographer', date: '1669', medium: 'Oil on canvas', slug: 'johannes-vermeer', image: 'staedel-1149-thumb-xl.jpg', width: 915, height: 1024 },
    ...[['atkins', 'anna-atkins', atkins], ['shen', 'shen-zhou', shen], ['lewis', 'edmonia-lewis', lewis]].map(([work, slug, data]) => {
      const thumb = data.views[0].variants[0];
      return { creator: data.record.creator, title: data.record.title, date: data.record.date, medium: data.record.medium, slug, image: thumb.file, width: thumb.width, height: thumb.height };
    }),
  ];
  const cards = entries.map(x => `<li><a href="${x.slug}/index.html"><div class="image-space"><img src="../art/${x.image}" width="${x.width}" height="${x.height}" alt="" loading="lazy"></div><p class="maker">${e(x.creator)}</p><h2>${e(x.title)}</h2><p class="medium">${e(x.date)} · ${e(x.medium)}</p></a></li>`).join('');
  const shelf = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Works · Please Start From Here</title><link rel="stylesheet" href="shelf.css"></head><body><main class="collection"><header><p>Please Start From Here · Unpublished collection preview</p><h1>Works</h1><p>Five works selected for this preview. A project-curated starting shelf, not a ranking or representative canon. Each opens onto its own page and museum record.</p></header><ul class="shelf">${cards}</ul><footer>This is a local review collection, not a published edition. The works are not endorsements of this project.</footer></main></body></html>`;
  requireValue(shelf.includes('not a ranking or representative canon'), 'Works selection aperture disclosure missing');
  put('works/index.html', shelf);

  requireValue(outputs.size === 36, `Expected 36 works routes, got ${outputs.size}`);
  for (const [route, bytes] of outputs) {
    if (!route.endsWith('.html')) continue;
    const html = bytes.toString('utf8');
    requireValue(!/<(?:script|form|iframe)\b/i.test(html), `Active content in ${route}`);
    for (const ref of references(html)) {
      const target = resolveLocal(route, ref);
      if (target) requireValue(outputs.has(target), `Missing local works route ${target} from ${route}`);
    }
  }

  const inventory = {};
  for (const [route, bytes] of outputs) {
    const destination = path.join(outRoot, route);
    await mkdir(path.dirname(destination), { recursive: true });
    await writeFile(destination, bytes);
    inventory[route] = { bytes: bytes.length, sha256: sha(bytes) };
  }
  return inventory;
}

export const WORKS = Object.freeze({
  source_review_head: 'dfe4b5fcfa279ef08a1d5aac5d3c3a1c59494175',
  powers_head: '548e1fe316d1ccb58b3f4008097deb9d0dbe6c39',
  vermeer_head: '36cc8c54e937318c61d2c317ff71c7f66bc38687',
  routes: ['/works/', '/works/harriet-powers/', '/works/johannes-vermeer/', '/works/anna-atkins/', '/works/shen-zhou/', '/works/edmonia-lewis/'],
  selection_ceiling: 'Project-curated starting shelf; not ranking, representative canon, completeness claim or diversity proof.',
});
