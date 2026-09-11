import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { VIEWS } from './source-views.mjs';

const parent = '4bf08436a917ab2c31881a035fa223fc57bbfb6b';
const old = file => execFileSync('git',['show',parent+':public/'+file],{encoding:'utf8'});
const sha = bytes => createHash('sha256').update(bytes).digest('hex');

test('arrival preserves the D022 wording changes and adds only the D034 project topology', async () => {
  const before = JSON.parse(old('explore/start.json'));
  const bytes = await readFile('public/explore/start.json');
  const after = JSON.parse(bytes);
  assert.equal(sha(bytes),'3073bc5014c289ac7959c6f7a8b0e92047d87b99b01e5e89baa4b964f555a3a5');
  assert.equal(Buffer.byteLength(bytes),2768);
  for (const key of ['question','invitation']) {
    assert.notEqual(before.greeting[key],after.greeting[key]);
    before.greeting[key] = after.greeting[key];
  }
  assert.notEqual(before.reading,after.reading);
  before.reading = after.reading;

  const parts = after.project_parts;
  delete after.project_parts;
  const addedRoutes = {};
  for (const key of ['mechanical_ethics','trace','trace_compact']) {
    addedRoutes[key] = after.routes[key];
    delete after.routes[key];
  }
  assert.deepEqual(after,before);
  assert.deepEqual(parts,{
    mechanical_ethics:'Human-facing framework for consequential decisions under uncertainty, especially where formal correction can arrive after a threatened path has hardened.',
    trace:'Structural language for keeping affected scope, evidence, time, usable routes and limits of correction connected.',
    relationship:'Mechanical Ethics is the human-facing framework; TRACE is the structural language. They are related, not a compulsory combined workflow. Neither grants authority, and another method may serve better.'
  });
  assert.deepEqual(addedRoutes,{
    mechanical_ethics:'../resources/mechanical-ethics/README.md',
    trace:'../resources/trace/README.md',
    trace_compact:'../resources/trace/TRACE-SPINE.md'
  });
  for (const route of Object.values(JSON.parse(bytes).routes)) await readFile('out/explore/'+route);
  const resourceMap = JSON.parse(await readFile('public/explore/map.json'));
  assert.deepEqual(resourceMap.resources.find(resource=>resource.path==='start.json'),{
    path:'start.json', bytes:2768, sha256:'3073bc5014c289ac7959c6f7a8b0e92047d87b99b01e5e89baa4b964f555a3a5'
  });
  assert.match(before.reading,/No automatic traversal or report-back/);
});

test('both source pins survive integration and describe the revised editions', async () => {
  for (const [source,expected] of [
    ['explore/start.json','3073bc5014c289ac7959c6f7a8b0e92047d87b99b01e5e89baa4b964f555a3a5'],
    ['llms.txt','fc182abcc176e23fe12eb1c470110a1e01cf61be2874033215b84ec403ba94e0'],
  ]) {
    const view = VIEWS.find(v=>v.source===source);
    assert.equal(view.sha256,expected);
    assert.equal(sha(await readFile('out/'+source)),expected);
    assert.match(view.edition,source==='llms.txt'?/D033/:/D034/);
    assert.doesNotMatch(view.edition,/publishing ba181/);
    const html = await readFile('out/'+view.output,'utf8');
    assert.ok(html.includes(expected));
  }
  const startView = await readFile('out/read/start.html','utf8');
  for (const href of [
    'https://pleasestartfromhere.com/resources/mechanical-ethics/README.md',
    'https://pleasestartfromhere.com/resources/trace/README.md',
    'https://pleasestartfromhere.com/read/trace-spine.html'
  ]) assert.ok(startView.includes('href="'+href+'"'), href);
});

test('indexes retain existing links, expose summaries first and route six prompts separately', async () => {
  const links = s=>[...s.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)].map(m=>m[1]).sort();
  for (const file of ['llms.txt','explore/llms.txt']) {
    const text = await readFile('out/'+file,'utf8');
    assert.match(text,/^# [^\n]+\r?\n\s*\r?\n> /);
    const expected = links(old(file));
    if (file==='llms.txt') expected.push('https://pleasestartfromhere.com/#small-loop');
    assert.deepEqual(links(text),expected.sort());
    for (const section of text.split(/^## /m).slice(1)) {
      for (const line of section.split(/\r?\n/).slice(1).filter(l=>l.trim())) {
        assert.match(line,/^- \[[^\]]+\]\(https:\/\/[^)]+\)/);
      }
    }
  }
  const root = await readFile('out/llms.txt','utf8');
  assert.equal(Buffer.byteLength(root),5416);
  assert.equal(root.split('## Start')[0].trim().split(/\s+/).length,306);
  const home = await readFile('out/index.html','utf8');
  const cell = home.split('id="small-loop"')[1].split('</section>')[0];
  for (const label of ['Notice','Choose','Decide','Responsibility','Repercussions','Check and correct']) {
    assert.ok(cell.includes('<strong>'+label+'.</strong>'));
  }
  assert.equal((cell.match(/<li>/g)||[]).length,6);
});

test('shared root keeps compatibility without adding a destination', async()=>{
 const m=JSON.parse(await readFile('out/manifest.json'));
 assert.equal(m.routes.shared_reading,'/'); assert.equal(m.routes.human_reading,'/');
 assert.match(await readFile('out/llms.txt','utf8'),/\[Shared web reading\]\(https:\/\/pleasestartfromhere.com\/\)/);
});
