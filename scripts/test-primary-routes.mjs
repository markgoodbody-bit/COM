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
test('alternative chooser is optional and existing fragment destinations survive', () => {
  const welcome = html.split('id="step-welcome"')[1].split('</section>')[0];
  assert.match(welcome, /<details class="alternative-entrance"><summary>Other ways in<\/summary>/);
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(new Set(ids).size, ids.length);
  for (const [, id] of html.matchAll(/href="#([^"]+)"/g)) assert.ok(ids.includes(id), id);
  for (const id of ['step-welcome', 'step-look', 'step-work', 'step-future', 'step-challenge', 'step-leave']) {
    assert.ok(ids.includes(id), id);
  }
  const work = html.split('id="step-work"')[1].split('</section>')[0];
  assert.match(work, /href="\/explore\/nodes\/futures.html"/);
  const purpose = html.split('class="project-purpose"')[1].split('</div>')[0];
  assert.match(purpose, /Reading as an AI\? <a href="\/llms.txt">Use the compact text guide<\/a>/);
});
