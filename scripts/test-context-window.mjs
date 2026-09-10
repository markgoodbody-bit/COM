import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';

test('only the named navigation and history outputs differ from the published art-first edition', async () => {
  const revision = '7135b629b4180ad07a500e41647d203c07f80879';
  const changed = new Set(['index.html','style.css','llms.txt','manifest.json','read/orientation.html','changes.md','changes.html']);
  const names = (await readdir('out', {recursive:true,withFileTypes:true})).filter(e=>e.isFile()).map(e=> (e.parentPath + '/' + e.name).replaceAll('\\','/').split('/out/').pop().replace(/^out\//,''));
  assert.equal(names.length, 155);
  let retained = 0;
  for (const name of names) {
    if (name === 'journey.js') continue;
    const before = execFileSync('git',['show',revision+':'+name],{maxBuffer:20*1024*1024});
    const after = await readFile('out/'+name);
    if (changed.has(name)) assert.notDeepEqual(after,before,name);
    else { assert.deepEqual(after,before,name); retained++; }
  }
  assert.equal(retained,147);
});

test('explicit seven-state graph has five arrival cues, a source-labelled encounter and no intake', async () => {
  const html = await readFile('out/index.html','utf8');
  assert.deepEqual([...html.matchAll(/data-step="([^"]+)"/g)].map(m=>m[1]), ['welcome','orientation','look','work','challenge','story','leave']);
  const orientation = html.split('id="step-orientation"')[1].split('</section>')[0];
  assert.deepEqual([...orientation.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['#step-look','#step-work','#step-look','#step-challenge','#step-look']);
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(new Set(ids).size,ids.length);
  for (const [,id] of html.matchAll(/href="#([^"]+)"/g)) assert.ok(ids.includes(id), id);
  assert.match(html,/not a documented tenant case/);
  assert.match(html,/<details class="full-reference" id="full-introduction" open/);
  assert.doesNotMatch(html,/<(?:form|input|textarea|iframe)\b/);
  const exits = html.split('class="journey-exits"')[1].split('</nav>')[0];
  assert.match(exits,/href="\/explore\/#reading-map"/);
  assert.match(exits,/href="#step-leave"/);
});

test('only the local integrity-pinned enhancement ships; offline fallback contains no script', async () => {
  const bytes = await readFile('out/journey.js');
  assert.deepEqual(bytes,await readFile('public/journey.js'));
  const html = await readFile('out/index.html','utf8');
  const scripts = [...html.matchAll(/<script\b[^>]*>.*?<\/script>/g)].map(m=>m[0]);
  assert.deepEqual(scripts,['<script defer src="/journey.js" integrity="sha256-'+createHash('sha256').update(bytes).digest('base64')+'"></script>']);
  assert.doesNotMatch(bytes.toString(),/\b(?:fetch|XMLHttpRequest|WebSocket|sendBeacon|localStorage|sessionStorage|indexedDB|eval)\b|document\.cookie/);
  const offline = await readFile('downloads/Campfire-preview.html','utf8');
  assert.doesNotMatch(offline,/<script\b/);
  assert.match(offline,/id="step-story"/);
  const manifest = JSON.parse(await readFile('out/manifest.json'));
  assert.equal(manifest.provenance.context_window.script_sha256,createHash('sha256').update(bytes).digest('hex'));
});

test('D017 is paired in both formats and earlier history remains exact', async () => {
  const md = await readFile('public/changes.md','utf8');
  const html = await readFile('public/changes.html','utf8');
  const paragraphs = md.split('### D017')[1].split('### D016')[0].trim().split(/\n\s*\n/);
  const rendered = html.split('<h3 id="d017">D017</h3>')[1].split('<h3 id="d016">')[0];
  const expected = paragraphs.map(p=>'<p>'+p.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll("'",'&#x27;')+'</p>').join('');
  assert.equal(rendered,expected);
  for (const [name,anchor] of [['changes.md','### D016'],['changes.html','<h3 id="d016">']]) {
    const before = execFileSync('git',['show','e40cfed5595923bc7f741424152044e485441362:public/'+name]).toString('utf8');
    const after = await readFile('public/'+name,'utf8');
    assert.equal(after.slice(after.indexOf(anchor)),before.slice(before.indexOf(anchor)),name);
  }
});
