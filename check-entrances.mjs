import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {VIEWS,digest,renderSource,sourceReferences} from './scripts/source-views.mjs';
const page=await readFile('app/page.tsx','utf8');
assert.match(page,/Current released sources:/);assert.match(page,/TRACE v0\.5\.0/);assert.match(page,/Mechanical Ethics v1\.0\.0/);
assert.doesNotMatch(page,/Current released reading copies:/);
const start=JSON.parse(await readFile('public/explore/start.json','utf8'));
const manifest=JSON.parse(await readFile('public/manifest.json','utf8'));
assert.equal(manifest.current_released_sources.mechanical_ethics.book,start.routes.mechanical_ethics);
assert.equal(manifest.current_released_sources.trace.specification,start.routes.trace);
assert.equal(manifest.current_released_sources.as_of,'2026-11-06');
assert.match(page,/historical local edition/);
const map=JSON.parse(await readFile('public/explore/map.json','utf8'));
const declared=map.resources.find(x=>x.path==='start.json');const raw=await readFile('public/explore/start.json');
assert.equal(declared.bytes,raw.length);assert.equal(declared.sha256,digest(raw));
await mkdir('focused-output',{recursive:true});
for(const view of VIEWS.filter(x=>['llms.txt','explore/start.json'].includes(x.source))){
 const bytes=await readFile('public/'+view.source);assert.equal(view.sha256,digest(bytes));
 const refs=sourceReferences(view,bytes.toString('utf8')).map(([label,url])=>[label,url.href]);
 const html=renderSource(view,bytes,refs);
 assert(html.includes(view.sha256));
 await writeFile('focused-output/'+view.output.split('/').pop(),html);
}
console.log('Human/source route consistency, machine parity, map hashes and two real source-view renders PASS');
