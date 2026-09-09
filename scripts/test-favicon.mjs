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
const baseline = '965687ee60552e11e25e5c9f797edc7f8b947dcd';
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

test('relative to published0.8.4 only the root head and three icon assets change', async () => {
  let checked=0;
  async function walk(dir,prefix='') {
    for (const item of await readdir(dir,{withFileTypes:true})) {
      const file=prefix+item.name;
      if(item.isDirectory()){await walk(dir+'/'+item.name,file+'/');continue;}
      if(file in pins)continue;
      const before=execFileSync('git',['show',baseline+':'+file],{cwd:publishing,maxBuffer:20*1024*1024});
      let actual=await readFile('out/'+file);
      if(file==='index.html'){
        const text=actual.toString();
        assert.equal(text.split(header).length,2);
        assert.ok(text.indexOf(header)<text.indexOf('</head>'));
        actual=Buffer.from(text.replace(header,''));
      }
      assert.deepEqual(actual,before,file);checked++;
    }
  }
  await walk('out');assert.equal(checked,115);
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
