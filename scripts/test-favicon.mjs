import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile, readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {createPreviewServer} from './serve.mjs';

const pins = {
  'favicon.svg': 'b2b950c89165e9c483853e608312f341ceceadb5c05958fd0be4ed77e9b9bd70',
  'favicon.ico': '2e7f27bab62301c5d5d27bf6802faf28753623a228c83abe4f66e5e80731a70e',
  'favicon-LICENSE.txt': '2d0c0cfe9630fcbf019e48b11349d220970e86a38fe05f06854321ee237d56b9',
};
const publishing = process.env.PSFH_PUBLISHED_CHECKOUT || 'C:/Users/markg/Downloads/DEV/campfire-door-pages';
const header = '<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml" sizes="any">';

test('favicon assets, legacy sizes and source notice have exact identities', async () => {
  for (const [file,pin] of Object.entries(pins)) {
    const bytes = await readFile('out/' + file);
    assert.equal(createHash('sha256').update(bytes).digest('hex'),pin,file);
  }
  const ico = await readFile('out/favicon.ico');
  assert.equal(ico.readUInt16LE(0),0); assert.equal(ico.readUInt16LE(2),1);
  assert.equal(ico.readUInt16LE(4),3);
  [16,32,48].forEach((size,i) => {
    const p=6+i*16, offset=ico.readUInt32LE(p+12), count=ico.readUInt32LE(p+8);
    assert.equal(ico[p],size); assert.equal(ico[p+1],size);
    assert.deepEqual(ico.subarray(offset,offset+8),Buffer.from([137,80,78,71,13,10,26,10]));
    assert.equal(ico.readUInt32BE(offset+16),size); assert.equal(ico.readUInt32BE(offset+20),size);
    assert.ok(offset+count<=ico.length);
  });
});

test('contextual art changes only two entrances, map identities, CSS and explicit bypasses', async () => {
  const published = '5af680b5f7016f4198b8819f2b9ed93d568eb1c3';
  let checked = 0, changed = [];
  async function walk(dir, prefix = '') {
    for (const item of await readdir(dir, {withFileTypes: true})) {
      const file = prefix + item.name;
      if (item.isDirectory()) { await walk(dir + '/' + item.name, file + '/'); continue; }
      const before = execFileSync('git', ['show', published + ':' + file], {cwd: publishing, maxBuffer: 20*1024*1024});
      const actual = await readFile('out/' + file);
      if (!actual.equals(before)) changed.push(file);
      if (file === 'index.html') {
        const html = actual.toString();
        assert.equal(html.split(header).length, 2);
        assert.ok(html.indexOf(header) < html.indexOf('</head>'));
        assert.match(html, /<a class="map-bypass" href="\/explore\/#reading-map">Just give me the map/);
        assert.match(html, /<h1>Please Start From <em>Here<\/em><\/h1>/);
        const old = before.toString();
        assert.equal((html.match(/href="\/explore\/#reading-map"/g) ?? []).length, 4);
        assert.equal(html.replaceAll('href="/explore/#reading-map"', 'href="/explore/"'), old);
      } else if (['explore/index.html', 'explore/nodes/futures.html'].includes(file)) {
        const oldBody = before.toString().split('<body>')[1];
        const unchanged = actual.toString().split('</section><main id="reading">')[1]
          .replace('<nav id="reading-map" aria-label="Optional routes">', '<nav aria-label="Optional routes">');
        assert.equal('<main>' + unchanged, oldBody, file);
        assert.doesNotMatch(actual.toString(), /<script\b|<form\b|<iframe\b/i);
      } else if (file === 'explore/map.json') {
        const map = JSON.parse(actual), prior = JSON.parse(before);
        for (const item of map.resources) {
          if (!['index.html','nodes/futures.html'].includes(item.path)) continue;
          const bytes = await readFile('out/explore/' + item.path);
          assert.equal(item.sha256, createHash('sha256').update(bytes).digest('hex'));
          assert.equal(item.bytes, bytes.length);
          Object.assign(item, prior.resources.find(p => p.path === item.path));
        }
        assert.deepEqual(map, prior);
      } else if (file === 'style.css') {
        assert.equal(actual.toString(), await readFile('app/globals.css', 'utf8'));
      } else if (file === 'manifest.json') {
        const map = JSON.parse(actual), oldMap = JSON.parse(before);
        assert.equal(map.provenance.presentation.stylesheet_sha256, createHash('sha256').update(await readFile('out/style.css')).digest('hex'));
        map.provenance.presentation.stylesheet_sha256 = oldMap.provenance.presentation.stylesheet_sha256;
        for (const [field, source] of [['change_history_sha256','public/changes.md'], ['change_history_input_html_sha256','public/changes.html'], ['change_history_html_sha256','out/changes.html']]) {
          assert.equal(map.provenance[field], createHash('sha256').update(await readFile(source)).digest('hex'));
          map.provenance[field] = oldMap.provenance[field];
        }
        assert.equal(map.provenance.change_history_previous_source_commit, '55b9690d7a45a313871e1b5fbbfc64083c4b1ebd');
        map.provenance.change_history_previous_source_commit = oldMap.provenance.change_history_previous_source_commit;
        assert.equal(map.provenance.change_history_addendum_note, 'D016 is a manually paired Markdown/HTML entry; earlier generator identity applies to the preserved older entries.');
        delete map.provenance.change_history_addendum_note;
        assert.deepEqual(map, oldMap);
      } else if (['changes.md','changes.html'].includes(file)) {
        const text = actual.toString(), old = before.toString();
        const marker = file.endsWith('.md') ? '### D015' : '<h3 id="d015">';
        assert.equal(text.slice(text.indexOf(marker)), old.slice(old.indexOf(marker)));
        assert.ok(text.includes('D016'));
        assert.ok(text.includes('5af680b5f7016f4198b8819f2b9ed93d568eb1c3'));
      } else assert.deepEqual(actual, before, file);
      checked++;
    }
  }
  await walk('out');
  assert.equal(checked, 154);
  assert.deepEqual(changed.sort(), ['changes.html', 'changes.md', 'explore/index.html', 'explore/map.json', 'explore/nodes/futures.html', 'index.html', 'manifest.json', 'style.css']);
});

test('preview serves SVG and ICO with their image MIME types', async () => {
  const server=await createPreviewServer();
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  try{
    const base='http://127.0.0.1:'+server.address().port;
    for(const [file,type] of [['favicon.svg','image/svg+xml'],['favicon.ico','image/x-icon']]){
      const response=await fetch(base+'/'+file);
      assert.equal(response.status,200);assert.equal(response.headers.get('content-type'),type);
      assert.deepEqual(Buffer.from(await response.arrayBuffer()),await readFile('out/'+file));
    }
  }finally{await new Promise(resolve=>server.close(resolve));}
});
