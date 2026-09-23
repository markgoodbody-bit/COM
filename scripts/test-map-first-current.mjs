import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { renderHumanMap } from './human-map.mjs';
const source = await readFile('public/explore/index.html', 'utf8');
const index = JSON.parse(await readFile('public/explore/questions.json'));
const records = Object.fromEntries(await Promise.all(index.nodes.map(async n => [n.id, JSON.parse(await readFile(`public/explore/nodes/${n.id}.json`))])));
const escape = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#x27;');

test('map precedes verbatim orientation and preserves every source route', async () => {
  const built = await readFile('out/explore/index.html','utf8');
  const details = built.split('<summary>About this reading space</summary>')[1].split('</details>')[0];
  const sections = [...source.matchAll(/<section>[\s\S]*?<\/section>/g)].map(m=>m[0]);
  assert.equal(sections.length,6);
  assert.equal(details,sections.join(''));
  assert.ok(built.indexOf('id="reading-map"') < built.indexOf('About this reading space'));
  assert.equal((built.match(/data-reading-node=/g)||[]).length,10);
  assert.equal((built.match(/data-relation=/g)||[]).length,30);
  for(const node of index.nodes) assert.ok(built.includes(escape(node.question)));
  for(const link of source.matchAll(/href="([^"]+)"/g)) assert.ok(built.includes(`href="${link[1]}"`),link[1]);
  assert.equal((built.match(/class="skip"/g)||[]).length,1);
  assert.ok(built.indexOf('<figure>') < built.indexOf('<main'));
});

test('changed orientation or graph is rejected rather than silently discarded',()=>{
  assert.throws(()=>renderHumanMap(source.replace('<section>','<section class="changed">'),index,records),/orientation sections/);
  const bad=structuredClone(index); bad.nodes[0].question+=' changed';
  assert.throws(()=>renderHumanMap(source,bad,records),/identity disagrees/);
});
