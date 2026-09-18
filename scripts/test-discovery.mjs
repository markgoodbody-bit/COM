import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,access} from 'node:fs/promises';
import path from 'node:path';
const html=await readFile('out/index.html','utf8');

test('D070 exposes the current separate Human Record route with bounded standing',()=>{
 assert.match(html,/href="https:\/\/thehumanrecord.net\/"/);
 assert.match(html,/three public records/);
 assert.match(html,/artwork provenance/);
 assert.match(html,/living-practice transmission-lineage/);
 assert.match(html,/not accepted/);
 assert.match(html,/not evidence for TRACE or Mechanical Ethics/);
});

test('released core aliases carry the released status without validation upgrade',async()=>{
 const trace=await readFile('out/resources/trace/README.md','utf8');
 const me=await readFile('out/resources/mechanical-ethics/README.md','utf8');
 assert.match(trace,/released TRACE v0\.3\.0 specification/);
 assert.match(trace,/NOT VALIDATED/);
 assert.match(me,/released Mechanical Ethics v0\.7\.0 baseline/);
 assert.match(me,/NOT VALIDATED/);
});


test('Explore keeps historical source basis separate from current repository routes',async()=>{
 const sources=JSON.parse(await readFile('out/explore/sources.json','utf8')).sources;
 assert.equal(sources.trace.commit,'46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b');
 assert.equal(sources.me.commit,'44f7efb59806242fd26c572cbfbaaeaefaea2058');
 assert.match(sources.trace.label,/source snapshot/);
 assert.match(sources.me.label,/source snapshot/);
 assert.equal(sources['trace-home'].commit,'8310d2531d3b2fe4e3b44c92d1d544a322f52bf4');
 assert.equal(sources['me-home'].commit,'25a9d793af1cded26dd2d766e1d1c08e1b30f652');
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

test('D068-D070 history and current edition agree',async()=>{
 const m=JSON.parse(await readFile('out/manifest.json'));
 assert.equal(m.site_edition,'0.8.27');
 assert.equal(m.updated,'2026-09-18');
 const md=await readFile('out/changes.md','utf8');
 const rendered=await readFile('out/changes.html','utf8');
 for(const [id,date] of [['D070','18 September 2026'],['D069','18 September 2026'],['D068','15 September 2026']]){
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
