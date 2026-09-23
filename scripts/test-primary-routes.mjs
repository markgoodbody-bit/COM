import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import test from 'node:test';

const html = readFileSync(new URL('../out/index.html', import.meta.url), 'utf8');
test('primary routes distinguish questions, reading and art', () => {
  const nav = html.match(/<nav class="project-routes"[^>]*>([\s\S]*?)<\/nav>/)?.[1];
  assert.ok(nav, 'primary navigation exists');
  assert.deepEqual([...nav.matchAll(/href="([^"]+)"/g)].map(match => match[1]),
    ['#step-work', '#reading', '/works/']);
  for (const id of ['step-work', 'reading']) assert.ok(html.includes(`id="${id}"`));
  assert.match(html, /href="\/explore\/challenge.html">Challenge or disagree with the work<\/a>/);
});
