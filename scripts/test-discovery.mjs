import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,access} from 'node:fs/promises';
import path from 'node:path';
const html=await readFile('out/index.html','utf8');

test('D072 exposes the current separate Human Record route with bounded standing',()=>{
 assert.match(html,/href="https:\/\/thehumanrecord.net\/"/);
 assert.match(html,/four public records/);
 assert.match(html,/artwork provenance/);
 assert.match(html,/living-practice transmission-lineage/);
 assert.match(html,/historical-person source-survival/);
 assert.match(html,/not accepted/);
 assert.match(html,/not evidence for TRACE or Mechanical Ethics/);
});

test('released core aliases carry the released status without validation upgrade',async()=>{
 const trace=await readFile('out/resources/trace/README.md','utf8');
 const me=await readFile('out/resources/mechanical-ethics/README.md','utf8');
 assert.match(trace,/TRACE v0\.4\.0 is the current released formal baseline/);
 assert.match(trace,/NOT VALIDATED/);
 assert.match(me,/Mechanical Ethics v0\.8\.0 is the current released formal baseline/);
 assert.match(me,/NOT VALIDATED/);
});


test('Explore keeps historical source basis separate from current repository routes',async()=>{
 const sources=JSON.parse(await readFile('out/explore/sources.json','utf8')).sources;
 assert.equal(sources.trace.commit,'46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b');
 assert.equal(sources.me.commit,'44f7efb59806242fd26c572cbfbaaeaefaea2058');
 assert.match(sources.trace.label,/source snapshot/);
 assert.match(sources.me.label,/source snapshot/);
 assert.equal(sources['trace-home'].commit,'6c68fae8cbc51d0ef1e77a18e220ceb7a1207025');
 assert.equal(sources['me-home'].commit,'e2ef746e931161cb70ac46a4eaa122442134e86b');
 assert.match(sources['trace-home'].label,/current-source route/);
 assert.match(sources['me-home'].label,/current-source route/);
 const packet=JSON.parse(await readFile('out/explore/packet.json','utf8')).sources;
 assert.deepEqual(packet,sources);

 const manifest=JSON.parse(await readFile('out/manifest.json','utf8'));
 const traceRepo=manifest.source_repositories.find(x=>x.name==='TRACE');
 const meRepo=manifest.source_repositories.find(x=>x.name==='Mechanical Ethics');
 assert.equal(traceRepo.human_preview_source_revision,'46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b');
 assert.equal(meRepo.human_preview_source_revision,'44f7efb59806242fd26c572cbfbaaeaefaea2058');
});

test('root metadata names only the first-party canonical origin',()=>{
 assert.match(html,/<link rel="canonical" href="https:\/\/pleasestartfromhere.com\/"/);
 for(const field of ['title','description','url','type'])assert.equal((html.match(new RegExp('property="og:'+field+'"','g'))||[]).length,1);
});

test('D078 history and current edition agree',async()=>{
 const m=JSON.parse(await readFile('out/manifest.json'));
 assert.equal(m.site_edition,'0.8.35');
 assert.equal(m.updated,'2026-09-23');
 const md=await readFile('out/changes.md','utf8');
 const rendered=await readFile('out/changes.html','utf8');
 for(const [id,date] of [['D078','23 September 2026'],['D077','23 September 2026'],['D076','23 September 2026'],['D075','23 September 2026'],['D074','23 September 2026'],['D073','23 September 2026'],['D072','18 September 2026'],['D071','18 September 2026'],['D070','18 September 2026'],['D069','18 September 2026'],['D068','15 September 2026']]){
   assert.match(md,new RegExp('### '+id+'\\s+'+date));
   assert.match(rendered,new RegExp('<h3 id="'+id.toLowerCase()+'">'+id+'<\\/h3>'));
 }
});

test('homepage local href and src paths exist',async()=>{
 for(const [,raw] of html.matchAll(/(?:href|src)="([^"]+)"/g)){
  const u=new URL(raw,'https://pleasestartfromhere.com/');if(u.origin!=='https://pleasestartfromhere.com')continue;
  const file=decodeURIComponent(u.pathname).replace(/^\//,'');await access(path.join('out',file.endsWith('/')?file+'index.html':file||'index.html'));
 }
});
