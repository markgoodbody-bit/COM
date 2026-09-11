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
  for (const route of ['change.md','change.json','/','/explore/#reading-map','/#step-leave']) assert.ok(uncollapsed.includes('href="'+route+'"'),route);
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
  assert.throws(()=>renderReadingRoom({...node,id:'unknown'},index,targets),/Unknown reading room/);
  const unsafe = structuredClone(node), unsafeIndex = structuredClone(index);
  unsafe.next[0].path = '../aperture.json';
  unsafeIndex.nodes.find(n=>n.id==='change').next[0].path = 'nodes/../aperture.json';
  assert.throws(()=>renderReadingRoom(unsafe,unsafeIndex,targets),/Unsafe graph edge/);
});

test('D029 routing plus the D030 homepage presentation are the only changes from D028', async () => {
  const revision = '146758fa9911460564646bec757e01bfad26b976';
  const changed = new Set(['index.html','style.css','explore/nodes/change.html','explore/map.json','manifest.json','changes.md','changes.html']);
  const files = (await readdir('out',{recursive:true,withFileTypes:true})).filter(e=>e.isFile()).map(e=>(e.parentPath+'/'+e.name).replaceAll('\\','/').split('/out/').pop().replace(/^out\//,''));
  assert.equal(files.length,155);
  for (const file of files) {
    const before = execFileSync('git',['show',revision+':'+file],{maxBuffer:32*1024*1024});
    const after = await readFile('out/'+file);
    if (changed.has(file)) assert.notDeepEqual(after,before,file); else assert.deepEqual(after,before,file);
  }
  const map = JSON.parse(await readFile('out/explore/map.json'));
  const beforeMap = JSON.parse(execFileSync('git',['show',revision+':explore/map.json']).toString('utf8'));
  const withoutDelivery = value => ({...value, resources: value.resources.map(({bytes,sha256,...item}) => item)});
  assert.deepEqual(withoutDelivery(map),withoutDelivery(beforeMap));
  const identityChanges = map.resources.filter((item,i)=>JSON.stringify(item)!==JSON.stringify(beforeMap.resources[i]));
  assert.deepEqual(identityChanges.map(item=>item.path),['nodes/change.html']);
  for (const item of map.resources) {
    const bytes = await readFile('out/explore/'+item.path);
    assert.equal(item.bytes,bytes.length,item.path);
    assert.equal(item.sha256,createHash('sha256').update(bytes).digest('hex'),item.path);
  }
});

test('all ten enabled rooms preserve their own fields, sources, routes and authored questions', async () => {
  assert.deepEqual(ENABLED_ROOMS,['change','aperture','significance','care','wisdom','selection','power','hardening','correction','futures']);
  for (const id of ENABLED_ROOMS) {
    const record = JSON.parse(await readFile('public/explore/nodes/'+id+'.json'));
    const html = await readFile('out/explore/nodes/'+id+'.html','utf8');
    const old = await readFile('public/explore/nodes/'+id+'.html','utf8');
    for (const [,p] of old.matchAll(/<p>(.*?)<\/p>/g)) assert.ok(html.includes(p),id+': '+p);
    for (const [,url] of old.matchAll(/href="(https:[^"]+)"/g)) assert.ok(html.includes('href="'+url+'"'),id+': '+url);
    for (const sourceKey of record.sources) assert.ok(html.includes('href="'+record.source_pointers[sourceKey].url+'"'),id+': '+sourceKey);
    const visible = html.replace(/<details\b[\s\S]*?<\/details>/g,'');
    for (const key of ['short','question','perspective','challenge','status']) assert.ok(visible.includes(escape(record[key])),id+': '+key);
    for (const key of ['detail','kind','boundary']) assert.ok(html.includes(escape(record[key])),id+': '+key);
    for (const ext of ['md','json']) assert.ok(visible.includes('href="'+id+'.'+ext+'"'),id+': '+ext);
    for (const route of ['/','/explore/#reading-map','/#step-leave']) assert.ok(visible.includes('href="'+route+'"'),id+': '+route);
    assert.doesNotMatch(html,/<script\b|<form\b/);
    // The existing art entrance has an image and a static opening link; the
    // reading itself must not invent history or duplicate that artwork.
    const reading = id === 'futures' ? html.match(/<article\b[\s\S]*?<\/article>/)[0] : html;
    assert.doesNotMatch(reading,/>Back\b|<img\b/);
    if (id === 'aperture') assert.doesNotMatch(html,/href="(?:change.html|\/#step-understand)"/);
    for (const edge of record.next) {
      const target = JSON.parse(await readFile('public/explore/nodes/'+edge.path));
      assert.ok(html.includes('href="'+edge.path.replace('.json','.html')+'"'),id+': '+edge.path);
      assert.ok(html.includes('>'+escape(target.question)+'</a>'),id+': '+target.question);
    }
  }
});

test('generic working syntheses remain deliberately unmarked while source kind remains in full account', async () => {
  const generic = ['change','aperture','selection','power','hardening','correction','futures'];
  for (const id of generic) {
    const record = JSON.parse(await readFile('public/explore/nodes/'+id+'.json'));
    assert.equal(record.kind,'working synthesis',id);
    const html = await readFile('out/explore/nodes/'+id+'.html','utf8');
    const visible = html.replace(/<details\b[\s\S]*?<\/details>/g,'');
    assert.doesNotMatch(html,/data-reading-kind/,id);
    assert.ok(html.includes('<h3>Status</h3><p>working synthesis. '),id);
  }
});

for (const id of ['significance','care','wisdom']) test(id + ' standing is visible before its account and question and comes from kind, not title', async () => {
  const record = JSON.parse(await readFile('public/explore/nodes/'+id+'.json'));
  const html = await readFile('out/explore/nodes/'+id+'.html','utf8');
  const visible = html.replace(/<details\b[\s\S]*?<\/details>/g,'');
  const marker = '<p data-reading-kind><strong>'+escape(record.kind)+'</strong></p>';
  assert.ok(visible.includes(marker));
  assert.ok(visible.indexOf(marker) < visible.indexOf('<p>'+escape(record.short)+'</p>'));
  assert.ok(visible.indexOf(marker) < visible.indexOf('<h2 id="question"'));
  assert.doesNotMatch(visible,/href="(?:change.html|\/#step-understand)"/);
  if (id !== 'wisdom') assert.doesNotMatch(visible,/href="aperture.html"/);
  const synthetic = renderReadingRoom({...node,kind:record.kind},index,targets);
  assert.ok(synthetic.includes(marker));
  assert.throws(()=>renderReadingRoom({...node,kind:''},index,targets),/Missing reading field: kind/);
  assert.ok(renderReadingRoom({...node,kind:'candidate <interpretation>'},index,targets).includes('candidate &lt;interpretation&gt;'));
});

test('generic rooms preserve authored provenance counts and real Futures edges', async () => {
  const expectedSources = {selection:1,power:2,hardening:2,correction:2,futures:2};
  for (const [id,count] of Object.entries(expectedSources)) {
    const record = JSON.parse(await readFile('public/explore/nodes/'+id+'.json'));
    const html = await readFile('out/explore/nodes/'+id+'.html','utf8');
    assert.equal(record.sources.length,count,id);
    for (const key of record.sources) assert.ok(html.includes(record.source_pointers[key].url),id+': '+key);
    for (const edge of record.next.filter(edge=>edge.target==='futures')) {
      const futures = JSON.parse(await readFile('public/explore/nodes/futures.json'));
      assert.ok(html.includes('href="futures.html"'),id);
      assert.ok(html.includes('>'+escape(futures.question)+'</a>'),id);
    }
  }
  assert.ok(ENABLED_ROOMS.includes('futures'));
});

test('authored edge count remains variable', () => {
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
  assert.equal(manifest.updated,'2026-09-11');
  assertRevisionDate(manifest,history);
  assert.throws(()=>assertRevisionDate({...manifest,updated:'2026-09-08'},history),/Manifest updated/);
  assert.throws(()=>assertRevisionDate(manifest,'no declared revision'),/date missing/);
  assertRevisionDate({updated:'2025-01-02'},'### D001\n\n2 January 2025 — A deliberate change.');
});
