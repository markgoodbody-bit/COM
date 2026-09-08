import { readFile, writeFile, mkdir } from 'node:fs/promises';
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
const html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Campfire | TRACE and Mechanical Ethics</title><meta name="description" content="A voluntary starting point for TRACE, Mechanical Ethics and neighbouring methods."><meta name="robots" content="noindex,nofollow"><link rel="describedby" type="text/plain" href="http://pleasestartfromhere.com/llms.txt"><link rel="stylesheet" href="./style.css"></head><body>' + body + '</body></html>\n';
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
await mkdir(path.join(root, 'downloads'), { recursive: true });
const css = await readFile(path.join(root, 'app/globals.css'), 'utf8');
await writeFile(path.join(root, 'downloads/Campfire-preview.html'), html.replace('<link rel="stylesheet" href="./style.css">', '<style>' + css + '</style>'));
await writeFile(path.join(root, 'out/404.html'), '<!doctype html><html lang="en"><meta charset="utf-8"><title>Not found</title><h1>Not found</h1><p>This prototype has one entry page.</p></html>');
console.log('Static build: human preview and five machine-reading files; no browser JavaScript or server runtime.');
for (const relativePath of ['out/index.html', 'downloads/Campfire-preview.html', ...machineFiles.map(name => 'out/' + name)]) {
  const bytes = await readFile(path.join(root, relativePath));
  console.log(`${relativePath}: ${bytes.length} bytes; SHA-256 ${createHash('sha256').update(bytes).digest('hex')}`);
}
