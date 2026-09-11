import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';

test('only named navigation, ten-room, machine and history outputs differ from the art-first edition', async () => {
  const revision = '7135b629b4180ad07a500e41647d203c07f80879';
  const changed = new Set(['index.html','style.css','llms.txt','manifest.json','read/orientation.html','read/start.html','explore/start.json','explore/llms.txt','changes.md','changes.html','explore/index.html','explore/nodes/change.html','explore/nodes/aperture.html','explore/nodes/significance.html','explore/nodes/care.html','explore/nodes/wisdom.html','explore/nodes/selection.html','explore/nodes/power.html','explore/nodes/hardening.html','explore/nodes/correction.html','explore/nodes/futures.html','explore/map.json']);
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
  assert.equal(retained,132);
});

test('seven-state homepage retains the Futures bridge, direct Change route and no intake', async () => {
  const html = await readFile('out/index.html','utf8');
  assert.deepEqual([...html.matchAll(/data-step="([^"]+)"/g)].map(m=>m[1]), ['welcome','look','work','future','challenge','story','leave']);
  const orientation = html.split('id="step-welcome"')[1].split('</section>')[0];
  assert.deepEqual([...orientation.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['#step-story','#step-work','#step-look','#step-challenge','#step-look']);
  assert.match(orientation,/What brought you here\?/);
  assert.doesNotMatch(html,/step-orientation|Would you like to continue\?/);
  assert.match(orientation,/I am here for the art, or just looking/);
  const work = html.split('id="step-work"')[1].split('</section>')[0];
  assert.deepEqual([...work.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['/explore/nodes/change.html','#step-future']);
  assert.match(work,/Understand what is happening/);
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
  assert.equal(manifest.routes.navigation_enhancement,'/journey.js');
  assert.equal(manifest.provenance.context_window.script_sha256,createHash('sha256').update(bytes).digest('hex'));
});

test('D017 through D036 are paired in both formats and earlier history remains exact', async () => {
  const md = await readFile('public/changes.md','utf8');
  const html = await readFile('public/changes.html','utf8');
  const d030 = md.split('### D030')[1].split('### D029')[0].trim().split(/\n\s*\n/);
  assert.equal(html.split('<h3 id="d030">D030</h3>')[1].split('<h3 id="d029">')[0], d030.map(p=>'<p>'+p.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll("'",'&#x27;')+'</p>').join(''));
  for (const [id,previous] of [['D017','D016'],['D018','D017'],['D019','D018'],['D020','D019'],['D021','D020'],['D022','D021'],['D023','D022'],['D024','D023'],['D025','D024'],['D026','D025'],['D027','D026'],['D028','D027'],['D029','D028'],['D031','D030'],['D032','D031'],['D033','D032'],['D034','D033'],['D035','D034'],['D036','D035']]) {
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

test('only the duplicate Change panel and special exit disappear; the Futures bridge remains exact', async () => {
  const html = await readFile('out/index.html','utf8');
  const escape = s=>s.replaceAll('&','&amp;').replaceAll("'",'&#x27;');
  const parent = '146758fa9911460564646bec757e01bfad26b976';
  let expected = execFileSync('git',['show',parent+':index.html']).toString('utf8');
  for (const [oldId,node] of [['understand','change']]) {
    expected = expected.replace('href="#step-'+oldId+'"','href="/explore/nodes/'+node+'.html"')
      .replace(new RegExp('<section data-step="'+oldId+'"[\\s\\S]*?</section>'),'');
    const record = JSON.parse(await readFile('public/explore/nodes/'+node+'.json'));
    const room = await readFile('out/explore/nodes/'+node+'.html','utf8');
    assert.ok(room.includes(escape(record.short)));
    assert.ok(room.includes(escape(record.question)));
  }
  // The exact D029 subtraction is historical; D030 adds an orientation spine.
  assert.equal(execFileSync('git',['show','57a86af13399916825570fbfb51e19b734ac71a8:index.html']).toString('utf8'),expected);
  const oldChange = execFileSync('git',['show',parent+':explore/nodes/change.html']).toString('utf8');
  const change = await readFile('out/explore/nodes/change.html','utf8');
  assert.equal(change,oldChange.replace('<a href="/#step-understand">Understand route</a>',''));
  assert.doesNotMatch(html+change,/step-understand/);
  const future = html.split('<section data-step="future"')[1].split('</section>')[0];
  const priorHtml = execFileSync('git',['show',parent+':index.html']).toString('utf8');
  assert.equal(future,priorHtml.split('<section data-step="future"')[1].split('</section>')[0]);
  assert.deepEqual(await readFile('out/journey.js'),execFileSync('git',['show',parent+':journey.js']));
  assert.doesNotMatch(await readFile('downloads/Campfire-preview.html','utf8'),/step-understand|<script\b/);
  const challenge = await readFile('public/explore/challenge.md','utf8');
  const statement = challenge.split('## Challenge the content')[1].split('## ')[0].trim();
  assert.ok(html.split('id="step-challenge"')[1].split('</section>')[0].includes(escape(statement)));
  const look = html.split('id="step-look"')[1].split('</section>')[0];
  assert.deepEqual([...look.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['/works/','#step-story']);
});
