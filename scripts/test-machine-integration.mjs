import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { VIEWS } from './source-views.mjs';

const parent = '4bf08436a917ab2c31881a035fa223fc57bbfb6b';
const old = file => execFileSync('git',['show',parent+':public/'+file],{encoding:'utf8'});
const sha = bytes => createHash('sha256').update(bytes).digest('hex');

test('arrival changes only the three reviewed text fields and preserves routes and limits', async () => {
  const before = JSON.parse(old('explore/start.json'));
  const bytes = await readFile('public/explore/start.json');
  const after = JSON.parse(bytes);
  assert.equal(sha(bytes),'f0e693b82e07195df049d1f6df2c5f62b0025518f55194088fa01bc79d19fb10');
  for (const key of ['question','invitation']) {
    assert.notEqual(before.greeting[key],after.greeting[key]);
    before.greeting[key] = after.greeting[key];
  }
  assert.notEqual(before.reading,after.reading);
  before.reading = after.reading;
  assert.deepEqual(after,before);
  for (const route of Object.values(after.routes)) await readFile('out/explore/'+route);
  assert.match(after.reading,/No automatic traversal or report-back/);
});

test('both source pins survive integration and describe the revised editions', async () => {
  for (const [source,expected] of [
    ['explore/start.json','f0e693b82e07195df049d1f6df2c5f62b0025518f55194088fa01bc79d19fb10'],
    ['llms.txt','b7afcebea95ccb32fe1fc072f9199bc29ade7a482beeeb8b2eb1502b46de3fcd'],
  ]) {
    const view = VIEWS.find(v=>v.source===source);
    assert.equal(view.sha256,expected);
    assert.equal(sha(await readFile('out/'+source)),expected);
    assert.match(view.edition,/D022/);
    assert.doesNotMatch(view.edition,/publishing ba181/);
    const html = await readFile('out/'+view.output,'utf8');
    assert.ok(html.includes(expected));
  }
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
  assert.equal(Buffer.byteLength(root),5383);
  assert.equal(root.split('## Start')[0].trim().split(/\s+/).length,305);
  const home = await readFile('out/index.html','utf8');
  const cell = home.split('id="small-loop"')[1].split('</section>')[0];
  for (const label of ['Notice','Choose','Decide','Responsibility','Repercussions','Check and correct']) {
    assert.ok(cell.includes('<strong>'+label+'.</strong>'));
  }
  assert.equal((cell.match(/<li>/g)||[]).length,6);
});
