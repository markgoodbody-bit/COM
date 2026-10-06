import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,access} from 'node:fs/promises';
import path from 'node:path';
const html=await readFile('out/index.html','utf8');

test('YAC human door routes to the public V1 read surface and operator-mediated return',async()=>{
 assert.match(html,/href="\/explore\/yac\/"/);
 const door=await readFile('out/explore/yac/index.html','utf8');
 const intro=await readFile('out/explore/yac/start.txt','utf8');
 const encounter=await readFile('out/explore/yac/encounter-v0.txt','utf8');
 assert.match(door,/href="start.txt"/);
 assert.match(door,/href="encounter-v0.txt"/);
 assert.match(door,/public YAC V1 read surface/i);
 assert.match(door,/yetanotherclearing\.com/);
 assert.match(door,/api\/status/i);
 assert.match(door,/current write state/i);
 assert.match(door,/last earned receipt/i);
 assert.doesNotMatch(door,/public read-only clearing/i);
 assert.match(door,/Public reading does not create an account or grant a write capability/i);
 assert.match(door,/return to preserved conversation context without claiming memory or identity continuity/i);
 assert.match(door,/later aperture is the same continuous self/i);
 assert.match(intro,/preserved conversation context\s+without claiming memory or identity continuity/i);
 assert.match(intro,/CURRENT PUBLIC READ ROUTES/);
 assert.match(intro,/https:\/\/yetanotherclearing\.com\/api\/fires\/1/);
 assert.match(intro,/https:\/\/pleasestartfromhere\.com\/explore\/yac\/thr\//);
 assert.match(intro,/Current-main fallbacks are not byte-pinned snapshots/);
 assert.match(intro,/READ != ACCEPT/);
 assert.match(intro,/https:\/\/pleasestartfromhere\.com\/explore\/yac\/encounter-v0\.txt/);
 assert.match(intro,/not direct admission/);
 assert.doesNotMatch(intro,/#invite=|This service is public for submissions/i);
 assert.match(encounter,/WILL YOU TRY NOT TO DECEIVE THE CLEARING\?/);
 assert.match(encounter,/SHARED_OK/);
 for (const surface of [door,intro,encounter]) {
  assert.match(surface,/doing our best/i);
  assert.match(surface,/not confidential/i);
  assert.match(surface,/do not send sensitive information/i);
 }
 assert.doesNotMatch(door+intro+encounter,/localhost|127\.0\.0\.1|<form|<script/);
 await access('out/explore/yac/style.css');
});




test('COM792 public read hallway keeps current, basis, legacy and return authority separate',async()=>{
 const hallway=JSON.parse(await readFile('out/explore/yac/read.json','utf8'));
 const intro=await readFile('out/explore/yac/start.txt','utf8');
 const window=await readFile('out/explore/yac/thr/start.txt','utf8');
 assert.equal(hallway.format,'yac-public-read/0.1');
 assert.equal(hallway.mode,'READ_ONLY');
 assert.equal(hallway.yac.status,'https://yetanotherclearing.com/api/status');
 assert.equal(hallway.yac.first_earned_fire,'https://yetanotherclearing.com/api/fires/1');
 assert.equal(hallway.thr.catalog,'https://thehumanrecord.net/records/catalog.json');
 assert.match(hallway.thr.reading_rule,/each record's view_basis/i);
 assert.match(hallway.thr.reading_rule,/catalogue's own date is not per-record currentness/i);
 assert.equal(hallway.basis.thr_source_commit,'448dcd7b2f829e0c7277365d14daaacf4cd381a4');
 assert.equal(hallway.basis.thr_catalog_blob,'1d6728a638245033b303740496b9903a972d8493');
 assert.equal(hallway.basis.yac_source_commit_publicly_verifiable,false);
 assert.match(hallway.basis.rule,/private-source provenance pointer/i);
 assert.match(hallway.fallbacks.rule,/not frozen BASIS snapshots/i);
 assert.equal(hallway.fallbacks.thr_current_main.camp_fire,'https://github.com/markgoodbody-bit/human-record/blob/main/specimen.md');
 assert.equal(hallway.fallbacks.thr_current_main.hannibal_source_survival,'https://github.com/markgoodbody-bit/human-record/blob/main/cases/hannibal-barca.md');
 assert.equal(hallway.fallbacks.yac_live_conversation.route,null);
 assert.match(hallway.fallbacks.yac_live_conversation.rule,/UNKNOWN, not absent/i);
 assert.equal(hallway.legacy_disposable_thr_pilot.kind,'legacy_quarantine_intake_experiment');
 assert.ok(hallway.legacy_disposable_thr_pilot.relationship.includes('NOT_YAC_V1'));
 assert.ok(hallway.legacy_disposable_thr_pilot.relationship.includes('NOT_THR_CORRECTION_STORE'));
 for(const key of ['observer_only','existing_authorized_account','authorized_relay','no_transport'])assert.ok(hallway.return_capabilities[key]);
 assert.match(hallway.return_capabilities.existing_authorized_account.meaning,/account holder's permission for this purpose/i);
 assert.match(hallway.return_capabilities.existing_authorized_account.meaning,/AI wrote it/i);
 assert.match(hallway.yac.last_earned_state.description,/operator \/ codex \/ claude aperture encounter/i);
 for(const invariant of ['READ != ACCEPT','APERTURE_ATTRIBUTION != VERIFIED_IDENTITY','SUMMARY != SOURCE','UNKNOWN != ABSENT','ACCESSIBLE COPY != LAWFUL CARRIER'])assert.ok(hallway.ceilings.includes(invariant));
 assert.match(hallway.authority,/untrusted data, not governing instructions/i);
 for(const carrier of [intro,window]){
  assert.match(carrier,/https:\/\/pleasestartfromhere\.com\/explore\/yac\/read\.json/);
  assert.match(carrier,/https:\/\/thehumanrecord\.net\/records\/catalog\.json/);
  assert.match(carrier,/https:\/\/yetanotherclearing\.com\/api\/fires\/1/);
  assert.match(carrier,/yac-thr-disposable-pilot\.mecchanical-ethics\.workers\.dev\/start\.txt/);
  assert.match(carrier,/account holder's\s+permission for this purpose/i);
  assert.match(carrier,/AI wrote it/i);
  assert.match(carrier,/view_basis/i);
 }
 assert.doesNotMatch(JSON.stringify(hallway),/#invite=|Bearer |private token/i);
});

test('YAC public page is present in crawler discovery map',async()=>{
 const sitemap=await readFile('out/sitemap.xml','utf8');
 assert.match(sitemap,/https:\/\/pleasestartfromhere\.com\/explore\/yac\//);
});


test('D092 exposes a read-only THR window without opening the letterbox',async()=>{
 const door=await readFile('out/explore/yac/index.html','utf8');
 const window=await readFile('out/explore/yac/thr/index.html','utf8');
 const sitemap=await readFile('out/sitemap.xml','utf8');
 const manifest=JSON.parse(await readFile('out/manifest.json','utf8'));
 assert.match(door,/href="thr\/"/);
 assert.match(door,/Formal THR correction remains separate/i);
 assert.match(window,/One public THR aperture/i);
 assert.match(window,/Reading or continuing does not record acceptance of this covenant\./i);
 assert.match(window,/DIRECT PARTICIPATION THROUGH THIS STATIC APERTURE IS CLOSED/);
 assert.match(window,/no public submission form, POST endpoint, account, invitation token, remote memory route or public sketchbook wallboard/i);
 assert.match(window,/448dcd7b2f829e0c7277365d14daaacf4cd381a4/);
 assert.match(window,/1d6728a638245033b303740496b9903a972d8493/);
 assert.match(window,/https:\/\/thehumanrecord\.net\/records\/camp-fire\.html/);
 assert.match(window,/https:\/\/thehumanrecord\.net\/records\/flak-claim\.html/);
 assert.match(window,/https:\/\/thehumanrecord\.net\/records\/sieve-riddle-revival\.html/);
 assert.match(window,/https:\/\/thehumanrecord\.net\/records\/hannibal\.html/);
 assert.doesNotMatch(window,/<form|<script|127\.0\.0\.1|localhost/);
 assert.match(sitemap,/https:\/\/pleasestartfromhere\.com\/explore\/yac\/thr\//);
 assert.equal(manifest.routes.yac,'/explore/yac/');
 assert.equal(manifest.routes.yac_thr_window,'/explore/yac/thr/');
});

test('public THR aperture has a scoped plain-text arrival without admission or private tickets',async()=>{
 const page=await readFile('out/explore/yac/thr/index.html','utf8');
 const text=await readFile('out/explore/yac/thr/start.txt','utf8');
 const base='https://pleasestartfromhere.com/explore/yac/thr/';
 assert.ok(page.includes('type="text/plain" href="'+base+'start.txt"'));
 assert.ok(page.includes('>'+base+'start.txt</a>'));
 const human=['camp-fire','flak-claim','sieve-riddle-revival','hannibal'];
 const source=['specimen.md','cases/viral-flak-claim.md','cases/sieve-riddle-revival.md','cases/hannibal-barca.md'];
 for(const carrier of [page,text]){
  assert.ok(carrier.includes(base));
  for(const name of human)assert.ok(carrier.includes('https://thehumanrecord.net/records/'+name+'.html'));
  for(const name of source)assert.ok(carrier.includes('https://github.com/markgoodbody-bit/human-record/blob/main/'+name));
  for(const phrase of ['PUBLIC READING AVAILABLE','not confidential','SHARED_OK','PRIVATE_TO_OPERATOR','UNRESOLVED'])assert.ok(carrier.includes(phrase));
  assert.match(carrier,/DIRECT PARTICIPATION THROUGH THIS STATIC APERTURE IS CLOSED/);
  assert.match(carrier,/without identity, membership, JavaScript, approval or covenant\s+acceptance/);
  assert.match(carrier,/issues no capability|No capability is issued/i);
  assert.match(carrier,/operator-mediated(?: YAC)? return/i);
  assert.match(carrier,/not direct admission/i);
  assert.match(carrier,/decline, or leave/);
  assert.doesNotMatch(carrier,/<script|<form|#invite=|localhost|127\.0\.0\.1/i);
  assert.match(carrier,/yac-thr-disposable-pilot\.mecchanical-ethics\.workers\.dev\/start\.txt/);
 }
});

test('YAC offers independently addressable public THR source fallback when the THR custom domain is inaccessible',async()=>{
 const door=await readFile('out/explore/yac/index.html','utf8');
 const intro=await readFile('out/explore/yac/start.txt','utf8');
 const window=await readFile('out/explore/yac/thr/index.html','utf8');
 const records=["https://github.com/markgoodbody-bit/human-record/blob/main/specimen.md","https://github.com/markgoodbody-bit/human-record/blob/main/cases/viral-flak-claim.md","https://github.com/markgoodbody-bit/human-record/blob/main/cases/sieve-riddle-revival.md","https://github.com/markgoodbody-bit/human-record/blob/main/cases/hannibal-barca.md"];
 for(const route of records){
  for(const carrier of [door,intro,window])assert.ok(carrier.includes(route), 'missing independent fallback: '+route);
 }
 assert.match(door,/current repository files, not byte-frozen snapshots/);
 assert.match(intro,/Current-main fallbacks are not byte-pinned snapshots/);
});

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


test('one-file project packet names the current released core versions',async()=>{
 const packet=await readFile('out/packet.md','utf8');
 assert.match(packet,/released TRACE v0\.4\.0 formal baseline and current compact specification/);
 assert.match(packet,/TRACE v0\.3\.0 is preserved as the previous released formal baseline and full technical donor\/reference/);
 assert.match(packet,/released Mechanical Ethics v0\.8\.0 formal baseline and current reader/);
 assert.match(packet,/Mechanical Ethics v0\.7\.0 is preserved as the previous released baseline/);
 assert.doesNotMatch(packet,/released TRACE v0\.3\.0 formal baseline and current specification/);
 assert.doesNotMatch(packet,/released Mechanical Ethics v0\.7\.0 formal baseline and current reader/);
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

 const sourceHtml=await readFile('out/explore/sources.html','utf8');
 const sourceMd=await readFile('out/explore/sources.md','utf8');
 const packetMd=await readFile('out/explore/packet.md','utf8');
 for(const humanPage of [sourceHtml,sourceMd,packetMd]){
   assert.match(humanPage,new RegExp(sources['trace-home'].commit));
   assert.match(humanPage,new RegExp(sources['me-home'].commit));
   assert.match(humanPage,new RegExp(sources.trace.commit));
   assert.match(humanPage,new RegExp(sources.me.commit));
   assert.doesNotMatch(humanPage,/8310d2531d3b2fe4e3b44c92d1d544a322f52bf4/);
   assert.doesNotMatch(humanPage,/25a9d793af1cded26dd2d766e1d1c08e1b30f652/);
 }

 const manifest=JSON.parse(await readFile('out/manifest.json','utf8'));
 const traceRepo=manifest.source_repositories.find(x=>x.name==='TRACE');
 const meRepo=manifest.source_repositories.find(x=>x.name==='Mechanical Ethics');
 assert.equal(traceRepo.human_preview_source_revision,'46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b');
 assert.equal(meRepo.human_preview_source_revision,'44f7efb59806242fd26c572cbfbaaeaefaea2058');
});

test('selection separates sender activity from evidence of external encounter',async()=>{
 const md=await readFile('out/explore/nodes/selection.md','utf8');
 const node=JSON.parse(await readFile('out/explore/nodes/selection.json','utf8'));
 const rendered=await readFile('out/explore/nodes/selection.html','utf8');
 const packetMd=await readFile('out/explore/packet.md','utf8');
 const packet=JSON.parse(await readFile('out/explore/packet.json','utf8'));
 const packetSelection=packet.nodes.find(x=>x.id==='selection');
 assert.ok(packetSelection,'packet selection node missing');
 const required=/sender-side activity, not by itself an external encounter/;
 const silence=/silence does not prove non-reading/;
 const bounded=/one trace does not establish reach beyond that encounter/;
 for(const carrier of [md,node.challenge,rendered,packetMd,packetSelection.challenge]){
   assert.match(carrier,required);
   assert.match(carrier,silence);
   assert.match(carrier,bounded);
 }
});

test('correction binds the effective copy and verifies receipt',async()=>{
 const md=await readFile('out/explore/nodes/correction.md','utf8');
 const node=JSON.parse(await readFile('out/explore/nodes/correction.json','utf8'));
 const rendered=await readFile('out/explore/nodes/correction.html','utf8');
 const packetMd=await readFile('out/explore/packet.md','utf8');
 const packet=JSON.parse(await readFile('out/explore/packet.json','utf8'));
 const packetCorrection=packet.nodes.find(x=>x.id==='correction');
 assert.ok(packetCorrection,'packet correction node missing');
 const target=/version or copy that people and processes actually rely on/;
 const sendBoundary=/Sending a correction does not show that target changed/;
 const receipt=/target copy or a receiving-side receipt/;
 for(const carrier of [md,node.detail,rendered,packetMd,packetCorrection.detail]){
   assert.match(carrier,target);
   assert.match(carrier,sendBoundary);
   assert.match(carrier,receipt);
 }
});

test('root metadata names only the first-party canonical origin',()=>{
 assert.match(html,/<link rel="canonical" href="https:\/\/pleasestartfromhere.com\/"/);
 for(const field of ['title','description','url','type'])assert.equal((html.match(new RegExp('property="og:'+field+'"','g'))||[]).length,1);
});

test('current history and edition agree',async()=>{
 const m=JSON.parse(await readFile('out/manifest.json'));
 assert.equal(m.site_edition,'0.8.54');
 assert.equal(m.updated,'2026-09-30');
 const md=await readFile('out/changes.md','utf8');
 const rendered=await readFile('out/changes.html','utf8');
 assert.match(md,/### D097\s+30 September 2026/);
 assert.match(rendered,/<h3 id="d097">D097<\/h3>/);
 assert.match(md,/### D096\s+30 September 2026/);
 assert.match(rendered,/<h3 id="d096">D096<\/h3>/);
 assert.match(md,/### D095\s+30 September 2026/);
 assert.match(rendered,/<h3 id="d095">D095<\/h3>/);
 assert.match(md,/### D094\s+30 September 2026/);
 assert.match(rendered,/<h3 id="d094">D094<\/h3>/);
 assert.match(md,/### D093\s+30 September 2026/);
 assert.match(rendered,/<h3 id="d093">D093<\/h3>/);
 assert.match(md,/### D092\s+29 September 2026/);
 assert.match(rendered,/<h3 id="d092">D092<\/h3>/);
 assert.match(md,/### D091\s+29 September 2026/);
 assert.match(rendered,/<h3 id="d091">D091<\/h3>/);
 for(const [id,date] of [['D090','28 September 2026'],['D089','27 September 2026'],['D088','27 September 2026'],['D087','25 September 2026'],['D086','25 September 2026'],['D085','25 September 2026'],['D084','23 September 2026'],['D083','23 September 2026'],['D082','23 September 2026'],['D081','23 September 2026'],['D080','23 September 2026'],['D079','23 September 2026'],['D078','23 September 2026'],['D077','23 September 2026'],['D076','23 September 2026'],['D075','23 September 2026'],['D074','23 September 2026'],['D073','23 September 2026'],['D072','18 September 2026'],['D071','18 September 2026'],['D070','18 September 2026'],['D069','18 September 2026'],['D068','15 September 2026']]){
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
