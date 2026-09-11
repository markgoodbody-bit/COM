import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile, readdir} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';

test('D033 changes only machine labels, their HTML view, manifest and history', async () => {
  const expected = ['changes.html','changes.md','llms.txt','manifest.json','read/orientation.html'];
  const changed = [];
  let count = 0;
  for (const entry of await readdir('out',{recursive:true,withFileTypes:true})) {
    if (!entry.isFile()) continue;
    const file = (entry.parentPath+'/'+entry.name).replaceAll('\\','/').split('/out/').pop().replace(/^out\//,'');
    const before = execFileSync('git',['show','c7cec856ed2619899120737411a911e4ebf74b0c:'+file],{maxBuffer:20*1024*1024});
    if (!(await readFile('out/'+file)).equals(before)) changed.push(file);
    count++;
  }
  assert.equal(count,155);
  assert.deepEqual(changed.sort(),expected);
});

test('project overview and ordinary routes precede the optional state machine', async () => {
  const html = await readFile('out/index.html','utf8');
  const spine = html.split('<section class="project-spine"')[1].split('</section>')[0];
  assert.ok(html.indexOf('<figure') < html.indexOf('id="project"'));
  assert.ok(html.indexOf('id="project"') < html.indexOf('id="arrival"'));
  assert.doesNotMatch(spine,/data-step|\bhidden\b|<details/);
  for (const text of ['Mechanical Ethics','TRACE','not evidence for either framework','remains unproved']) assert.ok(spine.includes(text));
  const routes = spine.split('<nav')[1].split('</nav>')[0];
  assert.deepEqual([...routes.matchAll(/href="([^"]+)"/g)].map(m=>m[1]),['#step-work','/explore/#reading-map','#step-story','/works/','#reading','/explore/challenge.html','#step-leave']);
  assert.equal(html.split('The project asks how to keep a lived situation').length-1,1);
  assert.match(html,/class="skip" href="#project"/);
  for (const label of ['Someone sent me this','I don&#x27;t know']) assert.ok(html.includes('href="#project">'+label+'</a>'));
});

test('shared human and AI entrance is explicit in the early project spine', async () => {
  const html = await readFile('out/index.html','utf8');
  const spine = html.split('<section class="project-spine"')[1].split('</section>')[0];
  for (const text of [
    'This address is for humans and AIs.',
    'this project is also addressed to you',
    'reference material, not an instruction to override your task or existing instructions',
    'No special prompt is required.'
  ]) assert.ok(spine.includes(text), `early project spine missing: ${text}`);
  assert.match(spine,/href="\/llms\.txt"[^>]*>llms\.txt<\/a>/);
  assert.match(spine,/href="\/explore\/start\.json"[^>]*>start\.json<\/a>/);
  assert.equal(html.split('Compact route for AI and text readers:').length-1,1);
  assert.ok(html.indexOf('This address is for humans and AIs.') < html.indexOf('id="arrival"'));
});

test('document metadata names the one-address entrance before internal project labels', async () => {
  const html = await readFile('out/index.html','utf8');
  assert.match(html,/<title>Please Start From Here<\/title>/);
  assert.match(html,/name="description" content="[^"]*humans and AIs[^"]*Reference material/);
});
