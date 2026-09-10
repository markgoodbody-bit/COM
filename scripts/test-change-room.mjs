import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { renderReadingRoom } from './change-room.mjs';

const ids = ['change', 'aperture'];
const index = JSON.parse(await readFile('public/explore/questions.json'));
const nodes = Object.fromEntries(await Promise.all(ids.map(async id => [id, JSON.parse(await readFile(`public/explore/nodes/${id}.json`))])));
const targets = {};
for (const id of ids) {
  targets[id] = Object.fromEntries(await Promise.all(nodes[id].next.map(async edge => [edge.target, JSON.parse(await readFile('public/explore/nodes/'+edge.path))])));
}
const escape = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#x27;');

test('Change and Partial views keep original paragraphs and source links, with challenge outside disclosure', async () => {
  for (const id of ids) {
    const node = nodes[id];
    const html = await readFile(`out/explore/nodes/${id}.html`,'utf8');
    const original = await readFile(`public/explore/nodes/${id}.html`,'utf8');
    for (const [,paragraph] of original.matchAll(/<p>(.*?)<\/p>/g)) assert.ok(html.includes(paragraph),`${id}: ${paragraph}`);
    for (const [,url] of original.matchAll(/href="(https:[^"]+)"/g)) assert.ok(html.includes('href="'+url+'"'),`${id}: ${url}`);
    const uncollapsed = html.replace(/<details\b[\s\S]*?<\/details>/g,'');
    for (const key of ['short','question','perspective','challenge','status']) assert.ok(uncollapsed.includes(escape(node[key])),`${id}: ${key}`);
    for (const route of [`${id}.md`,`${id}.json`,'/','/explore/#reading-map','/#step-leave']) assert.ok(uncollapsed.includes('href="'+route+'"'),`${id}: ${route}`);
    assert.doesNotMatch(html,/<(?:script|img|form|input|iframe)\b/);
    assert.match(html,/<details id="full-account"><summary/);
    assert.equal((html.match(/<h1\b/g)||[]).length,1,id);
  }
  const change = await readFile('out/explore/nodes/change.html','utf8');
  const aperture = await readFile('out/explore/nodes/aperture.html','utf8');
  assert.ok(change.includes('<a href="/#step-understand">Understand route</a>'));
  assert.ok(!change.includes('Back to Understand'));
  assert.ok(!aperture.includes('Back to Change'));
  assert.ok(!aperture.includes('/#step-understand'));
});

test('both rooms use original edges and exact target questions', async () => {
  for (const id of ids) {
    const node = nodes[id];
    const html = await readFile(`out/explore/nodes/${id}.html`,'utf8');
    const links = [...html.matchAll(/data-relation="([^"]+)" href="([^"]+)" title="[^"]+">([^<]+)<\/a>/g)];
    assert.deepEqual(links.map(m=>[m[1],m[2]]),node.next.map(e=>[e.relation,e.path.replace('.json','.html')]),id);
    for (const [i,link] of links.entries()) assert.equal(link[3],escape(targets[id][node.next[i].target].question),`${id}: ${node.next[i].target}`);
    for (const edge of node.next) await readFile('out/explore/nodes/'+edge.path.replace('.json','.html'));
  }
});

test('missing fields, disagreeing graph, and missing or unsafe targets fail closed', () => {
  for (const id of ids) {
    const node = nodes[id];
    for (const key of ['detail','perspective','challenge','boundary']) {
      assert.throws(()=>renderReadingRoom({...node,[key]:''},index,targets[id]),new RegExp(`Missing ${id} field`));
    }
    const wrongIndex = structuredClone(index);
    wrongIndex.nodes.find(n=>n.id===id).next[0].target = 'care';
    assert.throws(()=>renderReadingRoom(node,wrongIndex,targets[id]),/Graph edges disagree/);
    assert.throws(()=>renderReadingRoom(node,index,{}),/Missing edge target/);
    const unsafe = structuredClone(node), unsafeIndex = structuredClone(index);
    unsafe.next[0].path = '../'+unsafe.next[0].target+'.json';
    unsafeIndex.nodes.find(n=>n.id===id).next[0].path = 'nodes/../'+unsafe.next[0].target+'.json';
    assert.throws(()=>renderReadingRoom(unsafe,unsafeIndex,targets[id]),/Unsafe graph edge/);
  }
  assert.throws(()=>renderReadingRoom({...nodes.change,id:'care'},index,targets.change),/Only Change and Partial views/);
});

test('only the two room outputs and their machine records differ from the current public parent', async () => {
  const revision = 'cc13e294813446f64e130f27348c2fa4ee87d888';
  const changed = new Set(['explore/nodes/change.html','explore/nodes/aperture.html','explore/map.json','manifest.json']);
  const files = (await readdir('out',{recursive:true,withFileTypes:true})).filter(e=>e.isFile()).map(e=>(e.parentPath+'/'+e.name).replaceAll('\\','/').split('/out/').pop().replace(/^out\//,''));
  assert.equal(files.length,155);
  for (const file of files) {
    const before = execFileSync('git',['show',revision+':'+file],{maxBuffer:32*1024*1024});
    const after = await readFile('out/'+file);
    if (changed.has(file)) assert.notDeepEqual(after,before,file); else assert.deepEqual(after,before,file);
  }
  const manifest = JSON.parse(await readFile('out/manifest.json'));
  assert.equal(manifest.provenance.aperture_room.node,'/explore/nodes/aperture.json');
  assert.equal(manifest.provenance.change_room.node,'/explore/nodes/change.json');
  const map = JSON.parse(await readFile('out/explore/map.json'));
  for (const item of map.resources) {
    const bytes = await readFile('out/explore/'+item.path);
    assert.equal(item.bytes,bytes.length,item.path);
    assert.equal(item.sha256,createHash('sha256').update(bytes).digest('hex'),item.path);
  }
});
