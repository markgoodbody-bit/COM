import { readFile, mkdir, writeFile, access } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { SITE_EDITION } from './site-edition.mjs';
const ORIGIN = 'https://pleasestartfromhere.com';
export const VIEWS = [
  { output: 'read/start.html', source: 'explore/start.json', title: 'Start: complete JSON source text', edition: 'Door Preview 0.7, publishing ba181af07ed1254c9670010574c77c8503969de3; psfh-arrival format 0.1', sha256: '4cc066e604d73b3f21ff1072d23bbe9b5057dd82b8552bb1b899779f3f58ed2e' },
  { output: 'read/orientation.html', source: 'llms.txt', title: 'Orientation: complete text source', edition: 'Site Preview 0.8.2, maintained working edition with optional teaching questions; not validation', sha256: 'a89be8d20797428e82bc86be4ffa68df7c128a833c20a04826fedc449c1c0da9' },
  { output: 'read/trace-spine.html', source: 'resources/trace/TRACE-SPINE.md', title: 'TRACE compact spine: complete Markdown source text', edition: 'TRACE RC1, source 46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b; not a new TRACE release', sha256: '9ee106e98a34643929f82fa3296adffac46e650e4e8d0b775016269f0fe50999' },
  { output: 'read/me-book.html', source: 'resources/mechanical-ethics/MECHANICAL_ETHICS.md', title: 'Mechanical Ethics: complete Markdown source text', edition: 'ME v0.7.0 working candidate v0.2.4, source 44f7efb59806242fd26c572cbfbaaeaefaea2058; not a new ME release', sha256: '6a85d512904d00ea6e76b6d4f7fdff63cc9068a99d88b3541d501ed6ae2adc93' },
];
export const digest = bytes => createHash('sha256').update(bytes).digest('hex');
export function escapeText(text) {
  return text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;').replaceAll('\r', '&#13;');
}
export function decodeSource(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes);
  if (text.includes('\0')) throw Error('NUL cannot roundtrip through HTML text; raw source remains authority');
  if (!Buffer.from(text, 'utf8').equals(bytes)) throw Error('UTF-8 roundtrip failed');
  return text;
}
export function sourceReferences(view, text) {
  const refs = view.source.endsWith('.json')
    ? Object.entries(JSON.parse(text).routes).map(([label, href]) => [label.replaceAll('_', ' '), href])
    : [...text.matchAll(/!?\[([^\]\n]+)\]\(([^\s)]+)\)/g)].map(m => [m[1], m[2]]);
  return refs.map(([label, href]) => [label, new URL(href, ORIGIN + '/' + view.source)])
    .filter(([, url]) => url.origin === ORIGIN && url.protocol === 'https:' && !url.username && !url.password);
}
export function renderSource(view, bytes, links) {
  const text = decodeSource(bytes);
  if (digest(bytes) !== view.sha256) throw Error('Source changed: ' + view.source);
  const raw = ORIGIN + '/' + view.source;
  const nav = links.map(([label, url]) => '<li><a href="' + escapeText(url) + '">' + escapeText(label) + '</a></li>').join('');
  return '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + escapeText(view.title) + '</title><link rel="stylesheet" href="/style.css"><link rel="alternate" href="' + raw + '"></head><body><header class="masthead"><a href="/">Please Start From Here</a></header><main><p>Site Preview ' + SITE_EDITION + '</p><h1>' + escapeText(view.title) + '</h1><p>This is the full original source as text, not a formatted book, abridgement or executable instruction. It is an optional HTML representation, not a way around a reader’s access policy. No provider compatibility is guaranteed.</p><p>Source edition: ' + escapeText(view.edition) + '.</p><p>Raw source: <a href="' + raw + '">' + raw + '</a><br>UTF-8 bytes: ' + bytes.length + '<br>SHA-256: <span style="overflow-wrap:anywhere">' + view.sha256 + '</span>. The raw file remains the byte authority.</p><nav aria-label="Optional next readings"><ul>' + nav + '</ul></nav><pre style="white-space:pre-wrap;overflow-wrap:anywhere;font-size:1rem;line-height:1.5"><code id="source-text">' + escapeText(text) + '</code></pre><p><a href="/">Return or stop</a></p></main></body></html>\n';
}
export async function generateViews(publicRoot) {
  const files = new Map();
  for (const view of VIEWS) {
    const bytes = await readFile(path.join(publicRoot, view.source));
    const links = VIEWS.filter(v => v !== view).map(v => [v.title, ORIGIN + '/' + v.output]);
    links.push(['Reading catalogue and fixed editions', ORIGIN + '/resources/'],
               ['Example: existing HTML view', ORIGIN + '/explore/example/entry.html'],
               ['Challenge and reply limits: existing HTML view', ORIGIN + '/explore/challenge.html']);
    for (const [label, url] of sourceReferences(view, decodeSource(bytes))) {
      const local = decodeURIComponent(url.pathname).slice(1);
      if (local.split('/').some(p => p === '..') || url.search) throw Error('Unexpected source route');
      const counterpart = VIEWS.find(v => v.source === local);
      if (counterpart) url.pathname = '/' + counterpart.output;
      else {
        const htmlPath = local.replace(/\.(md|json)$/, '.html');
        try { await access(path.join(publicRoot, htmlPath)); url.pathname = '/' + htmlPath; }
        catch { await access(path.join(publicRoot, local)); }
      }
      links.push([label, url.href]);
    }
    files.set(view.output, Buffer.from(renderSource(view, bytes, links)));
  }
  return files;
}
export async function writeViews(publicRoot, outputRoot) {
  const files = await generateViews(publicRoot);
  for (const [relative, bytes] of files) {
    await mkdir(path.dirname(path.join(outputRoot, relative)), { recursive: true });
    await writeFile(path.join(outputRoot, relative), bytes);
  }
}
