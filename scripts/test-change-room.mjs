import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { renderChangeRoom } from './change-room.mjs';

const node = JSON.parse(await readFile('public/explore/nodes/change.json'));
const index = JSON.parse(await readFile('public/explore/questions.json'));
const targets = Object.fromEntries(await Promise.all(node.next.map(async edge => [edge.target, JSON.parse(await readFile('public/explore/nodes/'+edge.path))])));
const escape = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#x27;');

test('Change keeps all original paragraphs and source links, with challenge outside disclosure', async () => {
  const html = await readFile('out/explore/nodes/change.html','utf8');
  const original = await readFile('public/explore/nodes/change.html','utf8');
  for (const [,paragraph] of original.matchAll(/<p>(.*?)<\/p>/g)) assert.ok(html.includes(paragraph),paragraph);
  for (const [,url] of original.matchAll(/href="(https:[^"]+)"/g)) assert.ok(html.includes('href="'+url+'"'),url);
  const uncollapsed = html.replace(/<details\b[\s\S]*?<\/details>/g,'');
  for (const key of ['short','question','perspective','challenge','status']) assert.ok(uncollapsed.includes(escape(node[key])),key);
  for (const route of ['change.md','change.json','/#step-understand','/','/explore/#reading-map','/#step-leave']) assert.ok(uncollapsed.includes('href="'+route+'"'),route);
  assert.doesNotMatch(html,/<(?:script|img|form|input|iframe)\b/);
  assert.match(html,/<details id="full-account"><summary/);
  assert.equal((html.match(/<h1\b/g)||[]).length,1);
});

test('optional directions use original edges and exact target questions', async () => {
  const html = await readFile('out/explore/nodes/change.html','utf8');
  const links = [...html.matchAll(/data-relation="([^"]+)" href="([^"]+)" title="[^"]+">([^<]+)<\/a>/g)];
  assert.deepEqual(links.map(m=>[m[1],m[2]]),node.next.map(e=>[e.relation,e.path.replace('.json','.html')]));
  for (const [i,link] of links.entries()) assert.equal(link[3],escape(targets[node.next[i].target].question));
  for (const edge of node.next) await readFile('out/explore/nodes/'+edge.path.replace('.json','.html'));
});

test('missing challenge, disagreeing graph, and missing or unsafe targets fail closed', () => {
  for (const key of ['detail','perspective','challenge','boundary']) {
    assert.throws(()=>renderChangeRoom({...node,[key]:''},index,targets),/Missing Change field/);
  }
  const wrongIndex = structuredClone(index);
  wrongIndex.nodes.find(n=>n.id==='change').next[0].target = 'care';
  assert.throws(()=>renderChangeRoom(node,wrongIndex,targets),/Graph edges disagree/);
  assert.throws(()=>renderChangeRoom(node,index,{}),/Missing edge target/);
  assert.throws(()=>renderChangeRoom({...node,id:'care'},index,targets),/Only the Change/);
  const unsafe = structuredClone(node), unsafeIndex = structuredClone(index);
  unsafe.next[0].path = '../aperture.json';
  unsafeIndex.nodes.find(n=>n.id==='change').next[0].path = 'nodes/../aperture.json';
  assert.throws(()=>renderChangeRoom(unsafe,unsafeIndex,targets),/Unsafe graph edge/);
});

test('only Change and its delivery/history records differ from the immediate published parent', async () => {
  const revision = '1060d6ed3d7e2133a5aa63b1ec4dd8512e57dfc9';
  const changed = new Set(['explore/nodes/change.html','explore/map.json','manifest.json','changes.md','changes.html']);
  const files = (await readdir('out',{recursive:true,withFileTypes:true})).filter(e=>e.isFile()).map(e=>(e.parentPath+'/'+e.name).replaceAll('\\','/').split('/out/').pop().replace(/^out\//,''));
  assert.equal(files.length,155);
  for (const file of files) {
    const before = execFileSync('git',['show',revision+':'+file],{maxBuffer:32*1024*1024});
    const after = await readFile('out/'+file);
    if (changed.has(file)) assert.notDeepEqual(after,before,file); else assert.deepEqual(after,before,file);
  }
  const map = JSON.parse(await readFile('out/explore/map.json'));
  for (const item of map.resources) {
    const bytes = await readFile('out/explore/'+item.path);
    assert.equal(item.bytes,bytes.length,item.path);
    assert.equal(item.sha256,createHash('sha256').update(bytes).digest('hex'),item.path);
  }
});
