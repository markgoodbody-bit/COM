import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { renderReadingRoom, ENABLED_ROOMS } from './change-room.mjs';
import { assertRevisionDate } from './site-edition.mjs';

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
    assert.throws(()=>renderReadingRoom({...node,[key]:''},index,targets),/Missing reading field/);
  }
  const wrongIndex = structuredClone(index);
  wrongIndex.nodes.find(n=>n.id==='change').next[0].target = 'care';
  assert.throws(()=>renderReadingRoom(node,wrongIndex,targets),/Graph edges disagree/);
  assert.throws(()=>renderReadingRoom(node,index,{}),/Missing edge target/);
  assert.throws(()=>renderReadingRoom({...node,id:'wisdom'},index,targets),/Only Change, Aperture, Significance and Care/);
  const unsafe = structuredClone(node), unsafeIndex = structuredClone(index);
  unsafe.next[0].path = '../aperture.json';
  unsafeIndex.nodes.find(n=>n.id==='change').next[0].path = 'nodes/../aperture.json';
  assert.throws(()=>renderReadingRoom(unsafe,unsafeIndex,targets),/Unsafe graph edge/);
});

test('only Care and delivery/history outputs differ from the D023 published parent', async () => {
  const revision = '9f89bd10ea399e676f5eb8296a24ffbb7c6b6373';
  const changed = new Set(['explore/nodes/care.html','explore/map.json','manifest.json','changes.md','changes.html']);
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

test('all four rooms preserve their own fields and raw routes without invented history', async () => {
  assert.deepEqual(ENABLED_ROOMS,['change','aperture','significance','care']);
  for (const id of ENABLED_ROOMS) {
    const record = JSON.parse(await readFile('public/explore/nodes/'+id+'.json'));
    const html = await readFile('out/explore/nodes/'+id+'.html','utf8');
    const old = await readFile('public/explore/nodes/'+id+'.html','utf8');
    for (const [,p] of old.matchAll(/<p>(.*?)<\/p>/g)) assert.ok(html.includes(p),id+': '+p);
    for (const [,url] of old.matchAll(/href="(https:[^"]+)"/g)) assert.ok(html.includes('href="'+url+'"'),url);
    const visible = html.replace(/<details\b[\s\S]*?<\/details>/g,'');
    for (const key of ['short','question','perspective','challenge','status']) assert.ok(visible.includes(escape(record[key])),id+': '+key);
    for (const key of ['detail','kind','boundary']) assert.ok(html.includes(escape(record[key])),id+': '+key);
    for (const ext of ['md','json']) assert.ok(visible.includes('href="'+id+'.'+ext+'"'));
    for (const route of ['/','/explore/#reading-map','/#step-leave']) assert.ok(visible.includes('href="'+route+'"'));
    assert.doesNotMatch(html,/>Back\b|<script\b|<img\b|<form\b/);
    if (id === 'aperture') assert.doesNotMatch(html,/href="(?:change.html|\/#step-understand)"/);
    for (const edge of record.next) {
      const target = JSON.parse(await readFile('public/explore/nodes/'+edge.path));
      assert.ok(html.includes('href="'+edge.path.replace('.json','.html')+'"'));
      assert.ok(html.includes('>'+escape(target.question)+'</a>'));
    }
  }
});

for (const id of ['significance','care']) test(id + ' standing is visible before its account and question and comes from kind, not title', async () => {
  const record = JSON.parse(await readFile('public/explore/nodes/'+id+'.json'));
  const html = await readFile('out/explore/nodes/'+id+'.html','utf8');
  const visible = html.replace(/<details\b[\s\S]*?<\/details>/g,'');
  const marker = '<p data-reading-kind><strong>'+escape(record.kind)+'</strong></p>';
  assert.ok(visible.includes(marker));
  assert.ok(visible.indexOf(marker) < visible.indexOf('<p>'+escape(record.short)+'</p>'));
  assert.ok(visible.indexOf(marker) < visible.indexOf('<h2 id="question"'));
  assert.doesNotMatch(visible,/href="(?:change.html|aperture.html|\/#step-understand)"/);
  const synthetic = renderReadingRoom({...node,kind:record.kind},index,targets);
  assert.ok(synthetic.includes(marker));
  assert.throws(()=>renderReadingRoom({...node,kind:''},index,targets),/Missing reading field: kind/);
  assert.ok(renderReadingRoom({...node,kind:'candidate <interpretation>'},index,targets).includes('candidate &lt;interpretation&gt;'));
});

test('authored edge count is variable and unapproved nodes remain disabled', () => {
  for (const count of [0,1,2,4]) {
    const varied = structuredClone(node), variedIndex = structuredClone(index);
    varied.next = Array.from({length:count},(_,i)=>node.next[i % node.next.length]);
    variedIndex.nodes.find(n=>n.id==='change').next = varied.next.map(e=>({...e,path:'nodes/'+e.path}));
    const html = renderReadingRoom(varied,variedIndex,targets);
    assert.equal((html.match(/data-relation=/g)||[]).length,count);
  }
});

test('manifest date follows deliberate history, not build time or linked-source dates', async () => {
  const manifest = JSON.parse(await readFile('out/manifest.json'));
  const history = await readFile('public/changes.md','utf8');
  assert.equal(manifest.updated,'2026-09-10');
  assertRevisionDate(manifest,history);
  assert.throws(()=>assertRevisionDate({...manifest,updated:'2026-09-08'},history),/Manifest updated/);
  assert.throws(()=>assertRevisionDate(manifest,'no declared revision'),/date missing/);
  assertRevisionDate({updated:'2025-01-02'},'### D001\n\n2 January 2025 — A deliberate change.');
});
