import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';

test('only the named bridge and history outputs differ from the published context-window edition', async () => {
  const revision = '2989896fa53b9dd2e870af279a3861d710446b83';
  const changed = new Set(['index.html','manifest.json','changes.md','changes.html']);
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
  assert.equal(retained,150);
});

test('explicit nine-state graph has five arrival cues, two first-depth bridges, a source-labelled encounter and no intake', async () => {
  const html = await readFile('out/index.html','utf8');
  assert.deepEqual([...html.matchAll(/data-step="([^"]+)"/g)].map(m=>m[1]), ['welcome','orientation','look','work','understand','make','challenge','story','leave']);
  const orientation = html.split('id="step-orientation"')[1].split('</section>')[0];
  assert.deepEqual([...orientation.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['#step-look','#step-work','#step-look','#step-challenge','#step-look']);
  assert.match(orientation,/I am here for the art, or just looking/);
  const work = html.split('id="step-work"')[1].split('</section>')[0];
  assert.deepEqual([...work.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['#step-understand','#step-make']);
  assert.match(work,/Understand what is happening/);
  const understand = html.split('id="step-understand"')[1].split('</section>')[0];
  assert.deepEqual([...understand.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['/explore/nodes/change.html','#step-story']);
  assert.match(understand,/A description can remain still while the situation changes/);
  const make = html.split('id="step-make"')[1].split('</section>')[0];
  assert.deepEqual([...make.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['/explore/nodes/futures.html','#step-story']);
  assert.match(make,/An option written down is not necessarily an option someone can use/);
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

test('D017 through D019 are paired in both formats and earlier history remains exact', async () => {
  const md = await readFile('public/changes.md','utf8');
  const html = await readFile('public/changes.html','utf8');
  for (const [id,previous] of [['D017','D016'],['D018','D017'],['D019','D018']]) {
    const paragraphs = md.split('### '+id)[1].split('### '+previous)[0].trim().split(/\n\s*\n/);
    const rendered = html.split('<h3 id="'+id.toLowerCase()+'">'+id+'</h3>')[1].split('<h3 id="'+previous.toLowerCase()+'">')[0];
    const expected = paragraphs.map(p=>'<p>'+p.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll("'",'&#x27;')+'</p>').join('');
    assert.equal(rendered,expected);
  }
  for (const [name,anchor] of [['changes.md','### D016'],['changes.html','<h3 id="d016">']]) {
    const before = execFileSync('git',['show','e40cfed5595923bc7f741424152044e485441362:public/'+name]).toString('utf8');
    const after = await readFile('public/'+name,'utf8');
    assert.equal(after.slice(after.indexOf(anchor)),before.slice(before.indexOf(anchor)),name);
  }
});
