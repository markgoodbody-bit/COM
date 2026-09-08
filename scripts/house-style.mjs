import { readFile, writeFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';

const stylesheet = '<link rel="stylesheet" href="/style.css">';
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
export function sharedStyle(html) {
  if (!html.includes('</head>')) throw Error('HTML head missing');
  // Generated trusted HTML only. Body markup and source payload are untouched.
  const boundary = html.indexOf('</head>');
  const head = html.slice(0, boundary).replace(/<style>[\s\S]*?<\/style>/g, '');
  return head.includes('rel="stylesheet"') ? head + html.slice(boundary)
    : head + stylesheet + html.slice(boundary);
}

export async function applyHouseStyle(root) {
  const changed = [];
  async function walk(relative = '') {
    for (const entry of await readdir(path.join(root, relative), { withFileTypes: true })) {
      const child = path.posix.join(relative, entry.name);
      if (entry.isDirectory()) { await walk(child); continue; }
      if (!entry.isFile()) throw Error('Unexpected generated entry: ' + child);
      if (!child.endsWith('.html')) continue;
      const file = path.join(root, child);
      const before = await readFile(file, 'utf8'), after = sharedStyle(before);
      if (before !== after) { await writeFile(file, after); changed.push(child); }
    }
  }
  await walk();
  // Keep delivered representation identities distinct from original render inputs.
  const manifestPath = path.join(root, 'manifest.json');
  const manifest = JSON.parse(await readFile(manifestPath));
  const discussion = manifest.provenance.discussion;
  discussion.input_html_sha256 = discussion.html_sha256;
  discussion.html_sha256 = sha(await readFile(path.join(root, 'discussion/index.html')));
  manifest.provenance.presentation = {
    direction: 'https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5586692116',
    stylesheet: '/style.css', stylesheet_sha256: sha(await readFile(path.join(root, 'style.css'))),
    scope: 'Shared HTML presentation; original source text, raw files and fixed editions unchanged.',
  };
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
  const mapPath = path.join(root, 'explore/map.json');
  const map = JSON.parse(await readFile(mapPath));
  for (const item of map.resources) {
    const bytes = await readFile(path.join(root, 'explore', item.path));
    item.bytes = bytes.length; item.sha256 = sha(bytes);
  }
  await writeFile(mapPath, JSON.stringify(map, null, 2) + '\n');
  console.log('Shared stylesheet applied to', changed.length, 'previously separate HTML skins.');
}
