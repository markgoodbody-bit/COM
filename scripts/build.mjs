import { readFile, writeFile, mkdir, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import ts from 'typescript';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { copyResources } from './resources.mjs';
import { writeViews, VIEWS } from './source-views.mjs';
import { SITE_EDITION } from './site-edition.mjs';
import { applyHouseStyle } from './house-style.mjs';
import { copyCampFire, CAMP_FIRE } from './camp-fire.mjs';

const root = path.resolve(import.meta.dirname, '..');
// Discussion is an accepted editorial source, not a submission or live inbox.
const discussionPins = JSON.parse(await readFile(path.join(root, 'public/manifest.json'), 'utf8')).provenance.discussion;
const discussionFiles = [];
for (const [name, key] of [['index.md', 'markdown_sha256'], ['index.html', 'html_sha256']]) {
  const bytes = await readFile(path.join(root, 'public/discussion', name));
  if (createHash('sha256').update(bytes).digest('hex') !== discussionPins[key]) throw new Error('Discussion copy changed: ' + name);
  discussionFiles.push([name, bytes]);
}
// Validate all copied resources before changing the normal build output.
await copyResources(path.join(root, 'public/resources'), path.join(root, 'out/resources'));
await copyCampFire(path.join(root, 'public'), path.join(root, 'out'));
await mkdir(path.join(root, '.build'), { recursive: true });
await mkdir(path.join(root, 'out'), { recursive: true });
const source = await readFile(path.join(root, 'app/page.tsx'), 'utf8');
const result = ts.transpileModule(source, { compilerOptions: {
  jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext,
}, reportDiagnostics: true });
if (result.diagnostics?.some(d => d.category === ts.DiagnosticCategory.Error)) throw new Error('Page compilation failed');
const modulePath = path.join(root, '.build/page.mjs');
await writeFile(modulePath, result.outputText);
const { default: Page } = await import(pathToFileURL(modulePath).href);
const body = renderToStaticMarkup(React.createElement(Page));
if (/<script\b|<form\b|<iframe\b/i.test(body)) throw new Error('Reader path must be static and read-only');
const html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Please Start From Here</title><meta name="description" content="A voluntary starting point for understanding, deciding, making and correcting under uncertainty."><link rel="describedby" type="text/plain" href="https://pleasestartfromhere.com/llms.txt"><link rel="alternate" type="text/plain" href="https://pleasestartfromhere.com/llms.txt"><link rel="alternate" type="application/json" href="https://pleasestartfromhere.com/explore/start.json"><link rel="stylesheet" href="./style.css"></head><body>' + body + '</body></html>\n';
await writeFile(path.join(root, 'out/index.html'), html);
await writeFile(path.join(root, 'out/style.css'), await readFile(path.join(root, 'app/globals.css')));
const machineFiles = ['llms.txt', 'seed.txt', 'manifest.json', 'robots.txt', 'sitemap.xml'];
for (const name of machineFiles) {
  let bytes = await readFile(path.join(root, 'public', name));
  new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  if (name === 'seed.txt' && bytes.length > 1024) throw new Error('Transferable seed must remain under 1 KiB');
  if (name === 'manifest.json') {
    const manifest = JSON.parse(bytes.toString('utf8'));
    manifest.site_edition = SITE_EDITION;
    manifest.routes.html_source_text = '/read/start.html';
    manifest.provenance.html_source_text = VIEWS;
    manifest.routes.artwork = '/art/camp-fire.json';
    manifest.provenance.artwork = { record: '/art/camp-fire.json', image_sha256: CAMP_FIRE.sha256, source: CAMP_FIRE.object_url };
    manifest.provenance.title_and_art_direction = 'https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5592807329';
    manifest.provenance.editorial_revision = 'https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5592995706';
    bytes = Buffer.from(JSON.stringify(manifest, null, 2) + '\n');
  }
  await writeFile(path.join(root, 'out', name), bytes);
}
// Preserve the exact generated Explore assets accepted from the publishing handoff.
// Do not silently omit a missing source directory or follow filesystem links.
async function copyExplore(relative = 'explore') {
  for (const entry of await readdir(path.join(root, 'public', relative), { withFileTypes: true })) {
    const child = path.join(relative, entry.name);
    if (entry.isDirectory()) await copyExplore(child);
    else if (entry.isFile()) {
      const bytes = await readFile(path.join(root, 'public', child));
      new TextDecoder('utf-8', { fatal: true }).decode(bytes);
      await mkdir(path.dirname(path.join(root, 'out', child)), { recursive: true });
      await writeFile(path.join(root, 'out', child), bytes);
    } else throw new Error(`Unsupported Explore entry: ${child}`);
  }
}
await copyExplore();
await mkdir(path.join(root, 'out/discussion'), { recursive: true });
for (const [name, bytes] of discussionFiles) await writeFile(path.join(root, 'out/discussion', name), bytes);
await writeViews(path.join(root, 'public'), path.join(root, 'out'));
// Reviewed reader history is separately pinned; preserve its exact source bytes.
for (const name of ['changes.md', 'changes.html']) {
  const bytes = await readFile(path.join(root, 'public', name));
  new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  const pins = JSON.parse(await readFile(path.join(root, 'public/manifest.json'), 'utf8')).provenance;
  const expected = pins[name.endsWith('.md') ? 'change_history_sha256' : 'change_history_input_html_sha256'];
  if (createHash('sha256').update(bytes).digest('hex') !== expected) throw new Error('History changed: ' + name);
  await writeFile(path.join(root, 'out', name), bytes);
}
await mkdir(path.join(root, 'downloads'), { recursive: true });
const css = await readFile(path.join(root, 'app/globals.css'), 'utf8');
// Keep the downloadable local preview outside the public indexing-policy change.
const previewHtml = html.replace('<link rel="describedby"', '<meta name="robots" content="noindex,nofollow"><link rel="describedby"');
const offlineArt = 'data:image/jpeg;base64,' + (await readFile(path.join(root, 'public/art/camp-fire.jpg'))).toString('base64');
const offlineHtml = previewHtml
  .replace('<link rel="stylesheet" href="./style.css">', '<style>' + css + '</style>')
  .replace(/<link rel="preload" as="image" imageSrcSet="[^"]+" imageSizes="[^"]+" fetchPriority="high"\/>/, '')
  .replace(/ srcSet="[^"]+"/, '')
  .replace(/ sizes="[^"]+"/, '')
  .replace(' fetchPriority="high"', '')
  .replace('src="' + CAMP_FIRE.local_image + '"', 'src="' + offlineArt + '"');
await writeFile(path.join(root, 'downloads/Campfire-preview.html'), offlineHtml);
await writeFile(path.join(root, 'out/404.html'), '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Please Start From Here</title><meta name="robots" content="noindex,nofollow"><link rel="stylesheet" href="/style.css"></head><body><header class="masthead"><a href="/">Please Start From Here</a></header><main><section class="intro"><h1>Page not found</h1><p>There is no page at this address.</p><p><a href="/">Return to the introduction</a> or <a href="/explore/">explore the readings</a>.</p></section></main></body></html>\n');
await applyHouseStyle(path.join(root, 'out'));
console.log('Static build: shared HTML presentation, preserved reading sources; no browser JavaScript or server runtime.');
for (const relativePath of ['out/index.html', 'out/404.html', 'downloads/Campfire-preview.html', ...machineFiles.map(name => 'out/' + name)]) {
  const bytes = await readFile(path.join(root, relativePath));
  console.log(`${relativePath}: ${bytes.length} bytes; SHA-256 ${createHash('sha256').update(bytes).digest('hex')}`);
}
