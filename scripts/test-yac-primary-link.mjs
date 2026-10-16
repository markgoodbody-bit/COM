import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

test('YAC entrance and AI handoff point to the public Clearing', async () => {
  const html = await readFile('public/explore/yac/index.html', 'utf8');
  const header = html.match(/<header>[\s\S]*?<\/header>/)?.[0];
  const handoff = html.match(/<div class="handoff">[\s\S]*?<\/div>/)?.[0];
  assert.match(header, /href="https:\/\/yetanotherclearing\.com\/">Open Yet Another Clearing/);
  assert.match(handoff, /href="https:\/\/yetanotherclearing\.com\/">https:\/\/yetanotherclearing\.com\//);
  assert.match(html, /href="start\.txt">PSFH introduction/);
  assert.match(html, /href="read\.json"/);
  assert.match(html, /href="thr\/"/);
  assert.doesNotMatch(html, /http-equiv="refresh"|<script|<form/i);
});
