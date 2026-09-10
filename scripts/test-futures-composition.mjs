import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {addArtRoom, ROOMS} from './contextual-art.mjs';

const parent = '20559a4955e965073312008bdd31a8e147585081';
const previous = await import('data:text/javascript;base64,' + execFileSync('git',['show',parent+':scripts/contextual-art.mjs']).toString('base64'));
const assets = async room => [JSON.parse(await readFile('public/art/'+room.key+'.json')),JSON.parse(await readFile('public/art/'+room.key+'-images.json'))];

test('art wrapper preserves exact old static output and merges controlled template attributes', async () => {
  for (const room of ROOMS) {
    const [record,images] = await assets(room);
    const source = await readFile('public/'+room.page,'utf8');
    assert.equal(addArtRoom(source,room,record,images),previous.addArtRoom(source,room,record,images));
    const fixture = '<body class="reader" style="padding:0" data-purpose="reading"><main aria-label="Reading">text</main></body>';
    const wrapped = addArtRoom(fixture,room,record,images);
    assert.match(wrapped,/<body class="reader contextual-room" style="padding:0" data-purpose="reading">/);
    assert.match(wrapped,/<main aria-label="Reading" id="reading">/);
    assert.throws(()=>addArtRoom(wrapped,room,record,images),/already present/);
    for (const bad of ['<body><main id="other">x</main></body>','<body class=reader><main>x</main></body>','<body class="a" class="b"><main>x</main></body>','<body><main>x</main><main>y</main></body>']) assert.throws(()=>addArtRoom(bad,room,record,images),/template/);
  }
});

test('Futures composes one unchanged art entrance before the complete reading', async () => {
  const html = await readFile('out/explore/nodes/futures.html','utf8');
  const before = execFileSync('git',['show','37e3a92dbe361811dfeae45507f53d5125db9194:explore/nodes/futures.html']).toString('utf8');
  const art = s => s.match(/<section class="art-room art-room-shen"[\s\S]*?<\/section>/)[0];
  assert.equal(art(html),art(before));
  for (const token of ['class="art-room art-room-shen"','<figure>','id="reading"','id="question"']) assert.equal(html.split(token).length-1,1,token);
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(ids.length,new Set(ids).size);
  assert.match(html,/<body style="max-width:none;padding:0" class="contextual-room">/);
  assert.ok(html.indexOf('<figure>') < html.indexOf('<article'));
  assert.ok(html.indexOf('>Go straight to the reading</a>') < html.indexOf('<figure>'));
  assert.ok(html.indexOf('</section>') < html.indexOf('>Skip to the question</a>'));
  assert.ok(html.indexOf('>Skip to the question</a>') < html.indexOf('id="question"'));
  assert.doesNotMatch(html,/data-reading-kind|<script\b/);
  assert.match(html,/<details id="full-account">/);
});
