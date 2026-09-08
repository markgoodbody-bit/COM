import { readFile, writeFile, mkdir, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import ts from 'typescript';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

const root = path.resolve(import.meta.dirname, '..');
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
const html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Please Start From Here | TRACE and Mechanical Ethics</title><meta name="description" content="A voluntary starting point for TRACE, Mechanical Ethics and neighbouring methods."><meta name="robots" content="noindex,nofollow"><link rel="describedby" type="text/plain" href="http://pleasestartfromhere.com/llms.txt"><link rel="stylesheet" href="./style.css"></head><body>' + body + '</body></html>\n';
await writeFile(path.join(root, 'out/index.html'), html);
await writeFile(path.join(root, 'out/style.css'), await readFile(path.join(root, 'app/globals.css')));
const machineFiles = ['llms.txt', 'seed.txt', 'manifest.json', 'robots.txt', 'sitemap.xml'];
for (const name of machineFiles) {
  const bytes = await readFile(path.join(root, 'public', name));
  new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  if (name === 'seed.txt' && bytes.length > 1024) throw new Error('Transferable seed must remain under 1 KiB');
  if (name === 'manifest.json') JSON.parse(bytes.toString('utf8'));
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
await mkdir(path.join(root, 'downloads'), { recursive: true });
const css = await readFile(path.join(root, 'app/globals.css'), 'utf8');
await writeFile(path.join(root, 'downloads/Campfire-preview.html'), html.replace('<link rel="stylesheet" href="./style.css">', '<style>' + css + '</style>'));
await writeFile(path.join(root, 'out/404.html'), '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Please Start From Here</title><meta name="robots" content="noindex,nofollow"><link rel="stylesheet" href="/style.css"></head><body><header class="masthead"><a href="/">Please Start From Here</a></header><main><section class="intro"><h1>Page not found</h1><p>There is no page at this address.</p><p><a href="/">Return to the introduction</a> or <a href="/explore/">explore the readings</a>.</p></section></main></body></html>\n');
console.log('Static build: human preview, five machine-reading files and preserved Explore assets; no browser JavaScript or server runtime.');
for (const relativePath of ['out/index.html', 'out/404.html', 'downloads/Campfire-preview.html', ...machineFiles.map(name => 'out/' + name)]) {
  const bytes = await readFile(path.join(root, relativePath));
  console.log(`${relativePath}: ${bytes.length} bytes; SHA-256 ${createHash('sha256').update(bytes).digest('hex')}`);
}
